import boto3
import json
import urllib.request
from urllib.error import HTTPError, URLError
from botocore.config import Config

def lambda_handler(event, context):
    print('Event:', event)

    object_context = event.get("getObjectContext", {})
    s3_url = object_context.get("inputS3Url")
    request_route = object_context.get("outputRoute")
    request_token = object_context.get("outputToken")

    s3 = boto3.client('s3', config=Config(signature_version='s3v4'))

    try:
        # Validate input
        if not s3_url or not request_route or not request_token:
            raise ValueError("Missing inputS3Url, outputRoute, or outputToken.")

        # Attempt to read from S3
        with urllib.request.urlopen(s3_url) as response:
            original_object = response.read().decode("utf-8")

        # Parse JSON
        data = json.loads(original_object)

        # Redact sensitive fields
        if "ssn" in data:
            ssn = data["ssn"]
            data["ssn"] = "***-**-" + ssn[-4:] if len(ssn) >= 4 else "****"

        if "dob" in data:
            data["dob"] = "1990/**/**"

        if "address" in data and isinstance(data["address"], dict):
            addr = data["address"]
            addr["street"] = addr.get("street", "").split()[0] + " ****"
            addr["city"] = "****"
            addr["state"] = "**"
            addr["zip"] = addr.get("zip", "")[:3] + "**"

        if "phoneNumbers" in data and isinstance(data["phoneNumbers"], list):
            for phone in data["phoneNumbers"]:
                if "number" in phone:
                    phone["number"] = phone["number"][:4] + "****"

        # Create uppercase version
        redacted_json_str = json.dumps(data, indent=2).upper()

        combined_output = (
            "ORIGINAL OBJECT:\n" + original_object + "\n\n" +
            "TRANSFORMED OBJECT:\n" + redacted_json_str
        )

        # Return transformed object
        s3.write_get_object_response(
            Body=combined_output,
            RequestRoute=request_route,
            RequestToken=request_token,
            StatusCode=200
        )
        return {"status_code": 200}

    except (HTTPError, URLError) as e:
        error_msg = f"Unauthorized or inaccessible object: {e.reason}"
        print("HTTP error:", error_msg)

        s3.write_get_object_response(
            Body=error_msg,
            RequestRoute=request_route,
            RequestToken=request_token,
            StatusCode=e.code if hasattr(e, 'code') else 403
        )
        return {"status_code": e.code if hasattr(e, 'code') else 403}

    except Exception as e:
        error_msg = f"Internal error: {str(e)}"
        print("Exception:", error_msg)

        s3.write_get_object_response(
            Body=error_msg,
            RequestRoute=request_route,
            RequestToken=request_token,
            StatusCode=500
        )
        return {"status_code": 500}
