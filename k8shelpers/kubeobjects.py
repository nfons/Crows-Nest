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

K8sIngressObject = {
    "kind": "Ingress",
    "apiVersion": "extensions/v1beta1",
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


def createDeployObject(pod):
    deploy = K8sDeployObject
    deploy["metadata"]["name"] = pod.name
    deploy["spec"]["selector"]["app"] = pod.name
    deploy["template"]["metadata"]["labels"]["app"] = pod.name
    deploy["spec"]["spec"]["containers"]["name"] = pod.name
    deploy["spec"]["spec"]["containers"]["image"] = pod.image
    return deploy


def createIngressObject(pod):
    ingress = K8sIngressObject
    ingress["metadata"]["name"] = pod.name
    ingress["spec"]["rules"][0]["host"] = pod.host
    ingress["spec"]["rules"][0]["http"]["paths"][0]["backend"]["serviceName"] = pod.name
    return ingress



def createSvcObject(pod):
    svc = None
