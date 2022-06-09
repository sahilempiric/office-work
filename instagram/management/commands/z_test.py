from socketserver import UDPServer
import time, pandas as pd
from xml.dom import UserDataHandler
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from instagram.models import  Inactive_accounts_local, User_action_local, user_detail_local
import random
from django.utils import timezone
from django.db.models import Sum

# from twbot.management.commands.bot.create_acc import create_acc
import datetime
from datetime import  timedelta, time
class Command(BaseCommand):
    help = 'Create random users'

   
        
    def handle(self, *args, **kwargs):
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        date_from = timezone.utc.localize(date_from)

        # Active accounts
        active_accounts = user_detail_local.objects.filter(status="ACTIVE").count()

        # Inactive Accounts
        # login_issued_accounts = user_detail_local.objects.filter(status="LOGIN_ISSUE").count()
        login_issued_accounts = Inactive_accounts_local.objects.all().count()
        login_issued_accounts24 = Inactive_accounts_local.objects.filter(created_at__gte = date_from).count()

        
        
        # Profile updated Accounts
        profile_updated_accounts = user_detail_local.objects.filter(updated=True).count()
        profile_updated_accounts24 = user_detail_local.objects.filter(updated=True,created_at__gte = date_from).count()

        # Total Accounts
        total_accounts = active_accounts + login_issued_accounts 



        # total eligible accounts
        elegible_time = datetime.datetime.now() - datetime.timedelta(days=7)
        elegible_time = timezone.utc.localize(elegible_time)
        elegible_time24 = datetime.datetime.now() - datetime.timedelta(days=8)
        elegible_time24 = timezone.utc.localize(elegible_time24)
        total_eligible_acc = user_detail_local.objects.filter(status="ACTIVE",updated=True,created_at__lte = elegible_time).count()
        total_eligible_acc24 = user_detail_local.objects.filter(status="ACTIVE",updated=True,created_at__lte = elegible_time,created_at__gte = elegible_time24).count()

        #total under warm up
        total_warm_up = user_detail_local.objects.filter(status="ACTIVE",updated=False).count()
        total_warm_up24 = user_detail_local.objects.filter(status="ACTIVE",updated=False,created_at__gte=date_from).count()

        # Accounts created from last 24 hours
        accounts_created_in_last_24 = user_detail_local.objects.filter(created_at__gte=date_from).count()

        # Accounts updated from last 24 hours
        accounts_updated_in_last_24 = user_detail_local.objects.filter(created_at__gte=date_from,updated=True).count()

        # likes
        total_likes = User_action_local.objects.aggregate(Sum('like'))['like__sum']
        total_likes24 = User_action_local.objects.filter(created_at__gte=date_from).aggregate(Sum('like'))['like__sum']
        # total_likes = User_action_local.objects.filter(user_detail_local__updated__contains = True)


        # comment
        total_comment = User_action_local.objects.aggregate(Sum('comment'))['comment__sum']
        total_comment24 = User_action_local.objects.filter(created_at__gte=date_from).aggregate(Sum('comment'))['comment__sum']


        # share
        total_share = User_action_local.objects.aggregate(Sum('share'))['share__sum']
        total_share24 = User_action_local.objects.filter(created_at__gte=date_from).aggregate(Sum('share'))['share__sum']

        # follow
        total_follow = User_action_local.objects.aggregate(Sum('follow'))['follow__sum']
        total_follow24 = User_action_local.objects.filter(created_at__gte=date_from).aggregate(Sum('follow'))['follow__sum']

        # random
        total_random = User_action_local.objects.filter(action_type= 'RANDOM').count()
        total_random24 = User_action_local.objects.filter(action_type= 'RANDOM',created_at__gte=date_from).count()

        # total action
        total_action = User_action_local.objects.all().count()
        total_action24 = User_action_local.objects.filter(created_at__gte=date_from).count()


        print("*" * 50)
        print(f"\t\tAccount status\n\t\t******* ******\nTime : {datetime.datetime.now()}")

        print("*" * 50)
        # print(f"Report genrate Time : {datetime.datetime.now()}")
        print(f"Total accounts: {total_accounts}")
        print(f"total eligible accounts for Engagement : {total_eligible_acc}")
        print(f"Total active accounts : {active_accounts}")
        print(f"Total Issued Accounts During login Time: {login_issued_accounts}")
        print(f"Total Profile updated accounts : {profile_updated_accounts}")
        print(f"Total Random action performed : {total_random}")
        print(f"Total Accounts under warm up : {total_warm_up}")
        print(f"Total Likes Accounts : {total_likes}")
        print(f"Total Comments Accounts : {total_comment}")
        print(f"Total Share Accounts : {total_share}")
        print(f"Total Follow Accounts : {total_follow}")
        print(f"Total Action performed : {total_action}")
        print(f"Total Accounts created in last 24 hours : {accounts_created_in_last_24}")
        print(f"Total New eligible Accounts for Engagement in last 24 hours: {total_eligible_acc24}")
        print(f"Total Issued Accounts During login Time in last 24 hours: {login_issued_accounts24}")
        print(f"Total profile updated in last 24 hours: {profile_updated_accounts24}")
        print(f"Total random action performed in last 24 hours: {total_random24}")
        print(f"Total added for warm up Accounts in last 24 hours: {total_warm_up24}")
        print(f"Total Likes in last 24 hours: {total_likes24}")
        print(f"Total Comment in last 24 hours: {total_comment24}")
        print(f"Total Share in last 24 hours: {total_share24}")
        print(f"Total Follow in last 24 hours: {total_follow24}")
        print(f"Total Action performed in last 24 houtrs : {total_action24}")
        # print(f"Total updated Accounts created in last 24 hours: {accounts_updated_in_last_24}")


        # print(f"AVDS's used from last week : {avds_used_from_last_week.__len__()}")
        print("*" * 50)


