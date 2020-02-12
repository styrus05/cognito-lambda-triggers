import json
import os

def lambda_handler(event, context):
    
    # Needed group(s) 
    neededGroup = os.environ['NEEDED_GROUP_MEMBERSHIP']
    print('neededGroup:')
    print(neededGroup)
    
    print('full payload:')
    print(event)
    
    groups = []
    groups = neededGroup.split("|")

    print('Group membership for this user:')
    try:
        print(event["request"]['userAttributes']['custom:Groups'])
        allowed = any(item in event["request"]['userAttributes']['custom:Groups'] for item in groups)
        print(allowed)
        if allowed is True:
            return {
                'statusCode': 200,
                'body': json.dumps('User is allowed to access the app.')
            }
        else :
            return {
                    'statusCode': 403,
                    'body': json.dumps('User is NOT allowed to access the app.')
                }
    except Exception as e:
        print(e)
        return {
            'statusCode': 403,
            'body': json.dumps('Group membership check failed. This user CANNOT access the app.')
        }
