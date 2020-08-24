from artifact_lib import get_latest_artifact_url
import requests


# https://github.com/YatopiaMC/Yatopia
OWNER="YatopiaMC"
REPO="Yatopia"
# BRANCH="ver/1.16.2"
WORKFLOW_NAME="Yatopia Build Script"
WORKFLOW_EVENT="push"
# ARTIFACT_NAME="Yatopia-14"

def test_rate():
    url = "https://api.github.com/rate_limit"
    response = requests.get(url)
    json = response.json()
    remaining = json['resources']['core']['remaining']
    return remaining

if test_rate() == 0:
    print("Sorry, it seems like you've reached your api rate limit!")
    print("I recommend you wait a bit, and rerun this program.")
    exit(1)

def list_branches():
    url = "https://api.github.com/repos/{}/{}/branches".format(OWNER, REPO)
    response = requests.get(url)
    json = response.json()
    branches = []
    for ele in json:
        target = ele['name']
        if "ver/" in target:
            branches.append(target)
    return branches


artifact_dict = dict()

artifact_name_list = ["Yatopia-8", "Yatopia-11", "Yatopia-14"]
# branch_list = ["ver/1.16.2", "ver/1.16.1"]
branch_list = list_branches()


for BRANCH in branch_list:
    artifact_dict[BRANCH] = dict()
    for ARTIFACT_NAME in artifact_name_list:
        if ARTIFACT_NAME == "Yatopia-8":
            artifact_dict[BRANCH]["java-8"] = get_latest_artifact_url(WORKFLOW_NAME, WORKFLOW_EVENT, ARTIFACT_NAME, OWNER, REPO, BRANCH)
        elif ARTIFACT_NAME == "Yatopia-11":
            artifact_dict[BRANCH]["java-11"] = get_latest_artifact_url(WORKFLOW_NAME, WORKFLOW_EVENT, ARTIFACT_NAME, OWNER, REPO, BRANCH)
        elif ARTIFACT_NAME == "Yatopia-14":
            artifact_dict[BRANCH]["java-14"] = get_latest_artifact_url(WORKFLOW_NAME, WORKFLOW_EVENT, ARTIFACT_NAME, OWNER, REPO, BRANCH)

print(artifact_dict)