from asyncio import events
from pydoc import cli
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
# from pyrogram.raw.functions.messages import GetMessageReactionsList

number = 919978911838
id_ = 14251965
hash_ = '5e489dc4ddfdf6b48db7240a20d84c57'
# number = 85262550512
# id_ = 15451024
# hash_ = '6fb9eb2518d1bd451682c56ddc348be3'
client = TelegramClient(f'./sessions/{number}',id_,f'{hash_}')
client.connect()

if client.get_me():
    print('Script is started !')
else:
    client.send_code_request(number)
    client.sign_in(number,input('Enter the OTP: '))


client(JoinChannelRequest('xana_1'))
channel = client.get_entity('xana_1')
print( i.id for i in client.get_messages(channel))


# print( client.iter_messages(channel)[0].id)

for message in client.iter_messages(channel):
    print(message.reply_markup,'----',message.id,'----', message.text)
    print(message)
    client.send_message(channel, 'Great update!',comment_to=message.id)
# print('\n\n',client.iter_messages(channel),'\n\n')
# app = client
# with app:
#     peer = app.peer(1705305623)

#     for message in app.iter_history(chat_id=4):
#         print(message.reactions)


# @events.register(events.NewMessage)
# def handler(event):
#     message_id = event.id
#     print(message_id)


# posts = client.GetHistoryRequest(
#         peer='xana_text',
#         limit=1,
#         offset_date=None,
#         offset_id=0,
#         max_id=0,
#         min_id=0,
#         add_offset=0,
#         hash=0)
# aaaa = client.send_message(channel, message='fsdhgfbdash kjbafd',reply_to=4)
# print(aaaa.id,aaaa)
# client.send_message(channel, message="❤️", comment_to=client.get_messages(channel)[-1])
# print(channel.chat)
# print(client.iter_messages(
#     channel,limit=2,reverse=True
# ))