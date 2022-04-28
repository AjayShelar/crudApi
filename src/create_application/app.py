import boto3
import os
import json
import uuid
from datetime import datetime
import time
env = os.environ.get('AWS_ENV')
AWS_ACCESS_KEY_ID = os.environ.get('AWSAccessKeyID', 'AKIAXXKJPZR2EMB6ADGH')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWSSecretAccessKey', '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')
region = os.environ.get('Region', 'ap-south-1')

print(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY )

# instantiate aws resources
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=region
)

def lambda_handler(message, context):
    print(message)

    if ('body' not in message or message['httpMethod'] != 'POST'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }
    
    table = dynamodb.Table('Applications')
    application = json.loads(message['body'])
    username = application['username']

    response = table.get_item( Key={
        'username': username,
    })
    created_on = int(time.time())
    if 'Item' in response:
        item = response['Item']
        if 'applications' not in item:
            item['applications'] = []
        application['created_on'] = created_on
        item['applications'].append(application)
        print(item)
        params = item
        
    else:
        application['created_on'] = created_on
        params = {
            'id': str(uuid.uuid4()),
            'username': application.pop('username'),
            'created_on':created_on ,
            'applications':[application],
        }

    response = table.put_item( Item=params)
    print(response)

    return {
        'statusCode': 201,
        'headers': {},
        'body': json.dumps({'msg': 'Application created'})
    }
