from credentials.cred import USERNAME, PASSWORD, TOKEN
from api.authentication import auth, check_auth, write_down_token
from api.users import add_user, get_user, delete_user, edit_user
from api.objects import get_object, add_object
from api.clients import get_clients, add_client, delete_client, get_client, edit_client
from api import RequestException

import time

from credentials.test_data import d_good_parent, delete_user_token, owner, modelId, edit_user_token, get_client


def get_token():
    try:
        # token = auth(USERNAME + 'h', PASSWORD)   # Wrong User for Test
        token = auth(USERNAME, PASSWORD)
    except RequestException as e:
        print(e)
        return None
    return token


def main():
    print('Start')
    token = TOKEN
    if not check_auth(token):
        token = get_token()
        write_down_token(token, 'credentials/cred.py')

    try:
        # res = get_user(token, {'login': 'developer4'})
        # print(res)
        #
        # time.sleep(1)
        #
        # res = delete_user(token, delete_user_token)
        # print(res)

        # res = add_user(token, 'developer8', False, d)
        # print(res)
        # edit_fields = {
        #     'firstName': 'Иван',
        #     'lastName': 'Иванов'
        # }
        # res = edit_user(token, edit_user_token, edit_fields)
        # print(res)

        # res = get_object(token, {'name': 'devmobil'})

        # res = add_object(token, fields_objects)
        #
        # res = get_clients(token, d_good_parent)
        #
        # res = get_client(token, get_client)
        # print(res)

        # edit_fields = {
        #     'client': {
        #         'accFullName': 'DEVO PS 4'
        #     }
        # }
        # res = edit_client(token, get_client, edit_fields)
        # print(res)

        field_clients = {
            'owner': d_good_parent,
            'agentInfoType': '1'
        }
        res = add_client(token, 'DEV4', True, field_clients)
        print(res)
        # res = add_client(token, 'DEV3', True, field_clients)
        # print(res)
        # res = delete_client(token, [])
        # print(res)

    except RequestException as e:
        print(e)
        return None


if __name__ == '__main__':
    main()
