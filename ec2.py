#!/bin/python
import boto3
import json
def get_hosts(ec2,fv):
   f={'Name':'tag:Ansible','Values':[fv]}
   hosts=[]
   for each_in in ec2.instances.filter(Filters=[f]):
       print(each_in.private_ip_address)

def main():
   ec2=boto3.resource("ec2")
   db_group=get_hosts(ec2,"db")
   app_group=get_hosts(ec2,"App")


if __name__=="__main__":
 main()
