import datetime


def auto_fill_user(login) -> dict:
    """
    Глонасс Soft user autofill
    :param login: user's login
    :return: dict
    """
    d = datetime.datetime.now()
    return {
        'login': login,
        'email': login + '@tspb.su',
        'password': d.strftime("%d%m%Y"),
        'parentId': 'a29f3c54-4d06-4964-a80e-8bc6bcd68e30',
        'phone': '0000000',
        'firstName': ' ',
        'lastName': ' ',
        'groups': ['1313']  # Lowest access possible (20-07-2022)
    }


def auto_fill_client(name, owner) -> dict:
    """
    Глонасс Soft client autofill
    :param name: client's name
    :param owner: id of client owner
    :return:
    """
    return {
        'name': name,
        'agentInfoType': 2,
        'owner': owner,
        'client': {
            'accFullName': name
        }
    }
