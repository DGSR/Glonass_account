import requests

from api import RequestException

from credentials.config import (BASE_URL, HEADERS, OBJECTS_FIND_URL,
                                OBJECTS_ADD_URL, OBJECTS_DELETE_URL)


def get_object(search_parameter: dict) -> dict:
    """
    Gets user by search parameter
    :param search_parameter: dict with one field
    :return: dict User from server
    """

    final_url = BASE_URL + OBJECTS_FIND_URL
    res = requests.post(final_url, headers=HEADERS, json=search_parameter)
    result = res.json()[0]
    if result.get('Error'):
        raise RequestException(result.get('Error'))

    return result


def add_object(fields: dict = None) -> str:
    """
    Adds object with fields or pass login and use autofill
    fields REQUIRES: name, deviceTypeId, imei, modelId, owner
    :param fields: Add fields to the body of request
    :return: dict added user from server
    """
    request_data = {}
    request_data.update(fields)

    final_url = BASE_URL + OBJECTS_ADD_URL

    res = requests.post(final_url, headers=HEADERS, json=request_data)
    result = res.json()
    if result.get('Error'):
        return result.get('Error')

    return f'Created object with name: {request_data["name"]}'


def delete_object(object_id: str) -> str:
    """
    Deletes object by id
    :param object_id:
    :return:
    """
    final_url = BASE_URL + OBJECTS_DELETE_URL + object_id
    res = requests.delete(final_url, headers=HEADERS)
    if res.status_code != 200:
        raise RequestException('Something went wrong')

    return f'User with id = {object_id} has been deleted'
