def gitlab(payload):
    object = {}
    branch = payload["object_attributes"]["source_branch"]
    action = payload["object_attributes"]["state"]
    image = payload["object_attributes"]["source"]["path_with_namespace"]
    object["image"] = image
    object["action"] = action
    object["branch"] = branch
    # stupid gitab comment_url you have to build by hand
    base_url = payload["object_attributes"]["source"]["web_url"]
    base_url = base_url.replace(image, '')
    merge_request_id = payload["object_attributes"]["id"]
    project_id = payload["object_attributes"]["target_project_id"]
    url = base_url + '/projects/' + project_id + '/merge_requests/' + merge_request_id + '/notes'
    object['comment_url'] = url
    return object


def github(payload):
    object = {}
    branch = payload['pull_request']['head']["ref"]
    image = payload["repository"]["full_name"]
    action = payload["action"]
    object["image"] = image
    object["action"] = action
    object["branch"] = branch
    object["comment_url"] = payload['pull_request']['comments_url']
    return object


def getRepo(type, payload):
    if type == 'github':
        return github(payload)
    else:
        return gitlab(payload)
