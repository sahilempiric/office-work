from cgi import print_directory
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from telethon import TelegramClient
from home.management.commands.functions_file.function_msg import engagement, engagement_msg_id
from home.models import user_details
from main import LOGGER
import random, os

reaction_list = ["❤️","👍","🔥"]
definer_ = '''XANA has sold out its first metaverse avatar wearable NFTs by Hiroko Koshino, the world-renowned designer.

XANA produced 10 looks and 29 items from the 2022 Spring/Summer collection by Hiroko Koshino, a top international fashion designer, into 3D wearables for XANA avatars. 

The limited edition of 500 NFT sold out in just 45 minutes upon sale.

Through this project, XANA has fully demonstrated to the market the potential of the new "digital fashion" field, a fusion of the fashion industry and the Metaverse.

XANA will continue to actively collaborate with the world's top brands and outstanding independent designers to bring new business opportunities to the fashion industry.'''
# definer_ = '''XANA has sold out its first metaverse avatar wearable NFTs by Hiroko Koshino, the world-renowned designer.**

# XANA produced 10 looks and 29 items from the 2022 Spring/Summer collection by Hiroko Koshino, a top international fashion designer, into 3D wearables for XANA avatars'''
class Command(BaseCommand):
    help = 'For engagement'
    def handle(self, *args, **kwargs):

        all_active_user = user_details.objects.filter(status="ACTIVE").order_by('?')
        # ENGAGEMENT_COUNT = 100
        # AGENT_USER = 'xanaofficial'
        # AGENT_USER = 'xana_1234'

        # for get the message id
        # test_user = all_active_user[0]

        AGENT_USER = str(os.getenv('AGENT_USER',''))
        ENGAGEMENT_COUNT = int(os.getenv('ENGAGEMENT_COUNT',''))
        active_user_count = user_details.objects.filter(status="ACTIVE").count()
        if active_user_count < ENGAGEMENT_COUNT:
            ENGAGEMENT_COUNT = active_user_count
            LOGGER.error(f'There is not sufficient user in Database and there are only {active_user_count}, Thus only these user will do the engagement')
        # if user_details.objects.filter(status="")


        
        message_id = engagement_msg_id(groupname=AGENT_USER)
        print(AGENT_USER,ENGAGEMENT_COUNT)
        print(message_id,'---1')


        if message_id:
            for i in range(ENGAGEMENT_COUNT):
                user = all_active_user[i]
                engagement(random_=2,groupname=AGENT_USER,Message_id=message_id,number=user.number,apiid=user.api_id,apihash=user.api_hash)

        else:
            LOGGER.info('We could not find the message of which we are looking for to do engagement.')
        
        ...