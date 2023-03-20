import boto3
client = boto3.client('drs')
ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')

#Compares list of ebs volumes being replicated in DRS to the amount of ebs volumes attached to the source EC2 instance
ec2_id = []
paginator = client.get_paginator('describe_source_servers')
page = paginator.paginate()
source = [servers['sourceServerID'] for repl in page for servers in repl['items']]
response = client.describe_source_servers(filters={'sourceServerIDs': source })
for i in response['items']:
    id = i['sourceProperties']['identificationHints']
    ebs = ec2.describe_instances(InstanceIds=[id['awsInstanceID']])
    if len(ebs['Reservations'][0]['Instances'][0]['BlockDeviceMappings']) == len(i['sourceProperties']['disks']):
        print('The server ' + id['awsInstanceID'] + ' has ' + str(len(i['sourceProperties']['disks'])) + ' disks replicated and ' + str(len(ebs['Reservations'][0]['Instances'][0]['BlockDeviceMappings'])) + ' disks attached.')
    else:
        ec2_id.append((id['awsInstanceID']))
        print(id['awsInstanceID'] + ' server is out of sync. Reinstalling the DRS Agent')

#If the returned list has any entries, this will kick off an SSM doc to reinstall the DRS agent to allow the new volume to be replicated
if len(ec2_id) > 0:
    ssm.send_command(
        InstanceIds=ec2_id,
        DocumentName='Install-DRSAgent',
        DocumentVersion='$LATEST',
        TimeoutSeconds=600
    )