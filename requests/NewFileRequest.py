from pydantic import BaseModel


class NewFileRequest(BaseModel):
  file_name: str
  file_content: str

