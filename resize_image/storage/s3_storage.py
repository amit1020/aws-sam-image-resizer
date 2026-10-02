from PIL import Image
from PIL.ImageFile import ImageFile



class S3Storage:
    def __init__(self,s3_client) -> None:
        self.s3 = s3_client
        
        
        