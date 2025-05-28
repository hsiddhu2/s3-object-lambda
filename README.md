# S3 Object Transformer Lambda Function

This project contains an AWS Lambda function written in Python that processes and transforms JSON objects stored in Amazon S3. The function is designed to redact sensitive information from the JSON object and return a transformed version of the object.

## Features

- **Input Validation**: Ensures required parameters (`inputS3Url`, `outputRoute`, `outputToken`) are provided.
- **Data Redaction**: Redacts sensitive fields such as Social Security Numbers (SSN), dates of birth (DOB), addresses, and phone numbers.
- **Custom Transformation**: Converts the redacted JSON object to uppercase for additional processing.
- **Error Handling**: Handles HTTP errors, inaccessible objects, and internal exceptions gracefully.
- **Integration with S3 Object Lambda**: Uses the `WriteGetObjectResponse` API to return the transformed object.

## How It Works

1. The Lambda function is triggered by an S3 Object Lambda event.
2. It retrieves the JSON object from the provided `inputS3Url`.
3. Sensitive fields in the JSON object are redacted:
   - **SSN**: Only the last 4 digits are retained.
   - **DOB**: Replaced with a generic date format.
   - **Address**: Street, city, state, and zip code are partially redacted.
   - **Phone Numbers**: Only the first 4 digits are retained.
4. The redacted JSON object is converted to uppercase.
5. The original and transformed objects are combined into a single response.
6. The response is sent back to the client using the `WriteGetObjectResponse` API.

## Prerequisites

- **AWS Account**: Ensure you have an AWS account with permissions to deploy and execute Lambda functions.
- **IAM Role**: The Lambda function requires an IAM role with the following permissions:
  - `s3:GetObject`
  - `s3-object-lambda:WriteGetObjectResponse`
- **Python 3.8 or higher**: The function is written in Python and requires a compatible runtime.

## Deployment

1. **Package the Lambda Function**:
   - Zip the `transform.py` file along with any dependencies (if applicable).

   ```bash
   zip function.zip transform.py