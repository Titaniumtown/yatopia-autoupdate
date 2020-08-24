from artifact_lib import get_latest_artifact_url
import requests
from my_python_lib.my_library import run_command

def artifact_func():
    # https://github.com/YatopiaMC/Yatopia
    OWNER="YatopiaMC"
    REPO="Yatopia"

    WORKFLOW_NAME="Yatopia Build Script"
    WORKFLOW_EVENT="push"

    def list_branches():
        url = "https://api.github.com/repos/{}/{}/branches".format(OWNER, REPO)
        response = requests.get(url)
        json = response.json()
        branches = []
        for ele in json:
            target = ele['name']
            if "ver/" in target and target != "ver/1.15.2":
                branches.append(target)
        return branches


    artifact_dict = dict()

    artifact_name_list = ["Yatopia-8", "Yatopia-11", "Yatopia-14"]
    # branch_list = ["ver/1.16.2", "ver/1.16.1"]
    branch_list = list_branches()

    est_requests = int(3*len(artifact_name_list)*len(branch_list))
    print("running this command will use", str(est_requests), "requests to the github api")

    for BRANCH in branch_list:
        artifact_dict[BRANCH] = dict()
        for ARTIFACT_NAME in artifact_name_list:
            if ARTIFACT_NAME == "Yatopia-8":
                artifact_dict[BRANCH]["java-8"] = get_latest_artifact_url(WORKFLOW_NAME, WORKFLOW_EVENT, ARTIFACT_NAME, OWNER, REPO, BRANCH)
            elif ARTIFACT_NAME == "Yatopia-11":
                artifact_dict[BRANCH]["java-11"] = get_latest_artifact_url(WORKFLOW_NAME, WORKFLOW_EVENT, ARTIFACT_NAME, OWNER, REPO, BRANCH)
            elif ARTIFACT_NAME == "Yatopia-14":
                artifact_dict[BRANCH]["java-14"] = get_latest_artifact_url(WORKFLOW_NAME, WORKFLOW_EVENT, ARTIFACT_NAME, OWNER, REPO, BRANCH)

    return artifact_dict