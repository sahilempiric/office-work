from collections import UserList
from pprint import pprint
from urllib.request import DataHandler
from django.core.management.base import BaseCommand
from Telegram.settings import WEB_HOOK_URL
from home.models import user_details
from .functions_file.function_msg import *
import pandas as pd 
from django.db.models import Sum
import datetime
from datetime import  timedelta, time
from django.utils import timezone

date_from = datetime.datetime.now() - datetime.timedelta(days=1)
# date_from = timezone.utc.localize(date_from)
class Command(BaseCommand):
    help = 'send message as per csv'

    def handle(self,*args, **kwargs):
        total_acc = user_details.objects.all().count()
        total_acc24 = user_details.objects.filter(created_at__gte=date_from).count()

        comment = user_details.objects.aggregate(Sum('comment'))['comment__sum']
        views = user_details.objects.aggregate(Sum('views'))['views__sum']
        banned = user_details.objects.aggregate(Sum('banned'))['banned__sum']
        comment_24 = user_details.objects.filter(created_at__gte=date_from).aggregate(Sum('comment'))['comment__sum']
        views_24 = user_details.objects.filter(created_at__gte=date_from).aggregate(Sum('views'))['views__sum']
        banned_24 = user_details.objects.filter(created_at__gte=date_from).aggregate(Sum('banned'))['banned__sum']
        # print(all_user)

        print(total_acc,total_acc24,comment,comment_24,views,views_24)
        report = [
            f'Total accounts : {total_acc}',
            f'Total send comments : {comment}',
            f'Total send Views : {views}',
            f'Total banned user : {banned}',
            f'Total accounts created in last 24 hours  : {total_acc}',
            f'Total send comments in last 24 hours: {comment_24}',
            f'Total send Views in last 24 hours: {views_24}',
            f'Total banned user in last 24 hours: {banned_24}',
        ]
        text = ""
        text += "*" * 50+'\n'
        text += f"\t\tTelegram Account status\nTime : {datetime.datetime.now()}"+'\n'
        text += "*" * 50+'\n'
        for i in report: 
            text+= f"{i}"
            text+="\n"
        text += "*" * 50+'\n'
        print(text)


        if text:
            payload = {"text":text}
            print(payload)
            r = requests.post(WEB_HOOK_URL, json=payload)
            LOGGER.info(f"WEB HOOK Post Response:")
            LOGGER.info(r.text)