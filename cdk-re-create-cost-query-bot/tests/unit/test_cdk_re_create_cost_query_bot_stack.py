import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_re_create_cost_query_bot.cdk_re_create_cost_query_bot_stack import CdkReCreateCostQueryBotStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_re_create_cost_query_bot/cdk_re_create_cost_query_bot_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkReCreateCostQueryBotStack(app, "cdk-re-create-cost-query-bot")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
