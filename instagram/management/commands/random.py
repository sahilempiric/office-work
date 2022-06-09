import sys
import time
from concurrent import futures

import numpy as np
from django.core.management.base import BaseCommand

from conf import US_TIMEZONE, PARALLEL_NUMER
# from core.models import User
from exceptions import PhoneRegisteredException, CannotRegisterThisPhoneNumberException, GetSmsCodeNotEnoughBalance
from instagram.actions.follow import *
from instagram.bot import *
from instagram.models import Engagement_agent_user_local, Engagement_local, Inactive_accounts_local, User_action_local
from instagram.utils import COMMENTS_
from dotenv import load_dotenv	
from core.models import Engagement,Engagement_agent_user,Inactive_accounts, User,User_action
load_dotenv()
class Command(BaseCommand):
    def add_arguments(self, parser):
        # parser.add_argument('-n')
        # parser.add_argument('username', type=str, help="username")
        # parser.add_argument('comment_number', type=int, help='comment_number')
        # parser.add_argument('share_number', type=int, help='share_number')
        # parser.add_argument('username', type=str, help="username")
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
        count = 0
        user_cred_list = list(user_detail_local.objects.filter(updated=True,status='ACTIVE').order_by('?'))
        
        user_agent_name = os.getenv('AGENT_USER', '')
        TOTAL_LIKES = int(os.getenv('TOTAL_LIKES', ''))
        TOTAL_COMMENTS = int(os.getenv('TOTAL_COMMENTS', ''))
        TOTAL_SHARE = int(os.getenv('TOTAL_SHARE', ''))
        TOTAL_FOLLOW = int(os.getenv('TOTAL_FOLLOW', ''))
        complete_task = 0
        total_task = 0

        ac = [TOTAL_LIKES,TOTAL_COMMENTS,TOTAL_SHARE,TOTAL_FOLLOW ]
        for i_ac in ac:
            i_ac = int(i_ac)
            if i_ac > total_task:
                total_task = i_ac
        
        # if total_task > len(user_cred_list) :
        #     print("\n\n **** you Dont have enough user for engagement in your DATABASE **** \n\n")
        #     return

        # agent_user,a = Engagement_agent_user_local.objects.get_or_create(agent_user = user_agent_name,completed = False)
        # agent_user.total_likes = TOTAL_LIKES
        # agent_user.total_comments = TOTAL_COMMENTS
        
        # agent_user.total_shares = TOTAL_SHARE
        # agent_user.total_follow = TOTAL_FOLLOW
        # agent_user.save()
        # accounts_created = 0
        # liked_on_post = agent_user.liked
        # commented_on_post = agent_user.commented
        # shared_on_post = agent_user.shared
        # followed_on_post = agent_user.followed
        # all_engaged_data = Engagement_local.objects.filter()

        print(complete_task ,total_task,'complete_task < total_task')
        while True:
            if not Engagement_agent_user_local.objects.filter(agent_user = user_agent_name,completed = False).exists():
                agent_user = Engagement_agent_user_local.objects.create(
                    agent_user = user_agent_name,
                    total_likes = TOTAL_LIKES,
                    total_shares = TOTAL_SHARE,
                    total_comments = TOTAL_COMMENTS,
                    total_follow = TOTAL_FOLLOW
                    )
            if Engagement_agent_user_local.objects.filter(agent_user = user_agent_name,completed = False).exists():
                agent_user = Engagement_agent_user_local.objects.filter(agent_user = user_agent_name,completed = False).first()
                # and (liked_on_post >= agent_user.total_likes)  and (shared_on_post >= agent_user.total_shares) and (followed_on_post >= agent_user.total_follow)
            # agent_user,a = agent_user
            print(agent_user)
            # if (commented_on_post >= agent_user.total_comments) :
            #     print('------------')
            #     pass
                # agent_user.completed = True
                # agent_user.save()
            print('--------------')        
            if not Engagement_agent_user_local.objects.filter(agent_user = user_agent_name,completed = False).exists():
                agent_user = Engagement_agent_user_local.objects.create(
                    agent_user = user_agent_name,
                    total_likes = TOTAL_LIKES,
                    total_shares = TOTAL_SHARE,
                    total_comments = TOTAL_COMMENTS,
                    total_follow = TOTAL_FOLLOW
                    )
            liked_on_post = agent_user.liked
            commented_on_post = agent_user.commented
            shared_on_post = agent_user.shared
            followed_on_post = agent_user.followed
            random_user_for_login = list(user_detail_local.objects.filter(updated=True,status='ACTIVE').order_by('?'))[0]
            print(random_user_for_login,'========================')
            try:
                print(complete_task,'complete_task1')
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
                print(complete_task,'complete_task2')
                start_time = time.time()
                avd_name = random.choice(devices)
                port = random.choice(ports)
                # create all accounts in USA
                country = 'Hong Kong'
                LOGGER.debug(f'country: {country}')
                try:
                    # create an avd user, at the same time, creat the relative AVD
                    # before deleting this avd user, first deleting the relative AVD
                    LOGGER.debug('Start to creating AVD user')
                    print(complete_task,'complete_task3')
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
                    print(complete_task,'complete_task4')
                    LOGGER.debug(f'AVD USER: {user_avd}')

                    tb = TwitterBot(user_avd.name)

                    # Connect vpn
                    if not self.no_vpn:
                        time.sleep(10)
                        if not tb.connect_to_vpn(country=country):
                            raise Exception("Couldn't able to connect Nord VPN")
                    else:
                        tb.check_apk_installation()
                    print(complete_task,'complete_task5')
                    print(random_user_for_login)
                    username = random_user_for_login.username
                    password = random_user_for_login.password
                    comment_a = random.choice( COMMENTS_)
                    insta_login = True
                    insta_login,login_issue = tb.login_account(username,password)

                    if login_issue == False:
                        Inactive_accounts_local.objects.create(
                            user_detail = random_user_for_login,
                            updated = random_user_for_login.updated
                        )
                        random_user_for_login.status = 'LOGIN_ISSUE'
                        random_user_for_login.save()
                    print(complete_task,'complete_task6')
                    if insta_login and login_issue == True :
                        self.Create = False
                        # if self.Random == True:
                        insta_random,random_action_count = tb.random_actions()
                        if insta_random:
                            self.Random = False
                    # if insta_random != 0:
                            random_user_for_login.random_action += 1
                            random_user_for_login.save()

                        if type(random_action_count) == list:
                            like,comment_x,share,follow = random_action_count
                            print(like,comment_x,share,follow,'like,comment_x,share,follow')
                            user_action_1 = None
                            try:
                                # random_user_for_login = user_detail_local.objects.filter(username=i_user)
                                user_action_1 = User_action_local.objects.create(
                                    user_detail = random_user_for_login,

                                    like = like , 
                                    comment = comment_x ,
                                    share = share ,
                                    follow = follow if follow != None else 0,
                                    action_type = 'RANDOM'
                                )
                                print(user_action_1,'user_action_1user_action_1')
                            except Exception as e:print(e)


                    else:
                        print(complete_task,'complete_task10')
                        random_user_for_login.status = 'LOGIN_ISSUE'
                        random_user_for_login.save()
                        LOGGER.info(f'Got an issue on account Login, "user_id" : {random_user_for_login.username}')
                    # if login_issue == False:break
                    random_sleep(10,15)
                except GetSmsCodeNotEnoughBalance as e:
                    print(complete_task,'complete_task11')
                    print(complete_task,'complete_task11')
                    LOGGER.debug('Not enough balance in GetSMSCode')
                    tb.kill_bot_process(True, True)
                    sys.exit(1)
                except Exception as e:
                    print(complete_task,'complete_task12')
                    print(traceback.format_exc())
                    try:
                        tb.kill_bot_process(True, True)
                        user_avd.delete() if user_avd else None
                    except:
                        pass
                finally:
                    print(complete_task,'complete_task13')
                    if self.run_times != 0:
                        count += 1
                        if count >= self.run_times:
                            LOGGER.info(f'Real run times: {count}, now exit')
                            
                    print(complete_task,'complete_task14')

                    if 'tb' in locals() or 'tb' in globals():
                        LOGGER.info(f'Clean the bot: {user_avd.name}')
                        self.clean_bot(tb, False)
                    else:
                        name = user_avd.name
                        port = ''
                        parallel.stop_avd(name=name, port=port)
            except Exception as e:
                print(e)
                print(complete_task,'complete_task15')
            # finally:
                # print(complete_task,'complete_task16')
                # account_count +=1 
                # accounts_created += 1
                # user_cred_list.remove(random_user_for_login)


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
