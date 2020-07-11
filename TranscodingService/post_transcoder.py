from botocore.exceptions import ClientError
import logging
import os

def post_process(s3, file_name, bucket_name):
    try:
        s3.create_bucket(Bucket=bucket_name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            pass
        else:
            raise e

    s3.upload_file(file_name, bucket_name, file_name)
    os.remove(file_name)
