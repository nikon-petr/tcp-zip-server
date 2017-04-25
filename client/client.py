import base64
import os
import socket

from client.request_maker import make_request
from client.response_handler import handle_response


class Client:
    @staticmethod
    def request(request_body_dictionary):

        try:
            with socket.socket() as sock:
                make_request(sock, request_body_dictionary)
                response_dictionary = handle_response(sock)
                return response_dictionary

        except ConnectionRefusedError:
            raise ServerNotFound('Server not found.')

    @staticmethod
    def get_directory_tree():
        resp = Client.request({'tree': 'info'})
        if resp.get('error'):
            raise ServerError(resp['error'])
        return resp['tree']

    @staticmethod
    def get_directory_archive(path, save_path):
        resp = Client.request({'directory': path})
        if resp.get('error'):
            raise ServerError(resp['error'])
        save_path = os.path.join(save_path, os.path.basename(path)) + '.zip'

        with open(save_path, 'wb') as zip_file:
            zip_file.write(base64.decodebytes(resp['directory'].encode()))


class ServerError(Exception):
    def __init__(self, message):
        self.message = message


class ServerNotFound(Exception):
    def __init__(self, message):
        self.message = message


if __name__ == '__main__':
    from client_ui import start_ui
    start_ui()
