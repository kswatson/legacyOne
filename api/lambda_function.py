import os
import json
import boto3

table = os.environ['LegacyOneDatabase']
dynamodb = boto3.client('dynamodb')

default_headers = {
            'Content-Type': 'text/plain',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
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
    id = event['pathParameters']['id']
    response = dynamodb.get_item(TableName = table, Key = {'Id': {'N': id}})
    
    return respond(None, 204 if 'Item' in response else 404)

def respond(err, code=200):
    return {
        'statusCode': '400' if err else code,
        'body': None,
        'headers': default_headers
    }