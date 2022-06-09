from cgi import print_directory
from appium import webdriver
import os.path,random
# from main import LOGGER
import time, requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlencode
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from faker import Faker
fake = Faker()
country_name = 'malaysia'

def get_number(pid='8',country = 'hk'):
    url = "http://api.getsmscode.com/vndo.php?"

    payload = {
        "action": "getmobile",
        "username": "pay@noborders.net",
        "token": "87269a810f4a59d407d0e0efe58185e6",
        "pid": pid,
        "cocode":country
    }

    payload = urlencode(payload)
    full_url = url + payload
    response = requests.post(url=full_url)
    response = response.content.decode("utf-8")
    # print(response)
    # time.sleep(1000)

    return response

def get_sms(phone_number, pid='8',country = 'hk'):
    url = "http://api.getsmscode.com/vndo.php?"
    payload = {
        "action": "getsms",
        "username": "pay@noborders.net",
        "token": "87269a810f4a59d407d0e0efe58185e6",
        "pid": pid,
        "mobile": phone_number,
        "author": "pay@noborders.net",
        "cocode":country
    }
    payload = urlencode(payload)
    full_url = url + payload
    for x in range(10):
        response = requests.post(url=full_url).text
        if 'insta' in (response).lower():
            response = response.split(' ')
            otp = response[1]+response[2]
            return otp
        time.sleep(4)

    return False

def ban_number(phone_number, pid='8',country = 'hk'):
    url = "http://api.getsmscode.com/vndo.php?"
    payload = {
        "action": "addblack",
        "username": "pay@noborders.net",
        "token": "87269a810f4a59d407d0e0efe58185e6",
        "pid": pid,
        "mobile": phone_number,
        "author": "pay@noborders.net",
        "cocode":country
    }
    payload = urlencode(payload)
    full_url = url + payload
    response = requests.post(url=full_url)
    print(response.text)
    return response



class CyberGhost:
    timeout = 5
    def __init__(self):
        self.app_driver = self.get_driver()
        self.next_move()
        self.follow_count=0
        # self.logger = LOGGER
        self.timeout = 10
    @staticmethod
    def get_driver():
        """
        Starts appium driver
        """
        path = '/wd/hub'
        port = 4723
        host = "http://localhost"
        opts = {
            "platformName": "Android",
            "automationName": "uiautomator2",
            "noSign": True,
            "noVerify": True,
            "ignoreHiddenApiPolicyError": True,
        }
        url = f"{host}:{port}{path}"
        driver = webdriver.Remote(url, desired_capabilities=opts, keep_alive=True)
        print(driver)
        return driver

    
    
    def find_element(self, element, locator, locator_type=By.XPATH,
            page=None, timeout=10,
            condition_func=EC.presence_of_element_located,
            condition_other_args=tuple()):
        """Find an element, then return it or None.
        If timeout is less than or requal zero, then just find.
        If it is more than zero, then wait for the element present.
        """
        time.sleep(3)
        try:
            if timeout > 0:
                wait_obj = WebDriverWait(self.app_driver, timeout)
                ele = wait_obj.until(
                        condition_func((locator_type, locator),
                            *condition_other_args))
            else:
                print(f'Timeout is less or equal zero: {timeout}')
                ele = self.app_driver.find_element(by=locator_type,
                        value=locator)
            if page:
                print(
                        f'Found the element "{element}" in the page "{page}"')
            else:
                print(f'Found the element: {element}')
            return ele
        except (NoSuchElementException, TimeoutException) as e:
            if page:
                print(f'Cannot find the element "{element}"'
                        f' in the page "{page}"')
            else:
                print(f'Cannot find the element: {element}')


    
    def click_element(self, element, locator, locator_type=By.XPATH,
            timeout=timeout,page=None):
        time.sleep(3)
        
        """Find an element, then click and return it, or return None"""
        ele = self.find_element(element, locator, locator_type, timeout=timeout,page=page)
        if ele:
            ele.click()
            return ele

    def input_text(self, text, element, locator, locator_type=By.XPATH,
            timeout=timeout, hide_keyboard=True,page=None):
        time.sleep(3)
        
        """Find an element, then input text and return it, or return None"""
        try:
            if hide_keyboard :
                print(f'Hide keyboard')
                try:self.app_driver.hide_keyboard()
                except:None

            ele = self.find_element(element, locator, locator_type=locator_type,
                    timeout=timeout,page=page)
            if ele:
                ele.clear()
                ele.send_keys(text)
                print(f'Inputed "{text}" for the element: {element}')
                return ele
        except Exception as e :
            print(f'Got an error in input text :{element} {e}')

    def swip_display(self,scroll_height):
        window_size = self.app_driver.get_window_size()
        width = window_size["width"]
        height = window_size["height"]
        x1 = width*0.7
        y1 = height*(scroll_height/10)
        y2 = height*0.2
        self.app_driver.swipe(
            start_x = x1,
            start_y = y1,
            end_x = x1,
            end_y = y2, 
            duration=random.randrange(1050, 1250),
            )

    def try_again_popup(self):
        try:
            try_again_ele_id = 'com.instagram.android:id/default_dialog_title'
            try_again_ele_ele = self.find_element('Try again',try_again_ele_id,By.ID,timeout=3)

            if try_again_ele_ele:
                try_again_ok_id = 'com.instagram.android:id/negative_button_row'
                time.sleep(3)
                self.click_element('Ok btn',try_again_ok_id,By.ID,timeout=2)
                self.click_element('Ok btn',try_again_ok_id,By.ID,timeout=2)
                self.click_element('Ok btn',try_again_ok_id,By.ID,timeout=2)
                self.click_element('Ok btn',try_again_ok_id,By.ID,timeout=2)
                return True
            else:
                return False
        except :return False

    def next_move(self):
        aa = self.find_element('Follower count','com.instagram.android:id/row_profile_header_textview_followers_count',By.ID).get_attribute('text')
        print(aa)

        # first_user = self.find_element('First user','com.instagram.android:id/row_search_user_container',By.ID)
        # if first_user:
        #     first_user = self.app_driver.find_element_by_id('com.instagram.android:id/row_search_user_container')
        #     print(first_user,'first_user')
        #     first_user.click()
        
        # follow_ele_list = self.find_element('all ele','com.instagram.android:id/profile_header_actions_top_row',By.ID)
        # follow_ele_list = self.app_driver.find_element(By.ID,'com.instagram.android:id/profile_header_actions_top_row')
        # print(follow_ele_list,'follow_ele')
        # follow_ele = follow_ele_list.find_elements_by_xpath('//*')
        # print(follow_ele)
        # for i in follow_ele:
        #     if i.text == 'Follow':
        #         i.click()
        #         print('Yes')
        #         break
        #     elif i.text == 'Following':
        #         print('yes')
        #         break


        # all_pics = self.app_driver.find_elements_by_id('com.instagram.android:id/media_set_row_content_identifier')
        # first_3 = all_pics[0]
        # first_pic = first_3.find_element_by_class_name('android.widget.ImageView')
        # first_pic.click()


        # self.swip_display(3)
        # time_list = []
        # total_new_post = 0
        # for i in  range(6):
        #     all_pic_ele = self.app_driver.find_elements_by_xpath('//*')
        #     for pic_ele_time in all_pic_ele:
        #         try:
        #             time_step = str(pic_ele_time.get_attribute('text')).lower()
        #             if 'ago' in time_step :
        #                 if 'hour' or 'secound' in time_step:
        #                     if not time_step in time_list:
        #                         print(time_step)
        #                         time_list.append(str(pic_ele_time.get_attribute('text')).lower())

        #         except Exception as e:None

        #     self.swip_display(9)
        # for time_ in time_list:
        #     if 'hour' in time_:
        #         print(time_)
        #         total_new_post+=1
        #     elif 'minutes' in time_:
        #         print(time_)
        #         total_new_post+=1
        #     elif 'seconds'   in time_:
        #         print(time_)
        #         total_new_post+=1
        # if total_new_post == 0:
        #         print('There isnt any latest post')

        # else:print(total_new_post,'total_new_posttotal_new_post')



        # print(f'\n\n\t\t{total_new_post}\n\n')
        # print(f'\n\n\t\t{time_list}\n\n')
        

        pass


if __name__ == "__main__":
    driver = CyberGhost()

