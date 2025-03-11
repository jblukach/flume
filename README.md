# flume

What happens when Infrastructure as Code (IaC) is all written in a specific technology, but the pipeline is unavailable for deployments? Security teams do not have a choice requiring an alternative option to contain cloud environments. Enter Cloud Development Kit (CDK), which can generate a stand-alone CloudFormation stack for quick deployment.  

### Objective

- Ship Webhook logs to an S3 bucket with an API Gateway broker.

### Quick Stack

1. Download ```flume.yaml```
2. Check Regions [1](https://github.com/jblukach/flume/blob/05b2a09231def1b215e5023d9eefa3d36762c278/flume.yaml#L253C36-L253C45) [2](https://github.com/jblukach/flume/blob/05b2a09231def1b215e5023d9eefa3d36762c278/flume.yaml#L272C36-L272C45) [3](https://github.com/jblukach/flume/blob/05b2a09231def1b215e5023d9eefa3d36762c278/flume.yaml#L293C36-L293C45) [4](https://github.com/jblukach/flume/blob/05b2a09231def1b215e5023d9eefa3d36762c278/flume.yaml#L313C26-L313C35)
3. Create Stack
4. Stack Name
5. API Gateway Name
6. Existing S3 Bucket Name
7. Add Tags
8. Deploy CloudFormation
9. Change Verify Token

### Broker URL

```
https://3ta9vobuad.execute-api.us-east-1.amazonaws.com/logs?verify=<VERIFY>
```

### CloudFormation

```
cdk synth --no-version-reporting --no-path-metadata --no-asset-metadata > flume.yaml
```

Delete from the ```Parameters:``` section of the ```flume.yaml``` file.

```
  BootstrapVersion:
    Type: AWS::SSM::Parameter::Value<String>
    Default: /cdk-bootstrap/4n6ir/version
    Description: Version of the CDK Bootstrap resources in this environment, automatically retrieved from SSM Parameter Store. [cdk:skip]
```
