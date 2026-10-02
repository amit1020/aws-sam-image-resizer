from datetime import datetime
from urllib.parse import unquote_plus

class InvalidRecordError(Exception):
    """Raised when an S3 event record is missing expected fields or is malformed."""
    pass



class Record:
    IMAGE_EXTENSIONS: frozenset[str] = frozenset({"jpg", "jpeg", "png", "gif", "webp", "bmp", "tiff"})
    THUMBNAIL_PREFIX: str = "thumbnails/"
    def __init__(self) -> None:
        pass