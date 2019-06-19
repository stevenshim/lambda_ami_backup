import itertools

import boto3


class EC2Filter:

    def __init__(self, tag_key, tag_value):
        self.ec2_client = boto3.client('ec2', 'ap-northeast-2')
        self.reservations = None
        self.filter = None
        self.__init_filter(tag_key, tag_value)
        self.__do_filter()

    def __init_filter(self, tag_key, tag_value):
        self.filter = [{
            'Name': 'tag:' + tag_key, 'Values': [tag_value]
        }]

    def __do_filter(self):
        print(f'[Do_Filter] filter: {self.filter}')
        self.reservations = self.ec2_client.describe_instances(Filters=self.filter)

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
