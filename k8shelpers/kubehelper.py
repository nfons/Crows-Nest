import operator
import pykube
import logging as log
from k8shelpers.kubeobjects import *

class kubecluster:
    def __init__(self, pod, KUBE_CONF):
        self.pod = pod
        self.api = pykube.HTTPClient(pykube.KubeConfig.from_file(KUBE_CONF))

    def createDeploy(self):
        deploy = createDeployObject(self.pod)
        pykube.Deployment(self.api, deploy).create()
        log.info('creating deploy')

    def createIngress(self):
        ingress = createIngressObject(self.pod)
        pykube.Ingress(self.api, ingress).create()
        log.info('creating ingress rules')

    def createSvc(self):
        log.info('creating service')
        svc = createSvcObject(self.pod)
        pykube.Service(self.api, svc).create()

    def deleteDeploy(self):
        # we need to scale the pods to 0, since "delete" doesnt delete pods
        deploy = createDeployObject(self.pod, True)
        pykube.Deployment(self.api, deploy).update()
        pykube.Deployment(self.api, deploy).delete()
        log.info('deleting deploy')

    def deleteIngress(self):
        ingress = createIngressObject(self.pod)
        pykube.Ingress(self.api, ingress).delete()
        log.info('deleteing ingress')

    def deleteSvc(self):
        svc = createSvcObject(self.pod)
        pykube.Service(self.api, svc).delete()
        log.info('delete svc')
'''
Creates a kubernetes stack for a given svc pod.
pod arg must have pod.name = name you want svc...this should be the branch name
pod.image: the image you want to use
pod.dns: dns rule for ingress

The steps are as follows:
create k8s deployment
create k8s svc for deployment
create ingress-rules with dns
'''

def createStack(pod, KUBE_CONF):
    log.info('Creating k8s stack for : '+ pod["name"])
    k8s = kubecluster(pod, KUBE_CONF)
    k8s.createDeploy()
    k8s.createSvc()
    k8s.createIngress()

'''
deletes k8s stack. useful when PR is merged
The steps are as follows:
delete ingress
delete svc
delete deploy
'''
def deleteStack(pod):
    log.info('Deleting k8s stack for :' + pod["name"])


