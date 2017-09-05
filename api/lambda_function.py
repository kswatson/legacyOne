import os
import json
import boto3
import time

table = os.environ['LegacyOneDatabase']
dynamodb = boto3.client('dynamodb')

default_headers = {
            'Content-Type': 'text/plain',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': '*'
        }

def handler(event, context):
 
  method = event['httpMethod']
  if method == 'OPTIONS':
      return {
        'statusCode': '200',
        'body': None,
        'headers': default_headers
      }
  else:
    print('TOP')
    id = event['pathParameters']['id']
    response = dynamodb.get_item(TableName = table, Key = {'Id': {'N': id}})
    
    if 'Item' not in response:
      print('Item not in response')
      return respond(None, 404)
    elif 'authenticatedAt' in response['Item']:
      return respond(None, 409)
    else:
      dynamodb.put_item(TableName = table, Item = {'Id': {'N': id}, 'authenticatedAt': {'S': str(time.time())}})
      return respond(None, 204)

def respond(err, code=200):
    return {
        'statusCode': '400' if err else code,
        'body': None,
        'headers': default_headers
    }