import os
from dotenv import load_dotenv, set_key, find_dotenv

load_dotenv(find_dotenv())


def add_token_bot(name_bot: str, token: str):
    # TODO проверить
    if os.environ.get(name_bot) is None:
        set_key(find_dotenv(), name_bot, token)
        return True
    else:
        return False


if __name__ == '__main__':
    # TODO Тестовый, скорее всего изменить надо
    while True:
        namebot = input('Введите имя бота: ')
        if os.environ.get(namebot) is None:
            add_token_bot(namebot, input('Введите токен: '))
            break
        else:
            print('Такое название уже есть')
