from cgi import print_directory
from lib2to3.pgen2 import driver
from driver_ import get_driver
from selenium.webdriver.common.by import By
import time,random, pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def random_sleep(b,a=0):
    print(f'random sleep : {a} to {b} secound')
    time.sleep(random.randint(a,b))
driver = get_driver()
driver.get('https://2022.worldofprivatelabel.com/react/exhibitor?combine=&p=1&s=20')
random_sleep(5,3)
# edit-access-code
driver.find_element(By.ID,'edit-access-code').send_keys('HERRM403010')
time.sleep(1)
driver.find_element(By.ID,'edit-submit').click()
random_sleep(6,3)
driver.refresh()
random_sleep(6,3)
links = []
leadsources = []
company_name_li = []
company_web_li = []
address_li = []
contact_li = []
Phone_number_li = []
all_item = driver.find_elements(By.CLASS_NAME,'item')
value_page = [max(int(i.get_attribute('value')) if i.get_attribute('value') != None else 0  for i in all_item)]
page_index = value_page[0]

for i in range(page_index):
    i = i+1
    driver.get(f'https://2022.worldofprivatelabel.com/react/exhibitor?combine=&p={i}&s=20')
    random_sleep(5,3)
    all_exhibitor = driver.find_elements(By.CLASS_NAME,'exhibitor-list')
    for exhibitor in all_exhibitor:
        link_text_ = exhibitor.find_element(By.TAG_NAME,'h3')
        link_ = link_text_.find_element(By.TAG_NAME,'a').get_attribute('href')
        links.append(link_) if link_ not in links else None
        print(link_)


for link_ in links:
        driver.get(link_)
        random_sleep(3,2)
        company_name = driver.find_element(By.CLASS_NAME,'company_name').text

        company_web_ = driver.find_element_by_class_name('company_heading-info')
        try:
            company_web = company_web_.find_element_by_tag_name('a').text
        except Exception as e:company_web = '-'

        contact = ""
        try:
            contact_details = driver.find_elements(By.CLASS_NAME,'member_contact_detail')
            for contact_detail in contact_details:
                contact += str(contact_detail.text)
                contact += str(contact_detail.find_element_by_class_name('job_title').text) if contact_detail.find_element_by_class_name('job_title').is_displayed() else ""
        except :contact = "-"
        try:
            address_div = driver.find_element(By.CLASS_NAME,'address-outer')
            address = address_div.find_element(By.CLASS_NAME,'member_info_val').text
            address = str(address).replace('\n',' ')
        except:
            address = '-'
        try:
            Phone_number_div = driver.find_element(By.CLASS_NAME,'phone-outer')
            Phone_number = Phone_number_div.find_element_by_class_name('member_info_val').text
        except:Phone_number = "-"
        print(company_name)
        print(company_web)
        print(address)
        print(contact)
        print(Phone_number)    
        company_name_li.append(company_name)
        company_web_li.append(company_web)
        address_li.append(address)
        contact_li.append(contact)
        Phone_number_li.append(Phone_number)    
        leadsources.append('https://2022.worldofprivatelabel.com/react/exhibitor?combine=&p=1&s=20')


data_frame = pd.DataFrame(list(zip(leadsources,company_name_li,company_web_li,address_li,contact_li,Phone_number_li)),columns=['Lead Source','Company Name','Comapany Website','Address','Contact','Phone No.'],dtype=str,index=None)
data_frame.to_csv('/media/eu4/49fa581d-6d91-4c0f-886a-2d6d1a2b9857/project/scrapping/1_/scrapped_data.csv')

input("Enter:")
driver.quit()