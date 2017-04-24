import os
import socket

BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../server_files')

from lib.file_system_helper import directory_tree_to_dict
from lib.zip_helper import zip_directory
from lib.zip_helper import PathNotAllowed
from lib.zip_helper import PathNotFound

from request_handler import handle_request
from response_maker import make_response


def handle_error(decorating):
    def wrapper(*args):
        try:
            return decorating(*args)
        except PathNotFound:
            make_response(args[0].connection, args[0].client_address, {'error': 'Directory not found.'})
            raise
        except PathNotAllowed:
            make_response(args[0].connection, args[0].client_address, {'error': 'Directory not allowed.'})
            raise
        except KeyError:
            make_response(args[0].connection, args[0].client_address, {'error': 'Unknown request.'})
        except Exception:
            make_response(args[0].connection, args[0].client_address, {'error': 'Unknown error.'})
            raise
    return wrapper


class Server:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.bind(('', 9090))
        self.socket.listen(1)

        self.connection = None
        self.client_address = None

    def run(self):
        print('run server\n')

        while True:
            self.connection, self.client_address = self.socket.accept()
            req = handle_request(self.connection, self.client_address)
            self.route(req)
            # make_response(connection, client_address, {'OK': None})

    @handle_error
    def route(self, req):
        if req.get('tree'):
            self.get_directory_tree(req)
        elif req.get('directory'):
            self.get_directory_archive(req)

    def get_directory_tree(self, req):
        response_dict = {'tree': directory_tree_to_dict(BASE_DIR)}
        make_response(self.connection, self.client_address, response_dict)

    def get_directory_archive(self, req):
        response_dict = {'directory': zip_directory(req['directory'], BASE_DIR)}
        make_response(self.connection, self.client_address, response_dict)

    # def send_archive_dir(self, path):
    #     archive_file = archiver.zip_path(path)
    #     print('zipped directory')
    #
    #     print('sending archive...')
    #     pack = archive_file.read(1024)
    #     while pack:
    #         print('sending archive...')
    #         self.connection.sendall(pack)
    #         pack = archive_file.read(1024)
    #
    #     archive_file.close()
    #     print('done sending archive')
    #
    # def send_dir_tree(self):
    #     json_tree = dir_walker.json_dir_tree()
    #     print('walked directories')
    #
    #     print('sending directories tree...')
    #     self.connection.sendall(json_tree.encode())
    #
    #     print('done sending directories tree')


if __name__ == '__main__':
    server = Server()
    server.run()
