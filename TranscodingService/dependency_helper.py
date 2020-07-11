import boto3
from botocore.client import Config
from kafka import KafkaConsumer, KafkaProducer
import json
import logging
import time

def get_kafka_consumer(consumer_config):
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
    return consumer

def get_kafka_producer(producer_config):
    return KafkaProducer(
        bootstrap_servers=producer_config['broker'],
        value_serializer=lambda x: json.dumps(x).encode("utf-8"))

def get_s3_client(s3_config):
    return boto3.client(
        's3',
        endpoint_url=s3_config['endpoint_url'],
        aws_access_key_id=s3_config['aws_access_key'],
        aws_secret_access_key=s3_config['aws_secret_key'],
        config=Config(signature_version=s3_config['sig_version']),
        region_name=s3_config['region']
    )
