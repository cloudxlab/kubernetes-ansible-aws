## This document guides how to practice different kind of Ingress services.

Before starting this, make sure you have set up the nginx ingress controller using setup-nginx-ingress-controller.md

To start with, verify that nginx ingress controller is running fine. You should see LoadBalancer service ingress-nginx-controller.

```console
kubectl get svc -n ingress-nginx -o wide
```

#### Single service ingress
It shows very simple ingress - one url serving only one path.

Apply below deployment and service file, and verify that the app is accessible on service clusterip.

```console
kubectl apply -f flask-app.yml
kubectl apply -f flask-svc-ingress.yml
kubectl get deploy
kubectl get pod
kubectl get svc
cluster_ip=$(kubectl get svc flask-svc-ingress -ojsonpath='{.spec.clusterIP}')
curl $cluster_ip:4080
```

Now, create the Ingress and verify the status. Ingress may not the get the address right away, so wait for sometime.

```console
kubectl apply -f flask-ingress.yml
kubectl get ingress
```

Output may look like this:
```
NAME                         CLASS   HOSTS                               ADDRESS                      PORTS   AGE
flask-ingress                nginx   flask.app.com                       172.31.43.13,172.31.44.126   80      19m
```

Address of the ingress should match with the externalIPs entered during nginx ingress controller set up.

Now, ingress controller is ready to accept the connections from outside the world.
If master/worker machines added in externalIPs have public IPs, then add below entry into /etc/hosts or C:\Windows\System32\drivers\etc\hosts of your own machine or any other external machine exposed to internet.

Entries to be added will be like this:
```
13.127.76.200 flask.app.com
13.233.138.225 flask.app.com
```

Open the brower on external machine and enter the url - flask.app.com/v1 \
It should open the sample app running inside the Kubernetes cluster.

#### Fanout ingress
It shows multiple path ingress - one url serving mutiple paths which are serving different services or apps.

We will start another deployment with version 2 of the app and one more service to serve the version 2 of the apps.
```console
kubectl apply -f flask-app-v2.yml
kubectl apply -f flask-svc-ingress-v2.yml
kubectl get deploy
kubectl get pod
kubectl get svc
cluster_ip=$(kubectl get svc flask-svc-ingress-v2 -ojsonpath='{.spec.clusterIP}')
curl $cluster_ip:4080
```

Note that curl will show version 2 of the app.

Now, delete the previous ingress as new ingress will be using old as well as new path.
```console
kubectl delete ingress flask-ingress
```

Now, create new ingress having 2 paths.

```console
kubectl apply -f flask-ingress-fanout.yml
kubectl get ingress
```

Output may look like this. Wait for the address to be populated if blank.
```
NAME                   CLASS   HOSTS                         ADDRESS                      PORTS   AGE
flask-ingress-fanout   nginx   flask.app.com,flask.app.com   172.31.43.13,172.31.44.126   80      27s
```

Open the brower on external machine where you had added entries into hosts file and enter the url - flask.app.com/v1 or flask.app.com/v2 \
It should open the respective version of the app running inside the Kubernetes cluster.

#### Virtual Hosting ingress
It shows multiple hostnames ingress - mutiple hosts serving mutiple services or apps.

Create new ingress having 2 hosts.

```console
kubectl apply -f flask-ingress-virtual-host.yml
kubectl get ingress
```

Output may look like this. Wait for the address to be populated if blank.
```
NAME                   CLASS   HOSTS                         ADDRESS                      PORTS   AGE
flask-ingress-virtual-host   nginx   v1.flask.app.com,v2.flask.app.com   172.31.43.13,172.31.44.126   80      16s
```

Add entries for 2 hostnames into hosts file on the external machine.
Entries will be like this:
```
13.233.138.225 v1.flask.app.com
13.127.76.200 v2.flask.app.com
```
Open the brower on external machine and enter the url - v1.flask.app.com or v2.flask.app.com \
It should open the respective version of the app running inside the Kubernetes cluster.
