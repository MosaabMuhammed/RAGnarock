from pydantic import BaseModel
from typing import Optional

class ProcessData(BaseModel):
    file_id: str = None
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 0
    do_reset: Optional[int] = 0