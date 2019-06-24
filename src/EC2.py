import itertools

import boto3


class EC2:
    def __init__(self):
        self.ec2_client = boto3.client('ec2', 'ap-northeast-2')
        self.reservations = None

    def __get_id_and_name(self, instance):
        instance_id = instance['InstanceId']
        instance_name = ''

        for tags in instance.get('Tags', []):
            if 'Name' in tags.get('Key', ''):
                instance_name = tags.get('Value', '')

        return {
            'instance_id': instance_id,
            'instance_name': instance_name
        }

    def get_instance_ids_and_names(self) -> list:
        reserves = self.reservations.get('Reservations', [])
        item = []
        for res in reserves:
            instances = res.get('Instances', [])
            item.append(map(self.__get_id_and_name, instances))

        return list(itertools.chain(*item))

    def filter(self, tag_key: str, tag_value: str) -> 'EC2':
        filters = [{
            'Name': 'tag:' + tag_key, 'Values': [tag_value]
        }]
        print(f'[EC2.filter] filter: {filters}')

        self.reservations = self.ec2_client.describe_instances(Filters=filters)
        return self
