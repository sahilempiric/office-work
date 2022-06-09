import datetime
import time

import requests
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts_conf import PCS
from conf import WEB_HOOK_URL
from core.models import AccountStatusReport
from main import LOGGER
from surviral_avd.settings import SYSTEM_NO
from instagram.models import TwitterActionLog, TwitterAccount
from instagram.report import ActionReport
from utils import get_datetime_date_str


class Command(BaseCommand):
    def __init__(self):
        super().__init__()

    def add_arguments(self, parser):
        parser.add_argument(
            "--post_report",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help="Post the report to webhook if True",
        )

    def handle(self, *args, **options):
        post_report = options.get('post_report')

        total_active_accounts = 0
        total_active_updated_accounts = 0
        total_limited_accounts = 0
        total_suspended_accounts = 0
        total_inactive_accounts = 0
        total_eligible_for_engagement_accounts = 0
        total_banned_accounts = 0
        total_accounts = 0
        total_accounts_used_from_last_week_for_action = 0
        total_accounts_used_from_24_hour_for_action = 0
        total_accounts_created_in_last_24_hour = 0
        total_accounts_updated_in_last_24_hour = 0
        total_accounts_under_warm_up = 0
        total_likes_from_last_24_hour = 0
        total_retweets_from_last_24_hour = 0
        total_follows_from_last_24_hour = 0
        total_comments_from_last_24_hour = 0
        total_account_banned_from_last_24_hour = 0
        total_accounts_banned_from_last_week = 0
        available_pcs = [pc1 for pc1, pc2 in PCS]
        for sys_no in available_pcs:
            report_obj = AccountStatusReport.objects.using("monitor").filter(system_no=sys_no)
            if report_obj.exists():
                system_obj = report_obj.first()
                total_accounts += system_obj.total_accounts
                total_active_accounts += system_obj.active_accounts
                total_active_updated_accounts += system_obj.active_updated_accounts
                total_limited_accounts += system_obj.limited_accounts
                total_suspended_accounts += system_obj.suspended_accounts
                total_inactive_accounts += system_obj.inactive_accounts
                total_eligible_for_engagement_accounts += system_obj.eligible_for_engagement_accounts
                total_banned_accounts += system_obj.banned_accounts
                total_accounts_used_from_last_week_for_action += system_obj.accounts_used_from_last_week_for_action
                total_accounts_used_from_24_hour_for_action += system_obj.accounts_used_from_24_hour_for_action
                total_accounts_created_in_last_24_hour += system_obj.accounts_created_in_last_24
                total_accounts_updated_in_last_24_hour += system_obj.accounts_updated_in_last_24
                total_accounts_under_warm_up += system_obj.active_accounts - system_obj.eligible_for_engagement_accounts
                total_likes_from_last_24_hour += system_obj.likes_from_24_hour
                total_retweets_from_last_24_hour += system_obj.retweets_from_24_hour
                total_follows_from_last_24_hour += system_obj.follows_from_24_hour
                total_comments_from_last_24_hour += system_obj.comments_from_24_hour
                total_account_banned_from_last_24_hour += system_obj.accounts_banned_from_last_24_hour
                total_accounts_banned_from_last_week += system_obj.accounts_banned_from_last_week
        report = {'Total Accounts': total_accounts,
                  'Total Active Accounts': total_active_accounts,
                  'Total Active Updated_Accounts': total_active_updated_accounts,
                  'Total Eligible For Engagement_Accounts': total_eligible_for_engagement_accounts,
                  'Total Accounts Used From Last Week For Actions': total_accounts_used_from_last_week_for_action,
                  'Total Accounts Used From 24 Hour For Actions': total_accounts_used_from_24_hour_for_action,
                  'Total Accounts Created In Last 24 Hour': total_accounts_created_in_last_24_hour,
                  'Total Accounts Updated In Last 24 Hour': total_accounts_updated_in_last_24_hour,
                  'Total Accounts_Under_Warm_Up': total_accounts_under_warm_up,
                  'Total Limited Accounts': total_limited_accounts,
                  'Total Suspended Accounts': total_suspended_accounts,
                  'Total Inactive Accounts': total_inactive_accounts,
                  'Total Banned Accounts': total_banned_accounts,
                  'Total Likes from last 24 hour': total_likes_from_last_24_hour,
                  'Total Retweets from last 24 hour': total_retweets_from_last_24_hour,
                  'Total Follows from last 24 hour': total_follows_from_last_24_hour,
                  'Total Comments from last 24 hour': total_comments_from_last_24_hour,
                  "Total Accounts banned from last 24 hour": total_account_banned_from_last_24_hour,
                  'Total Accounts banned from last week': total_accounts_banned_from_last_week}
        payload_text = ""
        payload_text += "*" * 60 + "\n"
        payload_text += f"Twitter accounts statistics Report: {time.ctime()}\n"
        payload_text += "*" * 60 + "\n"
        for key, value in report.items():
            payload_text += f"{key} = {value}\n"
        payload_text += "*" * 60 + "\n"
        print(payload_text)
        if post_report:
            payload = {"text": payload_text}
            r = requests.post(WEB_HOOK_URL, json=payload)
            LOGGER.info(f"WEB HOOK Post Response:")
            LOGGER.info(r.text)
