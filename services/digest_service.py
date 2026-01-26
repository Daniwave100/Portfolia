# code to run agent at 8am daily
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app_agents.digest_agent import DigestAgent
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import boto3

def run_digest():
    agent = DigestAgent()
    llm_digest = agent.run_agent()
    json_str = json.dumps(llm_digest).encode("UTF-8")
    return json_str

def digest_to_s3():
    bucket_name = "portfolia-daily-digest"
    et = ZoneInfo("America/New_York")
    date_key = datetime.now(et).date().isoformat()
    s3_object_key = f"digests/{date_key}.json"

    body = run_digest()

    s3 = boto3.resource("s3")
    s3.Object(bucket_name, s3_object_key).put(
        Body=body,
        ContentType="application/json; charset=utf-8"
    )
    return f"s3://{bucket_name}/{s3_object_key}"

def s3_to_client():
    

if __name__ == "__main__":
    path = digest_to_s3()
    print(path)

# run agent
# save agent results to S3
# streamlit fetches from S3
# so forth