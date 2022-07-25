from copy import deepcopy
from typing import List
import requests
import time

from api.autofill import auto_fill_client
from api.base_request import base_delete, base_add, base_edit, base_get
from credentials.config import (BASE_URL, HEADERS, CLIENTS_FIND_URL,
                                CLIENTS_BASE_URL)


def get_client(client_id: str) -> dict:
    final_url = BASE_URL + CLIENTS_BASE_URL + client_id
    return base_get(final_url)


def delete_client(client_ids: List) -> str:
    final_url = BASE_URL + CLIENTS_BASE_URL
    return base_delete(final_url, client_ids, 'clients')


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


def add_client(name: str = '', autofill: bool = True,
               fields: dict = None) -> dict:
    """
    prepares data for adding
    """
    request_data = {}
    if fields:
        request_data = update_fields(request_data, fields)

    client_name = request_data.get('name', name)
    if autofill:
        request_data = update_fields(auto_fill_client(client_name), request_data)

    final_url = BASE_URL + CLIENTS_BASE_URL
    return base_add(final_url, request_data, 'name', 'client')


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


def edit_client(client_id: str, edit_fields: dict) -> str:
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
    return base_edit(final_url, client_fields, client_id, 'client')
