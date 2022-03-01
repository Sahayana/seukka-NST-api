import boto3
import tensorflow_hub as hub
import os
import json


# AWS 보안정보를 따로 관리하기위함 json파일을 불러와서 읽어줌
with open('config.json') as f:
    aws = json.loads(f.read())

AWS_ACCESS_KEY_ID = aws['AWS']['ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = aws['AWS']['SECRET_ACCESS_KEY']


class NstappConfig:
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nstapp'
    hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    s3 = boto3.client('s3', aws_access_key_id= AWS_ACCESS_KEY_ID, aws_secret_access_key= AWS_SECRET_ACCESS_KEY, region_name='ap-northeast-2')

