from copy import deepcopy
from typing import List, Dict, Optional, Union, Tuple
import requests
import time
from config import settings
from datetime import datetime, timedelta
from credentials.cred import USERNAME, PASSWORD, CRED_FILE

from api.utils import base64_encoding, write_down_token, first_index_lower


class RequestException(Exception):
    """"""


class GlonassSoftError(Exception):
    errors = {
        "200": 'OK',
        "301": 'Moved permanently',
        "400": 'Bad request',
        "401": 'Unauthorized',
        "403": 'Forbidden',
        "404": 'Not found',
        "500": 'Internal server error',
        "502": 'Bad gateway',
        "503": 'Service unavailable',
        "504": 'Gateway Timeout',
        "429": 'Requests Per Second Exceeded'
    }

    def __init__(self, msg=None, error_code=None):
        self.error_code = error_code
        self.error_description = self.errors.get(str(error_code), f'Undescribed error: {error_code}')
        if msg is None:
            self.msg = "A ГЛОНАССSoft error" if error_code is None else self.error_description
        else:
            self.msg = f"{msg.get('ExceptionMessage') or 'ГЛОНАССSoft error'} {self.error_description}"
        super().__init__(self.msg)


class GSApi:
    """
    API singleton class to work with GLONASS Soft API.

    :param `token`: token for API to properly send request

    :ivar `headers`: built
    :ivar `last_request_time`
    """
    _instance = None

    def __new__(cls, token=None):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, token=None):
        self.last_request_time = time.time()
        self.headers = settings.HEADERS
        self.token = token if token is not None else self.auth()
        self.headers['X-Auth'] = self.token

    def auth(self) -> str:
        """
        Send post request with username and base64 password
        If contains field error
        :return: Authentication Token (GUID)
        """
        password_encode = base64_encoding(PASSWORD)
        request_data = {
            'username': USERNAME,
            'password': password_encode
        }
        final_url = settings.BASE_URL + settings.AUTH_URL
        res = requests.post(final_url, data=request_data)
        result = res.json()
        if result.get('Error'):
            raise RequestException(result.get('Error'))
        token = result.get('AuthId')
        write_down_token(token, CRED_FILE)

        return token

    def request_handler(self, req: requests.Request,
                        retries: int = 3) -> Optional[Union[List, Dict]]:
        """
        handles prepared Request
        if response is 429 then sleep and retry number of retries
        :param req: prepared Request to be sent
        :param retries: number of retries (default= 3)
        :return: response
        """
        session_request = requests.Session()
        # start = time.time()  # log
        # print('First request', start)  # log
        for _ in range(retries):
            req.headers.update(self.headers)
            r = req.prepare()
            resp = session_request.send(r)
            # print(r.method, r.url, r.body, r.headers)

            if resp.status_code == 401:
                self.token = self.auth()
                self.headers['X-Auth'] = self.token
                continue
            if resp.status_code != 429:
                break
            time_diff = time.time() - self.last_request_time
            self.last_request_time = time.time()
            if time_diff < 1:
                # print('Awaiting time', 1 - time_diff)  # log
                time.sleep(1 - time_diff)

        # finish = time.time()  # log
        # print('Finish request', finish, finish - start)  # log
        session_request.close()
        return self.response_handler(resp)

    @staticmethod
    def response_handler(resp: requests.Response):
        """
        Handle response results, including errors
        :param resp: response object
        :return: data in response
        """
        if 200 < resp.status_code >= 300:
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

    def make_request(self,
                     method: str,
                     url: str,
                     base_url: str = None,
                     *args, **kwargs):

        base_url = base_url or settings.BASE_URL
        method = method.upper()
        headers = deepcopy(self.headers)

        if kwargs.get('headers', None) is not None:
            headers.update(kwargs.get('headers'))

        req = requests.Request(method, base_url + url, headers=headers)
        if method == 'GET':
            params = kwargs.get('params', None)
            setattr(req, 'params', params)
        if method == 'POST':
            body = kwargs.get('body', None)
            setattr(req, 'json', body)
        if method == 'PUT':
            body = kwargs.get('body', None)
            setattr(req, 'json', body)
        if method == 'DELETE':
            body = kwargs.get('body', None)
            setattr(req, 'data', str(body))
        return self.request_handler(req)

    # U S E R

    def get_all_users(self, **kwargs) -> List:
        return self.make_request('GET', settings.USERS_BASE_URL, **kwargs)

    def get_user(self, user_id: str) -> Dict:
        return self.make_request('GET', settings.USERS_BASE_URL + user_id)

    def add_user(self, data: Dict) -> Dict:
        return self.make_request('POST', settings.USERS_BASE_URL, body=data)

    def edit_user(self, user_id: str, data: Dict) -> Dict:
        return self.make_request('PUT', settings.USERS_BASE_URL + user_id, body=data)

    def delete_user(self, user_id: str):
        return self.make_request('DELETE', settings.USERS_BASE_URL, body=[user_id])

    def find_user(self, data: Dict):
        return self.make_request('POST', settings.USERS_FIND_URL, body=data)

    # C L I E N T

    def get_all_clients(self, **kwargs) -> List:
        return self.make_request('GET', settings.CLIENTS_BASE_URL, **kwargs)

    def get_client(self, client_id: str) -> dict:
        return self.make_request('GET', settings.CLIENTS_BASE_URL + client_id)

    def add_client(self, data: Dict) -> dict:
        return self.make_request('POST', settings.CLIENTS_BASE_URL, body=data)

    def edit_client(self, client_id: str, data: Dict) -> dict:
        return self.make_request('PUT', settings.CLIENTS_BASE_URL + client_id, body=data)

    def delete_client(self, client_id: str):
        return self.make_request('DELETE', settings.CLIENTS_BASE_URL, body=[client_id])

    def get_embedded_clients(self, client_id: str):
        url = settings.CLIENTS_BASE_URL
        return self.make_request('GET', url, params={'owner': client_id})

    # V E H I C L E   M O D E L

    def get_all_vehiclemodels(self, **kwargs) -> List:
        return self.make_request('GET', settings.VEHICLE_MODEL_BASE_URL, **kwargs)

    def get_vehiclemodel(self, vehicle_model_id: str) -> dict:
        url = settings.VEHICLE_MODEL_BASE_URL + vehicle_model_id
        return self.make_request('GET', url)

    def add_vehiclemodel(self, data: Dict) -> dict:
        url = settings.VEHICLE_MODEL_BASE_URL
        return self.make_request('POST', url, body=data)

    def edit_vehiclemodel(self, vehicle_model_id: str, data: Dict) -> dict:
        url = settings.VEHICLE_MODEL_BASE_URL + vehicle_model_id
        return self.make_request('PUT', url, body=data)

    def delete_vehiclemodel(self, vehicle_model_id: str):
        url = settings.VEHICLE_MODEL_BASE_URL
        return self.make_request('DELETE', url, body=[vehicle_model_id])

    #  O B J E C T   ( V E H I C L E )

    def get_all_vehicles(self, **kwargs) -> List:
        return self.make_request('GET', settings.VEHICLE_BASE_URL, **kwargs)

    def get_vehicle(self, vehicle_id: str) -> dict:
        url = settings.VEHICLE_BASE_URL + vehicle_id
        return self.make_request('GET', url)

    def search_vehicle(self, value):
        param = {'q': f'{{"search":"{value}"}}'}
        return self.make_request('GET', settings.VEHICLE_BASE_URL, params=param)

    def add_vehicle(self, data: Dict) -> dict:
        url = settings.VEHICLE_BASE_URL
        return self.make_request('POST', url, body=data)

    def edit_vehicle(self, vehicle_id: str, data: Dict) -> dict:
        url = settings.VEHICLE_BASE_URL + vehicle_id
        return self.make_request('PUT', url, body=data)

    def delete_vehicle(self, vehicle_id: str):
        url = settings.VEHICLE_BASE_URL
        return self.make_request('DELETE', url, data=[vehicle_id])

    def get_all_vehiclecounters(self, vehicle_id: str) -> list:
        url = settings.VEHICLE_GET_COUNTER_URL + vehicle_id
        data = self.make_request('GET', url)
        data_lower = first_index_lower(data)
        return data_lower

    def edit_vehiclecounter(self, data: Union[List, Dict]) -> Union[List, Dict]:
        url = settings.VEHICLE_PUT_COUNTER_URL
        data = [data]
        data = first_index_lower(data)
        api_response = self.make_request('PUT', url, body=data)
        return api_response[0]

    # S E N S O R

    def get_all_sensors(self, vehicle_id: str) -> List:
        return self.make_request('GET', settings.SENSORS_BASE_URL % vehicle_id)

    def add_sensor(self, data: Dict) -> List:
        vehicle_id = data['vehicleId']
        url = settings.SENSORS_BASE_URL % vehicle_id
        sensors_arr = self.make_request('POST', url, body=[data])
        return sensors_arr[0]

    def edit_sensor(self, vehicle_id: str, data: List) -> List:
        url = settings.SENSORS_BASE_URL % vehicle_id
        return self.make_request('PUT', url, body=data)

    def delete_sensor(self, vehicle_id: str, sensors_id: List):
        url = settings.SENSORS_BASE_URL % vehicle_id
        return self.make_request('DELETE', url, body=sensors_id)

    def get_sensor_types(self):
        return self.make_request('GET', settings.SENSORS_TYPES)

    # C O M M A N D S

    def get_all_commands(self, vehicle_id: str):
        params = {
            'vehicleGuid': '{' + f'{vehicle_id}' + '}'
        }
        url = settings.COMMANDS_GET_URL[:-1]
        return self.make_request('GET', url, params=params)

    def edit_command(self, data: List):
        body = data if type(data) == list else [data]
        return self.make_request('PUT', settings.COMMANDS_PUT_URL, body=body)[0]

    def add_command(self, data: List):
        return self.edit_command(data if type(data) == list else [data])

    def delete_command(self, commands_id: List):
        url = settings.COMMANDS_DELETE_URL
        return self.make_request('DELETE', url, body=commands_id)

    # T E M P L A T E S

    def get_all_templates(self, vehicle_id: str):
        params = {
            'q': str({"vehicleId": vehicle_id})
        }
        url = settings.TEMPLATES_BASE_URL[:-1]
        return self.make_request('GET', url, params=params)

    def edit_template(self, template_id: str, data: Dict):
        url = settings.TEMPLATES_BASE_URL + template_id
        return self.make_request('PUT', url, body=data)

    # I N S P E C T I O N  T A S K S

    def get_inspection_tasks(self, vehicle_id: str):
        """
        Get inspection tasks for current vehicle by its id
        """
        url = settings.INSPECTIONS_TASKS_BASE_URL + vehicle_id
        return self.make_request('GET', url)

    # M E S S A G E S

    def get_all_messages(self, vehicle_id: str) -> Tuple:
        """
        Get all messages for current vehicle by its id
        """
        url = settings.MESSAGES_BASE_URL + settings.MESSAGES_FOR_VEHICLE
        time_format = "%Y-%m-%d %H:%M"
        time_now = datetime.now()
        time_year_ago = time_now - timedelta(days=365)
        str_time_now = time_now.strftime(time_format)
        str_time_year_ago = time_year_ago.strftime(time_format)
        received_data = self.make_request(
            'GET',
            url,
            params={
                "unitId": vehicle_id,
                "DtStart": str_time_year_ago,
                "DtEnd": str_time_now,
                "Flag": 1
            },
        )['m']
        return received_data, int(time_year_ago.timestamp())

    def get_all_messages_generator(self, vehicle_id: str, stream: bool = False) -> Tuple:
        """
        Get commands for current vehicle by its id. Returns generator. Recommended to use.
        """
        url = settings.MESSAGES_BASE_URL + settings.MESSAGES_FOR_VEHICLE
        time_format = "%Y-%m-%d %H:%M"
        time_now = datetime.now()
        time_year_ago = time_now - timedelta(days=365)
        str_time_now = time_now.strftime(time_format)
        str_time_year_ago = time_year_ago.strftime(time_format)
        received_data = self.make_request(
            'GET',
            url,
            params={
                "unitId": vehicle_id,
                "DtStart": str_time_year_ago,
                "DtEnd": str_time_now,
                "Flag": 1
            },
            stream=stream
        )['m']
        return received_data, int(time_year_ago.timestamp())

    # G E O B J E C T S

    def get_all_geo_objects(self, client_id: str):
        url = settings.GEO_OBJECT_BASE_URL
        return self.make_request('GET', url, headers={'X-Agent': client_id})

    def add_geo_objects(self, client_id: str, data: dict):
        url = settings.GEO_OBJECT_BASE_URL
        return self.make_request('POST', url, body=data, headers={'X-Agent': client_id})

    def delete_geo_objects(self, client_id: str, data: List):
        url = settings.GEO_OBJECT_DELETE
        return self.make_request('DELETE', url, body=data, headers={'X-Agent': client_id})

    def edit_geo_objects(self, client_id: str, data: dict):
        url = settings.GEO_OBJECT_BASE_URL
        return self.make_request('PUT', url, body=data, headers={'X-Agent': client_id})

    def get_geo_wkt_info(self, client_id: str, data: List):
        url = settings.GEO_OBJECT_WKT_INFO
        return self.make_request('POST', url, body=data, headers={'X-Agent': client_id})

    # R E P O R T S

    def get_reports_list(self, client_id: str):
        url = settings.REPORTS_LIST_URL
        return self.make_request('GET', url, headers={'X-Agent': client_id})

    def export_user_report(self, client_id: str, user_report_id: str):
        url = settings.EXPORT_USER_REPORT_URL
        header = {'X-Agent': client_id}
        params = {'userReportGuid': user_report_id}
        return self.make_request('GET', url, headers=header, params=params)
