import json
import os
import uuid
import boto3
from datetime import datetime, timezone

# Connect to DynamoDB
dynamodb = boto3.resource("dynamodb")

# Read table name from environment variables
table = dynamodb.Table(os.environ["ORDERS_TABLE"])


def lambda_handler(event, context):

    try:
        # Read order data from API request
        body = json.loads(event.get("body", "{}"))

        # Generate a unique order ID
        order_id = str(uuid.uuid4())

        # Create order item
        order = {
            "orderId": order_id,
            "status": "PENDING_PAYMENT",
            "amount": body["amount"],
            "createdAt": datetime.now(timezone.utc).isoformat()
        }

        # Save order in DynamoDB
        table.put_item(Item=order)

        # Return successful response
        return {
            "statusCode": 201,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Order created successfully",
                "order": order
            })
        }

    except (KeyError, json.JSONDecodeError, TypeError):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Invalid order data. Amount is required."
            })
        }

    except Exception as e:
        print(f"Error creating order: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal server error"
            })
        }
