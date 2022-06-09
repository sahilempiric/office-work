import time
import subprocess
# from uuid import uuid4

from django.db import models
from accounts_conf import PCS
from constants import COUNTRIES
from urllib3.packages.six import u
from django.db.models import JSONField
from django.db.models.enums import Choices
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.signals import post_save, pre_delete

class instagram_report_test(models.Model):
    
    system = models.CharField(max_length=255,choices=PCS,blank=True,null=True)
    total_Account = models.IntegerField()
    total_eligible_for_engagement_account = models.IntegerField()
    total_active_accounts = models.IntegerField()
    total_issued_accounts_in_login = models.IntegerField()
    total_updated_accounts = models.IntegerField()
    total_random_action = models.IntegerField()
    total_accounts_under_warm_up = models.IntegerField()
    total_likes = models.IntegerField()
    total_comments = models.IntegerField()
    total_share = models.IntegerField()
    total_follow = models.IntegerField()
    total_action = models.IntegerField()
    total_accounts_created_in_last_24hours = models.IntegerField()
    total_new_eligible_accounts_in_login_in_last_24hours = models.IntegerField()
    total_issued_accounts_in_login_in_last_24hours = models.IntegerField()
    total_accounts_updated_in_last_24hours = models.IntegerField()
    total_random_action_performed_in_24hours = models.IntegerField()
    # total_account_used_in_last_24hour = models.IntegerField()
    total_accounts_added_under_warm_upin_last_24hours = models.IntegerField()
    total_likes_in_last_24hours = models.IntegerField()
    total_comments_in_last_24hours = models.IntegerField()
    total_share_in_last_24hours = models.IntegerField()
    total_follow_in_last_24hours = models.IntegerField()
    total_action_performed_in_last_24hours = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.system
    


class user_detail(models.Model):
    STATUS = (
        ("ACTIVE", "ACTIVE"),
        ("LOGIN_ISSUE","LOGIN_ISSUE")
    )
    avdsname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    number = models.BigIntegerField(null=False)
    password = models.CharField(max_length=255)
    birth_date = models.CharField(max_length=255)
    birth_month = models.CharField(max_length=255)
    birth_year = models.CharField(max_length=255)
    updated = models.BooleanField(default=False)
    random_action = models.IntegerField(default=0)
    status = models.CharField(max_length=255,choices=STATUS,default='ACTIVE')
    following = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    can_search = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    # created_at = models.DateTimeField( blank=True, null=True)
    # updated_at = models.DateTimeField(blank=True,null=True)

    def __str__(self) -> str:
        return self.username


class Engagement_agent_user(models.Model):
    import uuid

    order_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False,null=True,blank=True)
    agent_user = models.CharField(max_length=255,blank=True,null=True)
    total_likes = models.IntegerField(blank=True,null=True)
    total_shares = models.IntegerField(blank=True,null=True)
    total_comments = models.IntegerField(blank=True,null=True)
    total_follow = models.IntegerField(blank=True,null=True)
    liked = models.IntegerField(default=0)
    commented = models.IntegerField(default=0)
    followed = models.IntegerField(default=0)
    shared = models.IntegerField(default=0) 
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self) -> str:
        return f'{self.agent_user} - {self.completed}'

class Engagement(models.Model):
    """
    To confirm that one user will not use for the same engagement
    """
    avdsname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    agent_user = models.ForeignKey(Engagement_agent_user,on_delete=models.CASCADE)
    user_detail = models.ForeignKey(user_detail,on_delete=models.CASCADE)
    liked = models.IntegerField(default=0)
    commented = models.IntegerField(default=0)
    shared = models.IntegerField(default=0)
    followed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self) -> str:
        return f'{self.user_detail}'

class Inactive_accounts(models.Model):
    user_detail = models.ForeignKey(user_detail,on_delete=models.CASCADE)
    updated = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self) -> str:
        return f'{self.user_detail} '


class User_action(models.Model):
    ACTION = (
        ("RANDOM", "RANDOM"),
        ("ENGAGEMENT", "ENGAGEMENT"),
        ("NOT_DEFINED", "NOT_DEFINED"),
    )
    import uuid
    action_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False,null=True,blank=True)
    agent_user = models.ForeignKey(Engagement_agent_user,on_delete=models.CASCADE,null=True,blank=True)
    user_detail = models.ForeignKey(user_detail,on_delete=models.CASCADE)
    like = models.IntegerField()
    comment = models.IntegerField()
    share = models.IntegerField()
    follow = models.IntegerField()
    action_type = models.CharField(max_length=255, choices=ACTION, default="NOT_DEFINED")
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self) -> str:
        return f'{self.user_detail} '

class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """Helps Django work with our custom user model."""

    def create_user(self, email, username=None, password=None):
        """Creates a new user profile object."""

        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            username = email
        if not password:
            raise ValueError("Users must have an password.")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        """Creates and saves a new superuser with given details."""

        user = self.create_user(email, username, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampModel):
    """To Store user basic information"""

    LANGUAGE_CHOICES = (
        ("en-us", "English"),
        ("ja", "Japanese"),
        ("ko", "Korean"),
        ("zh_CN", "Chinese"),
    )

    USER_TYPES = (
        ("marketing_team", "marketing_team"),
        ("tester", "tester"),
        ("user", "user"),
    )

    APP_CHOICES = (
        ("IG", "IG"),  # Instagram
        ("TT", "TT"),  # TikTok
        ("YT", "YT"),  # YouTube
        ("TW", "TW"),  # Twitter
        ("TL", "TL"),  # Telegram
    )

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email_verified = models.BooleanField(default=False)
    app_choice = models.CharField(max_length=200, choices=APP_CHOICES, default="IG")
    user_type = models.CharField(max_length=200, choices=USER_TYPES, default="user")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    timezone = models.CharField(max_length=100, blank=True, null=True, default=None)
    user_language = models.CharField(
        default="en-us", choices=LANGUAGE_CHOICES, max_length=15
    )
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "email",
    ]

    def __str__(self):
        return self.username


class EmailOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    generated_otp = models.CharField(max_length=6, default="000000")

    def __str__(self):
        return str(self.user.username) + "_" + str(self.generated_otp)


class EngageTask(TimeStampModel):
    STASUES = (
        ("PENDING", "PENDING"),
        ("FAILED", "FAILED"),
        ("DONE", "DONE"),
        ("RUNNING", "RUNNING")
    )

    PCS = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
        ("11", "11"),
        ("12", "12"),
        ("13", "13"),
        ("14", "14"),
        ("15", "15"),
        ("16", "16"),
        ("17", "17"),
        ("18", "18"),
        ("19", "19"),
        ("20", "20"),
        ("21", "21"),
        ("22", "22"),
        ("23", "23"),
        ("24", "24"),
        ("25", "25")
    )

    target_name = models.CharField(max_length=300)
    tweet_id = models.CharField(max_length=300, blank=True, null=True)
    status = models.CharField(max_length=200, choices=STASUES, default="PENDING")
    system_no = models.CharField(max_length=3, choices=PCS, blank=True, null=True)

    def __str__(self):
        return f"{self.tweet_id} | {self.target_name} | {self.created} | {self.status}"
