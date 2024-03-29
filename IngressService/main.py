from kafka import KafkaProducer
from json import dumps
from time import sleep
import secrets
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import requests

if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers="localhost:9092", value_serializer=lambda x: dumps(x).encode('utf-8'))

    s3 = boto3.client('s3',
                        endpoint_url="http://localhost:9000",
                        aws_access_key_id="dev_access_key",
                        aws_secret_access_key="dev_secret_key",
                        config = Config(signature_version='s3v4'),
                        region_name='us-east-1'
    )

    file_name = "1280.mp4"

    s3_filename = secrets.token_hex(20) + file_name
    
    title = "Sintel"
    subtitle = "Blender foundation presents"
    synopsis = "The dragon movie you'll never forget"

    requests.post("http://localhost:4000/v1/store/video", json = {
        'title': title,
        'subtitle': subtitle,
        'synopsis': synopsis,
        'id': s3_filename
    })

    try:
        s3.create_bucket(Bucket="transcode-jobs")
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            pass
        else:
            raise e

    s3.upload_file(file_name, "transcode-jobs", s3_filename)


    message = {
        'file': {
            "bucket": "transcode-jobs",
            "object": s3_filename
        },
        'metadata': {
            'targets': [
                {
                    'bitrate': 4000,
                    'resolution': 1080
                }, 
                {
                    'bitrate': 2400,
                    'resolution': 720
                }
            ]
        }
    }

    producer.send("transcode", value=message)
    producer.flush()
