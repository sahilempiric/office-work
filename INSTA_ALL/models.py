from django.db import models
from django.db.models.fields import CharField
import os

# Create your models here.

PURCHASE = (
    ('0', 'NOT PURCHASED'),
    ('1', 'PURCHASE'),
)

REFFERED = (
    ('0', 'NOT REFFERED'),
    ('1', 'REFFERED'),
)

ACTIVE_STATUS = (
    ('0', 'NOT ACTIVE'),
    ('1', 'ACTIVE'),
)

STATUS = (
    ('0','ACTIVE'),
    ('1','DEACTIVE')
)

COIN_STATUS = (
    ('0','ACTIVE'),
    ('1','DEACTIVE'),
)

ORDER_TYPE = (
    ('0','LIKE'),
    ('1','FOLLOW'),
)

FROM_APP = (
    ('0','WEB'),
    ('1','APP'),
)

ORDER_STATUS = (
    ('0','DEACTIVE'),
    ('1','ACTIVE'),
)

PYMENT_METHOD = (
    ('0', 'PAYPAL'),
    ('1', 'RAZORPAY'),
)

POPULAR_STATUS = (
    ('0', 'NOT POPULAR'),
    ('1', 'POPULAR'),
)

class users(models.Model): 
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True,unique=True)
    user_id = models.CharField(primary_key=True, max_length=255, null=False, default="",unique=True)
    parent_id = models.CharField(max_length=255, null=False, default=0)
    ftoken = models.TextField(max_length=255, null=True)
    ip = models.CharField(max_length=255,null=True)
    username = models.CharField(max_length=255, null=False, default="")
    profile_picture = models.CharField(max_length=255, null=True)
    total_coins = models.CharField(max_length=255, null=True)
    referral_code = models.CharField(max_length=255, null=True, unique=True)
    is_purchase = models.CharField(choices=PURCHASE, max_length=1, null=True, default=0)
    is_referred = models.CharField(choices=REFFERED, max_length=1, null=True, default=0)
    fromapp = models.CharField(max_length=1, choices=FROM_APP, null=True, default=1)
    status = models.CharField(choices=ACTIVE_STATUS, max_length=1, null=False, default=1)
    remember_token = CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class orders(models.Model):
    type = models.CharField(max_length=1,choices=ORDER_TYPE,null=False)
    user = models.ForeignKey(users,on_delete=models.CASCADE,related_name='order_user_id')
    custom_user_id = models.TextField(null=False)
    username = models.TextField(null=True)
    post_id = models.CharField(max_length=255,null=True,default=0)
    short_code = models.CharField(max_length=255,null=True)
    needed = models.CharField(max_length=255,null=False)
    recieved = models.CharField(max_length=255,null=False,default=0)
    image_url = models.TextField(null=False)
    no_like_log = models.CharField(max_length=255,null=False,default=0)
    reason_for_cancelorder = models.CharField(max_length=255,null=True)
    fromapp = models.CharField(max_length=1,choices=FROM_APP,null=True,default=1)
    order_status = models.CharField(max_length=1,choices=ORDER_STATUS,null=False,default=1)
    deleted_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_time = models.DateTimeField(auto_now=True, null=True, blank=True)


class already_like_follow(models.Model):
    type = models.CharField(max_length=255, null=False, default="")
    user = models.ForeignKey(users,on_delete=models.CASCADE,related_name='al_user_id')
    custom_user_id = models.CharField(max_length=255, null=False)
    post_id = models.CharField(max_length=255, null=True, default=0)
    al_user_id = models.TextField(null=False)
    deleted_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class purchase_coins(models.Model):
    user = models.ForeignKey(users,on_delete=models.CASCADE,related_name='purchase_user_id')
    payment_id = models.TextField(null=True,unique=True)
    purchased_coin = models.IntegerField(null=True)
    amount = models.IntegerField(null=True)
    payment_state = models.TextField(null=True)
    payment_time = models.TextField(null=True)
    country_code = models.TextField(null=True)
    payment_method = models.CharField(choices=PYMENT_METHOD,default=1, max_length=1)
    transaction_id = models.TextField(null=True,unique=True)
    deleted_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class user_orders(models.Model):
    user =  models.ForeignKey(users,on_delete=models.CASCADE,related_name='uorders_user_id')
    packageName =  models.CharField(max_length=255,default="", null=False)
    acknowledgementState =  models.CharField(max_length=255,default="", null=False)
    orderId =  models.CharField(max_length=255,default="", null=False, unique=True)
    productId =  models.CharField(max_length=255,default="", null=False)
    token =  models.CharField(max_length=255,null=True)
    developerPayload =  models.CharField(max_length=255,default="", null=False)
    purchaseTime =  models.CharField(max_length=255,default="", null=False)
    purchaseState =  models.CharField(max_length=255,default="", null=False)
    purchaseToken = models.TextField(default="", null=False,  unique=True)
    inapp =  models.CharField(max_length=255,null=True)
    username =  models.CharField(max_length=255,null=True)
    code =  models.CharField(max_length=255,null=True)
    two_factor_identifier =  models.CharField(max_length=255,null=True)
    regionCode =  models.CharField(max_length=255,null=True)
    deleted_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


    
class app_data(models.Model):
    access_token = models.TextField(null=True)
    earn_like_coin = models.CharField(max_length=255,default="", null=False)
    spent_like_coin = models.CharField(max_length=255,default="", null=False)
    earn_follow_coin = models.CharField(max_length=255,default="", null=False)
    spent_follow_coin = models.CharField(max_length=255,default="", null=False)
    referrel_coin = models.CharField(max_length=255,default="", null=False)
    default_coin = models.CharField(max_length=255,default="", null=False)
    from_add_coin = models.IntegerField(null=True)
    maintenence_mode = models.CharField(max_length=200, blank=True, null=True,default='')
    update_mode = models.CharField(max_length=255,default="", null=False)
    update_url = models.CharField(max_length=255,default="", null=False)
    payment_method = models.CharField(max_length=255,default="", null=False)
    game_id = models.CharField(max_length=255,default="", null=False)
    banner_id = models.CharField(max_length=255,default="", null=False)
    initial_id = models.CharField(max_length=255,default="", null=False)
    maintenence_message = models.CharField(max_length=255,default="", null=False)
    notification_title = models.CharField(max_length=255,default="", null=False)
    notification_message = models.CharField(max_length=255,default="", null=False)
    notification_show = models.CharField(max_length=255,default="", null=False)
    update_message = models.CharField(max_length=255,default="", null=False)
    playstore_version = models.CharField(max_length=255,default="", null=False)
    web = models.CharField(max_length=255,default="", null=False)
    website = models.CharField(max_length=255,default="", null=False)
    user_agent = models.CharField(max_length=255,default="", null=False)
    use_second_user_agent = models.CharField(max_length=255,default=1, null=False)
    second_user_agent = models.CharField(max_length=255, null=True)
    share_url = models.CharField(max_length=255,default="", null=False)
    offer = models.CharField(max_length=10, default="", null=False)
    offer_percentage = models.CharField(max_length=255,default="", null=False)
    offer_starttime = models.CharField(max_length=255,default="", null=False)
    offer_endtime = models.CharField(max_length=255,default="", null=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    offer_discount_title = models.CharField(max_length=255,default="", null=False)
    updated_at = models.DateTimeField(null=True, blank=True)
    offer_discount_text = models.CharField(max_length=255,default="", null=False)
    offer_discount_image = models.CharField(max_length=255,default="")
    web_login = models.CharField(max_length=255,default="", null=False)
    email = models.EmailField(null=False, default="")
    privacy_policy = models.CharField(max_length=255,default="", null=False)
    facebook = models.CharField(max_length=255,default="", null=False)
    instagram = models.CharField(max_length=255,default="", null=False)
    twitter = models.CharField(max_length=255, default="", null=True)
    telegram = models.CharField(max_length=255, default="", null=True)
    rate_dialog = models.CharField(max_length=255,default="", null=False)
    share_dialog = models.CharField(max_length=255,default="", null=False)


class coin_details(models.Model):
    quantity = models.IntegerField(null=False)
    indian_rate = models.CharField(null=False,max_length=255)
    other_rate = models.TextField(null=False)
    notes = models.TextField(null=False)
    is_popular = models.CharField(max_length=1, choices=POPULAR_STATUS, null=False, default=0)
    coin_status = models.CharField(max_length=1, choices=COIN_STATUS, null=False, default=0)
    deleted_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class check_ip_addresses(models.Model):
    ip = models.CharField(max_length=255,null=False , unique=True)
    status = models.CharField(choices=STATUS,default=1, max_length=1, null=False)
    deleted_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
