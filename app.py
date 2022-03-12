import aws_cdk as cdk

from cdk_database.cdk_database_stack import CdkDatabaseStack
from shared_infrastructure.cherry_lab.environments import US_WEST_2

app = cdk.App()

CdkDatabaseStack(
    app,
    'CdkDatabaseStack',
    env=US_WEST_2,
)

app.synth()
