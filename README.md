Crows Nest is a open source project aimed to do rapid CI/CD with Kubernetes by allowing developers to
see feature branches auto-deployed in a testing environment, for better code review
and testing.


Crows Nest will:
* Create k8s deploy + service + ingress rules in your k8s cluster.
* create amazon r53 dns rules to your ingress resources.



### Requirements

* Kubernetes Cluster
* Github/Gitlab (default)
* AWS Route53 (currently only supporting AWS)

## Get started

1. edit the `yamls/deployment.yaml` file with relevant environment values
2. `kubectl create -f yaml/deployment.yaml`
3. `kubectl create -f yaml/service.yaml`

The above steps will create a barebones deployment of Crows Nest, exposed via NodePort. At this point
you can also add an ingress rule if you desire.

To verify crows nest is running:

1. get the NodePort value from crows nest service: `kubectl describe svc crows-nest`
2. curl healthcheck location: `curl {NODE_IP}:{Node_port}/healthCheck` this should return 200 OK
    * node ip = your cluster ip (you can use master ip)

Once you have a deployment up and running, next we need to set up the PR/MR webhooks
from either [gitlab](https://docs.gitlab.com/ce/user/project/integrations/webhooks.html) or [github](https://developer.github.com/webhooks/creating/)
for the url, choose `{node_ip}:{node_port}` of you crows-nest deployment. set method to `POST` and content-type to `json`

Congrats! you now have a working crows-nest.


## Limitations
1. Currently for docker regisry / VCS integration, the namespaces are tightly coupled.
 * that means: if your github repo is `username/reponame`, the docker registry has to also be in the namespace of `username/reponame`
2. Only 1 Node IP is used for the Route53 dns IP.




### TODO:
1. Have crows-nest comment on PR with url to see feature branch