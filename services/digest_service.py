import json
from datetime import datetime
from zoneinfo import ZoneInfo
import boto3
from botocore.exceptions import ClientError

class DigestService():
    def __init__(self):
        self.bucket_name = "portfolia-daily-digest"
        self.prefix = "digests"
        self.region = "us-east-2"

    def _get_json(self, s3_client, key: str) -> dict:
        response = s3_client.get_object(Bucket=self.bucket_name, Key=key)
        body_bytes = response["Body"].read()
        return json.loads(body_bytes.decode("utf-8"))

    def s3_to_client(self, fallback_to_latest: bool = True):
        et = ZoneInfo("America/New_York")
        date_key = datetime.now(et).date().isoformat()
        todays_key = f"{self.prefix}/{date_key}.json"

        s3_client = boto3.client("s3", region_name=self.region)

        try:
            return self._get_json(s3_client, todays_key)
        except ClientError as e:
            code = (e.response.get("Error", {}) or {}).get("Code")
            if code not in ("NoSuchKey", "404"):
                raise

            if not fallback_to_latest:
                raise FileNotFoundError(
                    f"No digest found at s3://{self.bucket_name}/{todays_key}"
                ) from e

        # Fallback: find newest digest in prefix
        resp = s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=f"{self.prefix}/")
        contents = resp.get("Contents", [])
        json_keys = [obj for obj in contents if obj.get("Key", "").endswith(".json")]

        if not json_keys:
            raise FileNotFoundError(
                f"No digests found at s3://{self.bucket_name}/{self.prefix}/"
            )

        latest = max(json_keys, key=lambda o: o["LastModified"])
        return self._get_json(s3_client, latest["Key"])

if __name__ == "__main__":
    digest_service = DigestService()
    print(digest_service.s3_to_client())