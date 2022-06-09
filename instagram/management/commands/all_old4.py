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




            try:
                print(f'\n\n\n{self.continue_process}\n\n\n')
                country = 'Hong Kong'
                if self.continue_process:
                    user_avd = self.avd_(country=country)
                    self.avd_name_ = user_avd.name
                    self.Connect_vpn = True
                    self.Create = True
                    self.Random = True
                    self.Ontarget = True
                    self.Engagement = True
                    self.Profile = True
                    self.Process = False
                    self.continue_process = True


                tb = TwitterBot(self.avd_name_)

                # tb.check_apk_installation()
                # Connect vpn
                if not self.no_vpn:
                    if self.Connect_vpn:
                        time.sleep(10)
                        if not tb.connect_to_vpn(country=country):
                            raise Exception("Couldn't able to connect Nord VPN")
                        else:
                            self.Connect_vpn = False
                    # else:
                    #     tb.check_apk_installation()
                        # tb.check_apk_installation()
                    
                try:

                    # for ip in range(4):
                    #     pic_prs = tb.start_file_manager()
                    #     if pic_prs:
                    #         break  
                    random_action_count = []
                    new_user = ''
                    insta_random,random_action_count  = False,[0,0,0,0]
                    if self.Create :
                        new_user = True
                        # new_user = tb.create_account()
                    if new_user :
                        self.Create = False
                        if self.Random == True:
                            insta_random,random_action_count = 1,[0,0,0,0]
                            # insta_random,random_action_count = tb.random_actions()
                            if insta_random:
                                self.Random = False
                    # if insta_random != 0:
                            # new_user.random_action += 1
                            # new_user.save()

                        # uncomment

                        # if type(random_action_count) == list:
                        #     like,comment_x,share,follow = random_action_count
                        #     print(like,comment_x,share,follow,'like,comment_x,share,follow')
                        #     user_action_1 = None
                        #     try:
                        #         # random_user_for_login = user_detail_local.objects.filter(username=i_user)
                        #         user_action_1 = User_action_local.objects.create(
                        #             user_detail = new_user,

                        #             like = like , 
                        #             comment = comment_x ,
                        #             share = share ,
                        #             follow = follow if follow != None else 0,
                        #             action_type = 'RANDOM'
                        #         )
                        #         print(user_action_1,'user_action_1user_action_1')
                        #     except Exception as e:print(e)
                                
                    if self.Engagement:
                        suceess_searched_user_bool = True
                        # suceess_searched_user_bool = tb.search_user(str(user_agent_name))
                        if suceess_searched_user_bool:
                            like_bool = False
                            sharing_bool = False
                            commenting_bool = False
                            follow_bool = False
                            # if 
                            if liked_on_post < TOTAL_LIKES:
                                like_bool= True
                            if followed_on_post < TOTAL_FOLLOW:
                                follow_bool= True
                            if commented_on_post < TOTAL_COMMENTS:
                                commenting_bool= True
                            if shared_on_post < TOTAL_SHARE:
                                sharing_bool = True
                            target_process,action_list = True,[0,0,0,0]
                            # target_process,action_list = tb.follow_like_comment_share_atonce(likes_b = like_bool,commenting=commenting_bool,sharing=sharing_bool,following = follow_bool)
                            if target_process:
                                self.Engagement = False
                            time.sleep(10)
                            likes,comments,shares,follows = action_list
                            commented_on_post+=1 if comments != 0 else 0
                            liked_on_post +=1 if likes !=0 else 0
                            shared_on_post+=1 if shares !=0 else 0
                            followed_on_post+=1 if follows !=0 else 0
                            print(complete_task,'complete_task7')

                            # uncomment

                            # if (likes or comments or share or follow) > 0:
                            #     print(complete_task,'complete_task8')
                            #     complete_task+=1
                            #     User_action_local.objects.create(
                            #     agent_user = agent_user,
                            #     user_detail = new_user,
                            #     like = likes,
                            #     comment = comments,
                            #     share = shares,
                            #     follow = follows,
                            #     action_type = 'ENGAGEMENT'
                            #     )


                            #     Engagement_local.objects.get_or_create(
                            #     agent_user = agent_user,
                            #     avdsname = user_avd.name,
                                # username = new_user.username,
                            #     # engagement_user = self.f_username,
                            #     user_detail = new_user,
                            #     liked = likes,
                            #     commented =comments,
                            #     shared = shares,
                            #     followed = follows
                            # )

                            # agent_user.avdsname = avd_name

                            # uncomment

                            # agent_user.liked += likes
                            # agent_user.shared += shares
                            # agent_user.commented +=  comments
                            # agent_user.followed += follows

                            # if (commented_on_post >= agent_user.total_comments) and (liked_on_post >= agent_user.total_likes)  and (shared_on_post >= agent_user.total_shares) and (followed_on_post >= agent_user.total_follow):
                            #     agent_user.completed = True
                            # total_task += 1
                            # agent_user.save()

                    success_updated_user_prof = ''
                    if self.Profile:
                        success_updated_user_prof = True
                        # success_updated_user_prof = tb.user_profile_main()
                        if success_updated_user_prof:
                            self.Profile = False
                            self.Process = True
                        print(f'\n\n{success_updated_user_prof} updating Bool\n\n')
                        # new_user.updated = success_updated_user_prof
                        # new_user.save()

                        print(complete_task,'complete_task9')
                        # random_sleep(10,15)
                        if self.Process == True:
                            self.continue_process = True
                        else:
                            self.continue_process = False
                except GetSmsCodeNotEnoughBalance as e:
                    print(complete_task,'complete_task11')
                    print(complete_task,'complete_task11')
                    LOGGER.debug('Not enough balance in GetSMSCode')
                    tb.kill_bot_process(True, True)
                    sys.exit(1)
                except Exception as e:
                    self.continue_process = False
                    self.Process = False

                    tb = TwitterBot(self.avd_name_)
                    print(tb)
                    print(complete_task,'complete_task12')
                    print(traceback.format_exc())
                    # try:
                    #     tb.kill_bot_process(True, True)
                    #     user_avd.delete() if user_avd else None
                    # except:
                    #     pass
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
                    tb.kill_bot_process()

                    if self.Process == True:
                        self.continue_process = True
                    else:
                        self.continue_process = False
                        # tb.check_apk_installation()
            except Exception as e:
                print(e)
                print(complete_task,'complete_task15')
            # finally:
                # print(complete_task,'complete_task16')
                # account_count +=1 
                # accounts_created += 1
                # user_cred_list.remove(new_user)


    def handle(self, *args, **options):
        self.Connect_vpn = True
        self.Create = True
        self.Random = True
        self.Ontarget = True
        self.Engagement = True
        self.Profile = True
        self.Process = False
        self.continue_process = True


        self.avd_name_ = ''
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


    def avd_(self,country='Hong kong'):
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
        # create all accounts in USA
        country = 'Hong Kong'
        LOGGER.debug(f'country: {country}')
        # create an avd user, at the same time, creat the relative AVD
        # before deleting this avd user, first deleting the relative AVD
        LOGGER.debug('Start to creating AVD user')
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

        return user_avd