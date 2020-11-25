import json


class ErrorEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Exception):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def to_pretty(obj):
    return json.dumps(obj, indent=2, separators=(',', ': '), ensure_ascii=False, cls=ErrorEncoder)
