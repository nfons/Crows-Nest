from flask import Flask
from flask import request
import logging as log
import boto.route53
import os
from boto.route53.record import ResourceRecordSets
from k8shelpers.kubehelper import kubecluster, createStack, deleteStack
import pykube
ZONE_ID = os.environ['CROW_ZONE_ID']  # k8s secret later
DNS = os.environ['CROW_DNS']  # need to get from secret later
NODE_IP = os.environ['CROW_NODE_IP']  # need to get from k8s secret later
AWS_REGION = os.getenv('AWS_REGION', 'us-west-2')
app = Flask(__name__)
conn = boto.route53.connect_to_region(AWS_REGION)
change_set = ResourceRecordSets(conn, ZONE_ID)
KUBE_CONF = os.getenv('KUBECONF', "")


@app.route('/', methods=['POST'])
def main():
    data = request.json
    branch = data["object_attributes"]["source_branch"]
    action = data["object_attributes"]["state"]
    if action == 'opened' or action == 'reopened':
        log.info('PR opened, creating DNS records + k8s deploy for branch' + branch)
        opened(branch)
    elif action == 'closed':
        log.info('PR closed, deleting DNS records + k8s deploy for branch' + branch)
        closed(branch)
    elif action == 'updated':
        log.info('PR has been updated, updating deployment' + branch)
    return 'OK'


def opened(branch):
    '''
     We will 1st need to create a deployment with branch image
     then we will need to create a svc for it + ingress rules
     finally create a r53 record
    '''
    changes1 = change_set.add_change("UPSERT", branch + '.' + DNS, type="A", ttl=300)
    changes1.add_value(NODE_IP)
    change_set.commit()
    pod = {
        "name": branch,
        "image": branch,
        "host": branch + '.' + DNS
    }
    # runs through the create stack process
    createStack(pod)


def closed(branch):
    '''
    We will need to get ingress, and then remove the ingress rule for this dns.
    delete deployments from this branch, as well as remove r53 record
    '''
    changes1 = change_set.add_change("DELETE", branch + '.' + DNS, type="A", ttl=300)
    changes1.add_value(NODE_IP)
    change_set.commit()

    pod = {
        "name": branch,
        "image": branch,
        "host": branch + '.' + DNS
    }

    # runs through the create stack process
    deleteStack(pod)


@app.route('/healthCheck')
def healthz():
    return "OK"


@app.route('/deploy')
def createDeploy():
    pod = {
        "name": "hello-minikube",
        "image": "gcr.io/google_containers/echoserver:1.4"
    }
    k8s = kubecluster(pod, KUBE_CONF)
    k8s.createDeploy()
    k8s.createSvc()
    return "Created"


@app.route('/delDeploy')
def deleteDeploy():
    pod = {
        "name": "hello-minikube",
        "image": "gcr.io/google_containers/echoserver:1.4"
    }
    k8s = kubecluster(pod, KUBE_CONF)
    k8s.deleteDeploy()
    return 'deleted'


if __name__ == "__main__":
    app.run()
