from resize_image.storage.s3_storage import S3Storage
from resize_image.processors.ImageProcessor import ImageProcessor



class ImageService:
    def __init__(self, storage:S3Storage,processor:ImageProcessor, output_bucket:str) -> None:
        self._storage = storage
        self._processor = processor
        self._output_bucket = output_bucket