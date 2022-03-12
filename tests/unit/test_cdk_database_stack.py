import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_database.cdk_database_stack import CdkDatabaseStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_database/cdk_database_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkDatabaseStack(app, "cdk-database")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
