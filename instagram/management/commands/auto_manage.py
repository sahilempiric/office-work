import tempfile

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from conf import PARALLEL_NUMER
from instagram.models import *
from conf import *
from main import LOGGER
from surviral_avd.settings import BASE_DIR, SYSTEM_NO
from instagram.report import get_target_names_standard_and_nonstandard_for_one_day
from instagram.utils import random_sleep
from utils import run_cmd


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--parallel_number',
            nargs='?',
            default=PARALLEL_NUMER,
            type=int,
            help=(f'Number of parallel running. Default: {PARALLEL_NUMER}'
                  '(PARALLEL_NUMER in the file conf.py)')
        )
        parser.add_argument(
            "--post_report",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help="Post the report to webhook if True",
        )
        parser.add_argument(
            "--run_auto_engage_only",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help="Run auto_engage only, for test",
        )
        parser.add_argument(
            "--run_random_cron_time_only",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help="Run random_cron_time_for_auto_manage only, for test",
        )
        parser.add_argument(
            "--run_check_git_pull_only",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help="Run check_or_add_git_pull_cmd only, for test",
        )
        parser.add_argument(
            '--venv_activate_path',
            nargs='?',
            default=f'{BASE_DIR}/env/bin/activate',
            help=('The path of "bin/activate" for python virtual environment. '
                  f'Default: {BASE_DIR}/env/bin/activate'),
        )
        parser.add_argument(
            "--no_vpn",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help="Whether to use VPN or not, if it presents, don't use VPN.",
        )

    def generate_yesterday_report(self):
        # Generating yesterday's engagement report
        try:
            LOGGER.debug("Generating engagement report")
            yesterday = datetime.today().date() - timedelta(days=1)
            date = f"{yesterday.year}-{yesterday.month}-{yesterday.day}"
            shell_cmd = f". {self.venv_activate_path} && {BASE_DIR}/manage.py generate_report --date {date} "
            if self.post_report:
                shell_cmd += "--post_report"
            subprocess.run(shell_cmd, check=True, shell=True)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            LOGGER.debug(e)
    
    def delete_avds_for_suspended_accounts(self):
        # Deleting suspended accounts and AVD's
        try:
            LOGGER.debug("Deleting AVD's od suspended accounts")
            suspended_avds = UserAvd.objects.filter(Q(twitter_account__status="SUSPENDED") | Q(twitter_account=None))
            LOGGER.debug(f"Deleting suspended AVD's: {suspended_avds}")
            suspended_avds.delete()
            shell_cmd = f". {self.venv_activate_path} && {BASE_DIR}/manage.py delete_avds"
            subprocess.run(shell_cmd, check=True, shell=True)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            LOGGER.debug(e)

    def create_accounts_if_not_enough(self):
        # Create new accounts if existing accounts are not enough
        try:
            active_accounts = TwitterAccount.objects.filter(status="ACTIVE")
            print(f"Active accounts: {active_accounts.count()}")
            if active_accounts.count() < MAX_ACTIVE_ACCOUNTS * 0.7:
                LOGGER.debug(f"Active accounts are less than 70% of required accounts so running account creation")
                accounts_to_create = min(MAX_ACCOUNTS_CREATION_PER_DAY, MAX_ACTIVE_ACCOUNTS - active_accounts.count())
                print(f"Accounts creating today {accounts_to_create}")
                shell_cmd = f". {self.venv_activate_path} && {BASE_DIR}/manage.py create_accounts " \
                            f"-n {accounts_to_create} --parallel_number {self.parallel_number}"
                subprocess.run(shell_cmd, check=True, shell=True)
            else:
                LOGGER.debug("Active accounts more than 70% of required accounts so skipping account creation")
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            LOGGER.debug(e)

    def update_required_profile(self):
        # Profile update if required
        try:
            profile_not_updated_accounts = TwitterAccount.objects.filter(profile_updated=False).exclude(
                status="SUSPENDED")
            if profile_not_updated_accounts:
                LOGGER.debug("Profile update is pending so running profile update")
                shell_cmd = f". {self.venv_activate_path} && {BASE_DIR}/manage.py update_profile " \
                            f"--parallel_number {self.parallel_number}"
                subprocess.run(shell_cmd, check=True, shell=True)
            else:
                LOGGER.debug("Profile update is not pending so skipping profile update")
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            LOGGER.debug(e)

    def inspect_accounts(self):
        # Inspecting accounts
        try:
           LOGGER.debug("Inspecting Accounts")
           shell_cmd = f". {self.venv_activate_path} && {BASE_DIR}/manage.py inspect"
           subprocess.run(shell_cmd, check=True, shell=True)
        except KeyboardInterrupt as e:
           raise e
        except Exception as e:
           LOGGER.debug(e)

    def run_check_jobs(self):
        # Running Check Jobs command
        LOGGER.debug("Running auto_engage")
        shell_cmd = f". {self.venv_activate_path} && {BASE_DIR}/manage.py check_jobs " \
                    f"--parallel_number {self.parallel_number}"
        subprocess.run(shell_cmd, check=True, shell=True)

    def run_auto_engage_one_time(self, target_names):
        try:
            if self.no_vpn:
                shell_cmd = f". {self.venv_activate_path} && {BASE_DIR}/manage.py auto_engage --must_like " \
                            f"--must_follow --must_retweet  --latest_post_number 3 --comment_number 1 " \
                            f"--target_names {target_names} --parallel_number {self.parallel_number}"\
                            f" --no_vpn"
            else:
                shell_cmd = f". {self.venv_activate_path} && {BASE_DIR}/manage.py auto_engage --must_like " \
                            f"--must_follow --must_retweet  --latest_post_number 3 --comment_number 1 " \
                            f"--target_names {target_names} --parallel_number {self.parallel_number}"
            LOGGER.info(f'Run the command: {shell_cmd}')
            subprocess.run(shell_cmd, check=True, shell=True)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            LOGGER.debug(e)

    def run_auto_engage_one_day(self, min_interval=1800, max_interval=3600):
        # if the count of active accounts is less than half of MAX_ACTIVE_ACCOUNTS
        # then just run auto_engage one time.
        run_one_time = False
        if (TwitterAccount.objects.filter(status='ACTIVE').count()
                < MAX_ACTIVE_ACCOUNTS / 2):
            LOGGER.info(f'The count of active accounts is less than half of'
                    ' {MAX_ACTIVE_ACCOUNTS}, then just run auto_engage one time')
            run_one_time = True

        today = timezone.now().date()
        times = 0
        while True:
            times += 1
            LOGGER.info(f'Times to try to run auto_engage: {times}')
            if times > 1 and run_one_time:
                break

            (nonstandard_target_names, standard_target_names) = (
                    get_target_names_standard_and_nonstandard_for_one_day())
            if nonstandard_target_names:
                # sleep the time between half hour and one hour before next running
                # don't sleep at first running
                if times > 1:
                    random_sleep(min_interval, max_interval)

                LOGGER.info(f'Run auto_engage with the target names: '
                        f'{nonstandard_target_names}')
                next_target_names = ' '.join(nonstandard_target_names)
                self.run_auto_engage_one_time(next_target_names)
            else:
                LOGGER.info('All actions of all target users reached the quotas')
                break

    def run_auto_engage(self):
        self.run_auto_engage_one_day()

    def random_cron_time_for_auto_manage(self):
        LOGGER.info('Create random time in crontab for auto_engage')
        cmd = 'auto_manage'
        cmds = 'crontab -l'
        verbose = True
        result = run_cmd(cmds, verbose=verbose)
        if result:
            (returncode, output) = result
            #  LOGGER.info(output)
            outs = output.strip().split('\n')
            outs_all = [e + '\n' for e in outs]
            effective_outs = [
                e + '\n' for e in outs if not e.strip().startswith('#')]
            if 'no crontab for' in output:
                #  outs_all = ['\n']
                outs_all = []
                effective_outs = []
            exist_flag = False
            exist_job = ''
            for item in effective_outs:
                if cmd in item:
                    LOGGER.info(f'There has already been one job for command {cmd}')
                    exist_flag = True
                    exist_job = item
                    break

            if exist_flag:
                LOGGER.info(f'Override the existing job: {exist_job}')
                outs_all.remove(exist_job)
                exist_job_parts = exist_job.strip().split()
                m = random.randint(0, 59)

                if exist_job_parts[1] != '*':
                    original_hour = int(exist_job_parts[1])
                else:
                    original_hour = random.randint(0, 23)
                next_hour = (original_hour + 8) % 24
                h =  (next_hour + random.randint(0, 4)) % 24

                exist_job_parts[0] = f'{m}'
                exist_job_parts[1] = f'{h}'
                new_job = ' '.join(exist_job_parts) + '\n'
                LOGGER.info(f'New crontab job: {new_job}')

                outs_all.append(new_job)
                jobs_text = ''.join(outs_all)
                LOGGER.debug(jobs_text)
                with tempfile.NamedTemporaryFile(mode='w+t') as fp:
                    #  LOGGER.debug(f'jobs_text: {jobs_text}')
                    LOGGER.debug(f'Write jobs to file {fp.name}')
                    fp.write(jobs_text)
                    fp.flush()
                    # import crontab job
                    cmds = f'crontab {fp.name}'
                    verbose = True
                    result = run_cmd(cmds, verbose=verbose)
                    if result:
                        (returncode, output) = result
                        if returncode == 0:
                            LOGGER.info('Imported jobs into crontab')
                        else:
                            LOGGER.info('Failed to importe jobs into crontab')
                    else:
                        LOGGER.info('Cannot importe jobs into crontab')
                #  LOGGER.debug(new_output)
            else:
                LOGGER.info(f'Cannot get crontab job for auto_manage')
        else:
            LOGGER.error('Cannot get crontab jobs')

    def check_or_add_git_pull_cmd(self):
        run_cmd('cd home/workspace')
        # cmd = 'git pull origin $(git rev-parse --abbrev-ref HEAD)'
        cmd = 'git pull "https://github.com/Riken00/Telegram.git"'
        auto_manage_sh = TASKS_DIR / 'auto_manage.sh'
        lines = auto_manage_sh.open().readlines()
        
        flag = False
        position = None
        for line in lines:
            if 'git pull' in line:
                flag = True
            if 'bin/activate' in line:
                position = lines.index(line)

        if flag:
            LOGGER.debug('git pull in the file auto_manage.sh, then do nothing')
            return
        run_cmd('git init')
        if position:
            lines.insert(position + 1, cmd + '\n')
        else:
            lines.insert(len(lines), cmd + '\n')
        auto_manage_sh.open('w').writelines(lines)
        LOGGER.debug('Wrote the command git pull into file auto_manage.sh')

    def handle(self, *args, **kwargs):
        self.parallel_number = kwargs.get('parallel_number')
        self.post_report = kwargs.get("post_report")
        self.run_auto_engage_only = kwargs.get("run_auto_engage_only")
        self.venv_activate_path = kwargs.get("venv_activate_path")
        self.no_vpn = kwargs.get("no_vpn")
        self.run_random_cron_time_only = kwargs.get("run_random_cron_time_only")
        self.run_check_git_pull_only = kwargs.get("run_check_git_pull_only")

        funcs = [
            self.random_cron_time_for_auto_manage,
            self.check_or_add_git_pull_cmd,

            self.generate_yesterday_report,
            #  self.delete_avds_for_suspended_accounts,
            #  self.create_accounts_if_not_enough,
            self.update_required_profile,
            self.run_auto_engage,
        ]

        if self.run_auto_engage_only:
            funcs = [self.run_auto_engage]

        if self.run_random_cron_time_only:
            funcs = [self.random_cron_time_for_auto_manage]

        if self.run_check_git_pull_only:
            funcs = [self.check_or_add_git_pull_cmd]

        for f in funcs:
            LOGGER.debug(f'Run: {f.__name__}')
            f()
            LOGGER.debug(f'Runing is done: {f.__name__}')
# generate_password?