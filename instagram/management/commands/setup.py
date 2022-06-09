"""Setup for this bot system"""

from django.core.management.base import BaseCommand

from main import LOGGER
from instagram.utils import update_pc_task
from utils import run_cmd
from instagram.models import ActionType, ShareActionType


def insert_initial_data_for_action_type():
    #  ActionType.objects.all().delete()
    for pair in ActionType.ACTION_TYPE:
        ActionType.objects.get_or_create(id=pair[0], text=pair[1])

def insert_initial_data_for_action_type_for_remote_db():
    #  ActionType.objects.all().delete()
    for pair in ShareActionType.ACTION_TYPE:
        ShareActionType.objects.using('monitor').get_or_create(
                id=pair[0], text=pair[1])


class Command(BaseCommand):
    def __init__(self):
        super().__init__()

    def add_arguments(self, parser):
        parser.add_argument(
            '-d', '--database',
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help='Setup for database')
        parser.add_argument(
            '-r', '--remote_database',
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help='Setup for remote database')

    def handle(self, *args, **options):
        #  update_pc_task("Project setup")
        db = options.get('database')
        remote_db = options.get('remote_database')

        if db:
            LOGGER.info('Database setup')
            core_models = ('python manage.py makemigrations --noinput core;'
                           'python manage.py migrate --noinput core')
            twbot_models = ('python manage.py makemigrations --noinput instagram;'
                            'python manage.py migrate --noinput instagram')

            all_models = ('python manage.py makemigrations --noinput;'
                          ' python manage.py migrate --noinput')

            run_cmd(twbot_models)
            run_cmd(core_models)
            run_cmd(all_models)

            # LOGGER.info('Insert initial data for twitter action type')
            # insert_initial_data_for_action_type()

        if remote_db:
            LOGGER.info('Insert initial data for twitter action type for remote db')
            insert_initial_data_for_action_type_for_remote_db()
