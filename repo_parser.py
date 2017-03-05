def gitlab(payload):
    object = {}
    branch = payload["object_attributes"]["source_branch"]
    action = payload["object_attributes"]["state"]
    image = payload["object_attributes"]["source"]["path_with_namespace"]
    object["image"] = image
    object["action"] = action
    object["branch"] = branch
    return object

def github(payload):
    object = {}
    return object

def getRepo(type, payload):
    if type == 'github':
       return github(payload)
    else:
        return gitlab(payload)