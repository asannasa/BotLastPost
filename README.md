# BotLastPost for Telegram
Телеграм-бот последнего сообщения
* Отправление сообщения в группы, удаление предыдущего сообщения бота
* Удаление предыдущего сообщения бота через определенное время TIME
* Удаляет служебные сообщения: (новый участник чата, вышел участник чата, изменено или удалено фото чата)
## Команды бота для администратора:
- `/start` - отправка приветствия администратору бота
- `/addnewbot` - добавить бота в базу данных
- `/allbots` - список всех ботов
- `/help` - справка

## Системные требования
- Linux (Ubuntu)
- Python ≥ 3.8
## Установить программу на сервер
Зайти на сервер от имени root или администратора, и вставить команду:
```bash
curl https://raw.githubusercontent.com/asannasa/BotLastPost/master/install.sh | bash
```

## Работа со службой BotLastPost.service
Запустить службу, как правило после установки служба запускается
```bash
systemctl start BotLastPost.service
```

Проверить статус службы
```bash
systemctl status BotLastPost.service
```

Остановить службу
```bash
systemctl stop BotLastPost.service
```

Перезапустить службу
```bash
systemctl restart BotLastPost.service
```


## Настройка программы

Во время установки появится окно для ввода первичных данных 


## Удалить программу

```bash
curl https://raw.githubusercontent.com/asannasa/BotLastPost/master/uninstall.sh | bash
```
