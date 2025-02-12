#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_apigateway as _api,
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

        role.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'apigateway:POST'
                ],
                resources = [
                    '*'
                ]
            )
        )

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
                PREFIX = 'logs'
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

        apilogs = _logs.LogGroup(
            self, 'apilogs',
            retention = _logs.RetentionDays.TWO_WEEKS,
            removal_policy = RemovalPolicy.DESTROY
        )

        api = _api.RestApi(
            self, 'api',
            rest_api_name = apigatewayname.value_as_string,
            endpoint_types = [_api.EndpointType.REGIONAL],
            deploy_options = _api.StageOptions(
                method_options={
                    '/*/*': _api.MethodDeploymentOptions(
                        throttling_rate_limit = 10000,
                        throttling_burst_limit = 5000
                    )
                }
            )
        )

        entity = api.root.add_resource('ingest')

        integration = _api.LambdaIntegration(
            flume,
            proxy = True, 
            integration_responses = [
                _api.IntegrationResponse(
                    status_code = '200',
                    response_parameters = {
                        'method.response.header.Access-Control-Allow-Origin': "'*'"
                    }
                )
            ]
        )

        methd = entity.add_method(
            'POST', 
            integration,
            api_key_required = False,
            method_responses = [
                _api.MethodResponse(
                    status_code = '200',
                    response_parameters = {
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ]
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