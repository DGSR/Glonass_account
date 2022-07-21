import requests
import base64

from credentials.config import (BASE_URL, AUTH_URL, AUTH_CHECK_URL,
                                HEADERS)
from api import RequestException

import os


def write_down_token(token: str, file: str) -> None:
    """
    ToDo: Delete on test or prod
    rewrite file with line 'TOKEN =' to store token value
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
    os.remove(file)
    os.rename(temp_file, file)


def base64_encoding(message: str) -> str:
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode('ascii')


def auth(username: str, password: str) -> str:
    """
    Send post request with username and base64 password
    If contains field error
    :param username: str
    :param password: str
    :return: Authentication Token (GUID)
    """
    password_encode = base64_encoding(password)
    request_data = {
        'username': username,
        'password': password_encode
    }
    final_url = BASE_URL + AUTH_URL
    res = requests.post(final_url, data=request_data)
    result = res.json()
    if result.get('Error'):
        raise RequestException(result.get('Error'))

    return result.get('AuthId')


def check_auth(token: str) -> bool:
    final_url = BASE_URL + AUTH_CHECK_URL

    headers = HEADERS
    headers['X-Auth'] = token

    req = requests.get(final_url, headers=headers)

    return False if req.status_code != 200 else True
