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
        
    def run_digest(self):
        agent = DigestAgent()
        llm_digest = agent.run_agent()
        json_str = json.dumps(llm_digest).encode("UTF-8")
        return json_str

    def digest_to_s3(self):
        et = ZoneInfo("America/New_York")
        date_key = datetime.now(et).date().isoformat()
        s3_object_key = f"digests/{date_key}.json"

        body = self.run_digest()

        s3 = boto3.resource("s3")
        s3.Object(self.bucket_name, s3_object_key).put(
            Body=body,
            ContentType="application/json; charset=utf-8"
        )
        return f"s3://{self.bucket_name}/{s3_object_key}"

    def s3_to_client(self):
        et = ZoneInfo("America/New_York")
        date_key = datetime.now(et).date().isoformat()
        s3_object_key = f"{self.prefix}/{date_key}.json"

        s3 = boto3.client("s3", region_name=self.region)

        try:
            response = s3.get_object(Bucket=self.bucket_name, Key=s3_object_key)
            body_bytes = response["Body"].read()
            return json.loads(body_bytes.decode("utf-8"))
        except s3.exceptions.NoSuchKey:
            raise FileNotFoundError(f"No digest found at s3://{self.bucket_name}/{s3_object_key}")
    

if __name__ == "__main__":
    digest_service = DigestService()

    path = digest_service.digest_to_s3()
    print(path)

# run agent
# save agent results to S3
# streamlit fetches from S3
# so forth