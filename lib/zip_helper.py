import base64
import io
import os
import zipfile
import tempfile


def zip_directory(relative_path, relative_for='.', exclude_hidden=True):
    absolute_path = os.path.realpath(os.path.join(relative_for, relative_path))

    if not os.path.exists(absolute_path):
        raise PathNotFound()
    if not absolute_path.startswith(os.path.realpath(relative_for)):
        raise PathNotAllowed()

    archive_bytes_stream = io.BytesIO()

    with zipfile.ZipFile(archive_bytes_stream, 'w', zipfile.ZIP_BZIP2) as zip_file:
        for root, dirs, files in os.walk(absolute_path):

            if exclude_hidden:
                files = [f for f in files if not f[0] == '.']
                dirs[:] = [d for d in dirs if not d[0] == '.']

            for file in files:
                archive_file_path = os.path.join(os.path.realpath(root).replace(absolute_path, ''), file)
                zip_file.write(os.path.join(root, file), archive_file_path)

    return base64.encodebytes(archive_bytes_stream.getvalue()).decode()


class PathNotFound(Exception):
    pass


class PathNotAllowed(Exception):
    pass
