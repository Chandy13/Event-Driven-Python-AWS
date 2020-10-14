from dataManipulation import dataManipulation
import boto3
import botocore
import json
import time

client = boto3.client('dynamodb')
snsclient = boto3.client('sns')
s3 = boto3.client('s3')

jsondata = [] #empty dict for data entry
def lambda_handler(event, context):
    for dataSet in dataManipulation():
        entry = {}
        entry['Date'] = {'S' : dataSet[0]}
        entry['Cases'] = {'N' : dataSet[1]}
        entry['Deaths'] = {'N' : dataSet[2]}
        entry['Recoveries'] = {'N' : dataSet[3]}
        jsondata.append(entry)
        try:
            client.put_item( #add response = at beginning if function doesn't work
                TableName = 'USCOVIDDATA',
                Item = {
                    'Date' : {
                        'S' : dataSet[0]
                    },
                    'Cases' : {
                        'N' : dataSet[1]
                    },
                    'Deaths' : {
                        'N' : dataSet[2]
                    },
                    'Recoveries' : {
                        'N' : dataSet[3]
                    }
                },
                ExpressionAttributeNames = {'#date': 'Date'},
                ConditionExpression = 'attribute_not_exists(#date)'
            )
        except botocore.exceptions.ClientError as e:
            # Ignore the ConditionalCheckFailedException
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                snsclient.publish(
                    TopicArn = 'arn:aws:sns:us-east-1:018943110893:NotifyMe',
                    Message = 'There is an error with the date being entered',
                    Subject = 'US Covid Data table update error'
                )
    s3.delete_object(
        Bucket = 'event-driven-python-aws-code',
        Key = 'DATA.json'
    )            
    time.sleep(1)
    s3.put_object(
        Bucket = 'event-driven-python-aws-code',
        Body = json.dumps(jsondata),
        Key = 'DATA.json'
    )