# flume

Write everything as Infrastructure as Code (IaC) in a specific technology; what happens when the pipeline is unavailable and security teams can not continuously improve and deploy (CI/CD) to environments?

Just because something is not working does not mean that there should not be alternative options for incident response. Cloud Development Kit (CDK) generates a standalone CloudFormation stack for quick deployment.

### Objective

- Webhook log shipment to HEC log collector over HTTPS using an API Gateway

### Quick Stack

1. Download ```flume.yaml```
2. Create Stack
3. Stack Name
4. API Gateway Name
5. Add Tags
6. Deploy CloudFormation
7. Update Secret for HEC Information
8. Configure Webhook Destination

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

### References

- https://docs.splunk.com/Documentation/SplunkCloud/latest/Data/FormateventsforHTTPEventCollector
- https://library.humio.com/logscale-api/log-shippers-hec.html
