# DynamoDB Setup
Explanation for how to set up AWS DynamoDB with the CodeReviewBot.

## Create AWS Educate Starter Account
Sign up for the account by going [here](https://aws.amazon.com/education/awseducate/)
and click "Join AWS Educate". Click "Student". 

Fill out the form with the appropriate data and click "Next". Agree to the terms and conditions.

You should receive an email asking to verify your email address. Make sure to do this.

Now you must wait for AWS Educate to review your application, which may take up to 48 hours. However, it may take as little as a few minutes. 

Once your application has been approved, you will receive another email detailing how to set up your account. Follow the instructions to set up a username and password. 

After your account has been created, nagivate to the [AWS Educate Starter Account homepage](https://www.awseducate.com/student/s/awssite). Click "AWS Educate Starter Account" to launch a Vocareum Workbench. Vocareum is the starting point to access all AWS features. **I recommend bookmarking this page.**

## Connecting AWS Educate with CodeReviewBot Repository
On the Vocareum Workbench page, click the blue button named "Account Details". Click "Show" next to AWS CLI. You will see the `aws_access_key_id`, `aws_secret_access_key`, and `aws_session_token`. 

Do **NOT** copy and paste these credentials into ~/.aws/credentials. Instead, copy and paste each credential into `config.json` in the `CAM2CodeReviewBot` Repository. There should a placeholder for each of these fields.

#### Important Notes
* These credentials will expire after 3 hours. You will need to update them in `config.json` after they expire.
* Even though CAM2CodeReviewBot is a private repository, please do **NOT** commit these credentials.

## Accessing DynamoDB on AWS and Viewing the Tables
On the Vocareum Workbench page, click the orange button named "AWS Console". In the top left-hand corner, click the "Services" button and search for "DynamoDB".

When running `cam2-code-review-bot.py` for the first time, 3 tables - `Defects`, `Issues`, and `Reviewers` - will be created with the appropriate primary key(s). You will now be able to see each of the tables and their elements.

## Using Database Methods
For each table in the database, there is corresponding file that contains methods to create, get, and update entries in the database. I have only included examples for the Defect table functions because the other functions work in a similar format.
Each of the functions will return `-1` if the inputs are formatted incorrectly or the wrong type is used, or it will return `0` if the function returns successfully. The getter functions will return `None` if there is no entry in the table with the corresponding key.

### defect.py

#### Create
```python
createDefect( 
    { 
        'defect_number': NUMBER, 
        'file_name': "String", 
        'description': "String", 
        'line_numbers': [Array of NUMBER], 
        'code_segments': [Array of "String"] 
    }
)
```

##### Example:
```python
createDefect( 
    { 
        'defect_number': 1, 
        'file_name': "example.py", 
        'description': "example defect", 
        'line_numbers': [1, 2, 3], 
        'code_segments': ['first line of code', 'second line of code', 'third line of code']
    } 
)
```

#### Get
`getDefect( defect_number )`

##### Example:
`getDefect( 1 )`

#### Update
```python
updateDefect( 
    defect_number, 
    { 
        'file_name': "String", 
        'description': "String", 
        'line_numbers': [Array of NUMBER], 
        'code_segments': [Array of "String"]
    } 
)
```

##### Example:
```python
updateDefect(
    1, 
    { 
        'file_name': "updatedExample.py", 
        'description': "updated example description", 
        'line_numbers': [4, 5, 6], 
        'code_segments': ['fourth line of code', 'fifth line of code', 'sixth line of code']
    }
)
```

**Note:** All attributes except `defect_number` are optional. If an updated value of an attribute is not provided, the existing value of the attribute will remain the same. 

### issue.py

#### Create
```python
createIssue( 
    { 
        'issue_number': NUMBER, 
        'reviewers': [Array of github_username], 
        'changed_files': [Array of "String"], 
        'parent_issue': issue_number, 
        'child_issues': [Array of issue_number], 
        'documentation_defects': [Array of defect_number], 
        'logic_defects': [Array of defect_number]
    }
)
```

#### Get
`getIssue( issue_number )`

#### Update
```python
updateIssue( 
    issue_number, 
    { 
        'reviewers': [Array of github_username], 
        'changed_files': [Array of "String"], 
        'parent_issue': issue_number, 
        'child_issues': [Array of issue_number], 
        'documentation_defects': [Array of defect_number], 
        'logic_defects': [Array of defect_number] 
    }
)
```

**Note:** All attributes except `issue_number` are optional. If an updated value of an attribute is not provided, the existing value of the attribute will remain the same.

### reviewer.py

#### Create
```python
createReviewer( 
    { 
        'github_username': "String",
        'issue_number': NUMBER, 
        'role': "String", 
        'role_description': "String" 
    } 
)
```

#### Get
`getReviewer( github_username, issue_number )`

#### Update
```python
updateReviewer( 
    github_username,
    issue_number,
    { 
        'role': "String", 
        'role_description': "String"
    }
)
```

**Note:** All attributes except `github_username` and `issue_number` are optional (both form the primary key). If an updated value of an attribute is not provided, the existing value of the attribute will remain the same.

## Issues or Questions?
If you experience any issues or have any questions, please DM David Wood on Slack or email him at wood154@purdue.edu.