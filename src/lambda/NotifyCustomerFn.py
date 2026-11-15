import json
import os
import boto3

sns = boto3.client("sns")

SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]


def lambda_handler(event, context):

    records = event.get("Records", [])

    print("Received SQS messages:", len(records))

    for record in records:

        message = json.loads(record["body"])

        order_id = message["orderId"]
        event_id = message["eventId"]
        payment_status = message["paymentStatus"]
        amount = message["amount"]

        notification = (
            f"Your order {order_id} has been processed. "
            f"Payment status: {payment_status}. "
            f"Amount: {amount}."
        )

        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Order Payment Update",
            Message=notification,
            MessageAttributes={
                "eventId": {
                    "DataType": "String",
                    "StringValue": event_id
                }
            }
        )

        print(
            f"Notification sent for order {order_id}. "
            f"SNS Message ID: {response['MessageId']}"
        )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Notifications published successfully"
        })
    }
