## Lambda Execution Role for S3 Object Lambda

This document provides the necessary IAM role and policies required for an AWS Lambda function that processes and transforms JSON objects stored in Amazon S3 using S3 Object Lambda. The s3-object-lambda:WriteGetObjectResponse API is used to return the transformed object.

### Steps:
1. Create an IAM role for the Lambda function. Name is `S3-Object-Lambda-Execution-Role`.
2. Attach the following policies to the role:
   - `AmazonS3ObjectLambdaExecutionRolePolicy`
   - `AmazonS3ReadOnlyAccess`
3. Complete the role with the necessary trust relationship for Lambda.

### Add "AmazonS3ObjectLambdaExecutionRolePolicy" - AWS Managed Policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "s3-object-lambda:WriteGetObjectResponse"
            ],
            "Resource": "*"
        }
    ]
}
```

### Add "AmazonS3ReadOnlyAccess" - AWS Managed Policy

```json

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:Get*",
                "s3:List*",
                "s3:Describe*",
                "s3-object-lambda:Get*",
                "s3-object-lambda:List*"
            ],
            "Resource": "*"
        }
    ]
}
```
