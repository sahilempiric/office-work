from collections import UserList
from pprint import pprint
from urllib.request import DataHandler
from django.core.management.base import BaseCommand
from home.models import user_details
from .functions_file.function_msg import *
import pandas as pd 

class Command(BaseCommand):
    help = 'send message as per csv'

    def handle(self,*args, **kwargs):

        aa = user_details.objects.all()
        count = 0
        succ_count = 0
        # for i in range(60):
        while succ_count < 60:
            from home.management.commands.functions_file.function_msg import script_chat
            user = aa[count]
            valu,bcs = script_chat(1,user.number,user.api_id,user.api_hash,'testing','qatestingxana')
            print(valu)
            # if
            count += 1
            if valu:succ_count += 1

