from django.core.management.base import BaseCommand
import subprocess
from instagram.models import user_detail_local


class Command(BaseCommand):
    # def add_arguments(self, parser):
    def handle(self, *args, **options):
        all_inactive_avds= [ user.avdsname for user in user_detail_local.objects.filter(status='LOGIN_ISSUE')]
        all_avds= [ user.avdsname for user in user_detail_local.objects.all()]
        # print(all_inactive_avds)
        avd_list = subprocess.check_output(['emulator', '-list-avds'])
        avd_list = [avd for avd in avd_list.decode().split("\n") if avd]
        print(avd_list)


        for avd in avd_list:
            if (avd in all_inactive_avds) or (not avd in all_avds):
                # if avd.startswith('instagram'):
                    print(f"AVD {avd} not there in data base so deleting")
                    try:
                        subprocess.check_output(['avdmanager', 'delete', 'avd', '-n', avd])
                    except:
                        pass
        # for user in all_users:



        