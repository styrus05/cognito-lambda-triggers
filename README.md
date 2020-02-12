## Problem statement
Cognito Lambda Triggers work at User Pool level and not at App Client level. We need a level of separation between code for different app clients.

## Solution
As part of the authentication process Cognito will call the main lambda function (pre-auth-lambda-trigger.py). This will be configured once at the Cognito User Pool level. This in turn will call the lambda function created for an app client (say cognito-authorisation-123456789.py, where 123456789 is the app client ID). Actual group membership checks and other validations will be done inside this app client specific lambda function which means no change is required in the main lambda trigger (pre-auth-lambda-trigger.py)