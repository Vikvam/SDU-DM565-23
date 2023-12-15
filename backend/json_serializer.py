import json
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from backend.google_api.datetime_converter import convert_datetime_to_str


def encode_json(data):
    return jsonable_encoder(data, custom_encoder={datetime: convert_datetime_to_str})


def write_to_json_file(file, data):
    json_object = json.dumps(data, indent=4, ensure_ascii=False, default=json_serialize).encode("utf-8")
    json_object = json_object.decode() + "\n"
    file.write(json_object)


def json_serialize(obj):
    if isinstance(obj, datetime):
        return convert_datetime_to_str(obj)
    raise TypeError("Type %s not serializable" % type(obj))
