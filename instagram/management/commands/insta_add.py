from socketserver import UDPServer
import time, pandas as pd
from xml.dom import UserDataHandler
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from instagram.models import  user_detail_local
import random
# from twbot.management.commands.bot.create_acc import create_acc
from datetime import datetime

class Command(BaseCommand):
    help = 'Create random users'

   
        
    def handle(self, *args, **kwargs):


        all_inactive = user_detail_local.objects.using('monitor').filter(status="LOGIN_ISSUE")
        for i in all_inactive:
            from core.models import Inactive_accounts
            Inactive_accounts.objects.using('monitor').using('monitor').create(
              user_detail = i,
              updated = i.updated  
            )


        # user_detail.objects.all().delete()
        # data = pd.read_csv('/home/eu4/Desktop/Riken/insta_new_tw/surviral_avd-debug/backups/1195_acc.csv')   # for creating accounts
        # # data = pd.read_csv('/home/eu4/Desktop/Riken/insta_new_tw/surviral_avd-debug/backups/156_updated.csv')  # for updating profile updated
        # print(len(data))
        # print(data.iloc[0]['username'])
        # for i in range(len(data)):
            # print(i)
            # avdsname = data[i]['avdsname']
            # username = data.loc[i]['username']
            # number = data[i]['number']
            # password = data[i]['password']
            # birth_date = data[i]['birth_date']
            # birth_month = data[i]['birth_month']
            # birth_year = data[i]['birth_year']
            # updated = data[i]['updated']


    # for adding new users


            # if not user_detail.objects.using('monitor').filter(username = username).exists():
            #     aa = user_detail.objects.create(
            #         avdsname = str(data.loc[i]['avdsname']),
            #         username = str(data.loc[i]['username']),
            #         number = str(data.loc[i]['number']),
            #         password = str(data.loc[i]['password']),
            #         birth_date = str(data.loc[i]['birth_date']),
            #         birth_month = str(data.loc[i]['birth_month']),
            #         birth_year = str(data.loc[i]['birth_year']),
            #         updated = data.loc[i]['updated'],
            #         created_at = data.loc[i]['created_at']
            #     )
            #     print(aa.username)
            # if  user_detail.objects.filter(username = username).exists():
            #     aa = user_detail.objects.filter(username = username).first()
            #     aa.created_at = data.loc[i]['created_at']
            #     aa.save()


    # for updating the user ig the profile is updated


            # if user_detail.objects.filter(username = username).exists():
            #     aa = user_detail.objects.filter(username = username).first()
            #     if (aa.updated == False ) and (data.loc[i]['updated'] == True):
            #         aa.updated = data.loc[i]['updated']
            #         aa.save()
                    
            #         print(aa.username,'---',aa.updated)