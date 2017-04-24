from lib.json_helper import decode_json


def handle_response(sock):
    print('handle response')

    response_pack = sock.recv(1024)
    print('receiving response...')
    response = response_pack
    while True:
        response_pack = sock.recv(1024)
        response += response_pack
        print('receiving response...')
        if not response_pack:
            break
    print('received response: ', response)

    response_dictionary = decode_json(response)
    print('decoded request: %s\n' % response_dictionary)

    return response_dictionary
