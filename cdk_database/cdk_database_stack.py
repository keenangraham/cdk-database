import aws_cdk as cdk

from aws_cdk.aws_rds import AuroraCapacityUnit
from aws_cdk.aws_rds import ServerlessCluster
from aws_cdk.aws_rds import DatabaseClusterEngine
from aws_cdk.aws_rds import ParameterGroup
from aws_cdk.aws_rds import ServerlessScalingOptions

from shared_infrastructure.cherry_lab.vpcs import VPCs


class CdkDatabaseStack(cdk.Stack):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        parameter_group = ParameterGroup.from_parameter_group_name(
            self,
            'ParameterGroup',
            'default.aurora-postgresql10'
        )
        vpcs = VPCs(
            self,
            'VPCs'
        )
        ServerlessCluster(
            self,
            'DatabaseCluster',
            engine=DatabaseClusterEngine.AURORA_POSTGRESQL,
            parameter_group=parameter_group,
            scaling=ServerlessScalingOptions(
                auto_pause=cdk.Duration.minutes(5),
                min_capacity=AuroraCapacityUnit.ACU_2,
                max_capacity=AuroraCapacityUnit.ACU_4,
            ),
            default_database_name='test'
        )
