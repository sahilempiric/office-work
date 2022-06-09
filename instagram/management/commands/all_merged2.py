from collections import UserDict
import sys
import time
from concurrent import futures

import numpy as np
from django.core.management.base import BaseCommand
from torch import rand

from conf import US_TIMEZONE, PARALLEL_NUMER
from core.models import User
# from core.models import User
from exceptions import PhoneRegisteredException, CannotRegisterThisPhoneNumberException, GetSmsCodeNotEnoughBalance
from instagram.actions.follow import *
# from instagram.bot import *
from core.models import Inactive_accounts,User_action,user_detail
from instagram.models import Inactive_accounts_local, User, User_action_local,UserAvd, user_detail_local
from django.utils import timezone
import datetime
elegible_time = datetime.datetime.now() - datetime.timedelta(days=7)
elegible_time = timezone.utc.localize(elegible_time)
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

    def run_tasks(self):
        
        count = 0
        print(33)
        accounts_created = 0
        print(elegible_time,'==========')
        user_cred_list=list(user_detail.objects.using('monitor').filter(created_at__gte=elegible_time,status="ACTIVE"))

        print(user_cred_list)
        # required_accounts = len(user_cred_list)
        # print(user_cred_list,'user_cred_listuser_cred_list')
        account_count = 0
        for i_user in range(len(user_cred_list)):
            random_user_for_login = list(user_detail.objects.using('monitor').filter(created_at__gte=elegible_time,status="ACTIVE").order_by('?'))[0]
            try:
                for i in range(3):
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
                                lambda x: f"instagram_{x}", range(1, 500)
                            )
                        )
                    )
                    start_time = time.time()
                    avd_name = random.choice(devices)
                    port = random.choice(ports)
                    country= 'Hong Kong'
                    city = ''
                    LOGGER.debug(f'country: {country}, City: {city}')
                    try:
                        LOGGER.debug('Start to creating AVD user')
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
                        from instagram.bot import TwitterBot
                        tb = TwitterBot(user_avd.name)
                        tb.check_apk_installation()
                        for ip in range(4):
                            pic_prs = tb.start_file_manager()
                            if pic_prs:
                                break   
                        if not self.no_vpn:
                            time.sleep(10)
                            if not tb.connect_to_vpn(country=country):
                                raise Exception("Couldn't able to connect Nord VPN")
                        else:
                            tb.check_apk_installation()
                        user_name,user_bio = user_bio_genrator()
                        username = str(random_user_for_login.username)
                        password = random_user_for_login.password
                        insta_login = True
                        insta_login,login_issue = tb.login_account(username,password)

                        if login_issue == False:
                            Inactive_accounts_local.objects.create(
                                user_detail = random_user_for_login,
                                updated = random_user_for_login.updated
                            )
                            # random_user_for_login = user_detail_local.objects.filter(username=i_user)
                            LOGGER.info(random_user_for_login,4)
                            random_user_for_login.status = 'LOGIN_ISSUE'
                            random_user_for_login.save()
                            continue

                        if insta_login == True and login_issue == True:
                            insta_random,random_action_count = tb.random_actions(username)
                            random_user_for_login = user_detail.objects.using('monitor').filter(username = username).first()
                            random_user_for_login.random_action += 1
                            random_user_for_login.save()
                            if type(random_action_count) == list:
                                    
                                like,comment_x,share,follow = random_action_count
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
                                except Exception as e:print(e)
                                

                            if True:
                                
        
                                tb.deny_permission1(deny_count=True)
                                followed_user = 0
                                follow_loop = 100 - random_user_for_login.following
                                follow_user_li = user_detail.objects.using('monitor').filter(status="ACTIVE",updated=True,created_at__lte = elegible_time).order_by('?')
                                for i in range(follow_loop):
                                    for i1 in range(3):
                                        follow_user = follow_user_li[i]
                                        if follow_user.username == random_user_for_login.username:continue 

                                        for i in range(3):
                                            search_user = tb.search_user(username=follow_user.username)
                                            if search_user:
                                                break
                                            follow_user.can_search = bool(search_user)
                                            follow_user.save()
                                        following = False
                                        if search_user:
                                            following = int(tb.follow_to_follow())
                                        # if following:
                                        #     if following == 'Follow':
                                            if following != False:
                                                follow_user.followers = int(following)
                                                follow_user.save()
                                                if int(following) < 0:
                                                    random_user_for_login.following += 1
                                                    random_user_for_login.save()
                                            # print(f'\n\n{follow_user.followers}follow_user.followers\n\n')
                                            # print(f'\n\n{random_user_for_login.following}user_cred.following\n\n')
                                            break


                            success_updated_user_prof = tb.user_profile_main()
                            # time.sleep(10)  
                            random_sleep(9,10)
                            # random_count = 0
                            # if success_updated_user_prof:
                            # random_count += 1 if insta_random != False else 0
                            # random_user_for_login = user_detail_local.objects.filter(username=i_user)
                            # LOGGER.info(random_user_for_login,1)
                            # if insta_random != 0:
                                # random_user_for_login.random_action += insta_random
                            random_user_for_login.updated = success_updated_user_prof
                            random_user_for_login.save()
                            if success_updated_user_prof or insta_random:break
                        else:
                            random_user_for_login.status = "LOGIN_ISSUE"
                            random_user_for_login.save()
                            # LOGGER.info(f'Got an issue on account Login, "user_id" : {random_user_for_login.username}')
                        if login_issue == False:break
                    except GetSmsCodeNotEnoughBalance as e:
                        LOGGER.debug('Not enough balance in GetSMSCode')
                        # tb.kill_bot_process(True, True)
                        sys.exit(1)
                    except Exception as e:
                        print(traceback.format_exc())
                    finally:
                        try:
                            tb.kill_bot_process(True, True)
                            user_avd.delete() if user_avd else None
                        except:
                            pass
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
                            import parallel
                            parallel.stop_avd(name=name, port=port)


            except Exception as e:None
            finally:
                    accounts_created += 1
                    account_count += 1
                    user_cred_list.remove(random_user_for_login)

    def handle(self, *args, **options):
        self.total_accounts_created = 0
        self.avd_pack = []
        if UserAvd.objects.all().count() >= 500:
            return "Cannot create more than 500 AVDs please delete existing to create a new one."

        required_accounts = 1

        self.no_vpn = options.get('no_vpn')
        self.parallel_number = options.get('parallel_number')
        self.run_times = options.get('run_times')
        LOGGER.debug(f'Run times: {self.run_times}')
        requied_account_list = [n.size for n in
                                np.array_split(np.array(range(required_accounts)), self.parallel_number)]
        with futures.ThreadPoolExecutor(max_workers=self.parallel_number) as executor:
            for i in range(self.parallel_number):
                # print(22)
                executor.submit(self.run_tasks)
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
        tb.kill_bot_process(appium=False, emulators=True)
        if is_sleep:
            random_sleep(6, 8)
def profile_img_download(url, file_name):
    '''
    downloading the file and saving it
    '''
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)

        return file


def user_bio_genrator():

    user_name = 'users name'
    user_bio = "this will be the bio"
    return user_name,user_bio