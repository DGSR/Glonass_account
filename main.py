from credentials.cred import USERNAME, PASSWORD, TOKEN, CRED_FILE
from credentials.config import HEADERS
from api.authentication import auth, check_auth, write_down_token
from api.users import add_user, get_user, delete_user, edit_user, find_users
from api.objects import find_object, add_object
from api.clients import get_clients, add_client, delete_client, get_client, edit_client
from api import RequestException
from create_client_user import create_client

import time

from credentials.test_data import d_good_parent, delete_user_token, owner, modelId, edit_user_id, get_client_token


def get_token():
    try:
        token = auth(USERNAME, PASSWORD)
    except RequestException as e:
        print(e)
        return None
    return token


def main():
    print('Start')
    token = TOKEN
    if not check_auth():
        token = get_token()
        write_down_token(token, CRED_FILE)
    HEADERS['X-Auth'] = token

    try:
        time.sleep(1)
        res = None
        # res = find_users({'login': 'developer'})
        # res = find_users({'userId': edit_user_id})
        # res = delete_user(delete_user_token)

        # res = add_user('developer8', False, d)

        edit_fields = {
            'firstName': 'Иван',
            'lastName': 'Федоров',
            'customGroups': ['Клиент']
        }
        # res = edit_user(edit_user_id, edit_fields)
        # res = get_user(edit_user_id)

        # res = find_object({'name': 'devmobil'})

        # res = add_object(fields_objects)
        #
        # res = get_clients(d_good_parent)

        # res = get_client(token)

        # edit_fields = {
        #     'client': {
        #         'accFullName': 'DEVO PS 4'
        #     }
        # }
        # res = edit_client(get_client, edit_fields)

        # field_clients = {
        #     'owner': d_good_parent,
        #     'agentInfoType': '0'
        # }
        # res = add_client('DEV5', True, field_clients)

        # res = delete_client([])

        # field_clients = {
        #     'name': '9090194590'
        # }
        # res = create_client(field_clients)

        print(res)

    except RequestException as e:
        print(e)
        return None


if __name__ == '__main__':
    main()
