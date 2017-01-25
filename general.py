# coding: utf-8

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
import time
from selenium.webdriver.support import expected_conditions as EC
import xlrd



def state_checker():
    wb = xlrd.open_workbook('WEF ACADEMIC Master MA Dues Table_Dec.xlsx')
    sheet = wb.sheet_by_name('2017 Dues')
    states = []
    for col in xrange(sheet.nrows - 1):
        states.append(sheet.cell_value(col + 1, 0))
    print 'Status checking test start..'
    driver = webdriver.Chrome()
    # driver = webdriver.PhantomJS()
    base_url = "http://joinwef.stg.lin.panth.com/main_form_WEF.php?code=587def2dd43f1&fName=Denial&lName=Redclip"
    state_field = 'state'
    step_2_title = "//h3[contains(text(), 'Membership Type and Member Association')]"
    price_list_new = []

    states_number = len(states)
    for i in xrange(states_number):
        driver.get(base_url)
        # time.sleep(1)
        current_state = states[i]
        # current_price = price[i]
        ma1_label = ".//*[@id='MA_1_label']"
        # ma_1_element = "//div[contains(@id, 'MA_option_1')]/*[starts-with(., " + "'" + current_state + "')]"
        # current_ma1_price_element = "//div[contains(@id, 'MA_option_1')]/span[contains(text(), '"+current_price+"')]"
        driver.find_element_by_id(state_field).clear()
        # time.sleep(1)
        driver.find_element_by_id(state_field).send_keys(current_state)
        # time.sleep(5)
        driver.find_element_by_xpath(".//*[@id='continue1']").click()
        time.sleep(1)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, step_2_title)))
        except:
            print "Step 2 page not loaded."

        # driver.find_element_by_xpath(".//*[@id='MA_1']").click()
        # time.sleep(1)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ".//*[@id='MA_price_1']")))
            # driver.find_element_by_xpath(".//*[@id='MA_price_1']")
        except:
            print "MA_1 price for %s not found." %current_state

        time.sleep(1)
        get_cuttent_ma1_label = driver.find_element_by_xpath(ma1_label).text
        get_current_price = driver.find_element_by_xpath(".//*[@id='MA_price_1']").text
        # for element in driver.find_elements_by_class_name("price"):
        #     print element.text
        price_list_new.append(get_current_price)
        # print current_state
        # print get_current_price
        # print get_cuttent_ma1_label
        print (get_cuttent_ma1_label+'  '+get_current_price+'  '+ current_state)

    driver.quit()


state_checker()
raw_input("Task Completed. Press Enter to exit..")