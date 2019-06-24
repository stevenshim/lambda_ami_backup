import operator
import os
from datetime import datetime

import boto3

TAG_KEY = os.environ.get('TAG_KEY', 'Backup')
TAG_VALUE = os.environ.get('TAG_VALUE', 'by_lambda')
MAX_RESERVED_COUNT = int(os.environ.get('MAX_RESERVED_COUNT', 5))


class Image:
    def __init__(self):
        self.ec2_client = boto3.client('ec2', 'ap-northeast-2')
        self.ec2_res = boto3.resource('ec2', 'ap-northeast-2')
        self.amis: list = []
        self.amis_to_delete: dict = {}

    def bake(self, ec2_id: str, name: str) -> None:
        now = datetime.now().strftime("%Y-%m-%dT%H-%M")
        image_name = f'auto_backup_{name}_{now}'

        ami: dict = self.ec2_client.create_image(
            NoReboot=True,
            Name=image_name,
            Description=f'Instance {name} - automated daily AMI backup by lambda.',
            InstanceId=ec2_id
        )

        image = self.ec2_res.Image(ami.get('ImageId', ''))

        if image:
            image.create_tags(
                Tags=[
                    {'Key': 'Name', 'Value': image_name},
                    {'Key': TAG_KEY, 'Value': TAG_VALUE},
                    {'Key': 'Image_group', 'Value': name},
                ]
            )

        print(f'created: {ami.get("ImageId", "")}')

    def filter(self) -> 'Image':
        filters = [
            {
                'Name': f'tag:{TAG_KEY}', 'Values': [TAG_VALUE]
            }
        ]
        filtered_amis = self.ec2_client.describe_images(Filters=filters)
        self.amis = filtered_amis.get('Images', '')
        return self

    def delete_amis(self):
        self.__get_ami_group_by_tag_name()

        for group_name, images in self.amis_to_delete.items():
            if (len(images)) > MAX_RESERVED_COUNT:
                images.sort(key=operator.itemgetter('CreationDate'), reverse=True)
                images_to_delete = images[MAX_RESERVED_COUNT:]
                self.__delete_amis(images_to_delete)

    def __delete_amis(self, images_to_delete):
        for img in images_to_delete:
            image_id = img['ImageId']
            print(f'This {image_id} is deleted.')
            self.ec2_client.deregister_image(ImageId=image_id)

    def __get_ami_group_by_tag_name(self):
        for img in self.amis:
            group_name = self.__get_tag_value_with_key(img['Tags'], 'Image_group')

            if group_name not in self.amis_to_delete:
                self.amis_to_delete[group_name] = []

            self.amis_to_delete[group_name].append({
                'ImageId': img['ImageId'],
                'CreationDate': img['CreationDate']
            })

    def __get_tag_value_with_key(self, tags, key):
        for key_value in tags:
            if key in key_value.get('Key', ''):
                return key_value.get('Value', '')
