import json

# import requests
#*Logger
import logging
logger = logging.getLogger(__name__)

def resize_image_handler(event, context):



    

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
