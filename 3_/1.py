from lib2to3.pgen2 import driver
from driver_ import get_driver
from selenium.webdriver.common.by import By
import time,random, pandas as pd

def random_sleep(b,a=0):
    print(f'random sleep : {a} to {b} secound')
    time.sleep(random.randint(a,b))
driver = get_driver()
driver.get('https://www.germansweets.de/german-sweets/mitglieder/hersteller')
random_sleep(5,3)
links = []
title = []
website = []
all_link = driver.find_elements(By.CLASS_NAME,'mitglied-detail-link')
for link in all_link:
    links.append(link.get_attribute('href'))
leads_li = []
data_frame = pd.DataFrame(list(zip(leads_li,title,website)),columns=['Lead Source','Title','Website'],dtype=str,index=None)
for link in links:
    try:
        driver.get(link)
        random_sleep(3,2)
        try:title_ = driver.find_element(By.CLASS_NAME,'title').text
        except Exception as e:title_='-'
        website_div = driver.find_element(By.CLASS_NAME,'website')
        try:
            try:website_ = website_div.find_element(By.TAG_NAME,'a').text
            except:website_ = website_div.find_element(By.TAG_NAME,'span').text
        except Exception as e:website_ = '-'
        title_ = '-' if title_ == '' else title_
        website_ = '-' if website_ == '' else website_
        title.append(title_)
        website.append(website_)
        leads_li.append('https://www.germansweets.de/german-sweets/mitglieder/hersteller')
        df = pd.DataFrame({'Title':[title_],'Website':[website_],'Lead Source':['https://www.germansweets.de/german-sweets/mitglieder/hersteller']})
        data_frame = pd.concat([data_frame,df],ignore_index=True,axis=0)
        data_frame.to_csv('/media/eu4/49fa581d-6d91-4c0f-886a-2d6d1a2b9857/project/scrapping/3_/scrapped_data.csv')
    except Exception as e:
        print(e)
        continue

driver.quit()