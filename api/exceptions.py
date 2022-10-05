class RequestException(Exception):
    """"""


class GlonassSoftError(Exception):
    errors = {
        "200": 'OK.',
        "301": 'Moved permanently.',
        "400": 'Некорректный запрос.',
        "401": 'Не авторизован.',
        "403": 'Запрещено.',
        "404": 'Не найден.',
        "500": 'Внутрення ошибка сервера.',
        "502": 'Плохой шлюх.',
        "503": 'Сервис недоступен.',
        "504": 'Шлюз не отвечает.',
        "429": 'Слишком много запросов.',
    }

    def __init__(self, msg=None, error_code=None):
        self.error_code = error_code
        self.error_description = self.errors.get(str(error_code), f'Неописуемая ошибка: {error_code}')
        self.msg = f"{msg.get('Message', False) or 'ГЛОНАССSoft ошибка'} {self.error_description}"
        super().__init__(self.msg)

