from credentials.cred import USERNAME, PASSWORD, TOKEN, CRED_FILE
from credentials.config import HEADERS
from api.authentication import auth, check_auth, write_down_token
from api.users import get_user, add_user, delete_user, find_users
from api.clients import get_clients
from api.objects import add_object, get_object
from api.models import get_model, add_model
from api import RequestException
from scripts import transition_to_custom_roles

import time

from credentials.test_data import edit_user_id, model_id, d_good_parent, d, user_groups_mapping, delete_user_id, fields_objects, owner, object_id


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
        # res = get_model(model_id)
        res = add_model(d_good_parent, name='Машина')

        # res = get_object(object_id)
        # res = find_users({'login': 'developer'})
        # res = delete_user(delete_user_id)

        # res = add_user('developer00', True, d)
        # print(res)
        # time.sleep(1)

        # res = transition_to_custom_roles.execute(user_groups_mapping)
        # edit_fields = {
        #     'firstName': 'Федор',
        #     'lastName': 'Иванов',
        # }39b9a7c3-3a32-4c5c-81cb-e0888e81e108
        # res = edit_user(edit_user_id, edit_fields)

        # res = get_user('b7c363d3-ad97-4bb5-81a7-bf71d97b0a1f')

        # res = find_object({'name': 'devmobil'})

        # res = add_object(fields_objects)

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
        #
        print(res)

    except RequestException as e:
        print(e)
        return None


if __name__ == '__main__':
    main()
