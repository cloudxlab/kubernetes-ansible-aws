# kubernates-ansible-aws
This repo installs 3 node Kubernetes cluster on AWS with 1 master and 2 worker 

# Steps to run this repo

# Install the pre-requistes 
1. ./packages.sh

# setup python virual env 
2.python3 -m venv ansible
3.source /root/aws-ansible/ansible/bin/activate
4. pip install pip --upgrade
5. pip install boto
6. pip install boto3
7. pip install ansible

# Configure AWS credential - this is needed for dynamic inventory 
8. aws configure

# Run create Infra for launch master and worked node
9. ansible-playbook -i inventory  create-infra.yml

# 10 .prepare host file from dynamic inventory . update the alias name
ansible -i ec2-k8.py worker --list | grep -v hosts > files/hosts 
ansible -i ec2-k8.py master --list | grep -v hosts >> files/hosts 

# 11. fetch private key on ansible controller

# 12. Update new hosts in playbooks
cat files/hosts  >> distribute-key.yml 

# 13 Disribute key on remote hosts
ansible-playbook -i inventory  distribute-key.yml 

# 14. Check ansible ping for all host
ansible -m ping -i ec2-k8.py master
ansible -m ping -i ec2-k8.py worker

# 15. Prepare host for k8 deployment
ansible-playbook -i ec2-k8.py  configue-ubuntu-infra.yml 

# 16. 
