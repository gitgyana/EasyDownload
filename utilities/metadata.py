import os
import json
from datetime import datetime


DATA_CACHE = f'cache_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
DATA_FILE = os.path.join('cache', DATA_CACHE)
os.makedirs('cache', exist_ok=True)

data = {}


def __create__(key, type='str'):
    if key in data:
        return

    if type == 'list':
        value = []
    elif type == 'int':
        value = 0
    elif type == 'str':
        value = ''
    elif type == 'dict':
        value = {}
    elif type == 'float':
        value = 0.0
    elif type == 'bool':
        value = False
    else:
        raise ValueError(f"Unsupported type: {type}")

    data[key] = value
    

def __initialize__():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)


def __load__():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception as load_err:
        __initialize__()
        return __load__()


def __save__(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def update(**kwargs):
    data = __load__()
    for key, value in kwargs.items():
        if key not in data:
            __create__(key, type='str')

        data[key] = value

    __save__(data)


def get(*args):
    data = __load__()
    result = {}
    for key in args:
        if key in data:
            result[key] = data[key]
            
    return result


def delete():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)


__initialize__()
