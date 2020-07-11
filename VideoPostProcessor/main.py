import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import json
from kafka import KafkaConsumer
import logging
import os
import time
import yaml
import metadata_updater
import seeder

if __name__ == "__main__":
    LOG_LEVEL = os.getenv('LOG_LEVEL', default='INFO').upper()
    logging.basicConfig(level=LOG_LEVEL)

    with open("config.yaml", "rb") as config_file:
        config = yaml.safe_load(config_file)

    kafka_config = config['kafka']
    s3_config = config['s3']
    edge_nodes = config['edge-nodes']
    metadata_storage_config = config['metadata-storage-service']

    while True:
        try:
            consumer = KafkaConsumer(
                kafka_config['topic'],
                group_id=kafka_config['group_id'],
                bootstrap_servers=kafka_config['broker'],
                value_deserializer=lambda x: json.loads(x.decode('utf-8')))
            break
        except Exception as e:
            logging.error(e)
            time.sleep(1)

    s3 = boto3.client(
        's3',
        endpoint_url=s3_config['endpoint_url'],
        aws_access_key_id=s3_config['aws_access_key'],
        aws_secret_access_key=s3_config['aws_secret_key'],
        config=Config(signature_version=s3_config['sig_version']),
        region_name=s3_config['region']
    )

    logging.info("Waiting for messages from kafka")

    for message in consumer:
        logging.info(f"Reading seed job from Kafka: {message}")

        file = message.value['object']
        bucket = message.value['bucket']
        video_id = message.value['id']

        logging.info(f"Downalding file from s3: bucket: {bucket}, file: {file}")

        s3.download_file(bucket, file, file)

        out_dir = seeder.seed(file, edge_nodes)
        logging.info(f"File successfully saved in dir: {out_dir}")

        logging.info("Marking video as live")
        metadata_updater.update_metadata(
            video_id, metadata_storage_config['host'])
