import itertools
import os
from datetime import datetime

import boto3

from src.EC2TagFilter import EC2TagFilter

ec2_client = boto3.client('ec2', 'ap-northeast-2')
ec2_res = boto3.resource('ec2', 'ap-northeast-2')
tag_key = os.environ.get('TAG_KEY', 'Backup')
tag_value = os.environ.get('TAG_VALUE', 'by_lambda')


def _get_instance_id_and_name(instance):
    instance_name = ''
    instance_id = instance['InstanceId']

    for key_value in instance['Tags']:
        if 'Name' in key_value.get('Key', ''):
            instance_name = key_value.get('Value', '')

    return {
        'instance_id': instance_id,
        'instance_name': instance_name
    }


def _get_instance_id_and_name_list(reservations) -> map:
    ids_names = map(lambda res: map(_get_instance_id_and_name, res['Instances']), reservations['Reservations'])
    chain = itertools.chain(*ids_names)
    return list(chain)


def _create_ec2_ami(inst_ids_names):
    for inst in inst_ids_names:
        instance_name = inst['instance_name']
        date_now = datetime.now().strftime("%Y-%m-%dT%H-%M")
        image_name = f'auto_backup_{instance_name}_{date_now}'

        image_info = ec2_client.create_image(
            NoReboot=True,
            Name=image_name,
            Description=f'Instance {instance_name} - automated daily AMI backup by lambda.',
            InstanceId=inst['instance_id']
        )

        image = ec2_res.Image(image_info['ImageId'])
        image.create_tags(
            Tags=[
                {'Key': 'Name', 'Value': image_name},
                {'Key': 'Auto_backup', 'Value': 'yes'},
                {'Key': 'Image_group', 'Value': instance_name},
            ]
        )


def lambda_handler(event, context):
    filter_generator = EC2TagFilter(tag_key=tag_key, tag_value=tag_value)
    reservations = filter_generator.do_filter()

    instance_ids_names = _get_instance_id_and_name_list(reservations)

    _create_ec2_ami(instance_ids_names)

    return {
        'statusCode': 200,
        'body': 'Create AMI backup requested.'
    }
