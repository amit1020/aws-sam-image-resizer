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
        