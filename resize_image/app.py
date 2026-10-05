import json, boto3 

#!Test - delete after that
from .config import load_config
from .S3EventManager import S3Event
from .processors import ImageProcessor
from .services import ImageService
from .storage import S3Storage, DynamoDBStorage

"""!Production
from config import load_config
from S3EventManager import S3Event
from processors import ImageProcessor
from services import ImageService
from storage import S3Storage, DynamoDBStorage
"""


#*Logger
import logging
logger = logging.getLogger(__name__)


#-----Cold start vars(Class objects - config and Image_service)
config = load_config()

Image_service = ImageService(
    s3_storage= S3Storage(boto3.client("s3")),
    metadata_store=DynamoDBStorage(boto3.resource("dynamodb").Table(config.table)),
    processor= ImageProcessor(config.size),
    output_bucket=config.output_bucket,
)



def resize_image_handler(event, context):
    s3_event = S3Event.from_dict(event) #Rescue the data and make it easy to use 
    records = s3_event.image_records

    logger.info("Received event", extra={"total":len(s3_event),"to_process":len(records)})

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
