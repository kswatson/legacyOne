import os
import json
import boto3
import time

table = os.environ["LegacyOneDatabase"]
dynamodb = boto3.client("dynamodb")

default_headers = {
            "Content-Type": "text/plain",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Origin": "*"
        }

def handler(event, context):
 
  method = event["httpMethod"]
  if method == "OPTIONS":
      return {
        "statusCode": "200",
        "body": None,
        "headers": default_headers
      }
  else:
    id = event["pathParameters"]["id"]
    response = dynamodb.get_item(TableName = table, Key = {"Id": {"N": id}})
    
    if "Item" not in response:
      print("Item not in response")
      return respond(None, 404)
    elif "firstAuthenticatedAt" in response["Item"]:
      count = int(response["Item"]["count"]["N"])
      dynamodb.put_item(TableName = table, Item = {"Id": {"N": id}, 
                                                   "firstAuthenticatedAt": {"S": response["Item"]["firstAuthenticatedAt"]["S"]},
                                                   "lastAuthenticatedAt": {"S": str(time.time())},
                                                   "count": {"N": str(count + 1)}})
      return respond(None, 409, {
        "count": count + 1,
        "firstAuthenticatedAt": response["Item"]["firstAuthenticatedAt"]["S"]
      })
    else:
      dynamodb.put_item(TableName = table, Item = {"Id": {"N": id}, "firstAuthenticatedAt": {"S": str(time.time())}, "count": {"N": "1"}})
      return respond(None, 204)

def respond(err, code=200, body=None):
    return {
        "statusCode": "400" if err else code,
        "body": str(body) if body else None,
        "headers": default_headers
    }