from datetime import datetime,timezone
from botocore.exceptions import ClientError


#*Logger
import logging
logger = logging.getLogger(__name__)



class DynamoDBStorage:
    def __init__(self,dynamodb_client) -> None:
        self._table = dynamodb_client
        
        
        
    def save_thumbnail(self,item_id:str,url_path:str,thumbnail_size_bytes:int) -> bool:
        #!-----item_id should be created by uuid5
        now = datetime.now(timezone.utc).isoformat()
        
        item = {
            'id': item_id,
            'entityType': 'THUMBNAIL',
            'url': url_path,
            'sizeBytes': thumbnail_size_bytes,
            'sizeKB': f'{thumbnail_size_bytes / 1024:.1f} KB',
            'createdAt': now,
            'updatedAt':now,
        }
        try:
            self._table.put_item(Item=item,ConditionExpression='attribute_not_exists(id)') 
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return False
            raise
        
    

    def delete_thumbnail(self, item_id: str) -> bool:
        try:
            self._table.delete_item(Key={'id': item_id})
            return True
        except:
            return False 
        
  