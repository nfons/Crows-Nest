from flask import Flask
from flask import request
import logging as log
import yaml
import sys
import boto.route53
import os
from commentModule import comment
from repo_parser import getRepo
from boto.route53.record import ResourceRecordSets
from k8shelpers.kubehelper import kubecluster, createStack, deleteStack, updateStack
from configParser import ConfigParser
import json


ZONE_ID = os.getenv('CROW_ZONE_ID', None)  # k8s secret later
DNS = os.getenv('CROW_DNS', None)  # need to get from secret later
NODE_IP = os.getenv('CROW_NODE_IP', None)  # need to get from k8s secret later
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
CROW_REGISTRY = os.getenv('CROW_REGISTRY', None)
KUBE_CONF = os.getenv('KUBECONF', None)
CROW_REPO = os.getenv("CROW_REPO", "github")
DNS_TYPE = 'A'
CROW_RAW_REPO = os.getenv("CROW_RAW_REPO", "https://raw.githubusercontent.com")
PROJECT_PORTS = {}

root = log.getLogger()
root.setLevel(log.INFO)

ch = log.StreamHandler(sys.stdout)
ch.setLevel(log.DEBUG)
formatter = log.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

app = Flask(__name__)
conn = boto.route53.connect_to_region(AWS_REGION)


@app.route('/', methods=['POST'])
def main():
    data = request.json
    parsed_data = getRepo(CROW_REPO, data)
    configUrl = CROW_RAW_REPO + '/' + parsed_data['image'] + '/' + parsed_data['branch'] + '/crow.yaml'
    config = ConfigParser(configUrl).getConfig()
    startCrow(parsed_data, config)
    return 'OK'


@app.route('/pipeline', methods=['POST'])
def pipeline_endpoint():
    data = request.json
    parsed_data = getRepo('pipeline', data)
    configUrl = parsed_data['config']
    config = ConfigParser(configUrl).getConfig()
    startCrow(parsed_data, config)
    return 'OK'

def startCrow(parsed_data, config):
    # set the config params to our variables
    global NODE_IP, DNS, ZONE_ID, DNS_TYPE

    port = config['port'] if 'port' in config else 8080
    zone = config['zone'] if 'zone' in config else ZONE_ID
    dns = config['dns'] if 'dns' in config else DNS
    ip = config['ip'] if 'ip' in config else NODE_IP
    dns_type = config['recordType'] if 'recordType' in config else 'A'

    parsed_data['port'] = port


    parsed_data['url'] = parsed_data['branch'] + '.' + dns

    if parsed_data['action'] == 'opened' or parsed_data['action'] == 'reopened':
        log.info('PR opened, creating DNS records + k8s deploy for branch' + parsed_data['branch'])
        opened(parsed_data['branch'], parsed_data['image'], parsed_data['port'], zone, dns, dns_type, ip)
        if ('comment_url' in parsed_data):
            comment(parsed_data)
    elif parsed_data['action'] == 'closed':
        log.info('PR closed, deleting DNS records + k8s deploy for branch' + parsed_data['branch'])
        closed(parsed_data['branch'], parsed_data['port'], zone, dns, dns_type, ip)
    elif parsed_data['action'] == 'updated' or parsed_data['action'] == 'synchronize':
        log.info('PR has been updated, updating deployment' + parsed_data['branch'])
        resync(parsed_data['branch'], parsed_data['image'], parsed_data['port'])


def opened(branch, image, port=8080, ZONE_ID=ZONE_ID, DNS=DNS, DNS_TYPE='A', NODE_IP=NODE_IP):
    '''
     We will 1st need to create a deployment with branch image
     then we will need to create a svc for it + ingress rules
     finally create a r53 record
    '''
    change_set = ResourceRecordSets(conn, ZONE_ID)
    changes1 = change_set.add_change("UPSERT", branch + '.' + DNS, type=DNS_TYPE, ttl=60)
    changes1.add_value(NODE_IP)
    change_set.commit()
    # need to change the pod stuff to be a bit more dynamic...
    pod = {
        "name": branch,
        "host": branch + '.' + DNS,
        "port": port
    }

    if (CROW_REGISTRY == None):
        pod['image'] = image + ':' + branch
    else:
        pod['image'] = CROW_REGISTRY + image + ':' + branch
    # runs through the create stack process
    createStack(pod, KUBE_CONF)


def closed(branch, port=8080, ZONE_ID=ZONE_ID, DNS=DNS, DNS_TYPE='A', NODE_IP=NODE_IP):
    '''
    We will need to get ingress, and then remove the ingress rule for this dns.
    delete deployments from this branch, as well as remove r53 record
    '''
    change_set = ResourceRecordSets(conn, ZONE_ID)
    changes1 = change_set.add_change("DELETE", branch + '.' + DNS, type=DNS_TYPE, ttl=60)
    changes1.add_value(NODE_IP)
    change_set.commit()

    pod = {
        "name": branch,
        "image": 'none',  # dont need image here for deletion
        "host": branch + '.' + DNS,
        "port": port
    }

    # runs through the create stack process
    deleteStack(pod, KUBE_CONF)


def resync(branch,image, port):
    ## no need for r53, we just need to redeploy the deployment
    pod = {
        "name": branch,
        "port": port
    }

    if (CROW_REGISTRY == None):
        pod['image'] = image + ':' + branch
    else:
        pod['image'] = CROW_REGISTRY + image + ':' + branch

    # update the deployment
    updateStack(pod, KUBE_CONF)


@app.route('/healthCheck')
def healthz():
    return "OK"


@app.route('/getProjects')
def getProjects():
    return json.dumps(PROJECT_PORTS)


@app.route('/setProjects', methods=['POST'])
def setProjects():
    data = request.json
    PROJECT_PORTS.update(data)
    return json.dumps(PROJECT_PORTS)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    log.info('Crows Nest Running')
