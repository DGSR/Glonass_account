from credentials.cred import USERNAME, PASSWORD, TOKEN, CRED_FILE
from credentials.config import HEADERS
from api.authentication import auth, check_auth, write_down_token
from api.sensors import add_sensors_to_object
from api.users import get_user, add_user, delete_user, find_users, edit_user
from api.clients import get_clients, delete_client
from api.objects import add_object, get_object
from api.models import get_model, add_model
from api import RequestException
from scripts import transition_to_custom_roles

import time

from credentials import test_data


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
        # time.sleep(1)
        res = None
        # names = [
        #     'геркон', 'блокировка', 'зажигание 12В', 'геркон по аналогу', 'CAN', 'штатный',
        #     'зажигание 24В', 'зажигание по проводу', '1 ДУТ', '2 ДУТ'
        #     ]
        # res = add_sensors_to_object('', 'Без ДУТ', 'блокировка')
        res = add_sensors_to_object('по проводу', 'CAN', 'блокировка')
        # [add_sensors_to_object(i) for i in names]

        # res = find_users({'login': 'developer'})
        # res = delete_user('fbe1f07a-1224-405b-b2bd-a594a3ed4226')

        # time.sleep(1)

        # res = transition_to_custom_roles.execute(user_groups_mapping)
        # edit_fields = {
        #     'firstName': 'Dick',
        #     'lastName': 'Good',
        #     'email': 'richardwell@mail.com',
        #     'password': '202020'
        # }
        # res = edit_user(test_data.d_good_id, edit_fields)

        # res = get_user(test_data.d_good_id)
        #
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
        #     'name': ''
        # }
        # res = create_client(field_clients)
        #
        print(res)

    except RequestException as e:
        print(e)
        return None


if __name__ == '__main__':
    main()
