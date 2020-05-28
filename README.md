# kubernates-ansible-aws
This repo installs 3 node Kubernetes cluster on AWS with 1 master and 2 worker 

# Steps to run this repo

# 1.Install the pre-requistes 
./packages.sh

# 2. setup python virual env and activate it
python3 -m venv ansible

source /root/kubernates-ansible-aws/ansible/bin/activate

# 3 Install requirements 

pip install pip --upgrade

pip install -r requirements.txt


# 4. Configure AWS credential - this is needed for dynamic inventory 
aws configure 
OR
EXPORT AWS_KEY_ID = XXXXXXXXXXXXX

EXPORT AWS_SECRET_KEY =XXXXXXXXXX

# 5. Run create Infra for launch master and worked node
ansible-playbook -i inventory  create-infra.yml

# 6. prepare host file from dynamic inventory . Update the alias name
ansible -i ec2-k8.py worker --list | grep -v hosts | awk '{print $1 "   worker"}' > files/hosts 

ansible -i ec2-k8.py master --list | grep -v hosts | awk '{print $1 "   master"}' >> files/hosts 

# 7. Update new hosts in playbooks
Update host in distribute key playbook

ansible -i ec2-k8.py  master --list | grep -v hosts | head -1 | awk '{print "       - "$1}' >> distribute-key.yml

ansible -i ec2-k8.py  worker --list | grep -v hosts | head -1 | awk '{print "       - "$1}' >> distribute-key.yml

# 8 Disribute key on remote hosts
ansible-playbook -i inventory  distribute-key.yml 

# 9. update kube-api-server variable in playbooks

export KUBE_API_SERVER_IP=`ansible -i ec2-k8.py  master --list | grep -v hosts | head -1 | awk '{print $1}'`

sed -ir "s/kube_api_server: ChangeMe/kube_api_server: ${KUBE_API_SERVER_IP}/g" deploy-k8-ubuntu.yml 

sed -ir "s/kube_api_server: ChangeMe/kube_api_server: ${KUBE_API_SERVER_IP}/g" add-node-ubuntu.yml 

# 10. Check ansible ping for all host
ansible -m ping -i ec2-k8.py master

ansible -m ping -i ec2-k8.py worker

# 11. Prepare host for k8 deployment
ansible-playbook -i ec2-k8.py  configue-ubuntu-infra.yml 


# 13. Deploy k8 cluster on master
ansible-playbook -v -i ec2-k8.py deploy-k8-ubuntu.yml 


# 14. Check Master is up and running ok
ansible -m shell -a "kubectl get no" -i ec2-k8.py master --become


# 15. Update token and discovery token in add-node playbook


# 16. Run Add node playbook
ansible-playbook -v -i ec2-k8.py  add-node-ubuntu.yml 


# 17. Check Node is added successfully
ansible -m shell -a "kubectl get no" -i ec2-k8.py master --become

ansible -m shell -a "kubectl get po --all-namespaces" -i ec2-k8.py master --become

