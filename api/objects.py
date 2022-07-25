from api.base_request import base_delete, base_find, base_add
from credentials.config import BASE_URL, OBJECTS_FIND_URL, OBJECTS_BASE_URL


def find_object(search_parameter: dict) -> dict:
    final_url = BASE_URL + OBJECTS_FIND_URL
    return base_find(final_url, search_parameter)


def add_object(fields: dict = None) -> dict:
    request_data = {}
    if fields:
        request_data.update(fields)

    final_url = BASE_URL + OBJECTS_BASE_URL

    return base_add(final_url, request_data, 'name', 'object')


def delete_object(object_id: str) -> str:
    final_url = BASE_URL + OBJECTS_BASE_URL + object_id
    return base_delete(final_url, object, 'object')
