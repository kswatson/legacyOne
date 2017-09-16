import sys
import boto3
from botocore.client import Config
from time import sleep

file_name = sys.argv[1]
table_name = sys.argv[2]
access_key = sys.argv[3]
secret_key = sys.argv[4]

dynamodb = boto3.client('dynamodb',
						aws_access_key_id=access_key,
						aws_secret_access_key=secret_key,
						region_name='ca-central-1',
						config=Config(signature_version='s3v4'))

with open(file_name) as f:

	for line in f:
		dynamodb.put_item(
			TableName=table_name,
			Item={
			  'Id': {
			    'N': str(line).strip()
			  }
			}
		)
		print('Inserted code ' + line)
		sleep(1)
f.closed