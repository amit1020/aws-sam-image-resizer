from datetime import datetime,timezone
import uuid
from boto3.dynamodb.conditions import Key

#*Logger
import logging
logger = logging.getLogger(__name__)

class DynampDBStorage:
    def __init__(self,dynamodb_client) -> None:
        self._table = dynamodb_client
        
        
        
    def putItem(self,url_path:str,thumbnail_size_bytes:int) -> bool:
        now = datetime.now(timezone.utc).isoformat()
        
        item = {
            'id': str(uuid.uuid4()),
            'url': url_path,
            'sizeBytes': thumbnail_size_bytes,
            'sizeKB': f'{thumbnail_size_bytes / 1024:.1f} KB',
            'createdAt': now,
            'updateAt':now,
        }
        try:
            self._table.put_item(Item=item,ConditionExpression='attribute_not_exists(id)') 
            return True
        except Exception as e:
            print(e)
            return False 
        
        
    

    def delete_thumbnail(self, item_id: str) -> bool:
        try:
            self._table.delete_item(Key={'id': item_id})
            return True
        except:
            return False 
        
  