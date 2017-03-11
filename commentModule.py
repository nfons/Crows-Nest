import requests
import os
import json
from requests.auth import HTTPBasicAuth

GIT_USER = os.getenv("GIT_USER", None)
GIT_PASS = os.getenv("GIT_PASS", None)
REPO = os.getenv("CROW_REPO", "github")


def comment(data):
    if REPO == 'github':
        github_comment(data)
    else:
        gitlab_comment(data)


def github_comment(data):
    payload = {
        "body": '[' + data['url'] + ']' + '(' + data['url'] + ')'
    }
    requests.post(data['comment_url'], data=json.dumps(payload), auth=HTTPBasicAuth(GIT_USER, GIT_PASS))


def gitlab_comment(data):
    payload = {
        "body": '[' + data['url'] + ']' + '(' + data['url'] + ')'
    }
    headers = {}
    requests.post(data['comment_url'], data=json.dumps(payload), headers=headers)
    return False
