from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from telethon import TelegramClient
from home.models import User_avds, user_details
from home.bot import Telegram_bot
import time

from home.conf import COUNTRY


class Command(BaseCommand):
    help = 'Create random users'


        # parser.add_argument('emulator', type=str, help='emulator of New user')

    def handle(self, *args, **kwargs):
        User_avds.objects.all().delete()
        aa = User_avds.objects.create(
            avdname='bavisi11',
            port=5554,

        )
        print(aa)
        # aa = User_avds.objects.all().first()
        tg = Telegram_bot(aa.avdname)
        tg.start_driver()
        tg.check_apk_installation()
        # if True:
        #     time.sleep(10)
        #     if not tg.connect_to_vpn(country=COUNTRY):
        #         print(tg.connect_to_vpn(country=COUNTRY))
        # input('Enter :')

        tg.create_account()

        

        # tg.Test()


        

        tg.kill_bot_process(True, True)
