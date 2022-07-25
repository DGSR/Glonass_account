import requests
from credentials.config import HEADERS
from api import RequestException


def base_find(url: str, search_parameter: dict) -> dict:
    """
    Gets entity by search parameter
    :param url: url to find entity
    :param search_parameter: dict with one field
    :return: entities from server matching search parameters
    """
    res = requests.post(url, headers=HEADERS, json=search_parameter)
    result = res.json()[0]
    if result.get('Error'):
        raise RequestException(result.get('Error'))

    return result


def base_get(url: str) -> dict:
    """
    Gets entity full info
    :param url: url to get entity
    :return: entity from server
    """
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        raise RequestException('Something went wrong')

    result = res.json()
    return result


def base_add(url: str, body: dict, entity_name: str, entity_hint: str) -> dict:
    """
    Adds user with fields or pass login and use autofill
    :param url: url to add entity
    :param body: request body
    :param entity_name: entity name's value in body
    :param entity_hint: string representing entity's name
    :return: status of operation
    """
    res = requests.post(url, headers=HEADERS, json=body)
    result = res.json()
    if result.get('Error'):
        return result.get('Error')

    print(f'Created {entity_hint} : {body.get(entity_name, None)}')
    return result


def base_edit(url: str, body: dict, entity_id: str, entity_hint: str) -> str:
    """
    Edit with parameters
    :param url: url to edit entity
    :param body: entity's body
    :param entity_id:
    :param entity_hint: string representing entity's name
    :return: status of operation
    """
    print(body)
    res = requests.put(url, headers=HEADERS, json=body)
    result = res.json()
    print(res.content)
    if result.get('Error'):
        return f'Error. Can NOT edit {entity_hint} : {entity_id}'
    print(result)

    return f'Edited {entity_hint} :  {entity_id}'


def base_delete(url: str, entity_id, entity_hint: str) -> str:
    """
    Delete entity by id
    :param url: url to delete entity
    :param entity_id: a string or a list with id
    :param entity_hint: string representing entity's name
    :return: status of operation
    """
    if type(entity_id) == list:
        res = requests.delete(url, headers=HEADERS, data=str(entity_id))
    else:
        res = requests.delete(url, headers=HEADERS)
    if res.status_code != 200:
        return f'Error. Can NOT delete {entity_hint} : {entity_id}'

    return f'Deleted {entity_hint} :  {entity_id}'
