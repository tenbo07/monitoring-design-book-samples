import json
import uuid
import boto3
import datetime
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch

# Enable trace by x-ray
libraries = (['botocore'])
patch(libraries)

# サンプルアプリのため固定値
USER_ID = "17b09832-2f24-4ff4-9456-f12d54d20071"

def lambda_handler(event, context):
    body = json.loads(event["body"])

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("tasks_management_table")

    item = {
        "user_id": USER_ID,
        "task_id": str(uuid.uuid4()),
        "title": body["title"],
        "description": body["description"],
        "due_date": body["due_date"],
        "status": "todo",
        "update_date": int(datetime.datetime.now().timestamp())
    }
    table.put_item(Item=item)
    response = {
        "user_id": item["user_id"],
        "task_id": item["task_id"]
    }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps(response),
    }
