import os
import time
import json
import logging
import requests
import boto3
import botocore

from {{ cookiecutter.project_slug }} import {{ cookiecutter.project_slug }}


IS_LOCAL = os.environ.get("IS_LOCAL")
AWS_LAMBDA_FUNCTION_NAME = os.environ['AWS_LAMBDA_FUNCTION_NAME']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

botoconfig = botocore.config.Config(connect_timeout=300, read_timeout=300, retries={'max_attempts': 0})

if IS_LOCAL:
    LAMBDA = boto3.client(
        "lambda",
        region_name="localhost",
        endpoint_url="http://localhost:3000",
        config=botoconfig
    )
else:
    LAMBDA = boto3.client('lambda', config=botoconfig)


def lambda_error_handler_decorator(func):
    def lambda_error_handler_wrapper(event, context):
        log_level = event.get('log_level', "INFO")
        logger.setLevel(log_level.upper())
        # logger.info("## ENVIRONMENT VARIABLES")
        # logger.info(os.environ)
        # logger.info("## EVENT")
        # logger.info(event)
        public_ip = requests.get('http://checkip.amazonaws.com').text.rstrip()
        logger.info("## PUBLIC IP")
        logger.info(public_ip)
        try:
            start_time = time.time()
            func(event, context)
            body = {
                "message": "Process completed successfully!",
                "input": event
            }

            response = {
                "statusCode": 200,
                "body": json.dumps(body)
            }

            logger.info("--- %s seconds ---", (time.time() - start_time))

            return response
        except Exception as e:
            logger.error(e)
            logger.info("--- %s seconds ---", (time.time() - start_time))
            raise

    return lambda_error_handler_wrapper


@lambda_error_handler_decorator
def run(event, context):
    print("Hello, World.")
