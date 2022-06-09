import sys
import time
from concurrent import futures

import numpy as np
from django.core.management.base import BaseCommand

from conf import US_TIMEZONE, PARALLEL_NUMER
from core.models import User
# from core.models import User
from exceptions import PhoneRegisteredException, CannotRegisterThisPhoneNumberException, GetSmsCodeNotEnoughBalance
from instagram.actions.follow import *
from instagram.bot import *
from instagram.models import Engagement_agent_user_local, Engagement_local, Inactive_accounts_local, User_action_local




class Command(BaseCommand):
    def add_arguments(self, parser):
        # parser.add_argument('-n')
        parser.add_argument('-m', '--run_times', type=int, default=0,
                            help='After the run times, the bot will exit(0 means no effect)')
        parser.add_argument(
            "--no_vpn",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help="Whether to use VPN or not, if it presents, don't use VPN.",
        )
        parser.add_argument(
            '--parallel_number',
            nargs='?',
            default=PARALLEL_NUMER,
            type=int,
            help=(f'Number of parallel running. Default: {PARALLEL_NUMER}'
                  '(PARALLEL_NUMER in the file conf.py)')
        )

    def run_tasks(self, required_accounts):
        print(1)
        user_agent_name = os.getenv('AGENT_USER', '')
        TOTAL_LIKES = int(os.getenv('TOTAL_LIKES', ''))
        TOTAL_COMMENTS = int(os.getenv('TOTAL_COMMENTS', ''))
        TOTAL_SHARE = int(os.getenv('TOTAL_SHARE', ''))
        TOTAL_FOLLOW = int(os.getenv('TOTAL_FOLLOW', ''))
        complete_task = 0
        total_task = 0
        print(2)
        ac = [TOTAL_LIKES,TOTAL_COMMENTS,TOTAL_SHARE,TOTAL_FOLLOW ]
        for i_ac in ac:
            i_ac = int(i_ac)
            if i_ac > total_task:
                total_task = i_ac



        if not Engagement_agent_user_local.objects.filter(agent_user = user_agent_name,completed = False).exists():
            agent_user = Engagement_agent_user_local.objects.create(
                agent_user = user_agent_name,
                total_likes = TOTAL_LIKES,
                total_shares = TOTAL_SHARE,
                total_comments = TOTAL_COMMENTS,
                total_follow = TOTAL_FOLLOW
                )
        print(3)
        if Engagement_agent_user_local.objects.filter(agent_user = user_agent_name,completed = False).exists():
            agent_user = Engagement_agent_user_local.objects.filter(agent_user = user_agent_name,completed = False)
        # agent_user.total_likes = TOTAL_LIKES
        # agent_user.total_comments = TOTAL_COMMENTS
        # agent_user.total_shares = TOTAL_SHARE
        # agent_user.total_follow = TOTAL_FOLLOW
        print(agent_user,'----')
        # agent_user.save()
        accounts_created = 0
        print(4)
        liked_on_post = agent_user.liked
        print(liked_on_post)
        commented_on_post = agent_user.commented
        shared_on_post = agent_user.shared
        followed_on_post = agent_user.followed
        print(5,'----')
        
        if (commented_on_post >= agent_user.total_comments) and (liked_on_post >= agent_user.total_likes)  and (shared_on_post >= agent_user.total_shares) and (followed_on_post >= agent_user.total_follow):
            agent_user.completed = True
            agent_user.save()

            agent_user = Engagement_agent_user_local.objects.create(
                agent_user = user_agent_name,
                total_likes = TOTAL_LIKES,
                total_shares = TOTAL_SHARE,
                total_comments = TOTAL_COMMENTS,
                total_follow = TOTAL_FOLLOW
                )
        count = 0
        accounts_created = 0
        print(required_accounts,accounts_created)
        if accounts_created < required_accounts:
            print('yes')
        else:print('noo','-----------------')
        # while accounts_created < required_accounts:
            # print('sajdhfgdtygafvdsuayvgdsuak')
        print(f'\n\n \t\t****{accounts_created}****\t\t \n\n')
        while True:
        # while accounts_created < required_accounts:
            # fix the error
            # psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "twbot_useravd_port_key"
            # DETAIL:  Key (port)=(5794) already exists.
            print(1)
            ports = list(
                filter(
                    lambda y: not UserAvd.objects.filter(port=y).exists(),
                    map(
                        lambda x: 5550 + x, range(1, 500)
                    )
                )
            )
            devices = list(
                filter(
                    lambda y: not UserAvd.objects.filter(name=y).exists(),
                    map(
                        lambda x: f"android_{x}", range(1, 500)
                    )
                )
            )
            start_time = time.time()
            avd_name = random.choice(devices)
            port = random.choice(ports)
            print(2)
            # create all accounts in USA
            # country, city = CyberGhostVpn.get_random_usa_server('Hong Kong')
            country= 'Hong Kong'
            city = ''
            LOGGER.debug(f'country: {country}')
            agent_user,a = Engagement_agent_user.objects.using('monitor').get_or_create(agent_user = user_agent_name,completed = False)
            agent_user.total_likes = TOTAL_LIKES
            agent_user.total_comments = TOTAL_COMMENTS
            agent_user.total_shares = TOTAL_SHARE
            agent_user.total_follow = TOTAL_FOLLOW
            agent_user.save()

            sharing_bool = False
            commenting_bool = False
            commented_on_post = agent_user.liked
            shared_on_post = agent_user.shared
            if commented_on_post <= TOTAL_COMMENTS:
                commenting_bool= True
            if shared_on_post <= TOTAL_SHARE:
                sharing_bool = True
            try:
                # create an avd user, at the same time, creat the relative AVD
                # before deleting this avd user, first deleting the relative AVD
                LOGGER.debug('Start to creating AVD user')
                print(3)
                # if the country is USA, then create timezone for AVD
                if 'united states' in country.lower():
                    user_avd = UserAvd.objects.create(
                        user=User.objects.all().first(),
                        name=avd_name,
                        port=port,
                        proxy_type="CYBERGHOST",
                        country=country,
                        timezone=random.choice(US_TIMEZONE),
                    )
                else:
                    user_avd = UserAvd.objects.create(
                        user=User.objects.all().first(),
                        name=avd_name,
                        port=port,
                        proxy_type="CYBERGHOST",
                        country=country
                    )

                LOGGER.debug(f'AVD USER: {user_avd}')
                print(user_avd.name,'-------------------')
                tb = TwitterBot(user_avd.name,user_avd)

                # Connect vpn
                if not self.no_vpn:
                    time.sleep(10)
                    if not tb.connect_to_vpn(country=country):
                        raise Exception("Couldn't able to connect Nord VPN")
                else:
                    tb.check_apk_installation()
                tb.check_apk_installation()
                user_ = tb.create_account()


                for ip in range(4):
                    pic_prs = tb.start_file_manager()
                    if pic_prs:
                        break  
                insta_random = False
                random_action_count = [0,0,0,0]
                random_count = 0

                if user_ :
                    i_user = user_.username
                    insta_random,random_action_count = tb.random_actions()

                suceess_searched_user_bool = False
                if insta_random:
                    random_count += 1
                    suceess_searched_user_bool = tb.search_user(str(user_agent_name))

                

                
                target_process = False
                action_list = []
                if suceess_searched_user_bool:
                    target_process,action_list = tb.follow_like_comment_share_atonce(commenting=commenting_bool,sharing=sharing_bool)

                success_updated_user_prof = False
                if target_process:
                    success_updated_user_prof = tb.user_profile_main()
                    random_sleep(9,10)
                
                if success_updated_user_prof:
                    user_ = user_detail.objects.using('monitor').get(username=i_user)
                    user_.random_action += random_count
                    user_.updated = success_updated_user_prof
                    user_.save()

                if type(random_action_count) == list:
                                    
                    like,comment_x,share,follow = random_action_count
                    print(like,comment_x,share,follow,'like,comment_x,share,follow')
                    user_action_1 = None
                    random_user_for_login = user_detail.objects.using('monitor').filter(username=i_user,updated = False,status = 'ACTIVE').order_by('?').first()
                    from core.models import User_action
                    User_action.objects.using('monitor').create(
                        user_detail = random_user_for_login,

                        like = like if like != None else 0, 
                        comment = comment_x if comment_x != None else 0,
                        share = share if share != None else 0,
                        follow = follow if follow != None else 0,
                        action_type = 'RANDOM'
                    )
                
                if target_process:
                    from core.models import Engagement_agent_user,Engagement
                    
                    likes,comments,shares,follows = action_list
                    User_action.objects.using('monitor').create(
                                agent_user = agent_user,
                                user_detail = random_user_for_login,
                                like = likes,
                                comment = comments,
                                share = shares,
                                follow = follows,
                                action_type = 'ENGAGEMENT'
                                )
                                
                    Engagement.objects.using('monitor').get_or_create(
                                agent_user = agent_user,
                                avdsname = user_avd.name,
                                username = random_user_for_login.username,
                                # engagement_user = self.f_username,
                                user_detail = random_user_for_login,
                                liked = likes,
                                commented =comments,
                                shared = shares,
                                followed = follows
                            )

                    agent_user.liked += likes
                    agent_user.shared += shares
                    agent_user.commented +=  comments
                    agent_user.followed += follows
                    agent_user.save()
                    
                    
                time.sleep(30)


                # accounts_created += 1

            except GetSmsCodeNotEnoughBalance as e:
                LOGGER.debug('Not enough balance in GetSMSCode')
                tb.kill_bot_process(True, True)
                sys.exit(1)
            except Exception as e:
                print(traceback.format_exc())
                try:
                    tb.kill_bot_process(True, True)
                    user_avd.delete() if user_avd else None
                except:
                    pass
            finally:
                if self.run_times != 0:
                    count += 1
                    if count >= self.run_times:
                        LOGGER.info(f'Real run times: {count}, now exit')
                        break

                if 'tb' in locals() or 'tb' in globals():
                    LOGGER.info(f'Clean the bot: {user_avd.name}')
                    self.clean_bot(tb, False)
                else:
                    name = user_avd.name
                    port = ''
                    parallel.stop_avd(name=name, port=port)

    def handle(self, *args, **options):
        self.total_accounts_created = 0
        self.avd_pack = []
        if UserAvd.objects.all().count() >= 500:
            return "Cannot create more than 500 AVDs please delete existing to create a new one."
        required_accounts = 1
        # required_accounts = int(options.get('n'))

        self.no_vpn = options.get('no_vpn')
        self.parallel_number = options.get('parallel_number')

        self.run_times = options.get('run_times')
        LOGGER.debug(f'Run times: {self.run_times}')
        requied_account_list = [n.size for n in
                                np.array_split(np.array(range(required_accounts)), self.parallel_number)]
        with futures.ThreadPoolExecutor(max_workers=self.parallel_number) as executor:
            for i in range(self.parallel_number):
                executor.submit(self.run_tasks, requied_account_list[i])
        print(f" All created UserAvd and TwitterAccount ****\n")
        print(self.avd_pack)
        for x, y in self.avd_pack:
            uavd = UserAvd.objects.filter(id=x)
                # tw_ac = TwitterAccount.objects.filter(id=y)
                # if uavd and tw_ac:
                #     UserAvd.objects.filter(id=x).update(twitter_account_id=y)

        random_sleep(10, 30)

    def clean_bot(self, tb, is_sleep=True):
        LOGGER.debug('Quit app driver and kill bot processes')
        #  tb.app_driver.quit()
        tb.kill_bot_process(appium=False, emulators=True)
        if is_sleep:
            random_sleep(6, 8)
