from lib.json_helper import decode_json


def handle_request(connection, client_address):
    print('handle request from ', client_address)

    request = connection.recv(4096)
    print('received request: ', request)

    request_dictionary = decode_json(request)
    print('decoded request: %s\n' % request_dictionary)

    return request_dictionary
