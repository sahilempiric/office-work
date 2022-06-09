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


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-n')
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
        accounts_created = 0
        print('dsafuihdsyefg')
        # user_cred_list = list(user_cred.objects.all())
        user_cred_list = list(user_detail.objects.filter(updated = False))
        print(user_cred_list,'user_cred_list')
        if required_accounts > len(user_cred_list) :
            random_user_for_login = i 
            print("\n\n **** you can't change in more profile than you have in your DATABASE **** \n\n")
            return
        for i in user_cred_list:

            if i.id<240:
                print(i.id)
                continue
            for ia in range(3):
                # fix the error
                # psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "twbot_useravd_port_key"
                # DETAIL:  Key (port)=(5794) already exists.
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
                country, city = CyberGhostVpn.get_random_usa_server()
                LOGGER.debug(f'country: {country}, City: {city}')
                try:
                    # create an avd user, at the same time, creat the relative AVD
                    # before deleting this avd user, first deleting the relative AVD
                    LOGGER.debug('Start to creating AVD user')

                    # if the country is USA, then create timezone for AVD
                    if 'united states' in country.lower():
                        user_avd = UserAvd.objects.create(
                            # user=User.objects.all().first(),
                            name=avd_name,
                            port=port,
                            proxy_type="CYBERGHOST",
                            country=country,
                            timezone=random.choice(US_TIMEZONE),
                        )
                    else:
                        user_avd = UserAvd.objects.create(
                            # user=User.objects.all().first(),
                            name=avd_name,
                            port=port,
                            proxy_type="CYBERGHOST",
                            country=country
                        )

                    LOGGER.debug(f'AVD USER: {user_avd}')

                    tb = TwitterBot(user_avd.name)

                    # Connect vpn
                    if not self.no_vpn:
                        time.sleep(10)
                        if not tb.connect_to_vpn(country=country, city=city):
                            raise Exception("Couldn't able to connect Nord VPN")
                    else:
                        tb.check_apk_installation()
                    # username = 'jasonlam71'
                    # password = 'Jason@9780'

                    url = "https://source.unsplash.com/random"
                    file_name = os.path.join(BASE_DIR,'prof_img/profile_pic.jpg')
                    

                    profile_img_download(url,file_name)
                    profile_pic_path = os.path.join(os.getcwd(), file_name)
                    LOGGER.info(f"profile image path : {profile_pic_path}")

                    run_cmd(f'adb push {profile_pic_path} /sdcard/Download')
                    tb.start_file_manager()

                    time.sleep(4)
                    
                    username = random_user_for_login.username
                    password = random_user_for_login.password
                    # scussess_login_bool = tb.login_account(username,password)
                    # user_name,user_bio = user_bio_genrator()
                    # success_updated_user_prof = tb.user_profile_main(user_name,user_bio)
                    success_updated_user_prof = True
                    # insta_login = tb.login_account(username,password)
                    insta_login = True
                    if insta_login == True:
                        print(insta_login,'insta_login'*3)
                        # success_updated_user_prof = tb.user_profile_main(user_name,user_bio)

                        if success_updated_user_prof:
                            time.sleep(10)
                            accounts_created += 1
                            random_user_for_login.updated = True
                            random_user_for_login.save()
                            user_cred_list.remove(random_user_for_login)
                            break
                        else:
                            print(success_updated_user_prof)
                            continue
                    else:
                        print(insta_login,'insta_login'*3)


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

        required_accounts = int(options.get('n'))

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

        # random_sleep(10, 30)

    def clean_bot(self, tb, is_sleep=True):
        LOGGER.debug('Quit app driver and kill bot processes')
        #  tb.app_driver.quit()
        tb.kill_bot_process(appium=False, emulators=True)
        # if is_sleep:
            # random_sleep(60, 80)

def user_bio_genrator():

    user_name = 'users name'
    user_bio = "this will be the bio"
    return user_name,user_bio

def profile_img_download(url, file_name):
    '''
    downloading the file and saving it
    '''
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)

        return file