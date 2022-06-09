from logging import Logger
from django.core.management.base import BaseCommand
from core.models import Engagement, Engagement_agent_user, Inactive_accounts, User_action, user_detail
from instagram.models import Engagement_agent_user_local, Engagement_local, Inactive_accounts_local, User_action_local, user_detail_local
from main import LOGGER
class Command(BaseCommand):

    def handle(self, *args, **options):
        

        # user details
        # if user_detail_local.objects.all().count() > user_detail.objects.using('monitor').all().count():
        for i_l in user_detail_local.objects.all():
            if not user_detail.objects.using('monitor').filter(username=i_l.username).exists():
                a = user_detail.objects.using('monitor').create(
                    avdsname = i_l.avdsname,
                    username = i_l.username,
                    number = i_l.number,
                    password = i_l.password,
                    birth_date = i_l.birth_date,
                    birth_month = i_l.birth_month,
                    birth_year = i_l.birth_year,
                    updated = i_l.updated,
                    random_action = i_l.random_action,
                    status = i_l.status,
                    # created_at = i_l.created_at,
                    # updated_at = i_l.updated_at
                )
                LOGGER.info(f'user id : {a.id} created in user on online storage')
            else:
                LOGGER.info(f'user id : {i_l.id} is already exists online storage')
        
        # if user_detail.objects.using('monitor').all().count() > user_detail_local.objects.all().count():
        for i_l in user_detail.objects.using('monitor').all():
            if not user_detail_local.objects.filter(username=i_l.username).exists():
                a = user_detail_local.objects.create(
                    avdsname = i_l.avdsname,
                    username = i_l.username,
                    number = i_l.number,
                    password = i_l.password,
                    birth_date = i_l.birth_date,
                    birth_month = i_l.birth_month,
                    birth_year = i_l.birth_year,
                    updated = i_l.updated,
                    random_action = i_l.random_action,
                    status = i_l.status,
                    # created_at = i_l.created_at,
                    # updated_at = i_l.updated_at
                )
                LOGGER.info(f'user id : {a.id} is created in user on local storage')
            else:
                LOGGER.info(f'user id : {i_l.id} is already exists local storage')

        # if user_detail.objects.using('monitor').all().count() > user_detail_local.objects.all().count():
        all_user_a = user_detail.objects.using('monitor').all()
        for i_a in all_user_a:
            # if i_a.id < 1200:
                # print(i_a.id)
                # continue
            if not user_detail_local.objects.filter(username=i_a.username).exists():
                aa = user_detail_local.objects.create(
                    avdsname = i_a.avdsname,
                    username = i_a.username,
                    number = i_a.number,
                    password = i_a.password,
                    birth_date = i_a.birth_date,
                    birth_month = i_a.birth_month,
                    birth_year = i_a.birth_year,
                    updated = i_a.updated,
                    random_action = i_a.random_action,
                    status = i_a.status,
                    created_at = i_a.created_at,
                    updated_at = i_a.updated_at
                )
                LOGGER.debug(aa.username)
            elif user_detail_local.objects.filter(username=i_a.username).exists():
                i_l = user_detail_local.objects.filter(username=i_a.username).first()
                if i_a.updated == True :
                    i_l.updated = True
                if i_l.updated == True:
                    i_a.updated = True
                
                if i_a.random_action < i_l.random_action :
                    i_a.random_action = i_l.random_action
                if i_a.random_action > i_l.random_action :
                    i_l.random_action = i_a.random_action

                if i_a.status == "LOGIN_ISSUE":
                    i_l.status = "LOGIN_ISSUE"
                if  i_l.status =="LOGIN_ISSUE":
                    i_a.status = "LOGIN_ISSUE"
                    
                if i_a.can_search == False :
                    i_l.can_search = False
                elif i_l.can_search == False:
                    i_a.can_search = False

                # if i_a.following == None:
                #     i_a.following = 0
                # if i_l.following == None:
                #     i_l.following = 0
                # i_a.save()
                # i_l.save()
                # if 
                print(i_a.id,i_l)
                # print(i_a.following , i_l.following,'i_a.following , i_l.following')
                if i_a.following > i_l.following:
                    i_l.following = i_a.following
                if i_a.following < i_l.following:
                    i_a.following = i_l.following

                if i_a.followers > i_l.followers:
                    i_l.followers = i_a.followers
                if i_a.followers < i_l.followers:
                    i_a.followers = i_l.followers

                
                i_a.save()
                i_l.save()
                LOGGER.info(f'user id : {i_a.id} is updated')

        
        # engageent agent user
        if Engagement_agent_user_local.objects.all().count() > Engagement_agent_user.objects.using('monitor').all().count():
            for i_l in Engagement_agent_user_local.objects.all():
                print(i_l.order_id)
                print(Engagement_agent_user.objects.using('monitor').filter(order_id=i_l.order_id).exists(),'sadsada')
                if Engagement_agent_user.objects.using('monitor').filter(order_id=i_l.order_id).exists():
                    pass
                else:
                    Engagement_agent_user.objects.using('monitor').create(
                        order_id = i_l.order_id,
                        agent_user = i_l.agent_user,
                        total_likes = i_l.total_likes,
                        total_shares = i_l.total_shares,
                        total_comments = i_l.total_comments,
                        total_follow = i_l.total_follow,
                        liked = i_l.liked,
                        commented = i_l.commented,
                        followed = i_l.followed,
                        shared = i_l.shared,
                        completed = i_l.completed
                    )
                    # LOGGER.info(f'{a} agent user is created at online storage')     

        if Engagement_agent_user.objects.using('monitor').all().count() > Engagement_agent_user_local.objects.all().count():
            for i_l in Engagement_agent_user.objects.using('monitor').all():
                if not Engagement_agent_user_local.objects.filter(order_id=i_l.order_id).exists():
                    a = Engagement_agent_user_local.objects.create(
                        order_id = i_l.order_id,
                        agent_user = i_l.agent_user,
                        total_likes = i_l.total_likes,
                        total_shares = i_l.total_shares,
                        total_comments = i_l.total_comments,
                        total_follow = i_l.total_follow,
                        liked = i_l.liked,
                        commented = i_l.commented,
                        followed = i_l.followed,
                        shared = i_l.shared,
                        completed = i_l.completed
                    )
                    LOGGER.info(f'{a} agent user is created at local storage')

        # if Engagement_agent_user.objects.using('monitor').all()
        for i_a in Engagement_agent_user_local.objects.all():
            if not Engagement_agent_user.objects.using('monitor').filter(order_id=i_a.order_id).exists():
                Engagement_agent_user_local.objects.create(
                    order_id = i_a.order_id,
                    agent_user = i_a.agent_user,
                    total_likes = i_a.total_likes,
                    total_shares = i_a.total_shares,
                    total_comments = i_a.total_comments,
                    total_follow = i_a.total_follow,
                    liked = i_a.liked,
                    commented = i_a.commented,
                    followed = i_a.followed,
                    shared = i_a.shared,
                    completed = i_a.completed
                )
                LOGGER.info(f'{a} agent user is created at local storage')
            elif Engagement_agent_user_local.objects.filter(order_id=i_a.order_id).exists():
                i_l = Engagement_agent_user_local.objects.filter(order_id=i_a.order_id).first()
                i_a.agent_user = i_l.agent_user
                if i_a.liked < i_l.liked :
                    i_a.liked = i_l.liked
                if i_a.liked > i_l.liked :
                    i_l.liked = i_a.liked

                if i_a.commented < i_l.commented :
                    i_a.commented = i_l.commented
                if i_a.commented > i_l.commented :
                    i_l.commented = i_a.commented
                    
                if i_a.followed < i_l.followed :
                    i_a.followed = i_l.followed
                if i_a.followed > i_l.followed :
                    i_l.followed = i_a.followed

                if i_a.shared < i_l.shared :
                    i_a.shared = i_l.shared
                if i_a.shared > i_l.shared :
                    i_l.shared = i_a.shared

                if i_l.completed == True:
                    i_a.completed = True
                if i_a.completed == True :
                    i_l.completed = True
                i_a.save()
                i_l.save()
                LOGGER.info(f'{i_a.agent_user} -- {i_l.agent_user}')


        #engagement 
        if Engagement_local.objects.all().count() > Engagement.objects.using('monitor').all().count():
            for i_l in Engagement_local.objects.all():
                if not Engagement.objects.using('monitor').filter(username=i_l.username,agent_user__order_id = i_l.agent_user.order_id).exists():
                    if Engagement_agent_user.objects.using('monitor').filter(order_id=i_l.agent_user.order_id).first() != None:
                        if user_detail.objects.using('monitor').filter(username=i_l.user_detail.username).first()  != None:
                            Engagement.objects.using('monitor').create(

                            avdsname = i_l.avdsname,
                            username = i_l.username,
                            agent_user = Engagement_agent_user.objects.using('monitor').filter(order_id=i_l.agent_user.order_id).first(),
                            user_detail = user_detail.objects.using('monitor').filter(username=i_l.user_detail.username).first(),
                            liked = i_l.liked,
                            commented = i_l.commented,
                            shared = i_l.shared,
                            followed = i_l.followed
                            )

        if Engagement.objects.using('monitor').all().count() > Engagement_local.objects.all().count():
            for i_a in Engagement.objects.using('monitor').all():
                if not Engagement_local.objects.filter(username=i_a.username,agent_user__order_id = i_a.agent_user.order_id).exists():
                    Engagement_local.objects.create(
                    avdsname = i_a.avdsname,
                    username = i_a.username,
                    agent_user = Engagement_agent_user_local.objects.filter(order_id=i_a.agent_user.order_id).first(),
                    user_detail = user_detail_local.objects.filter(username=i_a.user_detail.username).first(),
                    liked = i_a.liked,
                    commented = i_a.commented,
                    shared = i_a.shared,
                    followed = i_a.followed
                    )

        # inactive
        if Inactive_accounts_local.objects.all().count() > Inactive_accounts.objects.using('monitor').all().count():
            for i_l in Inactive_accounts_local.objects.all():
                if not Inactive_accounts.objects.using('monitor').filter(user_detail__username = i_l.user_detail.username).exists():
                    Inactive_accounts.objects.using('monitor').create(
                        user_detail = user_detail.objects.using('monitor').filter(username = i_l.user_detail.username).first(),
                        updated = i_l.user_detail.updated
                    )
            
        if Inactive_accounts.objects.using('monitor').all().count() > Inactive_accounts_local.objects.all().count():
            for i_a in Inactive_accounts.objects.using('monitor').all():
                if not Inactive_accounts_local.objects.filter(user_detail__username = i_a.user_detail.username).exists():
                    Inactive_accounts_local.objects.create(
                        user_detail = user_detail_local.objects.filter(username = i_a.user_detail.username).first(),
                        updated = i_a.user_detail.updated
                    )

        
        # User_action
        if User_action_local.objects.all().count() > User_action.objects.using('monitor').all().count():
            for i_l in User_action_local.objects.all():
                if not User_action.objects.using('monitor').filter(action_id=i_l.action_id).exists():
                    if i_l.action_type == "RANDOM":
                        a=User_action.objects.using('monitor').create(
                            action_id = i_l.action_id,
                            # agent_user = Engagement_agent_user.objects.using('monitor').filter(order_id=i_l.agent_user.order_id).first(),
                            user_detail = user_detail.objects.using('monitor').filter(username=i_l.user_detail.username).first(),
                            like = i_l.like,
                            comment = i_l.comment,
                            share = i_l.share,
                            follow = i_l.follow,
                            action_type = i_l.action_type
                        )
                    elif i_l.action_type == "ENGAGEMENT":
                        if not User_action.objects.using('monitor').filter(action_id=i_l.action_id).exists():
                            a=User_action.objects.using('monitor').create(
                                action_id = i_l.action_id,
                                agent_user = Engagement_agent_user.objects.using('monitor').filter(order_id=i_l.agent_user.order_id).first(),
                                user_detail = user_detail.objects.using('monitor').filter(username=i_l.user_detail.username).first(),
                                like = i_l.like,
                                comment = i_l.comment,
                                share = i_l.share,
                                follow = i_l.follow,
                                action_type = i_l.action_type
                            )
                    LOGGER.info(f"{a}'s action created at Online storage")

        if  User_action.objects.using('monitor').all().count() > User_action_local.objects.all().count() :
            for i_a in User_action.objects.using('monitor').all():
                if not User_action_local.objects.filter(action_id=i_a.action_id).exists():
                    if i_a.action_type == "RANDOM":
                        a=User_action_local.objects.create(
                            action_id = i_a.action_id,
                            # agent_user = Engagement_agent_user_local.objects.filter(order_id=i_a.agent_user.order_id).first(),
                            user_detail = user_detail_local.objects.filter(username=i_a.user_detail.username).first(),
                            like = i_a.like,
                            comment = i_a.comment,
                            share = i_a.share,
                            follow = i_a.follow,
                            action_type = i_a.action_type
                        )
                    elif i_a.action_type == "ENGAGEMENT":
                        a=User_action_local.objects.create(
                            action_id = i_a.action_id,
                            agent_user = Engagement_agent_user_local.objects.filter(order_id=i_a.agent_user.order_id).first(),
                            user_detail = user_detail_local.objects.filter(username=i_a.user_detail.username).first(),
                            like = i_a.like,
                            comment = i_a.comment,
                            share = i_a.share,
                            follow = i_a.follow,
                            action_type = i_a.action_type)
                    LOGGER.info(f"{a}'s {i_a.action_type} action created at local storage")