import boto3


class EC2TagFilter:
    tag_key = ''
    tag_value = ''
    filter = []
    ec2_client = object

    def __init__(self, tag_key, tag_value):
        self.tag_value = tag_key
        self.tag_value = tag_value
        self.ec2_client = boto3.client('ec2', 'ap-northeast-2')
        self.__init_filter()

    def __init_filter(self):
        self.filters = [{
            'Name': 'tag:' + self.tag_key, 'Values': [self.tag_value]
        }]

    def do_filter(self):
        return self.ec2_client.describe_instances(Filters=self.filter)
