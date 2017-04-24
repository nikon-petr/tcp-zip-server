import socket

from lib.json_helper import encode_json


def make_request(sock, request_dictionary):
    sock.connect(('localhost', 9090))
    print('making request')

    request = encode_json(request_dictionary)
    print('request encoded: %s\n' % request)

    sock.sendall(request)
    sock.shutdown(socket.SHUT_WR)
