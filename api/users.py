import time

from api.autofill import auto_fill_user
from api.base_request import base_delete, base_find, base_add, base_edit, base_get

from credentials.config import (BASE_URL, USERS_BASE_URL,
                                USERS_FIND_URL)


def find_users(search_parameter: dict) -> dict:
    final_url = BASE_URL + USERS_FIND_URL
    return base_find(final_url, search_parameter)


def get_user(user_id: str) -> dict:
    final_url = BASE_URL + USERS_BASE_URL + user_id
    return base_get(final_url)


def delete_user(user_id: str) -> str:
    final_url = BASE_URL + USERS_BASE_URL  # + user_id  v3
    return base_delete(final_url, [user_id], 'user')


def add_user(login: str = '', autofill: bool = True,
             fields: dict = None) -> dict:
    """
    prepares data for adding
    """
    request_data = {}
    user_name = fields.get('login', login)
    if autofill:
        request_data.update(auto_fill_user(user_name))
    if fields:
        request_data.update(fields)

    final_url = BASE_URL + USERS_BASE_URL

    return base_add(final_url, request_data, 'login', 'user')


def edit_user(user_id: str, edit_fields: dict) -> str:
    """
    Edit user fields by id.
    First get user by id and then merge user fields with edit fields
    :param user_id: user id string
    :param edit_fields: dict with fields that should be changed
    :return: user dict from server
    """
    user_fields = get_user(user_id)
    user_fields.update(edit_fields)

    # user_fields['login'] = user_fields['name']  #  v3
    # user_fields['parentId'] = user_fields['agentGuid']  #  v3

    time.sleep(1)

    final_url = BASE_URL + USERS_BASE_URL + user_id
    return base_edit(final_url, user_fields, user_id, 'user')
