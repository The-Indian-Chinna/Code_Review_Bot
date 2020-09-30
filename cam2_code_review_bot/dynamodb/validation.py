import logging


#### DEFECTS ####

# Checks if primary key (defect number) is an integer
def isDefectKeyValid(defectNumber):
    valid = True

    if not isinstance(defectNumber, int):
        logging.error("Please use an integer for the defect number")
        valid = False

    return valid


# Checks if attributes are formatted correctly and are the correct types
def isDefectAttributesValid(defect):
    valid = True

    if "file_name" in defect.keys():
        if not isinstance(defect["file_name"], str):
            logging.error("Please use a string for the file name")
            valid = False

    if "description" in defect.keys():
        if not isinstance(defect["description"], str):
            logging.error("Please use a string for the description")
            valid = False

    if "line_numbers" in defect.keys():
        if not isinstance(defect["line_numbers"], list):
            logging.error("Please use a correctly formatted [Array] of line numbers")
            valid = False
        else:
            for ln in defect["line_numbers"]:
                if not isinstance(ln, int):
                    logging.error("Please use an integer for each line number")
                    valid = False

    if "code_segments" in defect.keys():
        if not isinstance(defect["code_segments"], list):
            logging.error("Please use a correctly formatted [Array] of code segments")
            valid = False
        else:
            for cs in defect["code_segments"]:
                if not isinstance(cs, str):
                    logging.error("Please use a string for each code segment")
                    valid = False

    return valid


#### ISSUES ####

# Checks if primary key (issue number) is an integer
def isIssueKeyValid(issueNumber):
    valid = True

    if not isinstance(issueNumber, int):
        logging.error("Please use an integer for the issue number")
        valid = False

    return valid


# Checks if attributes are formatted correctly and are the correct types
def isIssueAttributesValid(issue):
    valid = True

    if "reviewers" in issue.keys():
        if not isinstance(issue["reviewers"], list):
            logging.error("Please use a correctly formatted [Array] of reviewers")
            valid = False
        else:
            for rv in issue["reviewers"]:
                if not isinstance(rv, str):
                    logging.error("Please use a string for each reviewer")
                    valid = False

    if "changed_files" in issue.keys():
        if not isinstance(issue["changed_files"], list):
            logging.error("Please use a correctly formatted [Array] of changed files")
            valid = False
        else:
            for cf in issue["changed_files"]:
                if not isinstance(cf, str):
                    logging.error("Please use a string for each changed file")
                    valid = False

    if "parent_issue" in issue.keys():
        if not isinstance(issue["parent_issue"], int):
            logging.error("Please use an integer for the parent issue")
            valid = False

    if "child_issues" in issue.keys():
        if not isinstance(issue["child_issues"], list):
            logging.error("Please use a correctly formatted [Array] of child issues")
            valid = False
        else:
            for ci in issue["child_issues"]:
                if not isinstance(ci, int):
                    logging.error("Please use an integer for each child issue number")
                    valid = False

    if "documentation_defects" in issue.keys():
        if not isinstance(issue["documentation_defects"], list):
            logging.error("Please use a correctly formatted [Array] of documentation defects")
            valid = False
        else:
            for dd in issue["documentation_defects"]:
                if not isinstance(dd, int):
                    logging.error("Please use an integer for each documentation defect number")
                    valid = False

    if "logic_defects" in issue.keys():
        if not isinstance(issue["logic_defects"], list):
            logging.error("Please use a correctly formatted [Array] of logic defects")
            valid = False
        else:
            for ld in issue["logic_defects"]:
                if not isinstance(ld, int):
                    logging.error("Please use an integer for each logic defect number")
                    valid = False

    return valid


#### REVIEWERS ####

# Checks if primary keys (GitHub username and issue number) are the correct types
def isReviewerKeyValid(githubUsername, issueNumber):
    valid = True

    if not isinstance(githubUsername, str):
        logging.error("Please use a string for the GitHub username")
        valid = False

    if not isinstance(issueNumber, int):
        logging.error("Please use an integer for the issue number")
        valid = False

    return valid


# Checks if attributes are formatted correctly and are the correct types
def isReviewerAttributesValid(reviewer):
    valid = True

    if "role" in reviewer.keys():
        if not isinstance(reviewer["role"], str):
            logging.error("Please use a string for the role")
            valid = False

    if "role_description" in reviewer.keys():
        if not isinstance(reviewer["role_description"], str):
            logging.error("Please use a string for the role description")
            valid = False

    return valid
