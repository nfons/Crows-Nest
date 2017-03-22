---
title: Crows Nest
type: index
weight: 9
---
Crows Nest is a open source project aimed to do rapid CI/CD with Kubernetes by allowing developers to
see feature branches auto-deployed in a testing environment, for better code review
and testing.


Crows Nest will:

* Create k8s deploy + service + ingress rules in your k8s cluster.

* create amazon r53 dns rules to your ingress resources.



### Requirements

* Kubernetes Cluster With [Ingress set up](https://github.com/kubernetes/ingress)

* Github (default) /Gitlab

* AWS Route53 (currently only supporting AWS)

## Quick Start
1. edit the `yamls/deployment.yaml` file with relevant environment values
2. `kubectl create -f yaml/deployment.yaml`
3. `kubectl create -f yaml/service.yaml`


## Environment Variables
1. **CROW_REPO**
 * Either "gitlab" or "github" (default). Tells which payload parser to use.
2. **CROW_ZONE_ID**
    * Route53 zone id. can get this from r53 url
3. **CROW_DNS**
 * base url for r53. i.e if your registered dns is "dev.example.com"
4. **AWS_ACCESS_KEY_ID**
 * get from AWS IAM
5. **AWS_SECRET_ACCESS_KEY**
 * get from AWS IAM
6. **AWS_REGION**
 * cluster region: defaults to us-west-2
7. **KUBECONF**
 * Location for kube.conf. REQUIRED if not running inside k8s cluster.
8. **CROW_NODE_IP**
 * IP of the node with an ingress service.
9. **GIT_USER** (optional)
 * Git bot account username
10. **GIT_PASS** (optional)
 * Git bot account access token

## Limitations
1. Currently for docker regisry / VCS integration, the namespaces are tightly coupled.
 * that means: if your github repo is `username/reponame`, the docker registry has to also be in the namespace of `username/reponame`
2. Only 1 Node IP is used for the Route53 dns IP. ideally you want ingress to be a daemon set

