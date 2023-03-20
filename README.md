# aws-boto3-scripts
Python3 scripts to manage AWS using the boto3 SDK


# Installation
Requires Python3 and [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#installation)

```
pip install -r requirements.txt
```

If you are using a workstation with no IAM roles access, you will need to set the AWS credentials from an IAM user.

For MacOS or Linux, use:

```
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_REGION=your_aws_region
```

For Windows, use:

```
set AWS_ACCESS_KEY_ID=your_access_key_id
set AWS_SECRET_ACCESS_KEY=your_secret_access_key
set AWS_REGION=your_aws_region
```


# Usage

## ec2_imds.py
This script will change the [IMDS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html) version ("required" is IMDSv2) based on the Tags set in the script. Single or multiple tag values are allowed.

#Edit script as needed

```python
#Changes EC2 instances to use IMDSv2 ("required") with the tag 'Environment' set to 'Dev' and 'UAT'
ec2_imds("required","Environment", "Dev", "UAT")
```
Run script after edit

```
python3 ec2_imds.py
```

## drs_recover_tag.py
This script will recover any replicated servers in Elastic Disaster Recovery (DRS) based on the tag key and value provided.

#Edit script as needed

```python
#Provide the tag key and value to get the Source Server IDs based on the tags
servers = get_tag('Application','Test')
#Run the recover_server function to recover the servers returned from the get_tag function
recover_server(servers)
```
Run script after edit

```
python3 drs_recover_tag.py
```

## drs_ebs_check.py
This script will compare the amount of replicated disks per server in DRS to the number of EBS volumes attached to the source server. If they don't match, it will run an SSM command to reinstall the agent to allow for the new volume to be replicated.

This is to be used with Install-DRSAgent.yml, which is to be deployed as an SSM Command document.