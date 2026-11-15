import json
import os
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["ORDERS_TABLE"])


def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        path_parameters = event.get("pathParameters") or {}
        order_id = path_parameters.get("orderId")

        if not order_id:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Missing order ID"
                })
            }

        response = table.get_item(
            Key={"orderId": order_id}
        )

        order = response.get("Item")

        if not order:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": "Order not found"
                })
            }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(order, default=str)
        }

    except Exception as e:
        print("ERROR:", repr(e))

        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal server error"
            })
        }
