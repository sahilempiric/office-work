from inspect import cleandoc
import requests
import json
import re
from django import shortcuts
from django.db.models.expressions import F
from django.db.models.fields import NullBooleanField
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls.conf import path
from django.utils.functional import empty
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from .models import app_data, coin_details, orders, user_orders, users, purchase_coins, already_like_follow, check_ip_addresses
from .serializers import app_data_serializer, coin_data_serializer, orders_data_serializer, users_data_serializer, child_users_data_serializer, appdata_serializer, purchase_coin_serializer, app_dataother_serializer, app_dataaccess_serializer
from django.db import connection
from collections import OrderedDict
from rest_framework import viewsets
from rest_framework.decorators import action
import random
import string
from django.db.models import Q
import os
import datetime
# from datetime import datetime
import math
from django.conf import settings 
import uuid
from django.templatetags.static import static
import firebase_admin
# from firebase_admin import credentials, messaging
import urllib.request
from django.views import View
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth.models import auth as authu
from django.contrib.auth import get_user_model
import socket
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import time
import http.client
import urllib
import base64
import hmac
import hashlib
from django.shortcuts import render
from django.http import HttpResponse  
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import messaging
from django.conf import settings
from django.contrib.auth.models import User
import logging   
logger = logging.getLogger(__name__)
# logger.info('dgfdsafgdsgsfrghtdey356ty5rge5yte54y checker')

base_url = settings.BASE_DIR
like_URL = f"{base_url}/static/img/like/"
follow_URL = f"{base_url}/static/img/follow/"
Offer_Img_URL = f"{base_url}/static/img/appdata_offer/"
# base_url = request.build_absolute_uri('/').strip("/")
# like_URL = request.build_absolute_uri('/').strip("/")
# follow_URL = "/root/insta_like_follow/static/img/follow/"
# Offer_Img_URL = "/root/insta_like_follow/static/img/appdata_offer/"

cred = credentials.Certificate(f"{base_url}/serviceAccountKey.json")
# cred = credentials.RefreshToken('path/to/refreshToken.json')
default_app = firebase_admin.initialize_app(cred)

def send_notification(title,body_desc,registration_token):
    
    message = messaging.Message(
        notification=messaging.Notification(title, body_desc),
        token=registration_token,
    )
    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)

    file = open(base_url + "INSTA_ALL/responce.txt", "a")
    file.write(str(response))
    file.close()

    return response

def getrandompost(userid,total_coins,request): 

    # app_data for maintenence check
    all_data1 = app_data.objects.all()
    serializer1 = app_data_serializer(all_data1, many=True)
    app_data_dic = serializer1.data
    if app_data_dic != []:
        app_data_dic = json.dumps(serializer1.data).strip('[]')
        app_data_dic = json.loads(app_data_dic)
        cca = app_data_dic['maintenence_mode'].split(',')
        ccb = app_data_dic['payment_method'].split(',')
        app_data_dic['maintenence_mode'] = cca
        app_data_dic['payment_method'] = ccb
    else:
        get_pre = {
            "success": False,
            "message": "Server Issue"
        }
        return Response(get_pre)
    # End app_data for maintenence check

    if len(app_data_dic['maintenence_mode']) == 2:
        orders_d = orders.objects.filter(~Q(needed = '0')).order_by('?')
    else:
        if "follow" in app_data_dic['maintenence_mode']:
            orders_d = orders.objects.filter(~Q(needed = '0'),type="1").order_by('?')
        elif "like" in app_data_dic['maintenence_mode']:
            orders_d = orders.objects.filter(~Q(needed = '0'),type="0").order_by('?')
        else:
            get_pre = {
                "success": False,
                "message": "currently app in maintenence."
            }
            return Response(get_pre)
    
    i = 0
    if len(orders_d) != 0:
        for order in orders_d:
            user_id = order.custom_user_id
            likefollow_listss = []
            likefollow_list = []
            # print(order.type)
            if order.type == "0":
                if already_like_follow.objects.filter(post_id=order.post_id, type=order.type).exists():
                    likefollow_list = list(already_like_follow.objects.filter(post_id=order.post_id, type=order.type).values('al_user_id'))

            elif order.type == "1":
                if already_like_follow.objects.filter(custom_user_id=order.custom_user_id, type=order.type).exists():
                    likefollow_list = list(already_like_follow.objects.filter(custom_user_id=order.custom_user_id, type=order.type).values('al_user_id'))

            # logger.info(likefollow_list)
            for lef in likefollow_list:
                likefollow_listss.append(lef['al_user_id'])

            if str(userid) not in likefollow_listss:
                thubnail_url = order.image_url
                if order.type == "0":
                    file = request.build_absolute_uri('/').strip("/") + '/static/img/like/'+thubnail_url
                elif order.type == "1":
                    file =  request.build_absolute_uri('/').strip("/") + '/static/img/follow/'+thubnail_url

                # image_path = settings.APP_URL + file
                image_path = file

                data = {
                    'user_id':order.user_id,
                    'total_coin':total_coins,
                    'post_id':order.post_id,
                    'type':order.type,
                    'image_url':image_path,
                    'fetch_post':True,
                }
                
                if order.custom_user_id:
                    data['custom_user_id'] = order.custom_user_id
                
                
                if order.type == "0":
                    data['short_code'] = order.short_code
                elif order.type == "1":
                    data['username'] = order.username

                return data
            else:
                i = 1
        if i == 1:
            data = {
                'total_coin':total_coins,
                'fetch_post':False,
            }
            return data
    else:
        data = {
            'total_coin':total_coins,
            'fetch_post':False,
        }
        return data

class app_datalist(APIView):
    def get(self, request):

        all_data1 = app_data.objects.all()
        serializer1 = app_data_serializer(all_data1, many=True)
        app_data_dic = serializer1.data

        all_data2 = coin_details.objects.filter(coin_status='0').extra(select={'indianrate': 'CAST(indian_rate AS INTEGER)'}).order_by('indianrate')
        serializer2 = coin_data_serializer(all_data2, many=True)
        app_data_dicsss = serializer2.data
        
        if app_data_dicsss != []:
            app_data_dicsss = json.dumps(serializer2.data)
            app_data_dicsss = json.loads(app_data_dicsss)
            for all in app_data_dicsss:
                ccc = int(all['indian_rate']) * 100
                all['indian_rate'] = ccc

            

        if app_data_dic != []:
            app_data_dic = json.dumps(serializer1.data).strip('[]')
            app_data_dic = json.loads(app_data_dic)
            
            cca = app_data_dic['maintenence_mode'].split(',')
            ccb = app_data_dic['payment_method'].split(',')
            if cca != [""]:
                app_data_dic['maintenence_mode'] = cca
            else:
                app_data_dic['maintenence_mode'] = []
            
            if ccb != [""]:
                app_data_dic['payment_method'] = ccb
            else:
                app_data_dic['payment_method'] = []

            if app_data_dic['offer_starttime'] != "" and app_data_dic['offer_endtime'] != "":
                app_data_dic['offer_starttime'] = int(time.mktime(datetime.datetime.strptime(str(app_data_dic['offer_starttime']),"%m/%d/%Y %I:%M %p").timetuple()))
                app_data_dic['offer_endtime'] = int(time.mktime(datetime.datetime.strptime(str(app_data_dic['offer_endtime']),"%m/%d/%Y %I:%M %p").timetuple()))

            app_data_dic['coin_detail'] = app_data_dicsss
            all_d = {
                "success": True,
                "data": app_data_dic,
                "message": "App Data List"
            }
            
        else:
            all_d = {
                "success": False,
                "data": "",
                "message": "Data Not Found!"
            }

        return Response(all_d)

def visitor_ip_address(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')     #('HTTP_X_REAL_IP') #['X_FORWARDED_FOR']

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    # ip, is_routable = get_client_ip(request)
    return ip

class get_profile(APIView):

    def post(self, request):

        get_pro = request.data
        userid_bool = False
        username_bool = False
        fromapp_bool = False

        check_ip = str(visitor_ip_address(request))

        if check_ip_addresses.objects.filter(ip=check_ip).exists():
            get_pre = {
                "success": False,
                "message": "Your behaviour not good"
            }
            return Response(get_pre)
        

        userid_param = request.data.get('user_id')
        if userid_param is not None:
            if str(get_pro['user_id']).replace(' ','') != "":
                userid_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "user_id Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "user_id Required"
            }
            return Response(get_pre)

        username_param = request.data.get('username')
        if username_param is not None:
            if str(get_pro['username']).replace(' ','') != "":
                username_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "username Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "username Required"
            }
            return Response(get_pre)

        
        fromapp_param = request.data.get('fromapp')
        if fromapp_param is not None:
            if str(get_pro['fromapp']).replace(' ','') != "":
                fromapp_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "fromapp Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "fromapp Required"
            }
            return Response(get_pre)
        
        reference_id_param = request.data.get('reference_id')
        if reference_id_param is not None:
            if str(get_pro['reference_id']).replace(' ','') != "":
                if userid_bool == True and username_bool == True and fromapp_bool == True:
                    # ftoken_param = request.data.get('ftoken')
                    # if ftoken_param is not None:
                    #     if str(parent_pro['ftoken']).replace(' ','') != "":
                    #         user_profile_attrs = {
                    #             "user_id": get_pro['user_id'],
                    #             "username": get_pro['username'],
                    #             "fromapp": get_pro['fromapp'],
                    #             "reference_id": get_pro['reference_id'],
                    #             "ftoken": request.data.get('ftoken')
                    #         }
                    #     else:
                    #         user_profile_attrs = {
                    #             "user_id": get_pro['user_id'],
                    #             "username": get_pro['username'],
                    #             "fromapp": get_pro['fromapp'],
                    #             "reference_id": get_pro['reference_id'],
                    #         }
                    # else:
                    #     user_profile_attrs = {
                    #         "user_id": get_pro['user_id'],
                    #         "username": get_pro['username'],
                    #         "fromapp": get_pro['fromapp'],
                    #         "reference_id": get_pro['reference_id'],
                    #     }

                    r = requests.post('http://'+str(request.META['HTTP_HOST'])+'/api/getprofileparent', data=request.POST)
                    # r = json.dumps(r.text)
                    r = json.loads(r.text)
                    return Response(r)


        if userid_bool == True and username_bool == True and fromapp_bool == True:
            if get_pro['fromapp'] == "1":
                    
                if users.objects.filter(user_id=get_pro['user_id']).exists():
                    user_id = get_pro['user_id']

                    if users.objects.filter(user_id=user_id, status="0").exists():
                        get_pre = {
                            "success": False,
                            "message": "Your Account is Suspended"
                        }
                        return Response(get_pre)
                    else:
                        ftoken_param = request.data.get('ftoken')
                        if ftoken_param is not None:
                            if str(get_pro['ftoken']).replace(' ','') != "":
                                user_data = users.objects.get(user_id=user_id)
                                user_data.ftoken = get_pro['ftoken']
                                user_data.save()


                        if users.objects.filter(parent_id='0', user_id=user_id).exists():
                            main_data = users.objects.filter(user_id=user_id)
                            serializer_main = users_data_serializer(main_data, many=True)
                            main_data_dix = serializer_main.data
                            main_data_dix = json.dumps(main_data_dix).strip('[]')
                            main_data_dix = json.loads(main_data_dix)

                            child_list = users.objects.filter(parent_id=user_id)
                            if len(child_list) > 0:
                                user_data = users.objects.get(user_id=user_id)
                                like_orders = []
                                follow_orders = []
                                child_list = []
                                child_list_d = users.objects.filter(~Q(user_id=user_id), parent_id=user_id)

                                for child_d in child_list_d:
                                    child_dd = users.objects.filter(user_id=child_d.user_id)
                                    serializer_chad = child_users_data_serializer(child_dd, many=True)
                                    child_chad = serializer_chad.data
                                    child_chad = json.dumps(child_chad).strip('[]')
                                    child_chad = json.loads(child_chad)
                                    child_chad['user_name'] = child_chad.pop('username')
                                    child_list.append(child_chad)

                                child_list_for_order = users.objects.filter(parent_id=user_id)
                                order_list_for_parent = orders.objects.filter(~Q(needed="0"), user_id=user_id)
                                for parent_order in order_list_for_parent:
                                    thubnail_url = parent_order.image_url

                                    if parent_order.type == "0":
                                        file = request.build_absolute_uri('/').strip("/") + '/static/img/like/'+thubnail_url
                                        # image_path = settings.APP_URL + file
                                        image_path = file

                                        order_dd = orders.objects.filter(id=parent_order.id)
                                        serializer_osd = orders_data_serializer(order_dd, many=True)
                                        parent_osd = serializer_osd.data
                                        parent_osd = json.dumps(parent_osd).strip('[]')
                                        parent_osd = json.loads(parent_osd)
                                        parent_osd['order_owner '] = "1"
                                        parent_osd['image_url'] = image_path

                                        like_orders.append(parent_osd)
                                    elif parent_order.type == "1":
                                        file = request.build_absolute_uri('/').strip("/") + '/static/img/follow/'+thubnail_url
                                        # image_path = settings.APP_URL + file
                                        image_path = file

                                        order_dd = orders.objects.filter(id=parent_order.id)
                                        serializer_osd = orders_data_serializer(order_dd, many=True)
                                        parent_osd = serializer_osd.data
                                        parent_osd = json.dumps(parent_osd).strip('[]')
                                        parent_osd = json.loads(parent_osd)
                                        parent_osd['order_owner '] = "1"
                                        parent_osd['image_url'] = image_path

                                        follow_orders.append(parent_osd)

                                for child_order_d in child_list_for_order:
                                    order_list = orders.objects.filter(~Q(needed="0"), user_id=child_order_d.user_id)
                                    for order_l in order_list:
                                        thubnail_url = order_l.image_url

                                        if order_l.type == "0":
                                            file = request.build_absolute_uri('/').strip("/") + '/static/img/like/'+thubnail_url
                                            # image_path = settings.APP_URL + file
                                            image_path = file

                                            order_ddd = orders.objects.filter(id=order_l.id)
                                            serializer_cosd = orders_data_serializer(order_ddd, many=True)
                                            child_cosd = serializer_cosd.data
                                            child_cosd = json.dumps(child_cosd).strip('[]')
                                            child_cosd = json.loads(child_cosd)
                                            child_cosd['order_owner '] = "0"
                                            child_cosd['image_url'] = image_path

                                            like_orders.append(child_cosd)
                                        elif order_l.type == "1":
                                            file = request.build_absolute_uri('/').strip("/") + '/static/img/follow/'+thubnail_url
                                            # image_path = settings.APP_URL + file
                                            image_path = file

                                            order_ddd = orders.objects.filter(id=order_l.id)
                                            serializer_cosd = orders_data_serializer(order_ddd, many=True)
                                            child_cosd = serializer_cosd.data
                                            child_cosd = json.dumps(child_cosd).strip('[]')
                                            child_cosd = json.loads(child_cosd)
                                            child_cosd['order_owner '] = "0"
                                            child_cosd['image_url'] = image_path

                                            follow_orders.append(child_cosd)

                                
                                
                                data = {
                                    "user_id": main_data_dix["user_id"],
                                    "username": main_data_dix["username"],
                                    "parent_id": main_data_dix["user_id"],
                                    "child_list": child_list,
                                    "parent_account": [],
                                    "total_coins": main_data_dix["total_coins"],
                                    "referral_code": main_data_dix["referral_code"],
                                    "is_referred": main_data_dix["is_referred"],
                                    "likeorder": like_orders,
                                    "followorder": follow_orders
                                }

                            else:
                                main_data = users.objects.filter(user_id=user_id)
                                serializer_main = users_data_serializer(main_data, many=True)
                                main_data_dix = serializer_main.data
                                main_data_dix = json.dumps(main_data_dix).strip('[]')
                                main_data_dix = json.loads(main_data_dix)
                                child_list = []
                                like_orders = []
                                follow_orders = []

                                order_list_for_parent = orders.objects.filter(~Q(needed="0"), user_id=user_id)
                                for parent_order in order_list_for_parent:
                                    thubnail_url = parent_order.image_url

                                    if parent_order.type == "0":
                                        file = request.build_absolute_uri('/').strip("/") + '/static/img/like/'+thubnail_url
                                        # image_path = settings.APP_URL + file
                                        image_path = file

                                        order_dd = orders.objects.filter(id=parent_order.id)
                                        serializer_osd = orders_data_serializer(order_dd, many=True)
                                        parent_osd = serializer_osd.data
                                        parent_osd = json.dumps(parent_osd).strip('[]')
                                        parent_osd = json.loads(parent_osd)
                                        parent_osd['image_url'] = image_path
                                        parent_osd['order_owner '] = "1"


                                        like_orders.append(parent_osd)
                                    elif parent_order.type == "1":
                                        file = request.build_absolute_uri('/').strip("/") + '/static/img/follow/'+thubnail_url
                                        # image_path = settings.APP_URL + file
                                        image_path = file

                                        order_dd = orders.objects.filter(id=parent_order.id)
                                        serializer_osd = orders_data_serializer(order_dd, many=True)
                                        parent_osd = serializer_osd.data
                                        parent_osd = json.dumps(parent_osd).strip('[]')
                                        parent_osd = json.loads(parent_osd)
                                        parent_osd['image_url'] = image_path
                                        parent_osd['order_owner '] = "1"


                                        follow_orders.append(parent_osd)

                                data = {
                                    "user_id": main_data_dix["user_id"],
                                    "username": main_data_dix["username"],
                                    "parent_id": main_data_dix["user_id"],
                                    "child_list": child_list,
                                    "parent_account": [],
                                    "total_coins": main_data_dix["total_coins"],
                                    "referral_code": main_data_dix["referral_code"],
                                    "is_referred": main_data_dix["is_referred"],
                                    "likeorder": like_orders,
                                    "followorder": follow_orders
                                }

                            # set_ip = str(visitor_ip_address(request))
                            # user_ip = users.objects.get(user_id=get_pro['user_id'])  
                            # user_id.ip = set_ip
                            # user_id.save()

                        else:
                            user_d_data = users.objects.get(user_id=user_id)
                            parent_use_id = user_d_data.parent_id

                            main_data = users.objects.filter(user_id=user_id)
                            serializer_main = users_data_serializer(main_data, many=True)
                            main_data_dix = serializer_main.data
                            main_data_dix = json.dumps(main_data_dix).strip('[]')
                            main_data_dix = json.loads(main_data_dix)

                            like_orders = []
                            follow_orders = []
                            child_list_dd = []

                            pranet_dd_data = users.objects.filter(user_id=parent_use_id)
                            serializer_f_parent = users_data_serializer(pranet_dd_data, many=True)
                            parent_mix = serializer_f_parent.data
                            parent_mix = json.dumps(parent_mix).strip('[]')
                            parent_mix = json.loads(parent_mix) 
                            parent_mix['user_name'] = parent_mix.pop('username')
                            serializer_fdata_parent = child_users_data_serializer(pranet_dd_data, many=True)
                            parent_data = serializer_fdata_parent.data
                            parent_data = json.dumps(parent_data).strip('[]')
                            parent_data = json.loads(parent_data)
                            parent_data['user_name'] = parent_data.pop('username')

                            child_list_dd.append(parent_data)
                            


                            child_list_fl = users.objects.filter(parent_id=parent_use_id)

                            child_list_d = users.objects.filter(~Q(user_id=user_id), parent_id=parent_use_id)

                            for child_d in child_list_d:
                                child_dd = users.objects.filter(user_id=child_d.user_id)
                                serializer_chad = child_users_data_serializer(child_dd, many=True)
                                child_chad = serializer_chad.data
                                child_chad = json.dumps(child_chad).strip('[]')
                                child_chad = json.loads(child_chad)
                                child_chad['user_name'] = child_chad.pop('username')

                                child_list_dd.append(child_chad)

                            order_list_for_parent = orders.objects.filter(~Q(needed="0"), user_id=parent_use_id)
                            for parent_order in order_list_for_parent:
                                thubnail_url = parent_order.image_url

                                if parent_order.type == "0":
                                    file = request.build_absolute_uri('/').strip("/") + '/static/img/like/'+thubnail_url
                                    # image_path = settings.APP_URL + file
                                    image_path = file

                                    order_dd = orders.objects.filter(id=parent_order.id)
                                    serializer_osd = orders_data_serializer(order_dd, many=True)
                                    parent_osd = serializer_osd.data
                                    parent_osd = json.dumps(parent_osd).strip('[]')
                                    parent_osd = json.loads(parent_osd)
                                    parent_osd['order_owner '] = "1"
                                    parent_osd['image_url'] = image_path

                                    like_orders.append(parent_osd)
                                elif parent_order.type == "1":
                                    file = request.build_absolute_uri('/').strip("/") + '/static/img/follow/'+thubnail_url
                                    # image_path = settings.APP_URL + file
                                    image_path = file

                                    order_dd = orders.objects.filter(id=parent_order.id)
                                    serializer_osd = orders_data_serializer(order_dd, many=True)
                                    parent_osd = serializer_osd.data
                                    parent_osd = json.dumps(parent_osd).strip('[]')
                                    parent_osd = json.loads(parent_osd)
                                    parent_osd['order_owner '] = "1"
                                    parent_osd['image_url'] = image_path

                                    follow_orders.append(parent_osd)

                            for child_ss in child_list_fl:
                                order_list_for_alchild = orders.objects.filter(~Q(needed="0"), user_id=child_ss.user_id)
                                for ordre_ch_al in order_list_for_alchild:
                                    thubnail_url = ordre_ch_al.image_url

                                    if ordre_ch_al.type == "0":
                                        file = request.build_absolute_uri('/').strip("/") + '/static/img/like/'+thubnail_url
                                        # image_path = settings.APP_URL + file
                                        image_path = file

                                        order_dd = orders.objects.filter(id=ordre_ch_al.id)
                                        serializer_osd = orders_data_serializer(order_dd, many=True)
                                        child_osd = serializer_osd.data
                                        child_osd = json.dumps(child_osd).strip('[]')
                                        child_osd = json.loads(child_osd)
                                        child_osd['order_owner '] = "0"
                                        child_osd['image_url'] = image_path

                                        like_orders.append(child_osd)
                                    elif ordre_ch_al.type == "1":
                                        file = request.build_absolute_uri('/').strip("/") + '/static/img/follow/'+thubnail_url
                                        # image_path = settings.APP_URL + file
                                        image_path = file

                                        order_dd = orders.objects.filter(id=ordre_ch_al.id)
                                        serializer_osd = orders_data_serializer(order_dd, many=True)
                                        child_osd = serializer_osd.data
                                        child_osd = json.dumps(child_osd).strip('[]')
                                        child_osd = json.loads(child_osd)
                                        child_osd['order_owner '] = "0"
                                        child_osd['image_url'] = image_path

                                        follow_orders.append(child_osd)
                            data = {
                                "user_id": main_data_dix["user_id"],
                                "username": main_data_dix["username"],
                                "parent_id": parent_data['user_id'],
                                "child_list": child_list_dd,
                                "total_coins": parent_mix["total_coins"],
                                "referral_code": parent_mix["referral_code"],
                                "is_referred": parent_mix["is_referred"],
                                "parent_account": parent_data,
                                "likeorder": like_orders,
                                "followorder": follow_orders
                            }

                        # set_ip = str(visitor_ip_address(request))
                        # user_ip = users.objects.get(user_id=get_pro['user_id'])  
                        # user_ip.ip = set_ip
                        # user_ip.save()


                        get_pre = {
                            "success": True,
                            "data": data,
                            "message": "User Login Successfully"
                        }
                        return Response(get_pre)
                else:
                    user_id = get_pro['user_id']
                    user_name = get_pro['username']
                    from_app = get_pro['fromapp']

                    e = app_data.objects.all()

                    if app_data.objects.all().exists():
                        # total_coin = e[0].default_coin
                        for e in app_data.objects.all():
                            total_coin = e.default_coin
                    else:
                        get_pre = {
                            "success": False,
                            "message": "Data Not found"
                        }
                        return Response(get_pre)

                    referal_code = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=6))

                    ftoken_param = request.data.get('ftoken')

                    set_ip = str(visitor_ip_address(request))

                    if ftoken_param is not None:
                        if str(get_pro['ftoken']).replace(' ','') != "":
                            ftoken = get_pro['ftoken']
                            get_pro = users.objects.create(username=user_name, user_id=user_id, ftoken=ftoken,total_coins=total_coin, referral_code=referal_code, fromapp=from_app,ip= set_ip)
                            # get_pro.save()
                    else:
                        get_pro = users.objects.create(username=user_name, user_id=user_id, total_coins=total_coin, referral_code=referal_code, fromapp=from_app, ip=set_ip)
                        # get_pro.save()  

                                     

                    user_data = users.objects.filter(user_id=user_id)
                    serializer = users_data_serializer(user_data, many=True)
                    user_data_dic = serializer.data
                    user_data_dic = json.dumps(user_data_dic)
                    user_data_dic = json.loads(user_data_dic)
                    user_data_dic[-1]["parent_id"] = user_data_dic[-1]['user_id']
                    user_data_dic[-1]["child_list"] = []
                    user_data_dic[-1]["likeorder"] = []
                    user_data_dic[-1]["followorder"] = []
                    user_data_dic = json.dumps(user_data_dic).strip('[]')
                    user_data_dic = json.loads(user_data_dic)

                    get_pre = {
                        "success": True,
                        "data": user_data_dic,
                        "message": "User login successfully"
                    }
                    return Response(get_pre)
            else:
                get_pre = {
                    "success": False,
                    "message": "fromapp is not valid"
                }
                return Response(get_pre)
        else:
            get_pre = {
                "success": False,
                "message": "All Arghument Required"
            }
            return Response(get_pre)

class get_profile_parent(APIView):

    def post(self, request):
        parent_pro = request.data
        username_bool = False
        userid_bool = False
        referceid_bool = False
        fromapp_bool = False
        
        userid_param = request.data.get('user_id')
        if userid_param is not None:
            if str(parent_pro['user_id']).replace(' ','') != "":
                userid_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "user_id is Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "user_id is Required"
            }
            return Response(get_pre)
        
        username_param = request.data.get('username')
        if username_param is not None:
            if str(parent_pro['username']).replace(' ','') != "":
                username_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "username is Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "username is Required"
            }
            return Response(get_pre)
        
        reference_id_param = request.data.get('reference_id')
        if reference_id_param is not None:
            if str(parent_pro['reference_id']).replace(' ','') != "":
                referceid_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "reference_id is Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "reference_id is Required"
            }
            return Response(get_pre)
        
        fromapp_param = request.data.get('fromapp')
        if fromapp_param is not None:
            if str(parent_pro['fromapp']).replace(' ','') != "":
                fromapp_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "fromapp is Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "fromapp is Required"
            }
            return Response(get_pre)



        if username_bool == True and userid_bool == True and referceid_bool == True and fromapp_bool == True:
            if parent_pro['fromapp'] == "1":
                user_id = parent_pro['user_id']
                reference_id = parent_pro['reference_id']
                like_orders = []
                follow_orders = []

                if users.objects.filter(user_id=reference_id).exists():
                    user_datas = users.objects.get(user_id=reference_id)

                    if users.objects.filter(user_id=user_id).exists():
                        if users.objects.filter(user_id=user_id,parent_id="0").exists():
                            get_pre = {
                                "success": False,
                                "message": "Your account is already a parent account."
                            }
                            return Response(get_pre)
                        child_ac_list = users.objects.filter(parent_id=reference_id)
                        child_list_check = []
                        if len(child_ac_list) > 0:
                            for child_ac in child_ac_list:
                                child_list_check.append(child_ac.user_id)
                        
                        
                        if str(parent_pro['user_id']) in child_list_check:
                            get_pre = {
                                "success": False,
                                "message": "Your account is already linked with another account"
                            }
                            return Response(get_pre)
                        set_user = users.objects.get(user_id=parent_pro['user_id'])

                        if set_user.parent_id != "0":
                            get_pre = {
                                "success": False,
                                "message": "Your account is already linked with another account"
                            }
                            return Response(get_pre)

                        ftoken_param = request.data.get('ftoken')
                        if ftoken_param is not None:
                            if str(parent_pro['ftoken']).replace(' ','') != "":
                                user_data = users.objects.get(user_id=user_id)
                                user_data.ftoken = parent_pro['ftoken']
                                user_data.save()

                        if user_datas.parent_id == "0":
                            parent_id = user_datas.user_id
                        else:
                            parent_id = user_datas.parent_id
                        
                        user_upd = users.objects.get(user_id=user_id)
                        user_upd.parent_id = parent_id
                        user_upd.save()

                        order_list_for_parent = orders.objects.filter(~Q(needed="0"), user_id=parent_id)
                        for parent_order in order_list_for_parent:
                            thubnail_url = parent_order.image_url
                            
                            if parent_order.type == "0":
                                file = request.build_absolute_uri('/').strip("/") + '/static/img/like/'+thubnail_url
                                # image_path = settings.APP_URL + file
                                image_path = file

                                order_dd = orders.objects.filter(id=parent_order.id)
                                serializer_osd = orders_data_serializer(order_dd, many=True)
                                parent_osd = serializer_osd.data
                                parent_osd = json.dumps(parent_osd).strip('[]')
                                parent_osd = json.loads(parent_osd)
                                parent_osd['order_owner '] = "1"
                                parent_osd['image_url'] = image_path
                                like_orders.append(parent_osd)

                            elif parent_order.type == "1":
                                file = request.build_absolute_uri('/').strip("/") + '/static/img/follow/'+thubnail_url
                                # image_path = settings.APP_URL + file
                                image_path = file

                                order_dd = orders.objects.filter(id=parent_order.id)
                                serializer_osd = orders_data_serializer(order_dd, many=True)
                                parent_osd = serializer_osd.data
                                parent_osd = json.dumps(parent_osd).strip('[]')
                                parent_osd = json.loads(parent_osd)
                                parent_osd['order_owner '] = "1"
                                parent_osd['image_url'] = image_path
                                follow_orders.append(parent_osd)

                        child_ll = users.objects.filter(~Q(user_id=user_id), parent_id=parent_id)

                        child_list_for_order = users.objects.filter(parent_id=parent_id)

                        for child_order_d in child_list_for_order:
                            order_list = orders.objects.filter(~Q(needed="0"), user_id=child_order_d.user_id)
                            for order_l in order_list:
                                thubnail_url = order_l.image_url

                                if order_l.type == "0":
                                    file = request.build_absolute_uri('/').strip("/") + '/static/img/like/'+thubnail_url
                                    # image_path = settings.APP_URL + file
                                    image_path = file

                                    order_ddd = orders.objects.filter(id=order_l.id)
                                    serializer_cosd = orders_data_serializer(order_ddd, many=True)
                                    child_cosd = serializer_cosd.data
                                    child_cosd = json.dumps(child_cosd).strip('[]')
                                    child_cosd = json.loads(child_cosd)
                                    child_cosd['order_owner '] = "0"
                                    child_cosd['image_url'] = image_path
                                    like_orders.append(child_cosd)
                                elif order_l.type == "1":
                                    file = request.build_absolute_uri('/').strip("/") + '/static/img/follow/'+thubnail_url
                                    # image_path = settings.APP_URL + file
                                    image_path = file

                                    order_ddd = orders.objects.filter(id=order_l.id)
                                    serializer_cosd = orders_data_serializer(order_ddd, many=True)
                                    child_cosd = serializer_cosd.data
                                    child_cosd = json.dumps(child_cosd).strip('[]')
                                    child_cosd = json.loads(child_cosd)
                                    child_cosd['order_owner '] = "0"
                                    child_cosd['image_url'] = image_path
                                    follow_orders.append(child_cosd)

                        child_list = []
                        child_ddss = users.objects.filter(parent_id=parent_id)
                        for chi in child_ddss:
                            etr = {"user_id":chi.user_id,"username":chi.username}
                            child_list.append(etr) 

                        parent_ddss = users.objects.filter(user_id=parent_id)
                        for parent in parent_ddss:
                            etrs = {"user_id":parent.user_id,"username":parent.username}
                            child_list.append(etrs) 


                        main_data = users.objects.filter(user_id=reference_id)
                        if main_data.parent_id == "0":
                            serializer_main = users_data_serializer(main_data, many=True)
                            main_data_dix = serializer_main.data
                            main_data_dix = json.dumps(main_data_dix).strip('[]')
                            main_data_dix = json.loads(main_data_dix)
                        else:
                            main_data = users.objects.filter(user_id=reference_id.parent_id)
                            serializer_main = users_data_serializer(main_data, many=True)
                            main_data_dix = serializer_main.data
                            main_data_dix = json.dumps(main_data_dix).strip('[]')
                            main_data_dix = json.loads(main_data_dix)

                        data = {
                            "user_id": parent_pro["user_id"],
                            "username": parent_pro["username"],
                            "parent_id": parent_id,
                            "total_coins": main_data_dix["total_coins"],
                            "is_referred": main_data_dix["is_referred"],
                            "referral_code": main_data_dix["referral_code"],
                            "child_list": child_list,
                            "likeorder": like_orders,
                            "followorder": follow_orders
                        }
                        get_pre = {
                            "success": True,
                            "data":data,
                            "message": "User Login Successfully"
                        }

                        return Response(get_pre)
                    else:
                        if user_datas.parent_id == "0":
                            parent_ids = user_datas.user_id
                        else:
                            parent_ids = user_datas.parent_id

                        # order_list_for_parent = orders.objects.filter(~Q(needed="0"), user_id=parent_ids)
                        # for parent_order in order_list_for_parent:
                        #     thubnail_url = parent_order.image_url

                        #     if parent_order.type == "0":
                        #         file = '/static/img/like/'+thubnail_url
                        #         image_path = settings.APP_URL + file

                        #         order_dd = orders.objects.filter(id=parent_order.id)
                        #         serializer_osd = orders_data_serializer(order_dd, many=True)
                        #         parent_osd = serializer_osd.data
                        #         parent_osd = json.dumps(parent_osd).strip('[]')
                        #         parent_osd = json.loads(parent_osd)
                        #         parent_osd['order_owner'] = "1"
                        #         parent_osd['image_url'] = image_path
                        #         like_orders.append(parent_osd)

                        #     elif parent_order.type == "1":
                        #         file = '/static/img/follow/'+thubnail_url
                        #         image_path = settings.APP_URL + file

                        #         order_dd = orders.objects.filter(id=parent_order.id)
                        #         serializer_osd = orders_data_serializer(order_dd, many=True)
                        #         parent_osd = serializer_osd.data
                        #         parent_osd = json.dumps(parent_osd).strip('[]')
                        #         parent_osd = json.loads(parent_osd)
                        #         parent_osd['order_owner'] = "1"
                        #         parent_osd['image_url'] = ''+image_path
                        #         follow_orders.append(parent_osd)

                        ftoken_param = request.data.get('ftoken')
                        if ftoken_param is not None:
                            if str(parent_pro['ftoken']).replace(' ','') != "":
                                users.objects.create(username=parent_pro['username'], user_id=parent_pro['user_id'], parent_id=parent_ids, fromapp="1", ftoken=parent_pro['ftoken'])
                        else:
                            users.objects.create(username=parent_pro['username'], user_id=parent_pro['user_id'], parent_id=parent_ids, fromapp="1")

                        child_list = []
                        child_ll = users.objects.filter(~Q(user_id=user_id), parent_id=parent_ids)
                        for chi in child_ll:
                            etr = {"user_id":chi.user_id,"username":chi.username}
                            child_list.append(etr)  

                        parent_ll = users.objects.filter(~Q(user_id=user_id), user_id=parent_ids)
                        for parent_cc in parent_ll:
                            etra = {"user_id":parent_cc.user_id,"username":parent_cc.username}
                            child_list.append(etra)  

                        
                        child_list = json.dumps(child_list)
                        child_list = json.loads(child_list)

                        child_list_for_order = users.objects.filter(parent_id=parent_ids)

                        # for child_order_d in child_list_for_order:
                        #     order_list = orders.objects.filter(~Q(needed="0"), user_id=child_order_d.user_id)
                        #     for order_l in order_list:
                        #         thubnail_url = order_l.image_url

                        #         if order_l.type == "0":
                        #             file = '/static/img/like/'+thubnail_url
                        #             image_path = settings.APP_URL + file
                                    
                        #             order_ddd = orders.objects.filter(id=order_l.id)
                        #             serializer_cosd = orders_data_serializer(order_ddd, many=True)
                        #             child_cosd = serializer_cosd.data
                        #             child_cosd = json.dumps(child_cosd).strip('[]')
                        #             child_cosd = json.loads(child_cosd)
                        #             child_cosd['order_owner'] = "0"
                        #             child_cosd['image_url'] = image_path
                        #             like_orders.append(child_cosd)

                        #         elif order_l.type == "1":
                        #             file = '/static/img/follow/'+thubnail_url
                        #             image_path = settings.APP_URL + file

                        #             order_ddd = orders.objects.filter(id=order_l.id)
                        #             serializer_cosd = orders_data_serializer(order_ddd, many=True)
                        #             child_cosd = serializer_cosd.data
                        #             child_cosd = json.dumps(child_cosd).strip('[]')
                        #             child_cosd = json.loads(child_cosd)
                        #             child_cosd['order_owner'] = "0"
                        #             child_cosd['image_url'] = image_path
                        #             follow_orders.append(child_cosd)


                        main_data = users.objects.filter(user_id=reference_id)
                        serializer_main = users_data_serializer(main_data, many=True)
                        main_data_dix = (serializer_main.data)
                        main_data_dix = json.dumps(main_data_dix).strip('[]')
                        main_data_dix = json.loads(main_data_dix)                        
                        data = {
                            "user_id": parent_pro["user_id"],
                            "username": parent_pro["username"],
                            "parent_id": parent_ids,
                            "total_coins": main_data_dix['total_coins'],
                            "is_referred": main_data_dix['is_referred'],
                            "referral_code": main_data_dix['referral_code'],
                            "child_list": child_list,
                            # "like_orders": like_orders,
                            # "follow_orders": follow_orders
                        }
                        get_pre = {
                            "success": True,
                            "data":data,
                            "message": "User Login Successfully"
                        }

                        return Response(get_pre)

                else:
                    get_pre = {
                        "success": False,
                        "message": "Refernce Account is not valid"
                    }
                    return Response(get_pre)

            else:
                get_pre = {
                    "success": False,
                    "message": "Fromapp not valid"
                }
                return Response(get_pre)
        else:
            get_pre = {
                "success": False,
                "message": "Not valid way"
            }
            return Response(get_pre)

class order_api(APIView):
    def post(self, request):
        order_dd = request.data
        type_bool = False
        userid_bool = False
        needed_bool = False
        imageurl_bool = False
        fromapp_bool = False
        custom_user_id_bool = False

        userid_param = request.data.get('user_id')
        if userid_param is not None:
            if str(order_dd['user_id']).replace(' ','') != "":
                userid_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "user_id is Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "user_id is Required"
            }
            return Response(get_pre)

        type_param = request.data.get('type')
        if type_param is not None:
            if str(order_dd['type']).replace(' ','') != "":
                type_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "type is Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "type is Required"
            }
            return Response(get_pre)

        needed_param = request.data.get('needed')
        if needed_param is not None:
            if str(order_dd['needed']).replace(' ','') != "":
                needed_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "needed is Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "needed is Required"
            }
            return Response(get_pre)

        image_url_param = request.data.get('image_url')
        if image_url_param is not None:
            if str(order_dd['image_url']).replace(' ','') != "":
                imageurl_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "image_url is Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "image_url is Required"
            }
            return Response(get_pre)

        fromapp_param = request.data.get('fromapp')
        if fromapp_param is not None:
            if str(order_dd['fromapp']).replace(' ','') != "":
                fromapp_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "From app is Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "From app is Required"
            }
            return Response(get_pre)


        if type_bool == True and userid_bool == True and needed_bool == True and imageurl_bool == True and fromapp_bool == True:
            if order_dd['fromapp'] == "1":
                
                if users.objects.filter(user_id=order_dd['user_id']).exists():
                    user_id = order_dd['user_id']
                    user_data_d = users.objects.get(user_id=user_id)
                    if user_data_d.parent_id == "0":
                        user_ids = user_data_d.user_id
                        ftoken = user_data_d.ftoken
                    elif user_data_d.parent_id  != "0":
                        user_ids = user_data_d.parent_id
                        parent_user = users.objects.get(user_id=user_data_d.parent_id)
                        ftoken = parent_user.ftoken

                    if user_data_d.status == "0":
                        get_pre = {
                            "success": False,
                            "message": "Your Account is Suspended"
                        }
                        return Response(get_pre)
                    else:
                        if order_dd['type'] == "0":
                            
                            post_id_param = request.data.get('post_id')
                            if post_id_param is not None:
                                if str(order_dd['post_id']).replace(' ','') == "":
                                    get_pre = {
                                        "success": False,
                                        "message": "Post id is Required"
                                    }
                                    return Response(get_pre)
                            else :
                                get_pre = {
                                    "success": False,
                                    "message": "Post id is Required"
                                }
                                return Response(get_pre)

                            short_code_param = request.data.get('short_code')
                            if short_code_param is not None:
                                if str(order_dd['short_code']).replace(' ','') == "":
                                    get_pre = {
                                        "success": False,
                                        "message": "short code is Required"
                                    }
                                    return Response(get_pre)
                            else :
                                get_pre = {
                                    "success": False,
                                    "message": "short code is Required"
                                }
                                return Response(get_pre)


                            # app_data for maintenence check
                            all_data1 = app_data.objects.all()
                            serializer1 = app_data_serializer(all_data1, many=True)
                            app_data_dic = serializer1.data
                            if app_data_dic != []:
                                app_data_dic = json.dumps(serializer1.data).strip('[]')
                                app_data_dic = json.loads(app_data_dic)
                                cca = app_data_dic['maintenence_mode'].split(',')
                                ccb = app_data_dic['payment_method'].split(',')
                                app_data_dic['maintenence_mode'] = cca
                                app_data_dic['payment_method'] = ccb
                            else:
                                get_pre = {
                                    "success": False,
                                    "message": "Server Issue"
                                }
                                return Response(get_pre)
                            # End app_data for maintenence check

                            if 'like' in app_data_dic['maintenence_mode']:
                                spent_like_coin = app_data_dic['spent_like_coin']
                                neededcoinfor_like = int(spent_like_coin) * int(order_dd['needed'])

                                if user_data_d.parent_id != "0":
                                    parent = users.objects.get(user_id=user_data_d.parent_id)
                                    usercoinbalance = int(parent.total_coins)
                                else:
                                    usercoinbalance = int(user_data_d.total_coins)

                                currentusercoinbalance = int(usercoinbalance) - int(neededcoinfor_like)

                                if currentusercoinbalance <= 0:
                                    get_pre = {
                                        "success": False,
                                        "message": "Insufficient Balance"
                                    }
                                    return Response(get_pre)
                                else:
                                    orders_idcheck_bool = False
                                    custom_user_id_param = request.data.get('custom_user_id')
                                    if custom_user_id_param is not None:
                                        if str(order_dd['custom_user_id']).replace(' ','') != "":
                                            if orders.objects.filter(~Q(post_id=""),post_id =order_dd['post_id'], user_id=order_dd['user_id'],custom_user_id=order_dd['custom_user_id'], type=order_dd['type']).exists():
                                                orders_idcheck_bool = True
                                        else:
                                            if orders.objects.filter(~Q(post_id=""),post_id =order_dd['post_id'], user_id=order_dd['user_id'],custom_user_id=order_dd['user_id'], type=order_dd['type']).exists():
                                                orders_idcheck_bool = True
                                    else:
                                        if orders.objects.filter(~Q(post_id=""),post_id =order_dd['post_id'], user_id=order_dd['user_id'],custom_user_id=order_dd['user_id'], type=order_dd['type']).exists():
                                            orders_idcheck_bool = True

                                    if orders_idcheck_bool == True:
                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(order_dd['custom_user_id']).replace(' ','') != "": 
                                                if orders.objects.filter(user_id=order_dd['user_id'], custom_user_id=order_dd['custom_user_id'], type=order_dd['type'], post_id =order_dd['post_id']).exists():
                                                    order = orders.objects.get(user_id=order_dd['user_id'], custom_user_id=order_dd['custom_user_id'], type=order_dd['type'], post_id =order_dd['post_id'])
                                            else:  
                                                if orders.objects.filter(user_id=order_dd['user_id'], custom_user_id=order_dd['user_id'], type=order_dd['type'], post_id =order_dd['post_id']).exists():
                                                    order = orders.objects.get(user_id=order_dd['user_id'], custom_user_id=order_dd['user_id'], type=order_dd['type'], post_id =order_dd['post_id'])
                                        else:  
                                            if orders.objects.filter(user_id=order_dd['user_id'], custom_user_id=order_dd['user_id'], type=order_dd['type'], post_id =order_dd['post_id']).exists():
                                                order = orders.objects.get(user_id=order_dd['user_id'], custom_user_id=order_dd['user_id'], type=order_dd['type'], post_id =order_dd['post_id'])
                                        
                                        total_needed = int(order_dd['needed']) + int(order.needed)
                                        order.needed = str(total_needed)
                                        # userdata_rc.is_referred = '1'
                                        order.save()

                                        users_change = users.objects.get(user_id=user_ids)
                                        users_change.total_coins = currentusercoinbalance
                                        users_change.save()
                                        
                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(order_dd['custom_user_id']).replace(' ','') != "":
                                                data = {
                                                    "user_id": order_dd['user_id'],
                                                    "custom_user_id": order_dd['custom_user_id'],
                                                    "total_coin": currentusercoinbalance
                                                }
                                                get_pre = {
                                                    "success": True,
                                                    "data": data,
                                                    "message": "Order Placed Successfully "
                                                }
                                                return Response(get_pre)
                                            else:
                                                data = {
                                                    "user_id": order_dd['user_id'],
                                                    "total_coin": currentusercoinbalance
                                                }
                                                get_pre = {
                                                    "success": True,
                                                    "data": data,
                                                    "message": "Order Placed Successfully"
                                                }
                                                return Response(get_pre)
                                        else:
                                            data = {
                                                "user_id": order_dd['user_id'],
                                                "total_coin": currentusercoinbalance
                                            }
                                            get_pre = {
                                                "success": True,
                                                "data": data,
                                                "message": "Order Placed Successfully"
                                            }
                                            return Response(get_pre)
                                    else:
                                       
                                        # image_unique_id = str(uuid.uuid4())
                                        filename, file_extension = os.path.splitext(order_dd['image_url'])

                                        # image_file = order_dd['post_id'] + "_like_order" + file_extension
                                        image_file = order_dd['post_id'] + ".jpeg"

                                        file = base_url + '/static/img/like/'+ image_file
                                        # file =  'static/img/like/'+ image_file

                                        try:
                                            urllib.request.urlretrieve(order_dd['image_url'], file)
                                        except:
                                            pass

                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(order_dd['custom_user_id']).replace(' ','') != "":
                                                if order_dd['custom_user_id'] != "0":
                                                    order_cr = orders.objects.create(user_id=order_dd['user_id'], type=order_dd['type'], post_id=order_dd['post_id'], fromapp=order_dd['fromapp'], custom_user_id=order_dd['custom_user_id'], needed=order_dd['needed'], short_code=order_dd['short_code'], image_url=image_file)
                                                else:
                                                    order_cr = orders.objects.create(user_id=order_dd['user_id'], type=order_dd['type'], post_id=order_dd['post_id'], fromapp=order_dd['fromapp'], custom_user_id=order_dd['user_id'], needed=order_dd['needed'], short_code=order_dd['short_code'], image_url=image_file)
                                            else:
                                                order_cr = orders.objects.create(user_id=order_dd['user_id'], type=order_dd['type'], post_id=order_dd['post_id'], fromapp=order_dd['fromapp'], custom_user_id=order_dd['user_id'], needed=order_dd['needed'], short_code=order_dd['short_code'], image_url=image_file)
                                        else:
                                            order_cr = orders.objects.create(user_id=order_dd['user_id'], type=order_dd['type'], post_id=order_dd['post_id'], fromapp=order_dd['fromapp'], custom_user_id=order_dd['user_id'], needed=order_dd['needed'], short_code=order_dd['short_code'], image_url=image_file)
                                            

                                        # child_accounts = users.objects.filter(parent_id=user_ids).values("user_id")
                                        # child_accounts.user_id = user_ids

                                        # custom_user_id_param = request.data.get('custom_user_id')
                                        # if custom_user_id_param is not None:
                                        #     if str(order_dd['custom_user_id']).replace(' ','') != "":
                                        #         child_accounts.user_id = order_dd['custom_user_id']


                                        # for child_ids_al in child_accounts:
                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(order_dd['custom_user_id']).replace(' ','') != "":
                                                already_likefollows = already_like_follow.objects.create(type=order_dd['type'], user_id=order_dd['user_id'], custom_user_id=order_dd['custom_user_id'],post_id=order_dd['post_id'], al_user_id=order_dd['user_id'])
                                                already_likefollows = already_like_follow.objects.create(type=order_dd['type'], user_id=order_dd['user_id'], custom_user_id=order_dd['custom_user_id'],post_id=order_dd['post_id'], al_user_id=order_dd['custom_user_id'])
                                            else:
                                                already_likefollows = already_like_follow.objects.create(type=order_dd['type'], user_id=order_dd['user_id'], custom_user_id=order_dd['user_id'],post_id=order_dd['post_id'], al_user_id=order_dd['user_id'])
                                        else:
                                            already_likefollows = already_like_follow.objects.create(type=order_dd['type'], user_id=order_dd['user_id'], custom_user_id=order_dd['user_id'],post_id=order_dd['post_id'], al_user_id=order_dd['user_id'])

                                        user_dda = users.objects.get(user_id=user_ids)
                                        user_dda.total_coins = currentusercoinbalance
                                        user_dda.save()

                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(order_dd['custom_user_id']).replace(' ','') != "":
                                                data = {
                                                    "user_id": order_dd['user_id'],
                                                    "custom_user_id": order_dd['custom_user_id'],
                                                    "total_coin": currentusercoinbalance
                                                }
                                                get_pre = {
                                                    "success": True,
                                                    "data": data,
                                                    "message": "Order Placed Successfully "
                                                }
                                                return Response(get_pre)
                                            else:
                                                data = {
                                                    "user_id": order_dd['user_id'],
                                                    "total_coin": currentusercoinbalance
                                                }
                                                get_pre = {
                                                    "success": True,
                                                    "data": data,
                                                    "message": "Order Placed Successfully"
                                                }
                                                return Response(get_pre)
                                        else:
                                            data = {
                                                "user_id": order_dd['user_id'],
                                                "total_coin": currentusercoinbalance
                                            }
                                            get_pre = {
                                                "success": True,
                                                "data": data,
                                                "message": "Order Placed Successfully"
                                            }
                                            return Response(get_pre)
                            else:
                                get_pre = {
                                    "success": False,
                                    "message": "Like Currently in Maintenence Mode"
                                }
                                return Response(get_pre)

                        elif order_dd['type'] == "1":
                            
                            username_param = request.data.get('username')
                            if username_param is not None:
                                if str(order_dd['username']).replace(' ','') == "":
                                    get_pre = {
                                        "success": False,
                                        "message": "user name is Required"
                                    }
                                    return Response(get_pre)
                            else :
                                get_pre = {
                                    "success": False,
                                    "message": "user name is Required"
                                }
                                return Response(get_pre)

                            
                            # app_data for maintenence check
                            all_data1 = app_data.objects.all()
                            serializer1 = app_data_serializer(all_data1, many=True)
                            app_data_dic = serializer1.data
                            if app_data_dic != []:
                                app_data_dic = json.dumps(serializer1.data).strip('[]')
                                app_data_dic = json.loads(app_data_dic)
                                cca = str(app_data_dic['maintenence_mode']).split(',')
                                ccb = str(app_data_dic['payment_method']).split(',')
                                app_data_dic['maintenence_mode'] = cca
                                app_data_dic['payment_method'] = ccb
                            else:
                                get_pre = {
                                    "success": False,
                                    "message": "Server Issue"
                                }
                                return Response(get_pre)
                            # End app_data for maintenence check

                            if 'follow' in app_data_dic['maintenence_mode']:
                                spent_follow_coin = app_data_dic['spent_follow_coin']
                                neededcoinfor_follow = int(spent_follow_coin)*int(order_dd['needed'])


                                if user_data_d.parent_id != "0":
                                    parent = users.objects.get(user_id=user_data_d.parent_id)
                                    usercoinbalance = parent.total_coins
                                else:
                                    usercoinbalance = user_data_d.total_coins
                                currentusercoinbalance = int(usercoinbalance) - int(neededcoinfor_follow)

                                if currentusercoinbalance <= 0:
                                    get_pre = {
                                        "success": False,
                                        "message": "Insufficient Balance"
                                    }
                                    return Response(get_pre)
                                else:
                                    orders_idcheck_bool = False
                                    custom_user_id_param = request.data.get('custom_user_id')
                                    if custom_user_id_param is not None:
                                        if str(order_dd['custom_user_id']).replace(' ','') != "":
                                            if orders.objects.filter(custom_user_id=order_dd['custom_user_id'], type='1', user_id=order_dd['user_id']).exists():
                                                orders_ad = orders.objects.get(custom_user_id=order_dd['custom_user_id'], type='1', user_id=order_dd['user_id'])
                                                orders_idcheck_bool = True
                                        else:
                                            if orders.objects.filter(user_id=order_dd['user_id'], type='1', custom_user_id=order_dd['user_id']).exists():
                                                orders_ad = orders.objects.get(user_id=order_dd['user_id'], type='1', custom_user_id=order_dd['user_id'])
                                                orders_idcheck_bool = True
                                    else:
                                        if orders.objects.filter(user_id=order_dd['user_id'], type='1', custom_user_id=order_dd['user_id']).exists():
                                            orders_ad = orders.objects.get(user_id=order_dd['user_id'], type='1', custom_user_id=order_dd['user_id'])
                                            orders_idcheck_bool = True

                                    if orders_idcheck_bool == True:
                                        total_needed = int(order_dd['needed']) + int(orders_ad.needed)
                                        
                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(order_dd['custom_user_id']).replace(' ','') != "":
                                                if orders.objects.filter(user_id=order_dd['user_id'], type='1', custom_user_id=order_dd['custom_user_id']).exists:
                                                    orders_ad = orders.objects.get(user_id=order_dd['user_id'], type='1', custom_user_id=order_dd['custom_user_id'])
                                                    orders_ad.needed = str(total_needed)
                                                    orders_ad.save()
                                            else:
                                                if  orders.objects.filter(user_id=order_dd['user_id'], type='1', custom_user_id=order_dd['user_id']).exists():
                                                    orders_ad = orders.objects.get(user_id=order_dd['user_id'], type='1', custom_user_id=order_dd['user_id'])
                                                    orders_ad.needed = str(total_needed)
                                                    orders_ad.save()
                                        else:
                                            if  orders.objects.filter(user_id=order_dd['user_id'], type='1', custom_user_id=order_dd['user_id']).exists():
                                                orders_ad = orders.objects.get(user_id=order_dd['user_id'], type='1', custom_user_id=order_dd['user_id'])
                                                orders_ad.needed = str(total_needed)
                                                orders_ad.save()
                                        
                                        user_aad = users.objects.get(user_id=user_ids)
                                        user_aad.total_coins = str(currentusercoinbalance)
                                        user_aad.save()

                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(order_dd['custom_user_id']).replace(' ','') != "":
                                                data = {
                                                    "user_id": user_ids,
                                                    "custom_user_id": order_dd['custom_user_id'],
                                                    "total_coin": currentusercoinbalance
                                                }
                                                get_pre = {
                                                    "success": True,
                                                    "data": data,
                                                    "message": "Order Placed Successfully "
                                                }
                                                return Response(get_pre)
                                            else:
                                                data = {
                                                    "user_id": order_dd['user_id'],
                                                    "total_coin": currentusercoinbalance
                                                }
                                                get_pre = {
                                                    "success": True,
                                                    "data": data,
                                                    "message": "Order Placed Successfully"
                                                }
                                                return Response(get_pre)
                                        else:
                                            data = {
                                                "user_id": order_dd['user_id'],
                                                "total_coin": currentusercoinbalance
                                            }
                                            get_pre = {
                                                "success": True,
                                                "data": data,
                                                "message": "Order Placed Successfully"
                                            }
                                            return Response(get_pre)
                                    else:
                                        
                                        image_unique_id = str(uuid.uuid4())
                                        filename, file_extension = os.path.splitext(order_dd['image_url'])

                                        # image_file = image_unique_id + "_follow_order" + file_extension
                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(order_dd['custom_user_id']).replace(' ','') != "":
                                                image_file = order_dd['custom_user_id'] + ".jpeg"
                                            else:
                                                image_file = order_dd['user_id'] + ".jpeg"
                                        else:
                                            image_file = order_dd['user_id'] + ".jpeg"


                                        file = base_url + '/static/img/follow/'+ image_file
                                        
                                        try:
                                            urllib.request.urlretrieve(order_dd['image_url'], file)
                                        except:
                                            pass

                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(order_dd['custom_user_id']).replace(' ','') != "":
                                                order_cr = orders.objects.create(user_id=order_dd['user_id'], type=order_dd['type'], username=order_dd['username'], needed=order_dd['needed'], fromapp=order_dd['fromapp'], custom_user_id=order_dd['custom_user_id'], image_url=image_file)
                                            else:
                                                order_cr = orders.objects.create(user_id=order_dd['user_id'], type=order_dd['type'], username=order_dd['username'], needed=order_dd['needed'], fromapp=order_dd['fromapp'], custom_user_id=order_dd['user_id'], image_url=image_file)
                                        else:
                                            order_cr = orders.objects.create(user_id=order_dd['user_id'], type=order_dd['type'], username=order_dd['username'], needed=order_dd['needed'], fromapp=order_dd['fromapp'], custom_user_id=order_dd['user_id'], image_url=image_file)

                                        # child_accounts = users.objects.filter(parent_id=user_ids).values('user_id')

                                        # child_accounts.user_id = user_ids

                                        # custom_user_id_param = request.data.get('custom_user_id')
                                        # if custom_user_id_param is not None:
                                        #     if str(order_dd['custom_user_id']).replace(' ','') != "":
                                        #         child_accounts.user_id = order_dd['custom_user_id']
                                        
                                        
                                        # for child_ids_al in child_accounts:
                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(order_dd['custom_user_id']).replace(' ','') != "":
                                                already_likefollows = already_like_follow.objects.create(type=order_dd['type'], user_id=order_dd['user_id'], custom_user_id=order_dd['custom_user_id'],al_user_id=order_dd['user_id'])
                                                already_likefollows = already_like_follow.objects.create(type=order_dd['type'], user_id=order_dd['user_id'], custom_user_id=order_dd['custom_user_id'],al_user_id=order_dd['custom_user_id'])
                                            else:
                                                already_likefollows= already_like_follow.objects.create(type=order_dd['type'], user_id=order_dd['user_id'], custom_user_id=order_dd['user_id'], al_user_id=order_dd['user_id'])
                                        else:
                                            already_likefollows= already_like_follow.objects.create(type=order_dd['type'], user_id=order_dd['user_id'], custom_user_id=order_dd['user_id'], al_user_id=order_dd['user_id'])
                                        
                                        user_dda = users.objects.get(user_id=user_ids)
                                        user_dda.total_coins = str(currentusercoinbalance)
                                        user_dda.save()

                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(order_dd['custom_user_id']).replace(' ','') != "":
                                                data = {
                                                    "user_id": order_dd['user_id'],
                                                    "custom_user_id": order_dd['custom_user_id'],
                                                    "total_coin": currentusercoinbalance
                                                }
                                                get_pre = {
                                                    "success": True,
                                                    "data": data,
                                                    "message": "Order Placed Successfully "
                                                }
                                                return Response(get_pre)
                                        else:
                                            data = {
                                                "user_id": order_dd['user_id'],
                                                "total_coin": currentusercoinbalance
                                            }
                                            get_pre = {
                                                "success": True,
                                                "data": data,
                                                "message": "Order Placed Successfully"
                                            }
                                            return Response(get_pre)
                            else:
                                get_pre = {
                                    "success": False,
                                    "message": "Follow Currently in Maitenence Mode"
                                }
                                return Response(get_pre)

                        else:
                            get_pre = {
                                "success": False,
                                "message": "Type Is Required"
                            }
                            return Response(get_pre)
                else:
                    get_pre = {
                            "success": False,
                            "message": "requested User is IN valid"
                    }
                    return Response(get_pre)

            else:
                get_pre = {
                    "success": False,
                    "message": "Not valid Way"
                }
                return Response(get_pre)
        else:
            get_pre = {
                "success": False,
                "message": "Not valid Way"
            }
            return Response(get_pre)

class refferalcode(APIView):
    def post(self, request):

        refferal_cd = request.data
        userid_bool = False
        refferalCode_bool = False

        userid_param = request.data.get('user_id')
        if userid_param is not None:
            if str(refferal_cd['user_id']).replace(' ','') != "":
                userid_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "user_id Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "user_id Required"
            }
            return Response(get_pre)

        refferal_code_param = request.data.get('refferal_code')
        if refferal_code_param is not None:
            if str(refferal_cd['refferal_code']).replace(' ','') != "":
                refferalCode_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "refferal_code Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "refferal_code Required"
            }
            return Response(get_pre)



        if userid_bool == True and refferalCode_bool == True:
            if users.objects.filter(user_id=refferal_cd['user_id']).exists():
                userdata_rc = users.objects.get(user_id=refferal_cd['user_id'])
            else:
                get_pre = {
                    "success": False,
                    "message": "user not Valid"
                }
                return Response(get_pre)

            if userdata_rc.status:

                if userdata_rc.parent_id == '0':
                    if userdata_rc.is_referred == '1':
                        get_pre = {
                            "success": False,
                            "message": "You are already reffered User"
                        }
                        return Response(get_pre)
                else:
                    parentdata_rc = users.objects.get(user_id=userdata_rc.parent_id)
                    if parentdata_rc.is_referred == '1':
                        get_pre = {
                            "success": False,
                            "message": "You are parent is already reffered User"
                        }
                        return Response(get_pre)

                if userdata_rc.status == '0':
                    get_pre = {
                        "success": False,
                        "message": "Your Account is Suspended"
                    }
                    return Response(get_pre)
                else:

                    if users.objects.filter(referral_code=refferal_cd['refferal_code'], parent_id="0").exists():
                        check_refferal_cd = users.objects.get(referral_code=refferal_cd['refferal_code'], parent_id="0")
                        requested_user_refferal_code  = []
                        if userdata_rc.parent_id == '0':
                            requested_user_refferal_code.append(userdata_rc.referral_code)
                            childlist_referral = users.objects.filter(parent_id=userdata_rc.user_id)
                            for child_rr in childlist_referral:
                                requested_user_refferal_code.append(child_rr.referral_code)
                            
                        else:
                            parentdata_rc = users.objects.get(user_id=userdata_rc.parent_id)
                            requested_user_refferal_code.append(parentdata_rc.referral_code)
                            childlist_referral = users.objects.filter(parent_id=parentdata_rc.user_id)
                            for child_rr in childlist_referral:
                                requested_user_refferal_code.append(child_rr.referral_code)

                        if refferal_cd['refferal_code'] not in requested_user_refferal_code:

                            # app_data for maintenence check
                            all_data1 = app_data.objects.all()
                            serializer1 = app_data_serializer(all_data1, many=True)
                            app_data_dic = serializer1.data

                            if app_data_dic != []:
                                app_data_dic = json.dumps(serializer1.data).strip('[]')
                                app_data_dic = json.loads(app_data_dic)
                                cca = app_data_dic['maintenence_mode'].split(',')
                                ccb = app_data_dic['payment_method'].split(',')
                                app_data_dic['maintenence_mode'] = cca
                                app_data_dic['payment_method'] = ccb
                            else:
                                get_pre = {
                                    "success": False,
                                    "message": "Server Issue"
                                }
                                return Response(get_pre)
                            # End app_data for maintenence check

                            if userdata_rc.parent_id == '0':
                                total_coins = userdata_rc.total_coins
                                finalCoinAmount = int(total_coins) + int(app_data_dic['referrel_coin'])
                                userdata_rc.total_coins = str(finalCoinAmount)
                                userdata_rc.is_referred = '1'
                                userdata_rc.save()
                                childlist_referral = users.objects.filter(parent_id=userdata_rc.user_id)
                                for child_rr in childlist_referral:
                                    child_rr.is_referred = '1'
                                    child_rr.save()
                            else:
                                parentAccount = users.objects.get(user_id=userdata_rc.parent_id)
                                total_coins = parentAccount.total_coins
                                finalCoinAmount = int(total_coins) + int(app_data_dic['referrel_coin'])
                                parentAccount.total_coins = str(finalCoinAmount)
                                parentAccount.is_referred = '1'
                                parentAccount.save()

                                childlist_referral = users.objects.filter(parent_id=parentAccount.user_id)
                                for child_rr in childlist_referral:
                                    child_rr.is_referred = '1'
                                    child_rr.save()

                            refferal_coinuser = int(check_refferal_cd.total_coins) + int(app_data_dic['referrel_coin'])
                            reffered_user_rc = users.objects.get(user_id=check_refferal_cd.user_id)
                            reffered_user_rc.total_coins = str(refferal_coinuser)
                            userdata_rc.is_referred = '1'
                            reffered_user_rc.save()

                            data = {
                                "user_id": refferal_cd['user_id'],
                                "total_coins": finalCoinAmount
                            }
                            get_pre = {
                                "success": True,
                                "data": data,
                                "message": "Reffered Sucessfully"
                            }
                            return Response(get_pre)

                        else:
                            get_pre = {
                                "success": False,
                                "message": "You can't use your this Refferal code"
                            }
                            return Response(get_pre)

                    else:
                        get_pre = {
                            "success": False,
                            "message": "Refferal code is invalid"
                        }
                        return Response(get_pre)

            else:
                get_pre = {
                    "success": False,
                    "message": "Refferal code is invalid"
                }
                return Response(get_pre)

        else:
            get_pre = {
                "success": False,
                "message": "not valid data not get"
            }
            return Response(get_pre)

class purchasecoin(APIView):
    def post(self, request):
        purchasecoin_jsondata = request.data
        purchase_userid_bool = False
        purchase_fromad_bool = False
        # purchase_paymentmethod_bool = False
        
        userid_param = request.data.get('user_id')
        if userid_param is not None:
            if str(purchasecoin_jsondata['user_id']).replace(' ','') != "":
                purchase_userid_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "user_id is Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "user_id is Required"
            }
            return Response(get_pre)
        
        from_ad_param = request.data.get('from_ad')
        if from_ad_param is not None:
            if str(purchasecoin_jsondata['from_ad']).replace(' ','') != "":
                purchase_fromad_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "From_ad is Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "From_ad is Required"
            }
            return Response(get_pre)
        

        if purchase_userid_bool == True and purchase_fromad_bool == True:
            if users.objects.filter(user_id=purchasecoin_jsondata['user_id']).exists():
                purchase_user = users.objects.get(user_id=purchasecoin_jsondata['user_id'])
                if purchase_user.status == "0":
                    get_pre = {
                        "success": False,
                        "message": "Your Account is Suspended"
                    }
                    return Response(get_pre)
                else:
                    if purchasecoin_jsondata['from_ad'] == "true" or purchasecoin_jsondata['from_ad'] == "True":
                        # app_data for maintenence check
                        all_data1 = app_data.objects.all()
                        serializer1 = app_dataother_serializer(all_data1, many=True)
                        app_data_dic = serializer1.data
                        if app_data_dic != []:
                            app_data_dic = json.dumps(serializer1.data).strip('[]')
                            app_data_dic = json.loads(app_data_dic)
                            cca = app_data_dic['maintenence_mode'].split(',')
                            ccb = app_data_dic['payment_method'].split(',')
                            app_data_dic['maintenence_mode'] = cca
                            app_data_dic['payment_method'] = ccb
                        else:
                            get_pre = {
                                "success": False,
                                "message": "Server Issue"
                            }
                            return Response(get_pre)
                        # End app_data for maintenence check
                        
                        if purchase_user.parent_id == "0":
                            purchase_userid = purchase_user.user_id
                            add_total_coin = int(purchase_user.total_coins) + app_data_dic['from_add_coin']
                            purchase_user.total_coins = str(add_total_coin)
                            purchase_user.save()
                        else:
                            parentuser = users.objects.get(user_id=purchase_user.parent_id)
                            add_total_coin = int(parentuser.total_coins )+ app_data_dic['from_add_coin']
                            parentuser.total_coins = str(add_total_coin)
                            parentuser.save()

                        data = {
                            "user_id": purchasecoin_jsondata['user_id'],
                            "total_coins": add_total_coin
                        }
                        get_pre = {
                            "success": True,
                            "data": data,
                            "message": "Coin Added Successfully"
                        }
                        return Response(get_pre)

                    elif purchasecoin_jsondata['from_ad'] == "false" or purchasecoin_jsondata['from_ad'] == "False" :

                        payment_method_param = request.data.get('payment_method')
                        if payment_method_param is not None:
                            if str(purchasecoin_jsondata['payment_method']).replace(' ','') != "":
                                purchase_paymentmethod_bool = True
                            else :
                                get_pre = {
                                    "success": False,
                                    "message": "payment_method is Required"
                                }
                                return Response(get_pre)
                        else :
                            get_pre = {
                                "success": False,
                                "message": "payment_method is Required"
                            }
                            return Response(get_pre)

                        purchased_coin_param = request.data.get('purchased_coin')
                        if purchased_coin_param is not None:
                            if str(purchasecoin_jsondata['purchased_coin']).replace(' ','') != "":
                                purchased_coin_bool = True
                            else :
                                get_pre = {
                                    "success": False,
                                    "message": "purchased_coin is Required"
                                }
                                return Response(get_pre)
                        else :
                            get_pre = {
                                "success": False,
                                "message": "purchased_coin is Required"
                            }
                            return Response(get_pre)

                        original_coin_param = request.data.get('original_coin')
                        if original_coin_param is not None:
                            if str(purchasecoin_jsondata['original_coin']).replace(' ','') != "":
                                original_coin_bool = True
                            else :
                                get_pre = {
                                    "success": False,
                                    "message": "original_coin is Required"
                                }
                                return Response(get_pre)
                        else :
                            get_pre = {
                                "success": False,
                                "message": "original_coin is Required"
                            }
                            return Response(get_pre)

                        purchased_coin = purchasecoin_jsondata['purchased_coin']
                        original_coin = purchasecoin_jsondata['original_coin']

                        # app_data for maintenence check
                        all_data1 = app_data.objects.all()
                        serializer1 = app_data_serializer(all_data1, many=True)
                        app_data_dic = serializer1.data
                        if app_data_dic != []:
                            app_data_dic = json.dumps(serializer1.data).strip('[]')
                            app_data_dic = json.loads(app_data_dic)
                            cca = app_data_dic['maintenence_mode'].split(',')
                            ccb = app_data_dic['payment_method'].split(',')
                            app_data_dic['maintenence_mode'] = cca
                            app_data_dic['payment_method'] = ccb
                        else:
                            get_pre = {
                                "success": False,
                                "message": "Server Issue"
                            }
                            return Response(get_pre)
                        # End app_data for maintenence check
                        if coin_details.objects.filter(quantity=original_coin).exists():
                            coinDetail = coin_details.objects.get(quantity=original_coin)
                        else:
                            get_pre = {
                                "success": False,
                                "message": "Original Coin Not Same!"
                            }
                            return Response(get_pre)

                        if app_data_dic['offer'] == '1':
                            discountCoins = int(original_coin) * int(app_data_dic['offer_percentage'])/100
                            discountTotalCoins = int(discountCoins) + int(original_coin)
                            if int(discountTotalCoins) != int(purchased_coin):
                                get_pre = {
                                    "success": False,
                                    "message": "Coin Not Same!"
                                }
                                return Response(get_pre)

                        elif app_data_dic['offer'] == '0':
                            discountCoins = int(original_coin)*10/100
                            discountTotalCoins = int(discountCoins) + int(original_coin)
                            if int(discountTotalCoins) != int(purchased_coin):
                                get_pre = {
                                    "success": False,
                                    "message": "Coin Not Same!"
                                }
                                return Response(get_pre)
                        else:
                            get_pre = {
                                "success": False,
                                "message": "Offer Is Not Valid!"
                            }
                            return Response(get_pre)

                        if purchasecoin_jsondata['payment_method'] == '0':
                            purchase_transactionid_bool = False
                            purchase_purchasedcoin_bool = False

                            response_param = request.data.get('response')
                            if response_param is not None:
                                if "id" in response_param  and "create_time" in response_param:

                                    if str(purchasecoin_jsondata['response']['id']).replace(' ','') != "" and str(purchasecoin_jsondata['response']['create_time']).replace(' ','') != "" :
                                        purchase_transactionid_bool = True
                                    else:
                                        get_pre = {
                                            "success": False,
                                            "message": "Response Field All Arguments Is Required"
                                        }
                                        return Response(get_pre)
                                else:
                                    get_pre = {
                                        "success": False,
                                        "message": "Response Field All Arguments Is Required"
                                    }
                                    return Response(get_pre)
                            else:
                                get_pre = {
                                    "success": False,
                                    "message": "Response Field All Arguments Is Required"
                                }
                                return Response(get_pre)
                            


                            purchased_coin_param = request.data.get('purchased_coin')
                            if purchased_coin_param is not None:
                                if str(purchasecoin_jsondata['purchased_coin']).replace(' ','') != "":
                                    purchase_purchasedcoin_bool = True
                                else:
                                    get_pre = {
                                        "success": False,
                                        "message": "purchased_coin is Required"
                                    }
                                    return Response(get_pre)
                            else:
                                get_pre = {
                                    "success": False,
                                    "message": "purchased_coin is Required"
                                }
                                return Response(get_pre)

                            amount = float(coinDetail.other_rate)
                            transaction_id = purchasecoin_jsondata['response']['id']
                            payment_times = purchasecoin_jsondata['response']['create_time']
                            country_code = purchasecoin_jsondata['country_code']

                            if purchase_coins.objects.filter(payment_id=transaction_id).exists():
                                get_pre = {
                                    "success": False,
                                    "message": "Not valid request"
                                }
                                return Response(get_pre)

                            if purchase_transactionid_bool == True and purchase_purchasedcoin_bool == True:
                                response_param = request.data.get('response')
                                if response_param is not None:
                                    if "state" in response_param:
                                        purchase_coin_save = purchase_coins.objects.create(user_id=purchasecoin_jsondata['user_id'], payment_id=transaction_id, purchased_coin=purchased_coin, amount=amount, payment_state=purchasecoin_jsondata['response']['state'], payment_time=str(payment_times), country_code=country_code, payment_method=purchasecoin_jsondata['payment_method'])
                                    else:
                                        purchase_coin_save = purchase_coins.objects.create(user_id=purchasecoin_jsondata['user_id'], payment_id=transaction_id, purchased_coin=purchased_coin, amount=amount, payment_time=str(payment_times), country_code=country_code,  payment_method=purchasecoin_jsondata['payment_method'])

                        elif purchasecoin_jsondata['payment_method'] == '1':
                            amount = float(coinDetail.indian_rate)
                            purchase_tcid_bool = False

                            transaction_id_param = request.data.get('transaction_id')
                            if transaction_id_param is not None:
                                if str(purchasecoin_jsondata['transaction_id']).replace(' ','') != "":
                                    purchase_tcid_bool = True
                                else:
                                    get_pre = {
                                        "success": False,
                                        "message": "transaction_id is Required"
                                    }
                                    return Response(get_pre)
                            else:
                                get_pre = {
                                    "success": False,
                                    "message": "transaction_id is Required"
                                }
                                return Response(get_pre)
                            
                            if purchase_coins.objects.filter(transaction_id=purchasecoin_jsondata['transaction_id']).exists():
                                get_pre = {
                                    "success": False,
                                    "message": "Not valid request"
                                }
                                return Response(get_pre)

                            if purchase_tcid_bool == True:
                                purchase_coin_save = purchase_coins.objects.create(user_id=purchasecoin_jsondata['user_id'], purchased_coin=purchased_coin, payment_time=datetime.datetime.now(), payment_method=purchasecoin_jsondata['payment_method'],transaction_id=purchasecoin_jsondata['transaction_id'])
                        else:
                            get_pre = {
                                "success": False,
                                "message": "payment_method not valid"
                            }
                            return Response(get_pre)
                       
                        if purchase_user.parent_id == '0':
                            total_coins = int(purchase_user.total_coins) + int(purchased_coin)
                            purchase_user.total_coins = str(total_coins)
                            purchase_user.save()
                        else:
                            parentuser_to = users.objects.get(user_id=purchase_user.parent_id)
                            total_coins = int(parentuser_to.total_coins) + int(purchased_coin)
                            parentuser_to.total_coins = str(total_coins)
                            parentuser_to.save()
                        
                        total_coins = int(math.ceil(total_coins))

                        data = {
                            "user_id": purchasecoin_jsondata['user_id'],
                            "total_coins": total_coins
                        }
                        get_pre = {
                            "success": True,
                            "data": data,
                            "message": "Coin Added Successfully"
                        }
                        return Response(get_pre)
                    
                    else:
                        get_pre = {
                            "success": False,
                            "message": "check your details!"
                        }
                        return Response(get_pre)

            else:
                get_pre = {
                    "success": False,
                    "message": "Requested Account is not found!"
                }
                return Response(get_pre)

        else:
            get_pre = {
                "success": False,
                "message": "Not valid data"
            }
            return Response(get_pre)

class fetchpost_api(APIView):
    def post(self, request):
        fetchpost_dd = request.data

        userid_bool = False

        userid_param = request.data.get('user_id')
        if userid_param is not None:
            if str(fetchpost_dd['user_id']).replace(' ','') != "":
                userid_bool = True
            else:
                get_pre = {
                    "success": False,
                    "message": "user_id is Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "user_id is Required"
            }
            return Response(get_pre)


        if userid_bool == True:
              
            if users.objects.filter(~Q(status=""),user_id=fetchpost_dd['user_id']).exists():
                user = users.objects.get(user_id=fetchpost_dd['user_id'])

                if user.status=="0":       
                    get_pre ={
                        "success" : False,
                        "message" : "Your Account is Suspended"
                    }
                    return Response(get_pre)        
                else:
                    alreadylike_bool = False
                    ownerid_bool = False
                    type_bool = False
                    post_id_bool = False

                    owner_id_param = request.data.get('owner_id')
                    if owner_id_param is not None:
                        if str(fetchpost_dd['owner_id']).replace(' ','') != "":
                            ownerid_bool = True


                    type_param = request.data.get('type')
                    if type_param is not None:
                        if str(fetchpost_dd['type']).replace(' ','') != "":
                            type_bool = True
                            if fetchpost_dd["type"] == "0":
                                post_id_param = request.data.get('post_id')
                                if post_id_param is not None:
                                    if str(fetchpost_dd['post_id']).replace(' ','') != "":
                                        post_id_bool = True  
                                    else:
                                        get_pre = {
                                            "success": False,
                                            "message": "post_id is Required"
                                        }
                                        return Response(get_pre)
                                else :
                                    get_pre = {
                                        "success": False,
                                        "message": "post_id is Required"
                                    }
                                    return Response(get_pre)


                            elif fetchpost_dd["type"] == "1":

                                username_param = request.data.get('username')
                                if username_param is not None:
                                    if str(fetchpost_dd['username']).replace(' ','') == "":
                                        get_pre = {
                                            "success": False,
                                            "message": "username is Required"
                                        }
                                        return Response(get_pre)
                                else :
                                    get_pre = {
                                        "success": False,
                                        "message": "username is Required"
                                    }
                                    return Response(get_pre)

                            else:
                                get_pre ={
                                    "success" : False,
                                    "message" : "type is not valid"
                                }
                                return Response(get_pre)
   

                    already_like_param = request.data.get('already_like')
                    if already_like_param is not None:
                        if str(fetchpost_dd['already_like']).replace(' ','') != "":
                            if fetchpost_dd['already_like'] == "true" or fetchpost_dd['already_like'] == "True":
                                alreadylike_bool = True


                    if user.parent_id == "0":
                        total_coin = user.total_coins
                    elif user.parent_id != "0":
                        parentAccount = users.objects.get(user_id=user.parent_id)
                        total_coin = parentAccount.total_coins
                     
                    
                    if alreadylike_bool == True and ownerid_bool == True and type_bool == True:   
                        if fetchpost_dd["type"] == "0":
                            if orders.objects.filter(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"], user_id=fetchpost_dd["owner_id"]).exists():
                                order = orders.objects.get(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"],user_id=fetchpost_dd["owner_id"])
                            else:
                                get_pre ={
                                    "success" : False,
                                    "message" : "Please check your details"
                                }
                                return Response(get_pre)

                        elif fetchpost_dd["type"] == "1":

                            custom_user_id_param = request.data.get('custom_user_id')
                            if custom_user_id_param is not None:
                                if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                    if orders.objects.filter(user_id=fetchpost_dd["owner_id"],custom_user_id=fetchpost_dd["custom_user_id"], type=fetchpost_dd["type"]).exists():
                                        order = orders.objects.get(user_id=fetchpost_dd["owner_id"],custom_user_id=fetchpost_dd["custom_user_id"], type=fetchpost_dd["type"])
                                    else:
                                        get_pre ={
                                            "success" : False,
                                            "message" : "Please check your details"
                                        }
                                        return Response(get_pre)
                                else:
                                    if orders.objects.filter(user_id=fetchpost_dd["owner_id"],custom_user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"]).exists:
                                        order = orders.objects.get(user_id=fetchpost_dd["owner_id"],custom_user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"])
                                    else:
                                        get_pre ={
                                            "success" : False,
                                            "message" : "Please check your details"
                                        }
                                        return Response(get_pre)
                            else:
                                if orders.objects.filter(user_id=fetchpost_dd["owner_id"],custom_user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"]).exists:
                                    order = orders.objects.get(user_id=fetchpost_dd["owner_id"],custom_user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"])
                                else:
                                    get_pre ={
                                        "success" : False,
                                        "message" : "Please check your details"
                                    }
                                    return Response(get_pre)

                        else:
                            get_pre ={
                                "success" : False,
                                "message" : "type is not valid"
                            }
                            return Response(get_pre)

                        if order.user_id :

                            if users.objects.filter(user_id=fetchpost_dd["owner_id"]).exists():
                                userowner = users.objects.get(user_id=fetchpost_dd["owner_id"])
                                no_like_log = int(order.no_like_log) + 1
                                if fetchpost_dd["type"] == "0":
                                    order_ud = orders.objects.get(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"])
                                    order_ud.no_like_log = str(no_like_log)
                                    order_ud.save()
                                elif fetchpost_dd["type"] == "1":
                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                                order_udd = orders.objects.get(user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd["custom_user_id"], type=fetchpost_dd["type"])
                                                order_udd.no_like_log = str(no_like_log)
                                                order_udd.save()
                                            else:
                                                order_udd = orders.objects.get(user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"])
                                                order_udd.no_like_log = str(no_like_log)
                                                order_udd.save()
                                        else:
                                            order_udd = orders.objects.get(user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"])
                                            order_udd.no_like_log = str(no_like_log)
                                            order_udd.save()

                                if user.parent_id == "0":
                                    total_coins = int(user.total_coins)
                                else:
                                    parentDetail = users.objects.get(user_id=user.parent_id)
                                    total_coins = parentDetail.total_coins
                                        
                                likefollow_list = []
                                likefollow_listss = []
                                if fetchpost_dd["type"] == "0":
                                    if already_like_follow.objects.filter(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"]).exists():
                                        likefollow_list = list(already_like_follow.objects.filter(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"]).values('al_user_id'))
                                    else:
                                        likefollow_list = []
                                        likefollow_listss = []
                                elif fetchpost_dd["type"] == "1":
                                    
                                    custom_user_id_param = request.data.get('custom_user_id')
                                    if custom_user_id_param is not None:
                                        if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                            likefollow_list = list(already_like_follow.objects.filter(custom_user_id=fetchpost_dd["custom_user_id"], type=fetchpost_dd["type"]).values('al_user_id'))
                                        else:
                                            likefollow_list = list(already_like_follow.objects.filter(custom_user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"]).values('al_user_id'))
                                    else:
                                        likefollow_list = list(already_like_follow.objects.filter(custom_user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"]).values('al_user_id'))

                                   

                                for lef in likefollow_list:
                                    likefollow_listss.append(lef['al_user_id'])

                                if fetchpost_dd["user_id"] not in likefollow_listss:
                                
                                    if fetchpost_dd["type"] == "0":
                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                                already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['custom_user_id'],post_id=fetchpost_dd['post_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                            else:
                                                already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'],post_id=fetchpost_dd['post_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                        else:  
                                            already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'],post_id=fetchpost_dd['post_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                    elif fetchpost_dd["type"] == "1":
                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                                already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['custom_user_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                            else:
                                                already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                        else:
                                            already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                            

                                data = getrandompost(fetchpost_dd["user_id"], total_coins, request)
                                data = json.dumps(data)
                                data = json.loads(data)
                                if data['fetch_post'] == False:
                                    get_pre ={
                                        "success" : False,
                                        "message" : "No post avaialble yet"
                                    }
                                    return Response(get_pre)
                                else:
                                    get_pre ={
                                        "success" : True,
                                        "data":data,
                                        "message" : "Success"
                                    }
                                    return Response(get_pre)
                            else:
                                if order.fromapp == "1":
                                    no_like_log = order.no_like_log + 1
                                    if fetchpost_dd["type"] == "0":
                                        order = orders.objects.filter(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"])
                                        order.no_like_log = no_like_log
                                        order.save()
                                    
                                    elif fetchpost_dd['type'] == "1":
                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                                order = orders.objects.get(user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['custom_user_id'], type=fetchpost_dd["type"])
                                                order.no_like_log = no_like_log
                                                order.save()
                                            else:
                                                order = orders.objects.get(user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'], type=fetchpost_dd["type"])
                                                order.no_like_log = no_like_log
                                                order.save()
                                        else:
                                            order = orders.objects.get(user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'], type=fetchpost_dd["type"])
                                            order.no_like_log = no_like_log
                                            order.save()
                                            
                                        
                                    if user.parent_id == "0":
                                        total_coins = user.total_coins
                                    else:
                                        parentDetail = users.objects.get(user_id=user.parent_id)
                                        total_coins = parentDetail.total_coins
                                    
                                    likefollow_listss = []

                                    if fetchpost_dd["type"] == "0":
                                        likefollow_list = list(already_like_follow.objects.filter(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"]).values('al_user_id'))
                                    elif fetchpost_dd["type"] == "1":
                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                                likefollow_list = list(already_like_follow.objects.filter(custom_user_id=fetchpost_dd["custom_user_id"], type=fetchpost_dd["type"]).values('al_user_id'))
                                            else:
                                                likefollow_list = list(already_like_follow.objects.filter(custom_user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"]).values('al_user_id'))
                                        else:
                                            likefollow_list = list(already_like_follow.objects.filter(custom_user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"]).values('al_user_id'))
                                            
                                    for lef in likefollow_list:
                                        likefollow_listss.append(lef['al_user_id'])

                                    if fetchpost_dd["user_id"] not in likefollow_listss:
                                        if fetchpost_dd["type"] == "0":
                                            custom_user_id_param = request.data.get('custom_user_id')
                                            if custom_user_id_param is not None:
                                                if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                                    already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['custom_user_id'],post_id=fetchpost_dd['post_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                                else:    
                                                    already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'],post_id=fetchpost_dd['post_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                            else:    
                                                already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'],post_id=fetchpost_dd['post_id'], al_user_id=str(fetchpost_dd["user_id"]))

                                        elif fetchpost_dd["type"] == "1":
                                            custom_user_id_param = request.data.get('custom_user_id')
                                            if custom_user_id_param is not None:
                                                if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                                    already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['custom_user_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                                else:
                                                    already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                            else:
                                                already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'], al_user_id=str(fetchpost_dd["user_id"]))

                                    data = getrandompost(fetchpost_dd["user_id"], total_coins, request)
                                    data = json.dumps(data)
                                    data = json.loads(data)
                                    if data['fetch_post'] == False:
                                        get_pre ={
                                            "success" : False,
                                            "message" : "No post avaialble yet"
                                        }
                                        return Response(get_pre)
                                    else:
                                        get_pre ={
                                            "success" : True,
                                            "data":data,
                                            "message" : "Success"
                                        }
                                        return Response(get_pre)
                                else:
                                    data_e = {
                                        "fetch_post" : False
                                    }
                                    get_pre ={
                                        "success" : False,
                                        "data": data_e,
                                        "message" : "Request user is not Valid"
                                    }
                                    return Response(get_pre)
                        else:
                            
                            data_e = {
                                "fetch_post" : False
                            }
                            
                            get_pre ={
                                "success" : False,
                                "data": data_e,
                                "message" : "Post Not Found"
                            }  
                            return Response(get_pre)  

                    elif ownerid_bool == True and type_bool == True:
                        if fetchpost_dd["type"] == "0":
                            custom_user_id_param = request.data.get('custom_user_id')
                            if custom_user_id_param is not None:
                                if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                    if orders.objects.filter(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"], custom_user_id=fetchpost_dd["custom_user_id"], user_id=fetchpost_dd["owner_id"]).exists():
                                        order = orders.objects.get(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"], custom_user_id=fetchpost_dd["custom_user_id"], user_id=fetchpost_dd["owner_id"])
                                    else:
                                        get_pre ={
                                            "success" : False,
                                            "message" : "Please check your details"
                                        }
                                        return Response(get_pre)    
                                else:
                                    if orders.objects.filter(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"], custom_user_id=fetchpost_dd["owner_id"], user_id=fetchpost_dd["owner_id"]).exists():
                                        order = orders.objects.get(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"], custom_user_id=fetchpost_dd["owner_id"], user_id=fetchpost_dd["owner_id"])
                                    else:
                                        get_pre ={
                                            "success" : False,
                                            "message" : "Please check your details"
                                        }
                                        return Response(get_pre)    
                            else:
                                if orders.objects.filter(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"], custom_user_id=fetchpost_dd["owner_id"], user_id=fetchpost_dd["owner_id"]).exists():
                                    order = orders.objects.get(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"], custom_user_id=fetchpost_dd["owner_id"], user_id=fetchpost_dd["owner_id"])
                                else:
                                    get_pre ={
                                        "success" : False,
                                        "message" : "Please check your details"
                                    }
                                    return Response(get_pre)    

                        elif fetchpost_dd["type"] == "1":
                            custom_user_id_param = request.data.get('custom_user_id')
                            if custom_user_id_param is not None:
                                if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                    if orders.objects.filter(custom_user_id=fetchpost_dd["custom_user_id"], user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"]).exists():
                                        order = orders.objects.get(custom_user_id=fetchpost_dd["custom_user_id"], user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"])
                                    else:
                                        get_pre ={
                                            "success" : False,
                                            "message" : "Please check your details"
                                        }
                                        return Response(get_pre)    
                                else:
                                    if orders.objects.filter(custom_user_id=fetchpost_dd["owner_id"], user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"]).exists():
                                        order = orders.objects.get(custom_user_id=fetchpost_dd["owner_id"], user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"])
                                    else:
                                        get_pre ={
                                            "success" : False,
                                            "message" : "Please check your details"
                                        }
                                        return Response(get_pre)    
                            else:
                                if orders.objects.filter(custom_user_id=fetchpost_dd["owner_id"], user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"]).exists():
                                    order = orders.objects.get(custom_user_id=fetchpost_dd["owner_id"], user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"])
                                else:
                                    get_pre ={
                                        "success" : False,
                                        "message" : "Please check your details"
                                    }
                                    return Response(get_pre)    
                        
                        if order == None:
                            custom_user_id_param = request.data.get('custom_user_id')
                            if custom_user_id_param is not None:
                                if fetchpost_dd['owner_id'] == fetchpost_dd['custom_user_id']:
                                    data = getrandompost(fetchpost_dd['user_id'], total_coin, request)
                                    data = json.dumps(data)
                                    data = json.loads(data)
                                    if data['fetch_post'] == False:
                                        get_pre ={
                                            "success" : False,
                                            "message" : "Currently record is not available 1"
                                        }
                                        return Response(get_pre)
                                    else:
                                        get_pre ={
                                            "success" : True,
                                            "data":data,
                                            "message" : "Success"
                                        }
                                        return Response(get_pre)
                                else:
                                    data = getrandompost(fetchpost_dd['user_id'], total_coin, request)
                                    data = json.dumps(data)
                                    data = json.loads(data)
                                    if data['fetch_post'] == False:
                                        get_pre ={
                                            "success" : False,
                                            "message" : "Currently record is not available 2"
                                        }
                                        return Response(get_pre)
                                    else:
                                        get_pre ={
                                            "success" : True,
                                            "data":data,
                                            "message" : "Success"
                                        }
                                        return Response(get_pre)
                            else:
                                data = getrandompost(fetchpost_dd['user_id'], total_coin, request)
                                data = json.dumps(data)
                                data = json.loads(data)
                                if data['fetch_post'] == False:
                                    get_pre ={
                                        "success" : False,
                                        "message" : "Currently record is not available 3"
                                    }
                                    return Response(get_pre)
                                else:
                                    get_pre ={
                                        "success" : True,
                                        "data":data,
                                        "message" : "Success"
                                    }
                                    return Response(get_pre)
                                    
                        # try:
                        #     a =  order.user_id
                        #     order_userid_bool = True
                        # except:
                        #     order_userid_bool = False 

                        # if order_userid_bool == True:

                        if order.user_id:
                            if users.objects.filter(user_id=fetchpost_dd['owner_id']).exists():
                                userowner = users.objects.get(user_id=fetchpost_dd['owner_id'])
                                likefollow_listss = []
                                if fetchpost_dd['type'] == '0':
                                    likefollow_list = list(already_like_follow.objects.filter(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"]).values('al_user_id'))
                                elif fetchpost_dd['type'] == '1':
                                    custom_user_id_param = request.data.get('custom_user_id')
                                    if custom_user_id_param is not None:
                                        if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                            likefollow_list = list(already_like_follow.objects.filter(custom_user_id=fetchpost_dd["custom_user_id"], type=fetchpost_dd["type"]).values('al_user_id'))
                                        else:
                                            likefollow_list = list(already_like_follow.objects.filter(custom_user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"]).values('al_user_id'))
                                    else:
                                        likefollow_list = list(already_like_follow.objects.filter(custom_user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"]).values('al_user_id'))

                                for lef in likefollow_list:
                                    likefollow_listss.append(lef['al_user_id'])
                                if str(fetchpost_dd['user_id']) in likefollow_listss:
                                    data = getrandompost(fetchpost_dd['user_id'], total_coin, request)
                                    data = json.dumps(data)
                                    data = json.loads(data)
                                    if data['fetch_post'] == False:
                                        get_pre ={
                                            "success" : False,
                                            "message" : "Currently record is not available 4"
                                        }
                                        return Response(get_pre)
                                    else:
                                        get_pre ={
                                            "success" : True,
                                            "data":data,
                                            "message" : "Success"
                                        }
                                        return Response(get_pre)
                                else:
                                    
                                    # app_data for maintenence check
                                    all_data1 = app_data.objects.all()
                                    serializer1 = app_data_serializer(all_data1, many=True)
                                    app_data_dic = serializer1.data
                                    if app_data_dic != []:
                                        app_data_dic = json.dumps(serializer1.data).strip('[]')
                                        app_data_dic = json.loads(app_data_dic)
                                        cca = app_data_dic['maintenence_mode'].split(',')
                                        ccb = app_data_dic['payment_method'].split(',')
                                        app_data_dic['maintenence_mode'] = cca
                                        app_data_dic['payment_method'] = ccb
                                    else:
                                        get_pre = {
                                            "success": False,
                                            "message": "Server Issue"
                                        }
                                        return Response(get_pre)
                                    # End app_data for maintenence check

                                    if user.parent_id == "0":
                                        total_coin = user.total_coins
                                    else:
                                        parent = users.objects.get(user_id=user.parent_id)
                                        total_coin = parent.total_coins

                                    if fetchpost_dd['type'] == "0":
                                        earn_like_coin = app_data_dic['earn_like_coin']
                                        getcoin = int(earn_like_coin) + int(total_coin)
                                    elif fetchpost_dd['type'] == "1":
                                        earn_follow_coin = app_data_dic['earn_follow_coin']
                                        getcoin = int(earn_follow_coin) + int(total_coin)

                                    if user.parent_id == "0":
                                        userss = users.objects.get(user_id=user.user_id)
                                        userss.total_coins = str(getcoin)
                                        userss.save()
                                    else:
                                        userss = users.objects.get(user_id=user.parent_id)
                                        userss.total_coins = str(getcoin)
                                        userss.save()

                                    neededrecieved = int(order.recieved) + 1

                                    if fetchpost_dd["type"] == "0":   
                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                                order = orders.objects.get(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"], custom_user_id=fetchpost_dd["custom_user_id"], user_id=fetchpost_dd["owner_id"])
                                                order.recieved = str(neededrecieved) 
                                                order.save()     
                                            else:
                                                order = orders.objects.get(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"], custom_user_id=fetchpost_dd["owner_id"], user_id=fetchpost_dd["owner_id"])
                                                order.recieved = str(neededrecieved) 
                                                order.save()
                                        else:
                                            order = orders.objects.get(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"], custom_user_id=fetchpost_dd["owner_id"], user_id=fetchpost_dd["owner_id"])
                                            order.recieved = str(neededrecieved) 
                                            order.save()

                    
                                    elif fetchpost_dd["type"] == "1":
                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                                order = orders.objects.get(custom_user_id=fetchpost_dd["custom_user_id"], user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"])
                                                order.recieved = str(neededrecieved) 
                                                order.save()
                                            else:
                                                order = orders.objects.get(custom_user_id=fetchpost_dd["owner_id"], user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"])
                                                order.recieved = str(neededrecieved) 
                                                order.save()
                                        else:
                                            order = orders.objects.get(custom_user_id=fetchpost_dd["owner_id"], user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"])
                                            order.recieved = str(neededrecieved) 
                                            order.save()
                                        
                                    if int(order.needed) <= int(neededrecieved):
                                        if fetchpost_dd["type"] == "0":
                                            ordersss = orders.objects.get(id=order.id,post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"], user_id=fetchpost_dd["owner_id"])
                                            ordersss.needed = "0" 
                                            ordersss.recieved = "0" 
                                            ordersss.no_like_log = "0" 
                                            ordersss.save()
                                        elif fetchpost_dd["type"] == "1":
                                            ordersss = orders.objects.get(id=order.id,type=fetchpost_dd["type"], user_id=fetchpost_dd["owner_id"])
                                            ordersss.needed = "0" 
                                            ordersss.recieved = "0" 
                                            ordersss.no_like_log = "0" 
                                            ordersss.save()
                                        

                                        if userowner.parent_id == "0":
                                            try:
                                                a = userowner.ftoken
                                                title = "Instagram Like Follow"
                                                body = {
                                                    "description" : "Your Order Completed Successfully",
                                                }
                                                send_notification(title,body,a)
                                            except:
                                                pass
                                        else:
                                            users_dd = users.objects.get(user_id=userowner.parent_id)
                                            try:
                                                a = users_dd.ftoken
                                                title = "Instagram Like Follow"
                                                body = {
                                                    "description" : "Your Order Completed Successfully",
                                                }
                                                send_notification(title,body,a)
                                            except:
                                                pass


                                    data = getrandompost(fetchpost_dd['user_id'], getcoin, request)
                                    data = json.dumps(data)
                                    data = json.loads(data)
                                    if data['fetch_post'] == False:
                                        get_pre ={
                                            "success" : False,
                                            "message" : "No Post avaialble yet"
                                        }
                                        return Response(get_pre)
                                    else:
                                        get_pre ={
                                            "success" : True,
                                            "data":data,
                                            "message" : "Success"
                                        }
                                        if fetchpost_dd["type"] == "0":
                                            custom_user_id_param = request.data.get('custom_user_id')
                                            if custom_user_id_param is not None:
                                                if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                                    already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['custom_user_id'],post_id=fetchpost_dd['post_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                                else:
                                                    already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'],post_id=fetchpost_dd['post_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                            else:
                                                already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'],post_id=fetchpost_dd['post_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                                
                                        elif fetchpost_dd["type"] == "1":
                                            custom_user_id_param = request.data.get('custom_user_id')
                                            if custom_user_id_param is not None:
                                                if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                                    already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['custom_user_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                                else:
                                                    already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                            else:
                                                already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'], al_user_id=str(fetchpost_dd["user_id"]))

                                        return Response(get_pre)
                            else:
                                userowner = users.objects.get(user_id=fetchpost_dd['owner_id'])
                                if order.fromapp == '1':
                                    
                                    likefollow_listss = []
                                    custom_user_id_param = request.data.get('custom_user_id')
                                    if custom_user_id_param is not None:
                                        if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                            if fetchpost_dd['owner_id'] == fetchpost_dd['custom_user_id']:
                                                user_id = fetchpost_dd['owner_id']
                                            else:
                                                user_id = fetchpost_dd['custom_user_id']
                                        else:
                                            user_id = fetchpost_dd['owner_id']
                                    else:
                                        user_id = fetchpost_dd['owner_id']


                                    if fetchpost_dd['type'] == "0":
                                        likefollow_list = list(already_like_follow.objects.filter(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"]).values('al_user_id'))
                                    elif fetchpost_dd['type'] == "1":
                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                                likefollow_list = list(already_like_follow.objects.filter(custom_user_id=fetchpost_dd["custom_user_id"], type=fetchpost_dd["type"]).values('al_user_id'))
                                            else:
                                                likefollow_list = list(already_like_follow.objects.filter(custom_user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"]).values('al_user_id'))
                                        else:
                                            likefollow_list = list(already_like_follow.objects.filter(custom_user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"]).values('al_user_id'))



                                    for lef in likefollow_list:
                                        likefollow_listss.append(lef['al_user_id'])

                                    if fetchpost_dd['user_id'] in likefollow_listss:
                                        data = getrandompost(fetchpost_dd['user_id'], total_coin, request)
                                        data = json.dumps(data)
                                        data = json.loads(data)
                                        if data['fetch_post'] == False:
                                            get_pre ={
                                                "success" : False,
                                                "message" : "No Post avaialble yet"
                                            }
                                            return Response(get_pre)
                                        else:
                                            get_pre ={
                                                "success" : True,
                                                "data":data,
                                                "message" : "Success"
                                            }   
                                            return Response(get_pre)

                                    
                                    # app_data for maintenence check
                                    all_data1 = app_data.objects.all()
                                    serializer1 = app_data_serializer(all_data1, many=True)
                                    app_data_dic = serializer1.data
                                    if app_data_dic != []:
                                        app_data_dic = json.dumps(serializer1.data).strip('[]')
                                        app_data_dic = json.loads(app_data_dic)
                                        cca = app_data_dic['maintenence_mode'].split(',')
                                        ccb = app_data_dic['payment_method'].split(',')
                                        app_data_dic['maintenence_mode'] = cca
                                        app_data_dic['payment_method'] = ccb
                                    else:
                                        get_pre = {
                                            "success": False,
                                            "message": "Server Issue"
                                        }
                                        return Response(get_pre)
                                    # End app_data for maintenence check  
                                        
                                    if user.parent_id == "0":
                                        total_coin = user.total_coins
                                    else:
                                        parent = users.objects.get(user_id=user.parent_id)
                                        total_coin = parent.total_coins

                                    if fetchpost_dd['type'] == "0":
                                        earn_like_coin = app_data_dic['earn_like_coin']
                                        getcoin = int(earn_like_coin) + int(total_coin)
                                    elif fetchpost_dd['type'] == "1":
                                        earn_follow_coin = app_data_dic['earn_follow_coin']
                                        getcoin = int(earn_follow_coin) + int(total_coin)

                                    if user.parent_id == "0":
                                        userss = users.objects.get(user_id=user.user_id)
                                        userss.total_coins = str(getcoin)
                                        userss.save()
                                    else:
                                        userss = users.objects.get(user_id=user.parent_id)
                                        userss.total_coins = str(getcoin)
                                        userss.save()

                                    
                                    neededrecieved = int(order.recieved) + 1

                                    if fetchpost_dd["type"] == "0":    
                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                                order = orders.objects.get(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"], custom_user_id=fetchpost_dd["custom_user_id"], user_id=fetchpost_dd["owner_id"])
                                                order.recieved = str(neededrecieved) 
                                                order.save()  
                                            else:
                                                order = orders.objects.get(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"], custom_user_id=fetchpost_dd["owner_id"], user_id=fetchpost_dd["owner_id"])
                                                order.recieved = str(neededrecieved) 
                                                order.save()                
                                        else:
                                            order = orders.objects.get(post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"], custom_user_id=fetchpost_dd["owner_id"], user_id=fetchpost_dd["owner_id"])
                                            order.recieved = str(neededrecieved) 
                                            order.save()                

                                    elif fetchpost_dd["type"] == "1":
                                        custom_user_id_param = request.data.get('custom_user_id')
                                        if custom_user_id_param is not None:
                                            if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                                order = orders.objects.get(custom_user_id=fetchpost_dd["custom_user_id"], user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"])
                                                order.recieved = str(neededrecieved) 
                                                order.save()
                                            else:
                                                order = orders.objects.get(custom_user_id=fetchpost_dd["owner_id"], user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"])
                                                order.recieved = str(neededrecieved) 
                                                order.save()
                                        else:
                                            order = orders.objects.get(custom_user_id=fetchpost_dd["owner_id"], user_id=fetchpost_dd["owner_id"], type=fetchpost_dd["type"])
                                            order.recieved = str(neededrecieved) 
                                            order.save()

                                    
                                    if int(order.needed) <= int(neededrecieved):
                                        if fetchpost_dd["type"] == "0":
                                            ordersss = orders.objects.get(id=order.id,post_id=fetchpost_dd["post_id"], type=fetchpost_dd["type"], user_id=fetchpost_dd["owner_id"])
                                            ordersss.needed = "0" 
                                            ordersss.recieved = "0" 
                                            ordersss.no_like_log = "0" 
                                            ordersss.save()
                                        elif fetchpost_dd["type"] == "1":
                                            ordersss = orders.objects.get(id=order.id,type=fetchpost_dd["type"], user_id=fetchpost_dd["owner_id"])
                                            ordersss.needed = "0" 
                                            ordersss.recieved = "0" 
                                            ordersss.no_like_log = "0" 
                                            ordersss.save()
                                        
                                        user_ddd = users.objects.get(id=order.user_id)
                                        if userowner.parent_id == "0":
                                            try:
                                                a = userowner.ftoken
                                                title = "Instagram Like Follow"
                                                body = {
                                                    "description" : "Your Order Completed Successfully",
                                                }
                                                send_notification(title,body,a)
                                            except:
                                                pass
                                        else:
                                            users_dd = users.objects.get(user_id=userowner.parent_id)
                                            try:
                                                a = users_dd.ftoken
                                                title = "Instagram Like Follow"
                                                body = {
                                                    "description" : "Your Order Completed Successfully",
                                                }
                                                send_notification(title,body,a)
                                            except:
                                                pass

                                    data = getrandompost(fetchpost_dd['user_id'], getcoin, request)
                                    data = json.dumps(data)
                                    data = json.loads(data)
                                    if data['fetch_post'] == False:
                                        get_pre ={
                                            "success" : False,
                                            "message" : "No Post avaialble yet"
                                        }
                                        return Response(get_pre)
                                    else:
                                        get_pre ={
                                            "success" : True,
                                            "data":data,
                                            "message" : "Success"
                                        }
                                        if fetchpost_dd["type"] == "0":
                                            custom_user_id_param = request.data.get('custom_user_id')
                                            if custom_user_id_param is not None:
                                                if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                                    already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['custom_user_id'],post_id=fetchpost_dd['post_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                                else:
                                                    already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'],post_id=fetchpost_dd['post_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                            else:
                                                already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'],post_id=fetchpost_dd['post_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                                

                                        elif fetchpost_dd["type"] == "1":
                                            custom_user_id_param = request.data.get('custom_user_id')
                                            if custom_user_id_param is not None:
                                                if str(fetchpost_dd['custom_user_id']).replace(' ','') != "":
                                                    already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['custom_user_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                                else:
                                                    already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'], al_user_id=str(fetchpost_dd["user_id"]))
                                            else:
                                                already_likefollows = already_like_follow.objects.create(type=fetchpost_dd['type'], user_id=fetchpost_dd["owner_id"], custom_user_id=fetchpost_dd['owner_id'], al_user_id=str(fetchpost_dd["user_id"]))

                                        return Response(get_pre)
                                else:
                                    data_e = {
                                        "fetch_post" : False
                                    }
                                    get_pre ={
                                        "success" : False,
                                        "message" : "Request user is not Valid"
                                    }
                                    return Response(get_pre)
                        else:
                            data = {
                                "fetch_post" : False
                            }
                            get_pre ={
                                "success" : False,
                                "message" : "Post Not Found"
                            } 
                            return Response(get_pre)

                    elif ownerid_bool == False and type_bool == False and alreadylike_bool == False and post_id_bool == False:   
                        data = getrandompost(fetchpost_dd['user_id'], total_coin, request)
                        data = json.dumps(data)
                        data = json.loads(data)
                        if data['fetch_post'] == False:
                            get_pre ={
                                "success" : False,
                                "message" : "No Post avaialble yet"
                            }
                            return Response(get_pre)
                        else:
                            get_pre ={
                                "success" : True,
                                "data":data,
                                "message" : "Success"
                            }   
                            return Response(get_pre)
                    
                    else:
                        get_pre ={
                            "success" : False,
                            "message" : "Argument Required"
                        }     
                        return Response(get_pre)

            else:
                get_pre ={
                    "success" : False,
                    "message" : "Requested Account is not Found"
                } 
                return Response(get_pre)
             
        else :
            get_pre = {
                "success": False,
                "message": "user_id is Required"
            }
            return Response(get_pre)

class verifyinapp(APIView):
    
    def post(self, request):
        verify_data = request.data

        # app_data for maintenence check
        all_data1 = app_data.objects.all()
        serializer1 = app_dataaccess_serializer(all_data1, many=True)
        app_data_dic = serializer1.data
        if app_data_dic != []:
            app_data_dic = json.dumps(serializer1.data).strip('[]')
            app_data_dic = json.loads(app_data_dic)
            cca = app_data_dic['maintenence_mode'].split(',')
            ccb = app_data_dic['payment_method'].split(',')
            app_data_dic['maintenence_mode'] = cca
            app_data_dic['payment_method'] = ccb
        else:
            get_pre = {
                "success": False,
                "message": "Server Issue"
            }
            return Response(get_pre)
        # End app_data for maintenence check


        access_token = app_data_dic['access_token']
        # access_token = "ya29.a0ARrdaM97qb8NfF9J5mbCehbJxXi7ah_OgJJ_UPgjsWeYYDQqHhJQNr28TgLRvNojJup6OuEZoDAonzcWwcNolnAZtoIrbCTMPMF15vChwamzYqLLEGENnvlu9EnT6mprAZ1C4ZZTCrbw8T7WGMTNI0dAIvG2jdE"

        inappResponse = request.data.get('purchase_data')
        # purchaseTime = inappResponse['purchaseTime']
        # now = datetime.datetime.now()
        # purchaseToken = inappResponse['purchaseToken']
        # productId = inappResponse['productId']
        # packageName = inappResponse['packageName']
        # user_id = inappResponse['user_id']
        now = datetime.datetime.now()

        # with open('/root/insta_like_follow/INSTA_ALL/inapp_api_log.txt', 'a+') as f:
        #     f.write("request("+str(now)+"):-\n")
        #     f.write(str(verify_data))
        #     f.write("\n")
        #     f.write("\n")
            

        if inappResponse is not None:


            if "user_id" in inappResponse and "purchaseToken" in inappResponse and "productId" in inappResponse and "packageName" in inappResponse and "orderId" in inappResponse:
                # purchaseTime = inappResponse['purchaseTime']
                purchaseToken = inappResponse['purchaseToken']
                productId = inappResponse['productId']
                packageName = inappResponse['packageName']
                user_id = inappResponse['user_id']
                if users.objects.filter(user_id=inappResponse['user_id']).exists():
                    users_dd = users.objects.get(user_id=inappResponse['user_id'])
                    if users_dd.status == "0":
                        get_pre = {
                            "success":False,
                            "message":"Your Account is Suspended By admin contact to support team"
                        }
                        return Response(get_pre)
                    else:
                        if users_dd.parent_id == "0":
                            user_id = users_dd.user_id
                            total_coins = int(users_dd.total_coins)
                        else:
                            parentaccount = users.objects.get(user_id=users_dd.parent_id)
                            user_id = parentaccount.user_id
                            total_coins = int(parentaccount.total_coins)

                        if user_orders.objects.filter(orderId=inappResponse['orderId']).exists():
                            get_pre = {
                                "success": False,
                                "message": "Not valid request"
                            }
                            return Response(get_pre)

                        if user_orders.objects.filter(purchaseToken=purchaseToken).exists():
                            get_pre = {
                                "success": False,
                                "message": "Purchase Token Already Used"
                            }
                            return Response(get_pre)

                        # logger.info(access_token)

                        conn = requests.get(f"https://www.googleapis.com/androidpublisher/v3/applications/{packageName}/purchases/products/{productId}/tokens/{purchaseToken}?access_token={access_token}")
                        
                        # logger.info("conn")
                        logger.info(conn.status_code)
                        data = conn.content
                        # conn.close()

                        logger.info("data")
                        logger.info(data)

                        decoderesponse = json.loads(data)


                        if str(conn.status_code) == "200":
                            # if 'purchaseToken' in inappResponse:
                            if str(inappResponse['purchaseToken']).replace(' ','') != "":
                                
                                data_of_user_order = user_orders.objects.create(user_id=inappResponse['user_id'],packageName=inappResponse['packageName'],orderId=inappResponse['orderId'],productId=inappResponse['productId'],purchaseToken=purchaseToken, acknowledgementState=decoderesponse['acknowledgementState'], regionCode=decoderesponse['regionCode'], token=inappResponse['purchaseToken'])
                                data_of_user_orderss = user_orders.objects.get(id=data_of_user_order.id)

                                if "purchaseTime" in inappResponse:
                                    data_of_user_orderss.purchaseTime=inappResponse['purchaseTime']
                                    data_of_user_orderss.save()
                                if "developerPayload" in inappResponse:
                                    data_of_user_orderss.developerPayload=inappResponse['developerPayload']
                                    data_of_user_orderss.save()
                                if "purchaseState" in inappResponse:
                                    data_of_user_orderss.purchaseState=inappResponse['purchaseState']
                                    data_of_user_orderss.save()
                            else:
                                data_of_user_order = user_orders.objects.create(user_id=inappResponse['user_id'],packageName=inappResponse['packageName'],orderId=inappResponse['orderId'],productId=inappResponse['productId'],purchaseToken=purchaseToken,acknowledgementState=decoderesponse['acknowledgementState'], regionCode=decoderesponse['regionCode'])

                                data_of_user_orderss = user_orders.objects.get(id=data_of_user_order.id)

                                if "purchaseTime" in inappResponse:
                                    data_of_user_orderss.purchaseTime=inappResponse['purchaseTime']
                                    data_of_user_orderss.save()
                                if "developerPayload" in inappResponse:
                                    data_of_user_orderss.developerPayload=inappResponse['developerPayload']
                                    data_of_user_orderss.save()
                                if "purchaseState" in inappResponse:
                                    data_of_user_orderss.purchaseState=inappResponse['purchaseState']
                                    data_of_user_orderss.save()

                            # else:
                            #     user_orders.objects.create(user_id=inappResponse['user_id'],packageName=inappResponse['packageName'],orderId=inappResponse['orderId'],productId=inappResponse['productId'],developerPayload=inappResponse['developerPayload'],purchaseToken=purchaseToken,purchaseTime=inappResponse['purchaseTime'],purchaseState=inappResponse['purchaseState'],acknowledgementState=decoderesponse['acknowledgementState'], regionCode=decoderesponse['regionCode'])



                            updated_coin = int(total_coins) + int(inappResponse['productId'])

                            users.objects.filter(user_id=user_id).update(total_coins=updated_coin, is_purchase='1')
                            
                            datas = {
                                "total_coins":updated_coin,
                            }
                            get_pre = {
                                "success":True,
                                "data":datas,
                                "message":f"You Purchased {inappResponse['productId']} hearts successfully."
                            }

                            with open('/root/insta_like_follow/INSTA_ALL/inapp_api_log.txt', 'a+') as f:
                                f.write("success("+str(now)+"):-\n")
                                f.write(str(verify_data))
                                f.write("\n")
                                f.write(str(data))
                                f.write("\n")
                                f.write(str(get_pre))
                                f.write("\n")
                                f.write("\n")

                            return Response(get_pre)

                        else:
                                
                            get_pre = {
                                "success":False,
                                "message":"check your details"
                            }
                            with open('/root/insta_like_follow/INSTA_ALL/inapp_api_log.txt', 'a+') as f:
                                f.write("error("+str(now)+"):-\n")
                                f.write(str(verify_data))
                                f.write("\n")
                                f.write(str(data))
                                f.write("\n")
                                f.write(str(get_pre))
                                f.write("\n")
                                f.write("\n")
                            return Response(get_pre)
            
                else:
                    get_pre = {
                        "success":False,
                        "message":"Requested Account is not Found"
                    }
                    return Response(get_pre)
            else:
                get_pre = {
                    "success":False,
                    "message":"Request not valid"
                }
                return Response(get_pre)
        else:
            get_pre = {
                "success":False,
                "message":"inappResponse is Required"
            }
            return Response(get_pre)


def base64_url_decode(inputss):
    input  = inputss.replace('-','+').replace('_','/')
    base64_bytes = base64.b64encode(input)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def parse_signed_request(signed_request):
    encoded_sig,payload = signed_request.split(".",1)

    secret = '857b771fd1664e064944b18ed08786c6' # Use your app secret here

    # decode the data
    sig = base64_url_decode(encoded_sig)
    data = json.dumps(base64_url_decode(payload))
    expected_sig = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    
    if sig != expected_sig:
        return None

    return data
    # string_bytes = input.encode('ascii')
    
class callback_2048(APIView):
    def get(self, request):
        signed_request = request.data.get('signed_request')
        data = parse_signed_request(signed_request)
        user_id = data['user_id']
        
        # Start data deletion
        status_url = ''
        confirmation_code = ''

        data = {
            'url': status_url,
            'confirmation_code':confirmation_code
        } 
        print(data)





#admin panel code       
# ADMIN PAGE
class admin(View):
    def get(self, request):
        email_param = request.session.get('email')
        if email_param is not None:
            if request.session.get('email') == None:
                return render(request, 'admin_login.html')
            else:
                return redirect('home')
        else:
            return render(request, 'admin_login.html')

    def post(self, request):
       
        if request.session.get('email'):
            return redirect('home')
        else:
            email = request.POST.get('email')
            password = request.POST.get('password')
            if User.objects.filter(email = email).exists():
                username = User.objects.get(email = email)

                user = authenticate(username=username.username, password=password)

                if user is not None:
                    request.session['email'] = email
                    return redirect('home')
                else:
                    messages.error(request, "Email or password Invalid" )
                    return redirect('admin')
            else:
                messages.error(request, "Email or password Invalid" )
                return redirect('admin')

# HOME
class home(View):
   
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:
            user_num = users.objects.count()
            like_num = orders.objects.filter(type='0').count()
            follow_num = orders.objects.filter(type='1').count()
            active_user_num = users.objects.filter(status='1').count()
            premium_user_num = users.objects.filter(is_purchase='1').count()
            return render(request, 'home.html',{'user_num':user_num, 'like_num':like_num, 'follow_num':follow_num, 'active_user_num':active_user_num, 'premium_user_num':premium_user_num})
        else:
            return redirect('admin')

    def post(self, request):
        if request.session.get('email'):
            return render(request, 'home.html')
        else:
            return redirect('admin')

# APP DATA
class appdata_coindetail(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:
            app_data_d = app_data.objects.all()
            app_data_num = app_data.objects.all().count()
            if app_data_num != 0:

                app_data_d = app_data.objects.get()
                earn_like = app_data_d.earn_like_coin
                spend_like = app_data_d.spent_like_coin
                earn_follow = app_data_d.earn_follow_coin
                spen_follow = app_data_d.spent_follow_coin
                referrel_coin = app_data_d.referrel_coin
                default_coin = app_data_d.default_coin
                from_add_coin = app_data_d.from_add_coin

                return render(request, 'appdata_coindetail.html',{'earn_like':earn_like,'spend_like':spend_like,'earn_follow':earn_follow,'spen_follow':spen_follow,'referrel_coin':referrel_coin,'default_coin':default_coin,'from_add_coin':from_add_coin})
            
            else:
                return render(request, 'appdata_coindetail.html')

        else:
            return redirect('admin')

    def post(self,request):
        if request.session.get('email') and request.session.get('email') != None:

            EarnLikeCoin_param = request.POST.get("EarnLikeCoin")
            if EarnLikeCoin_param is not None:
                EarnLikeCoin = str(request.POST.get("EarnLikeCoin")).replace(' ', '')
                if EarnLikeCoin != "":
                    if EarnLikeCoin.isnumeric():
            
                        spendLikeCoin_param = request.POST.get("spendLikeCoin")
                        if spendLikeCoin_param is not None:
                            spendLikeCoin = str(request.POST.get("spendLikeCoin")).replace(' ', '')
                            if spendLikeCoin != "":
                                if spendLikeCoin.isnumeric():
            
                                    EarnFollowCoin_param = request.POST.get("EarnFollowCoin")
                                    if EarnFollowCoin_param is not None:
                                        EarnFollowCoin = str(request.POST.get("EarnFollowCoin")).replace(' ', '')
                                        if EarnFollowCoin != "":
                                            if EarnFollowCoin.isnumeric():
                            
                                                spendFollowCoin_param = request.POST.get("spendFollowCoin")
                                                if spendFollowCoin_param is not None:
                                                    spendFollowCoin = str(request.POST.get("spendFollowCoin")).replace(' ', '')
                                                    if spendFollowCoin != "":
                                                        if spendFollowCoin.isnumeric():
                                        
                                                            RefferralCoin_param = request.POST.get("RefferralCoin")
                                                            if RefferralCoin_param is not None:
                                                                RefferralCoin = str(request.POST.get("RefferralCoin")).replace(' ', '')
                                                                if RefferralCoin != "":
                                                                    if RefferralCoin.isnumeric():
                                                    
                                                                        DefaultCoin_param = request.POST.get("DefaultCoin")
                                                                        if DefaultCoin_param is not None:
                                                                            DefaultCoin = str(request.POST.get("DefaultCoin")).replace(' ', '')
                                                                            if DefaultCoin != "":
                                                                                if DefaultCoin.isnumeric():
                                                                
                                                                                    FromAddCoin_param = request.POST.get("FromAddCoin")
                                                                                    if FromAddCoin_param is not None:
                                                                                        FromAddCoin = str(request.POST.get("FromAddCoin")).replace(' ', '').replace('-', '')
                                                                                        if FromAddCoin != "":
                                                                                            if FromAddCoin.isnumeric():
                                                                                                EarnLikeCoin = str(request.POST.get("EarnLikeCoin")).replace('-', '')
                                                                                                spendLikeCoin = str(request.POST.get("spendLikeCoin")).replace('-', '')
                                                                                                EarnFollowCoin = str(request.POST.get("EarnFollowCoin")).replace('-', '')
                                                                                                spendFollowCoin = str(request.POST.get("spendFollowCoin")).replace('-', '')
                                                                                                RefferralCoin = str(request.POST.get("RefferralCoin")).replace('-', '')
                                                                                                DefaultCoin = str(request.POST.get("DefaultCoin")).replace('-', '')
                                                                                                FromAddCoin = str(request.POST.get("FromAddCoin")).replace('-', '')

                                                                                                
                                                                                                app_data_d = app_data.objects.all()
                                                                                                app_data_num = app_data.objects.all().count()
                                                                                                print(app_data_d)
                                                                                                if app_data_num == 0:
                                                                                                    app_data.objects.create(earn_like_coin=EarnLikeCoin, spent_like_coin=spendLikeCoin, earn_follow_coin= EarnFollowCoin, spent_follow_coin=spendFollowCoin, referrel_coin=RefferralCoin, default_coin=DefaultCoin, from_add_coin=FromAddCoin)
                                                                                                    
                                                                                                else:
                                                                                                    app_data_d = app_data.objects.get()
                                                                                                    app_data_d.earn_like_coin = EarnLikeCoin
                                                                                                    app_data_d.spent_like_coin = spendLikeCoin
                                                                                                    app_data_d.earn_follow_coin = EarnFollowCoin
                                                                                                    app_data_d.spent_follow_coin = spendFollowCoin
                                                                                                    app_data_d.referrel_coin = RefferralCoin
                                                                                                    app_data_d.default_coin = DefaultCoin
                                                                                                    app_data_d.from_add_coin = FromAddCoin
                                                                                                    app_data_d.save()
                                                                                                return redirect('appdatacoindetail')
                                                                                            else:
                                                                                                messages.error(request, "From App Coin is not valid")
                                                                                                return redirect('appdatacoindetail')
                                                                                        else:
                                                                                            messages.error(request, "From App Coin is Empty!")
                                                                                            return redirect('appdatacoindetail')
                                                                                    else:
                                                                                        messages.error(request, "From Add Coin is Required")
                                                                                        return redirect('appdatacoindetail')
                                                                                else:
                                                                                    messages.error(request, "Default Coin is not valid")
                                                                                    return redirect('appdatacoindetail')
                                                                            else:
                                                                                messages.error(request, "Default Coin is Empty!")
                                                                                return redirect('appdatacoindetail')
                                                                        else:
                                                                            messages.error(request, "Default Coin is Required")
                                                                            return redirect('appdatacoindetail')
                                                                    else:
                                                                        messages.error(request, "Refferral Coin is not valid")
                                                                        return redirect('appdatacoindetail')
                                                                else:
                                                                    messages.error(request, "Refferral Coin is Empty!")
                                                                    return redirect('appdatacoindetail')
                                                            else:
                                                                messages.error(request, "Refferral Coin is Required")
                                                                return redirect('appdatacoindetail')
                                                        else:
                                                            messages.error(request, "Spend Follow Coin is not valid")
                                                            return redirect('appdatacoindetail')
                                                    else:
                                                        messages.error(request, "Spend Follow Coin is Empty!")
                                                        return redirect('appdatacoindetail')
                                                else:
                                                    messages.error(request, "Spend Follow Coin is Required")
                                                    return redirect('appdatacoindetail')
                                            else:
                                                messages.error(request, "Refferral Coin is not valid")
                                                return redirect('appdatacoindetail')
                                        else:
                                            messages.error(request, "Earn Follow Coin is Empty!")
                                            return redirect('appdatacoindetail')
                                    else:
                                        messages.error(request, "Earn Follow Coin is Required")
                                        return redirect('appdatacoindetail')
                                else:
                                    messages.error(request, "Spend Like Coin is not valid")
                                    return redirect('appdatacoindetail')
                            else:
                                messages.error(request, "Spend Like Coin is Empty!")
                                return redirect('appdatacoindetail')
                        else:
                            messages.error(request, "Spend Like Coin is Required")
                            return redirect('appdatacoindetail')
                    else:
                        messages.error(request, "Earn Like Coin is Not Valid!")
                        return redirect('appdatacoindetail')
                else:
                    messages.error(request, "Earn Like Coin is Empty!")
                    return redirect('appdatacoindetail')
            else:
                messages.error(request, "Earn Like Coin is Required")
                return redirect('appdatacoindetail')
        else:
            return redirect('admin') 

class appdata_offer(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:
            app_data_d = app_data.objects.all()
            app_data_NUM = app_data.objects.all().count()
            if app_data_NUM != 0:

                return render(request, 'appdata_offer.html', {'app_data_d':app_data_d[0]})

            else:
                return render(request, 'appdata_offer.html')
        else:
            return redirect('admin')

    def post(self, request):
        if request.session.get('email') and request.session.get('email') != None:

            offer_type_param = request.POST.get("offer_type")
            if offer_type_param is not None:
                offer_type = str(request.POST.get("offer_type")).replace(' ', '')
                if offer_type != "":

                    Offer_Percentage_param = request.POST.get("Offer_Percentage")
                    if Offer_Percentage_param is not None:
                        Offer_Percentage = str(request.POST.get("Offer_Percentage")).replace(' ', '')
                        if Offer_Percentage != "":
                            if Offer_Percentage.isnumeric():

                                offer_start_date_param = request.POST.get("offer_start_date")
                                if offer_start_date_param is not None:
                                    offer_start_date = str(request.POST.get("offer_start_date"))
                                    if offer_start_date != "":

                                        o_start_date = str(offer_start_date).split(" ")
                                        s_dates = o_start_date[0].split("/")
                                        s_time =  re.split('; | |:', o_start_date[1])
                                        o_s_year = int(s_dates[2])
                                        o_s_month = int(s_dates[0])
                                        o_s_date = int(s_dates[1])

                                        o_s_hh = int(s_time[0])
                                        o_s_mm = int(s_time[1])

                                        if o_start_date[2] == 'PM' and o_s_hh != 12 :
                                            o_s_hh = o_s_hh + 12

                                        date_time1 = datetime.datetime(o_s_year, o_s_month, o_s_date, o_s_hh, o_s_mm)

                                        offer_end_date_param = request.POST.get("offer_end_date")
                                        if offer_end_date_param is not None:
                                            offer_end_date = str(request.POST.get("offer_end_date"))
                                            if offer_end_date != "":

                                                o_end_date = str(offer_end_date).split(" ")
                                                e_dates = o_end_date[0].split("/")
                                                e_time =  re.split('; | |:', o_end_date[1])
                                                o_e_year = int(e_dates[2])
                                                o_e_month = int(e_dates[0])
                                                o_e_date = int(e_dates[1])

                                                o_e_hh = int(e_time[0])
                                                o_e_mm = int(e_time[1])

                                                if o_end_date[2] == 'PM' and o_e_hh != 12 :
                                                    o_e_hh = o_e_hh + 12

                                                date_time2 = datetime.datetime(o_e_year, o_e_month, o_e_date, o_e_hh, o_e_mm)

                                                if (date_time1 < date_time2):

                                                    offerDiscountTitle_param = request.POST.get("offerDiscountTitle")
                                                    if offerDiscountTitle_param is not None:
                                                        offerDiscountTitle = str(request.POST.get("offerDiscountTitle")).replace(' ', '')
                                                        if offerDiscountTitle != "":
                                                            
                                                            offerDiscountText_param = request.POST.get("offerDiscountText")
                                                            if offerDiscountText_param is not None:
                                                                offerDiscountText = str(request.POST.get("offerDiscountText")).replace(' ', '')
                                                                if offerDiscountText != "":

                                                                    OfferType = request.POST.get("offer_type")
                                                                    OfferPercentage = str(request.POST.get("Offer_Percentage")).replace('-', '')
                                                                    OfferStartDate = request.POST.get("offer_start_date")
                                                                    OfferEndDate = request.POST.get("offer_end_date")
                                                                    OfferdiscountTitle = request.POST.get("offerDiscountTitle")
                                                                    offerDiscountText = request.POST.get("offerDiscountText")

                                                                    image_param = request.FILES.get("offer_discount_image")
                                                                    if image_param is not None:

                                                                        offer_discount_image = str(request.FILES["offer_discount_image"]).replace(' ', '')
                                                                        if offer_discount_image != "":
                                                                            OfferDiscountImage = request.FILES["offer_discount_image"]

                                                                            image = request.FILES.get('offer_discount_image')
                                                                            filename, file_extension = str(image).split(".")
                                                                            file_extension = file_extension.lower()
                                                                            file_extension = "."+file_extension
                                                                            if file_extension == '.jpeg' or file_extension == '.jpg' or file_extension == '.png' or file_extension == '.gif' or file_extension == '.tiff' or file_extension == '.psd' or file_extension == '.pdf' or file_extension == '.eps' or file_extension == '.ai' or file_extension == '.indd' or file_extension == '.raw' :
                                                                            
                                                                            
                                                                            
                                                                                image_unique_id = str(uuid.uuid4())
                                                                                image_file = image_unique_id + "_like_order" + file_extension
                                                                                img = request.FILES['offer_discount_image']
                                                                                fs = FileSystemStorage(location=Offer_Img_URL, base_url=None)
                                                                                filename = fs.save(image_file, img)
                                                                                uploaded_file_url = fs.url(filename)

                                                                                app_data_d = app_data.objects.get()
                                                                                app_data_num = app_data.objects.all().count()

                                                                                if app_data_num == 0:
                                                                                    app_data.objects.create(offer=OfferType, offer_percentage=OfferPercentage, offer_starttime=OfferStartDate, offer_endtime=OfferEndDate, offer_discount_title=OfferdiscountTitle,offer_discount_text=offerDiscountText, offer_discount_image=image_file)

                                                                                else:
                                                                                    app_data_d.offer = str(OfferType)
                                                                                    app_data_d.offer_percentage = str(OfferPercentage)
                                                                                    app_data_d.offer_starttime = str(OfferStartDate)
                                                                                    app_data_d.offer_endtime = str(OfferEndDate)
                                                                                    app_data_d.offer_discount_title = str(OfferdiscountTitle)
                                                                                    app_data_d.offer_discount_text = str(offerDiscountText)
                                                                                    app_data_d.offer_discount_image = str(filename)
                                                                                    app_data_d.save()
                                                                                return redirect('appdataoffer')
                                                                            else:
                                                                                messages.error(request, "Offer Image is not valid")
                                                                                return redirect('appdataoffer')
                                                                        else:
                                                                            app_data_d = app_data.objects.all()
                                                                            app_data_num = app_data.objects.all().count()

                                                                            if app_data_num == 0:
                                                                                app_data.objects.create(offer=OfferType, offer_percentage=OfferPercentage, offer_starttime=OfferStartDate, offer_endtime=OfferEndDate, offer_discount_title=OfferdiscountTitle,offer_discount_text=offerDiscountText, offer_discount_image='')

                                                                            else:
                                                                                app_data_d.offer = str(OfferType)
                                                                                app_data_d.offer_percentage = str(OfferPercentage)
                                                                                app_data_d.offer_starttime = str(OfferStartDate)
                                                                                app_data_d.offer_endtime = str(OfferEndDate)
                                                                                app_data_d.offer_discount_title = str(OfferdiscountTitle)
                                                                                app_data_d.offer_discount_text = str(offerDiscountText)
                                                                                app_data_d.offer_discount_image = ''
                                                                                app_data_d.save()

                                                                            return redirect('appdataoffer')
                                                                    else:
                                                                        app_data_d = app_data.objects.all()
                                                                        app_data_num = app_data.objects.all().count()

                                                                        if app_data_num == 0:
                                                                            app_data.objects.create(offer=OfferType, offer_percentage=OfferPercentage, offer_starttime=OfferStartDate, offer_endtime=OfferEndDate, offer_discount_title=OfferdiscountTitle,offer_discount_text=offerDiscountText, offer_discount_image='')

                                                                        else:
                                                                            app_data_d = app_data.objects.get()
                                                                            app_data_d.offer = str(OfferType)
                                                                            app_data_d.offer_percentage = str(OfferPercentage)
                                                                            app_data_d.offer_starttime = str(OfferStartDate)
                                                                            app_data_d.offer_endtime = str(OfferEndDate)
                                                                            app_data_d.offer_discount_title = str(OfferdiscountTitle)
                                                                            app_data_d.offer_discount_text = str(offerDiscountText)
                                                                            app_data_d.offer_discount_image = ''
                                                                            app_data_d.save()

                                                                        return redirect('appdataoffer')
                                                                else:
                                                                    messages.error(request, "Offer Discount Description is not valid")
                                                                    return redirect('appdataoffer')
                                                            else:
                                                                messages.error(request, "Offer Discount Description is Required")
                                                                return redirect('appdataoffer')
                                                        else:
                                                            messages.error(request, "Offer Discount Title is not valid")
                                                            return redirect('appdataoffer')
                                                    else:
                                                        messages.error(request, "Offer Discount Title is Required")
                                                        return redirect('appdataoffer')
                                                else:
                                                    messages.error(request, "Enter Valid Date Period!")
                                                    return redirect('appdataoffer')
                                            else:
                                                messages.error(request, "Offer End Date is not valid")
                                                return redirect('appdataoffer')
                                        else:
                                            messages.error(request, "Offer End Date is Required")
                                            return redirect('appdataoffer')
                                    else:
                                        messages.error(request, "Offer Start Date is not valid")
                                        return redirect('appdataoffer')
                                else:
                                    messages.error(request, "Offer Start Date is Required")
                                    return redirect('appdataoffer')
                            else:
                                messages.error(request, "Offer Percentage is not valid")
                                return redirect('appdataoffer')
                        else:
                            messages.error(request, "Offer Percentage is Empty!")
                            return redirect('appdataoffer')
                    else:
                        messages.error(request, "Offer Percentage is Required")
                        return redirect('appdataoffer')
                else:
                    messages.error(request, "Offer Type is not valid")
                    return redirect('appdataoffer')
            else:
                messages.error(request, "Offer Type is Required")
                return redirect('appdataoffer')
        else:
            return redirect('admin')

class appdata_maintenence(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:
            app_data_dd = app_data.objects.all()
            app_data_num = app_data.objects.all().count()
            if app_data_num != 0:
                app_data_dd = app_data.objects.all()
                serializer1 = appdata_serializer(app_data_dd, many=True)
                app_data_dic = json.dumps(serializer1.data).strip('[]')
                app_data_dic = json.loads(app_data_dic)
                cca = str(app_data_dic['maintenence_mode']).split(',')
                ccb = str(app_data_dic['payment_method']).split(',')
                app_data_dic['maintenence_mode'] = cca
                app_data_dic['payment_method'] = ccb
                return render(request, 'appdata_maintenence.html',{'app_data_dd':app_data_dic, 'maintenence_mode':cca, 'payment_method':ccb})

            else:
                return render(request, 'appdata_maintenence.html')
        else:
            return redirect('admin')

    def post(self, request):
        if request.session.get('email') and request.session.get('email') != None:
        
            app_data_dd = app_data.objects.all()
            app_data_num = app_data.objects.all().count()

            if app_data_num == 0:
                message_param = request.POST.get('maintenence_msg')
                if message_param is not None:
                    message = request.POST.get('maintenence_msg')
                else:
                    message = None

                like_follow = []
                like_param = request.POST.get('like')
                if like_param is not None:
                    like = request.POST.get('like')
                    if like == 'on':
                        like_follow.append('like')
                else:
                    pass
                follow_param = request.POST.get('follow')
                if follow_param is not None:
                    follow = request.POST.get('follow')
                    if follow == 'on':
                        like_follow.append('follow')
                else:
                    pass
                like_follow = str(like_follow).strip("[]").replace("'","").replace(" ","")
                
                updateMode_param = request.POST.get('update_mode')
                if updateMode_param is not None:
                    updateMode = request.POST.get('update_mode')
                    if updateMode == '0':
                        updatemode_data = 'None'
                    elif updateMode == '1':
                        updatemode_data = 'Flexible'
                    elif updateMode == '2':
                        updatemode_data = 'Immiediate'
                else:
                    updatemode_data = None
                
                updateURL_param = request.POST.get('update_url')
                if updateURL_param is not None:
                    updateURL = request.POST.get('update_url')
                else:
                    updateURL = None

                updateMsg_param = request.POST.get('update_message')
                if updateMsg_param is not None:
                    updateMsg = request.POST.get('update_message')
                else:
                    updateMsg = None

                inapp_paypal = []
                inapp_param = request.POST.get('inapp')
                if inapp_param is not None:
                    inapp = request.POST.get('inapp')
                    if inapp == 'on':
                        inapp_paypal.append('inapp')
                else:
                    pass
                paypal_param = request.POST.get('paypal')
                if paypal_param is not None:
                    paypal = request.POST.get('paypal')
                    if paypal == 'on':
                        inapp_paypal.append('paypal')
                else:
                    pass
                inapp_paypal = str(inapp_paypal).strip("[]").replace("'","").replace(" ","")

                app_data.objects.create(maintenence_message=message, maintenence_mode=like_follow, update_mode=updatemode_data, update_url=updateURL, update_message=updateMsg, payment_method=inapp_paypal)

            else:
                app_data_dd = app_data.objects.get()
                message_param = request.POST.get('maintenence_msg')
                if message_param is not None:
                    message = request.POST.get('maintenence_msg')
                    app_data_dd.maintenence_message = message
                    app_data_dd.save()
                else:
                    pass
                
                like_follow = []
                like_param = request.POST.get('like')
                if like_param is not None:
                    like = request.POST.get('like')
                    if like == 'on':
                        like_follow.append('like')
                else:
                    pass
                follow_param = request.POST.get('follow')
                if follow_param is not None:
                    follow = request.POST.get('follow')
                    if follow == 'on':
                        like_follow.append('follow')
                else:
                    pass

                like_follow = str(like_follow).strip("[]").replace("'","").replace(" ","")
                app_data_dd.maintenence_mode = like_follow

                updateMode_param = request.POST.get('update_mode')
                if updateMode_param is not None:
                    updateMode = request.POST.get('update_mode')
                    if updateMode == '0':
                        app_data_dd.update_mode = 'none'
                    elif updateMode == '1':
                        app_data_dd.update_mode = 'flexible'
                    elif updateMode == '2':
                        app_data_dd.update_mode = 'immiediate'
                    app_data_dd.save()
                else:
                    pass
                
                update_url_param = request.POST.get('update_url')
                if update_url_param is not None:
                    updateURL = request.POST.get('update_url')
                    app_data_dd.update_url = updateURL
                    app_data_dd.save()
                else:
                    pass
                
                update_message_param = request.POST.get('update_message')
                if update_message_param is not None:
                    updateMsg = request.POST.get('update_message')
                    app_data_dd.update_message = updateMsg
                    app_data_dd.save()
                else:
                    pass
                
                inapp_paypal = []
                inapp_param = request.POST.get('inapp')
                if inapp_param is not None:
                    inapp = request.POST.get('inapp')
                    if inapp == 'on':
                        inapp_paypal.append('inapp')
                else:
                    pass
                paypal_param = request.POST.get('paypal')
                if paypal_param is not None:
                    paypal = request.POST.get('paypal')
                    if paypal == 'on':
                        inapp_paypal.append('paypal')
                else:
                    pass

                inapp_paypal = str(inapp_paypal).strip("[]").replace("'","").replace(" ","")
                app_data_dd.payment_method = inapp_paypal
                app_data_dd.save()
            return redirect('appdatamaintenence')

        else:
            return redirect('admin')            
    
class appdata_ads_detail(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:
            app_data_ads = app_data.objects.all()
            app_data_num = app_data.objects.all().count()
            if app_data_num != 0:
                app_data_ads = app_data.objects.get()
                return render(request, 'appdata_ads_detail.html',{'app_data_ads':app_data_ads})

            else:
                return render(request, 'appdata_ads_detail.html')
        else:
            return redirect('admin')

    def post(self,request):
        if request.session.get('email') and request.session.get('email') != None:
            app_data_ads = app_data.objects.all()
            app_data_num = app_data.objects.all().count()

            if app_data_num == 0:
                GameId_param = request.POST.get('game_id')
                if GameId_param is not None:
                    GameId = request.POST.get('game_id')
                else:
                    GameId = None
                
                BannerId_param = request.POST.get('banner_id')
                if BannerId_param is not None:
                    BannerId = request.POST.get('banner_id')
                else:
                    BannerId = None

                InitialId_param = request.POST.get('initial_id')
                if InitialId_param is not None:
                    InitialId = request.POST.get('initial_id')
                else:
                    InitialId = None

                app_data.objects.create(game_id=GameId, banner_id=BannerId, initial_id=InitialId)

            else:
                app_data_ads = app_data.objects.get()

                GameId_param = request.POST.get('game_id')
                if GameId_param is not None:
                    GameId = request.POST.get('game_id')
                    app_data_ads.game_id = GameId
                    app_data_ads.save()
                else:
                    pass

                BannerId_param = request.POST.get('banner_id')
                if BannerId_param is not None:
                    BannerId = request.POST.get('banner_id')
                    app_data_ads.banner_id = BannerId
                    app_data_ads.save()
                else:
                    pass

                InitialId_param = request.POST.get('initial_id')
                if InitialId_param is not None:
                    InitialId = request.POST.get('initial_id')
                    app_data_ads.initial_id = InitialId
                    app_data_ads.save()
                else:
                    pass
            return redirect('appdataadsdetail')

        else:
            return redirect('admin')

class appdata_other(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:
            app_data_other = app_data.objects.all()
            app_data_num = app_data.objects.all().count()
            if app_data_num != 0:
                app_data_other = app_data.objects.get()
                print(app_data_other)
                return render(request, 'appdata_other.html',{'app_data_other':app_data_other})

            else:
                return render(request, 'appdata_other.html')
        else:
            return redirect('admin')

    def post(self,request):
        if request.session.get('email') and request.session.get('email') != None:
            app_data_other = app_data.objects.get()
            app_data_other_num = app_data.objects.all().count()

            if app_data_other_num == 0:
                user_agent_param = request.POST.get("user_agent")
                if user_agent_param is not None:
                    user_agent = str(request.POST.get("user_agent")).replace(' ', '')
                    if user_agent != "":
                    
                        PlayStoreVersion_param = request.POST.get('play_store_version')
                        if PlayStoreVersion_param is not None:
                            PlayStoreVersion = request.POST.get('play_store_version')
                        else:
                            PlayStoreVersion = None

                        WebLogin_param = request.POST.get('Web_Login')
                        if WebLogin_param is not None:
                            WebLogin = request.POST.get('Web_Login')
                            if WebLogin == '0':
                                app_data_other_web = '0'
                            elif WebLogin == '1':
                                app_data_other_web = '1'
                        else:
                            app_data_other_web = None
                        
                        WebView_param = request.POST.get('Web_View')
                        if WebView_param is not None:
                            WebView = request.POST.get('Web_View')
                            if WebView == '0':
                                app_data_other_view = '0'
                            elif WebView == '1':
                                app_data_other_view = '1'
                        else:
                            app_data_other_view = None

                        ShareUrl_param = request.POST.get('share_url')
                        if ShareUrl_param is not None:
                            ShareUrl = request.POST.get('share_url')
                        else:
                            ShareUrl = None

                        Email_param = request.POST.get('email')
                        if Email_param is not None:
                            Email = request.POST.get('email')
                        else:
                            Email = None

                        WebSite_param = request.POST.get('website')
                        if WebSite_param is not None:
                            WebSite = request.POST.get('website')
                        else:
                            WebSite = None

                        PrivacyPolicy_param = request.POST.get('privacy_policy')
                        if PrivacyPolicy_param is not None:
                            PrivacyPolicy = request.POST.get('privacy_policy')
                        else:
                            PrivacyPolicy = None

                        Facebook_param = request.POST.get('facebook')
                        if Facebook_param is not None:
                            Facebook = request.POST.get('facebook')
                        else:
                            Facebook = None

                        Instagram_param = request.POST.get('instagram')
                        if Instagram_param is not None:
                            Instagram = request.POST.get('instagram')
                        else:
                            Instagram = None

                        Twitter_param = request.POST.get('twitter')
                        if Twitter_param is not None:
                            Twitter = request.POST.get('twitter')
                        else:
                            Twitter = None

                        Telegram_param = request.POST.get('telegram')
                        if Telegram_param is not None:
                            Telegram = request.POST.get('telegram')
                        else:
                            Telegram = None

                        RateDialog_param = request.POST.get('Rate_Dialog')
                        if RateDialog_param is not None:
                            RateDialog = request.POST.get('Rate_Dialog')
                            if RateDialog == '0':
                                app_data_other_rate_dialog = '0'
                            elif RateDialog == '1':
                                app_data_other_rate_dialog = '1'
                        else:
                            app_data_other_rate_dialog = None

                        ShareDialog_param = request.POST.get('Share_Dialog')
                        if ShareDialog_param is not None:
                            ShareDialog = request.POST.get('Share_Dialog')
                            if ShareDialog == '0':
                                app_data_other_share_dialog = '0'
                            elif ShareDialog == '1':
                                app_data_other_share_dialog = '1'
                        else:
                            app_data_other_share_dialog = None

                        UserAgent = request.POST.get("user_agent")
                        app_data.objects.create(user_agent=UserAgent, playstore_version=PlayStoreVersion, web_login=app_data_other_web, web=app_data_other_view, share_url=ShareUrl, email=Email, website=WebSite, privacy_policy=PrivacyPolicy, facebook=Facebook, instagram=Instagram, twitter=Twitter, telegram=Telegram, rate_dialog=app_data_other_rate_dialog, share_dialog=app_data_other_share_dialog)
                        return redirect('appdataother')
                    else:
                        messages.error(request, "User Agent is not valid")
                        return redirect('appdataother')
                else:
                    messages.error(request, "User Agent is Required")
                    return redirect('appdataother')

            else:
                app_data_other=app_data.objects.get()
                user_agent_param = request.POST.get("user_agent")
                if user_agent_param is not None:
                    user_agent = str(request.POST.get("user_agent")).replace(' ', '')
                    if user_agent != "":
                        
                        PlayStoreVersion_param = request.POST.get("play_store_version")
                        if PlayStoreVersion_param is not None:
                            PlayStoreVersion = request.POST.get('play_store_version')
                            app_data_other.playstore_version = PlayStoreVersion
                            app_data_other.save()
                        else:
                            pass
                        
                        WebLogin_param = request.POST.get("Web_Login")
                        if WebLogin_param is not None:
                            WebLogin = request.POST.get('Web_Login')
                            if WebLogin == '0':
                                app_data_other.web_login = '0'
                            elif WebLogin == '1':
                                app_data_other.web_login = '1'
                            app_data_other.save()
                        else:
                            pass
                        
                        WebView_param = request.POST.get("Web_View")
                        if WebView_param is not None:
                            WebView = request.POST.get('Web_View')
                            if WebView == '0':
                                app_data_other.web = '0'
                            elif WebView == '1':
                                app_data_other.web = '1'
                            app_data_other.save()
                        else:
                            pass
                        
                        ShareUrl_param = request.POST.get("share_url")
                        if ShareUrl_param is not None:
                            ShareUrl = request.POST.get('share_url')
                            app_data_other.share_url = ShareUrl
                            app_data_other.save()
                        else:
                            pass
                        
                        Email_param = request.POST.get("email")
                        if Email_param is not None:
                            Email = request.POST.get('email')
                            app_data_other.email = Email
                            app_data_other.save()
                        else:
                            pass
                        
                        WebSite_param = request.POST.get("website")
                        if WebSite_param is not None:
                            WebSite = request.POST.get('website')
                            app_data_other.website = WebSite
                            app_data_other.save()
                        else:
                            pass
                        
                        PrivacyPolicy_param = request.POST.get("privacy_policy")
                        if PrivacyPolicy_param is not None:
                            PrivacyPolicy = request.POST.get('privacy_policy')
                            app_data_other.privacy_policy = PrivacyPolicy
                            app_data_other.save()
                        else:
                            pass
                        
                        Facebook_param = request.POST.get("facebook")
                        if Facebook_param is not None:
                            Facebook = request.POST.get('facebook')
                            app_data_other.facebook = Facebook
                            app_data_other.save()
                        else:
                            pass
                        
                        Instagram_param = request.POST.get("instagram")
                        if Instagram_param is not None:
                            Instagram = request.POST.get('instagram')
                            app_data_other.instagram = Instagram
                            app_data_other.save()
                        else:
                            pass
                        
                        Twitter_param = request.POST.get("twitter")
                        if Twitter_param is not None:
                            Twitter = request.POST.get('twitter')
                            app_data_other.twitter = Twitter
                            app_data_other.save()
                        else:
                            pass
                        
                        Telegram_param = request.POST.get("telegram")
                        if Telegram_param is not None:
                            Telegram = request.POST.get('telegram')
                            app_data_other.telegram = Telegram
                            app_data_other.save()
                        else:
                            pass
                        
                        updateMode_param = request.POST.get("Rate_Dialog")
                        if updateMode_param is not None:
                            updateMode = request.POST.get('Rate_Dialog')
                            if updateMode == '0':
                                app_data_other.rate_dialog = '0'
                            elif updateMode == '1':
                                app_data_other.rate_dialog = '1'
                            app_data_other.save()
                        else:
                            pass
                        
                        updateMode_param = request.POST.get("Share_Dialog")
                        if updateMode_param is not None:
                            updateMode = request.POST.get('Share_Dialog')
                            if updateMode == '0':
                                app_data_other.share_dialog = '0'
                            elif updateMode == '1':
                                app_data_other.share_dialog = '1'
                            app_data_other.save()
                        else:
                            pass

                        UserAgent = request.POST.get("user_agent")
                        app_data_other.user_agent = UserAgent
                        app_data_other.save()
                        return redirect('appdataother')
                    else:
                        messages.error(request, "User Agent is not valid")
                        return redirect('appdataother')
                else:
                    messages.error(request, "User Agent is Required")
                    return redirect('appdataother')
        else:
            return redirect('admin')

# NOTIFICATION
class Daily_Notification(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:
            app_data_dn = app_data.objects.all()
            app_data_num = app_data.objects.all().count()

            if app_data_num != 0:
                app_data_dn = app_data.objects.all()
                serializer1 = appdata_serializer(app_data_dn, many=True)
                app_data_dic = json.dumps(serializer1.data).strip('[]')
                app_data_dic = json.loads(app_data_dic)
                return render(request, 'daily_notification.html', {'app_data_dic':app_data_dic})
            else:
                return render(request, 'daily_notification.html')
        else:
            return redirect('admin')

    def post(self, request):
        if request.session.get('email') and request.session.get('email') != None:
        
            DN = app_data.objects.all()
            DN_num = app_data.objects.all().count()

            if DN_num == 0:
                notification_Show_param = request.POST.get("notification_show")
                if notification_Show_param is not None:
                    notification_Show = request.POST.get('notification_show')
                    if notification_Show == '0':
                        DN_notification_show = '0'
                    elif notification_Show == '1':
                        DN_notification_show = '1'
                else:
                    DN_notification_show = None

                notification_Message_param = request.POST.get("notification_message")
                if notification_Message_param is not None:
                    notification_Message = request.POST.get('notification_message')
                else:
                    notification_Message = None

                notification_Title_param = request.POST.get("notification_title")
                if notification_Title_param is not None:
                    notification_Title = request.POST.get('notification_title')
                else:
                    notification_Title = None

                app_data.objects.create(notification_show=DN_notification_show, notification_message=notification_Message, notification_title=notification_Title)
                return redirect('dailynotification')
            else:
                DN = app_data.objects.get()
                notification_Show_param = request.POST.get("notification_show")
                if notification_Show_param is not None:
                    notification_Show = request.POST.get('notification_show')
                    if notification_Show == '0':
                        DN.notification_show = '0'
                    elif notification_Show == '1':
                        DN.notification_show = '1'
                    DN.save()
                else:
                    pass
                
                notification_Message_param = request.POST.get("notification_message")
                if notification_Message_param is not None:
                    notification_Message = request.POST.get('notification_message')
                    DN.notification_message = notification_Message
                    DN.save()
                else:
                    pass

                notification_Title_param = request.POST.get("notification_title")
                if notification_Title_param is not None:
                    notification_Title = request.POST.get('notification_title')
                    DN.notification_title = notification_Title
                    DN.save()
                else:
                    pass

                return redirect('dailynotification')

        else:
            return redirect('admin')

class Send_Notification(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:
            # logger.info('response checker')
            return render(request, 'send_notification.html')
        else:
            return redirect('admin')

    def post(self, request):
        if request.session.get('email') and request.session.get('email') != None:

            # logger.info('response checker')

            #0=Premium
            #1=None Premium
            #2=all
            notification_Show_param = request.POST.get('send_reciever_type')
            if notification_Show_param is not None:
                notification_Show = request.POST.get('send_reciever_type')
            else:
                notification_Show=""
            
            notification_Message_param = request.POST.get('send_notification_message')
            if notification_Message_param is not None:
                notification_Message = request.POST.get('send_notification_message')
            else:
                notification_Message = ""

            notification_Title_param = request.POST.get('send_notification_title')
            if notification_Title_param is not None:
                notification_Title = request.POST.get('send_notification_title')
            else:
                notification_Title = ""

            userss = []
            if str(notification_Show) == "0":
                userss = users.objects.filter(is_purchase="1", parent_id="0")
            elif str(notification_Show) == "1":
                userss = users.objects.filter(is_purchase="0", parent_id="0")
            elif str(notification_Show) == "2":
                userss = users.objects.filter(parent_id="0")
            else:
                userss = []
            
            file = open(base_url + "INSTA_ALL/responce.txt", "a")
            # file = open("responce.txt", "a")
            file.write("\nuser")
            file.write(str(userss))
            file.close()
            if userss != []:
                for user in userss:
                    registration_token = user.ftoken
                    send_notification(notification_Title,notification_Message,registration_token)
                    
            return redirect('home')
        
        else:
            return redirect('admin')

# COIN DETAILS
class Coin_Details(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:
            coins_details = coin_details.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(coins_details, 100)
            try:
                coins_details_data = paginator.page(page)
            except PageNotAnInteger:
                coins_details_data = paginator.page(1)
            except EmptyPage:
                coins_details_data = paginator.page(paginator.num_pages)
            return render(request, 'coin_details.html', {'coins_details':coins_details_data})
        else:
            return redirect('admin')

    def post(self,request):
        if request.session.get('email') and request.session.get('email') != None:

            app_data_num = app_data.objects.all().count()

            if app_data_num == 0:
                messages.error(request, "Please enter appdata First!")
                return redirect('coindetails')

            else:
                type_bool = False
                edit_form_bool = False
                delete_form_bool = False

                type_param = request.POST.get('type')
                if type_param is not None:
                    type_bool = True

                edit_form_param = request.POST.get('edit_form')
                if edit_form_param is not None:
                    edit_form_bool = True
                
                delete_form_param = request.POST.get('delete_form')
                if delete_form_param is not None:
                    delete_form_bool = True
                
                if type_bool == True:

                    coin_details_id_param = request.POST.get("id")
                    if coin_details_id_param is not None:
                        coin_details_id = request.POST.get("id")

                        coin_detail_data = coin_details.objects.get(id=coin_details_id)
                        Quantity_Coin = coin_detail_data.quantity
                        IndianRate_Coin = coin_detail_data.indian_rate
                        OtherRate_Coin = coin_detail_data.other_rate
                        Notes_Coin = coin_detail_data.notes
                        IsPopular_Coin = coin_detail_data.is_popular
                        Status_Coin = coin_detail_data.coin_status

                        coin_detail_list = {'Quantity_Coin':Quantity_Coin, 'IndianRate_Coin':IndianRate_Coin, 'OtherRate_Coin':OtherRate_Coin, 'Notes_Coin':Notes_Coin, 'IsPopular_Coin':IsPopular_Coin, 'Status_Coin':Status_Coin}
                        coin_detail_list = json.dumps(coin_detail_list)
                        coin_detail_list = json.loads(coin_detail_list)

                        msg = 'Success!'
                        return JsonResponse(coin_detail_list)
                    else:
                        Messages = "No id!"
                        return HttpResponse(Messages)

                if edit_form_bool == True:
                    id_param = request.POST.get("id")
                    if id_param is not None:
                        id = str(request.POST.get("id")).replace(' ', '')
                        if id != "":
                    
                            quantity_param = request.POST.get("quantity")
                            if quantity_param is not None:
                                quantity = str(request.POST.get("quantity")).replace(' ', '')
                                if quantity != "":
                                    if quantity.isnumeric():

                                        indian_rate_param = request.POST.get("indian_rate")
                                        if indian_rate_param is not None:
                                            indian_rate = str(request.POST.get("indian_rate")).replace(' ', '')
                                            if indian_rate != "":

                                                other_rate_param = request.POST.get("other_rate")
                                                if other_rate_param is not None:
                                                    other_rate = str(request.POST.get("other_rate")).replace(' ', '')
                                                    if other_rate != "":
                                                
                                                        notes_param = request.POST.get("notes")
                                                        if notes_param is not None:
                                                            notes = request.POST.get("notes")
                                                            if notes != "":
                                                        
                                                                is_popular_param = request.POST.get("is_popular")
                                                                if is_popular_param is not None:
                                                                    is_popular = str(request.POST.get("is_popular")).replace(' ', '')
                                                                    if is_popular != "":

                                                                        coin_status_param = request.POST.get("coin_status")
                                                                        if coin_status_param is not None:
                                                                            coin_status = str(request.POST.get("coin_status")).replace(' ', '')
                                                                            if coin_status != "":

                                                                                coin_detail_id = request.POST.get("id")
                                                                                Quantity_coin = request.POST.get("quantity")
                                                                                Indian_Rate_coin = request.POST.get("indian_rate")
                                                                                Other_Rate_coin = request.POST.get("other_rate")
                                                                                Note_coin = request.POST.get("notes")
                                                                                Is_Popular_coin = request.POST.get("is_popular")
                                                                                Coin_Status_coin = request.POST.get("coin_status")

                                                                                ipc = "0"
                                                                                if Is_Popular_coin == "true":
                                                                                    ipc="1"
                                                                                elif Is_Popular_coin == "false":
                                                                                    ipc="0"

                                                                                ip_block_list = coin_details.objects.get(id=coin_detail_id)
                                                                                ip_block_list.quantity = Quantity_coin
                                                                                ip_block_list.indian_rate = Indian_Rate_coin
                                                                                ip_block_list.other_rate = Other_Rate_coin
                                                                                ip_block_list.notes = Note_coin
                                                                                ip_block_list.is_popular = ipc
                                                                                ip_block_list.coin_status = Coin_Status_coin
                                                                                ip_block_list.save()
                                                                                
                                                                                msg = 'Success'
                                                                                return HttpResponse(msg)   
                                                                        
                                                                            else:
                                                                                msg = 'Coin Status is not Valid'
                                                                                return HttpResponse(msg)
                                                                        else:
                                                                            msg = 'Coin Status is Required'
                                                                            return HttpResponse(msg)
                                                                    else:
                                                                        msg = 'Popular is not Valid'
                                                                        return HttpResponse(msg)
                                                                else:
                                                                    msg = 'Popular is Required'
                                                                    return HttpResponse(msg)
                                                            else:
                                                                msg = 'Notes is Empty'
                                                                return HttpResponse(msg)
                                                        else:
                                                            msg = 'Notes is Required'
                                                            return HttpResponse(msg)
                                                    else:
                                                        msg = 'Other Rate is Empty'
                                                        return HttpResponse(msg)
                                                else:
                                                    msg = 'Other Rate is Required'
                                                    return HttpResponse(msg)
                                            else:
                                                msg = 'Indian Rate is Empty'
                                                return HttpResponse(msg)
                                        else:
                                            msg = 'Indian Rate is Required'
                                            return HttpResponse(msg)
                                    else:
                                        msg = 'Quantity is not Valid'
                                        return HttpResponse(msg)
                                else:
                                    msg = 'Quantity is Empty'
                                    return HttpResponse(msg)
                            else:
                                msg = 'Quantity is Required'
                                return HttpResponse(msg)
                        else:
                            msg = 'ID is not Valid'
                            return HttpResponse(msg)
                    else:
                        msg = 'ID is Required'
                        return HttpResponse(msg)    

                if delete_form_bool == True :
                    id_param = request.POST.get("id")
                    if id_param is not None:
                        id = str(request.POST.get("id")).replace(' ', '')
                        if id != "":

                            coin_details_id = request.POST.get("id")
                            coin_details.objects.filter(id=coin_details_id).delete()

                            msg = 'Success'
                            return HttpResponse(msg)

                        else:
                            msg = 'ID is not Valid'
                            return HttpResponse(msg)
                    else:
                        msg = 'ID is Required'
                        return HttpResponse(msg)

                quantity_param = request.POST.get("quantity")
                if quantity_param is not None:
                    quantity = str(request.POST.get("quantity")).replace(' ', '')
                    if quantity != "":
                        if quantity.isnumeric():

                            indian_rate_param = request.POST.get("indian_rate")
                            if indian_rate_param is not None:
                                indian_rate = str(request.POST.get("indian_rate")).replace(' ', '')
                                if indian_rate != "":

                                    other_rate_param = request.POST.get("other_rate")
                                    if other_rate_param is not None:
                                        other_rate = str(request.POST.get("other_rate")).replace(' ', '')
                                        if other_rate != "":

                                            notes_param = request.POST.get("notes")
                                            if notes_param is not None:
                                                notes = str(request.POST.get("notes")).replace(' ', '')
                                                if notes != "":

                                                    coin_status_param = request.POST.get("coin_status")
                                                    if coin_status_param is not None:
                                                        coin_status = str(request.POST.get("coin_status")).replace(' ', '')
                                                        if coin_status != "":
                                                    
                                                            is_popular_param = request.POST.get("is_popular")
                                                            if is_popular_param is not None:
                                                                is_popular = str(request.POST.get("is_popular")).replace(' ', '')
                                                                if is_popular != "":
                                                            
                                                                    Quantity = request.POST.get("quantity")
                                                                    IndianRate = request.POST.get("indian_rate")
                                                                    OtherRate = request.POST.get("other_rate")
                                                                    Notes = request.POST.get("notes")
                                                                    Popular = request.POST.get("is_popular")
                                                                    coin_status = request.POST.get("coin_status")
                                                                    
                                                                    a = "0"
                                                                    if Popular == "on":
                                                                        a = "1"

                                                                    coin_details.objects.create(quantity=Quantity, indian_rate=IndianRate, other_rate=OtherRate, notes=Notes, is_popular=a, coin_status=coin_status)
                                                                    return redirect('coindetails')
                                                                else:
                                                                    return redirect('coindetails')
                                                            else:

                                                                Quantity = request.POST.get("quantity")                  
                                                                IndianRate = request.POST.get("indian_rate")
                                                                OtherRate = request.POST.get("other_rate")
                                                                Notes = request.POST.get("notes")
                                                                coin_status = request.POST.get("coin_status")
                                                                coin_details.objects.create(quantity=Quantity, indian_rate=IndianRate, other_rate=OtherRate, notes=Notes, is_popular="0", coin_status=coin_status)
                                                                
                                                                return redirect('coindetails')
                                                        else:
                                                            messages.error(request, "Coin Status is not valid")
                                                            return redirect('coindetails')
                                                    else:
                                                        messages.error(request, "Coin Status is Required")
                                                        return redirect('coindetails')
                                                else:
                                                    messages.error(request, "Notes is Empty!")
                                                    return redirect('coindetails')
                                            else:
                                                messages.error(request, "Notes is Required")
                                                return redirect('coindetails')
                                        else:
                                            messages.error(request, "Other Rate is Empty!")
                                            return redirect('coindetails')
                                    else:
                                        messages.error(request, "Other Rate is Required")
                                        return redirect('coindetails')
                                else:
                                    messages.error(request, "Indian Rate is Empty!")
                                    return redirect('coindetails')
                            else:
                                messages.error(request, "Indian Rate is Required")
                                return redirect('coindetails')
                        else:
                            messages.error(request, "Quantity is not valid")
                            return redirect('coindetails')
                    else:
                        messages.error(request, "Quantity is Empty!")
                        return redirect('coindetails')
                else:
                    messages.error(request, "Quantity is Required")
                    return redirect('coindetails')

        else:
            return redirect('admin')

# IP BLOCK
class Ip_Block(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:
            IPBlock = check_ip_addresses.objects.all().order_by("-id")
            page = request.GET.get('page', 1)

            paginator = Paginator(IPBlock, 100)
            try:
                IPBlock_data = paginator.page(page)
            except PageNotAnInteger:
                IPBlock_data  = paginator.page(1)
            except EmptyPage:
                IPBlock_data  = paginator.page(paginator.num_pages)
            return render(request, 'ip_block.html', {'IPBlock':IPBlock_data })
        else:
            return redirect('admin')

    def post(self, request):
        if request.session.get('email') and request.session.get('email') != None:

            delete_form_bool = False
            delete_form_param = request.POST.get('delete_form')
            if delete_form_param is not None:
                delete_form_bool = True
            
            if delete_form_bool == True :
                id_param = request.POST.get("id")
                if id_param is not None:
                    id = request.POST.get("id").replace(' ', '')
                    if id != "":

                        ipblock_id = request.POST.get("id")
                        check_ip_addresses.objects.filter(id=ipblock_id).delete()

                        msg = 'Success'
                        return HttpResponse(msg)
                    else:
                        msg = 'ID is not Valid'
                        return HttpResponse(msg)
                else:
                    msg = 'ID is Required'
                    return HttpResponse(msg)

            ip_address_param = request.POST.get("ip_address")
            if ip_address_param is not None:
                ip_address = str(request.POST.get("ip_address")).replace(' ', '').replace('-','')
               
                if ip_address != "" and  socket.inet_aton(ip_address):
                    ip_check = check_ip_addresses.objects.filter(ip=request.POST.get("ip_address"))
                    ip_list=[]
                    for i in ip_check:
                        ip_list.append(i.ip)
                    if ip_address in ip_list:
                            messages.error(request, "IP Address is Already Exiest!")
                            return redirect('ipblock')
                    else:
                        status_param = request.POST.get("status")
                        if status_param is not None:
                            status = str(request.POST.get("status")).replace(' ', '')
                            if status != "":
                                IP_Block = str(request.POST.get("ip_address")).replace('-','')
                                Status = request.POST.get("status")
                                check_ip_addresses.objects.create(ip=IP_Block, status=Status)
                                return redirect('ipblock')
                            else:
                                messages.error(request, "Status is not valid")
                                return redirect('ipblock')
                        else:
                            messages.error(request, "Status is Required")
                            return redirect('ipblock')
                else:
                    messages.error(request, "IP Address is Empty!")
                    return redirect('ipblock')
            else:
                messages.error(request, "IP Address is Required")
                return redirect('ipblock')
        else:
            return redirect('admin')

# MANAGE PROFILE
class Manage_Profile(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:
            superusers = User.objects.get(username=request.session.get('email'))
            return render(request, 'manage_profile.html', {'superusers':superusers})
        else:
            return redirect('admin')

    def post(self, request):
        if request.session.get('email') and request.session.get('email') != None:
            email = request.session.get('email')

            current_password_param = request.POST.get("current_password")
            if current_password_param is not None:
                current_password = request.POST.get("current_password").replace(' ', '')
                if current_password != "":

                    current_password = request.POST.get("current_password")
                    user = authenticate(username=email, password=current_password)

                    if user is not None:

                        new_password_param = request.POST.get("new_password")
                        if new_password_param is not None:
                            new_password = request.POST.get("new_password").replace(' ', '')
                            if new_password != "":
                                new_password = request.POST.get("new_password")
                        
                                new_confirm_password_param = request.POST.get("new_confirm_password")
                                if new_confirm_password_param is not None:
                                    new_confirm_password = request.POST.get("new_confirm_password").replace(' ', '')
                                    if new_confirm_password != "":
                                        new_confirm_password = request.POST.get("new_confirm_password")

                                        if current_password != new_password:
                                            if new_password == new_confirm_password:

                                                new_pass = User.objects.get(username=email)
                                                new_pass.set_password(new_password)
                                                new_pass.save()
                                                messages.success(request, "Password successfully Changed!")
                                                request.session.flush() # cookie delete
                                                request.session.clear_expired() # cookie delete in data-base
                                                return redirect('manageprofile')
                                            else:
                                                messages.error(request, "Password Does Not Match!")
                                                return redirect('manageprofile')
                                        else:
                                            messages.error(request, "Current Password and New Password are Match! Enter Different Password.")
                                            return redirect('manageprofile')
                                    else:
                                        messages.error(request, "Confirm Password is Empty!")
                                        return redirect('manageprofile')
                                else:
                                    messages.error(request, "Confirm Password is Required!")
                                    return redirect('manageprofile')
                            else:
                                messages.error(request, "New Password is Empty!")
                                return redirect('manageprofile')
                        else:
                            messages.error(request, "New Password is Required!")
                            return redirect('manageprofile')
                    else:
                        messages.error(request, "Current Password Does Not Match!")
                        return redirect('manageprofile')
                else:
                    messages.error(request, "Current Password is Empty!")
                    return redirect('manageprofile')
            else:
                messages.error(request, "Current Password is Required!")
                return redirect('manageprofile')
        else:
            return redirect('admin')

# OTHER LISTS
class Active_Order_List(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:

            date_bool = False
            active_order_usertype_bool = False
            start_date = request.GET.get('active_order_start_date')
            end_date = request.GET.get('active_order_end_date')
            search_field = request.GET.get('active_order_usertype')

            start_date_param = request.GET.get('active_order_start_date')
            if start_date_param is not None:
                if str(start_date_param).replace(" ","") != "":
                    start_date = request.GET.get('active_order_start_date')
                    start_all_array = str(start_date).split('/')
                    start_date_up = str(start_all_array[2])+'-'+str(start_all_array[0])+'-'+str(start_all_array[1])+' 00:00'
                    date_bool = True
             
            end_date_param = request.GET.get('active_order_end_date')
            if end_date_param is not None:
                if str(end_date_param).replace(" ","") != "":
                    end_date = request.GET.get('active_order_end_date')
                    end_all_array = str(end_date).split('/')
                    end_date_up = str(end_all_array[2])+'-'+str(end_all_array[0])+'-'+str(end_all_array[1])+' 00:00'
                    date_bool = True
            
            search_field_param = request.GET.get('active_order_usertype')
            if search_field_param is not None:
                search_field = request.GET.get('active_order_usertype')
                if str(search_field).replace(" ","") != '':
                    active_order_usertype_bool = True
            
            search_type = request.GET.get("active_order_usertype_select")
            if date_bool == True:

                start_date_param = request.GET.get('active_order_start_date')
                end_date_param = request.GET.get('active_order_end_date')
                if start_date_param and end_date_param is not None:
                    start_date = request.GET.get('active_order_start_date')
                    end_date = request.GET.get('active_order_end_date')
                   
                else:
                    messages.info(request, "Start and end both date are required!")
                    return redirect('activeorder')
                    
                if active_order_usertype_bool == True:

                    if request.GET.get("active_order_usertype_select") == "0":
                        user_id = request.GET.get("active_order_usertype")
                        order_list = orders.objects.filter(~Q(needed="0"),user_id=user_id, created_at__gte=start_date_up, created_at__lte=end_date_up, order_status='1')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(order_list, 100)
                        try:
                            order_data = paginator.page(page)
                        except PageNotAnInteger:
                            order_data = paginator.page(1)
                        except EmptyPage:
                            order_data = paginator.page(paginator.num_pages)
                        return render(request, 'active_order.html', {'order_list':order_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("active_order_usertype_select") == "1":
                        custom_user_id = request.GET.get("all_order_usertype")
                        order_list = orders.objects.filter(~Q(needed="0"),custom_user_id=custom_user_id, created_at__gte=start_date_up, created_at__lte=end_date_up, order_status='1')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(order_list, 100)
                        try:
                            order_data = paginator.page(page)
                        except PageNotAnInteger:
                            order_data = paginator.page(1)
                        except EmptyPage:
                            order_data = paginator.page(paginator.num_pages)
                        return render(request, 'active_order.html', {'order_list':order_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("active_order_usertype_select") == "2":
                        post_id = request.GET.get("active_order_usertype")
                        order_list = orders.objects.filter(~Q(needed="0"),post_id=post_id, created_at__gte=start_date_up, created_at__lte=end_date_up, order_status='1')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(order_list, 100)
                        try:
                            order_data = paginator.page(page)
                        except PageNotAnInteger:
                            order_data = paginator.page(1)
                        except EmptyPage:
                            order_data = paginator.page(paginator.num_pages)
                        return render(request, 'active_order.html', {'order_list':order_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})
                    
                else:
                    order_list = orders.objects.filter(~Q(needed="0"),created_at__gte=start_date_up, created_at__lte=end_date_up, order_status='1')
                    page = request.GET.get('page', 1)

                    paginator = Paginator(order_list, 100)
                    try:
                        order_data = paginator.page(page)
                    except PageNotAnInteger:
                        order_data = paginator.page(1)
                    except EmptyPage:
                        order_data = paginator.page(paginator.num_pages)
                    return render(request, 'active_order.html', {'order_list':order_data,'start_date':start_date,'end_date':end_date})

            else:
                if active_order_usertype_bool == True:
                    if request.GET.get("active_order_usertype_select") == "0":
                        user_id = request.GET.get("active_order_usertype")
                        order_list = orders.objects.filter(~Q(needed="0"),user_id=user_id, order_status='1')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(order_list, 100)
                        try:
                            order_data = paginator.page(page)
                        except PageNotAnInteger:
                            order_data = paginator.page(1)
                        except EmptyPage:
                            order_data = paginator.page(paginator.num_pages)
                        return render(request, 'active_order.html', {'order_list':order_data,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("active_order_usertype_select") == "1":
                        custom_user_id = request.GET.get("active_order_usertype")
                        order_list = orders.objects.filter(~Q(needed="0"),custom_user_id=custom_user_id, order_status='1')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(order_list, 100)
                        try:
                            order_data = paginator.page(page)
                        except PageNotAnInteger:
                            order_data = paginator.page(1)
                        except EmptyPage:
                            order_data = paginator.page(paginator.num_pages)
                        return render(request, 'active_order.html', {'order_list':order_data,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("active_order_usertype_select") == "2":
                        post_id = request.GET.get("active_order_usertype")
                        order_list = orders.objects.filter(~Q(needed="0"),post_id=post_id, order_status='1')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(order_list, 100)
                        try:
                            order_data = paginator.page(page)
                        except PageNotAnInteger:
                            order_data = paginator.page(1)
                        except EmptyPage:
                            order_data = paginator.page(paginator.num_pages)
                        return render(request, 'active_order.html', {'order_list':order_data,'search_field':search_field,'search_type':search_type})

            order_list = orders.objects.filter(~Q(needed="0"),order_status='1').order_by("-id")
            page = request.GET.get('page', 1)

            paginator = Paginator(order_list, 100)
            try:
                order_data = paginator.page(page)
            except PageNotAnInteger:
                order_data = paginator.page(1)
            except EmptyPage:
                order_data = paginator.page(paginator.num_pages)
            return render(request, 'active_order.html',{'order_list':order_data})
        else:
            return redirect('admin')

    def post(self,request):
        if request.session.get('email') and request.session.get('email') != None:

            type_bool = False
            edit_form_bool = False
            delete_form_bool = False

            type_param = request.POST.get('type')
            if type_param is not None:
                type_bool = True
            
            edit_form_param = request.POST.get('edit_form')
            if edit_form_param is not None:
                edit_form_bool = True
            
            delete_form_param = request.POST.get('delete_form')
            if delete_form_param is not None:
                delete_form_bool = True
            

            if type_bool == True:

                id_param = request.POST.get("id")
                if id_param is not None:
                    order_id = request.POST.get("id")

                    all_order_data = orders.objects.get(id=order_id)
                    Needed = all_order_data.needed
                    Recieved = all_order_data.recieved
                    no_like_log = all_order_data.no_like_log

                    all_order_list = {'Needed':Needed, 'Recieved':Recieved, 'no_like_log':no_like_log}
                    all_order_list = json.dumps(all_order_list)
                    all_order_list = json.loads(all_order_list)

                    msg = 'Success!'
                    return JsonResponse(all_order_list)
                else:
                    Messages = "No id!"
                    return HttpResponse(Messages)

            if edit_form_bool == True:

                id_param = request.POST.get("id")
                if id_param is not None:
                    id = str(request.POST.get("id")).replace(' ', '')
                    if id != "":

                        needed_param = request.POST.get("needed")
                        if needed_param is not None:
                            needed = str(request.POST.get("needed")).replace(' ', '')
                            if needed != "":
                                if needed.isnumeric():
                                    if int(needed)>=0:

                                        received_param = request.POST.get("received")
                                        if received_param is not None:
                                            received = str(request.POST.get("received")).replace(' ', '')
                                            if received != "":
                                                if received.isnumeric():

                                                    no_like_log_param = request.POST.get("no_like_log")
                                                    if no_like_log_param is not None:
                                                        no_like_log = str(request.POST.get("no_like_log")).replace(' ', '')
                                                        if no_like_log != "":
                                                            if no_like_log.isnumeric():

                                                                user_id_like = request.POST.get("id")
                                                                Needed = request.POST.get("needed")
                                                                Received = request.POST.get("received")
                                                                no_like_log = request.POST.get("no_like_log")

                                                                all_active_list = orders.objects.get(id=user_id_like)
                                                                all_active_list.needed = Needed
                                                                all_active_list.recieved = Received
                                                                all_active_list.no_like_log = no_like_log
                                                                all_active_list.save()
                                                                
                                                                msg = 'Success'
                                                                return HttpResponse(msg)   
                                                            else:
                                                                msg = 'No_like_log is Integer'
                                                                return HttpResponse(msg)
                                                        else:
                                                            msg = 'No_like_log is not Valid'
                                                            return HttpResponse(msg)
                                                    else:
                                                        msg = 'No_like_log is Required'
                                                        return HttpResponse(msg)
                                                else:
                                                    msg = 'Received is Integer'
                                                    return HttpResponse(msg)
                                            else:
                                                msg = 'Received is not Valid'
                                                return HttpResponse(msg)
                                        else:
                                            msg = 'Received is Required'
                                            return HttpResponse(msg)
                                    else:
                                        msg = 'Needed is Not Less then 0!'
                                        return HttpResponse(msg)
                                else:
                                    msg = 'Enter needed in an integer'
                                    return HttpResponse(msg)
                            else:
                                msg = 'Needed is not Valid'
                                return HttpResponse(msg)
                        else:
                            msg = 'Needed is Required'
                            return HttpResponse(msg)
                    else:
                        msg = 'ID is not Valid'
                        return HttpResponse(msg)
                else:
                    msg = 'ID is Required'
                    return HttpResponse(msg)    

            if delete_form_bool == True :
                id_param = request.POST.get("id")
                if id_param is not None:
                    id = str(request.POST.get("id")).replace(' ', '')
                    if id != "":

                        user_id_active_order = request.POST.get("id")
                        order_dd = orders.objects.get(id=user_id_active_order)
                        orders.objects.filter(id=user_id_active_order).delete()
                        user_data = users.objects.get(user_id = order_dd.user_id)
                        app_data_dic = app_data.objects.get()
                        
                        if (int(order_dd.needed) - int(order_dd.recieved)) > 0:

                            remains = int(order_dd.needed) - int(order_dd.recieved)
                            total_coins = user_data.total_coins
                            if order_dd.type == "0":
                                update_coin = int(total_coins) + (remains*int(app_data_dic.spent_like_coin))
                                nofify_coin = (remains*int(app_data_dic.spent_like_coin))
                            elif order_dd.type == "1":
                                update_coin = int(total_coins) + (remains*int(app_data_dic.spent_follow_coin))
                                nofify_coin = (remains*int(app_data_dic.spent_follow_coin))
                            user_data.total_coins = update_coin
                            user_data.save()

                            title = "Coin refunded"
                            body_desc = str(nofify_coin) + " coin refunded"
                            registration_token = user_data.ftoken
                            send_notification(title,body_desc,registration_token)
                            

                        msg = 'Success'
                        return HttpResponse(msg)

                    else:
                        msg = 'ID is not Valid'
                        return HttpResponse(msg)
                else:
                    msg = 'ID is Required'
                    return HttpResponse(msg)

            order_type_bool = False
            order_type_param = request.POST.get('order_type')
            if order_type_param is not None:
                order_type_bool = True
            
            if order_type_bool == True:
                order_type_param = request.POST.get('order_type')
                if order_type_param is not None:
                    order_type = str(request.POST.get("order_type")).replace(' ', '')
                    if order_type != "":

                        user_id_param = request.POST.get('user_id')
                        if user_id_param is not None:
                            user_id = str(request.POST.get("user_id")).replace(' ', '')
                            if user_id != "":
                                if users.objects.filter(user_id=request.POST.get("user_id")).exists():
                                    users.objects.get(user_id=request.POST.get("user_id"))
                                else:
                                    messages.error(request, "User is not Register!")
                                    return redirect('activeorder')

                                custom_user_id_param = request.POST.get("custom_user_id")
                                if custom_user_id_param is not None:
                                    custom_user_id = str(request.POST.get("custom_user_id")).replace(' ', '')
                                    if custom_user_id != "":

                                        needed_param = request.POST.get("needed")
                                        if needed_param is not None:
                                            needed = str(request.POST.get("needed")).replace(' ', '')
                                            if needed != "":
                                                if needed.isnumeric():
                                                    if int(needed)>=0:

                                                        order_status_param = request.POST.get("order_status")
                                                        if order_status_param is not None:
                                                            order_status = str(request.POST.get("order_status")).replace(' ', '')
                                                            if order_status != "":

                                                                image_param = request.FILES.get('file')
                                                                if image_param is not None:
                                                                    image = request.FILES.get('file')
                                                                    filename, file_extension = str(image).split(".")
                                                                    file_extension = file_extension.lower()
                                                                    file_extension = "."+file_extension
                                                                    if file_extension == '.jpeg' or file_extension == '.jpg' or file_extension == '.png' or file_extension == '.gif' or file_extension == '.tiff' or file_extension == '.psd' or file_extension == '.pdf' or file_extension == '.eps' or file_extension == '.ai' or file_extension == '.indd' or file_extension == '.raw' :

                                                                        order_type = request.POST.get("order_type")
                                                                        user_id = request.POST.get("user_id")
                                                                        custom_user_id = request.POST.get("custom_user_id")
                                                                        needed = request.POST.get("needed")
                                                                        order_status = request.POST.get("order_status")

                                                                        if order_type == '0':

                                                                            short_code_param = request.POST.get("short_code")
                                                                            if short_code_param is not None:
                                                                                short_code = str(request.POST.get("short_code")).replace(' ', '')
                                                                                if short_code != "":

                                                                                    post_id_param = request.POST.get("post_id")
                                                                                    if post_id_param is not None:
                                                                                        post_id = str(request.POST.get("post_id")).replace(' ', '')
                                                                                        if post_id != "":

                                                                                            post_id = request.POST.get("post_id")
                                                                                            image_unique_id = str(uuid.uuid4())
                                                                                            image_file = str(post_id) + file_extension
                                                                                            file = base_url + 'static/img/like/'+ image_file
                                                                                            short_code = request.POST.get("short_code")
                                                                                            img = request.FILES['file']
                                                                                            fs = FileSystemStorage(location=like_URL, base_url=None)
                                                                                            filename = fs.save(image_file, img)
                                                                                            uploaded_file_url = fs.url(filename)
                                                                                            
                                                                                            orders.objects.create(type=order_type, user_id=user_id, custom_user_id=custom_user_id, needed=needed, image_url=image_file, short_code=short_code, post_id=post_id, order_status = order_status)
                                                                                            return redirect('activeorder')
                                                                                        else:
                                                                                            messages.error(request, "Post ID is not valid")
                                                                                            return redirect('activeorder')
                                                                                    else:
                                                                                        messages.error(request, "Post ID is Required")
                                                                                        return redirect('activeorder')
                                                                                else:
                                                                                    messages.error(request, "Short Code is not valid")
                                                                                    return redirect('activeorder')
                                                                            else:
                                                                                messages.error(request, "Shoet Code is Required")
                                                                                return redirect('activeorder')
                                                                        elif order_type == '1':
                                                                            username_param = request.POST.get("username")
                                                                            if username_param is not None:
                                                                                username = str(request.POST.get("username")).replace(' ', '')
                                                                                if username != "":

                                                                                    username = request.POST.get("username")

                                                                                    image_unique_id = str(uuid.uuid4())
                                                                                    image_file = str(custom_user_id) + file_extension
                                                                                    file = base_url + 'static/img/follow/'+ image_file
                                                                                    img = request.FILES['file']
                                                                                    fs = FileSystemStorage(location=follow_URL, base_url=None)
                                                                                    filename = fs.save(image_file, img)
                                                                                    uploaded_file_url = fs.url(filename)

                                                                                    orders.objects.create(type=order_type, user_id=user_id, custom_user_id=custom_user_id, needed=needed, image_url=image_file, username=username, order_status = order_status)
                                                                                    return redirect('activeorder')
                                                                            else:
                                                                                messages.error(request, "username is not valid")
                                                                                return redirect('activeorder')
                                                                        else:
                                                                            messages.error(request, "type is not valid")
                                                                            return redirect('activeorder')
                                                                    else:
                                                                        messages.error(request, "Image is not valid")
                                                                        return redirect('activeorder')
                                                                else:
                                                                    messages.error(request, "Image is Required")
                                                                    return redirect('activeorder')
                                                            else:
                                                                messages.error(request, "Order status is not valid")
                                                                return redirect('activeorder')
                                                        else:
                                                            messages.error(request, "Order status is Required")
                                                            return redirect('activeorder')
                                                    else:
                                                        messages.error(request, "Enter Valid an integer")
                                                        return redirect('activeorder')
                                                else:
                                                    messages.error(request, "Enter needed in an integer")
                                                    return redirect('activeorder')
                                            else:
                                                messages.error(request, "Needed is not valid")
                                                return redirect('activeorder')
                                        else:
                                            messages.error(request, "Needed is Required")
                                            return redirect('activeorder')
                                    else:
                                        messages.error(request, "Custom User ID is not valid")
                                        return redirect('activeorder')
                                else:
                                    messages.error(request, "Custom User ID is Required")
                                    return redirect('activeorder')
                            else:
                                messages.error(request, "User ID is not valid")
                                return redirect('activeorder')
                        else:
                            messages.error(request, "User ID is Required")
                            return redirect('activeorder')
                    else:
                        messages.error(request, "Order Type is not valid")
                        return redirect('activeorder')
                else:
                    messages.error(request, "Order Type is Required")
                    return redirect('activeorder')
            return redirect('activeorder')
        else:
            return redirect('admin')

class All_Order(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:
            date_bool = False
            all_order_usertype_bool = False
            start_date = request.GET.get('all_order_startdate')
            end_date = request.GET.get('all_order_enddate')
            search_field = request.GET.get('all_order_usertype')

            start_date_param = request.GET.get('all_order_startdate')
            if start_date_param is not None:
                if str(start_date_param).replace(" ","") != "":
                    start_date = request.GET.get('all_order_startdate')
                    start_all_array = str(start_date).split('/')
                    start_date_up = str(start_all_array[2])+'-'+str(start_all_array[0])+'-'+str(start_all_array[1])+' 00:00'
                    date_bool = True
              
            end_date_param = request.GET.get('all_order_enddate')
            if end_date_param is not None:
                if str(end_date_param).replace(" ","") != "":
                    end_date = request.GET.get('all_order_enddate')
                    end_all_array = str(end_date).split('/')
                    end_date_up = str(end_all_array[2])+'-'+str(end_all_array[0])+'-'+str(end_all_array[1])+' 00:00'
                    date_bool = True
              
            search_field_param = request.GET.get('all_order_usertype')
            if search_field_param is not None:
                search_field = request.GET.get('all_order_usertype')
                if str(search_field).replace(" ","") != '':
                    all_order_usertype_bool = True
            
            search_type = request.GET.get("all_order_usertype_select")
            if date_bool == True:

                start_date_param = request.GET.get('all_order_startdate')
                end_date_param = request.GET.get('all_order_enddate')
                if start_date_param and end_date_param is not None:
                    start_date = request.GET.get('all_order_startdate')
                    end_date = request.GET.get('all_order_enddate')
                   
                else:
                    messages.info(request, "Start and end both date are required!")
                    return redirect('allorder')
                    
                if all_order_usertype_bool == True:

                    if request.GET.get("all_order_usertype_select") == "0":
                        user_id = request.GET.get("all_order_usertype")
                        all_order_list = orders.objects.filter(user_id=user_id, created_at__gte=start_date_up, created_at__lte=end_date_up)
                        page = request.GET.get('page', 1)

                        paginator = Paginator(all_order_list, 100)
                        try:
                            all_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            all_order_data = paginator.page(1)
                        except EmptyPage:
                            all_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'all_order.html', {'all_order_list':all_order_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("all_order_usertype_select") == "1":
                        custom_user_id = request.GET.get("all_order_usertype")
                        all_order_list = orders.objects.filter(custom_user_id=custom_user_id, created_at__gte=start_date_up, created_at__lte=end_date_up)
                        page = request.GET.get('page', 1)

                        paginator = Paginator(all_order_list, 100)
                        try:
                            all_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            all_order_data = paginator.page(1)
                        except EmptyPage:
                            all_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'all_order.html', {'all_order_list':all_order_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("all_order_usertype_select") == "2":
                        post_id = request.GET.get("all_order_usertype")
                        all_order_list = orders.objects.filter(post_id=post_id, created_at__gte=start_date_up, created_at__lte=end_date_up)
                        page = request.GET.get('page', 1)

                        paginator = Paginator(all_order_list, 100)
                        try:
                            all_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            all_order_data = paginator.page(1)
                        except EmptyPage:
                            all_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'all_order.html', {'all_order_list':all_order_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("all_order_usertype_select") == "3":
                        short_code = request.GET.get("all_order_usertype")
                        all_order_list = orders.objects.filter(short_code=short_code, created_at__gte=start_date_up, created_at__lte=end_date_up)
                        page = request.GET.get('page', 1)

                        paginator = Paginator(all_order_list, 100)
                        try:
                            all_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            all_order_data = paginator.page(1)
                        except EmptyPage:
                            all_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'all_order.html', {'all_order_list':all_order_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})
                    
                else:
                    all_order_list = orders.objects.filter(created_at__gte=start_date_up, created_at__lte=end_date_up)
                    page = request.GET.get('page', 1)

                    paginator = Paginator(all_order_list, 100)
                    try:
                        all_order_data = paginator.page(page)
                    except PageNotAnInteger:
                        all_order_data = paginator.page(1)
                    except EmptyPage:
                        all_order_data = paginator.page(paginator.num_pages)
                    return render(request, 'all_order.html', {'all_order_list':all_order_data,'start_date':start_date,'end_date':end_date})

            else:
                if all_order_usertype_bool == True:
                    if request.GET.get("all_order_usertype_select") == "0":
                        user_id = request.GET.get("all_order_usertype")
                        all_order_list = orders.objects.filter(user_id=user_id)
                        page = request.GET.get('page', 1)

                        paginator = Paginator(all_order_list, 100)
                        try:
                            all_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            all_order_data = paginator.page(1)
                        except EmptyPage:
                            all_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'all_order.html', {'all_order_list':all_order_data,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("all_order_usertype_select") == "1":
                        custom_user_id = request.GET.get("all_order_usertype")
                        all_order_list = orders.objects.filter(custom_user_id=custom_user_id)
                        page = request.GET.get('page', 1)

                        paginator = Paginator(all_order_list, 100)
                        try:
                            all_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            all_order_data = paginator.page(1)
                        except EmptyPage:
                            all_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'all_order.html', {'all_order_list':all_order_data,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("all_order_usertype_select") == "2":
                        post_id = request.GET.get("all_order_usertype")
                        all_order_list = orders.objects.filter(post_id=post_id)
                        page = request.GET.get('page', 1)

                        paginator = Paginator(all_order_list, 100)
                        try:
                            all_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            all_order_data = paginator.page(1)
                        except EmptyPage:
                            all_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'all_order.html', {'all_order_list':all_order_data,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("all_order_usertype_select") == "3":
                        short_code = request.GET.get("all_order_usertype")
                        all_order_list = orders.objects.filter(short_code=short_code)
                        page = request.GET.get('page', 1)

                        paginator = Paginator(all_order_list, 100)
                        try:
                            all_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            all_order_data = paginator.page(1)
                        except EmptyPage:
                            all_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'all_order.html', {'all_order_list':all_order_data,'search_field':search_field,'search_type':search_type})
                    

            all_order_list = orders.objects.all().order_by("-id")
            page = request.GET.get('page', 1)

            paginator = Paginator(all_order_list, 100)
            try:
                all_order_data = paginator.page(page)
            except PageNotAnInteger:
                all_order_data = paginator.page(1)
            except EmptyPage:
                all_order_data = paginator.page(paginator.num_pages)
            return render(request, 'all_order.html', {'all_order_list':all_order_data})
        else:
            return redirect('admin')

    def post(self,request):
        if request.session.get('email') and request.session.get('email') != None:

            type_bool = False
            edit_form_bool = False
            delete_form_bool = False

            type_param = request.POST.get('type')
            if type_param is not None:
                type_bool = True
            
            edit_form_param = request.POST.get('edit_form')
            if edit_form_param is not None:
                edit_form_bool = True
            
            delete_form_param = request.POST.get('delete_form')
            if delete_form_param is not None:
                delete_form_bool = True
            
            if type_bool == True:
                id_param = request.POST.get("id")
                if id_param is not None:
                    order_id = request.POST.get("id")

                    all_order_data = orders.objects.get(id=order_id)
                    Needed = all_order_data.needed
                    Recieved = all_order_data.recieved

                    all_order_list = {'Needed':Needed, 'Recieved':Recieved}
                    all_order_list = json.dumps(all_order_list)
                    all_order_list = json.loads(all_order_list)

                    msg = 'Success!'
                    return JsonResponse(all_order_list)
                else:
                    Messages = "No id!"
                    return HttpResponse(Messages)

            if edit_form_bool == True:
                id_param = request.POST.get("id")
                if id_param is not None:
                    id = str(request.POST.get("id")).replace(' ', '')
                    if id != "":

                        needed_param = request.POST.get("needed")
                        if needed_param is not None:
                            needed = str(request.POST.get("needed")).replace(' ', '')
                            if needed != "":
                                if needed.isnumeric():
                                    if int(needed)>=0:

                                        received_param = request.POST.get("received")
                                        if received_param is not None:
                                            received = str(request.POST.get("received")).replace(' ', '')
                                            if received != "":
                                                if received.isnumeric():

                                                    user_id_orders = request.POST.get("id")
                                                    Needed = request.POST.get("needed")
                                                    Received = request.POST.get("received")

                                                    all_order_list = orders.objects.get(id=user_id_orders)
                                                    all_order_list.needed = Needed
                                                    all_order_list.recieved = Received
                                                    all_order_list.save()
                                                    
                                                    msg = 'Success'
                                                    return HttpResponse(msg)   
                                                else:
                                                    msg = 'Received is in Integer'
                                                    return HttpResponse(msg)
                                            else:
                                                msg = 'Received is not Valid'
                                                return HttpResponse(msg)
                                        else:
                                            msg = 'Received is Required'
                                            return HttpResponse(msg)
                                    else:
                                        msg = 'Enter Valid an integer'
                                        return HttpResponse(msg)
                                else:
                                    msg = 'Enter needed in an integer'
                                    return HttpResponse(msg)
                            else:
                                msg = 'Needed is not Valid'
                                return HttpResponse(msg)
                        else:
                            msg = 'Needed is Required'
                            return HttpResponse(msg)
                    else:
                        msg = 'ID is not Valid'
                        return HttpResponse(msg)
                else:
                    msg = 'ID is Required'
                    return HttpResponse(msg)    

            if delete_form_bool == True :
                id_param = request.POST.get("id")
                if id_param is not None:
                    id = str(request.POST.get("id")).replace(' ', '')
                    if id != "":

                        order_id = request.POST.get("id")

                        order_dd = orders.objects.get(id=order_id)
                        orders.objects.filter(id=order_id).delete()
                        user_data = users.objects.get(user_id = order_dd.user_id)
                        app_data_dic = app_data.objects.get()
                        
                        if (int(order_dd.needed) - int(order_dd.recieved)) > 0:

                            remains = int(order_dd.needed) - int(order_dd.recieved)
                            total_coins = user_data.total_coins
                            if order_dd.type == "0":
                                update_coin = int(total_coins) + (remains*int(app_data_dic.spent_like_coin))
                                nofify_coin = (remains*int(app_data_dic.spent_like_coin))
                            elif order_dd.type == "1":
                                update_coin = int(total_coins) + (remains*int(app_data_dic.spent_follow_coin))
                                nofify_coin = (remains*int(app_data_dic.spent_follow_coin))
                            
                            user_data.total_coins = update_coin
                            user_data.save()

                            title = "Coin refunded"
                            body_desc = str(nofify_coin) + " coin refunded"
                            registration_token = user_data.ftoken
                            send_notification(title,body_desc,registration_token)

                        msg = 'Success'
                        return HttpResponse(msg)

                    else:
                        msg = 'ID is not Valid'
                        return HttpResponse(msg)
                else:
                    msg = 'ID is Required'
                    return HttpResponse(msg)

            order_type_bool = False
            order_type_param = request.POST.get('order_type')
            if order_type_param is not None:
                order_type_bool = True
            
            if order_type_bool == True:
                order_type_param = request.POST.get("order_type")
                if order_type_param is not None:
                    order_type = str(request.POST.get("order_type")).replace(' ', '')
                    if order_type != "":

                        user_id_param = request.POST.get("user_id")
                        if user_id_param is not None:
                            user_id = str(request.POST.get("user_id")).replace(' ', '')
                            if user_id != "":
                                if users.objects.filter(user_id=request.POST.get("user_id")).exists():
                                    users.objects.get(user_id=request.POST.get("user_id"))
                                else:
                                    messages.error(request, "User is not Register!")
                                    return redirect('allorder')

                                custom_user_id_param = request.POST.get("custom_user_id")
                                if custom_user_id_param is not None:
                                    custom_user_id = str(request.POST.get("custom_user_id")).replace(' ', '')
                                    if custom_user_id != "":

                                        needed_param = request.POST.get("needed")
                                        if needed_param is not None:
                                            needed = str(request.POST.get("needed")).replace(' ', '')
                                            if needed != "":
                                                if needed.isnumeric():
                                                    if int(needed)>=0:

                                                        order_status_param = request.POST.get("order_status")
                                                        if order_status_param is not None:
                                                            order_status = str(request.POST.get("order_status")).replace(' ', '')
                                                            if order_status != "":

                                                                image_param = request.FILES.get('file')
                                                                if image_param is not None:
                                                                    image = request.FILES.get('file')
                                                                    filename, file_extension = str(image).split(".")
                                                                    file_extension = file_extension.lower()
                                                                    file_extension = "."+file_extension

                                                                    if file_extension == '.jpeg' or file_extension == '.jpg' or file_extension == '.png' or file_extension == '.gif' or file_extension == '.tiff' or file_extension == '.psd' or file_extension == '.pdf' or file_extension == '.eps' or file_extension == '.ai' or file_extension == '.indd' or file_extension == '.raw' :

                                                                        order_type = request.POST.get("order_type")
                                                                        user_id = request.POST.get("user_id")
                                                                        custom_user_id = request.POST.get("custom_user_id")
                                                                        needed = request.POST.get("needed")
                                                                        order_status = request.POST.get("order_status")
                                                                        
                                                                        if order_type == '0':
                                                                            short_code_param = request.POST.get("short_code")
                                                                            if short_code_param is not None:
                                                                                short_code = str(request.POST.get("short_code")).replace(' ', '')
                                                                                if short_code != "":

                                                                                    post_id_param = request.POST.get("post_id")
                                                                                    if post_id_param is not None:
                                                                                        post_id = str(request.POST.get("post_id")).replace(' ', '')
                                                                                        if post_id != "":

                                                                                            post_id = request.POST.get("post_id")
                                                                                            image_unique_id = str(uuid.uuid4())
                                                                                            image_file = str(post_id) + file_extension
                                                                                            file = base_url + 'static/img/like/'+ image_file
                                                                                            short_code = request.POST.get("short_code")
                                                                                            img = request.FILES['file']

                                                                                            fs = FileSystemStorage(location=like_URL, base_url=None)
                                                                                            filename = fs.save(image_file, img)
                                                                                            uploaded_file_url = fs.url(filename)
                                                                                            
                                                                                            orders.objects.create(type=order_type, user_id=user_id, custom_user_id=custom_user_id, needed=needed, image_url=image_file, short_code=short_code, post_id=post_id, order_status=order_status)
                                                                                            return redirect('allorder')
                                                                                        else:
                                                                                            messages.error(request, "Post ID is not valid")
                                                                                            return redirect('allorder')
                                                                                    else:
                                                                                        messages.error(request, "Post ID is Required")
                                                                                        return redirect('allorder')
                                                                                else:
                                                                                    messages.error(request, "Short Code is not valid")
                                                                                    return redirect('allorder')
                                                                            else:
                                                                                messages.error(request, "Shoet Code is Required")
                                                                                return redirect('allorder')
                                                                        elif order_type == '1':
                                                                            username_param = request.POST.get("username")
                                                                            if username_param is not None:
                                                                                username = str(request.POST.get("username")).replace(' ', '')
                                                                                if username != "":

                                                                                    username = request.POST.get("username")

                                                                                    image_unique_id = str(uuid.uuid4())
                                                                                    image_file = str(custom_user_id) + file_extension
                                                                                    file = base_url + 'static/img/follow/'+ image_file
                                                                                    img = request.FILES['file']
                                                                                    fs = FileSystemStorage(location=follow_URL, base_url=None)
                                                                                    filename = fs.save(image_file, img)
                                                                                    uploaded_file_url = fs.url(filename)

                                                                                    orders.objects.create(type=order_type, user_id=user_id, custom_user_id=custom_user_id, needed=needed, image_url=image_file, username=username, order_status=order_status)
                                                                                    return redirect('allorder')
                                                                            else:
                                                                                messages.error(request, "username is not valid")
                                                                                return redirect('allorder')
                                                                        else:
                                                                            messages.error(request, "type is not valid")
                                                                            return redirect('allorder')
                                                                    else:
                                                                        messages.error(request, "Image is not valid")
                                                                        return redirect('allorder')
                                                                else:
                                                                    messages.error(request, "Image is Required")
                                                                    return redirect('allorder')
                                                            else:
                                                                messages.error(request, "Order Status is not valid")
                                                                return redirect('allorder')
                                                        else:
                                                            messages.error(request, "Order Status is Required")
                                                            return redirect('allorder')
                                                    else:
                                                        messages.error(request, "Enter Valid an integer")
                                                        return redirect('allorder')
                                                else:
                                                    messages.error(request, "Enter needed in an integer")
                                                    return redirect('allorder')
                                            else:
                                                messages.error(request, "Needed is not valid")
                                                return redirect('allorder')
                                        else:
                                            messages.error(request, "Needed is Required")
                                            return redirect('allorder')
                                    else:
                                        messages.error(request, "Custom User ID is not valid")
                                        return redirect('allorder')
                                else:
                                    messages.error(request, "Custom User ID is Required")
                                    return redirect('allorder')
                            else:
                                messages.error(request, "User ID is not valid")
                                return redirect('allorder')
                        else:
                            messages.error(request, "User ID is Required")
                            return redirect('allorder')
                    else:
                        messages.error(request, "Order Type is not valid")
                        return redirect('allorder')
                else:
                    messages.error(request, "Order Type is Required")
                    return redirect('allorder')
            return redirect('allorder')
        else:
            return redirect('admin')

class Like_Order(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:

            date_bool = False
            like_order_usertype_bool = False
            start_date = request.GET.get('like_order_start_date')
            end_date = request.GET.get('like_order_end_date')
            search_field = request.GET.get('like_order_usertype')

            start_date_param = request.GET.get('like_order_start_date')
            if start_date_param is not None:
                if str(start_date_param).replace(" ","") != "":
                    start_date = request.GET.get('like_order_start_date')
                    start_all_array = str(start_date).split('/')
                    start_date_up = str(start_all_array[2])+'-'+str(start_all_array[0])+'-'+str(start_all_array[1])+' 00:00'
                    date_bool = True
              
            end_date_param = request.GET.get('like_order_end_date')
            if end_date_param is not None:
                if str(end_date_param).replace(" ","") != "":
                    end_date = request.GET.get('like_order_end_date')
                    end_all_array = str(end_date).split('/')
                    end_date_up = str(end_all_array[2])+'-'+str(end_all_array[0])+'-'+str(end_all_array[1])+' 00:00'
                    date_bool = True
              
            search_field_param = request.GET.get('like_order_usertype')
            if search_field_param is not None:
                search_field = request.GET.get('like_order_usertype')
                if str(search_field).replace(" ","") != '':
                    like_order_usertype_bool = True
            
            search_type = request.GET.get("like_order_usertype_select")
            if date_bool == True:
                start_date_param = request.GET.get('like_order_start_date')
                end_date_param = request.GET.get('like_order_end_date')
                if start_date_param and end_date_param is not None:
                    start_date = request.GET.get('like_order_start_date')
                    end_date = request.GET.get('like_order_end_date')
                else:
                    messages.info(request, "Start and end both date are required!")
                    return redirect('likeorder')
                    
                if like_order_usertype_bool == True:

                    if request.GET.get("like_order_usertype_select") == "0":
                        user_id = request.GET.get("like_order_usertype")
                        like_order = orders.objects.filter(user_id=user_id, created_at__gte=start_date_up, created_at__lte=end_date_up, type='0')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(like_order, 100)
                        try:
                            like_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            like_order_data = paginator.page(1)
                        except EmptyPage:
                            like_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'like_order.html', {'like_order':like_order_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("like_order_usertype_select") == "1":
                        custom_user_id = request.GET.get("all_order_usertype")
                        like_order = orders.objects.filter(custom_user_id=custom_user_id, created_at__gte=start_date_up, created_at__lte=end_date_up, type='0')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(like_order, 100)
                        try:
                            like_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            like_order_data = paginator.page(1)
                        except EmptyPage:
                            like_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'like_order.html', {'like_order':like_order_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("like_order_usertype_select") == "2":
                        post_id = request.GET.get("like_order_usertype")
                        like_order = orders.objects.filter(post_id=post_id, created_at__gte=start_date_up, created_at__lte=end_date_up, type='0')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(like_order, 100)
                        try:
                            like_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            like_order_data = paginator.page(1)
                        except EmptyPage:
                            like_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'like_order.html', {'like_order':like_order_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("like_order_usertype_select") == "3":
                        short_code = request.GET.get("like_order_usertype")
                        like_order = orders.objects.filter(short_code=short_code, created_at__gte=start_date_up, created_at__lte=end_date_up, type='0')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(like_order, 100)
                        try:
                            like_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            like_order_data = paginator.page(1)
                        except EmptyPage:
                            like_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'like_order.html', {'like_order':like_order_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})
                    
                else:
                    like_order = orders.objects.filter(created_at__gte=start_date_up, created_at__lte=end_date_up, type='0')
                    page = request.GET.get('page', 1)

                    paginator = Paginator(like_order, 100)
                    try:
                        like_order_data = paginator.page(page)
                    except PageNotAnInteger:
                        like_order_data = paginator.page(1)
                    except EmptyPage:
                        like_order_data = paginator.page(paginator.num_pages)
                    return render(request, 'like_order.html', {'like_order':like_order_data,'start_date':start_date,'end_date':end_date})

            else:
                if like_order_usertype_bool == True:
                    if request.GET.get("like_order_usertype_select") == "0":
                        user_id = request.GET.get("like_order_usertype")
                        like_order = orders.objects.filter(user_id=user_id, type='0')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(like_order, 100)
                        try:
                            like_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            like_order_data = paginator.page(1)
                        except EmptyPage:
                            like_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'like_order.html', {'like_order':like_order_data,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("like_order_usertype_select") == "1":
                        custom_user_id = request.GET.get("like_order_usertype")
                        like_order = orders.objects.filter(custom_user_id=custom_user_id, type='0')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(like_order, 100)
                        try:
                            like_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            like_order_data = paginator.page(1)
                        except EmptyPage:
                            like_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'like_order.html', {'like_order':like_order_data,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("active_order_usertype_select") == "2":
                        post_id = request.GET.get("active_order_usertype")
                        like_order = orders.objects.filter(post_id=post_id, type='0')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(like_order, 100)
                        try:
                            like_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            like_order_data = paginator.page(1)
                        except EmptyPage:
                            like_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'like_order.html', {'like_order':like_order_data,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("like_order_usertype_select") == "3":
                        short_code = request.GET.get("like_order_usertype")
                        like_order = orders.objects.filter(short_code=short_code, type='0')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(like_order, 100)
                        try:
                            like_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            like_order_data = paginator.page(1)
                        except EmptyPage:
                            like_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'like_order.html', {'like_order':like_order_data,'search_field':search_field,'search_type':search_type})

            like_order = orders.objects.filter(type='0').order_by("-id")
            page = request.GET.get('page', 1)

            paginator = Paginator(like_order, 100)
            try:
                like_order_data = paginator.page(page)
            except PageNotAnInteger:
                like_order_data = paginator.page(1)
            except EmptyPage:
                like_order_data = paginator.page(paginator.num_pages)
            return render(request, 'like_order.html',{'like_order':like_order_data})
        else:
            return redirect('admin')

    def post(self, request):
        if request.session.get('email') and request.session.get('email') != None:

            type_bool = False
            edit_form_bool = False
            delete_form_bool = False

            type_param = request.POST.get('type')
            if type_param is not None:
                type_bool = True
            
            edit_form_param = request.POST.get('edit_form')
            if edit_form_param is not None:
                edit_form_bool = True
            
            delete_form_param = request.POST.get('delete_form')
            if delete_form_param is not None:
                delete_form_bool = True
            

            if type_bool == True:
                id_param = request.POST.get("id")
                if id_param is not None:
                    order_id = request.POST.get("id")

                    all_order_data = orders.objects.get(id=order_id)
                    Needed = all_order_data.needed
                    Recieved = all_order_data.recieved

                    all_order_list = {'Needed':Needed, 'Recieved':Recieved}
                    all_order_list = json.dumps(all_order_list)
                    all_order_list = json.loads(all_order_list)

                    msg = 'Success!'
                    return JsonResponse(all_order_list)
                else:
                    Messages = "No id!"
                    return HttpResponse(Messages)

            if edit_form_bool == True:

                id_param = request.POST.get("id")
                if id_param is not None:
                    id = str(request.POST.get("id")).replace(' ', '')
                    if id != "":

                        needed_param = request.POST.get("needed")
                        if needed_param is not None:
                            needed = str(request.POST.get("needed")).replace(' ', '')
                            if needed != "":
                                if needed.isnumeric():
                                    if int(needed)>=0:

                                        received_param = request.POST.get("received")
                                        if received_param is not None:
                                            received = str(request.POST.get("received")).replace(' ', '')
                                            if received != "":
                                                if received.isnumeric() :

                                                    user_id_like = request.POST.get("id")
                                                    Needed = request.POST.get("needed")
                                                    Received = request.POST.get("received")

                                                    all_active_list = orders.objects.get(id=user_id_like)
                                                    all_active_list.needed = Needed
                                                    all_active_list.recieved = Received
                                                    all_active_list.save()
                                                    
                                                    msg = 'Success'
                                                    return HttpResponse(msg)   
                                                else:
                                                    msg = 'Received is in Integer'
                                                    return HttpResponse(msg)
                                            else:
                                                msg = 'Received is not Valid'
                                                return HttpResponse(msg)
                                        else:
                                            msg = 'Received is Required'
                                            return HttpResponse(msg)
                                    else:
                                        msg = 'Enter valid an integer'
                                        return HttpResponse(msg)
                                else:
                                    msg = 'Enter needed in an integer'
                                    return HttpResponse(msg)
                            else:
                                msg = 'Needed is not Valid'
                                return HttpResponse(msg)
                        else:
                            msg = 'Needed is Required'
                            return HttpResponse(msg)
                    else:
                        msg = 'ID is not Valid'
                        return HttpResponse(msg)
                else:
                    msg = 'ID is Required'
                    return HttpResponse(msg)    

            if delete_form_bool == True :
                id_param = request.POST.get("id")
                if id_param is not None:
                    id = str(request.POST.get("id")).replace(' ', '')
                    if id != "":

                        user_id_active_order = request.POST.get("id")
                        

                        order_dd = orders.objects.get(id=user_id_active_order)
                        orders.objects.filter(id=user_id_active_order).delete()
                        user_data = users.objects.get(user_id = order_dd.user_id)
                        app_data_dic = app_data.objects.get()
                        
                        if (int(order_dd.needed) - int(order_dd.recieved)) > 0:

                            remains = int(order_dd.needed) - int(order_dd.recieved)
                            total_coins = user_data.total_coins
                            if order_dd.type == "0":
                                update_coin = int(total_coins) + (remains*int(app_data_dic.spent_like_coin))
                                nofify_coin = (remains*int(app_data_dic.spent_like_coin))
                            elif order_dd.type == "1":
                                update_coin = int(total_coins) + (remains*int(app_data_dic.spent_follow_coin))
                                nofify_coin = (remains*int(app_data_dic.spent_follow_coin))
                            
                            user_data.total_coins = update_coin
                            user_data.save()

                            title = "Coin refunded"
                            body_desc = str(nofify_coin) + " coin refunded"
                            registration_token = user_data.ftoken
                            send_notification(title,body_desc,registration_token)

                        msg = 'Success'
                        return HttpResponse(msg)

                    else:
                        msg = 'ID is not Valid'
                        return HttpResponse(msg)
                else:
                    msg = 'ID is Required'
                    return HttpResponse(msg)

            order_type_bool = False
            order_type_param = request.POST.get('order_type')
            if order_type_param is not None:
                order_type_bool = True
            
            if order_type_bool == True:
                order_type_param = request.POST.get('order_type')
                if order_type_param is not None:
                    order_type = str(request.POST.get("order_type")).replace(' ', '')
                    if order_type != "":

                        user_id_param = request.POST.get('user_id')
                        if user_id_param is not None:
                            user_id = str(request.POST.get("user_id")).replace(' ', '')
                            if user_id != "":
                                if users.objects.filter(user_id=request.POST.get("user_id")).exists():
                                    users.objects.get(user_id=request.POST.get("user_id"))
                                else:
                                    messages.error(request, "User is not Register!")
                                    return redirect('likeorder')

                                custom_user_id_param = request.POST.get('custom_user_id')
                                if custom_user_id_param is not None:
                                    custom_user_id = str(request.POST.get("custom_user_id")).replace(' ', '')
                                    if custom_user_id != "":

                                        needed_param = request.POST.get('needed')
                                        if needed_param is not None:
                                            needed = str(request.POST.get("needed")).replace(' ', '')
                                            if needed != "":
                                                if needed.isnumeric():
                                                    if int(needed)>=0:

                                                        order_status_param = request.POST.get('order_status')
                                                        if order_status_param is not None:
                                                            order_status = str(request.POST.get("order_status")).replace(' ', '')
                                                            if order_status != "":

                                                                image_param = request.FILES.get('file')
                                                                if image_param is not None:
                                                                    image = request.FILES.get('file')
                                                                    filename, file_extension = str(image).split(".")
                                                                    file_extension = file_extension.lower()
                                                                    file_extension = "."+file_extension
                                                                    if file_extension == '.jpeg' or file_extension == '.jpg' or file_extension == '.png' or file_extension == '.gif' or file_extension == '.tiff' or file_extension == '.psd' or file_extension == '.pdf' or file_extension == '.eps' or file_extension == '.ai' or file_extension == '.indd' or file_extension == '.raw' :
                                                                        order_type = request.POST.get("order_type")

                                                                        user_id = request.POST.get("user_id")
                                                                        custom_user_id = request.POST.get("custom_user_id")
                                                                        needed = request.POST.get("needed")
                                                                        order_status = request.POST.get("order_status")

                                                                        if order_type == '0':
                                                                            short_code_param = request.POST.get('short_code')
                                                                            if short_code_param is not None:
                                                                                short_code = str(request.POST.get("short_code")).replace(' ', '')
                                                                                if short_code != "":

                                                                                    post_id_param = request.POST.get('post_id')
                                                                                    if post_id_param is not None:
                                                                                        post_id = str(request.POST.get("post_id")).replace(' ', '')
                                                                                        if post_id != "":

                                                                                            post_id = request.POST.get("post_id")
                                                                                            image_unique_id = str(uuid.uuid4())
                                                                                            image_file = str(post_id) + file_extension
                                                                                            file = base_url + 'static/img/like/'+ image_file
                                                                                            short_code = request.POST.get("short_code")
                                                                                            img = request.FILES['file']
                                                                                            fs = FileSystemStorage(location=like_URL, base_url=None)
                                                                                            filename = fs.save(image_file, img)
                                                                                            uploaded_file_url = fs.url(filename)
                                                                                            
                                                                                            orders.objects.create(type=order_type, user_id=user_id, custom_user_id=custom_user_id, needed=needed, image_url=image_file, short_code=short_code, post_id=post_id, order_type=order_status)
                                                                                            return redirect('likeorder')
                                                                                        else:
                                                                                            messages.error(request, "Post ID is not valid")
                                                                                            return redirect('likeorder')
                                                                                    else:
                                                                                        messages.error(request, "Post ID is Required")
                                                                                        return redirect('likeorder')
                                                                                else:
                                                                                    messages.error(request, "Short Code is not valid")
                                                                                    return redirect('likeorder')
                                                                            else:
                                                                                messages.error(request, "Shoet Code is Required")
                                                                                return redirect('likeorder')
                                                                        elif order_type == '1':
                                                                            username_param = request.POST.get('username')
                                                                            if username_param is not None:
                                                                                username = str(request.POST.get("username")).replace(' ', '')
                                                                                if username != "":

                                                                                    username = request.POST.get("username")

                                                                                    image_unique_id = str(uuid.uuid4())
                                                                                    image_file = str(custom_user_id) + file_extension
                                                                                    file = base_url + 'static/img/follow/'+ image_file
                                                                                    img = request.FILES['file']
                                                                                    fs = FileSystemStorage(location=follow_URL, base_url=None)
                                                                                    filename = fs.save(image_file, img)
                                                                                    uploaded_file_url = fs.url(filename)

                                                                                    orders.objects.create(type=order_type, user_id=user_id, custom_user_id=custom_user_id, needed=needed, image_url=image_file, username=username, order_type=order_status)
                                                                                    return redirect('likeorder')
                                                                            else:
                                                                                messages.error(request, "username is not valid")
                                                                                return redirect('likeorder')
                                                                        else:
                                                                            messages.error(request, "type is not valid")
                                                                            return redirect('likeorder')
                                                                    else:
                                                                        messages.error(request, "Image is not valid")
                                                                        return redirect('likeorder')
                                                                else:
                                                                    messages.error(request, "Image is Required")
                                                                    return redirect('likeorder')
                                                            else:
                                                                messages.error(request, "Order Type is not valid")
                                                                return redirect('likeorder')
                                                        else:
                                                            messages.error(request, "Order Type is Required")
                                                            return redirect('likeorder')
                                                    else:
                                                        messages.error(request, "Enter Valid an integer")
                                                        return redirect('likeorder')
                                                else:
                                                    messages.error(request, "Enter needed in an integer")
                                                    return redirect('likeorder')
                                            else:
                                                messages.error(request, "Needed is not valid")
                                                return redirect('likeorder')
                                        else:
                                            messages.error(request, "Needed is Required")
                                            return redirect('likeorder')
                                    else:
                                        messages.error(request, "Custom User ID is not valid")
                                        return redirect('likeorder')
                                else:
                                    messages.error(request, "Custom User ID is Required")
                                    return redirect('likeorder')
                            else:
                                messages.error(request, "User ID is not valid")
                                return redirect('likeorder')
                        else:
                            messages.error(request, "User ID is Required")
                            return redirect('likeorder')
                    else:
                        messages.error(request, "Order Type is not valid")
                        return redirect('likeorder')
                else:
                    messages.error(request, "Order Type is Required")
                    return redirect('likeorder')
            return redirect('likeorder')
        else:
            return redirect('admin')

class Follow_Order(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:

            date_bool = False
            follow_order_usertype_bool = False
            start_date = request.GET.get('follow_order_start_date')
            end_date = request.GET.get('follow_order_end_date')
            search_field = request.GET.get('follow_order_usertype')

            start_date_param = request.GET.get('follow_order_start_date')
            if start_date_param is not None:
                if str(start_date_param).replace(" ","") != "":
                    start_date = request.GET.get('follow_order_start_date')
                    start_all_array = str(start_date).split('/')
                    start_date_up = str(start_all_array[2])+'-'+str(start_all_array[0])+'-'+str(start_all_array[1])+' 00:00'
                    date_bool = True
             
            end_date_param = request.GET.get('follow_order_end_date')
            if end_date_param is not None:
                if str(end_date_param).replace(" ","") != "":
                    end_date = request.GET.get('follow_order_end_date')
                    end_all_array = str(end_date).split('/')
                    end_date_up = str(end_all_array[2])+'-'+str(end_all_array[0])+'-'+str(end_all_array[1])+' 00:00'
                    date_bool = True
              
            search_field_param = request.GET.get('follow_order_usertype')
            if search_field_param is not None:
                search_field = request.GET.get('follow_order_usertype')
                if str(search_field).replace(" ","") != '':
                    follow_order_usertype_bool = True
            
            search_type = request.GET.get("follow_order_usertype_select")
            if date_bool == True:
                start_date_param = request.GET.get('follow_order_start_date')
                end_date_param = request.GET.get('follow_order_end_date')
                if start_date_param and end_date_param is not None:
                    start_date = request.GET.get('follow_order_start_date')
                    end_date = request.GET.get('follow_order_end_date')
                else:
                    messages.info(request, "Start and end both date are required!")
                    return redirect('followorder')
                    
                if follow_order_usertype_bool == True:

                    if request.GET.get("follow_order_usertype_select") == "0":
                        user_id = request.GET.get("follow_order_usertype")
                        follow_order = orders.objects.filter(user_id=user_id, created_at__gte=start_date_up, created_at__lte=end_date_up, type='1')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(follow_order, 100)
                        try:
                            follow_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            follow_order_data = paginator.page(1)
                        except EmptyPage:
                            follow_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'follow_order.html', {'follow_order':follow_order_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("follow_order_usertype_select") == "1":
                        custom_user_id = request.GET.get("all_order_usertype")
                        follow_order = orders.objects.filter(custom_user_id=custom_user_id, created_at__gte=start_date_up, created_at__lte=end_date_up, type='1')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(follow_order, 100)
                        try:
                            follow_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            follow_order_data = paginator.page(1)
                        except EmptyPage:
                            follow_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'follow_order.html', {'follow_order':follow_order_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})
                    
                else:
                    follow_order = orders.objects.filter(created_at__gte=start_date_up, created_at__lte=end_date_up, type='1')
                    page = request.GET.get('page', 1)

                    paginator = Paginator(follow_order, 100)
                    try:
                        follow_order_data = paginator.page(page)
                    except PageNotAnInteger:
                        follow_order_data = paginator.page(1)
                    except EmptyPage:
                        follow_order_data = paginator.page(paginator.num_pages)
                    return render(request, 'follow_order.html', {'follow_order':follow_order_data,'start_date':start_date,'end_date':end_date})

            else:
                if follow_order_usertype_bool == True:
                    if request.GET.get("follow_order_usertype_select") == "0":
                        user_id = request.GET.get("follow_order_usertype")
                        follow_order = orders.objects.filter(user_id=user_id, type='1')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(follow_order, 100)
                        try:
                            follow_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            follow_order_data = paginator.page(1)
                        except EmptyPage:
                            follow_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'follow_order.html', {'follow_order':follow_order_data,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("follow_order_usertype_select") == "1":
                        custom_user_id = request.GET.get("like_order_usertype")
                        follow_order = orders.objects.filter(custom_user_id=custom_user_id, type='1')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(follow_order, 100)
                        try:
                            follow_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            follow_order_data = paginator.page(1)
                        except EmptyPage:
                            follow_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'follow_order.html', {'follow_order':follow_order_data,'search_field':search_field,'search_type':search_type})

            follow_order = orders.objects.filter(type='1').order_by("-id")
            page = request.GET.get('page', 1)

            paginator = Paginator(follow_order, 100)
            try:
                follow_order_data = paginator.page(page)
            except PageNotAnInteger:
                follow_order_data = paginator.page(1)
            except EmptyPage:
                follow_order_data = paginator.page(paginator.num_pages)
            return render(request, 'follow_order.html',{'follow_order':follow_order_data})
        else:
            return redirect('admin')

    def post(self, request):
        if request.session.get('email') and request.session.get('email') != None:

            type_bool = False
            edit_form_bool = False
            delete_form_bool = False

            type_param = request.POST.get('type')
            if type_param is not None:
                type_bool = True
            
            edit_form_param = request.POST.get('edit_form')
            if edit_form_param is not None:
                edit_form_bool = True
            
            delete_form_param = request.POST.get('delete_form')
            if delete_form_param is not None:
                delete_form_bool = True

            if type_bool == True:
                id_param = request.POST.get("id")
                if id_param is not None:
                    order_id = request.POST.get("id")

                    all_order_data = orders.objects.get(id=order_id)
                    Needed = all_order_data.needed
                    Recieved = all_order_data.recieved

                    all_order_list = {'Needed':Needed, 'Recieved':Recieved}
                    all_order_list = json.dumps(all_order_list)
                    all_order_list = json.loads(all_order_list)

                    msg = 'Success!'
                    return JsonResponse(all_order_list)
                else:
                    Messages = "No id!"
                    return HttpResponse(Messages)

            if edit_form_bool == True:
                id_param = request.POST.get("id")
                if id_param is not None:
                    id = str(request.POST.get("id")).replace(' ', '')
                    if id != "":

                        needed_param = request.POST.get('needed')
                        if needed_param is not None:
                            needed = str(request.POST.get("needed")).replace(' ', '')
                            if needed != "":
                                if needed.isnumeric():
                                    if int(needed)>=0:

                                        received_param = request.POST.get('received')
                                        if received_param is not None:
                                            received = str(request.POST.get("received")).replace(' ', '')
                                            if received != "":
                                                if received.isnumeric():

                                                    user_id_like = request.POST.get("id")
                                                    Needed = request.POST.get("needed")
                                                    Received = request.POST.get("received")

                                                    all_active_list = orders.objects.get(id=user_id_like)
                                                    all_active_list.needed = Needed
                                                    all_active_list.recieved = Received
                                                    all_active_list.save()
                                                    
                                                    msg = 'Success'
                                                    return HttpResponse(msg)   
                                                else:
                                                    msg = 'Received is in Integer'
                                                    return HttpResponse(msg)
                                            else:
                                                msg = 'Received is not Valid'
                                                return HttpResponse(msg)
                                        else:
                                            msg = 'Received is Required'
                                            return HttpResponse(msg)
                                    else:
                                        msg = 'Enter Valid an integer'
                                        return HttpResponse(msg)
                                else:
                                    msg = 'Enter needed in an integer'
                                    return HttpResponse(msg)
                            else:
                                msg = 'Needed is not Valid'
                                return HttpResponse(msg)
                        else:
                            msg = 'Needed is Required'
                            return HttpResponse(msg)
                    else:
                        msg = 'ID is not Valid'
                        return HttpResponse(msg)
                else:
                    msg = 'ID is Required'
                    return HttpResponse(msg)    

            if delete_form_bool == True :
                id_param = request.POST.get("id")
                if id_param is not None:
                    id = str(request.POST.get("id")).replace(' ', '')
                    if id != "":

                        user_id_active_order = request.POST.get("id")

                        order_dd = orders.objects.get(id=user_id_active_order)
                        orders.objects.filter(id=user_id_active_order).delete()
                        user_data = users.objects.get(user_id = order_dd.user_id)
                        app_data_dic = app_data.objects.get()
                        
                        if (int(order_dd.needed) - int(order_dd.recieved)) > 0:

                            remains = int(order_dd.needed) - int(order_dd.recieved)
                            total_coins = user_data.total_coins
                            if order_dd.type == "0":
                                update_coin = int(total_coins) + (remains*int(app_data_dic.spent_like_coin))
                                nofify_coin = (remains*int(app_data_dic.spent_like_coin))
                            elif order_dd.type == "1":
                                update_coin = int(total_coins) + (remains*int(app_data_dic.spent_follow_coin))
                                nofify_coin = (remains*int(app_data_dic.spent_follow_coin))
                            
                            user_data.total_coins = update_coin
                            user_data.save()

                            title = "Coin refunded"
                            body_desc = str(nofify_coin) + " coin refunded"
                            registration_token = user_data.ftoken
                            send_notification(title,body_desc,registration_token)

                        msg = 'Success'
                        return HttpResponse(msg)
                    else:
                        msg = 'ID is not Valid'
                        return HttpResponse(msg)
                else:
                    msg = 'ID is Required'
                    return HttpResponse(msg)

            order_type_bool = False
            order_type_param = request.POST.get('order_type')
            if order_type_param is not None:
                order_type_bool = True
           
            if order_type_bool == True:
                order_type_param = request.POST.get('order_type')
                if order_type_param is not None:
                    order_type = str(request.POST.get("order_type")).replace(' ', '')
                    if order_type != "":

                        user_id_param = request.POST.get('user_id')
                        if user_id_param is not None:
                            user_id = str(request.POST.get("user_id")).replace(' ', '')
                            if user_id != "":
                                if users.objects.filter(user_id=request.POST.get("user_id")).exists():
                                    users.objects.get(user_id=request.POST.get("user_id"))
                                else:
                                    messages.error(request, "User is not Register!")
                                    return redirect('followorder')

                                custom_user_id_param = request.POST.get('custom_user_id')
                                if custom_user_id_param is not None:
                                    custom_user_id = str(request.POST.get("custom_user_id")).replace(' ', '')
                                    if custom_user_id != "":

                                        needed_param = request.POST.get('needed')
                                        if needed_param is not None:
                                            needed = str(request.POST.get("needed")).replace(' ', '')
                                            if needed != "":
                                                if needed.isnumeric():
                                                    if int(needed)>=0:

                                                        order_status_param = request.POST.get('order_status')
                                                        if order_status_param is not None:
                                                            order_status = str(request.POST.get("order_status")).replace(' ', '')
                                                            if order_status != "":

                                                                image_param = request.FILES.get('file')
                                                                if image_param is not None:
                                                                    image = request.FILES.get('file')
                                                                    filename, file_extension = str(image).split(".")
                                                                    file_extension = file_extension.lower()
                                                                    file_extension = "."+file_extension

                                                                    if file_extension == '.jpeg' or file_extension == '.jpg' or file_extension == '.png' or file_extension == '.gif' or file_extension == '.tiff' or file_extension == '.psd' or file_extension == '.pdf' or file_extension == '.eps' or file_extension == '.ai' or file_extension == '.indd' or file_extension == '.raw' :

                                                                        order_type = request.POST.get("order_type")
                                                                        user_id = request.POST.get("user_id")
                                                                        custom_user_id = request.POST.get("custom_user_id")
                                                                        needed = request.POST.get("needed")
                                                                        order_status = request.POST.get("order_status")

                                                                        if order_type == '0':
                                                                            short_code_param = request.POST.get('short_code')
                                                                            if short_code_param is not None:
                                                                                short_code = str(request.POST.get("short_code")).replace(' ', '')
                                                                                if short_code != "":

                                                                                    post_id_param = request.POST.get('post_id')
                                                                                    if post_id_param is not None:
                                                                                        post_id = str(request.POST.get("post_id")).replace(' ', '')
                                                                                        if post_id != "":

                                                                                            post_id = request.POST.get("post_id")
                                                                                            image_unique_id = str(uuid.uuid4())
                                                                                            image_file = str(post_id) + file_extension
                                                                                            file = base_url + 'static/img/like/'+ image_file
                                                                                            short_code = request.POST.get("short_code")
                                                                                            img = request.FILES['file']
                                                                                            fs = FileSystemStorage(location=like_URL, base_url=None)
                                                                                            filename = fs.save(image_file, img)
                                                                                            uploaded_file_url = fs.url(filename)
                                                                                            
                                                                                            orders.objects.create(type=order_type, user_id=user_id, custom_user_id=custom_user_id, needed=needed, image_url=image_file, short_code=short_code, post_id=post_id, order_status = order_status)
                                                                                            
                                                                                            return redirect('followorder')
                                                                                        else:
                                                                                            messages.error(request, "Post ID is not valid")
                                                                                            return redirect('followorder')
                                                                                    else:
                                                                                        messages.error(request, "Post ID is Required")
                                                                                        return redirect('followorder')
                                                                                else:
                                                                                    messages.error(request, "Short Code is not valid")
                                                                                    return redirect('followorder')
                                                                            else:
                                                                                messages.error(request, "Shoet Code is Required")
                                                                                return redirect('followorder')
                                                                        elif order_type == '1':
                                                                            username_param = request.POST.get('username')
                                                                            if username_param is not None:
                                                                                username = str(request.POST.get("username")).replace(' ', '')
                                                                                if username != "":

                                                                                    username = request.POST.get("username")

                                                                                    image_unique_id = str(uuid.uuid4())
                                                                                    image_file = str(custom_user_id) + file_extension
                                                                                    file = base_url + 'static/img/follow/'+ image_file
                                                                                    img = request.FILES['file']
                                                                                    fs = FileSystemStorage(location=follow_URL, base_url=None)
                                                                                    filename = fs.save(image_file, img)
                                                                                    uploaded_file_url = fs.url(filename)

                                                                                    orders.objects.create(type=order_type, user_id=user_id, custom_user_id=custom_user_id, needed=needed, image_url=image_file, username=username, order_status = order_status)
                                                                                    return redirect('followorder')
                                                                            else:
                                                                                messages.error(request, "username is not valid")
                                                                                return redirect('followorder')
                                                                        else:
                                                                            messages.error(request, "type is not valid")
                                                                            return redirect('followorder')
                                                                    else:
                                                                        messages.error(request, "Image is not valid")
                                                                        return redirect('followorder')
                                                                else:
                                                                    messages.error(request, "Image is Required")
                                                                    return redirect('followorder')
                                                            else:
                                                                messages.error(request, "Order Status is not valid")
                                                                return redirect('followorder')
                                                        else:
                                                            messages.error(request, "Order Status is Required")
                                                            return redirect('followorder')
                                                    else:
                                                        messages.error(request, "Enter Valid an integer")
                                                        return redirect('followorder')
                                                else:
                                                    messages.error(request, "Enter needed in an integer")
                                                    return redirect('followorder')
                                            else:
                                                messages.error(request, "Needed is not valid")
                                                return redirect('followorder')
                                        else:
                                            messages.error(request, "Needed is Required")
                                            return redirect('followorder')
                                    else:
                                        messages.error(request, "Custom User ID is not valid")
                                        return redirect('followorder')
                                else:
                                    messages.error(request, "Custom User ID is Required")
                                    return redirect('followorder')
                            else:
                                messages.error(request, "User ID is not valid")
                                return redirect('followorder')
                        else:
                            messages.error(request, "User ID is Required")
                            return redirect('followorder')
                    else:
                        messages.error(request, "Order Type is not valid")
                        return redirect('followorder')
                else:
                    messages.error(request, "Order Type is Required")
                    return redirect('followorder')
            return redirect('followorder')
        else:
            return redirect('admin')

class Complete_Order(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:

            date_bool = False
            complete_order_usertype_bool = False
            start_date = request.GET.get('complete_order_startdate')
            end_date = request.GET.get('complete_order_enddate')
            search_field = request.GET.get('complete_order_usertype')

            start_date_param = request.GET.get('complete_order_startdate')
            if start_date_param is not None:
                if str(start_date_param).replace(" ","") != "":
                    start_date = request.GET.get('complete_order_startdate')
                    start_all_array = str(start_date).split('/')
                    start_date_up = str(start_all_array[2])+'-'+str(start_all_array[0])+'-'+str(start_all_array[1])+' 00:00'
                    date_bool = True
             
            end_date_param = request.GET.get('complete_order_enddate')
            if end_date_param is not None:
                if str(end_date_param).replace(" ","") != "":
                    end_date = request.GET.get('complete_order_enddate')
                    end_all_array = str(end_date).split('/')
                    end_date_up = str(end_all_array[2])+'-'+str(end_all_array[0])+'-'+str(end_all_array[1])+' 00:00'
                    date_bool = True
             
            search_field_param = request.GET.get('complete_order_usertype')
            if search_field_param is not None:
                search_field = request.GET.get('complete_order_usertype')
                if str(search_field).replace(" ","") != '':
                    complete_order_usertype_bool = True
            
            search_type = request.GET.get("complete_order_usertype_select")
            if date_bool == True:
                start_date_param = request.GET.get('complete_order_startdate')
                end_date_param = request.GET.get('complete_order_enddate')
                if start_date_param and end_date_param is not None:
                    start_date = request.GET.get('complete_order_startdate')
                    end_date = request.GET.get('complete_order_enddate')
                else:
                    messages.info(request, "Start and end both date are required!")
                    return redirect('completeorder')
                    
                if complete_order_usertype_bool == True:

                    if request.GET.get("complete_order_usertype_select") == "0":
                        user_id = request.GET.get("complete_order_usertype")
                        complete_order = orders.objects.filter(user_id=user_id, created_at__gte=start_date_up, created_at__lte=end_date_up, needed='0')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(complete_order, 100)
                        try:
                            complete_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            complete_order_data = paginator.page(1)
                        except EmptyPage:
                            complete_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'complete_order.html', {'complete_order':complete_order_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("complete_order_usertype_select") == "1":
                        custom_user_id = request.GET.get("complete_order_usertype")
                        complete_order = orders.objects.filter(custom_user_id=custom_user_id, created_at__gte=start_date_up, created_at__lte=end_date_up, needed='0')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(complete_order, 100)
                        try:
                            complete_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            complete_order_data = paginator.page(1)
                        except EmptyPage:
                            complete_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'complete_order.html', {'complete_order':complete_order_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("complete_order_usertype_select") == "2":
                        post_id = request.GET.get("complete_order_usertype")
                        complete_order = orders.objects.filter(post_id=post_id, created_at__gte=start_date_up, created_at__lte=end_date_up, needed='0')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(complete_order, 100)
                        try:
                            complete_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            complete_order_data = paginator.page(1)
                        except EmptyPage:
                            complete_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'complete_order.html', {'complete_order':complete_order_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("complete_order_usertype_select") == "3":
                        short_code = request.GET.get("complete_order_usertype")
                        complete_order = orders.objects.filter(short_code=short_code, created_at__gte=start_date_up, created_at__lte=end_date_up, needed='0')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(complete_order, 100)
                        try:
                            complete_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            complete_order_data = paginator.page(1)
                        except EmptyPage:
                            complete_order_data = paginator.page(paginator.num_pages)

                        return render(request, 'complete_order.html', {'complete_order':complete_order_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})
                    
                else:
                    complete_order = orders.objects.filter(created_at__gte=start_date_up, created_at__lte=end_date_up, needed='0')
                    page = request.GET.get('page', 1)

                    paginator = Paginator(complete_order, 100)
                    try:
                        complete_order_data = paginator.page(page)
                    except PageNotAnInteger:
                        complete_order_data = paginator.page(1)
                    except EmptyPage:
                        complete_order_data = paginator.page(paginator.num_pages)
                    return render(request, 'complete_order.html', {'complete_order':complete_order_data,'start_date':start_date,'end_date':end_date})

            else:
                if complete_order_usertype_bool == True:
                    if request.GET.get("complete_order_usertype_select") == "0":
                        user_id = request.GET.get("complete_order_usertype")
                        complete_order = orders.objects.filter(user_id=user_id, needed='0')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(complete_order, 100)
                        try:
                            complete_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            complete_order_data = paginator.page(1)
                        except EmptyPage:
                            complete_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'complete_order.html', {'complete_order':complete_order_data,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("complete_order_usertype_select") == "1":
                        custom_user_id = request.GET.get("complete_order_usertype")
                        complete_order = orders.objects.filter(custom_user_id=custom_user_id, needed='0')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(complete_order, 100)
                        try:
                            complete_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            complete_order_data = paginator.page(1)
                        except EmptyPage:
                            complete_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'complete_order.html', {'complete_order':complete_order_data,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("complete_order_usertype_select") == "2":
                        post_id = request.GET.get("complete_order_usertype")
                        complete_order = orders.objects.filter(post_id=post_id, needed='0')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(complete_order, 100)
                        try:
                            complete_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            complete_order_data = paginator.page(1)
                        except EmptyPage:
                            complete_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'complete_order.html', {'complete_order':complete_order_data,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("complete_order_usertype_select") == "3":
                        short_code = request.GET.get("complete_order_usertype")
                        complete_order = orders.objects.filter(short_code=short_code, needed='0')
                        page = request.GET.get('page', 1)

                        paginator = Paginator(complete_order, 100)
                        try:
                            complete_order_data = paginator.page(page)
                        except PageNotAnInteger:
                            complete_order_data = paginator.page(1)
                        except EmptyPage:
                            complete_order_data = paginator.page(paginator.num_pages)
                        return render(request, 'complete_order.html', {'complete_order':complete_order_data,'search_field':search_field,'search_type':search_type})

            complete_order = orders.objects.filter(needed='0').order_by("-id")
            page = request.GET.get('page', 1)

            paginator = Paginator(complete_order, 100)
            try:
                complete_order_data = paginator.page(page)
            except PageNotAnInteger:
                complete_order_data = paginator.page(1)
            except EmptyPage:
                complete_order_data = paginator.page(paginator.num_pages)
            return render(request, 'complete_order.html',{'complete_order':complete_order_data})
        else:
            return redirect('admin')

    def post(self, request):
        if request.session.get('email') and request.session.get('email') != None:

            type_bool = False
            edit_form_bool = False
            delete_form_bool = False

            type_param = request.POST.get('type')
            if type_param is not None:
                type_bool = True
            
            edit_form_param = request.POST.get('edit_form')
            if edit_form_param is not None:
                edit_form_bool = True
            
            delete_form_param = request.POST.get('delete_form')
            if delete_form_param is not None:
                delete_form_bool = True

            if type_bool == True:
                id_param = request.POST.get('id')
                if id_param is not None:
                    order_id = request.POST.get("id")

                    all_order_data = orders.objects.get(id=order_id)
                    Needed = all_order_data.needed
                    Recieved = all_order_data.recieved

                    all_order_list = {'Needed':Needed, 'Recieved':Recieved}
                    all_order_list = json.dumps(all_order_list)
                    all_order_list = json.loads(all_order_list)

                    msg = 'Success!'
                    return JsonResponse(all_order_list)
                else:
                    Messages = "No id!"
                    return HttpResponse(Messages)

            if edit_form_bool == True:
                id_param = request.POST.get('id')
                if id_param is not None:
                    id = str(request.POST.get("id")).replace(' ', '')
                    if id != "":

                        needed_param = request.POST.get('needed')
                        if needed_param is not None:
                            needed = str(request.POST.get("needed")).replace(' ', '')
                            if needed != "":
                                if needed.isnumeric():
                                    if int(needed)>=0:

                                        received_param = request.POST.get('received')
                                        if received_param is not None:
                                            received = str(request.POST.get("received")).replace(' ', '')
                                            if received != "":
                                                if received.isnumeric():

                                                    user_id_like = request.POST.get("id")
                                                    Needed = request.POST.get("needed")
                                                    Received = request.POST.get("received")

                                                    all_active_list = orders.objects.get(id=user_id_like)
                                                    all_active_list.needed = Needed
                                                    all_active_list.recieved = Received
                                                    all_active_list.save()
                                                    
                                                    msg = 'Success'
                                                    return HttpResponse(msg)   
                                                else:
                                                    msg = 'Received is in Integer'
                                                    return HttpResponse(msg)
                                            else:
                                                msg = 'Received is not Valid'
                                                return HttpResponse(msg)
                                        else:
                                            msg = 'Received is Required'
                                            return HttpResponse(msg)
                                    else:
                                        msg = 'Enter Valid an integer'
                                        return HttpResponse(msg)
                                else:
                                    msg = 'Enter needed in an integer'
                                    return HttpResponse(msg)
                            else:
                                msg = 'Needed is not Valid'
                                return HttpResponse(msg)
                        else:
                            msg = 'Needed is Required'
                            return HttpResponse(msg)
                    else:
                        msg = 'ID is not Valid'
                        return HttpResponse(msg)
                else:
                    msg = 'ID is Required'
                    return HttpResponse(msg)    

            if delete_form_bool == True :
                id_param = request.POST.get('id')
                if id_param is not None:
                    id = str(request.POST.get("id")).replace(' ', '')
                    if id != "":

                        user_id_active_order = request.POST.get("id")
                        orders.objects.filter(id=user_id_active_order).delete()

                        msg = 'Success'
                        return HttpResponse(msg)

                    else:
                        msg = 'ID is not Valid'
                        return HttpResponse(msg)
                else:
                    msg = 'ID is Required'
                    return HttpResponse(msg)

            order_type_bool = False
            order_type_param = request.POST.get('order_type')
            if order_type_param is not None:
                order_type_bool = True
            
            if order_type_bool == True:
                order_type_param = request.POST.get('order_type')
                if order_type_param is not None:
                    order_type = str(request.POST.get("order_type")).replace(' ', '')
                    if order_type != "":

                        user_id_param = request.POST.get('user_id')
                        if user_id_param is not None:
                            user_id = str(request.POST.get("user_id")).replace(' ', '')
                            if user_id != "":
                                if users.objects.filter(user_id=request.POST.get("user_id")).exists():
                                    users.objects.get(user_id=request.POST.get("user_id"))
                                else:
                                    messages.error(request, "User is not Register!")
                                    return redirect('completeorder')

                                custom_user_id_param = request.POST.get('custom_user_id')
                                if custom_user_id_param is not None:
                                    custom_user_id = str(request.POST.get("custom_user_id")).replace(' ', '')
                                    if custom_user_id != "":

                                        needed_param = request.POST.get('needed')
                                        if needed_param is not None:
                                            needed = str(request.POST.get("needed")).replace(' ', '')
                                            if needed != "":
                                                if needed.isnumeric():
                                                    if int(needed)>=0:

                                                        order_status_param = request.POST.get('order_status')
                                                        if order_status_param is not None:
                                                            order_status = str(request.POST.get("order_status")).replace(' ', '')
                                                            if order_status != "":

                                                                image_param = request.FILES.get('file')
                                                                if image_param is not None:
                                                                    image = request.FILES.get('file')
                                                                    filename, file_extension = str(image).split(".")
                                                                    file_extension = file_extension.lower()
                                                                    file_extension = "."+file_extension

                                                                    if file_extension == '.jpeg' or file_extension == '.jpg' or file_extension == '.png' or file_extension == '.gif' or file_extension == '.tiff' or file_extension == '.psd' or file_extension == '.pdf' or file_extension == '.eps' or file_extension == '.ai' or file_extension == '.indd' or file_extension == '.raw' :

                                                                        order_type = request.POST.get("order_type")
                                                                        user_id = request.POST.get("user_id")
                                                                        custom_user_id = request.POST.get("custom_user_id")
                                                                        needed = request.POST.get("needed")
                                                                        order_status = request.POST.get("order_status")

                                                                        if order_type == '0':
                                                                            short_code_param = request.POST.get('short_code')
                                                                            if short_code_param is not None:
                                                                                short_code = str(request.POST.get("short_code")).replace(' ', '')
                                                                                if short_code != "":

                                                                                    post_id_param = request.POST.get('post_id')
                                                                                    if post_id_param is not None:
                                                                                        post_id = str(request.POST.get("post_id")).replace(' ', '')
                                                                                        if post_id != "":

                                                                                            image_unique_id = str(uuid.uuid4())
                                                                                            image_file = str(post_id) + file_extension
                                                                                            file = base_url + 'static/img/like/'+ image_file
                                                                                            short_code = request.POST.get("short_code")
                                                                                            post_id = request.POST.get("post_id")
                                                                                            img = request.FILES['file']
                                                                                            fs = FileSystemStorage(location=like_URL, base_url=None)
                                                                                            filename = fs.save(image_file, img)
                                                                                            uploaded_file_url = fs.url(filename)
                                                                                            
                                                                                            orders.objects.create(type=order_type, user_id=user_id, custom_user_id=custom_user_id, needed=needed, image_url=image_file, short_code=short_code, post_id=post_id, order_status = order_status)
                                                                                            return redirect('completeorder')
                                                                                        else:
                                                                                            messages.error(request, "Post ID is not valid")
                                                                                            return redirect('completeorder')
                                                                                    else:
                                                                                        messages.error(request, "Post ID is Required")
                                                                                        return redirect('completeorder')
                                                                                else:
                                                                                    messages.error(request, "Short Code is not valid")
                                                                                    return redirect('completeorder')
                                                                            else:
                                                                                messages.error(request, "Shoet Code is Required")
                                                                                return redirect('completeorder')
                                                                        elif order_type == '1':
                                                                            username_param = request.POST.get('username')
                                                                            if username_param is not None:
                                                                                username = str(request.POST.get("username")).replace(' ', '')
                                                                                if username != "":

                                                                                    username = request.POST.get("username")

                                                                                    image_unique_id = str(uuid.uuid4())
                                                                                    image_file = str(custom_user_id) + file_extension
                                                                                    file = base_url + 'static/img/follow/'+ image_file
                                                                                    img = request.FILES['file']
                                                                                    fs = FileSystemStorage(location=follow_URL, base_url=None)
                                                                                    filename = fs.save(image_file, img)
                                                                                    uploaded_file_url = fs.url(filename)

                                                                                    orders.objects.create(type=order_type, user_id=user_id, custom_user_id=custom_user_id, needed=needed, image_url=image_file, username=username, order_status = order_status)
                                                                                    return redirect('completeorder')
                                                                            else:
                                                                                messages.error(request, "username is not valid")
                                                                                return redirect('completeorder')
                                                                        else:
                                                                            messages.error(request, "type is not valid")
                                                                            return redirect('completeorder')
                                                                    else:
                                                                        messages.error(request, "Image is not valid")
                                                                        return redirect('completeorder')
                                                                else:
                                                                    messages.error(request, "Image is Required")
                                                                    return redirect('completeorder')
                                                            else:
                                                                messages.error(request, "Order Status is not valid")
                                                                return redirect('followorder')
                                                        else:
                                                            messages.error(request, "Order Status is Required")
                                                            return redirect('followorder')
                                                    else:
                                                        messages.error(request, "Enter Valid an integer")
                                                        return redirect('completeorder')
                                                else:
                                                    messages.error(request, "Enter needed in an integer")
                                                    return redirect('completeorder')
                                            else:
                                                messages.error(request, "Needed is not valid")
                                                return redirect('completeorder')
                                        else:
                                            messages.error(request, "Needed is Required")
                                            return redirect('completeorder')
                                    else:
                                        messages.error(request, "Custom User ID is not valid")
                                        return redirect('completeorder')
                                else:
                                    messages.error(request, "Custom User ID is Required")
                                    return redirect('completeorder')
                            else:
                                messages.error(request, "User ID is not valid")
                                return redirect('completeorder')
                        else:
                            messages.error(request, "User ID is Required")
                            return redirect('completeorder')
                    else:
                        messages.error(request, "Order Type is not valid")
                        return redirect('completeorder')
                else:
                    messages.error(request, "Order Type is Required")
                    return redirect('completeorder')
            return redirect('completeorder')
        else:
            return redirect('admin')

class User_List(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:

            date_bool = False
            user_list_usertype_bool = False
            start_date = request.GET.get('user_list_startdate')
            end_date = request.GET.get('user_list_enddate')
            search_field = request.GET.get('user_list_usertype')

            start_date_param = request.GET.get('user_list_startdate')
            if start_date_param is not None:
                if str(start_date_param).replace(" ","") != "":
                    start_date = request.GET.get('user_list_startdate')
                    start_all_array = str(start_date).split('/')
                    start_date_up = str(start_all_array[2])+'-'+str(start_all_array[0])+'-'+str(start_all_array[1])+' 00:00'
                    date_bool = True
             
            end_date_param = request.GET.get('user_list_enddate')
            if end_date_param is not None:
                if str(end_date_param).replace(" ","") != "":
                    end_date = request.GET.get('user_list_enddate')
                    end_all_array = str(end_date).split('/')
                    end_date_up = str(end_all_array[2])+'-'+str(end_all_array[0])+'-'+str(end_all_array[1])+' 00:00'
                    date_bool = True
              
            search_field_param = request.GET.get('user_list_usertype')
            if search_field_param is not None:
                search_field = request.GET.get('user_list_usertype')
                if str(search_field).replace(" ","") != '':
                    user_list_usertype_bool = True
            
            search_type = request.GET.get("user_list_usertype_select")
            if date_bool == True:
                start_date_param = request.GET.get('user_list_startdate')
                end_date_param = request.GET.get('user_list_enddate')
                if start_date_param and end_date_param is not None:
                    start_date = request.GET.get('user_list_startdate')
                    end_date = request.GET.get('user_list_enddate')
                else:
                    messages.info(request, "Start and end both date are required!")
                    return redirect('userlist')
                    
                if user_list_usertype_bool == True:

                    if request.GET.get("user_list_usertype_select") == "0":
                        user_id = request.GET.get("user_list_usertype")
                        user = users.objects.filter(user_id=user_id, created_at__gte=start_date_up, created_at__lte=end_date_up)
                        page = request.GET.get('page', 1)

                        paginator = Paginator(user, 100)
                        try:
                            user_data = paginator.page(page)
                        except PageNotAnInteger:
                            user_data = paginator.page(1)
                        except EmptyPage:
                            user_data = paginator.page(paginator.num_pages)
                        return render(request, 'user_list.html', {'users':user_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("user_list_usertype_select") == "1":
                        parent_id = request.GET.get("user_list_usertype")
                        user = users.objects.filter(parent_id=parent_id, created_at__gte=start_date_up, created_at__lte=end_date_up)
                        page = request.GET.get('page', 1)

                        paginator = Paginator(user, 100)
                        try:
                            user_data = paginator.page(page)
                        except PageNotAnInteger:
                            user_data = paginator.page(1)
                        except EmptyPage:
                            user_data = paginator.page(paginator.num_pages)
                        return render(request, 'user_list.html', {'users':user_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("user_list_usertype_select") == "2":
                        username = request.GET.get("user_list_usertype")
                        user = users.objects.filter(username=username, created_at__gte=start_date_up, created_at__lte=end_date_up)
                        page = request.GET.get('page', 1)

                        paginator = Paginator(user, 100)
                        try:
                            user_data = paginator.page(page)
                        except PageNotAnInteger:
                            user_data = paginator.page(1)
                        except EmptyPage:
                            user_data = paginator.page(paginator.num_pages)
                        return render(request, 'user_list.html', {'users':user_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("user_list_usertype_select") == "3":
                        referral_code = request.GET.get("user_list_usertype")
                        user = users.objects.filter(referral_code=referral_code, created_at__gte=start_date_up, created_at__lte=end_date_up)
                        page = request.GET.get('page', 1)

                        paginator = Paginator(user, 100)
                        try:
                            user_data = paginator.page(page)
                        except PageNotAnInteger:
                            user_data = paginator.page(1)
                        except EmptyPage:
                            user_data = paginator.page(paginator.num_pages)
                        return render(request, 'user_list.html', {'users':user_data,'start_date':start_date,'end_date':end_date,'search_field':search_field,'search_type':search_type})
                    
                else:
                    user = users.objects.filter(created_at__gte=start_date_up, created_at__lte=end_date_up)
                    page = request.GET.get('page', 1)

                    paginator = Paginator(user, 100)
                    try:
                        user_data = paginator.page(page)
                    except PageNotAnInteger:
                        user_data = paginator.page(1)
                    except EmptyPage:
                        user_data = paginator.page(paginator.num_pages)
                    return render(request, 'user_list.html', {'users':user_data,'start_date':start_date,'end_date':end_date})

            else:
                if user_list_usertype_bool == True:
                    if request.GET.get("user_list_usertype_select") == "0":
                        user_id = request.GET.get("user_list_usertype")
                        user = users.objects.filter(user_id=user_id)
                        page = request.GET.get('page', 1)

                        paginator = Paginator(user, 100)
                        try:
                            user_data = paginator.page(page)
                        except PageNotAnInteger:
                            user_data = paginator.page(1)
                        except EmptyPage:
                            user_data = paginator.page(paginator.num_pages)
                        return render(request, 'user_list.html', {'users':user_data,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("user_list_usertype_select") == "1":
                        parent_id = request.GET.get("user_list_usertype")
                        user = users.objects.filter(parent_id=parent_id)
                        page = request.GET.get('page', 1)

                        paginator = Paginator(user, 100)
                        try:
                            user_data = paginator.page(page)
                        except PageNotAnInteger:
                            user_data = paginator.page(1)
                        except EmptyPage:
                            user_data = paginator.page(paginator.num_pages)
                        return render(request, 'user_list.html', {'users':user_data,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("user_list_usertype_select") == "2":
                        username = request.GET.get("user_list_usertype")
                        user = users.objects.filter(username=username)
                        page = request.GET.get('page', 1)

                        paginator = Paginator(user, 100)
                        try:
                            user_data = paginator.page(page)
                        except PageNotAnInteger:
                            user_data = paginator.page(1)
                        except EmptyPage:
                            user_data = paginator.page(paginator.num_pages)
                        return render(request, 'user_list.html', {'users':user_data,'search_field':search_field,'search_type':search_type})

                    elif request.GET.get("user_list_usertype_select") == "3":
                        referral_code = request.GET.get("user_list_usertype")
                        user = users.objects.filter(referral_code=referral_code)
                        page = request.GET.get('page', 1)

                        paginator = Paginator(user, 100)
                        try:
                            user_data = paginator.page(page)
                        except PageNotAnInteger:
                            user_data = paginator.page(1)
                        except EmptyPage:
                            user_data = paginator.page(paginator.num_pages)
                        return render(request, 'user_list.html', {'users':user_data,'search_field':search_field,'search_type':search_type})

            user = users.objects.all().order_by('-user_id')
            page = request.GET.get('page', 1)

            paginator = Paginator(user, 100)
            try:
                user_data = paginator.page(page)
            except PageNotAnInteger:
                user_data = paginator.page(1)
            except EmptyPage:
                user_data = paginator.page(paginator.num_pages)
            return render(request, 'user_list.html', {'users':user_data})
        else:
            return redirect('admin')
    
    def post(self, request):
        if request.session.get('email') and request.session.get('email') != None:

            type_bool = False
            edit_form_bool = False
            delete_form_bool = False

            type_param = request.POST.get('type')
            if type_param is not None:
                type_bool = True
            
            edit_form_param = request.POST.get('edit_form')
            if edit_form_param is not None:
                edit_form_bool = True
            
            delete_form_param = request.POST.get('delete_form')
            if delete_form_param is not None:
                delete_form_bool = True
            

            if type_bool == True:
                id_param = request.POST.get('id')
                if id_param is not None:
                    user_id_users = request.POST.get("id")

                    if users.objects.filter(user_id=user_id_users,parent_id="0").exists():
                        appdata = users.objects.get(user_id=user_id_users)
                        TotalCoin = appdata.total_coins
                        Status = str(appdata.status)
                        user_list = {'TotalCoin':TotalCoin, 'Status':Status}

                    elif users.objects.filter(~Q(parent_id="0"),user_id=user_id_users).exists():
                        appdata = users.objects.get(user_id=user_id_users)
                        Status = str(appdata.status)
                        user_list = {'Status':Status}

                    user_list = json.dumps(user_list)
                    user_list = json.loads(user_list)

                    msg = 'Success!'
                    return JsonResponse(user_list)
                else:
                    Messages = "No id!"
                    return HttpResponse(Messages)

            if edit_form_bool == True:
                id_param = request.POST.get('id')
                if id_param is not None:
                    id = str(request.POST.get("id")).replace(' ', '')
                    if id != "":

                        user_status_param = request.POST.get('user_status')
                        if user_status_param is not None:

                            user_status = str(request.POST.get("user_status")).replace(' ', '')
                            if user_status != "":

                                user_id_users = request.POST.get("id")
                                Total_Coin = str(request.POST.get("total_coin")).replace(' ', '').replace('-', '')
                                Status_User = request.POST.get("user_status")
                                
                                if users.objects.filter(user_id=user_id_users,parent_id="0").exists():
                                    user_List = users.objects.get(user_id=user_id_users)
                                    child_list = users.objects.filter(parent_id=user_id_users).values('user_id')
                                    for i in child_list:
                                        child_data = users.objects.get(user_id=i['user_id'])
                                        child_data.status = Status_User
                                        child_data.save()
                                    
                                elif users.objects.filter(~Q(parent_id="0"),user_id=user_id_users).exists():
                                    user_List = users.objects.get(user_id=user_id_users)

                                user_List.status = Status_User


                                total_coin_param = request.POST.get('total_coin')
                                if total_coin_param is not None:

                                    total_coin = str(request.POST.get("total_coin")).replace(' ', '').replace('-', '')
                                    if total_coin != "":

                                        if total_coin.isnumeric():
                                            if int(total_coin)>=0:

                                                user_List.total_coins = Total_Coin
                                user_List.save()

                                msg = 'Success'
                                return HttpResponse(msg)   
                            else:
                                msg = 'Status is not Valid'
                                return HttpResponse(msg)
                        else:
                            msg = 'Status is Required'
                            return HttpResponse(msg)

                    else:
                        msg = 'ID is not Valid'
                        return HttpResponse(msg)
                else:
                    msg = 'ID is Required'
                    return HttpResponse(msg)    

            if delete_form_bool == True :
                id_param = request.POST.get('id')
                if id_param is not None:
                    id = str(request.POST.get("id")).replace(' ', '')
                    if id != "":

                        user_id_users = request.POST.get("id")
                        if users.objects.filter(user_id=user_id_users,parent_id="0").exists():

                            users.objects.filter(user_id=user_id_users).delete()
                            child_list = users.objects.filter(parent_id=user_id_users).values('user_id')
                            for i in child_list:
                                child_data = users.objects.filter(user_id=i['user_id']).delete()
                                
                        
                        elif users.objects.filter(~Q(parent_id="0"),user_id=user_id_users).exists():
                            users.objects.filter(user_id=user_id_users).delete()
                            

                        msg = 'Success'
                        return HttpResponse(msg)

                    else:
                        msg = 'ID is not Valid'
                        return HttpResponse(msg)
                else:
                    msg = 'ID is Required'
                    return HttpResponse(msg)

            add_user_bool = False
            user_id_param = request.POST.get("user_id")
            if user_id_param is not None:
                add_user_bool = True
            
            if add_user_bool == True:
                user_id_param = request.POST.get('user_id')
                if user_id_param is not None:
                    user_id = str(request.POST.get("user_id")).replace(' ', '')
                    if user_id != "":

                        username_param = request.POST.get('username')
                        if username_param is not None:
                            username = str(request.POST.get("username")).replace(' ', '')
                            if username != "":

                                total_coin_param = request.POST.get('total_coin')
                                if total_coin_param is not None:
                                    total_coin = str(request.POST.get("total_coin")).replace(' ', '')
                                    if total_coin != "":
                                        if total_coin.isnumeric():

                                            referral_code_param = request.POST.get('referral_code')
                                            if referral_code_param is not None:
                                                referral_code = str(request.POST.get("referral_code")).replace(' ', '')
                                                if referral_code != "":

                                                    user_purchased_param = request.POST.get('user_purchased')
                                                    if user_purchased_param is not None:
                                                        user_purchased = str(request.POST.get("user_purchased")).replace(' ', '')
                                                        if user_purchased != "":

                                                            user_referred_param = request.POST.get('user_referred')
                                                            if user_referred_param is not None:
                                                                user_referred = str(request.POST.get("user_referred")).replace(' ', '')
                                                                if user_referred != "":

                                                                    user_status_param = request.POST.get('user_status')
                                                                    if user_status_param is not None:
                                                                        user_status = str(request.POST.get("user_status")).replace(' ', '')
                                                                        if user_status != "":

                                                                            user_id = request.POST.get("user_id")
                                                                            username = request.POST.get("username")
                                                                            total_coin = str(request.POST.get("total_coin")).replace('-','')
                                                                            referral_code = request.POST.get("referral_code")
                                                                            user_purchased = request.POST.get("user_purchased")
                                                                            user_referred = request.POST.get("user_referred")
                                                                            user_status = request.POST.get("user_status")

                                                                            if users.objects.filter(user_id=user_id).exists():
                                                                                users.objects.get(user_id=user_id)
                                                                                messages.error(request, "User ID is already in Database")
                                                                                return redirect('userlist')
                                                                            else:
                                                                                if users.objects.filter(referral_code=referral_code).exists():
                                                                                    users.objects.get(referral_code=referral_code)
                                                                                    messages.error(request, "Referral Code is already in Database")
                                                                                    return redirect('userlist')

                                                                            users.objects.create(user_id=user_id, username=username, total_coins=total_coin, referral_code=referral_code, is_purchase=user_purchased, is_referred=user_referred, status=user_status)
                                                                            return redirect('userlist')
                                                
                                                                        else:
                                                                            messages.error(request, "User status is not valid")
                                                                            return redirect('userlist')
                                                                    else:
                                                                        messages.error(request, "User status is Required")
                                                                        return redirect('userlist')
                                                                else:
                                                                    messages.error(request, "User referred is not valid")
                                                                    return redirect('userlist')
                                                            else:
                                                                messages.error(request, "User referred is Required")
                                                                return redirect('userlist')
                                                        else:
                                                            messages.error(request, "User purchased is not valid")
                                                            return redirect('userlist')
                                                    else:
                                                        messages.error(request, "User purchased is Required")
                                                        return redirect('userlist')
                                                else:
                                                    messages.error(request, "Referral code is not valid")
                                                    return redirect('userlist')
                                            else:
                                                messages.error(request, "Referral code is Required")
                                                return redirect('userlist')
                                        else:
                                            messages.error(request, "Total Coin is not valid")
                                            return redirect('userlist')
                                    else:
                                        messages.error(request, "Total Coin is Empty!")
                                        return redirect('userlist')
                                else:
                                    messages.error(request, "Total Coin is Required")
                                    return redirect('userlist')
                            else:
                                messages.error(request, "Username is not valid")
                                return redirect('userlist')
                        else:
                            messages.error(request, "Username is Required")
                            return redirect('userlist')
                    else:
                        messages.error(request, "User ID is not Valide!")
                        return redirect('userlist')
                else:
                    messages.error(request, "User ID is Required!")
                    return redirect('userlist')
            return redirect('userlist')

        else:
            return redirect('admin')

class Premium_User_List(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:

            date_bool = False
            start_date = request.GET.get('premium_user_list_startdate')
            end_date = request.GET.get('premium_user_list_enddate')

            start_date_param = request.GET.get('premium_user_list_startdate')
            if start_date_param is not None:
                if str(start_date_param).replace(" ","") != "":
                    start_date = request.GET.get('premium_user_list_startdate')
                    start_all_array = str(start_date).split('/')
                    start_date_up = str(start_all_array[2])+'-'+str(start_all_array[0])+'-'+str(start_all_array[1])+' 00:00'
                    date_bool = True

            end_date_param = request.GET.get('premium_user_list_enddate')
            if end_date_param is not None:
                if str(end_date_param).replace(" ","") != "":
                    end_date = request.GET.get('premium_user_list_enddate')
                    end_all_array = str(end_date).split('/')
                    end_date_up = str(end_all_array[2])+'-'+str(end_all_array[0])+'-'+str(end_all_array[1])+' 00:00'
                    date_bool = True
            
            
            if date_bool == True:
                start_date_param = request.GET.get('premium_user_list_startdate')
                end_date_param = request.GET.get('premium_user_list_enddate')
                if start_date_param and end_date_param is not None:
                    start_date = request.GET.get('premium_user_list_startdate')
                    end_date = request.GET.get('premium_user_list_enddate')
                else:
                    messages.info(request, "Start and end both date are required!")
                    return redirect('premiumuserlist')
                    
                premium_user = users.objects.filter(created_at__gte=start_date_up, created_at__lte=end_date_up, is_purchase='1')
                page = request.GET.get('page', 1)

                paginator = Paginator(premium_user, 100)
                try:
                    premium_user_data = paginator.page(page)
                except PageNotAnInteger:
                    premium_user_data = paginator.page(1)
                except EmptyPage:
                    premium_user_data = paginator.page(paginator.num_pages)
                return render(request, 'premium_user.html', {'premium_user':premium_user_data,'start_date':start_date,'end_date':end_date})

            premium_user = users.objects.filter(is_purchase='1')
            page = request.GET.get('page', 1)

            paginator = Paginator(premium_user, 100)
            try:
                premium_user_data = paginator.page(page)
            except PageNotAnInteger:
                premium_user_data = paginator.page(1)
            except EmptyPage:
                premium_user_data = paginator.page(paginator.num_pages)
            return render(request, 'premium_user.html',{'premium_user':premium_user_data})
        else:
            return redirect('admin')

class Purchase_Coin_Other_method_List(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:
            purchase_coin_other_method_list = purchase_coins.objects.all().order_by('-id')
            page = request.GET.get('page', 1)

            paginator = Paginator(purchase_coin_other_method_list, 100)
            try:
                purchase_coin_other_method_list_data = paginator.page(page)
            except PageNotAnInteger:
                purchase_coin_other_method_list_data = paginator.page(1)
            except EmptyPage:
                purchase_coin_other_method_list_data = paginator.page(paginator.num_pages)
            for i in purchase_coin_other_method_list_data:
                users_name_d = users.objects.get(user_id=i.user_id)
                uss = users_name_d.username
                i.username = uss
            return render(request, 'purchase_coin_other_method_list.html', {'purchase_coin_other_method_list':purchase_coin_other_method_list_data})
        else:
            return redirect('admin')

    def post(self, request):
        if request.session.get('email') and request.session.get('email') != None:

            type_bool = False
            edit_form_bool = False
            delete_form_bool = False

            type_param = request.POST.get('type')
            if type_param is not None:
                type_bool = True

            edit_form_param = request.POST.get('edit_form')
            if edit_form_param is not None:
                edit_form_bool = True

            delete_form_param = request.POST.get('delete_form')
            if delete_form_param is not None:
                delete_form_bool = True

            if type_bool == True:
                id_param = request.POST.get("id")
                if id_param is not None:
                    id_d = request.POST.get("id")

                    appdata = purchase_coins.objects.get(id=id_d)
                    PurchaseCoin = appdata.purchased_coin
                    CountryCode = appdata.country_code

                    pur = {'PurchaseCoin':PurchaseCoin, 'CountryCode':CountryCode}
                    pur = json.dumps(pur)
                    pur = json.loads(pur)

                    msg = 'Success!'
                    return JsonResponse(pur)
                else:
                    Messages = "No id!"
                    return HttpResponse(Messages)

            if edit_form_bool == True:
                id_param = request.POST.get("id")
                if id_param is not None:
                    id = str(request.POST.get("id")).replace(' ', '')
                    if id != "":

                        purchase_co_param = request.POST.get('purchase_co')
                        if purchase_co_param is not None:
                            purchase_co = str(request.POST.get("purchase_co")).replace(' ', '')
                            if purchase_co != "":
                                if purchase_co.isnumeric():

                                    country_co_param = request.POST.get('country_co')
                                    if country_co_param is not None:
                                        country_co = str(request.POST.get("country_co")).replace(' ', '')
                                        if country_co != "":

                                            id_p = request.POST.get("id")
                                            Purchased_Coin = request.POST.get("purchase_co")
                                            Country_Code = request.POST.get("country_co")

                                            purch_coin_other_methode = purchase_coins.objects.get(id=id_p)
                                            purch_coin_other_methode.purchased_coin = Purchased_Coin
                                            purch_coin_other_methode.country_code = Country_Code
                                            purch_coin_other_methode.save()
                                            
                                            msg = 'Success'
                                            return HttpResponse(msg)   
                                        else:
                                            msg = 'Country Code is not Valid'
                                            return HttpResponse(msg)
                                    else:
                                        msg = 'Country Code is Required'
                                        return HttpResponse(msg)
                                else:
                                    msg = 'Purchase Coin is not Valid'
                                    return HttpResponse(msg)
                            else:
                                msg = 'Purchase Coin is Empty!'
                                return HttpResponse(msg)
                        else:
                            msg = 'Purchase Coin is Required'
                            return HttpResponse(msg)
                    else:
                        msg = 'ID is not Valid'
                        return HttpResponse(msg)
                else:
                    msg = 'ID is Required'
                    return HttpResponse(msg)

            if delete_form_bool == True :
                id_param = request.POST.get("id")
                if id_param is not None:
                    id = str(request.POST.get("id")).replace(' ', '')
                    if id != "":

                        id_p = request.POST.get("id")
                        purchase_coins.objects.filter(id=id_p).delete()

                        msg = 'Success'
                        return HttpResponse(msg)
                    else:
                        msg = 'ID is not Valid'
                        return HttpResponse(msg)
                else:
                    msg = 'ID is Required'
                    return HttpResponse(msg)
            return redirect('purchasecoin_other_method_list')
        else:
            return redirect('admin')

class Purchase_Coin_InApp_List(View):
    def get(self, request):
        if request.session.get('email') and request.session.get('email') != None:
            purchase_coin_inapp_list = user_orders.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(purchase_coin_inapp_list, 100)
            try:
                purchase_coin_inapp_list_data = paginator.page(page)
            except PageNotAnInteger:
                purchase_coin_inapp_list_data = paginator.page(1)
            except EmptyPage:
                purchase_coin_inapp_list_data = paginator.page(paginator.num_pages)
            for i in purchase_coin_inapp_list_data:
                users_name_d = users.objects.get(user_id=i.user_id)
                user_name = users_name_d.username
                i.username = user_name
            return render(request, 'purchase_coin_inapp_method_list.html',{'purchase_coin_inapp_list':purchase_coin_inapp_list_data})
        else:
            return redirect('admin')

    def post(self, request):
        if request.session.get('email') and request.session.get('email') != None:

            delete_form_inapp_bool = False
            delete_form_inapp_param = request.POST.get('delete_form_inapp')
            if delete_form_inapp_param is not None:
                delete_form_inapp_bool = True
            # logger.info(request.POST.get('delete_form_inapp'))
            # logger.info(request.POST.get('id'))
            if delete_form_inapp_bool == True :
                id_param = request.POST.get("id")
                if id_param is not None:
                    id = str(request.POST.get("id")).replace(' ', '')
                    if id != "":

                        id_p = request.POST.get("id")
                        user_orders.objects.filter(id=id_p).delete()

                        msg = 'Success'
                        return HttpResponse(msg)
                    else:
                        msg = 'ID is not Valid'
                        return HttpResponse(msg)
                else:
                    msg = 'ID is Required'
                    return HttpResponse(msg)
            
            return redirect('purchasecoin_inapp_method_list')
        else:
            return redirect('admin')


class Logout(View):
    def get(self, request):
        authu.logout(request)
        request.session.flush() # cookie delete
        request.session.clear_expired() # cookie delete in data-base
        return redirect('admin')
 

class privacy_pollicy(View):
    def get(self, request):
        return render(request, 'privacy_pollicy.html')

class term_of_service(View):
    def get(self, request):
        return render(request, 'term_of_service.html')
    
