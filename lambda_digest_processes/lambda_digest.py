import json
from datetime import datetime
from zoneinfo import ZoneInfo
import boto3
from app_agents.digest_agent import DigestAgent

class DigestService():
    def __init__(self):
        self.bucket_name = "portfolia-daily-digest"
        self.prefix = "digests"
        self.region = "us-east-2"
        self.s3 = boto3.resource("s3", region_name=self.region)
        
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