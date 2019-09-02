This project is a AWS lambda to interact with kubernetes.

## Dependencies:
kubernetes needs to be 9.0.0.
When using 10+, i got an error on config.load_config()

This is an implmementatio follwoing this blog: https://medium.com/@alejandro.millan.frias/managing-kubernetes-from-aws-lambda-7922c3546249


## AWS Config:
* Created a role granting sts and eks access:
``` yaml
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "sts:GetCallerIdentity",
                "eks:DescribeCluster"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
```
* using build.sh to package, upload to S3 bucket and update the function. (Initial function setup currently is manual)

##  Kubernetes Config:
Need to create a role (see role.yaml) and role binding (see rolebinding.yaml) to link the AWS role with Kube user
