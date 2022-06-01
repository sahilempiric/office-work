# aa = '''
# Web login code. Dear Riken, we received a request from your account to log in on my.telegram.org. This is your login code: HFPbcQGDcbQ Do not give this code to anyone, even if they say they're from Telegram! This code can be used to delete your Telegram account. We never ask to send it anywhere. If you didn't request this code by trying to log in on my.telegram.org, simply ignore this message. Received at 10:39 AM
# '''

# a = aa.split('This is your login code: ')
# a.remove(a[0])
# a = a[0].split(' ')[0]

# print(a)


import requests,json

a = requests.get('http://127.0.0.1:8000/test')
# a = )
print(a.json())


# a = [1,2,34,4,5,6]
# a.reverse()
# print(a.count(34))


# a={
#     'b' : 'weqr'
# }
# # del a['b']
# print(a.items())


# response = '''1|Telegram code: 68399You can also tap on this link to log in:https://t.me/login/68399[HandLing]'''
# if 'telegram' in str(response).lower():
#     response = str(response).split('Telegram code:')[-1]
# #     response.replace('Telegram code: ','')
#     response = response.split(' ')[1].replace("You",'')
#     # response = response.replace("You",'')
# print(response)
# import random,string
# b = '243235'
# a = ''.join(random.choices(string.ascii_lowercase,k=5) )
# print(a,'===')

# import time
# def myfunc1():
#     print('hello')
#     time.sleep(4)
#     print('hello22')

# def myfunc2():
#     print('world')
#     time.sleep(4)
#     print('world22')



# from multiprocessing import Process
# p = Process(target=myfunc1)
# p.start()
# p2 = Process(target=myfunc2)
# p2.start()
# # and so on
# p.join()
# p2.join()

# print('-----------')
# def test():
#     import time
#     print('hello')
#     time.sleep(3)
#     print('world')
# from threading import Thread
# Thread(target=test).start()
# print("this will be printed immediately")