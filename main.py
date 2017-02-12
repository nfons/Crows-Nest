from flask import Flask
from flask import request
import boto.route53
from boto.route53.record import ResourceRecordSets

ZONE_ID = 'NEED TO CHANGE LATER'  # k8s secret later
DNS = 'example.com'  # need to get from secret later
NODE_IP = '123.1.1'  # need to get from k8s secret later
app = Flask(__name__)
conn = boto.route53.connect_to_region('us-west-2')
change_set = ResourceRecordSets(conn, ZONE_ID)


@app.route('/', methods=['POST'])
def main():
    data = request.json
    branch = data.branch

    action = data.action
    if (action == 'opened' or action == 'reopened'):
        opened(branch)
    elif (action == 'closed'):
        closed(branch);

def opened(branch):
    '''
     We will 1st need to create a deployment with branch image
     then we will need to create a svc for it + ingress rules
     finally create a r53 record
    '''
    changes1 = change_set.add_change("UPSERT", branch + DNS, type="CNAME", ttl=1000)
    changes1.add_value(NODE_IP)
    change_set.commit()

def closed(branch):
    '''
    We will need to get ingress, and then remove the ingress rule for this dns.
    delete deployments from this branch, as well as remove r53 record
    '''
    changes1 = change_set.add_change("DELETE", branch + DNS, type="CNAME", ttl=1000)
    changes1.add_value(NODE_IP)
    change_set.commit()


@app.route('/healthCheck')
def healthz():
    return "OK"


if __name__ == "__main__":
    app.run()
