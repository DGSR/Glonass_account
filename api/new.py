import time
from typing import Dict
import base64
from credentials.cred import USERNAME, PASSWORD
from credentials import settings
from api.exceptions import GlonassSoftError, RequestException
import requests

RQT = time.time()


def request_handler(req: requests.Request,
                    retries: int = 3) -> Dict:
    """
    handles prepared Request
    if response is 429 then sleep and retry number of retries
    :param req: prepared Request to be sent
    :param retries: number of retries (default  3)
    :return: response
    """
    session = requests.Session()
    print(req.data)
    # start = time.time()  # log
    # print('First request', start)  # log
    for _ in range(retries):
        r = req.prepare()
        resp = session.send(r)
        time_diff = time.time() - RQT
        RQT = time.time()
        if resp.status_code != 429:
            break
        if time_diff < 1:
            # print('Awaiting time', 1 - time_diff)  # log
            time.sleep(1 - time_diff)

    # finish = time.time()  # log
    # print('Finish request', finish, finish - start)  # log
    session.close()
    return response_handler(resp)


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


def base64_encoding(message: str) -> str:
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode('ascii')


def auth_from_creds() -> str:
    """
    Basic Authentication using username and encoded password
    from credentials
    :return: Token
    """
    password_encode = base64_encoding(PASSWORD)
    request_data = {
        'username': USERNAME,
        'password': password_encode
    }
    url = settings.BASE_URL + settings.AUTH_URL
    req = requests.Request('POST', url, headers=settings.HEADERS, data=request_data)
    res = request_handler(req)
    return res.get('AuthId')

print(auth_from_creds())