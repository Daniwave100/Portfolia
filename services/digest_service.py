import json
from datetime import datetime
from zoneinfo import ZoneInfo
import boto3

class DigestService():
    def __init__(self):
        self.bucket_name = "portfolia-daily-digest"
        self.prefix = "digests"
        self.region = "us-east-2"

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

if __name__ == "__main__":
    digest_service = DigestService()
    path = digest_service.digest_to_s3()
    print(path)

