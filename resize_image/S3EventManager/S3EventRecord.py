from datetime import datetime
from urllib.parse import unquote_plus

class InvalidRecordError(Exception):
    """Raised when an S3 event record is missing expected fields or is malformed."""
    pass