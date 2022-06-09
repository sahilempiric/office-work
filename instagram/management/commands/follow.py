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
        from django.utils import timezone
        import datetime
        elegible_time = datetime.datetime.now() - datetime.timedelta(days=7)
        elegible_time = timezone.utc.localize(elegible_time)
        elegible_time24 = datetime.datetime.now() - datetime.timedelta(days=8)
        elegible_time24 = timezone.utc.localize(elegible_time24)
        count = 0
        # user_cred_list = list(user_detail_local.objects.filter(updated=True,status='ACTIVE',following__lt = 100 ))
        # user_cred_list = list(user_detail_local.objects.filter(status='ACTIVE',following__lt = 100 ).order_by('?'))
        user_cred_list = list(user_detail.objects.using('monitor').filter(status="ACTIVE",updated=True,created_at__lte = elegible_time).order_by('?'))

        
        

        for user_cred in user_cred_list:
            

            try:
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
                try:
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

                    tb = TwitterBot(user_avd.name)

                    tb.check_apk_installation()
                    if not self.no_vpn:
                        time.sleep(10)
                        if not tb.connect_to_vpn(country=country):
                            raise Exception("Couldn't able to connect Nord VPN")
                    # else:
                    #     tb.check_apk_installation()

                    user_login,sucess_login = tb.login_account(username=user_cred.username,password=user_cred.password)

                    if sucess_login:
                        tb.deny_permission1(deny_count=True)
                        followed_user = 0
                        follow_loop = 100 - user_cred.following
                        print(f'\n\n{follow_loop}\n\n')
                        follow_user_li = user_detail.objects.using('monitor').filter(status="ACTIVE",updated=True,created_at__lte = elegible_time).order_by('?')
                        for i in range(follow_loop):
                            for i1 in range(3):
                                follow_user = follow_user_li[i]
                                
                                if follow_user.username == user_cred.username:
                                    continue    

                                searched_user = False
                                # follow_user = user_detail_local.objects.filter(updated = True,status = 'ACTIVE', followers__lt = 100).order_by('?').first()
                                for i in range(3):
                                    
                                    search_user = tb.search_user(username=follow_user.username)
                                    print(search_user,'search_usersearch_user')
                                    if search_user:
                                        break
                                # if not searched_user:
                                    follow_user.can_search = bool(search_user)
                                    follow_user.save()
                                    print(f'\n\n{follow_user.can_search} : follow_user.can_search\n\n')
                                following = False
                                if search_user:
                                    following = tb.follow_to_follow()
                                print(following,'followingfollowing')
                                if search_user:
                                    following = tb.follow_to_follow()
                                # if following:
                                #     if following == 'Follow':
                                    follow_user.followers = int(following)
                                    follow_user.save()
                                    if following < 0:
                                        user_cred.following += 1
                                        user_cred.save()
                                    print(f'\n\n{follow_user.followers}follow_user.followers\n\n')
                                    print(f'\n\n{user_cred.following}user_cred.following\n\n')
                                    break


                        followed_user += 1
                    else:
                        user_cred.status = "LOGIN_ISSUE"
                        user_cred.save()


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
                            

                    if 'tb' in locals() or 'tb' in globals():
                        LOGGER.info(f'Clean the bot: {user_avd.name}')
                        self.clean_bot(tb, False)
                    else:
                        name = user_avd.name
                        port = ''
                        parallel.stop_avd(name=name, port=port)
            except Exception as e:
                print(e)


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
