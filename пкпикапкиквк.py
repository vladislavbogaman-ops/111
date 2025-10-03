from telethon.sync import TelegramClient, errors
from telethon.errors.rpcerrorlist import MessageTooLongError, PeerIdInvalidError
import os
import random
from time import sleep


api_id = int(os.environ.get("API_ID", "0"))
api_hash = os.environ.get("API_HASH", "")
base_delay = int(os.environ.get("BASE_DELAY", "30"))

if not api_id or not api_hash:
    raise ValueError("Не заданы переменные окружения API_ID и API_HASH!")

client = TelegramClient('client2', api_id, api_hash)

EXCLUDED_GROUPS = [
    'Скупы UNION',
    'USF || Чат сливов',
    'Отзывы с продаж',
    'Отзывы с Тейвата',
    'STOP SCAM | КИДКИ | TRASH',
    'Гаранты Genshin Impact | SS PROJECT | GENSHIN | HSR | HONKAI | GARANTS',
    123456789
]


def dialog_sort(dialog):
    return dialog.unread_count


def spammer(client):
    k = 0
    j = 0

    def create_groups_list(groups=[]):
        for dialog in client.iter_dialogs():
            if dialog.is_group and dialog.unread_count >= 1:
                if dialog.name in EXCLUDED_GROUPS:
                    continue
                if getattr(dialog.entity, 'username', None) in EXCLUDED_GROUPS:
                    continue
                if dialog.id in EXCLUDED_GROUPS:
                    continue
                groups.append(dialog)
        return groups

    with client:
        for m in client.iter_messages('me', 1):
            msg = m

        while True:
            groups = create_groups_list()
            groups.sort(key=dialog_sort, reverse=True)

            for g in groups[:10000]:
                try:
                    client.forward_messages(g, msg, 'me')
                    print(f'✅ Отправлено в: {g.name or g.entity.username}')
                    k += 1
                    delay_random = random.randint(5, 12)
                    print(f'⏱ Пауза {delay_random} сек перед следующим сообщением...')
                    sleep(delay_random)

                except errors.ForbiddenError as o:
                    client.delete_dialog(g)
                    if g.entity.username:
                        print(f'Error: {o.message} Аккаунт покинул @{g.entity.username}')
                    else:
                        print(f'Error: {o.message} Аккаунт покинул {g.name}')
                except errors.FloodError as e:
                    if e.seconds > 80:
                        continue
                    else:
                        print(f'Error: {e.message} Требуется ожидание {e.seconds} секунд')
                        sleep(e.seconds)
                except PeerIdInvalidError:
                    client.delete_dialog(g)
                except MessageTooLongError:
                    print(f'Message was too long ==> {g.name}')
                except errors.BadRequestError as i:
                    print(f'Error: {i.message}')
                except errors.RPCError as a:
                    print(f'Error: {a.message}')

            j += k
            k = 0
            print('Отправлено сообщений: ', j)

            full_delay = base_delay + random.randint(2, 7)
            print(f'🔁 Пауза между циклами: {full_delay} сек...')
            sleep(full_delay)
            groups.clear()


if __name__ == '__main__':
    spammer(client)
