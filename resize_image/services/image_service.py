import uuid
from PIL.ImageFile import ImageFile
from PIL.Image import Image
from storage import S3Storage,DynamoDBStorage
from processors import ImageProcessor





#*Logger
import logging
logger = logging.getLogger(__name__)

class ImageService:
    def __init__(self, s3_storage:S3Storage,processor:ImageProcessor, output_bucket:str, metadata_store:DynamoDBStorage) -> None:
        self._s3_storage = s3_storage
        self._metadata_store = metadata_store
        self._processor = processor
        self._output_bucket = output_bucket
        
        
    def processImage(self, src_bucket:str,src_key:str, dst_key:str, etag:str | None = None) -> str:
        """
        Download an image from S3, create a thumbnail,
        and upload the processed image to the output bucket.

        Args:
            src_bucket (str): The source S3 bucket name.
            src_key (str): The source object's key.
            dst_key (str): The destination key for the thumbnail.

        Returns:
            str: The S3 URI of the uploaded thumbnail.
        """
        image: ImageFile = self._s3_storage.downloadImage(bucket=src_bucket,key=src_key)
        thumbnail = self._processor.createThumbnail(image=image)
        uri, size_bytes = self._s3_storage.uploadImage(image=thumbnail,bucket=self._output_bucket,key=dst_key)
        item_id = self._make_id(src_bucket,src_key,etag=etag)
        
        self._metadata_store.save_thumbnail(
            item_id=item_id,
            url_path=uri,
            thumbnail_size_bytes=size_bytes)
        
        logger.info("Image processed", extra={"id": item_id, "src_key": src_key, "dst_key": dst_key})
        
        return item_id
    
    @staticmethod
    def _make_id(bucket:str, key:str, etag:str |None):
        """Same object (bucket + key + etag) always gets the same id."""
        return str(uuid.uuid5(uuid.NAMESPACE_URL,f"{bucket}/{key}/{etag or ''}"))
        
        
        
        
