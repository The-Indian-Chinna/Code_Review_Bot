import boto3
import json
import logging
from os import path, getenv
from cam2_code_review_bot.dynamodb.validation import isDefectKeyValid, isDefectAttributesValid
from cam2_code_review_bot.dynamodb.entry_count import incrementDefectCount, decrementDefectCount

key_id = getenv("AWS_SERVER_PUBLIC_KEY")
access_key = getenv("AWS_SERVER_SECRET_KEY")
session_token = getenv("AWS_SERVER_SESSION_TOKEN")

session = boto3.Session(
    aws_access_key_id=key_id, aws_secret_access_key=access_key, aws_session_token=session_token,
)

# Get the service resource
dynamodb = session.resource("dynamodb", region_name="us-east-1")

# Specify the Defects table
table = dynamodb.Table("Defects")

# Creates Defect table with defect number as partition key
def createDefectsTable():
    try:
        table = dynamodb.create_table(
            TableName="Defects",
            KeySchema=[{"AttributeName": "Defect_Number", "KeyType": "HASH"}],  # Partion key
            AttributeDefinitions=[{"AttributeName": "Defect_Number", "AttributeType": "N"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        table.meta.client.get_waiter("table_exists").wait(TableName="Defects")
    except:
        pass


# Create a new defect
def createDefect(defect):
    if not isDefectKeyValid(defect["defect_number"]) or not isDefectAttributesValid(defect):
        return -1

    response = incrementDefectCount()
    if response != 0:
        return -1
    response = table.put_item(
        Item={
            "Defect_Number": defect["defect_number"],
            "File_Name": defect["file_name"],
            "Description": defect["description"],
            "Line_Numbers": defect["line_numbers"],
            "Code_Segments": defect["code_segments"],
        }
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return 0
    else:
        response = decrementDefectCount()
        if response == -1:
            logging.critical(
                "FAILED TO DECREMENT COUNTER AFTER UNSUCCESSFUL ATTEMPT TO ADD TABLE ENTRY"
            )
        return -1


# Get all fields of a defect based on the defect number
def getDefect(defectNumber):
    if not isDefectKeyValid(defectNumber):
        return -1

    response = table.get_item(Key={"Defect_Number": defectNumber,})
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        if "Item" not in response.keys():
            return None

        item = response["Item"]

        for i in range(len(item["Line_Numbers"])):
            item["Line_Numbers"][i] = int(item["Line_Numbers"][i])

        defect = {
            "defect_number": item["Defect_Number"],
            "file_name": item["File_Name"],
            "line_numbers": item["Line_Numbers"],
            "description": item["Description"],
            "code_segments": item["Code_Segments"],
        }
        return defect
    else:
        return -1


# Update one or more fields on a defect
def updateDefect(defectNumber, updatedDefect):
    if not isDefectKeyValid(defectNumber) or not isDefectAttributesValid(updatedDefect):
        return -1

    currDefect = getDefect(defectNumber)

    filename = (
        updatedDefect["file_name"]
        if "file_name" in updatedDefect.keys()
        else currDefect["file_name"]
    )
    dscrp = (
        updatedDefect["description"]
        if "description" in updatedDefect.keys()
        else currDefect["description"]
    )
    linenum = (
        updatedDefect["line_numbers"]
        if "line_numbers" in updatedDefect.keys()
        else currDefect["line_numbers"]
    )
    codeseg = (
        updatedDefect["code_segments"]
        if "code_segments" in updatedDefect.keys()
        else currDefect["code_segments"]
    )

    response = table.update_item(
        Key={"Defect_Number": defectNumber,},
        UpdateExpression="SET File_Name = :val1, Description = :val2, Line_Numbers = :val3, Code_Segments = :val4",
        ExpressionAttributeValues={
            ":val1": filename,
            ":val2": dscrp,
            ":val3": linenum,
            ":val4": codeseg,
        },
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return 0
    else:
        return -1
