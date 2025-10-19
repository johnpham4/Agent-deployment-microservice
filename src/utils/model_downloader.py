import boto3
from dotenv import load_dotenv
import os
from tqdm.auto import tqdm

def load_model_from_s3(s3_prefix: str, local_dir: str = "downloaded_model"):
    """
    Download an entire model directory (e.g., from MLflow-registered S3 prefix).
    Example s3_prefix: "models/health-llm/b3f91d2b6f42464aab9b9ff07d22ad89"
    """

    load_dotenv()

    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_DEFAULT_REGION", "ap-southeast-2")
    bucket_name = os.getenv("AWS_BUCKET_NAME", "mlflow-artifacts-monitor")

    if not all([aws_access_key, aws_secret_key, bucket_name]):
        raise ValueError("Missing AWS credentials or bucket name in .env file")

    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )

    os.makedirs(local_dir, exist_ok=True)

    paginator = s3.get_paginator("list_objects_v2")
    total_files = 0

    # Đếm file trước (để tqdm chạy đẹp)
    for page in paginator.paginate(Bucket=bucket_name, Prefix=s3_prefix):
        for obj in page.get("Contents", []):
            total_files += 1

    with tqdm(total=total_files, desc=f"Downloading model from {s3_prefix}") as pbar:
        for page in paginator.paginate(Bucket=bucket_name, Prefix=s3_prefix):
            for obj in page.get("Contents", []):
                key = obj["Key"]
                local_path = os.path.join(local_dir, os.path.relpath(key, s3_prefix))
                os.makedirs(os.path.dirname(local_path), exist_ok=True)

                s3.download_file(bucket_name, key, local_path)
                pbar.update(1)

    print(f"Model downloaded successfully → {local_dir}")
    return local_dir