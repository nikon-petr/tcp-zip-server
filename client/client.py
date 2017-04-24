import base64
import os
import socket

from request_maker import make_request
from response_handler import handle_response


class Client:
    @staticmethod
    def request(request_body_dictionary):
        with socket.socket() as sock:
            make_request(sock, request_body_dictionary)
            response_dictionary = handle_response(sock)
            return response_dictionary

    @staticmethod
    def get_directory_tree():
        return Client.request({'tree': 'info'})

    @staticmethod
    def get_directory_archive(path, save_path):
        resp = Client.request({'directory': path})
        save_path = os.path.join(save_path, os.path.basename(path)) + '.zip'

        with open(save_path, 'wb') as zip_file:
            zip_file.write(base64.decodebytes(resp['directory'].encode()))


if __name__ == '__main__':
    from client_ui import start_ui
    # Client.get_directory_tree()
    # Client.get_directory_archive('img', '/Users/nikon/Desktop')
    start_ui()
