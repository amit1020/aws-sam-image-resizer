from PIL.ImageFile import ImageFile


from PIL.Image import Image


from resize_image.storage.s3_storage import S3Storage
from resize_image.processors.ImageProcessor import ImageProcessor



class ImageService:
    def __init__(self, storage:S3Storage,processor:ImageProcessor, output_bucket:str) -> None:
        self._storage = storage
        self._processor = processor
        self._output_bucket = output_bucket
        
        
    def processImage(self, src_bucket:str,src_key:str, dst_key:str) -> str:
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
        image: ImageFile = self._storage.downloadImage(bucket=src_bucket,key=src_key)
        thumbnail = self._processor.createThumbnail(image=image)
        
        return self._storage.uploadImage(image=thumbnail,bucket=self._output_bucket,key=dst_key)