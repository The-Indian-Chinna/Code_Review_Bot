import boto3
import json
from os import path, getenv
from cam2_code_review_bot.dynamodb.validation import isReviewerKeyValid, isReviewerAttributesValid

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "..", "config.json"))

key_id = getenv("AWS_SERVER_PUBLIC_KEY")
access_key = getenv("AWS_SERVER_SECRET_KEY")
session_token = getenv("AWS_SERVER_SESSION_TOKEN")

session = boto3.Session(
    aws_access_key_id=key_id, aws_secret_access_key=access_key, aws_session_token=session_token,
)

# Get the service resource
dynamodb = session.resource("dynamodb", region_name="us-east-1")

# Specify the Reviewer table
table = dynamodb.Table("Reviewers")

# Creates Reviewer table with GitHub username as partition key and issue number as sort key
def createReviewersTable():
    try:
        table = dynamodb.create_table(
            TableName="Reviewers",
            KeySchema=[
                {"AttributeName": "Github_Username", "KeyType": "HASH"},  # Partion key
                {"AttributeName": "Issue_Number", "KeyType": "RANGE"},  # Sort key
            ],
            AttributeDefinitions=[
                {"AttributeName": "Github_Username", "AttributeType": "S"},
                {"AttributeName": "Issue_Number", "AttributeType": "N"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        table.meta.client.get_waiter("table_exists").wait(TableName="Reviewers")
    except:
        pass


# Create a new reviewer
def createReviewer(reviewer):
    if not isReviewerKeyValid(
        reviewer["github_username"], reviewer["issue_number"]
    ) or not isReviewerAttributesValid(reviewer):
        return -1

    response = table.put_item(
        Item={
            "Github_Username": reviewer["github_username"],
            "Issue_Number": reviewer["issue_number"],
            "Role": reviewer["role"],
            "Role_Description": reviewer["role_description"],
        }
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return 0
    else:
        return -1


# Get all fields of a reviewer based on the github username
def getReviewer(githubUsername, issueNumber):
    if not isReviewerKeyValid(githubUsername, issueNumber):
        return -1

    response = table.get_item(Key={"Github_Username": githubUsername, "Issue_Number": issueNumber})
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        if "Item" not in response.keys():
            return None

        item = response["Item"]
        reviewer = {
            "github_username": item["Github_Username"],
            "issue_number": item["Issue_Number"],
            "role": item["Role"],
            "role_description": item["Role_Description"],
        }
        return reviewer
    else:
        return -1


# Update one or more fields on a reviewer
def updateReviewer(githubUsername, issueNumber, updatedReviewer):
    if not isReviewerKeyValid(githubUsername, issueNumber) or not isReviewerAttributesValid(
        updatedReviewer
    ):
        return -1

    currReviewer = getReviewer(githubUsername, issueNumber)

    currReviewer["role"].extend(updatedReviewer["role"])
    rl = currReviewer["role"]
    currReviewer["role_description"].extend(updatedReviewer["role_description"])
    rldescrp = currReviewer["role_description"]

    response = table.update_item(
        Key={"Github_Username": githubUsername, "Issue_Number": issueNumber},
        UpdateExpression="SET Role = :val1, Role_Description = :val2",
        ExpressionAttributeValues={":val1": rl, ":val2": rldescrp,},
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return 0
    else:
        return -1
