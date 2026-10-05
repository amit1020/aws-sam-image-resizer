import json, boto3 

#!Test - delete after that
from .config import load_config
from .S3EventManager import S3Event
from .processors import ImageProcessor
from .services import ImageService
from .storage import S3Storage, DynamoDBStorage

"""roduction
from config import load_config
from S3EventManager import S3Event
from processors import ImageProcessor
from services import ImageService
from storage import S3Storage, DynamoDBStorage
"""





# import requests
#*Logger
import logging
logger = logging.getLogger(__name__)

def resize_image_handler(event, context):


    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
