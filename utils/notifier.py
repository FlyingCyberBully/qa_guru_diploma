import requests

from config import settings


def send_telegram_notification(message: str | None = None):
    token = settings.telegram_bot_token
    chat_id = settings.telegram_chat_id

    if not token or not chat_id:
        return

    if message is None:
        message = (
            '<b>Тесты завершены!</b>\n'
            'Отчёт Allure сформирован.'
        )

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    requests.post(
        url,
        json={'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'},
        timeout=10,
    )


if __name__ == '__main__':
    send_telegram_notification()
