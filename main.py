from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
import os

from requests.NewFileRequest import NewFileRequest

app = FastAPI()
FILES_DIR = "resources/"


@app.get("/")
def root(response: Response):
  response.headers['Content-Type'] = 'application/json'
  response.status_code = status.HTTP_200_OK
  return {"message": "Accediste al endpoint de prueba"}


@app.get("/files",
         tags=["FILES"],
         summary="Get all file names",
         description="Retrieve a list of all files in the system.")
def get_files(response: Response):
  response.headers['Content-Type'] = 'application/json'
  data = _get_files_names()
  return JSONResponse(content={'data':data}, status_code=200)


@app.post("/files",
          tags=["FILES"],
          summary="Create a new file",
          description="Create a new file in the system.")
def create_new_file(request: NewFileRequest, response: Response):
  response.headers['Content-Type'] = 'application/json'
  response.status_code = status.HTTP_201_CREATED
  _create_file_with_name(request.file_name, request.file_content)
  return response


@app.get("/files/{file_name}",
         tags=["FILES"],
         summary="Obtain content of a file ",
         description="Get file content.")
def get_file_content(file_name: str, response: Response):
  response.headers['Content-Type'] = 'application/json'
  return JSONResponse(content={'data': _read_file(file_name)}, status_code=200)


def _read_file(file_name: str):
  with open(f'{FILES_DIR}/{file_name}', 'r') as file:
    return file.read()


def _create_file_with_name(file_name, file_content):
  with open(f'{FILES_DIR}/{file_name}', 'w') as file:
    file.write(file_content)


def _get_files_names():
  file_names = []
  for item_name in os.listdir(FILES_DIR):
    item_full_path = os.path.join(FILES_DIR, item_name)
    if os.path.isfile(item_full_path):
      file_names.append(item_name)
  return file_names
