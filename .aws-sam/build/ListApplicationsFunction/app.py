import boto3
import os
import json

env = os.environ.get('AWS_ENV')
AWS_ACCESS_KEY_ID = os.environ.get('AWSAccessKeyID', 'AKIAXXKJPZR2H3QRZQ5V')
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

from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)
def lambda_handler(event, context):
    print(event)

    queryStringParameters = event['queryStringParameters']

    if ('httpMethod' not in event or
            event['httpMethod'] != 'GET') or 'username' not in queryStringParameters:
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }


    table = dynamodb.Table('Applications')
    response = table.get_item( Key={
        'username': queryStringParameters['username'],
    })

    print(response)

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(response['Item']['applications'], cls=DecimalEncoder)
    }
