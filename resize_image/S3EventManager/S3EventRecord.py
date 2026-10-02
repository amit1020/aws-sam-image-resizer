from datetime import datetime
from urllib.parse import unquote_plus

class InvalidRecordError(Exception):
    """Raised when an S3 event record is missing expected fields or is malformed."""
    pass



class Record:
    IMAGE_EXTENSIONS: frozenset[str] = frozenset({"jpg", "jpeg", "png", "gif", "webp", "bmp", "tiff"})
    THUMBNAIL_PREFIX: str = "thumbnails/"
    def __init__(self,
                 event_name:str,
                 event_time: datetime,
                 bucket_name:str,
                 key: str, 
                 raw_key: str,
                 size: int | None = None,
                 etag:str  | None = None,
                 version_id: str | None = None,
                 sequencer: str | None = None,
                 arn: str | None = None
        ) -> None:
        self.event_name = event_name
        self.event_time = event_time
        self.bucket_name = bucket_name
        self.key = key
        self.raw_key = raw_key
        self.size = size
        self.etag = etag
        self.version_id = version_id
        self.sequencer = sequencer

    @classmethod
    def from_dict(cls,raw_record):
        try:
            s3_data = raw_record["s3"]
            bucket_data = s3_data["bucket"]
            object_data = s3_data["object"]
            raw_key = object_data["key"]

            return cls(
                event_name=raw_record["eventName"],
                event_time=cls._parse_event_time(raw_record["eventTime"]),
                bucket_name=bucket_data["name"],
                key=unquote_plus(raw_key),
                raw_key=raw_key,
                size=object_data.get("size"),
                etag=object_data.get("eTag"),
                version_id=object_data.get("versionId"),
                sequencer=object_data.get("sequencer"),
                arn=bucket_data.get("arn")
            )
        except KeyError as e:
            raise InvalidRecordError(f"Missing expected field: {e}") from e

    @staticmethod
    def _parse_event_time(value: str) -> datetime:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))        
    
    
    @property
    def filename(self) -> str:
        return self.key.rsplit("/", 1)[-1]
        
    
    
    @property
    def extention(self):
        #?Lowercase file extension without the leading dot, or empty if none
        name: str = self.filename
        try:
            return name.rsplit(".",1)[-1].lower()
        except Exception as e:
            raise e
    
    @property
    def is_folder_marker(self):
        #?return True for console-created folders and empty uploads.
        return self.key.endswith("/") or not self.size#Check if self.size is 0
    
    @property
    def is_image(self):
        return self.extention in self.IMAGE_EXTENSIONS
    

    @property
    def is_thumbnail(self) -> bool:
        """True if this object is itself a generated thumbnail."""
        return self.key.startswith(self.THUMBNAIL_PREFIX)

    @property
    def thumbnail_key(self) -> str:
        #?Destination key for the generated thumbnail."""
        return f"{self.THUMBNAIL_PREFIX}{self.key}"

    def should_process(self) -> bool:
        #?True if this record represents an image worth resizing."""
        return (
            not self.is_folder_marker
            and self.is_image
            and not self.is_thumbnail
        )
        
        


