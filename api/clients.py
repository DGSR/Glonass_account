from copy import deepcopy
from typing import List
import requests
import time

from api.autofill import auto_fill_client
from api import RequestException
from credentials.config import (BASE_URL, HEADERS, CLIENTS_FIND_URL,
                                CLIENTS_BASE_URL)


def get_clients(parent_id: str = '') -> List:
    """
    Return basic info about clients by parentId
    :param parent_id: dict with one field
    :return: dict User from server
    """

    final_url = BASE_URL + CLIENTS_FIND_URL

    if parent_id != '':
        params = {'parentId': parent_id}
        res = requests.get(final_url, headers=HEADERS, params=params)
    else:
        res = requests.get(final_url, headers=HEADERS)

    result = res.json()

    return result


def get_client(client_id: str) -> dict:
    """
    Get all info about client using id
    :param client_id:
    :return:
    """

    final_url = BASE_URL + CLIENTS_BASE_URL + client_id
    res = requests.get(final_url, headers=HEADERS)

    if res.status_code != 200:
        print(res.content)
        raise RequestException('Something went wrong')

    result = res.json()
    return result


def add_client(name: str = '', autofill: bool = True,
               fields: dict = None) -> dict:
    """
    Adds user with fields or pass login and use autofill
    :param name: If using autofill
    :param autofill: Enables autofill
    :param fields: Add fields to the body of request
    :return: dict added user from server
    """
    request_data = {}
    if fields:
        request_data = update_fields(request_data, fields)

    client_name = request_data.get('name', name)
    if autofill:
        request_data = update_fields(auto_fill_client(client_name), request_data)

    final_url = BASE_URL + CLIENTS_BASE_URL
    res = requests.post(final_url, headers=HEADERS, json=request_data)

    result = res.json()
    if result.get('Error'):
        raise RequestException(result.get('Error'))

    return result


def update_fields(clients_fields: dict, edit_fields: dict) -> dict:
    """
    updates client_fields with edit_fields
    nested field 'clients' is updated separately
    :param clients_fields:
    :param edit_fields:
    :return:
    """
    update_dict = deepcopy(edit_fields)
    final_dict = deepcopy(clients_fields)
    clients = update_dict.get('clients', None)
    if clients:
        del update_dict['clients']
        final_dict['clients'].update(clients)
    final_dict.update(update_dict)
    return final_dict


def edit_client(client_id: str, edit_fields: dict) -> dict:
    """
    Edit client using id and fields
    :param client_id:
    :param edit_fields: updates dict with these fields
    :return:
    """
    client_fields = get_client(client_id)
    client_fields = update_fields(client_fields, edit_fields)

    time.sleep(1)

    final_url = BASE_URL + CLIENTS_BASE_URL + client_id
    res = requests.put(final_url, headers=HEADERS, json=client_fields)
    result = res.json()
    if result.get('Error'):
        raise RequestException(result.get('Error'))

    return result


def delete_client(client_ids: List) -> str:
    """
    Deletes client_ids
    client_ids passed as List of str then list get stringified and sent raw
    :param client_ids:
    :return: str result
    """
    final_url = BASE_URL + CLIENTS_BASE_URL
    req = requests.delete(final_url, headers=HEADERS, data=str(client_ids))
    print(req.request.body)
    if req.status_code != 200:
        raise f'Can not delete clients with ids {client_ids}'

    return f'Clients with id = {client_ids} have been deleted'
