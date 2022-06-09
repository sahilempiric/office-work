from socketserver import UDPServer
import time, pandas as pd
from importlib_metadata import PathDistribution
from click import open_file
from xml.dom import UserDataHandler
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from instagram.actions.follow import T
from instagram.models import   Engagement_agent_user_local, Engagement_local
from core.models import Engagement, User_action,user_detail,Engagement_agent_user
import random
from django.utils import timezone
from django.db.models import Sum
from django.core.management.base import BaseCommand
from core.models import Engagement, Engagement_agent_user, Inactive_accounts, User_action, user_detail
from instagram.models import Engagement_agent_user_local, Engagement_local, Inactive_accounts_local, User_action_local, user_detail_local
# from twbot.management.commands.bot.create_acc import create_acc
import datetime,os
from datetime import  timedelta, time
from main import LOGGER

class Command(BaseCommand):
    help = 'Create random users'

  
    
    def handle(self, *args, **kwargs):
        # print(list(user_detail_local.objects.filter(updated=True,status='ACTIVE',following__gt = 1 ).order_by('?')))
        # a = user_detail_local.objects.filter(username='mark4875hall').first()
        # a.can_search = False
        # a.save()
        a = user_detail.objects.using('monitor').filter(followers__gte = 2)
        # a = user_detail_local.objects.filter(username = 'david373campbell').first()
        print(a)
        for i in a:
            print(i.followers)
    
        a = user_detail.objects.using('monitor').filter(username = 'philippowell908').first()
        print(a.password)
        # a = user_detail_local.objects.filter(username='ericchaney55').first()
        # print(a.followers)
        # print(a.can_search)
        # print(user_detail_local.objects.filter(username='brandonhansen869').first().following)
        # a = user_detail_local.objects.filter(username='Chris15112470').first()
        # a.random_action += 1
        # a.save()
        # for i_l in User_action_local.objects.all():
        #     print(i_l)
        #     if not User_action.objects.using('monitor').filter(action_id=i_l.action_id).exists():
        #         if i_l.action_type == "RANDOM":
        #             a=User_action.objects.using('monitor').create(
        #                 action_id = i_l.action_id,
        #                 # agent_user = Engagement_agent_user.objects.using(   'monitor').filter(order_id=i_l.agent_user.order_id).first(),
        #                 user_detail = user_detail.objects.using('monitor').filter(username=i_l.user_detail.username).first(),
        #                 like = i_l.like,
        #                 comment = i_l.comment,
        #                 share = i_l.share,
        #                 follow = i_l.follow,
        #                 action_type = i_l.action_type
        #             )
        #         elif i_l.action_type == "ENGAGEMENT":
        #             if not User_action.objects.using('monitor').filter(action_id=i_l.action_id).exists():
        #                 print(f'\n\n{i_l}\n\n')
        #                 a=User_action.objects.using('monitor').create(
        #                     action_id = i_l.action_id,
        #                     agent_user = Engagement_agent_user.objects.using('monitor').filter(order_id=i_l.agent_user.order_id).first(),
        #                     user_detail = user_detail.objects.using('monitor').filter(username=i_l.user_detail.username).first(),
        #                     like = i_l.like,
        #                     comment = i_l.comment,
        #                     share = i_l.share,
        #                     follow = i_l.follow,
        #                     action_type = i_l.action_type
        #                 )
        # for i_a in User_action.objects.using('monitor').all():
        #     print(i_a)
        #     if not User_action_local.objects.filter(action_id=i_a.action_id).exists():
        #         if i_a.action_type == "RANDOM":
        #             a=User_action_local.objects.create(
        #                 action_id = i_a.action_id,
        #                 # agent_user = Engagement_agent_user_local.objects.filter(order_id=i_a.agent_user.order_id).first(),
        #                 user_detail = user_detail_local.objects.filter(username=i_a.user_detail.username).first(),
        #                 like = i_a.like,
        #                 comment = i_a.comment,
        #                 share = i_a.share,
        #                 follow = i_a.follow,
        #                 action_type = i_a.action_type
        #             )
        #         elif i_a.action_type == "ENGAGEMENT":
        #             a=User_action_local.objects.create(
        #                 action_id = i_a.action_id,
        #                 agent_user = Engagement_agent_user_local.objects.filter(order_id=i_a.agent_user.order_id).first(),
        #                 user_detail = user_detail_local.objects.filter(username=i_a.user_detail.username).first(),
        #                 like = i_a.like,
        #                 comment = i_a.comment,
        #                 share = i_a.share,
        #                 follow = i_a.follow,
        #                 action_type = i_a.action_type)



        # b = user_detail_local.objects.filter(username='tylerross3771').first()
        # print(b.id)
        # print(b.updated)
        # print(User_action_local.objects.all().count())
        # print(User_action.objects.using('monitor').filter(action_id='9d5701e1-2ace-422a-9d49-05498c183ef4').exists())
        # print(User_action.objects.using('monitor').filter(like = 0).exists())
        # # for i_a in User_action.objects.using('monitor').all():
        # #     print(i_a.action_id)

        # all_user_a = user_detail.objects.using('monitor').all()
        # for i_a in all_user_a:
        #     # if i_a.id < 1200:
        #         # print(i_a.id)
        #         # continue
        #     if not user_detail_local.objects.filter(username=i_a.username).exists():
        #         aa = user_detail_local.objects.create(
        #             avdsname = i_a.avdsname,
        #             username = i_a.username,
        #             number = i_a.number,
        #             password = i_a.password,
        #             birth_date = i_a.birth_date,
        #             birth_month = i_a.birth_month,
        #             birth_year = i_a.birth_year,
        #             updated = i_a.updated,
        #             random_action = i_a.random_action,
        #             status = i_a.status,
        #             created_at = i_a.created_at,
        #             updated_at = i_a.updated_at
        #         )
        #         LOGGER.debug(aa.username)
        #     elif user_detail_local.objects.filter(username=i_a.username).exists():
        #         i_l = user_detail_local.objects.filter(username=i_a.username).first()
        #         if i_a.updated == True :
        #             i_l.updated = True
        #         if i_l.updated == True:
        #             i_a.updated = True
                
        #         if i_a.random_action < i_l.random_action :
        #             i_a.random_action = i_l.random_action
        #         if i_a.random_action > i_l.random_action :
        #             i_l.random_action = i_a.random_action

        #         if i_a.status == "LOGIN_ISSUE":
        #             i_l.status = "LOGIN_ISSUE"
        #         if  i_l.status =="LOGIN_ISSUE":
        #             i_a.status = "LOGIN_ISSUE"
                
        #         i_a.save()
        #         i_l.save()
        #         LOGGER.info(f'{i_a.id} -> {i_a} -- {i_l}')
        #     else:print(f'\n\n{i_a}\n\n')
        # import pandas as pd
        # user_action = pd.read_csv('/home/eu4/Desktop/Riken/insta_new_tw/surviral_avd-debug/action_insta.csv')
        # for i in range(len(user_action)):
        #     User_action_local.objects.create(

        #         like = user_action.loc[i]['like'],
        #         comment = user_action.loc[i]['comment'],
        #         share = user_action.loc[i]['share'],
        #         follow = user_action.loc[i]['follow'],
        #         action_type = user_action.loc[i]['action_type'],
        #         created_at = user_action.loc[i]['created_at'],
        #         updated_at = user_action.loc[i]['updated_at'],
        #         user_detail_id = user_action.loc[i]['user_detail_id'],
        #         # agent_user_id = user_action.loc[i]['agent_user_id']
        #     )


        # print(User_action.objects.using('monitor').all().count())
        # for i in User_action_local.objects.all():
        # #     print(11)
        #     User_action.objects.using('monitor').create(
        #                 user_detail = user_detail.objects.using('monitor').filter(username=i.username).first(),
        #                 like = i.like,
        #                 comment = i.comment,
        #                 share = i.share,
        #                 follow = i.follow,
        #                 action_type = "RANDOM"
        #             )




        # print('---')
        # print(Inactive_accounts_local.objects.all().count())
        # for i_l in Inactive_accounts_local.objects.all():
        #     print(1)
        #     if not Inactive_accounts.objects.using('monitor').filter(user_detail__username = i_l.user_detail.username).exists():
        #         Inactive_accounts.objects.using('monitor').create(
        #             user_detail = user_detail.objects.using('monitor').filter(username = i_l.user_detail.username).first(),
        #             updated = i_l.user_detail.updated
        #         )
        # print(Inactive_accounts.objects.using('monitor').all().count())
        # for i_a in Inactive_accounts.objects.using('monitor').all():
        #     print(2)
        #     if not Inactive_accounts_local.objects.filter(user_detail__username = i_a.user_detail.username).exists():
        #         Inactive_accounts_local.objects.create(
        #             user_detail = user_detail_local.objects.filter(username = i_a.user_detail.username).first(),
        #             updated = i_a.user_detail.updated
        #         )

        # print(Engagement_local.objects.all())
        # for i_l in Engagement.objects.using('monitor').all():
            # print(i_l.agent_user.order_id)
            # print(Engagement.objects.using('monitor').filter(agent_user__order_id = i_l.agent_user__order_id))
            # print(Engagement.objects.using('monitor').filter(username=i_l.username,agent_user__order_id = i_l.agent_user.order_id))




        # for i_l in Engagement_agent_user_local.objects.all():
        #     if not Engagement_agent_user.objects.using('monitor').filter(agent_user = i_l.agent_user,order_id=i_l.order_id).exists():
        #         Engagement_agent_user.objects.using('monitor').create(
        #             order_id = i_l.order_id,
        #             agent_user = i_l.agent_user,
        #             total_likes = i_l.total_likes,
        #             total_shares = i_l.total_shares,
        #             total_comments = i_l.total_comments,
        #             total_follow = i_l.total_follow,
        #             liked = i_l.liked,
        #             commented = i_l.commented,
        #             followed = i_l.followed,
        #             shared = i_l.shared,
        #             completed = i_l.completed
        #         )


        # print(len(list(user_detail.objects.using('monitor').filter(updated = False,status = 'ACTIVE').order_by('?'))))
            # User_action.objects.using('monitor').create(
            #                             user_detail = list(user_detail.objects.using('monitor').filter(updated = True,status = 'ACTIVE').order_by('?'))[0],
            #                             like = 3,
            #                             comment = 3,
            #                             share = 0,
            #                             follow = 1,
            #                             action_type = 'RANDOM'
            #                         )
        # user_agent_name = os.getenv('AGENT_USER', '')
        # agent_user,a = Engagement_agent_user.objects.get_or_create(agent_user = user_agent_name,completed = False)
        # print(agent_user)
        # all_engaged_data = Engagement.objects.filter(agent_user=agent_user)
        # already_like = 0
        # already_comment = 0
        # already_shar = 0
        # already_follow = 0

        # for i in all_engaged_data:
        #     already_like+= i.liked
        #     already_comment += i.commented
        #     already_shar += i.shared
        #     already_follow += i.followed

        # print(already_comment,already_follow,already_like,already_shar)

        # if already_like < agent_user.total_likes:None

        # User_action.objects.create(
        # user_detail = list(user_detail.objects.filter(updated=True,status='ACTIVE').order_by('?'))[0],
        # like = 1,
        # comment = 2,
        # share = 1,
        # follow = 1,
        # action_type = 'RANDOM'
        # )
        # Engagement_agent_user.objects.create(
        # agent_user = 'xana',
        # total_likes = '10',
        # total_shares = '5',
        # total_comments = '6',
        # total_follow = '8',
        # liked = '0',
        # commented = '0',
        # followed = '0',
        # shared = '0',
        # completed = False
        # )

        # a = True
        # b = True
        # if a and b == True:
        #     print('yess')

        # a = Engagement_agent_user.objects.get_or_create(agent_user = 'xana',completed = False)
        # print(a)
    #       common part of task files
        # common_part = f"""
        # created_at = {datetime.datetime.now()}

        # # project path
        # export CURRENT_DIR=`dirname $(readlink -f $0)`
        # export PRJ_DIR=`dirname $CURRENT_DIR`
        # # go to project root directory
        # cd $PRJ_DIR
        # #. ./tasks/environment.sh
    

        # # Kill python and AVD process
        # killall -9 python qemu-system-x86_64

        # # activate the virtual environment for python
        # #. env/bin/activate
        
        # # update code
        # git pull origin $(git rev-parse --abbrev-ref HEAD)

        # # setup database
        # python manage.py setup --database
        # """
    
        # f = open(r'/home/eu4/Desktop/Riken/insta_new_tw/surviral_avd-debug/logic.txt','a+')
        # f.write(str(common_part))
        # f.close()
        # '/home/eu4/Desktop/Riken/insta_new_tw/surviral_avd-debug/logic.txt'.write_text(common_part )
        # print(User_action.objects.aggregate(Sum('like'))['like__sum'])











        # print(User_action.objects.filter(user_detail__updated = True)[0].like)

        # all_user = list(user_detail.objects.filter(updated  = True,status = "ACTIVE"))
        # User_action.objects.create(
        #     user_detail = all_user[-1],
        #     agent_user = 'another_test_user',
        #     like = 3,
        #     comment = 2,
        #     share = 4,
        #     follow = 6,
        #     action_type = "ENGAGEMENT"
        # )





        # print(Inactive_accounts.objects.all())
        # print(len(user_detail.objects.filter(status = "LOGIN_ISSUE")))
        # for i in user_detail.objects.filter(status = "LOGIN_ISSUE"):
        #     if not Inactive_accounts.objects.filter(user_detail = i).exists():
        #         print(i.username,1)
                
        #         Inactive_accounts.objects.create(
        #             user_detail = i,
        #             updated = i.updated
        #         )
        #     else:
        #         print(i.username,2)



        # all_user = list(user_detail.objects.all())
        # print(all_user)
        # for i in all_user:
        #     print(i.username) if i.username == 'brianfarmer25' else None
        #     print(all_user.index(i)) if i.username == 'brianfarmer25' else None
        #     if i.username == 'brianfarmer25' :
                
        #         User_action.objects.create(
        #             agent_user = 'test_user',
        #             user_detail = i,
        #             like = 3,
        #             comment = 2,
        #             share = 1,
        #             follow = 1,
        #             action_type = "ENGAGEMENT"
        #         )

        #     else :None

        # pass