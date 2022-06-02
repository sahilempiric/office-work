from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from telethon import TelegramClient
from home.models import user_details

class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('number', type=str, help='Phone number of New user')
        parser.add_argument('api_id', type=str, help='api_id of New user')
        parser.add_argument('api_hash', type=str, help='api_hash of New user')
        # parser.add_argument('username', type=str, help='username of New user')
        # parser.add_argument('emulator', type=str, help='emulator of New user')

    def handle(self, *args, **kwargs):
        number = kwargs['number']
        api_id = kwargs['api_id']
        api_hash = kwargs['api_hash']
        print(number,api_id,api_hash)
        if user_details.objects.filter(number=number).exists():
            print('User is already Exists in Database !')
        else :
            tclient = TelegramClient(f'./sessions/{number}',api_id,api_hash)
            if tclient.start(phone=number):
                user_details.objects.create(number=number,api_id=api_id,api_hash=api_hash,username='Rrfgju',emulator='-')
                print('User Exists in database ')
            else:
                print('Please Enter Valid Credentials or OTP !')








                