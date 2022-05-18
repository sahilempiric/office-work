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

driver.get('https://fmig-online.de/unsere-mitglieder/?L=cpxjywytlgjuwjn')
random_sleep(5,3)
links = []
title = []
address = []
telephone = []
mail = []
leadsources = []
website = []
accept = driver.find_elements(By.CLASS_NAME,'_brlbs-btn-accept-all')[0]
accept.click()
random_sleep(5,3)
driver.refresh()
all_links = [ i.get_attribute('href') for i in  driver.find_elements(By.CLASS_NAME,'grid-item')]
data_frame = pd.DataFrame(list(zip(leadsources,title,address,telephone,mail)),columns=['Lead Source','Title','Address','Telephone','Email'],dtype=str,index=None)
for link in all_links:
    driver.get(link)

    grid_item_members = driver.find_elements(By.CLASS_NAME,'grid-item')
    for member in grid_item_members:
        title_ = member.find_element(By.CLASS_NAME,'title').text
        cordinates = member.find_element(By.CLASS_NAME,'coordinates').text
        cordinates = str(cordinates).split('\n')
        address_ = cordinates[0]+" "+cordinates[1]
        for i in cordinates:
            if 'Telefon:' in i:
                i = i.split('Telefon:')
                telephone_ = i[-1].strip()
                break
            else:
                telephone_ = "-"

        email = member.find_element(By.CLASS_NAME,'theme-hover-color').text
        print(email)
        title.append(title_)
        address.append(address_)
        telephone.append(telephone_)
        mail.append(email)
        leadsources.append('https://fmig-online.de/unsere-mitglieder/?L=cpxjywytlgjuwjn')
        df = pd.DataFrame({'Lead Source':['https://fmig-online.de/unsere-mitglieder/?L=cpxjywytlgjuwjn'],'Title':[title_],'Address':[address_],'Telephone':[telephone_],'Email':[email]})
        data_frame = pd.concat([data_frame,df],ignore_index=True,axis=0)
        data_frame.to_csv('/media/eu4/49fa581d-6d91-4c0f-886a-2d6d1a2b9857/project/scrapping/5_/scrapped_data.csv')

# input("Enter:")
driver.quit()