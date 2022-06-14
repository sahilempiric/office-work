
# from urllib.parse import urlencode
from urllib.parse import urlencode
import requests



import time
# import s

# from urllib.parse import urlencode
# urlencode()


import urllib3 

def get_number(pid='10',country = 'hk'):
    url = "http://api.getsmscode.com/vndo.php?"

    while True:
            payload = {
                "action": "getmobile",
                "username": "pay@noborders.net",
                "token": "87269a810f4a59d407d0e0efe58185e6",
                "pid": pid,
                "cocode":country
            }
        # try:
            payload = urlencode(query=payload,doseq=0)
            print(payload)
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
        # except Exception as e:print(e)
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



print(get_number()) 