from flask import Flask
import boto.route53
from boto.route53.record import ResourceRecordSets
ZONE_ID = 'NEED TO CHANGE LATER' #k8s secret later
DNS = 'example.com' # need to get from secret later
NODE_IP = '123.1.1' # need to get from k8s secret later
app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
    data = request.data
    branch = data.branch
    conn = boto.route53.connect_to_region('us-west-2')
    change_set = ResourceRecordSets(conn, ZONE_ID)
    changes1 = change_set.add_change("UPSERT", branch + DNS, type="CNAME", ttl=1000)
    changes1.add_value(NODE_IP)
    change_set.commit()

@app.route('/healthCheck')
def healthz():
    return "OK"



if __name__ == "__main__":
    app.run()
