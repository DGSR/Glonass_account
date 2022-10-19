from api.api_class import GSApi
from api.autofill import autofill_client


def main():
    print('Start')
    try:
        res = None
        api = GSApi()

        res = api.find_user({'login': 'developer'})

        print(res)

    except Exception as e:
        print(e)
        return None
    return None


if __name__ == '__main__':
    main()
