import os
import json
from datetime import datetime


DATA_CACHE = f'cache_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
DATA_FILE = os.path.join('cache', DATA_CACHE)
os.makedirs('cache', exist_ok=True)

data = {}


def __create__(key, value, set_default=True):
    global data

    if key in data and set_default:
        return

    if isinstance(value, list) or isinstance(value, set):
        value = []
    elif isinstance(value, int):
        value = 0
    elif isinstance(value, str):
        value = ''
    elif isinstance(value, dict):
        value = {}
    elif isinstance(value, float):
        value = 0.0
    elif isinstance(value, bool):
        value = False
    else:
        raise ValueError(f"Unsupported type: {type(value)}")

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
    global data
    data = __load__()

    for key, value in kwargs.items():
        if key not in data:
            __create__(key=key, value=value)
            __save__(data)
            data = __load__()

        if isinstance(data[key], list):
            if isinstance(value, list):
                data[key].extend(value)
            else:
                data[key].append(value)
        elif isinstance(data[key], dict):
            data[key].update(value)
        elif isinstance(data[key], tuple):
            raise ValueError(f"Unsupported type: {type(value)}")
        elif isinstance(data[key], int) or isinstance(value, float):
            data[key] += value
        else:
            data[key] = value

    __save__(data)


def get(*args, default=''):
    global data

    data = __load__()
    result = {}
    for key in args:
        if key in data:
            result[key] = data[key]
        else:
            __create__(key=key, value=default)
            __save__(data)
            data = __load__()
            result[key] = data[key]
    
    if len(args) == 1:
        return result[args[0]]
    
    return result


def reset(*args):
    global data

    data = __load__()
    result = {}
    for key in args:
        if key in data:
            __create__(key=key, value=data[key], set_default=False)
        else:
            __create__(key=key, value='')
        
        __save__(data)
        data = __load__()
        result[key] = data[key]
    
    if len(args) == 1:
        return result[args[0]]
    
    return result


def delete():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)


def clear():
    global data
    data = {}
    __save__(data)


__initialize__()
