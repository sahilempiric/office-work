import random
import time, string
from turtle import title
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
        except Exception as e:driver.quit();print(e)

        data = {'sucsess' : sucsess}

        return JsonResponse(data=data)


class application(View):
    def get(self,request,otp):
        app_api_id = ''
        try:
            print(driver.find_element_by_id('app_edit_form').is_displayed(),'=======================')
        except Exception as e:print(e)
        app_api_hash = ''
        # driver.get('https://www.google.com')
        try:
            try:
                driver.find_element(By.ID,'my_password').send_keys(str(otp))
                # driver.find_element(By.NAME,'remember').click()
                driver.find_element_by_name('remember').click()
                driver.find_element(By.XPATH,'//*[@id="my_login_form"]/div[4]/button').click()
                time.sleep(5)
                driver.refresh()
                time.sleep(3)
                driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div/div/div/div[2]/div/ul/li[1]/a').click()
                time.sleep(5)
                driver.refresh()
                time.sleep(3)
            except Exception as e:print(e)


            while True:
                length = random.randint(8,13)
                titles = ''.join(random.choices(string.ascii_lowercase,k=length))
                short_name = titles[:int(length/2)]
                app_title = driver.find_element(By.ID,'app_title')
                app_title.clear()
                app_title.send_keys(titles)
                app_shortname = driver.find_element(By.ID,'app_shortname')
                app_shortname.clear()
                app_shortname.send_keys(short_name)
                try:
                    driver.execute_script('document.querySelector("#app_create_form > div:nth-child(6) > div > div:nth-child(8) > label > input[type=radio]").click()')
                except Exception as e:print(e)
                # driver.find_element(By.NAME,'app_platform').click()
                # driver.find_element(By.NAME,'app_platform').click()
                time.sleep(1)
                driver.find_element(By.ID,'app_save_btn').click()
                time.sleep(2)
                # driver.refresh()
                try:
                    driver.switch_to.alert.accept() 
                except Exception as e:print(e)
                try:
                    if driver.find_element_by_id('app_edit_form').is_displayed():break
                    elif driver.find_element_by_id('app_create_form').is_displayed():continue
                    else:continue
                except Exception as e:print(e)
            time.sleep(5)



            driver.refresh()
            app_api_id = driver.find_element(By.XPATH,'//*[@id="app_edit_form"]/div[1]/div[1]/span').get_attribute('innerText')
            app_api_hash = driver.find_element(By.XPATH,'//*[@id="app_edit_form"]/div[2]/div[1]/span').get_attribute('innerText')

            if app_api_id and app_api_hash:
                success = True
            else:success = False
            
            
        except Exception as e:print(e)
        data = {
            'sucsess' : success,
            'app_api_id' : app_api_id,
            'app_api_hash' : app_api_hash,
        }


        
        return JsonResponse(data=data)