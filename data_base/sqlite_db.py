import sqlite3 as sq
import string
import random
__DB_LOCATION = "./bot.db"

# TODO: Изменить на ООП


def sql_start():
    global cursor, base
    base = sq.connect(__DB_LOCATION)
    cursor = base.cursor()
    if base:
        pass
        # print("DB connect!")
    base.execute('CREATE TABLE IF NOT EXISTS chatDB '
                 '(nameBOT TEXT UNIQUE, TOKEN TEXT, chatID INTEGER, text TEXT, lastID INTEGER)')
    base.commit()


# исправить
async def add_chat_text(state):
    try:
        cursor.execute('INSERT INTO chatDB VALUES(?, ?, ?, ?, "")', tuple(state.values()))
        base.commit()
        # print(tuple(state.values()[-1]))
        # print("Успех новой записи")
    except sq.Error:
        # print(err, " - не могу добавить, попробуй обновить")
        cursor.execute('UPDATE chatDB SET text = ? WHERE nameBOT = ?',
                       (tuple(state.values())[3], tuple(state.values())[0]))
        base.commit()
        # print("Обновил")


def update_last_message(chat_id: int, last_m: int):
    try:
        cursor.execute('UPDATE chatDB SET lastID = ? WHERE chatID = ?', (last_m, chat_id))
        base.commit()
        # print("Обновил")
    except sq.Error:
        pass
        # print(err, " - не могу обновить")


# исправить, вроде должно работать
async def delete_chat(id_chat: int):
    try:
        cursor.execute('DELETE FROM chatDB WHERE chatID = ?', (id_chat, ))
        base.commit()
        # print("Удалил")
    except sq.Error:
        pass
        # print(err, " - не могу удалить")


# исправить
async def last_message(id_chat: int) -> int:
    cursor.execute('SELECT * FROM chatDB WHERE chatID = ?', (id_chat, ))
    record = cursor.fetchone()
    # print('Последнее сообщение:', record[2])
    return record[2]


async def chat_message(id_chat: int) -> str:
    cursor.execute('SELECT * FROM chatDB WHERE chatID = ?', (id_chat, ))
    record = cursor.fetchone()
    # print('Text: ', record[1])
    return record[1]


def db_chat() -> list:
    cursor.execute('SELECT * FROM chatDB')
    record = cursor.fetchall()
    return record


def db_chat_bot(name: str) -> list:
    cursor.execute('SELECT * FROM chatDB WHERE nameBOT = ?', (name, ))
    record = cursor.fetchall()
    return record


def len_db():
    cursor.execute('SELECT * FROM chatDB')
    record = cursor.fetchall()
    return len(record)


async def save_text(state):
    cursor.execute('UPDATE chatDB SET text = ? WHERE nameBOT = ?', (tuple(state.values())[1], tuple(state.values())[0]))
    base.commit()


async def delete_bot(state):
    cursor.execute('DELETE FROM chatDB WHERE nameBOT = ?', (tuple(state.values())))
    base.commit()


def add_db_temp():
    state = {}
    for i in range(3, 25):
        state[0] = "Bot" + str(i)
        state[1] = str(random.randint(5700000000, 5799999999)) + ":AA"
        for b in range(33):
            state[1] += random.choice(string.ascii_letters)
        state[2] = random.randint(1001649586527, 1001731025682) * -1
        state[3] = f"Последние сообщение от {state[0]}"
        add_chat_text(state)


def list_bot() -> list:
    zlist = []
    list1 = cursor.execute('SELECT nameBOT FROM chatDB').fetchall()
    for i in list1:
        t = str(i).replace("('","").replace("',)","")
        zlist.append(t)
    return zlist
