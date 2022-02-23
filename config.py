
import boto3
import tensorflow_hub as hub
import flask

class NstappConfig:
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nstapp'
    hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    s3 = boto3.client('s3', aws_access_key_id='AKIAWFK2LWOXX23LBLE4', aws_secret_access_key='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', region_name='ap-northeast-2')

