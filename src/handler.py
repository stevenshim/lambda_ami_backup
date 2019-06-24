import os

import boto3

from EC2 import EC2
from Image import Image

ec2_client = boto3.client('ec2', 'ap-northeast-2')
ec2_res = boto3.resource('ec2', 'ap-northeast-2')
tag_key = os.environ.get('TAG_KEY', 'Backup')
tag_value = os.environ.get('TAG_VALUE', 'by_lambda')

def _ami_backup():
    ec2_filtered = EC2().filter(tag_key=tag_key, tag_value=tag_value)
    ec2_info: list = ec2_filtered.get_instance_ids_and_names()

    image = Image()
    for ec2 in ec2_info:
        name = ec2.get('instance_name')
        ec2_id = ec2.get('instance_id')
        image.bake(ec2_id=ec2_id, name=name)


def _ami_delete():
    image = Image().filter()
    image.delete_amis()


def lambda_handler(event, context):
    _ami_backup()
    _ami_delete()

    return {
        'statusCode': 200,
        'body': 'Create AMI backup requested.'
    }
