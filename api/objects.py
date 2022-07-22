import requests

from api import RequestException

from credentials.config import (BASE_URL, HEADERS, OBJECTS_FIND_URL,
                                OBJECTS_ADD_URL, OBJECTS_DELETE_URL)


def get_object(token: str, search_parameter: dict) -> dict:
    """
    Gets user by search parameter
    :param token: Authentication token
    :param search_parameter: dict with one field
    :return: dict User from server
    """
    headers = HEADERS
    headers['X-Auth'] = token

    final_url = BASE_URL + OBJECTS_FIND_URL
    res = requests.post(final_url, headers=headers, json=search_parameter)
    result = res.json()[0]
    if result.get('Error'):
        raise RequestException(result.get('Error'))

    return result


def add_object(token: str, fields: dict = None) -> dict:
    """
    Adds user with fields or pass login and use autofill
    :param token: Authentication token
    :param fields: Add fields to the body of request
    :return: dict added user from server
    """
    request_data = {}
    request_data.update(fields)

    headers = HEADERS
    headers['X-Auth'] = token

    final_url = BASE_URL + OBJECTS_ADD_URL
    print(request_data)
    res = requests.post(final_url, headers=headers, json=request_data)
    result = res.json()
    if result.get('Error'):
        raise RequestException(result.get('Error'))

    return result


def delete_object(token: str, object_id: str) -> str:
    """
    Deletes object by id
    :param token:
    :param object_id:
    :return:
    """
    headers = HEADERS
    headers['X-Auth'] = token

    final_url = BASE_URL + OBJECTS_DELETE_URL + object_id
    res = requests.delete(final_url, headers=headers)
    if res.status_code != 200:
        raise RequestException('Something went wrong')

    return f'User with id = {object_id} has been deleted'
