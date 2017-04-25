import os


def directory_tree_to_dict(path, exclude_hidden=True):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['path'] = os.path.relpath(path, '/Users/nikon/PycharmProjects/AIS/server_shared_files')
        d['children'] = [directory_tree_to_dict(os.path.join(path, x), exclude_hidden) for x in os.listdir(path) if not x[0] == '.' or not exclude_hidden]
    else:
        d['type'] = "file"
        d['path'] = os.path.relpath(path, '/Users/nikon/PycharmProjects/AIS/server_shared_files')
    return d
