from __future__ import print_function
import urllib
import json
import boto3

print ("Loading function")

lam = boto3.client('lambda')

cognito_idp_client = boto3.client('cognito-idp')

def lambda_handler(event, context):
 #raise Exception("User is not authorised to access this application")
    # Send post authentication data to Cloudwatch logs
    print ("Authentication successful")
    print ("Trigger function =", event['triggerSource'])
    
    userPool = event['userPoolId']
    appClientID = event['callerContext']['clientId']
    userID = event['userName']
    print ("User pool = ", userPool)
    print ("App client ID = ", appClientID)
    print ("User ID = ", userID)

    function_name='cognito-authorisation-' + appClientID
    print (function_name)
    try:
        response = lam.invoke(
            FunctionName= function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(event))
    except Exception as e:
        print(e)
        raise e
        
    print("Response from other lambda:")
    print(response)    
    
    response_string = response['Payload'].read().decode()
    
    #print(response_string)
    
    response_from_auth_lambda = json.loads(response_string)
    
    print(response_from_auth_lambda)
    print(response_from_auth_lambda["statusCode"])

    # raise error
    if response_from_auth_lambda["statusCode"]==403:
        raise Exception("User is not authorised to access this application")
        print("Logout user..")
        response = cognito_idp_client.admin_user_global_sign_out(
           UserPoolId=userPool,
            Username=userID
        )
        print("Response form logout request = ",response)
        
    # Return to Amazon Cognito
    
    return event

