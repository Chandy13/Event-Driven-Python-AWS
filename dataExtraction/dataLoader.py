from dataManipulation import dataManipulation
import boto3
import botocore

client = boto3.client('dynamodb')

def dataLoader():
    for dataSet in dataManipulation():
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
                ExpressionAttributeNames={'#date': 'Date'},
                ConditionExpression='attribute_not_exists(#date)'
            )
        except botocore.exceptions.ClientError as e:
            # Ignore the ConditionalCheckFailedException
            # other exceptions.
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise

dataLoader()