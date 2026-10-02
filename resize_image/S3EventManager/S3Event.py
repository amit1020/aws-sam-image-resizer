import logging
from .S3EventRecord import InvalidRecordError,Record

logger = logging.getLogger(__name__)


class S3Event:
    def __init__(self, records: list[Record]) -> None:
        self.records = records
