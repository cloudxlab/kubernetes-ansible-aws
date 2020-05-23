#!/bin/bash
yum install git -y
sudo su - 
git clone https://github.com/singh-ashok25/kubernates-ansible-aws.git
curl https://raw.githubusercontent.com/ansible/ansible/stable-2.9/contrib/inventory/ec2.ini -o /etc/ansible/ec2.ini
