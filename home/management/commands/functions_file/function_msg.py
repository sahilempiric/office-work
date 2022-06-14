from distutils.log import error
import time
import random
from numpy import full
from requests import request
from telethon import TelegramClient
from telethon.sync import TelegramClient
from home.models import Engagements, comment_view, user_details
import telethon,os
from telethon import errors
from telethon.tl.functions.channels import JoinChannelRequest
from pyrogram import Client
from pyrogram import errors as p_errors
p_errors.SessionPasswordNeeded
p_errors.PhoneNumberBanned
p_errors.AuthKeyUnregistered



def add_group(view_group,groupname,Message,number,apiid,apihash):
    try:
        client = TelegramClient(f'./sessions/{number}',apiid,apihash)
        user = user_details.objects.filter(number=number).first()
        client.connect()
        if client.is_user_authorized():
            me = client.get_me()
            client(JoinChannelRequest(groupname))
            time.sleep(0.3)
            entity = client.get_entity(view_group)
            if client.send_read_acknowledge(entity):
                user.views += 1
                print(f"{me.first_name} {number} have Marked as seen in {view_group}'s chat")
            else : 
                print(f"{me.first_name} {number} have No new messages in {view_group}'s chat")
            # if client.send_message(groupname,Message):
            #     user.comment += 1
            #     print(f'+{number} {me.first_name} has sent a message in {groupname}')
            # else:
            #     print(f"+{number} {me.first_name} couldn't sent Message in {groupname}")
            # time.sleep(random.randint(60, 70))
            # user.save()
        else:
            print(f'{number} is not authorized So please authorized it')    
        client.disconnect()
    except Exception as e :
        client.disconnect()
        print(e)

def send_messages(view_group,groupname,Message,number,apiid,apihash):
    try:
        client = TelegramClient(f'./sessions/{number}',apiid,apihash)
        user = user_details.objects.filter(number=number).first()
        view_counts = comment_view.objects.create(user=user,comment_on=groupname,view_on=view_group)
        client.connect()
        if client.is_user_authorized():
            me = client.get_me()
            client(JoinChannelRequest(groupname))
            entity = client.get_entity(view_group)
            if client.send_read_acknowledge(entity):
                user.views += 1
                view_counts.views += 1
                user.save()
                view_counts.save()
                print(f"{me.first_name} {number} have Marked as seen in {view_group}'s chat")
            else : 
                print(f"{me.first_name} {number} have No new messages in {view_group}'s chat")
            if client.send_message(groupname,Message):
                user.comment += 1
                view_counts.comment += 1
                user.save()
                view_counts.save()
                print(f'+{number} {me.first_name} has sent a message in {groupname}')
            else:
                print(f"+{number} {me.first_name} couldn't sent Message in {groupname}")
            time.sleep(0.2)
            # time.sleep(random.randint(60, 70))
        else:
            print(f'{number} is not authorized So please authorized it')    
        client.disconnect()
    except errors.FloodWaitError as e:
        user.banned = "TEMP BANNED"
        user.save()
    except errors.UserBannedInChannelError as e:
        user.banned = "BANNED"
        user.save()

    except Exception as e :
        client.disconnect()
        print(e)

    

def view_chat(groupname,number,apiid,apihash):
    try:
        client = TelegramClient(f'./sessions/{number}',apiid,apihash)
        client.connect()
        if client.is_user_authorized():
            me = client.get_me()
            entity = client.get_entity(groupname)
            if client.send_read_acknowledge(entity):
                print(f"{me.first_name} {number} have Marked as seen in {groupname}'s chat")
            else : 
                print(f"{me.first_name} {number} have No new messages in {groupname}'s chat")
        time.sleep(random.randint(3,5))
        client.disconnect()
    except Exception as e :
        client.disconnect()
        print(e)

def user_banned(number,apiid,apihash):
    try:
        banned = False
        client = TelegramClient(f'./sessions/{number}',apiid,apihash)
        client.connect()
        if not client.is_user_authorized():
            try:
                client.send_code_(phone=number)
                client.sign_in(code=(input(f'Please Enter the OTP of {number} : ')))
                client.disconnect()
                return banned
            except telethon.errors.rpcerrorlist.PhoneNumberBannedError:
                print(f'Phone number {number} is banned !')
                if os.path.exists(f'./sessions/{number}.session'):
                    banned = True
                    os.remove(f'./sessions/{number}.session')
                    user_details.objects.filter(number=number).delete()
                print(f'{number} is deleted from DATABASE')
                banned = True
                client.disconnect()
                return banned
        else: 
            client.disconnect()
            return banned
    except Exception as e :
        client.disconnect()
        print(e)


def script_chat(i,number,id,hash,msg,group):
    if str(msg) == "nan" :
        return True, False

    try:
        complete = False 
        temp_banned = False
        try:
            client = TelegramClient(f'./sessions/{number}',id,hash)
            client.connect()
            # client(JoinChannel(group))
            # entity = client.get_entity(group)
            # client.send_message(entity,msg)
            f_name = client.get_me().first_name
            print(f"{number} : {f_name} --- sent a message {msg}")
            time.sleep(random.randint(0,1))
            # time.sleep(random.randint(60,70))
            client.disconnect()
            complete = True
            return complete,temp_banned
        except errors.FloodWaitError as e:
            client.disconnect()
            print(f'{number} can not send message till',e.seconds,'secounds') 
            temp_banned = True
            return complete,temp_banned
    except Exception as err :
        print(err)   
        return complete,temp_banned



def pyrogram_authorization(number,apiid,apihash,client_):
    user = user_details.objects.filter(number=number).first()

    try:
        client_.connect()
        app = Client(f'./sessions/{number}_p',api_id=f"{apiid}",api_hash=f"{apihash}",phone_number=str(number))
        app.connect()
        is_authorized = False
        try:is_authorized = True if app.get_me() else False
        except Exception as e:...

        if is_authorized:...
        else:
            sent_code = app.send_code(phone_number=str(number))
            phone_code_hash_ = sent_code.phone_code_hash
            time.sleep(4)
            telegram_msg = client_.get_dialogs()[0].message
            try:otp__ = str(telegram_msg.text).replace('**Login code:**','').split(' ')[1].replace('.','')
            except Exception as e:otp__=''
            app.sign_in(phone_number=str(number),phone_code_hash=phone_code_hash_,phone_code=f"{otp__}")
        
        app.disconnect()
        client_.disconnect()
    except p_errors.SessionPasswordNeeded as e:
        user.banned = 'NEED PASSWORD'
        user.save()
    except p_errors.PhoneNumberBanned as e:
        user.banned = 'BANNED'
        user.save()
    except p_errors.AuthKeyUnregistered as e:
        user.banned = 'BANNED'
        user.save()
    except Exception as e:print(e)

from datetime import  timedelta, time
import datetime
import pytz

def engagement_msg_id(groupname):
    last_few_days= datetime.datetime.now() - datetime.timedelta(days=4)
    msg_id = 0
    utc=pytz.UTC
    msg_id_li = []
    for i in range(15):
        if msg_id_li: return msg_id_li
        user = user_details.objects.filter(banned="ACTIVE").order_by('?').first()
        try:
            client = TelegramClient(f'./sessions/{user.number}',user.api_id,user.api_hash)
            client.connect()
            if client.is_user_authorized():
                me = client.get_me()
                client(JoinChannelRequest(groupname))
                message_count = 0
                for message in client.iter_messages(groupname):
                    # print(message.text)
                    if utc.localize(last_few_days) <  message.date:
                        msg_id = message.id
                        msg_id_li.append(msg_id)


                    if message_count > 50 : break
                    message_count += 1

                # return msg_id

        except errors.FloodWaitError as e:
            user.banned = "TEMP BANNED"
            user.save()
            continue
        except errors.UserBannedInChannelError as e:
            user.banned = "BANNED"
            user.save()
            continue

        except Exception as e :
            client.disconnect()
            print(e)
            continue

    return msg_id_li

def engagement(groupname,Message_id,number,apiid,apihash,random_=0):
    reaction_list = ["❤️","👍","🔥"]

    user = user_details.objects.filter(number=number).first()
    try:
        client = TelegramClient(f'./sessions/{number}',apiid,apihash)
        pyrogram_authorization(number,apiid,apihash,client)
        
        engagement_data = Engagements.objects.create(user = user)
        client.connect()
        if client.is_user_authorized():
            me = client.get_me()
            client(JoinChannelRequest(groupname))
            entity = client.get_entity(groupname)
            # client.send_read_acknowledge()
            if client.send_read_acknowledge(entity):
                user.views += 1
                user.save()
                engagement_data.views += 1
                engagement_data.save()
                print(f"{me.first_name} {number} have Marked as seen in {groupname}'s chat")
            else : 
                print(f"{me.first_name} {number} have No new messages in {groupname}'s chat")

            p_client = Client(f'./sessions/{number}_p',api_id=f"{apiid}",api_hash=f"{apihash}",phone_number=str(number))
            p_client.connect()

                
            

            if p_client.get_me():
                message_id_len = 0
                if not random_:
                    message_id_len = len(Message_id)
                    Message_id = random.sample(Message_id,k=message_id_len)
                else: Message_id = random.sample(Message_id,k=random_)
                for msg in Message_id:
                    reaction = random.choice(reaction_list)
                    if p_client.send_reaction(groupname,msg,reaction):
                        engagement_data.reaction = reaction
                        engagement_data.engagement_on = groupname
                        engagement_data.save()
                        print(f"{me.first_name} has send reaction {reaction} on message id : {msg} of {groupname} channel / group")
                    else:
                        print(f"{me.first_name} couldn't send reaction {reaction} on message id : {msg} of {groupname} channel / group")
                    time.sleep(2)
            # time.sleep(random.randint(60, 70))
            p_client.disconnect()
        else:
            print(f'{number} is not authorized So please authorized it')    
        client.disconnect()
    except p_errors.SessionPasswordNeeded as e:
        user.banned = 'NEED PASSWORD'
        user.save()
    except p_errors.PhoneNumberBanned as e:
        user.banned = 'BANNED'
        user.save()
    except p_errors.AuthKeyUnregistered as e:
        user.banned = 'BANNED'
        user.save()
    except errors.FloodWaitError as e:
        user.banned = "TEMP BANNED"
        user.save()
    except errors.UserBannedInChannelError as e:
        user.banned = "BANNED"
        user.save()

    except Exception as e :
        client.disconnect()
        # if p_client:p_client.disconnect()
        print(e)





import requests



import time
# import s

from urllib.parse import urlencode


def get_number(pid='10',country = 'hk'):
    url = "http://api.getsmscode.com/vndo.php?"

    while True:
        try:
            payload = {
                "action": "getmobile",
                "username": "pay@noborders.net",
                "token": "87269a810f4a59d407d0e0efe58185e6",
                "pid": pid,
                "cocode":country
            }
            payload = urlencode(payload)
            full_url = str(url) + str(payload)
            
            response = requests.post(url=full_url)
            response = response.content.decode("utf-8")
            # print(response)
            # time.sleep(1000)

            try:response = int(response);break
            except Exception as e:print(e)
            
            # if str(response) == ('Message|Capture Max mobile numbers,you max is 5' or 'Message|unavailable'):
            #     continue
            # else:break
        except Exception as e:print(e)
    return response

def get_sms(phone_number, pid='10',country = 'hk'):
    url = "http://api.getsmscode.com/vndo.php?"
    payload = {
        "action": "getsms",
        "username": "pay@noborders.net",
        "token": "87269a810f4a59d407d0e0efe58185e6",
        "pid": pid,
        "mobile": phone_number,
        "author": "pay@noborders.net",
        "cocode":country
    }
    payload = urlencode(payload)
    full_url = url + payload
    for x in range(15):
        response = requests.post(url=full_url).text
        print(response,'=================================')
        if 'telegram' in str(response).lower():
            response = str(response).split('Telegram code:')[-1]
            otp = response.split(' ')[1].replace("You",'')
            return otp
        time.sleep(4)

    return False

def ban_number(phone_number, pid='10',country = 'hk'):
    url = "http://api.getsmscode.com/vndo.php?"
    payload = {
        "action": "addblack",
        "username": "pay@noborders.net",
        "token": "87269a810f4a59d407d0e0efe58185e6",
        "pid": pid,
        "mobile": phone_number,
        "author": "pay@noborders.net",
        "cocode":country
    }
    payload = urlencode(payload)
    full_url = url + payload
    response = requests.post(url=full_url)
    print(response.text)
    return response
