from django.core.management.base import BaseCommand
from core.models import instagram_report_test
from instagram.models import  *
import random
from django.utils import timezone
from django.db.models import Sum
# from twbot.management.commands.bot.create_acc import create_acc
# from datetime import datetime
import datetime
from datetime import  timedelta, time
from surviral_avd.settings import SYSTEM_NO

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
        # total_likes = User_action_local.objects.filter(user_detail__updated__contains = True)


        # comment
        total_comment = User_action_local.objects.aggregate(Sum('comment'))['comment__sum']
        total_comment24 = User_action_local.objects.filter(created_at__gte=date_from).aggregate(Sum('comment'))['comment__sum']

        # share
        total_share = User_action_local.objects.aggregate(Sum('share'))['share__sum']
        total_share24 = User_action_local.objects.filter(created_at__gte=date_from).aggregate(Sum('share'))['share__sum']

        # follow
        total_follow = User_action_local.objects.aggregate(Sum('follow'))['follow__sum']
        total_follow24 = User_action_local.objects.filter(created_at__gte=date_from).aggregate(Sum('follow'))['follow__sum'] 
        print(total_follow24,'total_follow24')
        # random
        total_random = User_action_local.objects.filter(action_type= 'RANDOM').count()
        total_random24 = User_action_local.objects.filter(action_type= 'RANDOM',created_at__gte=date_from).count()

        # total action
        total_action = User_action_local.objects.all().count()
        total_action24 = User_action_local.objects.filter(created_at__gte=date_from).count()

        total_accounts = total_accounts if total_accounts != None else 0
        total_eligible_acc = total_eligible_acc if total_eligible_acc != None else 0
        active_accounts = active_accounts if active_accounts != None else 0
        login_issued_accounts = login_issued_accounts if login_issued_accounts != None else 0
        profile_updated_accounts = profile_updated_accounts if profile_updated_accounts != None else 0
        total_random = total_random if total_random != None else 0 
        total_warm_up = total_warm_up if total_warm_up != None else 0
        total_likes = total_likes if total_likes != None else 0
        total_comment = total_comment if total_comment != None else 0
        total_share = total_share if total_share != None else 0
        total_follow = total_follow if total_follow != None else 0
        total_action = total_action if total_action != None else 0
        accounts_created_in_last_24 = accounts_created_in_last_24 if accounts_created_in_last_24 != None else 0
        total_eligible_acc24 = total_eligible_acc24 if total_eligible_acc24 != None else 0 
        login_issued_accounts24 = login_issued_accounts24 if login_issued_accounts24 != None else 0
        profile_updated_accounts24 = profile_updated_accounts24 if profile_updated_accounts24 != None else 0
        total_random24 = total_random24 if total_random24 != None else 0
        total_warm_up24 = total_warm_up24 if total_warm_up24 != None else 0
        total_likes24 = total_likes24 if total_likes24 != None else 0
        total_comment24 = total_comment24 if total_comment24 != None else 0
        total_share24 = total_share24 if total_share24 != None else 0 
        total_follow24 = total_follow24 if total_follow24 != None else 0 
        total_action24 = total_action24 if total_action24 != None else 0

        if not instagram_report_test.objects.using('monitor').filter(system = SYSTEM_NO).exists():
            print('yess')
            instareport = instagram_report_test.objects.using('monitor').create(
            system = SYSTEM_NO,
            total_Account = total_accounts,
            total_eligible_for_engagement_account = total_eligible_acc,
            total_active_accounts = active_accounts,
            total_issued_accounts_in_login = login_issued_accounts,
            total_updated_accounts = profile_updated_accounts,
            total_random_action = total_random ,
            total_accounts_under_warm_up = total_warm_up,
            total_likes =total_likes,
            total_comments = total_comment,
            total_share = total_share,
            total_follow = total_follow,
            total_action = total_action,
            total_accounts_created_in_last_24hours = accounts_created_in_last_24,
            total_new_eligible_accounts_in_login_in_last_24hours =total_eligible_acc24 ,
            total_issued_accounts_in_login_in_last_24hours = login_issued_accounts24,
            total_accounts_updated_in_last_24hours = profile_updated_accounts24,
            total_random_action_performed_in_24hours = total_random24,
            total_accounts_added_under_warm_upin_last_24hours = total_warm_up24,
            total_likes_in_last_24hours = total_likes24,
            total_comments_in_last_24hours = total_comment24,
            total_share_in_last_24hours =total_share24 ,
            total_follow_in_last_24hours =total_follow24 ,
            total_action_performed_in_last_24hours =total_action24
            )
        else:
            print('Nooo')
            instareport = instagram_report_test.objects.using('monitor').filter(system = SYSTEM_NO)[0]
            
            instareport.total_Account = total_accounts
            instareport.total_eligible_for_engagement_account = total_eligible_acc
            instareport.total_active_accounts = active_accounts
            instareport.total_issued_accounts_in_login = login_issued_accounts
            instareport.total_updated_accounts = profile_updated_accounts
            instareport.total_random_action = total_random 
            instareport.total_accounts_under_warm_up = total_warm_up
            instareport.total_likes =total_likes
            instareport.total_comments = total_comment
            instareport.total_share = total_share
            instareport.total_follow = total_follow
            instareport.total_action = total_action
            instareport.total_accounts_created_in_last_24hours = accounts_created_in_last_24
            instareport.total_new_eligible_accounts_in_login_in_last_24hours =total_eligible_acc24 
            instareport.total_issued_accounts_in_login_in_last_24hours = login_issued_accounts24
            instareport.total_accounts_updated_in_last_24hours = profile_updated_accounts24
            instareport.total_random_action_performed_in_24hours = total_random24
            instareport.total_accounts_added_under_warm_upin_last_24hours = total_warm_up24
            instareport.total_likes_in_last_24hours = total_likes24
            instareport.total_comments_in_last_24hours = total_comment24
            instareport.total_share_in_last_24hours =total_share24 
            instareport.total_follow_in_last_24hours =total_follow24 
            instareport.total_action_performed_in_last_24hours =total_action24
            instareport.save()
            print(instareport)
        # pass