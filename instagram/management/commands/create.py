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
                        lambda x: f"instagram_{x}", range(1, 500)
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
                create_acc_bool = tb.create_account()
                if create_acc_bool:
                    accounts_created += 1
                time.sleep(30)


                # accounts_created += 1

            except GetSmsCodeNotEnoughBalance as e:
                LOGGER.debug('Not enough balance in GetSMSCode')
                # tb.kill_bot_process(True, True)
                sys.exit(1)
            except Exception as e:
                LOGGER.error(e)
                print(traceback.format_exc())
                
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
                user_avd.delete()

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
