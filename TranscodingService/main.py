import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import json
from kafka import KafkaConsumer, KafkaProducer
import logging
import os
import time
import yaml
import transcoder

if __name__ == "__main__":
    logging.info("Starting transcoding service")
    with open("config.yaml", "rb") as config_file:
        config = yaml.safe_load(config_file)

    consumer_config = config['transcode_consumer']
    producer_config = config['post_transcode_producer']
    s3_config = config['s3']

    logging.info("Config loaded. Waiting for Kafka to be online")

    while True:
        try:
            consumer = KafkaConsumer(
                consumer_config['topic'],
                group_id=consumer_config['group_id'],
                bootstrap_servers=consumer_config['broker'],
                auto_offset_reset='earliest',
                value_deserializer=lambda x: json.loads(x.decode('utf-8')))
            break
        except Exception as e:
            logging.error(e)
            time.sleep(1)

    seed_producer = KafkaProducer(
        bootstrap_servers=producer_config['broker'],
        value_serializer=lambda x: json.dumps(x).encode("utf-8"))

    logging.info("Connected to Kafka")

    s3 = boto3.client(
        's3',
        endpoint_url=s3_config['endpoint_url'],
        aws_access_key_id=s3_config['aws_access_key'],
        aws_secret_access_key=s3_config['aws_secret_key'],
        config=Config(signature_version=s3_config['sig_version']),
        region_name=s3_config['region']
    )

    logging.info("Waiting for messages")

    for message in consumer:
        logging.info(f"Reading trancode job from kafka: {message}")

        file = message.value['file']['object']
        bucket = message.value['file']['bucket']

        logging.info(
            f"Downalding file from s3: bucket: {bucket}, file: {file}")

        s3.download_file(bucket, file, file)

        output_filename = transcoder.transcode(
            file, metadata=message.value['metadata'])

        logging.info("Uploading trancoded files to s3")

        try:
            s3.create_bucket(Bucket="transcoded-files")
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                pass
            else:
                raise e

        s3.upload_file(output_filename, "transcoded-files", output_filename)

        seed_message = {
            "bucket": "transcoded-files",
            "object": output_filename,
            "id": file
        }

        logging.info(f"Publishing new seed job to Kafka: {seed_message}")

        seed_producer.send(producer_config['topic'], value=seed_message)

        logging.info("Cleaning up transcoded zip file")
        os.remove(output_filename)
