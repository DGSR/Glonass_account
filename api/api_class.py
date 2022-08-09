from typing import List, Dict, Optional, Union
import base64
import requests
import time

from config import settings
from credentials import config
from api.exceptions import RequestException, GlonassSoftError
from credentials.cred import USERNAME, PASSWORD


class GSApi:

    def __init__(self):
        self.last_request_time = time.time()

        self.headers = config.HEADERS
        self.token = self.auth_from_creds()
        self.headers['X-Auth'] = self.token

    def refresh_headers(self):
        self.headers['X-Auth'] = self.auth_from_creds()

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
    def response_handler(resp: requests.Response) -> Optional[Dict]:
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

    @staticmethod
    def base64_encoding(message: str) -> str:
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        return base64_bytes.decode('ascii')

    def auth_from_creds(self) -> str:
        """
        Basic Authentication using username and encoded password
        from credentials
        :return: Token
        """
        password_encode = self.base64_encoding(PASSWORD)
        request_data = {
            'username': USERNAME,
            'password': password_encode
        }
        url = settings.BASE_URL + settings.AUTH_URL
        req = requests.Request('POST', url, data=request_data)
        res = self.request_handler(req)
        return res.get('AuthId')

    def check_auth(self) -> bool:
        """
        Server checks token validity
        """
        url = settings.BASE_URL + settings.AUTH_CHECK_URL
        req = requests.get(url, config.HEADERS)
        return False if req.status_code != 200 else True

    def base_get(self, url: str):
        req = requests.Request('GET', url, headers=self.headers)
        return self.request_handler(req)

    def base_add(self, url: str, body: Dict, entity_name: str,
                 entity_hint: str = '') -> dict:
        """
        POST request with body
        :param url: url to add entity
        :param body: request body
        :param entity_name: str entity name's value in body
        :param entity_hint: str representing entity's name (for logging purpose)
        :return: status of operation
        """
        print(url, body)
        req = requests.Request('POST', url=url, headers=self.headers, json=body)

        res = self.request_handler(req)
        print(f'Created {entity_hint}: {body.get(entity_name, None)}')
        return res

    def base_edit(self, url: str, body: Union[List, Dict], entity_id: str,
                  entity_hint: str = '') -> Union[List, Dict]:
        """
        PUT request with parameters
        :param url: url to edit entity
        :param body: entity's body
        :param entity_id: str
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

    # U S E R

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

    def get_all_clients(self) -> List:
        return self.base_get(settings.BASE_URL + settings.CLIENTS_BASE_URL)

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

    # V E H I C L E   M O D E L

    def get_all_vehicle_models(self) -> List:
        return self.base_get(settings.BASE_URL + settings.VEHICLE_MODEL_BASE_URL)

    def get_vehicle_model(self, vehicle_model_id: str) -> dict:
        url = settings.BASE_URL + settings.VEHICLE_MODEL_BASE_URL + vehicle_model_id
        return self.base_get(url)

    def add_vehicle_model(self, data: Dict) -> dict:
        url = settings.BASE_URL + settings.VEHICLE_MODEL_BASE_URL
        return self.base_add(url, data, 'name', 'vehicle model')

    def edit_vehicle_model(self, vehicle_model_id: str, data: Dict) -> dict:
        url = settings.BASE_URL + settings.VEHICLE_MODEL_BASE_URL + vehicle_model_id
        return self.base_edit(url, data, vehicle_model_id, 'vehicle model')

    def delete_vehicle_model(self, vehicle_model_id: str) -> str:
        url = settings.BASE_URL + settings.VEHICLE_MODEL_BASE_URL
        return self.base_delete(url, [vehicle_model_id], 'vehicle model')

    #  O B J E C T   ( V E H I C L E )

    def get_all_vehicles(self) -> List:
        return self.base_get(settings.BASE_URL + settings.VEHICLE_BASE_URL)

    def get_vehicle(self, vehicle_id: str) -> dict:
        url = settings.BASE_URL + settings.VEHICLE_BASE_URL + vehicle_id
        return self.base_get(url)

    def add_vehicle(self, data: Dict) -> dict:
        url = settings.BASE_URL + settings.VEHICLE_BASE_URL
        return self.base_add(url, data, 'name', 'vehicle')

    def edit_vehicle(self, vehicle_id: str, data: Dict) -> dict:
        url = settings.BASE_URL + settings.VEHICLE_BASE_URL + vehicle_id
        return self.base_edit(url, data, vehicle_id, 'vehicle')

    def delete_vehicle(self, vehicle_id: str) -> str:
        url = settings.BASE_URL + settings.VEHICLE_BASE_URL
        return self.base_delete(url, [vehicle_id], 'vehicle')

    def get_vehicle_counter(self, vehicle_id: str) -> list:
        url = settings.BASE_URL + settings.VEHICLE_GET_COUNTER_URL + vehicle_id
        return self.base_get(url)

    def edit_vehicle_counter(self, vehicle_id: str, data: Union[List, Dict]) -> Union[List, Dict]:
        url = settings.BASE_URL + settings.VEHICLE_PUT_COUNTER_URL
        return self.base_edit(url, data, vehicle_id, 'vehicle_counter')

    # S E N S O R

    def get_sensors(self, vehicle_id: str) -> dict:
        url = settings.BASE_URL + settings.SENSORS_BASE_URL % vehicle_id
        return self.base_get(url)

    def add_sensor(self, vehicle_id: str, data: Dict) -> dict:
        url = settings.BASE_URL + settings.SENSORS_BASE_URL % vehicle_id
        return self.base_add(url, data, 'name', 'sensor')

    def edit_sensor(self, vehicle_id: str, data: Dict) -> dict:
        url = settings.BASE_URL + settings.SENSORS_BASE_URL % vehicle_id
        return self.base_edit(url, data, vehicle_id, 'sensor')

    def delete_sensor(self, vehicle_id: str) -> str:
        url = settings.BASE_URL + settings.SENSORS_BASE_URL % vehicle_id
        return self.base_delete(url, [vehicle_id], 'sensor')

    def get_sensor_types(self):
        return self.base_get(settings.BASE_URL + settings.SENSORS_TYPES)
