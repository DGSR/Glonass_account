import time

from api.clients import add_client
from api.users import add_user
from credentials.cred import OWNER


def create_client(client_fields: dict, user_fields: dict = None) -> str:
    """
    create client and user for created client, using ONLY username
    REQUIRED params: username inside client_fields
    username MUST be digits
    IMPORTANT params: groups for user_fields
    :param client_fields: REQUIRES name
    :param user_fields: OPTIONAL fields for users
    :return:
    """
    client_dict = {
        'agentInfoType': '0',
        'owner': OWNER
    }
    client_dict.update(client_fields)

    new_client = add_client(fields=client_dict)
    print(new_client)

    user_dict = {
        'login': client_dict['name'],
        'parentId': new_client['client']['id']
    }
    user_dict.update(user_fields) if user_fields else 0

    time.sleep(1)

    print(add_user(fields=user_dict))

    return f'Created client and user inside it with name: {client_dict["name"]}'
