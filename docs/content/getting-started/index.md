---
title: Getting Started
weight: 10
---

## Pre Requisites

1. AWS account with IAM set up. you will need the key + secret from IAM
2. A Kubernetes Cluster. (kops , kubeadm or plain ol minikube) + general understanding of getting around K8s.
3. Ingress set up in your cluster + AWS Route53  DNS pointing to your cluster
4. *only if using kubeadm* SSH into the machine with kubectl set up
5. *optional* a “bot” github account with personal access token set up

## Get the code

> git clone https://github.com/lilnate22/Crows-Nest.git

## Edit Yamls

### Next Edit the **yamls/deployment.yaml** file with the relevant config params in the environment section
{{< note title="Note" >}} for our example, we will use “Github” as the CROW_REPO. and the CROW_DNS will be “natefonseka.tech” and CROW_NODE_IP = “123.45.67". Refer to the [Environment section](/#environment-variables) for possible environment values and their purpose. and replace the above values with your values when following the example. {{< /note >}}

after editing the yamls, deploy the deployment, and service

>kubectl create -f yamls/deployment.yaml
>kubectl create -f yamls/service.yaml

You should now see crows-nest deployment, and a service running on a NodePort. we need to get this NodePort to test if everything is running OK

>kubectl get svc crows-nest

![](https://cdn-images-1.medium.com/max/1600/1*rfFLOND5BZlFSiiY3P_ZnQ.png)

>curl {YOUR_NODE_IP}:{NODE_PORT}/healthCheck

>following example: (curl 123.45.67:31250/healthCheck)

**Congrats! you now have Crows-nest Running!**

## Configure Git Webhook
You can follow the guide for setting up the webhook [for GitHub Here](https://support.hockeyapp.net/kb/third-party-bug-trackers-services-and-webhooks/how-to-set-up-a-webhook-in-github) or [gitlab here](https://docs.gitlab.com/ce/user/project/integrations/webhooks.html)
{{<note title="Note">}}the payload url should be {YOUR_NODE_IP}:{NODE_PORT}

example: http://123.45.67:31250{{</note>}}

## Configure Docker Hub integration

We will also need to set up Docker hub integration with github. which you can follow HERE. this will make it so that images are built automatically when branches are pushed.

**All Done! You should now have a project ready to go with crows nest**