from typing import List, Dict
import base64
import requests
from credentials import settings
from credentials.cred import USERNAME, PASSWORD
from api.exceptions import RequestException, GlonassSoftError
from api.authentication import auth_from_creds
import time


class GSApi:

    def __init__(self):

        self.headers = settings.HEADERS
        self.token = auth_from_creds()
        self.headers['X-Auth'] = self.token
        self.last_request_time = time.time()

    def refresh_headers(self):
        self.headers['X-Auth'] = auth_from_creds()

    def request_handler(self, req: requests.Request,
                        retries: int = 3) -> Dict:
        """
        handles prepared Request
        if response is 429 then sleep and retry number of retries
        :param req: prepared Request to be sent
        :param retries: number of retries (default  3)
        :return: response
        """
        session = requests.Session()
        # start = time.time()  # log
        # print('First request', start)  # log
        for _ in range(retries):
            r = req.prepare()
            print(req.method)
            print(req.url)
            print(req.data)
            print(req.headers)
            resp = session.send(r)
            time_diff = time.time() - self.last_request_time
            self.last_request_time = time.time()
            if resp.status_code != 429:
                break
            if time_diff < 1:
                # print('Awaiting time', 1 - time_diff)  # log
                time.sleep(1 - time_diff)

        # finish = time.time()  # log
        # print('Finish request', finish, finish - start)  # log
        session.close()
        return self.response_handler(resp)

    @staticmethod
    def base64_encoding(message: str) -> str:
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        return base64_bytes.decode('ascii')

    def auth_from_creds(self):
        password_encode = self.base64_encoding(PASSWORD)
        request_data = {
            'username': USERNAME,
            'password': password_encode
        }
        url = settings.BASE_URL + settings.AUTH_URL
        req = requests.Request('POST', url, headers=self.headers, data=request_data)
        res = self.request_handler(req)
        return res.get('AuthId')

    @staticmethod
    def response_handler(resp: requests.Response) -> Dict:
        if resp.status_code != 200:
            json_data = {}
            try:
                json_data = resp.json()
            except Exception as e:
                print(e)
            raise GlonassSoftError(error_code=resp.status_code, msg=json_data)
        if not resp.text:
            return {}
        result = resp.json()
        if type(result) == list:
            return result
        if result.get('Error'):
            raise RequestException(result.get('Error'))
        return result

    def base_get(self, url: str):
        """
        GET request
        """
        req = requests.Request('GET', url, headers=self.headers)
        return self.request_handler(req)

    def base_add(self, url: str, body: Dict, entity_name: str,
                 entity_hint: str = '') -> dict:
        """
        POST request with body
        :param url: url to add entity
        :param body: request body
        :param entity_name: entity name's value in body
        :param entity_hint: str representing entity's name (for logging purpose)
        :return: status of operation
        """
        print(url, body)
        req = requests.Request('POST', url=url, headers=self.headers, json=body)

        res = self.request_handler(req)
        print(f'Created {entity_hint}: {body.get(entity_name, None)}')
        return res

    def base_edit(self, url: str, body: Dict, entity_id: str,
                  entity_hint: str = '') -> dict:
        """
        PUT request with parameters
        :param url: url to edit entity
        :param body: entity's body
        :param entity_id:
        :param entity_hint: str representing entity's name (for logging purpose)
        :return: status of operation
        """
        print('edit', body)
        req = requests.Request('PUT', url=url, headers=self.headers, json=body)
        res = self.request_handler(req)
        print(f'Edited {entity_hint}:  {entity_id}')
        return res

    def base_delete(self, url: str, entity_id, entity_hint: str = '') -> str:
        """
        DELETE request with data
        :param url: url to delete entity
        :param entity_id: a list with id(s)
        :param entity_hint: str representing entity's name (for logging purpose)
        :return: status of operation
        """
        req = requests.Request('DELETE', url=url, headers=self.headers,
                               data=str(entity_id))
        self.request_handler(req)
        return f'Deleted {entity_hint}:  {entity_id}'

    def get_all_users(self) -> List:
        return self.base_get(settings.BASE_URL + settings.USERS_BASE_URL)

    def get_user(self, user_id: str) -> Dict:
        url = settings.BASE_URL + settings.USERS_BASE_URL + user_id
        return self.base_get(url)

    def add_user(self, data: Dict) -> Dict:
        url = settings.BASE_URL + settings.USERS_BASE_URL
        return self.base_add(url, data, 'name', 'user')

    def edit_user(self, user_id: str, data: Dict) -> Dict:
        url = settings.BASE_URL + settings.USERS_BASE_URL + user_id
        return self.base_edit(url, data, user_id, 'user')

    def delete_user(self, user_id: str) -> str:
        url = settings.BASE_URL + settings.USERS_BASE_URL
        return self.base_delete(url, [user_id], 'user')

    # C L I E N T

    def get_client(self, client_id: str) -> dict:
        url = settings.BASE_URL + settings.CLIENTS_BASE_URL + client_id
        return self.base_get(url)

    def add_client(self, data: Dict) -> dict:
        url = settings.BASE_URL + settings.CLIENTS_BASE_URL
        return self.base_add(url, data, 'name', 'client')

    def edit_client(self, client_id: str, data: Dict) -> dict:
        url = settings.BASE_URL + settings.CLIENTS_BASE_URL + client_id
        return self.base_edit(url, data, client_id, 'client')

    def delete_client(self, client_id: str) -> str:
        url = settings.BASE_URL + settings.CLIENTS_BASE_URL
        return self.base_delete(url, [client_id], 'client')


a = GSApi()
print(a.auth_from_creds())