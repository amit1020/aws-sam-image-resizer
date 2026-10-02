from dataclasses import dataclass

from S3EventManager.S3Event import S3Event

import logging,json,os 
from PIL import Image, ImageOps
from PIL.ImageFile import ImageFile
from io import BytesIO



@dataclass
class Config:
    size:int 
    output_bucket: str
    table:str


class ImageProcessor:
    def __init__(self) -> None:
        pass