from credentials.cred import USERNAME, PASSWORD, CRED_FILE
from credentials.config import HEADERS
from api.authentication import auth, check_auth, write_down_token
from api.exceptions import GlonassSoftError
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

        print(res)

    except Exception as e:
        print(e)
        return None
    return None


if __name__ == '__main__':
    main()
