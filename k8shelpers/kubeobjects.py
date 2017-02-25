K8sDeployObject = {
    "apiVersion": "extensions/v1beta1",
    "kind": "Deployment",
    "metadata": {
        "name": "CHANGE",
    },
    "spec": {
        "selector": {
            "matchLabels": {
                "run": "CHANGE"
            }
        },
        "replicas": 1,
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

K8sIngressObject = {
    "apiVersion": "extensions/v1beta1",
    "kind": "Ingress",
    "metadata": {
        "name": "CHANGE",
    },
    "spec": {
        "rules": [
            {
                "host": "CHANGE",
                "http": {
                    "paths": [
                        {
                            "path": "/",
                            "backend": {
                                "serviceName": "CHANGE",
                                "servicePort": 8080
                            }
                        }
                    ]
                }
            }
        ]
    }
}

K8sSvcObject = {
    "apiVersion": "extensions/v1beta1",
    "kind": "Service",
    "metadata": {
        "name": "CHANGE",
    },
    "spec": {
        "type": "NodePort",
        "ports": [
            {
                "port" : 8080,
                "targetPort": 8080
            }
        ],
        "selector": {
            "run": "CHANGE"
        }
    }
}


def createDeployObject(pod):
    deploy = K8sDeployObject
    deploy["metadata"]["name"] = pod["name"]
    deploy["spec"]["template"]["metadata"]["labels"]["app"] = pod["name"]
    deploy["spec"]["template"]["spec"]["containers"][0]["name"] = pod["name"]
    deploy["spec"]["selector"]["matchLabels"]["run"] = pod["name"]
    deploy["spec"]["template"]["spec"]["containers"][0]["image"] = pod["image"]
    return deploy


def createIngressObject(pod):
    ingress = K8sIngressObject
    ingress["metadata"]["name"] = pod["name"]
    ingress["spec"]["rules"][0]["host"] = pod["host"]
    ingress["spec"]["rules"][0]["http"]["paths"][0]["backend"]["serviceName"] = pod["name"]
    return ingress



def createSvcObject(pod):
    svc = K8sSvcObject
    svc["metadata"]["name"] = pod["name"]
    svc["spec"]["selector"]["run"] = pod["name"]
