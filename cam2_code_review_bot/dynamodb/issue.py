import boto3
import json
from os import path, getenv
from cam2_code_review_bot.dynamodb.validation import isIssueKeyValid, isIssueAttributesValid

key_id = getenv("AWS_SERVER_PUBLIC_KEY")
access_key = getenv("AWS_SERVER_SECRET_KEY")
session_token = getenv("AWS_SERVER_SESSION_TOKEN")

session = boto3.Session(
    aws_access_key_id=key_id, aws_secret_access_key=access_key, aws_session_token=session_token,
)

# Get the service resource
dynamodb = session.resource("dynamodb", region_name="us-east-1")

# Specify the Defects table
table = dynamodb.Table("Issues")

# Creates Defect table with defect number as partition key
def createIssuesTable():
    try:
        table = dynamodb.create_table(
            TableName="Issues",
            KeySchema=[{"AttributeName": "Issue_Number", "KeyType": "HASH"}],  # Partion key
            AttributeDefinitions=[{"AttributeName": "Issue_Number", "AttributeType": "N"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        table.meta.client.get_waiter("table_exists").wait(TableName="Issues")
    except:
        pass


# Create a new issue
def createIssue(issue):
    if not isIssueKeyValid(issue["issue_number"]) or not isIssueAttributesValid(issue):
        return -1

    response = table.put_item(
        Item={
            "Issue_Number": issue["issue_number"],
            "Reviewers": issue["reviewers"],
            "Changed_Files": issue["changed_files"],
            "Parent_Issue": issue["parent_issue"],
            "Child_Issues": issue["child_issues"],
            "Documentation_Defects": issue["documentation_defects"],
            "Logic_Defects": issue["logic_defects"],
        }
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return 0
    else:
        return -1


# Get all fields of an issue based on the issue number
def getIssue(issueNumber):
    if not isIssueKeyValid(issueNumber):
        return -1

    response = table.get_item(Key={"Issue_Number": issueNumber,})
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        if "Item" not in response.keys():
            return None

        item = response["Item"]

        item["Parent_Issue"] = int(item["Parent_Issue"])
        for i in range(len(item["Child_Issues"])):
            item["Child_Issues"][i] = int(item["Child_Issues"][i])
        for i in range(len(item["Documentation_Defects"])):
            item["Documentation_Defects"][i] = int(item["Documentation_Defects"][i])
        for i in range(len(item["Logic_Defects"])):
            item["Logic_Defects"][i] = int(item["Logic_Defects"][i])

        issue = {
            "issue_number": item["Issue_Number"],
            "reviewers": item["Reviewers"],
            "changed_files": item["Changed_Files"],
            "parent_issue": item["Parent_Issue"],
            "child_issues": item["Child_Issues"],
            "documentation_defects": item["Documentation_Defects"],
            "logic_defects": item["Logic_Defects"],
        }
        return issue
    else:
        return -1


# Update one or more fields on an issue
def updateIssue(issueNumber, updatedIssue):
    if not isIssueKeyValid(issueNumber) or not isIssueAttributesValid(updatedIssue):
        return -1

    currIssue = getIssue(issueNumber)

    rvwers = (
        updatedIssue["reviewers"] if "reviewers" in updatedIssue.keys() else currIssue["reviewers"]
    )
    chgdfls = (
        updatedIssue["changed_files"]
        if "changed_files" in updatedIssue.keys()
        else currIssue["changed_files"]
    )
    prntiss = (
        updatedIssue["parent_issue"]
        if "parent_issue" in updatedIssue.keys()
        else currIssue["parent_issue"]
    )
    chldiss = (
        updatedIssue["child_issues"]
        if "child_issues" in updatedIssue.keys()
        else currIssue["child_issues"]
    )
    docdef = (
        updatedIssue["documentation_defects"]
        if "documentation_defects" in updatedIssue.keys()
        else currIssue["documentation_defects"]
    )
    logdef = (
        updatedIssue["logic_defects"]
        if "logic_defects" in updatedIssue.keys()
        else currIssue["logic_defects"]
    )

    response = table.update_item(
        Key={"Issue_Number": issueNumber,},
        UpdateExpression="SET Reviewers = :val1, Changed_Files = :val2, Parent_Issue = :val3, Child_Issues = :val4, Documentation_Defects = :val5, Logic_Defects = :val6",
        ExpressionAttributeValues={
            ":val1": rvwers,
            ":val2": chgdfls,
            ":val3": prntiss,
            ":val4": chldiss,
            ":val5": docdef,
            ":val6": logdef,
        },
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return 0
    else:
        return -1
