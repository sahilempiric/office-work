



from pydoc import cli
import click
from telethon.sync import TelegramClient
number = 85262550512
id_ = 15451024
hash_ = '6fb9eb2518d1bd451682c56ddc348be3'

client = TelegramClient(f'./sessions/{number}',id_,hash_)

client.connect()
client.get_me()
client.send_message(client.get_entity('xanaofficial'),message='v.good',comment_to=269)
client.disconnect()


number = 85262550512
id_ = 15451024
hash_ = '6fb9eb2518d1bd451682c56ddc348be3'
# from pyrogram import Client
# app = Client(
#     f'{number}_p',
#     api_id=id_,
#     api_hash=f'{hash_}',
#     phone_number=str(number),
#     )
client = TelegramClient(f'./sessions/{number}',id_,f'{hash_}')
client.connect()
# app.start()

# abc = client.get_messages('xanaofficial',269)
# print(abc)

print(client.get_messages('telegram')[-1].message)

# print(client.send_code_request(number))
# print(client.get_entity('xana_1234').title)
# aaa = app.send_reaction('xanaofficial',269,'👍')
# aaa = app.send_comment(
#     'xanaofficial',269,'👍'
# )
# print(aaa)
# with app:print(app.get_me())
client.disconnect()