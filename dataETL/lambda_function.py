from dataManipulation import dataManipulation
import boto3
import botocore
import time

client = boto3.client('dynamodb')
snsclient = boto3.client('sns')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    for dataSet in dataManipulation():
        try:
            client.put_item( 
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
                    },
                    'New-Cases' : {
                        'N' : dataSet[4]
                    },
                    'New-Deaths' : {
                        'N' : dataSet[5]
                    },
                    'New-Recoveries' : {
                        'N' : dataSet[6]
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