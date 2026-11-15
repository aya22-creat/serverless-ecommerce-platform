import json
import os
import boto3

from datetime import datetime, timezone
from botocore.exceptions import ClientError
from boto3.dynamodb.types import TypeDeserializer


# DynamoDB client for transactional operations
dynamodb = boto3.client("dynamodb")

# DynamoDB resource for reading existing items
dynamodb_resource = boto3.resource("dynamodb")

orders_table_name = os.environ["ORDERS_TABLE"]
outbox_table_name = os.environ["OUTBOX_TABLE"]

orders_table = dynamodb_resource.Table(orders_table_name)
outbox_table = dynamodb_resource.Table(outbox_table_name)

deserializer = TypeDeserializer()


def lambda_handler(event, context):

    records = event.get("Records", [])

    print("Received records:", len(records))

    for record in records:

        # Process only newly inserted orders
        if record.get("eventName") != "INSERT":
            print("Skipping event:", record.get("eventName"))
            continue

        # Read the new order data from DynamoDB Stream
        new_image = record["dynamodb"]["NewImage"]

        order = {
            key: deserializer.deserialize(value)
            for key, value in new_image.items()
        }

        order_id = order["orderId"]
        amount = order["amount"]

        print("Processing order:", order_id)
        print("Order amount:", amount)

        # Simulate successful payment
        payment_status = "PAID"

        timestamp = datetime.now(timezone.utc).isoformat()

        # Stable event ID prevents duplicate Outbox events
        event_id = f"PAYMENT#{order_id}"

        try:

            # Update the order and create the Outbox event
            # in one atomic DynamoDB transaction
            dynamodb.transact_write_items(

                TransactItems=[

                    {
                        "Update": {
                            "TableName": orders_table_name,

                            "Key": {
                                "orderId": {
                                    "S": order_id
                                }
                            },

                            "UpdateExpression": (
                                "SET #status = :paid, "
                                "paymentProcessedAt = :time"
                            ),

                            "ConditionExpression": (
                                "#status = :pending"
                            ),

                            "ExpressionAttributeNames": {
                                "#status": "status"
                            },

                            "ExpressionAttributeValues": {
                                ":paid": {
                                    "S": payment_status
                                },
                                ":pending": {
                                    "S": "PENDING_PAYMENT"
                                },
                                ":time": {
                                    "S": timestamp
                                }
                            }
                        }
                    },

                    {
                        "Put": {
                            "TableName": outbox_table_name,

                            "Item": {
                                "eventId": {
                                    "S": event_id
                                },

                                "orderId": {
                                    "S": order_id
                                },

                                "eventType": {
                                    "S": "PAYMENT_COMPLETED"
                                },

                                "paymentStatus": {
                                    "S": payment_status
                                },

                                "amount": {
                                    "N": str(amount)
                                },

                                "createdAt": {
                                    "S": timestamp
                                }
                            },

                            "ConditionExpression": (
                                "attribute_not_exists(eventId)"
                            )
                        }
                    }

                ]
            )

            print(
                f"SUCCESS: Order {order_id} updated to PAID "
                "and Outbox event created."
            )

        except dynamodb.exceptions.TransactionCanceledException:

            # Check whether this order was already processed
            order_response = orders_table.get_item(
                Key={"orderId": order_id}
            )

            existing_order = order_response.get("Item", {})

            outbox_response = outbox_table.get_item(
                Key={"eventId": event_id}
            )

            existing_event = outbox_response.get("Item")

            # Both records exist: this is a duplicate delivery
            if (
                existing_order.get("status") == "PAID"
                and existing_event is not None
            ):
                print(
                    f"Order {order_id} was already processed. "
                    "Skipping duplicate event."
                )
                continue

            # Something else caused the transaction to fail
            print(
                f"Transaction failed for order {order_id}. "
                f"Current order: {existing_order}, "
                f"Outbox event exists: {existing_event is not None}"
            )

            raise

        except ClientError as error:

            print(
                "DynamoDB error:",
                error.response["Error"]["Message"]
            )

            raise

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Payment processing completed"
        })
    }
