import io
import socket

from lib.json_helper import encode_json


def make_response(connection, client_address, response_dictionary):
    print('making response for ', client_address)

    response = encode_json(response_dictionary)
    response_stream = io.BytesIO(response)
    print('encoded response: ', response)

    response_pack = response_stream.read(1024)
    print('sending response...')
    while response_pack:
        connection.sendall(response_pack)
        response_pack = response_stream.read(1024)
        print('sending response...')
    print('sent response\n')

    connection.shutdown(socket.SHUT_WR)

