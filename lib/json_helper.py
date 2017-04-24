import json


def decode_json(bytes_string):
    json_string = bytes_string.decode()
    return json.loads(json_string)


def encode_json(dictionary):
    json_string = json.dumps(dictionary)
    bytes_string = json_string.encode()
    return bytes_string