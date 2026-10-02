from PIL import Image
from PIL.ImageFile import ImageFile
from io import BytesIO 


class S3Storage:
    def __init__(self,s3_client) -> None:
        self._s3 = s3_client
        
        
        

    def downloadImage(self,bucket: str, key:str):
        """_summary_
        Download pre-process image from the upload bucket
        Args:
            bucket (str): _description_
            key (str): _description_

        Returns:
            _type_: _description_
        """
        image_bytes = self._s3.get_object(Bucket=bucket,Key=key)["Body"].read()
        
        return Image.open(fp=BytesIO(initial_bytes=image_bytes))
        
    
    def uploadImage(self,image:ImageFile,bucket:str,key:str):
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
            
            
        
            url = f"s3://{bucket}/{key}"
            #TODO: Add the new image to the table 
            
            return url 
            
        except Exception as e:
            raise e 