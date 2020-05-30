import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch

# Enable trace by x-ray
libraries = (['botocore'])
patch(libraries)

# サンプルアプリのため固定値
USER_ID = "17b09832-2f24-4ff4-9456-f12d54d20071"

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("tasks_management_table")
    response = table.query(KeyConditionExpression=Key("user_id").eq(USER_ID))
    items = response["Items"]

    res_data = {}
    for item in items:
        del item['update_date']
        if res_data.get(item["status"]) is None:
            res_data[item["status"]] = []
        res_data[item["status"]].append(item)
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": json.dumps(res_data),
    }
