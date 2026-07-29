from pydantic import BaseModel


class Source(BaseModel):
    file_name: str
    page: int