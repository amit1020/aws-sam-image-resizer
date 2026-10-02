from dataclasses import dataclass
import os 

@dataclass(frozen=True)
class Config:
    size : int 
    output_bucket: str
    table:str


def load_config():
    return Config(int(os.environ["THUMBNAIL_SIZE"]),
                  os.environ["OUTPUT_BUCKET"],
                  os.environ["TABLE_NAME"])
