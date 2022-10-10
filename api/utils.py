import base64
import os
from typing import List


def write_down_token(token: str, file: str) -> None:
    """
    Rewrite given file with line 'TOKEN =' to store token value
    :param token: any string to write (token)
    :param file: any file to rewrite
    :return: None
    """
    temp_file = file + '.tmp'
    with open(file, 'r') as old_file:
        new_file = open(temp_file, 'w')
        for line in old_file:
            if line.startswith('TOKEN = '):
                new_file.write(f'TOKEN = \'{token}\' \n')
                continue
            new_file.write(line)
        new_file.close()
    os.remove(file)
    os.rename(temp_file, file)


def base64_encoding(message: str) -> str:
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode('ascii')


def first_index_lower(data: List) -> List:
    """
    Lowercase first letter of index. Pythonic style
    :arg data List of dicts
    """
    dict_list = []
    for counters in data:
        inside_dict = {}
        for i, v in counters.items():
            inside_dict[i[0].lower() + i[1:]] = v
        dict_list.append(inside_dict)
    return dict_list