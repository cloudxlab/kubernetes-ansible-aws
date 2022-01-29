
## Set up Nginx Ingress Controller on bare-metal Kubernetes cluster using Helm 

There are 2 options to set up Nginx Ingress Controller:
1. Using Manifest files

https://docs.nginx.com/nginx-ingress-controller/installation/installation-with-manifests/


2. Using Helm

https://docs.nginx.com/nginx-ingress-controller/installation/installation-with-helm/

This readme is simplified version of the set up process using Helm. Helm is package manager for Kubernetes, similar to yum or apt for OS packages.

### Step 1: Install helm on master node

```console
cd ~/
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
helm version
```

### Step 2: Download nginx controller package code

```console

controller_tag=$(curl -s https://api.github.com/repos/kubernetes/ingress-nginx/releases/latest | grep tag_name | cut -d '"' -f 4)
wget https://github.com/kubernetes/ingress-nginx/archive/refs/tags/${controller_tag}.tar.gz

tar xvf ${controller_tag}.tar.gz

cd ingress-nginx-${controller_tag}

cd charts/ingress-nginx/
```

### Step 3: Set up all nodes to run nginx controller pods

Label nodes that will run ingress controller pods. Later, we can the node selector to define the nodes where ingress controller pods will run.

List the nodes, check their labels, set the label and verify the labels:

```console
kubectl get nodes

kubectl get nodes --show-labels

kubectl get nodes --show-labels -o wide

kubectl label node k8s-master-01 run-nginx-ingress=true

kubectl describe node k8s-master-01
kubectl get nodes --show-labels
```

### Step 4: Configure controller yml

Add tolerations for Master nodes as we want controller to run on master too.

```console
cd ~/ingress-nginx-helm-chart-4.0.16/charts/ingress-nginx/
vi values.yaml
```

Change the the file to look like this below:

```
controller:
  tolerations:
    - key: node-role.kubernetes.io/master
      operator: Equal
      value: "true"
      effect: NoSchedule
    - key: node-role.kubernetes.io/master
      operator: Equal
      effect: NoSchedule
```

Set controller.service.externalIPs:\
This is IP or IPs of master/workers nodes. Traffic from internet DNS will come to one of these IPs. You can put one or more depending on which nodes you want the external traffic come to first. From those hosts, traffic will be routed to other nodes and pods by kube-proxy. 

Say, master has IP of XX.XX.XX.00 and worker 01 has IP of XX.XX.XX.11. Then, in DNS server of AWS Route 53 or any other DNS provider, you will map your user-friendly website name to those IPs.

For example, DNS server mapping might be like below.

XX.XX.XX.00 www.learndevops.com \
XX.XX.XX.11 www.app.learndevops.com

To simukate the DNS server, you can add the entries to /etc/hosts or C:\Windows\System32\drivers\etc\hosts file.

```console
vi values.yaml
```

Add the IPs of master/worker Change the the file to look like this below:

```
controller:
  service:
    externalIPs: [172.31.43.13,172.31.44.126]
```

To set number of replicas of the Ingress controller deployment on controller.replicaCount

```
controller:
  replicaCount: 1
```

If using node selector for pod assignment for the Ingress controller pods set on controller.nodeSelector
```
controller:
  nodeSelector:
    kubernetes.io/os: linux
    run-nginx-ingress: "true"
```

Create a new namespace for nginx container
```console
kubectl create namespace ingress-nginx
```

### Step 5: Deploy Nginx Ingress Controller

Delete any existing set up if needed.
```
kubectl delete deploy ingress-nginx-controller -n ingress-nginx
helm list -A
helm uninstall ingress-nginx -n ingress-nginx
```

```console
helm install -n ingress-nginx ingress-nginx  -f values.yaml .
```

Verify that a service of type LoadBalancer has been created. In the output, under EXTERNAL-IP, you should see all the IPs that you had configured earlier in controller.service.externalIPs.

```console
kubectl get svc -n ingress-nginx -o wide
```
