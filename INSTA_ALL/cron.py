import logging
import http.client
import re
import json

from firebase_admin.messaging import Notification
from .models import app_data, users
from .views import *
import datetime
from datetime import date
from django.conf import settings


logger = logging.getLogger(__name__)

def getRefreshToken():
    client_id = "896862870299-doc0jvrlip4t191ept9n13pue7gl9g11.apps.googleusercontent.com"
    client_secret = "bwvsYiuo4rC5Db3Aq98uy_Ux"
    refresh_token = "1//0g4p9vDBrzUxKCgYIARAAGBASNwF-L9Irc4epGbUvVR0sAK4eziRxXnQcYsg2Xm-wgNIFFDho4pZyv7rNbmhWmFTnM4BRnUvizck"

    post_data = f"grant_type=refresh_token&client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}"

    curl = f"grant_type=refresh_token&client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}" #curl= is not write check that
    

    conn = http.client.HTTPSConnection("accounts.google.com")
    headers = { 'content-type': "application/x-www-form-urlencoded" }
    conn.request("POST", "/o/oauth2/token", post_data, headers)


    # data = conn.read()
    res = conn.getresponse()
    data = res.read()
    # data = data.decode("utf-8")

    # print(data.decode("utf-8"))

    # logger.info("re_data")
    # logger.info(data)
    # logger.info("conn")
    # logger.info(conn)
    # re_data = json.dumps(data)
    re_data = json.loads(data)

    if re_data['access_token']:
       
        # logger.info("re_data")
        # logger.info(re_data)
        app_data.objects.update(access_token=re_data['access_token'])
        return re_data
    else:
        f = open(f"{settings.BASE_DIR}/log/access_token_log.txt", "a")
        datetime_nn = datetime.datetime.now()
        f.write(f'{datetime_nn} : {conn.rrson}')
        f.close()
        getRefreshToken()
    return True

def offer_check():
    app_data_dates = app_data.objects.all()
    # logger.info(len(app_data_dates))
    if len(app_data_dates) == 1:
        #logger.info("11111111111")
        start_date = app_data_dates[0].offer_starttime
        end_date = app_data_dates[0].offer_endtime

        o_start_date = str(start_date).split(" ")
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

        o_end_date = str(end_date).split(" ")
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

        datetime_nn = datetime.datetime.now()

       # logger.info("222222222")
        app_data_datesss = app_data.objects.get(id=app_data_dates[0].id)
        if date_time1 <= datetime_nn and date_time2 >= datetime_nn:
            #logger.info("333333333")
            app_data_datesss.offer = "1"
            app_data_datesss.save()
        else:
           # logger.info("44444444444")

            app_data_datesss.offer = "0"
            app_data_datesss.save()

def dailynotify():
    Notification_data = app_data.objects.all()

    if len(Notification_data ) != 0:
        status = Notification_data[0].notification_show

        if status == "1":
            title = Notification_data[0].notification_title
            body_desc = Notification_data[0].notification_message
            usersss = users.objects.filter(parent_id="0")
            for user in usersss:
                registration_token = user.ftoken
                send_notification(title,body_desc,registration_token)


def offer_notify():
    Notification_data = app_data.objects.all()
    if len(Notification_data ) != 0:
        status = Notification_data[0].offer
        if status == "1":
            title = Notification_data[0].offer_discount_title
            body_desc = Notification_data[0].offer_discount_text
            usersss = users.objects.filter(parent_id="0")
            for user in usersss:
                registration_token = user.ftoken
                send_notification(title,body_desc,registration_token)


def user_order_del():
    order = orders.object.filter(needed="0")
    for ord in order:
        up_date = ord.updated_time
        up_date = str(up_date).split(' ')
        date_u = str(up_date[0]).split('-')
        time_u = str(up_date[1]).split(":")

        year_upd = date_u[0]
        month_upd = date_u[1]
        date_upd = date_u[2]
        hour_upd = time_u[0]
        min_upd = time_u[1]
        
        date_time1 = datetime.datetime(year_upd, month_upd, date_upd, hour_upd, min_upd)

        date_time2 = datetime.datetime.now()

        if (date_time2 - date_time1).days >= 15:
            orders.object.delete(id=order.id)


