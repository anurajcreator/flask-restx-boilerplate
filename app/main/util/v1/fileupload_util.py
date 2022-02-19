import os 
import boto3
import botocore
import io
import app.main.config as config
from app.main.util.v1.database import save_db

import logging
import os

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "/tmp/file_upload_service/logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'running_logs.log'), level=logging.INFO, format=logging_str,
                    filemode="a")


def aws_session():
    return boto3.session.Session(aws_access_key_id=config.S3_KEY,
                                aws_secret_access_key=config.S3_SECRET,
                                region_name=config.S3_DEFAULT_REGION)


def upload_file_to_bucket(file_path, upload_dir):
    session = aws_session()
    s3_resource = session.resource('s3')
    file_dir, file_name = os.path.split(file_path)

    bucket = s3_resource.Bucket(config.S3_BUCKET)
    bucket.upload_file(
    Filename=file_path,
    Key=upload_dir+file_name,
    ExtraArgs={'ACL': 'public-read'}
    )

    # url = config.bucket_link+upload_dir+file_name
    url = upload_dir+file_name
    # url = file_name
    return url

# s3_url = upload_file_to_bucket('app/main/files/menucategory/image4.png')
# print(s3_url) 




def download_file_from_bucket(bucket_name, s3_key, dst_path):
    session = aws_session()
    s3_resource = session.resource('s3')
    bucket = s3_resource.Bucket(bucket_name)
    bucket.download_file(Key=s3_key, Filename=dst_path)
 

def upload_data_to_bucket(bytes_data, bucket_name, s3_key):
    session = aws_session()
    s3_resource = session.resource('s3')
    obj = s3_resource.Object(bucket_name, s3_key)
    obj.put(ACL='private', Body=bytes_data)

    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
    return s3_url


def download_data_from_bucket(bucket_name, s3_key):
    session = aws_session()
    s3_resource = session.resource('s3')
    obj = s3_resource.Object(bucket_name, s3_key)
    io_stream = io.BytesIO()
    obj.download_fileobj(io_stream)

    io_stream.seek(0)
    data = io_stream.read().decode('utf-8')

    return data

def check_file(filename):
    session = aws_session()
    s3 = session.resource('s3')

    try:
        s3.Object(config.S3_BUCKET, filename).load()
        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # The object does not exist.
            return False
        else:
            # Something else has gone wrong.
            raise e