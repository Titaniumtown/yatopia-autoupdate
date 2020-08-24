from artifact_lib import get_latest_artifact_url
import requests
from my_python_lib.my_library import run_command
from bs4 import BeautifulSoup
from lxml import html
import urllib.request
import bs4 as bs

def list_branches(OWNER, REPO):
    url = "https://api.github.com/repos/{}/{}/branches".format(OWNER, REPO)
    response = requests.get(url)
    json = response.json()
    branches = []
    for ele in json:
        target = ele['name']
        if "ver/" in target and target != "ver/1.15.2":
            branches.append(target)
    return branches


def artifact_func():
    # https://github.com/YatopiaMC/Yatopia
    OWNER="YatopiaMC"
    REPO="Yatopia"

    WORKFLOW_NAME="Yatopia Build Script"
    WORKFLOW_EVENT="push"
    verbose = False
    



    artifact_dict = dict()

    artifact_name_list = ["Yatopia-8", "Yatopia-11", "Yatopia-14"]
    # branch_list = ["ver/1.16.2", "ver/1.16.1"]
    branch_list = list_branches(OWNER, REPO)

    est_requests = int(3*len(artifact_name_list)*len(branch_list))
    print("running this command will use", str(est_requests), "requests to the github api")

    for BRANCH in branch_list:
        artifact_dict[BRANCH] = dict()
        for ARTIFACT_NAME in artifact_name_list:
            if ARTIFACT_NAME == "Yatopia-8":
                artifact_dict[BRANCH]["java-8"] = get_latest_artifact_url(WORKFLOW_NAME, WORKFLOW_EVENT, ARTIFACT_NAME, OWNER, REPO, BRANCH, verbose)
            elif ARTIFACT_NAME == "Yatopia-11":
                artifact_dict[BRANCH]["java-11"] = get_latest_artifact_url(WORKFLOW_NAME, WORKFLOW_EVENT, ARTIFACT_NAME, OWNER, REPO, BRANCH, verbose)
            elif ARTIFACT_NAME == "Yatopia-14":
                artifact_dict[BRANCH]["java-14"] = get_latest_artifact_url(WORKFLOW_NAME, WORKFLOW_EVENT, ARTIFACT_NAME, OWNER, REPO, BRANCH, verbose)

    return artifact_dict

#My attempt to just parse the html and not use the github api
def artifact_func_2():
    OWNER="YatopiaMC"
    REPO="Yatopia"
    url = "https://github.com/%s/%s/actions" % (OWNER, REPO)
    # r = requests.get(url)
    source = urllib.request.urlopen(url).read()
    # print(source)

    def get_run_branch(url):
        source = urllib.request.urlopen(url).read()
        soup = bs.BeautifulSoup(source, 'lxml')
        for url in soup.find_all('a'):
            href = url.get('href')
            if "/%s/%s/compare/" % (OWNER, REPO) in href:
                return href.replace("/%s/%s/compare/" % (OWNER, REPO), "")
    branch_list = list_branches(OWNER, REPO)

    soup = bs.BeautifulSoup(source, 'lxml')
    list_runs = []
    runs_dict = {}
    
    for BRANCH in branch_list:
        runs_dict[BRANCH] = dict()
    
    runs_num_list = []
    for url in soup.find_all('a'):
        href = str(url.get('href'))
        if "actions/runs" in href and "/workflow" not in href:
            run_num = href.replace(str(OWNER+"/"+REPO+"/actions/runs/"), '').replace('/', '')
            # print(run_num)
            runs_num_list.append(run_num)
    

    for run_num in runs_num_list:
        url = str("https://www.github.com/"+OWNER+"/"+REPO+"/actions/runs/"+run_num)
        # print(url)
        output_branch = get_run_branch(url)
        
        if output_branch in branch_list:
            list_runs.append(run_num)

    del runs_num_list
    

    organized_run_list = []
    for BRANCH in branch_list:
        organized_run_list[BRANCH] = list()

    for run_num in list_runs:
        url = str("https://www.github.com/"+OWNER+"/"+REPO+"/actions/runs/"+run_num)
        output_branch = get_run_branch(url)
        organized_run_list[output_branch].append(run_num)

    




    
    print(organized_run_list)