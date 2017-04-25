import os
import socket

BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../server_shared_files')

from lib.file_system_helper import directory_tree_to_dict
from lib.zip_helper import zip_directory
from lib.zip_helper import PathNotAllowed
from lib.zip_helper import PathNotFound

from server.request_handler import handle_request
from server.response_maker import make_response


def handle_error(decorating):
    def wrapper(*args):
        try:
            return decorating(*args)
        except PathNotFound:
            make_response(args[0].connection, args[0].client_address, {'error': 'Directory not found.'})
        except PathNotAllowed:
            make_response(args[0].connection, args[0].client_address, {'error': 'Directory not allowed.'})
        except KeyError:
            make_response(args[0].connection, args[0].client_address, {'error': 'Unknown request.'})
        except Exception:
            make_response(args[0].connection, args[0].client_address, {'error': 'Unknown error.'})
    return wrapper


class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 9090))
        self.socket.listen(1)

        self.connection = None
        self.client_address = None

    def run(self):
        print('run server\n')

        while True:
            self.connection, self.client_address = None, None

            try:
                self.connection, self.client_address = self.socket.accept()
                req = handle_request(self.connection, self.client_address)
                self.route(req)

            except KeyboardInterrupt:
                if self.connection:
                    self.connection.close()
                print('server stopped\n')
                break

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
