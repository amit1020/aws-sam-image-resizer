import json, boto3

from resize_image.services import ImageService 

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

imageservice = ImageService(
    s3_storage= S3Storage(boto3.client("s3")),
    metadata_store=DynamoDBStorage(boto3.resource("dynamodb").Table(config.table)),
    processor= ImageProcessor(config.size),
    output_bucket=config.output_bucket,
)



def resize_image_handler(event, context):
    s3_event = S3Event.from_dict(event) #Rescue the data and make it easy to use 
    records = s3_event.image_records

    logger.info("Received event", extra={"total":len(s3_event),"to_process":len(records)})
    failed = 0 
    
    for record in records:
        try:
            imageservice.processImage(
src_bucket=record.bucket_name,
                src_key=record.key,
                dst_key=record.thumbnail_key,
                etag=record.etag
            )
        except Exception:
            failed +=1
            logger.exception("Failed to process image",
                             extra={"bucket": record.bucket_name, "key": record.key})
    if failed:
        raise RuntimeError(f"{failed} of {len(records)} records failed")

    return {"processed": len(records)}
    
