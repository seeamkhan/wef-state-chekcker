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

    # Set the member type here.
    # member = 'aca'
    # member = 'pro'
    member = 'sw'
    file_name = ''

    if (member == 'aca'):
        file_name = "WEF ACADEMIC Master MA Dues Table_Dec.xlsx"
    elif (member == 'pro' or member == 'sw'):
        file_name = "WEF PROFESSIONAL Master MA Dues Table_Dec.xlsx"
    wb = xlrd.open_workbook(file_name)
    sheet = wb.sheet_by_name('2017 Dues')
    states = []
    prices = []
    correct_price_state = 0
    wrong_price_state = 0
    log = []
    message = ''

    for col in xrange(sheet.nrows - 1):
        states.append(sheet.cell_value(col + 1, 0))

    for col in xrange(sheet.nrows - 1):
        xl_price = str(sheet.cell_value(col + 1, 3))
        prices.append(xl_price)
    # print prices

    print 'Status checking test start..'
    driver = webdriver.Chrome()
    # driver = webdriver.PhantomJS()

    # Set URL according to member type
    if (member == 'aca'):
        base_url = "https://joinwef.org/main_form_WEF.php?code=58882986575d0&fName=Pantheon&lName=Member10"
    elif (member == 'pro'):
        base_url = "https://joinwef.org/main_form_WEF.php?code=588825ac4e897&fName=Pantheon&lName=Member9"
    elif (member == 'sw'):
        base_url = "https://joinwef.org/main_form_WEF.php?code=58882b9b53c7b&fName=Pantheon&lName=Member11"
    else:
        log.append("Wrong membership type. Test failed.")
        base_url = ""

    state_field = 'state'
    step_2_title = "//h3[contains(text(), 'Membership Type and Member Association')]"
    price_list_new = []

    message = base_url
    log.append(message)
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
            message = "Step 2 page not loaded."
            log.append(message)
            print message

        # driver.find_element_by_xpath(".//*[@id='MA_1']").click()
        # time.sleep(1)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ".//*[@id='MA_price_1']")))
            # driver.find_element_by_xpath(".//*[@id='MA_price_1']")
        except:
            message = "MA_1 price for %s not found." %current_state
            log.append(message)
            print message

        time.sleep(1)
        get_cuttent_ma1_label = driver.find_element_by_xpath(ma1_label).text
        get_current_price = driver.find_element_by_xpath(".//*[@id='MA_price_1']").text
        # for element in driver.find_elements_by_class_name("price"):
        #     print element.text
        price_list_new.append(get_current_price)
        # print current_state
        # print get_current_price
        # print get_cuttent_ma1_label
        # print (get_cuttent_ma1_label+'  '+get_current_price+'  '+ current_state)
        trimmed_current_price =  get_current_price[2:]
        # print trimmed_current_price
        # print prices[i]
        try:
            if (prices[i] in trimmed_current_price):
                correct_price_state=correct_price_state+1
                message = "State '%s' price matches." % current_state
                log.append(message)
                print message
            else:
                message = "Error! State '%s' price does not match.\nIn Website the price is: %s\nIn Excel Sheet the price is: %s" % (current_state, trimmed_current_price, prices[i])
                log.append(message)
                print message
                wrong_price_state = wrong_price_state+1
        except:
            print 'Price error found.'

    message = "------------------------\nTotal %s states price are correct." % str(correct_price_state)
    log.append(message)
    print message
    message = "Total %s states price are wrong.\n------------------------" % str(wrong_price_state)
    log.append(message)
    print message
    driver.quit()
    final_log = '\n'.join(log)
    return final_log


# Function for writing the final output in a file named 'plugin_report.txt'. New file will be created if the file is not already exist.
def write_output(something):
    target = open("log", 'w')
    target.truncate()
    target.write(something)
    target.close()

# state_checker()
result = state_checker()
write_output(result)
# raw_input("Task Completed. Press Enter to exit..")