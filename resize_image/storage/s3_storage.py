from PIL import Image
from PIL.ImageFile import ImageFile
from io import BytesIO 


class S3Storage:
    def __init__(self,s3_client) -> None:
        self._s3 = s3_client
        
        
        

    def downloadImage(self,bucket: str, key:str):
        
        image_bytes = self._s3.get_object(Bucket=bucket,Key=key)["Body"].read()
        
        pass
        