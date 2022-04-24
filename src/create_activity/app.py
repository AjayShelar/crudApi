import boto3
import os
import json
import uuid
from datetime import datetime


def lambda_handler(message, context):

    if ('body' not in message or message['httpMethod'] != 'POST'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    table_name = os.environ.get('TABLE', 'Applications')
    region = os.environ.get('REGION', 'ap-south-1')
    aws_environment = os.environ.get('AWSENV', 'AWS')

    if aws_environment == 'AWS_SAM_LOCAL':
        applications_table = boto3.resource(
            'dynamodb', endpoint_url='http://dynamodb:8000')
    else:
        applications_table = boto3.resource('dynamodb', region_name=region)

    table = applications_table.Table(table_name)
    application = json.loads(message['body'])
    username = application['name']

    item = table.get_item(TableName=table_name, Key={
        'username': username,
    })

    if item:
        params = item
        params['applications'].append(application)
    else:
        params = {
            'id': str(uuid.uuid4()),
            'created_on': str(datetime.timestamp(datetime.now())),
            'applications': item['applications'].append(application),
        }

    response = table.put_item(TableName=table_name, Item=params)
    print(response)

    return {
        'statusCode': 201,
        'headers': {},
        'body': json.dumps({'msg': 'Activity created'})
    }
