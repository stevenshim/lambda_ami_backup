import os

import boto3

from EC2Filter import EC2Filter
from Image import Image

ec2_client = boto3.client('ec2', 'ap-northeast-2')
ec2_res = boto3.resource('ec2', 'ap-northeast-2')
tag_key = os.environ.get('TAG_KEY', 'Backup')
tag_value = os.environ.get('TAG_VALUE', 'by_lambda')


def lambda_handler(event, context):
    ec2_filter = EC2Filter(tag_key=tag_key, tag_value=tag_value)
    ec2_info: list = ec2_filter.get_instance_ids_and_names()
    print(f'ec2_info: {ec2_info}')

    baker = Image()
    for ec2 in ec2_info:
        name = ec2.get('instance_name')
        ec2_id = ec2.get('instance_id')
        baker.bake(ec2_id=ec2_id, name=name)

    return {
        'statusCode': 200,
        'body': 'Create AMI backup requested.'
    }
