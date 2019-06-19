from datetime import datetime

import boto3


class Image:
    def __init__(self):
        self.ec2_client = boto3.client('ec2', 'ap-northeast-2')
        self.ec2_res = boto3.resource('ec2', 'ap-northeast-2')
        self.amis = []

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
                    {'Key': 'Auto_backup', 'Value': 'yes'},
                    {'Key': 'Image_group', 'Value': name},
                ]
            )

        self.amis.append(ami)
        print(f'created: {ami.get("ImageId", "")}')
