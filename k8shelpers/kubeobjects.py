K8sDeployObject = {
    "apiVersion": "extensions/v1beta1",
    "kind": "Deployment",
    "metadata": {
        "name": "CHANGE",
        "namespace": "default"
    },
    "spec": {
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
                        ],
                        "imagePullPolicy": "Always"
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
        "namespace": "default"
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
    "apiVersion": "v1",
    "kind": "Service",
    "metadata": {
        "name": "CHANGE",
        "namespace": "default"
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
            "app": "CHANGE"
        }
    }
}


def createDeployObject(pod, delete=False):
    deploy = K8sDeployObject
    deploy["metadata"]["name"] = pod["name"]
    deploy["spec"]["template"]["metadata"]["labels"]["app"] = pod["name"]
    deploy["spec"]["template"]["spec"]["containers"][0]["name"] = pod["name"]
    deploy["spec"]["template"]["spec"]["containers"][0]["image"] = pod["image"]
    if delete:
        deploy["spec"]["replicas"] = 0
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
    svc["spec"]["selector"]["app"] = pod["name"]
    return svc
