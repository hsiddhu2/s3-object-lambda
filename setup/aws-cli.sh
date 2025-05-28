# Step 1: Create a general purpose S3 bucket using aws cli command  
aws s3api create-bucket --bucket demo-s3-object-lambda --region us-east-1 --create-bucket-configuration LocationConstraint=us-east-1

// Upload user-info.json file to the S3 bucket
aws s3 cp user-info.json s3://demo-s3-object-lambda/user-info.json

# Step 2: Create support S3 Access point - internet
aws s3control create-access-point --account-id 123456789012 --name s3-object-lambda-ap --bucket demo-s3-object-lambda --region us-east-1
aws s3control get-access-point --account-id 123456789012 --name s3-object-lambda-ap

# Step 4: Create Lambda execution role with S3 as well as S3 Object Lambda permissions
Follow the steps in `lambda-execution-role.md` 

# Step 6: Create a AWS Lambda function with Python latest as the run time and use the code transform.py 

zip transform.zip transform.py

aws lambda create-function 
    --function-name s3-object-lambda-transform 
    --runtime python3.9 
    --handler transform.handler 
    --role arn:aws:iam::123456789012:role/S3-Object-Lambda-Execution-Role 
    --zip-file fileb://transform.zip

# Step 6: Create S3 Object Lambda Access Point 
aws s3control create-access-point-for-object-lambda 
    --account-id 123456789012 
    --name s3-object-lambda-ap-ol 
    --supporting-access-point-arn arn:aws:s3:us-east-1:123456789012:accesspoint/s3-object-lambda-ap 
    --object-lambda-configuration '{"SupportingAccessPoint": "arn:aws:s3:us-east-1:123456789012:accesspoint/s3-object-lambda-ap", "TransformationConfigurations": [{"Actions": ["GetObject"], "ContentTransformation": {"AwsLambda": {"FunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:s3-object-lambda-transform"}}}]}' 
    --region us-east-1

# Step 7: Test the S3 Object Lambda Access Point
aws s3api get-object --bucket s3-object-lambda-ap-ol --key user-info.json output.json

# Step 8: Verify the output
cat output.json

# Step 9: Clean up
aws s3 rm s3://s3-object-lambda-ap-ol --recursive
aws s3api delete-bucket --bucket demo-s3-object-lambda --region us-east-1
aws s3control delete-access-point --account-id 123456789012 --name s3-object-lambda-ap
aws s3control delete-access-point-for-object-lambda --account-id 123456789012 --name s3-object-lambda-ap-ol
aws lambda delete-function --function-name s3-object-lambda-transform
aws iam delete-role --role-name S3-Object-Lambda-Execution-Role
