import json

def json_reader(json_path:str):
    with open(json_path) as fd:
        json_data=json.load(fd)
    return json_data


