#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_apigatewayv2 as _api,
    aws_apigatewayv2_integrations as _integrations,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_s3 as _s3
)

from constructs import Construct

class FlumeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        apigatewayname = cdk.CfnParameter(
            self,
            'apigatewayname',
            default = 'flume',
            type = 'String',
            description = 'Provide API Gateway Name'
        )

        s3bucketname = cdk.CfnParameter(
            self,
            's3bucketname',
            default = 'flume',
            type = 'String',
            description = 'Existing S3 Bucket Name'
        )

        verifytokenvalue = cdk.CfnParameter(
            self,
            'verifytokenvalue',
            default = '<VERIFY>',
            type = 'String',
            description = 'Set Unique Verification Value'
        )

    ### S3 BUCKET ###

        bucket = _s3.Bucket.from_bucket_name(
            self, 'bucket',
            bucket_name = s3bucketname.value_as_string
        )

    ### IAM ROLE ###

        role = _iam.Role(
            self, 'role', 
            assumed_by = _iam.ServicePrincipal(
                'lambda.amazonaws.com'
            )
        )

        role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'service-role/AWSLambdaBasicExecutionRole'
            )
        )

        role.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    's3:PutObject'
                ],
                resources = [
                    bucket.arn_for_objects('*')
                ]
            )
        )

    ### API LOG ROLE ###

        apirole = _iam.Role(
            self, 'apirole', 
            assumed_by = _iam.ServicePrincipal(
                'apigateway.amazonaws.com'
            )
        )

        apirole.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'service-role/AmazonAPIGatewayPushToCloudWatchLogs'
            )
        )

    ### LAMBDA FUNCTION ####

        with open('flume.py', encoding="utf8") as f:
            code = f.read()
        f.close()

        flume = _lambda.Function(
            self, 'flume',
            handler = 'index.handler',
            code = _lambda.InlineCode(code),
            runtime = _lambda.Runtime.PYTHON_3_13,
            architecture = _lambda.Architecture.ARM_64,
            timeout = Duration.seconds(30),
            environment = dict(
                BUCKET = bucket.bucket_name,
                PREFIX = 'logs',
                VERIFY = verifytokenvalue.value_as_string
            ),
            memory_size = 128,
            role = role
        )

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+flume.function_name,
            retention = _logs.RetentionDays.TWO_WEEKS,
            removal_policy = RemovalPolicy.DESTROY
        )

    ### API GATEWAY ###

        integration = _integrations.HttpLambdaIntegration(
            'integration', flume
        )

        api = _api.HttpApi(
            self, 'api',
            api_name = apigatewayname.value_as_string,
            description = apigatewayname.value_as_string
        )

        api.add_routes(
            path = '/logs',
            methods = [
                _api.HttpMethod.POST
            ],
            integration = integration
        )

### FLUME APPLICATION ###

app = cdk.App()

FlumeStack(
    app, 'FlumeStack',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = os.getenv('CDK_DEFAULT_REGION')
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

cdk.Tags.of(app).add('GitHub','https://github.com/jblukach/flume')

app.synth()