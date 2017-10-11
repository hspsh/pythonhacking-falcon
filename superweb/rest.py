import json
import datetime


def json_serializer_handler(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    else:
        return None


def json_dumps(obj):
    return json.dumps(obj, default=json_serializer_handler)
