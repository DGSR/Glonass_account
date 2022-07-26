from api.base_request import base_delete, base_find, base_add, base_get
from credentials.config import BASE_URL, MODELS_BASE_URL


def get_model(model_id: str) -> dict:
    url = BASE_URL + MODELS_BASE_URL + model_id
    return base_get(url)


def add_model(**kwargs) -> dict:
    url = BASE_URL + MODELS_BASE_URL
    return base_add(url, kwargs, 'name', 'model')
