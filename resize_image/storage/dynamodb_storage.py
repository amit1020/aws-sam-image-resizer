from datetime import datetime

class DynampDBStorage:
    def __init__(self,dynamodb_client) -> None:
        self.dodb = dynamodb_client
