#!/bin/python
import boto3
import json
import pprint
def get_hosts(ec2,fv):
   f={'Name':'tag:node-type','Values':[fv]}
   hosts=[]
   for each_in in ec2.instances.filter(Filters=[f]):
       print(each_in.private_ip_address)
       hosts.append(each_in.private_ip_address)
   return hosts

def main():
   ec2=boto3.resource("ec2")
   master_group=get_hosts(ec2,"master")
   worker_group=get_hosts(ec2,"worker")
   
   all_groups={
	            'master': {
			'hosts': master_group,
			'var': {
			     'group_name': 'k8-master'
                               }
			},
		    'worker': {
			'hosts': worker_group,
			'var': {
			     'group_name': 'k8-node'
                               }
			}
     	      }
   pprint.pprint (all_groups)	
   

if __name__=="__main__":
 main()
 
