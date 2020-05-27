#!/bin/bash
yum install git -y
cd /root/
git clone https://github.com/singh-ashok25/kubernates-ansible-aws.git
./kubernates-ansible-aws/packages.sh
mkdir -p /etc/ansible
curl https://raw.githubusercontent.com/ansible/ansible/stable-2.9/contrib/inventory/ec2.ini -o /etc/ansible/ec2.ini
