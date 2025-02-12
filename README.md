# flume

What happens when Infrastructure as Code (IaC) is all written in a specific technology, but the pipeline is unavailable for deployments? Security teams do not have a choice requiring an alternative option to contain cloud environments. Enter Cloud Development Kit (CDK), which can generate a stand-alone CloudFormation stack for quick deployment.  

### Objective

- Ship Webhook logs to an S3 bucket with an API Gateway broker.

### Quick Stack

1. Download ```flume.yaml```
2. Create Stack
3. Stack Name
4. API Gateway Name
5. Existing S3 Bucket Name
6. Add Tags
7. Deploy CloudFormation

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
