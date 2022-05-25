from django.db import models
import random, subprocess

from home.conf import AVD_DEVICES,AVD_PACKAGES
from utils import LOGGER
# Create your models here.

class user_details(models.Model):
    emulator = models.CharField(max_length=255)
    number = models.IntegerField()
    api_id = models.CharField(max_length=255)
    api_hash = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    def __str__(self) :
        return str(self.number)

class User_avds(models.Model):
    avdname = models.CharField(max_length=255)
    port = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=True,null=True,blank=True)


    def __str__(self) -> str:
        return str(f'{self.avdname} : {self.port}')


from django.db.models.signals import post_save, pre_delete

def create_better_avd(sender, instance, **kwargs):
    created = kwargs.get('created')

    if created:
        LOGGER.info('Start to create AVD')
        try:
            from home.bot import Telegram_bot
            telegram_bot = Telegram_bot(instance.avdname, start_appium=False, start_adb=False)

            device = random.choice(AVD_DEVICES)  # get a random device
            package = random.choice(AVD_PACKAGES)  # get a random package
            telegram_bot.create_avd(avd_name=instance.avdname, package=package,
                             device=device)

            LOGGER.info(f"**** AVD created with name: {instance.avdname} and port: {instance.port} ****")

        except Exception as e:
            instance.delete()
            LOGGER.error(f"Couldn't create avd due to the following error \n")
            LOGGER.error(e)
            print('Start to create AVD')


def delete_avd(sender, instance, **kwargs):
    try:
        cmd = f'avdmanager delete avd --name {instance.name}'
        p = subprocess.Popen([cmd], stdin=subprocess.PIPE, shell=True, stdout=subprocess.DEVNULL)
    except Exception as e:
        pass

post_save.connect(create_better_avd, sender=User_avds)
pre_delete.connect(delete_avd, sender=User_avds)