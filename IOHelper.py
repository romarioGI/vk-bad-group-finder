import json


class ErrorEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Exception):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def to_pretty(obj):
    return json.dumps(obj, indent=2, separators=(',', ': '), ensure_ascii=False, cls=ErrorEncoder)


def serialize(data, file_name):
    with open(file_name, "w") as write_file:
        json.dump(data, write_file)


def deserialize(file_name):
    with open(file_name, "r") as read_file:
        return json.load(read_file)
