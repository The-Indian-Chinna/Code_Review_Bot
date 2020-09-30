import boto3
import json
import threading
from os import path, getenv
from cam2_code_review_bot.dynamodb.validation import isDefectKeyValid, isDefectAttributesValid

key_lock = threading.Lock()

key_id = getenv("AWS_SERVER_PUBLIC_KEY")
access_key = getenv("AWS_SERVER_SECRET_KEY")
session_token = getenv("AWS_SERVER_SESSION_TOKEN")

session = boto3.Session(
    aws_access_key_id=key_id, aws_secret_access_key=access_key, aws_session_token=session_token,
)

# Get the service resource
dynamodb = session.resource("dynamodb", region_name="us-east-1")

# Specify the Defects table
table = dynamodb.Table("Entry_Count")

# Creates entry count table to keep track of the number entries in the Defects table
def createEntryCountTable():
    try:
        table = dynamodb.create_table(
            TableName="Entry_Count",
            KeySchema=[{"AttributeName": "Table_Name", "KeyType": "HASH"}],  # Partion key
            AttributeDefinitions=[{"AttributeName": "Table_Name", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        table.meta.client.get_waiter("table_exists").wait(TableName="Entry_Count")

        table.put_item(Item={"Table_Name": "Defects", "Entry_Count": 0})
    except:
        pass


# Increments the number of entries in the Defects table by 1
def incrementDefectCount():
    with key_lock:
        defectCount = getDefectCount() + 1
        response = table.update_item(
            Key={"Table_Name": "Defects",},
            UpdateExpression="SET Entry_Count = :val1",
            ExpressionAttributeValues={":val1": defectCount,},
        )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return 0
    else:
        return -1


# Decrements the number of entries in the Defects table by 1
def decrementDefectCount():
    with key_lock:
        defectCount = getDefectCount() - 1
        response = table.update_item(
            Key={"Table_Name": "Defects",},
            UpdateExpression="SET Entry_Count = :val1",
            ExpressionAttributeValues={":val1": defectCount,},
        )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return 0
    else:
        return -1


# Get the number of defect entries in a table
def getDefectCount():
    response = table.get_item(Key={"Table_Name": "Defects",})
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        count = int(response["Item"]["Entry_Count"])
        return count
    else:
        return -1
