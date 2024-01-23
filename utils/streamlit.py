import os
from streamlit.runtime.uploaded_file_manager import UploadedFile


def save_file(file: UploadedFile, file_name: str | None = None):
  if file is not None:
    cwd = os.getcwd()

    if file_name is None:
      file_name = file.name

    file_path = os.path.join(cwd, 'tmp', file_name)

    if os.path.exists(file_path):
      os.remove(file_path)

    with open(file_path, "wb") as f:
      f.write(file.getbuffer())
