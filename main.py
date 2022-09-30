from credentials.cred import USERNAME, PASSWORD, CRED_FILE
from credentials.config import HEADERS
from api.authentication import auth, check_auth, write_down_token
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

    token = get_token()
    write_down_token(token, CRED_FILE)

    # if not check_auth():
    #     token = get_token()
    #     write_down_token(token, CRED_FILE)
    HEADERS['X-Auth'] = token

    try:
        res = None
        # res = get_clients('')
        # time.sleep(1)

        # [add_sensors_to_object(i) for i in names]

        # res = transition_to_custom_roles.execute(user_groups_mapping)
        # res = edit_user(test_data.d_good_id, edit_fields)
        #
        # res = add_object(fields_objects)
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
