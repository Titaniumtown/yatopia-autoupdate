#!/usr/bin/env python3
import sys
from http.server import BaseHTTPRequestHandler
import requests

API_URL="https://api.github.com"

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

def get_workflow_id(workflow_name, OWNER, REPO):
  response = requests.get("%s/repos/%s/%s/actions/workflows" % (API_URL, OWNER, REPO))
  print(response.status_code)
  json = response.json()
  for workflow in json['workflows']:
    if workflow['name'] == workflow_name:
      print(workflow['name'])
      return workflow['id']
  return None #FIXME: Exception

def get_latest_workflow_run_id(workflow_id, workflow_event, OWNER, REPO, BRANCH):
  response = requests.get("%s/repos/%s/%s/actions/workflows/%s/runs" % (API_URL, OWNER, REPO, workflow_id))
  print(response.status_code)
  json = response.json()
  for workflow_run in json['workflow_runs']:

    # Only consider completed runs
    if workflow_run['status'] != "completed":
      continue
    if workflow_run['conclusion'] != "success":
      continue

    # Match by BRANCH
    if workflow_run['head_branch'] != BRANCH:
      continue

    # Match by event
    if workflow_run['event'] != workflow_event:
      continue

    return workflow_run['id']

  return None #FIXME: Exception

def get_artifact_id(workflow_run_id, name, OWNER, REPO):
  response = requests.get("%s/repos/%s/%s/actions/runs/%s/artifacts" % (API_URL, OWNER, REPO, workflow_run_id))
  print(response.status_code)
  json = response.json()
  for artifact in json['artifacts']:

    # Match by name
    if artifact['name'] == name:
      return artifact['id']

  return None #FIXME: Exception

def get_latest_artifact_url(workflow_name, worfklow_event, artifact_name, OWNER, REPO, BRANCH):

  workflow_id = get_workflow_id(workflow_name, OWNER, REPO)
  print("found workflow %d" % workflow_id)

  workflow_run_id = get_latest_workflow_run_id(workflow_id, worfklow_event, OWNER, REPO, BRANCH)
  print("found workflow_run_id %d" % workflow_run_id)

  artifact_id = get_artifact_id(workflow_run_id, artifact_name, OWNER, REPO)
  print("found artifact_id %d" % workflow_run_id)

  return "%s/repos/%s/%s/actions/artifacts/%s/zip" % (API_URL, OWNER, REPO, artifact_id)