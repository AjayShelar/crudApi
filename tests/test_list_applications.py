import boto3
import json
import os
from moto import mock_dynamodb2
from unittest.mock import patch
from src.list_Applications import app
from contextlib import contextmanager

table_name = 'Applications'

event_data = 'events/list_apps_event.json'
with open(event_data, 'r') as f:
    event = json.load(f)


@contextmanager
def do_test_setup():
    with mock_dynamodb2():
        set_up_dynamodb()
        put_item_dynamodb()
        yield


def set_up_dynamodb():
    conn = boto3.client(
        'dynamodb',
        region_name='ap-south-1',
        aws_access_key_id='mock',
        aws_secret_access_key='mock',
    )
    conn.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'},
            {'AttributeName': 'date', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'},
            {'AttributeName': 'date', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        },
    )


def put_item_dynamodb():
    conn = boto3.client(
        'dynamodb',
        region_name='ap-south-1',
        aws_access_key_id='mock',
        aws_secret_access_key='mock',
    )

    conn.put_item(
        TableName=table_name,
        Item={
 "username": {
  "S": "kijay@gmail.com"
 },
 "created_on": {
  "N": "12313"
 },
 "applications": {
  "L": [
   {
    "M": {
     "name": {
      "S": "eth0"
     },
     "chain": {
      "S": "Ethereum"
     },
     "id": {
      "S": "wqe123e23e"
     },
     "secret": {
      "S": "dawe23dw4"
     }
    }
   }
  ]
 }
}
    )

    conn.put_item(
        TableName=table_name,
        Item={
 "username": {
  "S": "ajay@gmail.com"
 },
 "created_on": {
  "N": "12313"
 },
 "applications": {
  "L": [
   {
    "M": {
     "name": {
      "S": "eth0"
     },
     "chain": {
      "S": "Ethereum"
     },
     "id": {
      "S": "wqe123e23e"
     },
     "secret": {
      "S": "dawe23dw4"
     }
    }
   }
  ]
 }
}
    )


@patch.dict(os.environ, {
    'TABLE': 'Applications',
    'REGION': 'ap-south-1',
    'AWSENV': 'MOCK'
})
def test_list_applications_200():
    with do_test_setup():
        response = app.lambda_handler(event, '')

        payload = [
    {
        "name": "eth0",
        "chain": "Etherium",
        "id": "asdlasldas",
        "secret": "dawe23dw4",
        "created_on": "1650940732"
    },
    {
        "name": "eth0",
        "chain": "Etherium",
        "id": "asdlasldas",
        "secret": "dawe23dw4",
        "created_on": "1650941308",
        "username": "kijay@gmail.com"
    }
]
        data = json.loads(response['body'])

        assert event['httpMethod'] == 'GET'
        assert data == payload


@patch.dict(os.environ, {
    'TABLE': 'Applications',
    'REGION': 'ap-south-1',
    'AWSENV': 'MOCK'
})
def test_list_applications_400():
    with do_test_setup():
        response = app.lambda_handler({}, '')

        payload = {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

        assert response == payload
