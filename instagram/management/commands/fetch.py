from pprint import pprint
from django.core.management.base import BaseCommand
from conf import WEB_HOOK_URL
from core.models import instagram_report_test
from core.models import  *
import random, requests
from django.utils import timezone
from django.db.models import Sum
# from twbot.management.commands.bot.create_acc import create_acc
# from datetime import datetime
import datetime
from datetime import  timedelta, time
from surviral_avd.settings import SYSTEM_NO
from accounts_conf import PCS
class Command(BaseCommand):
    help = 'Create random users'

   
        
    def handle(self, *args, **kwargs):
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        date_from = timezone.utc.localize(date_from)
        elegible_time = datetime.datetime.now() - datetime.timedelta(days=7)
        elegible_time = timezone.utc.localize(elegible_time)
        elegible_time24 = datetime.datetime.now() - datetime.timedelta(days=8)
        elegible_time24 = timezone.utc.localize(elegible_time24)
        insta_report = instagram_report_test.objects.using('monitor').filter(system__in  = [pc1 for pc1, pc2 in PCS])
        total_accounts = user_detail.objects.using('monitor').all().count()
        total_eligible_acc = user_detail.objects.using('monitor').filter(status="ACTIVE",updated=True,created_at__lte = elegible_time).count()
        active_accounts = user_detail.objects.using('monitor').filter(status="ACTIVE").count()

        login_issued_accounts = Inactive_accounts.objects.using('monitor').all().count()
        profile_updated_accounts = user_detail.objects.using('monitor').filter(updated=True).count()
        total_random = User_action.objects.using('monitor').filter(action_type= 'RANDOM').count()
        total_warm_up = user_detail.objects.using('monitor').filter(status="ACTIVE",updated=False).count()
        total_likes = User_action.objects.using('monitor').aggregate(Sum('like'))['like__sum']
        total_comment = User_action.objects.using('monitor').aggregate(Sum('comment'))['comment__sum']
        total_share = User_action.objects.using('monitor').aggregate(Sum('share'))['share__sum']
        total_follow = User_action.objects.using('monitor').aggregate(Sum('follow'))['follow__sum']
        total_action = User_action.objects.using('monitor').all().count()
        accounts_created_in_last_24 = user_detail.objects.using('monitor').filter(created_at__gte=date_from).count()
        total_eligible_acc24 = user_detail.objects.using('monitor').filter(status="ACTIVE",updated=True,created_at__lte = elegible_time,created_at__gte = elegible_time24).count()
        login_issued_accounts24 = Inactive_accounts.objects.using('monitor').filter(created_at__gte = date_from).count()
        profile_updated_accounts24 = user_detail.objects.using('monitor').filter(updated=True,created_at__gte = date_from).count()
        total_random24 = User_action.objects.using('monitor').filter(action_type= 'RANDOM',created_at__gte=date_from).count()
        total_warm_up24 = user_detail.objects.using('monitor').filter(status="ACTIVE",updated=False,created_at__gte=date_from).count()
        total_likes24 = User_action.objects.using('monitor').filter(created_at__gte=date_from).aggregate(Sum('like'))['like__sum']
        total_comment24 = User_action.objects.using('monitor').filter(created_at__gte=date_from).aggregate(Sum('comment'))['comment__sum']
        total_share24 = User_action.objects.using('monitor').filter(created_at__gte=date_from).aggregate(Sum('share'))['share__sum']
        total_follow24 = User_action.objects.using('monitor').filter(created_at__gte=date_from).aggregate(Sum('follow'))['follow__sum'] 
        total_action24 = User_action.objects.using('monitor').filter(created_at__gte=date_from).count()
        # for i in insta_report:
        #     total_accounts += i.total_Account
        #     total_eligible_acc += i.total_eligible_for_engagement_account
        #     active_accounts+= i.total_active_accounts
        #     login_issued_accounts += i.total_issued_accounts_in_login
        #     profile_updated_accounts+= i.total_updated_accounts
        #     total_random += i.total_random_action
        #     total_warm_up += i.total_accounts_under_warm_up
        #     total_likes += i.total_likes
        #     total_comment += i.total_comments
        #     total_share += i.total_share
        #     total_follow += i.total_follow
        #     total_action += i.total_action
        #     accounts_created_in_last_24 += i.total_accounts_created_in_last_24hours
        #     total_eligible_acc24 += i.total_new_eligible_accounts_in_login_in_last_24hours
        #     login_issued_accounts24 += i.total_issued_accounts_in_login_in_last_24hours
        #     profile_updated_accounts24 += i.total_accounts_updated_in_last_24hours
        #     total_random24 += i.total_random_action_performed_in_24hours
        #     total_warm_up24 += i.total_accounts_added_under_warm_upin_last_24hours
        #     total_likes24 += i.total_likes_in_last_24hours
        #     total_comment24 += i.total_comments_in_last_24hours
        #     total_share24 += i.total_share_in_last_24hours
        #     total_follow24 += i.total_follow_in_last_24hours
        #     total_action24 += i.total_action_performed_in_last_24hours

        report = [
            f"Total accounts = {total_accounts} ",
            f"Total active accounts = {active_accounts}",
            f"total eligible accounts for Engagement = {total_eligible_acc} ",
            f"Total Issued Accounts During login Time = {login_issued_accounts}",
            f"Total Profile updated accounts = {profile_updated_accounts} ",
            f"Total Random action performed = {total_random}",
            f"Total Accounts under warm up = {total_warm_up}",
            f"Total Likes Accounts = {total_likes}",
            f"Total Comments Accounts = {total_comment}",
            f"Total Share Accounts = {total_share} ",
            f"Total Follow Accounts = {total_follow} ",
            f"Total Action performed = {total_action}",
            f"Total Accounts created in last 24 hours = {accounts_created_in_last_24} ",
            f"Total New eligible Accounts for Engagement in last 24 hours = {total_eligible_acc24} ",
            f"Total Issued Accounts During login Time in last 24 hours = {login_issued_accounts24}",
            f"Total profile updated in last 24 hours = {profile_updated_accounts24}",
            f"Total random action performed in last 24 hours = {total_random24}",
            f"Total added for warm up Accounts in last 24 hours = {total_warm_up24} ",
            f"Total Likes in last 24 hours = {total_likes24}",
            f"Total Comment in last 24 hours = {total_comment24} ",
            f"Total Share in last 24 hours = {total_share24}",
            f"Total Follow in last 24 hours = {total_follow24}",
            f"Total Action performed in last 24 houtrs = {total_action24}",
        ]
        # pprint(report)

        text = ""
        text += "*" * 50+'\n'
        text += f"\t\tAccount status\n\t\t******* ******\nTime : {datetime.datetime.now()}"+'\n'
        text += "*" * 50+'\n'
        for i in report: 
            text+= f"{i}"
            text+="\n"
        text += "*" * 50+'\n'
        print(text)

        # if text:
        #     payload = {"text":text}
        #     print(payload)
        #     r = requests.post(WEB_HOOK_URL, json=payload)
        #     LOGGER.info(f"WEB HOOK Post Response:")
        #     LOGGER.info(r.text)


        







        # "Total accounts" : total_accounts ,
        #     "total eligible accounts for Engagement " : total_eligible_acc ,
        #     "Total active accounts " :  active_accounts,
        #     "Total Issued Accounts During login Time" :  login_issued_accounts,
        #     "Total Profile updated accounts " : profile_updated_accounts ,
        #     "Total Random action performed " :  total_random,
        #     "Total Accounts under warm up " :  total_warm_up,
        #     "Total Likes Accounts " :  total_likes,
        #     "Total Comments Accounts " :  total_comment,
        #     "Total Share Accounts " : total_share ,
        #     "Total Follow Accounts " : total_follow ,
        #     "Total Action performed " :  total_action,
        #     "Total Accounts created in last 24 hours " : accounts_created_in_last_24 ,
        #     "Total New eligible Accounts for Engagement in last 24 hours" : total_eligible_acc24 ,
        #     "Total Issued Accounts During login Time in last 24 hours" :  login_issued_accounts24,
        #     "Total profile updated in last 24 hours" :  profile_updated_accounts24,
        #     "Total random action performed in last 24 hours" :  total_random24,
        #     "Total added for warm up Accounts in last 24 hours" : total_warm_up24 ,
        #     "Total Likes in last 24 hours" :  total_likes24,
        #     "Total Comment in last 24 hours" : total_comment24 ,
        #     "Total Share in last 24 hours" :  total_share24,
        #     "Total Follow in last 24 hours" :  total_follow24,
        #     "Total Action performed in last 24 houtrs " :  total_action24,