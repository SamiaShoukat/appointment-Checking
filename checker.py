import os
import logging
import requests



from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv

load_dotenv()

def check(driver):
    
    #driver = Driver(uc=True, incognito=True, headless=True)

    """options = []
    try:
        driver.get("https://service2.diplo.de/rktermin/extern/appointment_showForm.do?locationCode=isla&realmId=108&categoryId=1600")
        print('ACTIVE')
        return (None, True,options)
    except Exception as e:
        print('NOT-ACTIVE')
        return (None, False,options)"""


    try:
        options = []
        driver.get("https://service2.diplo.de/rktermin/extern/appointment_showForm.do?locationCode=isla&realmId=108&categoryId=1600")
        elem_select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[1]/fieldset/form/div[8]/div[2]/select")))
        print('Select Element Fetched')

        option_elems = elem_select.find_elements(By.TAG_NAME ,"option")
        print('Options Fetched')

        active = False
        
        for opt in option_elems:
            opt_value = opt.get_attribute("value")
            print(f' keyword to search : {os.environ.get("KEYWORD")}')
            options.append(opt_value)
            print(opt_value.lower())
            if isinstance(opt_value, str) and os.environ.get('KEYWORD') in opt_value.lower():
                active = True
                print('Found')
                break
            
        if active:
            print('ACTIVE')
            return (None, True,options)
        else:
            print('NOT-ACTIVE')
            return (None, False,options)
    except Exception as e:
        print('ERROR')
        #logging.error('An error occurred: %s', e)
        #print(e)
        return (e, False,[])
    # finally:
    #     driver.quit()

if __name__ == '__main__':
    check()
