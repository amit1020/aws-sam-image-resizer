from dataclasses import dataclass

from S3EventManager.S3Event import S3Event

import logging,json,os 
from PIL import Image, ImageOps
from PIL.ImageFile import ImageFile
from io import BytesIO





class ImageProcessor:
    def __init__(self,s3_client,config) -> None:
        self.s3 = s3_client
        self.config = config
        
        
        
        
    