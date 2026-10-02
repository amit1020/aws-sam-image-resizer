from dataclasses import dataclass

@dataclass
class Config:
    size : int 
    output_bucket: str
    table:str


