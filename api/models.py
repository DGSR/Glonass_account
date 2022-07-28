from api.base_request import base_delete, base_find, base_add, base_get
from api.autofill import autofill_model
from credentials.config import BASE_URL, MODELS_BASE_URL


def get_model(model_id: str) -> dict:
    url = BASE_URL + MODELS_BASE_URL + model_id
    return base_get(url)


def add_model(owner, **kwargs) -> dict:
    url = BASE_URL + MODELS_BASE_URL
    body = autofill_model(owner)
    body.update(**kwargs)
    return base_add(url, body, 'name', 'model')
