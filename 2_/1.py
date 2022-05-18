from cgi import print_directory
from lib2to3.pgen2 import driver
from driver_ import get_driver
from selenium.webdriver.common.by import By
import time,random, pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def random_sleep(b,a=1):
    # print(f'random sleep : {a} to {b} secound')
    time.sleep(random.randint(a,b))

driver = get_driver()

driver.get('https://www.vitafoods.eu.com/en/exhibitor-list.html')
random_sleep(5,3)

ifram_div = driver.find_element_by_class_name('cmp-iframe__content')
print(ifram_div.find_element_by_tag_name('iframe'))
driver.switch_to_frame(ifram_div.find_element_by_tag_name('iframe'))
print(len(driver.find_elements_by_class_name('company-card')))

comapny_name_li = []
from_li = []
linkdin_li = []
details_li = []
company_web_li = []
lead_li = []
scraped_card = 0
all_cards_len = len(driver.find_elements_by_class_name('company-card'))
card_count = 0
while card_count < all_cards_len:
    try:
        random_sleep(2)
        card__ = driver.find_elements_by_class_name('company-card')[card_count]
        driver.execute_script("arguments[0].scrollIntoView();", card__)
        card__.click()
        random_sleep(2)
        div_company_card = driver.find_element_by_id('company-iframe-div')
        comapny_name = div_company_card.find_element_by_class_name('company-details-row__header').text
        random_sleep(2)
        comapny_details_div = driver.find_element(By.CLASS_NAME,'company-details-row')
        try:
            comapny_name = comapny_details_div.find_element(By.CLASS_NAME,'company-details-row__header').text
        except Exception as e:comapny_name = '-'
        comapny_name = str(comapny_name).replace('\n',' ').replace('  ',' ').strip()
        comapny_name_list = str(comapny_name).split('Stand:')
        comapny_name_ = comapny_name_list[0]
        try:
            if driver.find_element_by_class_name('fa-linkedin').is_displayed():linkdin = driver.find_elements(By.CLASS_NAME,'company-details-row__link')[-1].get_attribute('href')
            else:linkdin='-'
        except Exception as e:linkdin='-'
        linkdin_li.append(linkdin)
        from_ = str(comapny_name_list[-1]).strip()
        details_p = comapny_details_div.find_elements(By.TAG_NAME,'p')
        details = ""
        for details__ in details_p:
            details += str(details__.text)
        company_web = comapny_details_div.find_elements(By.TAG_NAME,'a')[-1].text
        comapny_name_ = "-" if comapny_name_ == "" else comapny_name_ 
        from_ = "-" if from_ == "" else from_ 
        details = "-" if details == "" else details 
        company_web = "-" if company_web == "" else company_web 
        linkdin = "-" if linkdin == "" else linkdin 

        comapny_name_li.append(comapny_name_)
        from_li.append(from_)
        details_li.append(details)
        company_web_li.append(company_web)
        lead_li.append('https://www.vitafoods.eu.com/en/exhibitor-list.html')

        try:driver.execute_script('document.querySelector("#company-iframe-div > a").click()')
        except Exception as e:None
        if card_count % 10 == 0:
            driver.execute_script('document.querySelector("#listBottomElement > a").click()')
            random_sleep(3)
            all_cards_len = len(driver.find_elements_by_class_name('company-card'))

    except Exception as e:print(e)
    card_count += 1 

data_frame = pd.DataFrame(list(zip(lead_li,comapny_name_li,linkdin,from_li,company_web_li,details_li,)),columns=['Lead source','Company Name','Linkdin','Located','Comapany Website','Details'],dtype=str,index=None)
data_frame.to_csv('/media/eu4/49fa581d-6d91-4c0f-886a-2d6d1a2b9857/project/scrapping/2_/scrapped_data.csv')
input("Enter:") 
driver.quit()