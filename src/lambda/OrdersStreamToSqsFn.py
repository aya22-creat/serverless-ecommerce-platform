import json
import os
import boto3

from boto3.dynamodb.types import TypeDeserializer

sqs = boto3.client("sqs")
deserializer = TypeDeserializer()

QUEUE_URL = os.environ["QUEUE_URL"]


def lambda_handler(event, context):

    records = event.get("Records", [])

    print("Received records:", len(records))

    for record in records:

        if record.get("eventName") != "INSERT":
            continue

        new_image = record["dynamodb"]["NewImage"]

        outbox_event = {
            key: deserializer.deserialize(value)
            for key, value in new_image.items()
        }

        message = {
            "eventId": outbox_event["eventId"],
            "orderId": outbox_event["orderId"],
            "eventType": outbox_event["eventType"],
            "paymentStatus": outbox_event["paymentStatus"],
            "amount": str(outbox_event["amount"])
        }

        response = sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(message)
        )

        print("Message sent to SQS:", response["MessageId"])

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Outbox events sent to SQS"
        })
    }
