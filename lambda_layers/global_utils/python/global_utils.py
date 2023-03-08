import json
import os
import boto3

dynamodb_client = boto3.client("dynamodb")
dynamodb_resource = boto3.resource("dynamodb")
test_table_name = os.environ.get("TEST_TABLE", None)
