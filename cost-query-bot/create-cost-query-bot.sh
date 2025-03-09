export AWS_PROFILE=$DEV_ACCOUNT
aws sso login 

# Create an IAM Role for Lambda with Cost Explorer Permissions
aws iam create-role --role-name demo-lambda-role --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}'

aws iam attach-role-policy --role-name demo-lambda-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam put-role-policy --role-name demo-lambda-role --policy-name demo-cost-explorer-policy --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "ce:GetCostAndUsage",
            "Resource": "*"
        }
    ]
}'
# package and deploy the lambda function
zip function.zip lambda_function.py

aws lambda create-function --function-name demo-cost-query \
    --runtime python3.9 --role arn:aws:iam::$(aws sts get-caller-identity --query "Account" --output text):role/demo-lambda-role \
    --handler lambda_function.lambda_handler --zip-file fileb://function.zip

# Create an API Gateway HTTP API
API_ID=$(aws apigatewayv2 create-api --name demo-cost-api --protocol-type HTTP --query "ApiId" --output text)

LAMBDA_ARN=$(aws lambda get-function --function-name demo-cost-query --query "Configuration.FunctionArn" --output text)

INTEGRATION_ID=$(aws apigatewayv2 create-integration \
    --api-id $API_ID \
    --integration-type AWS_PROXY \
    --integration-uri $LAMBDA_ARN \
    --payload-format-version 2.0 \
    --query "IntegrationId" --output text)
# 4️⃣ Create a route for the API (e.g., /cost)
aws apigatewayv2 create-route \
    --api-id $API_ID \
    --route-key "GET /cost" \
    --target "integrations/$INTEGRATION_ID"

# 5️⃣ Grant API Gateway permission to invoke Lambda
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
REGION=$(aws configure get region)

aws lambda add-permission \
    --function-name demo-cost-query \
    --statement-id apigateway-invoke \
    --action lambda:InvokeFunction \
    --principal apigateway.amazonaws.com \
    --source-arn "arn:aws:execute-api:$REGION:$ACCOUNT_ID:$API_ID/*"


# 6️⃣ Deploy the API
aws apigatewayv2 create-stage --api-id $API_ID --stage-name prod --deployment-id $(aws apigatewayv2 create-deployment --api-id $API_ID --query "DeploymentId" --output text)

aws apigatewayv2 create-deployment --api-id $API_ID --stage-name prod

# 7️⃣ Get the API Gateway URL
API_URL=$(aws apigatewayv2 get-api --api-id $API_ID --query "ApiEndpoint" --output text)
echo "API Gateway URL: $API_URL/prod/cost"
# test hit the gateway
echo $API_URL
curl -s $API_URL/prod/cost | jq