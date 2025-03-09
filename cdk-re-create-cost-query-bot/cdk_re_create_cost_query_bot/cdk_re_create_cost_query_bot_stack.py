from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_apigatewayv2 as apigw_v2,
    aws_apigatewayv2_integrations as apigw_v2_integrations,
    CfnOutput
)
from constructs import Construct

class CdkReCreateCostQueryBotStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create IAM role for Lambda
        lambda_role = iam.Role(
            self, "CostQueryLambdaRole",
            role_name="demo-lambda-role-2",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )

        # Add AWS Lambda basic execution policy
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )

        # Add inline policy for Cost Explorer access
        cost_explorer_policy = iam.Policy(
            self, "CostExplorerPolicy",
            policy_name="demo-cost-explorer-policy-2",
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["ce:GetCostAndUsage"],
                    resources=["*"]
                )
            ]
        )
        cost_explorer_policy.attach_to_role(lambda_role)

        # Create Lambda function
        cost_query_function = lambda_.Function(
            self, "CostQueryFunction",
            function_name="demo-cost-query-2",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=lambda_.Code.from_asset("lambda"),
            role=lambda_role,
            memory_size=128,
            timeout=Duration.seconds(3),
            architecture=lambda_.Architecture.X86_64,
            environment={
                "LOG_FORMAT": "Text"
            }
        )

        # Create HTTP API
        http_api = apigw_v2.HttpApi(
            self, "CostQueryApi",
            api_name="demo-cost-api-2"
        )

        # Add Lambda integration
        lambda_integration = apigw_v2_integrations.HttpLambdaIntegration(
            "CostQueryIntegration",
            handler=cost_query_function,
            payload_format_version=apigw_v2.PayloadFormatVersion.VERSION_2_0
        )

        # Add route to the API
        http_api.add_routes(
            path="/cost",
            methods=[apigw_v2.HttpMethod.GET],
            integration=lambda_integration
        )

        # Add stage to the API
        stage = apigw_v2.HttpStage(
            self, "ProdStage",
            http_api=http_api,
            stage_name="prod",
            auto_deploy=True
        )

        # Output the API endpoint
        CfnOutput(
            self, "ApiEndpoint",
            value=http_api.api_endpoint
        )
