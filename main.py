from artifact_lib import get_latest_artifact_url



# https://github.com/YatopiaMC/Yatopia
OWNER="YatopiaMC"
REPO="Yatopia"
# BRANCH="ver/1.16.2"
WORKFLOW_NAME="Yatopia Build Script"
WORKFLOW_EVENT="push"
# ARTIFACT_NAME="Yatopia-14"

artifact_dict = {'ver/1.16.2' : {'java-8':'', 'java-11':'', 'java-14':''},
                 'ver/1.16.1' : {'java-8':'', 'java-11':'', 'java-14':''}}

artifact_name_list = ["Yatopia-8", "Yatopia-11", "Yatopia-14"]
branch_list = ["ver/1.16.2", "ver/1.16.1"]

for BRANCH in branch_list:
    for ARTIFACT_NAME in artifact_name_list:
        if ARTIFACT_NAME == "Yatopia-8":
            artifact_dict[BRANCH]["java-8"] = get_latest_artifact_url(WORKFLOW_NAME, WORKFLOW_EVENT, ARTIFACT_NAME, OWNER, REPO, BRANCH)
        elif ARTIFACT_NAME == "Yatopia-11":
            artifact_dict[BRANCH]["java-11"] = get_latest_artifact_url(WORKFLOW_NAME, WORKFLOW_EVENT, ARTIFACT_NAME, OWNER, REPO, BRANCH)
        elif ARTIFACT_NAME == "Yatopia-14":
            artifact_dict[BRANCH]["java-14"] = get_latest_artifact_url(WORKFLOW_NAME, WORKFLOW_EVENT, ARTIFACT_NAME, OWNER, REPO, BRANCH)

print(artifact_dict)