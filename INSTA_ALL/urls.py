from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework import routers
# from . import views
from .views import *


urlpatterns = [
    path('api/appdata',app_datalist.as_view()),
    path('api/getprofile',get_profile.as_view()),
    path('api/getprofileparent',get_profile_parent.as_view()),
    path('api/order',order_api.as_view()),
    path('api/refferalcode',refferalcode.as_view()),
    path('api/purchasecoin',purchasecoin.as_view()),
    path('api/fetchpost',fetchpost_api.as_view()),
    path('api/verifyinapp',verifyinapp.as_view()),
    path('api/callback_2048',callback_2048.as_view()),

    # App Data
    path('unknown/', admin.as_view(), name='admin'),
    path('unknown/home/', home.as_view(), name='home'),
    path('unknown/appcoindetail/', appdata_coindetail.as_view(), name='appdatacoindetail'),
    path('unknown/offer/', appdata_offer.as_view(), name='appdataoffer'),
    path('unknown/maintenence/', appdata_maintenence.as_view(), name='appdatamaintenence'),
    path('unknown/ads/', appdata_ads_detail.as_view(), name='appdataadsdetail'),
    path('unknown/other/', appdata_other.as_view(), name='appdataother'),
    # Notification
    path('unknown/dailynotification/', Daily_Notification.as_view(), name='dailynotification'),
    path('unknown/sendnotification/', Send_Notification.as_view(), name='sendnotification'),
    # Home 
    path('unknown/coin_details/', Coin_Details.as_view(), name='coindetails'),
    path('unknown/ip_block/', Ip_Block.as_view(), name='ipblock'),
    path('unknown/manage_profile/', Manage_Profile.as_view(), name='manageprofile'),
    # Other List
    path('unknown/activeorder/', Active_Order_List.as_view(), name='activeorder'),
        path('unknown/allorder/', All_Order.as_view(),name='allorder'),
        path('unknown/likeorder/', Like_Order.as_view(),name='likeorder'),
        path('unknown/followorder/', Follow_Order.as_view(),name='followorder'),
        path('unknown/completeorder/', Complete_Order.as_view(),name='completeorder'),
    path('unknown/userlist/', User_List.as_view(), name='userlist'),
    path('unknown/premiumuserlist/', Premium_User_List.as_view(), name='premiumuserlist'),
    path('unknown/purchasecoin_other_method_list/', Purchase_Coin_Other_method_List.as_view(), name='purchasecoin_other_method_list'),
    path('unknown/purchasecoin_inapp_method_list/', Purchase_Coin_InApp_List.as_view(), name='purchasecoin_inapp_method_list'),
    # LogOut
    path('unknown/logout/', Logout.as_view(), name='logout'),

    #privacy_pollicy
    path('public/privacy_pollicy/', privacy_pollicy.as_view(), name='privacy_pollicy'),
    path('public/term_of_service/', term_of_service.as_view(), name='term_of_service'),
]
