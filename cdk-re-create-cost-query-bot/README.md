# AWS CDK Resource Recreation Demo

This repository demonstrates how to recreate existing AWS resources using AWS CDK, effectively bringing manually created resources under Infrastructure as Code (IaC) management. This accompanies a [YouTube video tutorial](https://youtu.be/nfZhPgK2jXk) showing the complete process.

## Overview

This project shows how to:
1. Export existing AWS resources configuration to JSON
2. Use that JSON configuration to recreate the resources using AWS CDK
3. Create a new version of the infrastructure with slight modifications (using "-2" suffix)

The example recreates a serverless cost query system consisting of:
- AWS Lambda function
- IAM Role with necessary permissions
- API Gateway HTTP API
- CloudWatch logging configuration

## Prerequisites

- AWS CLI configured with appropriate credentials
- Node.js and npm installed
- Python 3.9 or later
- AWS CDK CLI installed (`npm install -g aws-cdk`)
- Virtual environment tool (e.g., `python -m venv`)

## Project Structure

```
.
├── README.md
├── app.py
├── cdk.json
├── cost_query_bot_config.json    # Original resources configuration
├── lambda/                       # Lambda function code directory
│   └── lambda_function.py
├── cdk_re_create_cost_query_bot/
│   └── cdk_re_create_cost_query_bot_stack.py
└── requirements.txt
```

## Exporting Existing Resources

To export your existing AWS resources configuration to JSON, use the following script:

```bash
# Set your resource names/ARNs
role_name=<iam-role-name>
function_arn=<function-arn>
api_id=<api-id>
output_file="cost_query_bot_config.json"

# Export the configuration
{
  echo "{"
  echo "\"role\": $(aws iam get-role --role-name "$role_name" --output json),"
  echo "\"attached_policies\": $(aws iam list-attached-role-policies --role-name "$role_name" --output json),"
  echo "\"inline_policies\": $(aws iam list-role-policies --role-name "$role_name" --output json),"
  echo "\"inline_policy_def\": $(aws iam get-role-policy --role-name "$role_name" --policy-name demo-cost-explorer-policy --output json),"
  echo "\"lambda_function\": $(aws lambda get-function --function-name "$function_arn" --output json),"
  echo "\"api\": $(aws apigatewayv2 get-api --api-id "$api_id" --output json),"
  echo "\"routes\": $(aws apigatewayv2 get-routes --api-id "$api_id" --output json),"
  echo "\"stages\": $(aws apigatewayv2 get-stages --api-id "$api_id" --output json),"
  echo "\"deployments\": $(aws apigatewayv2 get-deployments --api-id "$api_id" --output json),"
  echo "\"integrations\": $(aws apigatewayv2 get-integrations --api-id "$api_id" --output json)"
  echo "}"
} > "$output_file"
```

This script will create a JSON file containing all the configuration details of your existing resources. You can then use this file to recreate the resources using CDK.

## Getting Started

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd cdk-re-create-cost-query-bot
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create the Lambda function code directory and add your function code:
   ```bash
   mkdir lambda
   # Add your lambda_function.py to the lambda directory
   ```

5. Deploy the stack:
   ```bash
   cdk deploy
   ```

## How It Works

1. **Resource Export**: 
   - The original AWS resources were exported to `cost_query_bot_config.json`
   - This JSON file contains all the configuration details of the existing resources

2. **CDK Stack Creation**:
   - The CDK stack (`cdk_re_create_cost_query_bot_stack.py`) was created using AI assistance
   - The AI analyzed the JSON configuration and generated the appropriate CDK constructs
   - Resource names include "-2" suffix to avoid conflicts with existing resources

3. **Deployment**:
   - The CDK stack creates new resources based on the original configuration
   - All resources are created with infrastructure as code, making them easier to manage and version control

## Resource Modifications

The new stack includes these modifications from the original:
- All resource names have "-2" suffix to avoid naming conflicts
- Maintains the same functionality as the original resources
- Uses CDK best practices for resource creation

## Useful Commands

* `cdk ls`          list all stacks in the app
* `cdk synth`       emits the synthesized CloudFormation template
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk destroy`     destroy the stack

## Video Tutorial

For a detailed walkthrough of this process, check out the accompanying YouTube video: [Link to Video]

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Your chosen license]
