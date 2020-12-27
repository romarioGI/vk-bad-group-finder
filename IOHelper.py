import json
import pickle


class ErrorEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Exception):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def to_pretty(obj):
    return json.dumps(obj, indent=2, separators=(',', ': '), ensure_ascii=False, cls=ErrorEncoder)


def json_serialize(data, file_name, pretty=False):
    if pretty:
        with open(file_name, 'w', encoding='utf-8') as write_file:
            json.dump(data, write_file, indent=2, separators=(',', ': '), ensure_ascii=False)
    else:
        with open(file_name, 'w', encoding='utf-8') as write_file:
            json.dump(data, write_file)


def json_deserialize(file_name):
    with open(file_name, 'r', encoding='utf-8') as read_file:
        return json.load(read_file)


def pickle_serialize(data, file_name: str):
    with open(file_name, 'wb') as write_file:
        pickle.dump(data, write_file)


def pickle_deserialize(file_name: str):
    with open(file_name, 'rb') as read_file:
        return pickle.load(read_file)
