import aws_cdk as cdk

from constructs import Construct

from aws_cdk.aws_ec2 import SubnetSelection
from aws_cdk.aws_ec2 import SubnetType
from aws_cdk.aws_ec2 import InstanceClass
from aws_cdk.aws_ec2 import InstanceType
from aws_cdk.aws_ec2 import InstanceSize

from aws_cdk.aws_rds import AuroraCapacityUnit
from aws_cdk.aws_rds import AuroraPostgresEngineVersion
from aws_cdk.aws_rds import DatabaseCluster
from aws_cdk.aws_rds import InstanceProps
from aws_cdk.aws_rds import ServerlessCluster
from aws_cdk.aws_rds import DatabaseClusterEngine
from aws_cdk.aws_rds import ParameterGroup
from aws_cdk.aws_rds import ServerlessScalingOptions

from shared_infrastructure.cherry_lab.vpcs import VPCs


class ServerlessAurora(Construct):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        parameter_group = ParameterGroup.from_parameter_group_name(
            self,
            'ParameterGroup',
            'default.aurora-postgresql10'
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


class CdkDatabaseStack(cdk.Stack):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        vpcs = VPCs(
            self,
            'VPCs'
        )
        engine = DatabaseClusterEngine.aurora_postgres(
            version=AuroraPostgresEngineVersion.VER_13_4
        )
        DatabaseCluster(
            self,
            'CDKTestDatabase',
            engine=engine,
            instances=1,
            instance_props=InstanceProps(
                instance_type=InstanceType.of(
                    InstanceClass.BURSTABLE3,
                    InstanceSize.MEDIUM,
                ),
                vpc_subnets=SubnetSelection(
                    subnet_type=SubnetType.PUBLIC,
                ),
                vpc=vpcs.default_vpc
            ),
            default_database_name='igvfd',
        )
