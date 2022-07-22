import time
import requests

from api.autofill import auto_fill_user
from api import RequestException

from credentials.config import (BASE_URL, HEADERS, USERS_BASE_URL,
                                USERS_FIND_URL, USERS_GET_URL)


def find_users(token: str, search_parameter: dict) -> dict:
    """
    Gets user by search parameter
    :param token: Authentication token# res = add_user(token, 'developer8', False, d)
    :param search_parameter: dict with one field
    :return: dict User from server
    """
    headers = HEADERS
    headers['X-Auth'] = token

    final_url = BASE_URL + USERS_FIND_URL
    res = requests.post(final_url, headers=headers, json=search_parameter)
    result = res.json()[0]
    if result.get('Error'):
        raise RequestException(result.get('Error'))

    return result


def get_user(token: str, user_id: str) -> dict:
    """
    Gets all user details by id
    :param token:
    :param user_id:
    :return:
    """
    headers = HEADERS
    headers['X-Auth'] = token

    final_url = BASE_URL + USERS_GET_URL + user_id
    res = requests.get(final_url, headers=headers)
    result = res.json()
    print(result)
    if res.status_code != 200:
        raise RequestException('Something went wrong')

    return result


def add_user(token: str, login: str = '', autofill: bool = True,
             fields: dict = None) -> str:
    """
    Adds user with fields or pass login and use autofill
    :param token: Authentication token
    :param login: If using autofill
    :param autofill: Enables autofill
    :param fields: Add fields to the body of request
    :return: dict added user from server
    """
    request_data = {}
    user_name = fields.get('login', login)
    if autofill:
        request_data.update(auto_fill_user(user_name))
    if fields:
        request_data.update(fields)

    headers = HEADERS
    headers['X-Auth'] = token

    final_url = BASE_URL + USERS_BASE_URL

    res = requests.post(final_url, headers=headers, json=request_data)
    result = res.json()
    if result.get('Error'):
        return result.get('Error')

    return f'Created user with name: {user_name}'


def delete_user(token: str, user_id: str) -> str:
    """
    Delete user by id
    :param token: Authentication token
    :param user_id:
    :return:
    """
    headers = HEADERS
    headers['X-Auth'] = token

    final_url = BASE_URL + USERS_BASE_URL + user_id
    res = requests.delete(final_url, headers=headers)
    if res.status_code != 200:
        raise RequestException('Something went wrong')

    return f'User with id = {user_id} has been deleted'


def edit_user(token: str, user_id: str, edit_fields: dict) -> dict:
    """
    Edit user fields by id.
    First get user by id and then merge user fields with edit fields
    :param token: Authentication token
    :param user_id: user id string
    :param edit_fields: dict with fields that should be changed
    :return: user dict from server
    """
    user_fields = get_user(token, user_id)
    user_fields.update(edit_fields)
    user_fields['login'] = user_fields['name']

    headers = HEADERS
    headers['X-Auth'] = token

    time.sleep(1)

    final_url = BASE_URL + USERS_BASE_URL
    res = requests.put(final_url, headers=headers, json=user_fields)
    result = res.json()
    if result.get('Error'):
        raise RequestException(result.get('Error'))

    return result
