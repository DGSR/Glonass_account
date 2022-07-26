import datetime
from credentials.cred import OWNER


def autofill_user(login: str, client_id: str) -> dict:
    """
    Глонасс Soft user autofill
    :param login: user's login
    :param client_id: client
    :return: dict
    """
    d = datetime.datetime.now()
    return {
        # 'login': login,   #  v3
        'name': login,
        'email': login + '@tspb.su',
        'password': d.strftime("%d%m%Y"),
        # 'parentId': client,  #  v3
        'agentGuid': client_id,
        'phone': login,
        'firstName': login,
        'lastName': login,
        'organization': login,
        'description': login,
        'position': login,
        'isEnabled': True,
        'groups': [],
        'language': 1,
        'customGroups': ['f471d984-9bc1-44e1-a4a3-93eb83add545']  # Клиент
    }


def autofill_client(name: str) -> dict:
    """
    Глонасс Soft client autofill
    :param name: client's name
    :return:
    """
    return {
        'name': name,
        'agentInfoType': 0,
        'owner': OWNER,
        'client': {
            'accFullName': name
        }
    }


def autofill_model(owner: str):
    """
    Глонасс Soft model autofill
    :param owner: client's id who owns model type
    :return:
    """
    return {
        'modelType': 3,
        'name': 'Транспорт',
        'owner': owner
    }
