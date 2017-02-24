K8sDeployObject = {
    "apiVersion": "v1",
    "kind": "Deployment",
    "metadata": {
        "name": "CHANGE",
    },
    "spec": {
        "replicas": 1,
        "selector": {
            "app": "CHANGE"
        },
        "template": {
            "metadata": {
                "labels": {
                    "app": "CHANGE"
                }
            },
            "spec": {
                "containers": [
                    {
                        "name": "CHANGE",
                        "image": "CHANGE",
                        "ports": [
                            {"containerPort": 8080}
                        ]
                    }
                ]
            }
        }
    }
}

def createDeployObject(pod):
    deploy = K8sDeployObject
    deploy["metadata"]["name"] = pod.name
    deploy["spec"]["selector"]["app"] = pod.name
    deploy["template"]["metadata"]["labels"]["app"] = pod.name
    deploy["spec"]["spec"]["containers"]["name"] = pod.name
    deploy["spec"]["spec"]["containers"]["image"] = pod.image

def createIngressObject(pod):
    ingress = None

def createSvcObject(pod):
    svc = None


