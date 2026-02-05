# code to run agent at 8am daily
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app_agents.digest_agent import DigestAgent
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import boto3

class DigestService():
    def __init__(self):
        self.bucket_name = "portfolia-daily-digest"
        self.prefix = "digests"
        self.region = "us-east-2"
        self.s3 = boto3.resource("s3", region_name=self.region) # Lambda / IAM role will automatically provide credentials
        
    def run_digest(self):
        agent = DigestAgent()
        llm_digest = agent.run_agent()
        json_str = json.dumps(llm_digest).encode("UTF-8")
        return json_str

    def digest_to_s3(self):
        et = ZoneInfo("America/New_York")
        date_key = datetime.now(et).date().isoformat()
        s3_object_key = f"{self.prefix}/{date_key}.json"

        body = self.run_digest()

        self.s3.Object(self.bucket_name, s3_object_key).put(
            Body=body,
            ContentType="application/json; charset=utf-8"
        )
        return f"s3://{self.bucket_name}/{s3_object_key}"

    def s3_to_client(self):
        et = ZoneInfo("America/New_York")
        date_key = datetime.now(et).date().isoformat()
        s3_object_key = f"{self.prefix}/{date_key}.json"

        s3_client = boto3.client("s3", region_name=self.region)

        try:
            response = s3_client.get_object(Bucket=self.bucket_name, Key=s3_object_key)
            body_bytes = response["Body"].read()
            return json.loads(body_bytes.decode("utf-8"))
        except s3_client.exceptions.NoSuchKey:
            raise FileNotFoundError(f"No digest found at s3://{self.bucket_name}/{s3_object_key}")
    
# not inside class
def lambda_handler(event, context):
    service = DigestService()
    s3_path = service.digest_to_s3()

    return {
        "statusCode": 200,
        "body": {
            "message": "Digest generated successfully",
            "s3_path": s3_path
        }
    }

if __name__ == "__main__":
    digest_service = DigestService()
    path = digest_service.digest_to_s3()
    print(path)

