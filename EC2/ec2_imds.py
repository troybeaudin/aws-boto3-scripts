#!/usr/bin/python

import boto3

#switches EC2 IMDS version based on Tag

def ec2_imds(token, tag_key, *tag_value):
    client = boto3.client('ec2')
    
    if token not in ['optional', 'required']:
        print("Token needs to be set to 'optional' or 'required'")
    
    
    instance = client.describe_instances(
        Filters=[
            {'Name': 'tag:'+tag_key,
            'Values':list(tag_value)}
            ]
        )
    
    ids = [i['Instances'][0]['InstanceId'] for i in instance['Reservations']]
    for id in ids:
        client.modify_instance_metadata_options(InstanceId=id,HttpTokens=token)
        
#Changes EC2 instances to use IMDSv2 ("required") with the tag 'Environment' set to 'Dev' and 'UAT'
ec2_imds("required","Environment", "Dev", "UAT")