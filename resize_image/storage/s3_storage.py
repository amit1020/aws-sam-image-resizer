from PIL import Image
from PIL.ImageFile import ImageFile
from io import BytesIO 


class S3Storage:
    def __init__(self,s3_client) -> None:
        self._s3 = s3_client
        

    def downloadImage(self,bucket: str, key:str):
        """
        Download an image from S3 and load it into memory as a PIL image.

        Args:
            bucket (str): The source S3 bucket name.
            key (str): The source object's key.

        Returns:
            ImageFile: A PIL image created from the downloaded object data.
        """
        image_bytes = self._s3.get_object(Bucket=bucket,Key=key)["Body"].read()
        return Image.open(fp=BytesIO(initial_bytes=image_bytes))
        
    
    
    
    
    def uploadImage(self,image:ImageFile,bucket:str,key:str):
        """
        Upload a PIL image to an S3 bucket as a PNG file.

        Args:
            image (ImageFile): The image to upload.
            bucket (str): The destination S3 bucket name.
            key (str): The object's key in the S3 bucket.

        Returns:
            str: The S3 URI of the uploaded image.
        """
                
        
        image_buffer = BytesIO()
        try:
            image.save(image_buffer,'PNG')
            image_buffer.seek(0) #Set the cursor at the beggining 
            
            response = self._s3.put_object(        
                Body=image_buffer,
                Bucket=bucket,
                ContentType=f'image/png',
                Key=key                 
                
            )
            #TODO check the response 
            
            
        
            url = f"s3://{bucket}/{key}"
            #TODO: Add the new image to the table 
            return url 
            
        except Exception as e:
            raise e 