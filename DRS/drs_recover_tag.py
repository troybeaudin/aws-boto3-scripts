import boto3
client = boto3.client('drs')


#Gets source server IDs from DRS based on tag key and value provided
def get_tag(tag_key, value):
    paginator = client.get_paginator('describe_source_servers')
    page = paginator.paginate()
    source = [servers['sourceServerID'] for repl in page for servers in repl['items']]
    response = client.describe_source_servers(filters={'sourceServerIDs': source })
    sourceids = []
    for src in response['items']:
        try:
            tag = src['tags']
            if tag[tag_key] == value:                                                                                                                                                                                                                                
                sourceids.append(src['sourceServerID'])
        except:
            print('Server ' + src['sourceServerID'] + ' does not have the tag ' + tag_key)
    return sourceids

#Recovers EC2s based on the list provided
def recover_server(source):
    for server in source:
        client.start_recovery(
            isDrill=False,
                sourceServers=[
                    {
                        'sourceServerID': server
                    }
                ]
            )
        
servers = get_tag('Application','Test')
recover_server(servers)