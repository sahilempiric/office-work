import time
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from selenium.webdriver.common.by import By
from home.models import user_details
from home.driver.driver import get_driver
# Create your views here.

driver = ''
class login(View):
    def get(self,request,number):
        global driver
        driver = get_driver(number)
        driver.get('https://my.telegram.org/auth')
        sucsess = False
        try:
            driver.find_element(By.ID,'my_login_phone').send_keys(str(number))
            time.sleep(1)
            driver.find_element(By.XPATH,'//*[@id="my_send_form"]/div[2]/button').click()
            sucsess = True
        except Exception as e:print(e)

        data = {'sucsess' : sucsess}

        return JsonResponse(data=data)


class application(View):
    def get(self,request,otp):
        # driver.get('https://www.google.com')
        try:
            driver.find_element(By.ID,'my_password').send_keys(str(otp))
            driver.find_element(By.NAME,'remember').click()
            driver.find_element(By.XPATH,'//*[@id="my_login_form"]/div[4]/button').click()

            time.sleep(5)
            driver.refresh()
            time.sleep(3)
            driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div/div/div/div[2]/div/ul/li[1]/a').click()
            time.sleep(5)
            driver.refresh()
            time.sleep(3)
            driver.find_element(By.ID,'app_title').send_keys('applldiadsyfvtu')
            driver.find_element(By.ID,'app_shortname').send_keys('sjhdu')
            driver.find_element(By.NAME,'app_platform').click()
            time.sleep(2)
            driver.find_element(By.ID,'app_save_btn').click()
            time.sleep(5)



            driver.refresh()
            app_api_id = driver.find_element(By.XPATH,'//*[@id="app_edit_form"]/div[1]/div[1]/span').get_attribute('text')
            app_api_hash = driver.find_element(By.XPATH,'//*[@id="app_edit_form"]/div[2]/div[1]/span').get_attribute('text')

            
            
        except Exception as e:print(e)
        data = {
            'sucsess' : otp,
            'app_api_id' : app_api_id,
            'app_api_hash' : app_api_hash,
        }


        
        return JsonResponse(data=data)