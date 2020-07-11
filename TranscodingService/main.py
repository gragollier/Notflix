import logging
import os
import yaml

from dependency_helper import get_kafka_consumer, get_kafka_producer, get_s3_client
from post_transcoder import post_process
import transcoder

POST_TRANCODE_BUCKET = "transcoded-files"

if __name__ == "__main__":
    LOG_LEVEL = os.getenv('LOG_LEVEL', default='INFO').upper()
    logging.basicConfig(level=LOG_LEVEL)

    logging.info("Starting transcoding service")
    with open("config.yaml", "rb") as config_file:
        config = yaml.safe_load(config_file)

    consumer_config = config['transcode_consumer']
    producer_config = config['post_transcode_producer']
    s3_config = config['s3']

    logging.info("Config loaded. Waiting for Kafka to be online")

    consumer = get_kafka_consumer(consumer_config)
    seed_producer = get_kafka_producer(producer_config)
    s3 = get_s3_client(s3_config)

    logging.info("Connected to dependencies. Waiting for messages")
    for message in consumer:
        logging.info(f"Reading trancode job from kafka: {message}")

        file = message.value['file']['object']
        bucket = message.value['file']['bucket']

        logging.info(f"Downalding file from s3: bucket: {bucket}, file: {file}")

        s3.download_file(bucket, file, file)

        message_metadata = message.value['metadata']
        output_filename = transcoder.transcode(file, metadata=message_metadata)

        logging.info("Uploading trancoded files to s3 and cleaning up archive")
        post_process(s3, output_filename, POST_TRANCODE_BUCKET)

        seed_message = {
            "bucket": POST_TRANCODE_BUCKET,
            "object": output_filename,
            "id": file
        }
        logging.info(f"Publishing new seed job to Kafka: {seed_message}")

        seed_producer.send(producer_config['topic'], value=seed_message)
