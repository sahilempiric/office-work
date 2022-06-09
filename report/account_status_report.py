import datetime

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from accounts_conf import PCS
from core.models import AccountStatusReport
from main import LOGGER
from surviral_avd.settings import SYSTEM_NO
from instagram.models import (TwitterActionLog, TwitterAccount, ActionForBotAccount, ActionForTargetAccount,
                          ActionForOtherAccount, ActionType, ActionResult
                          )
from instagram.report import ActionReport
from utils import get_datetime_date_str


class Command(BaseCommand):
    def __init__(self):
        super().__init__()

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # Active accounts
        active_accounts = TwitterAccount.objects.filter(status="ACTIVE").count()
        # Testing Accounts
        testing_accounts = TwitterAccount.objects.filter(status="TESTING").count()
        # Inactive Accounts
        inactive_accounts = TwitterAccount.objects.filter(status="INACTIVE").count()
        # Banned Accounts
        banned_accounts = TwitterAccount.objects.filter(status="BANNED").count()
        # Suspended Accounts
        suspended_accounts = TwitterAccount.objects.filter(status="SUSPENDED").count()
        # Limited Accounts
        limited_accounts = TwitterAccount.objects.filter(status="LIMITED").count()
        # Profile updated Accounts
        active_updated_accounts = TwitterAccount.objects.filter(profile_updated=True, status="ACTIVE").count()
        # Total Accounts
        total_accounts = TwitterAccount.objects.all().count()
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        date_from = timezone.utc.localize(date_from)
        # Accounts created from last 24 hours
        accounts_created_in_last_24 = TwitterAccount.objects.filter(created__gte=date_from).count()
        accounts_updated_in_last_24 = TwitterAccount.objects.filter(profile_updated_on__gte=date_from,
                                                                    profile_updated=True
                                                                    ).count()
        # Accounts banned from last 24 hour
        accounts_banned_from_last_24_hour = TwitterAccount.objects.filter(updated__gte=date_from
                                                                          ).exclude(status="ACTIVE").count()

        action_logs_from_last_24_hour = TwitterActionLog.objects.filter(created__gte=date_from)
        # # Accounts used from last 24 hour for engagement
        accounts_used_from_last_24_hour_for_action = set()
        for log in action_logs_from_last_24_hour:
            accounts_used_from_last_24_hour_for_action.add(log.avd.twitter_account)

        # Eligible accounts for engagement
        date_from = datetime.datetime.now() - datetime.timedelta(days=7)
        date_from = timezone.utc.localize(date_from)
        accounts_eligible_for_engagement = TwitterAccount.objects.filter(created__lte=date_from,
                                                                         profile_updated=True,
                                                                         status="ACTIVE"
                                                                         ).count()
        # Accounts banned from last week
        accounts_banned_from_last_week = TwitterAccount.objects.filter(updated__gte=date_from
                                                                       ).exclude(status="ACTIVE").count()

        action_logs_from_last_week = TwitterActionLog.objects.filter(created__gte=date_from)

        # Accounts used from last week for engagement
        accounts_used_from_last_week_for_action = set()
        for log in action_logs_from_last_week:
            accounts_used_from_last_week_for_action.add(log.avd.twitter_account)

        # Last 24-hour actions
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        date_from = timezone.utc.localize(date_from)
        action_log_from_24_hour = TwitterActionLog.objects.filter(created__gte=date_from)
        likes_from_24_hour = self.get_likes_from_24_hour()
        retweets_from_24_hour = self.get_retweets_from_24_hour()
        follows_from_24_hour = self.get_follows_from_24_hour()
        comments_from_24_hour = self.get_comments_from_24_hour()
        # Available PC's
        available_pcs = [pc1 for pc1, pc2 in PCS]
        if SYSTEM_NO in available_pcs:
            report_obj, created = AccountStatusReport.objects.using("monitor").get_or_create(system_no=SYSTEM_NO)
            report_obj.active_accounts = active_accounts
            report_obj.active_updated_accounts = active_updated_accounts
            report_obj.limited_accounts = limited_accounts
            report_obj.suspended_accounts = suspended_accounts
            report_obj.inactive_accounts = inactive_accounts
            report_obj.eligible_for_engagement_accounts = accounts_eligible_for_engagement
            report_obj.banned_accounts = banned_accounts
            report_obj.total_accounts = total_accounts
            report_obj.accounts_used_from_last_week_for_action = len(accounts_used_from_last_week_for_action)
            report_obj.accounts_used_from_24_hour_for_action = len(accounts_used_from_last_24_hour_for_action)
            report_obj.accounts_created_in_last_24 = accounts_created_in_last_24
            report_obj.accounts_updated_in_last_24 = accounts_updated_in_last_24
            report_obj.likes_from_24_hour = likes_from_24_hour
            report_obj.retweets_from_24_hour = retweets_from_24_hour
            report_obj.follows_from_24_hour = follows_from_24_hour
            report_obj.comments_from_24_hour = comments_from_24_hour
            report_obj.accounts_banned_from_last_24_hour = accounts_banned_from_last_24_hour
            report_obj.accounts_banned_from_last_week = accounts_banned_from_last_week
            report_obj.save()
            print(f"Updated account status of SYSTEM {SYSTEM_NO} to database")
        else:
            print(f"SYSTEM_NO : {SYSTEM_NO} is not in available PC's")
            print("Pls update proper SYSTEM_NO to environment")

    @staticmethod
    def get_comments_from_24_hour():
        # Last 24-hour actions
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        date_from = timezone.utc.localize(date_from)
        bot_account_comments = ActionForBotAccount.objects.filter(created__gte=date_from,
                                                                  result=ActionResult.SUCCESSFUL,
                                                                  action=ActionType.COMMENT_TWEET).count()
        target_account_comments = ActionForTargetAccount.objects.filter(created__gte=date_from,
                                                                        result=ActionResult.SUCCESSFUL,
                                                                        action=ActionType.COMMENT_TWEET).count()
        other_account_comments = ActionForOtherAccount.objects.filter(created__gte=date_from,
                                                                      result=ActionResult.SUCCESSFUL,
                                                                      action=ActionType.COMMENT_TWEET).count()
        total_comments = bot_account_comments + target_account_comments + other_account_comments
        return total_comments

    @staticmethod
    def get_likes_from_24_hour():
        # Last 24-hour actions
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        date_from = timezone.utc.localize(date_from)
        bot_account_likes = ActionForBotAccount.objects.filter(created__gte=date_from,
                                                               result=ActionResult.SUCCESSFUL,
                                                               action=ActionType.LIKE_TWEET).count()
        target_account_likes = ActionForTargetAccount.objects.filter(created__gte=date_from,
                                                                     result=ActionResult.SUCCESSFUL,
                                                                     action=ActionType.LIKE_TWEET).count()
        other_account_likes = ActionForOtherAccount.objects.filter(created__gte=date_from,
                                                                   result=ActionResult.SUCCESSFUL,
                                                                   action=ActionType.LIKE_TWEET).count()
        total_likes = bot_account_likes + target_account_likes + other_account_likes
        return total_likes

    @staticmethod
    def get_follows_from_24_hour():
        # Last 24-hour actions
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        date_from = timezone.utc.localize(date_from)
        bot_account_follows = ActionForBotAccount.objects.filter(created__gte=date_from,
                                                                 result=ActionResult.SUCCESSFUL,
                                                                 action=ActionType.FOLLOW_ACCOUNT).count()
        target_account_follows = ActionForTargetAccount.objects.filter(created__gte=date_from,
                                                                       result=ActionResult.SUCCESSFUL,
                                                                       action=ActionType.FOLLOW_ACCOUNT).count()
        other_account_follows = ActionForOtherAccount.objects.filter(created__gte=date_from,
                                                                     result=ActionResult.SUCCESSFUL,
                                                                     action=ActionType.FOLLOW_ACCOUNT).count()
        total_follows = bot_account_follows + target_account_follows + other_account_follows
        return total_follows

    @staticmethod
    def get_retweets_from_24_hour():
        # Last 24-hour actions
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        date_from = timezone.utc.localize(date_from)
        bot_account_retweets = ActionForBotAccount.objects.filter(created__gte=date_from,
                                                                  result=ActionResult.SUCCESSFUL,
                                                                  action=ActionType.RETWEET_TWEET).count()
        target_account_retweets = ActionForTargetAccount.objects.filter(created__gte=date_from,
                                                                        result=ActionResult.SUCCESSFUL,
                                                                        action=ActionType.RETWEET_TWEET).count()
        other_account_retweets = ActionForOtherAccount.objects.filter(created__gte=date_from,
                                                                      result=ActionResult.SUCCESSFUL,
                                                                      action=ActionType.RETWEET_TWEET).count()
        total_retweets = bot_account_retweets + target_account_retweets + other_account_retweets
        return total_retweets
