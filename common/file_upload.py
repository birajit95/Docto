import os
from DOCTO.settings import BASE_DIR
from datetime import datetime
import time


def generate_unique_identifier():
    return str(datetime.now()).replace('-', "").replace(':', "").replace(" ", "").replace('.', "") + str(
        time.time()).replace('.', '')


def upload_file(file, subdir):
    uniqe_file_identifier = generate_unique_identifier()
    unique_file_name = uniqe_file_identifier + "_" + file._name
    filename = os.path.join(BASE_DIR, 'uploaded_files', subdir, unique_file_name)
    with open(filename, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    return filename
