from .S3EventRecord import InvalidRecordError,Record

#*Logger
import logging
logger = logging.getLogger(__name__)


class S3Event:
    def __init__(self, records: list[Record]) -> None:
        self.records = records

    @classmethod
    def from_dict(cls,raw_event):
        records = []
        for raw_record in raw_event.get("Record",[]):
            try:
                records.append(Record.from_dict(raw_event))
            except InvalidRecordError as e :
                logger.warning("Skipping malformed record: %s", e)
        return cls(records)
        
    @property
    def image_records(self):
        return[record for record in self.records if record.should_process()]

    def __len__(self):
        return len(self.records)
    
    def __iter__(self):
        return iter(self.records)
        