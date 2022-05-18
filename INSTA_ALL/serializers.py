from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import app_data,coin_details, orders,users,purchase_coins


class coin_data_serializer(serializers.ModelSerializer):
    class Meta:
        model = coin_details
        fields = ['quantity','indian_rate','other_rate','notes','is_popular']

class app_data_serializer(serializers.ModelSerializer):
    # coin_detail = coin_data_serializer(many=True,read_only=True)
    class Meta:
        model = app_data
        fields =  ['earn_like_coin', 'spent_like_coin', 'earn_follow_coin', 'spent_follow_coin', 'referrel_coin', 'default_coin', 'maintenence_mode', 'playstore_version', 'update_mode', 'update_url', 'payment_method', 'game_id', 'banner_id', 'initial_id', 'maintenence_message', 'notification_title', 'notification_message', 'notification_show', 'update_message', 'user_agent', 'share_url', 'web', 'website', 'offer', 'offer_percentage', 'offer_starttime', 'offer_endtime', 'offer_discount_text', 'offer_discount_image', 'web_login', 'email', 'privacy_policy', 'facebook', 'instagram', 'twitter', 'telegram', 'rate_dialog', 'share_dialog']
        # ,'coin_detail']

class app_dataaccess_serializer(serializers.ModelSerializer):
    # coin_detail = coin_data_serializer(many=True,read_only=True)
    class Meta:
        model = app_data
        fields =  ['access_token','earn_like_coin', 'spent_like_coin', 'earn_follow_coin', 'spent_follow_coin', 'referrel_coin', 'default_coin', 'maintenence_mode', 'playstore_version', 'update_mode', 'update_url', 'payment_method', 'game_id', 'banner_id', 'initial_id', 'maintenence_message', 'notification_title', 'notification_message', 'notification_show', 'update_message', 'user_agent', 'share_url', 'web', 'website', 'offer', 'offer_percentage', 'offer_starttime', 'offer_endtime', 'offer_discount_text', 'offer_discount_image', 'web_login', 'email', 'privacy_policy', 'facebook', 'instagram', 'twitter', 'telegram', 'rate_dialog', 'share_dialog']
        # ,'coin_detail']

class app_dataother_serializer(serializers.ModelSerializer):
    # coin_detail = coin_data_serializer(many=True,read_only=True)
    class Meta:
        model = app_data
        fields =  ['earn_like_coin', 'spent_like_coin', 'earn_follow_coin', 'spent_follow_coin', 'referrel_coin', 'default_coin', 'from_add_coin', 'maintenence_mode', 'playstore_version', 'update_mode', 'update_url', 'payment_method', 'game_id', 'banner_id', 'initial_id', 'maintenence_message', 'notification_title', 'notification_message', 'notification_show', 'update_message', 'user_agent', 'share_url', 'web', 'website', 'offer', 'offer_percentage', 'offer_starttime', 'offer_endtime', 'offer_discount_text', 'offer_discount_image', 'web_login', 'email', 'privacy_policy', 'facebook', 'instagram', 'twitter', 'telegram', 'rate_dialog', 'share_dialog']
        # ,'coin_detail']

class users_data_serializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ['user_id','username','total_coins','referral_code','is_referred']

class orders_data_serializer(serializers.ModelSerializer):
    class Meta:
        model = orders
        fields = ['user_id','custom_user_id','needed','recieved','image_url']

class child_users_data_serializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ['user_id','username']




class appdata_serializer(serializers.ModelSerializer):
    class Meta:
        model = app_data
        fields =  "__all__"

class purchase_coin_serializer(serializers.ModelSerializer):
    class Meta:
        model = purchase_coins
        fields =  "__all__"
