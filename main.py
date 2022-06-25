from locale import setlocale, LC_NUMERIC, atof
from unicodedata import decimal
import threading

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import selenium
import os
import time

browser = webdriver.Chrome()
browser.get("https://orteil.dashnet.org/cookieclicker/")
time.sleep(3)
try:
    english = browser.find_element(By.CLASS_NAME, "langSelectButton")
    english.click()
except:
    pass
time.sleep(3)

try:
    settings = browser.find_element(By.CLASS_NAME, "subButton")
    settings.click()
    time.sleep(.05)
    short_numbers = browser.find_element(By.ID, "formatButton")
    browser.execute_script("window.scrollTo(0," + str(short_numbers.location_once_scrolled_into_view) + " )")
    short_numbers.click()
    time.sleep(2)
    browser.execute_script("window.scrollTo(0," + str(settings.location_once_scrolled_into_view) + " )")
    settings.click()
except:
    pass

try:
    settings = browser.find_element(By.CLASS_NAME, "subButton")
    settings.click()
    time.sleep(.05)
    load_save = browser.find_elements(By.CLASS_NAME, "option.smallFancyButton")

    text = ""
    with open('save.txt', 'r') as f:
        text = f.readline()

    if(text != ""):
        browser.execute_script("arguments[0].click();", load_save[3])
        time.sleep(2)
        textarea = browser.find_element(By.ID, "textareaPrompt")
        textarea.send_keys(text)
        time.sleep(2)
        textarea.send_keys(Keys.ENTER)


    time.sleep(1)
    short_numbers = browser.find_element(By.ID, "formatButton")
    #print(short_numbers.get_attribute("class"))
    if(short_numbers.get_attribute("class") != "smallFancyButton prefButton option off"):
        browser.execute_script("window.scrollTo(0," + str(short_numbers.location_once_scrolled_into_view) + " )")
        short_numbers.click()
        time.sleep(2)
        browser.execute_script("window.scrollTo(0," + str(settings.location_once_scrolled_into_view) + " )")
    settings.click()
except:
    pass







game_over = False
section_right = browser.find_element(By.ID, 'sectionRight')
big_cookie = browser.find_element(By.ID, "bigCookie")
current_cookies = browser.find_element(By.ID, 'cookies')
#cookies_per_second = browser.find_element(By.ID, 'cookiesPerSecond')
upgrades = browser.find_element(By.ID, 'upgrades')
action = ActionChains(browser)
action.move_to_element_with_offset(upgrades, +0, +40)




def buy_buildings(browser, section_right, num_cookies):
    for i in range(18, -1, -1):
        item = browser.find_element(By.ID, "product" + str(i))
        #print(item.get_attribute("class"))
        #word = current_cookies.text[0:current_cookies.text.find("c") - 1]
        #word = word.replace(",", '')
        #num_cookies = float(word)

        if(item.get_attribute("class") == 'product unlocked enabled'):
            section_right.click()
            price = float(item.find_element(By.ID, "productPrice" + str(i)).text.replace(",", ''))

            if (num_cookies >= price):
                if(not item.is_displayed()):
                    browser.execute_script("window.scrollTo(0," + str(item.location_once_scrolled_into_view) + " )")
                browser.execute_script("arguments[0].click();", item)
                num_cookies -= price
        else:
            price = (item.find_element(By.ID, "productPrice" + str(i)).text.replace(",", ''))
            if(price != ""):
                price = float(price)
                num_owned = (browser.find_element(By.ID, 'productOwned'+str(i)).text)
                if(num_owned == ""):
                    num_owned = 0
                else:
                    num_owned = float(num_owned)
                if (price > num_cookies >= price * 0.6 and i > 0 and num_owned < float(browser.find_element(By.ID, 'productOwned'+str(i-1)).text)):# and cps >= price*0.01):
                    #print("working")
                    break


def click():
    action2 = ActionChains(browser)
    action2.move_to_element(big_cookie)
    #action2.click()
    action2.perform()
    for i in range(0, 15):
        action2 = ActionChains(browser)
        action2.click()
        action2.perform()
        #big_cookie.click()
        #browser.execute_script("arguments[0].click();", big_cookie)
        time.sleep(0.01)

time.sleep(1)

save_delay = 300
count = 0
start = time.time_ns()
end = 0
#browser.maximize_window()
while not game_over:

        start = time.time_ns()


        click()

        try:
            golden_cookie = browser.find_element(By.CLASS_NAME, "shimmer")
            golden_cookie.click()
        except:
            pass
        time.sleep(.01)
        word = current_cookies.text[0:current_cookies.text.find("c") - 1]
        word = word.replace(",", '')
        try:
            num_cookies = float(word)
        except:
            word = current_cookies.text[0:current_cookies.text.find("\n") - 1]
            word = word.replace(",", '')
            num_cookies = float(word)
            pass
        #word = cookies_per_second.text[current_cookies.text.find(":")+1:]
        #cps = float(word)

        buy_buildings(browser, section_right, num_cookies)

        browser.execute_script("window.scrollTo(0," + str(upgrades.location_once_scrolled_into_view) + " )")

        action = ActionChains(browser)
        action.move_to_element_with_offset(upgrades, +00, +40)
        action.click()
        time.sleep(0.005)
        action.perform()
        action.click()




        if(count>=save_delay):
            try:
                settings = browser.find_element(By.CLASS_NAME, "subButton")
                settings.click()
                time.sleep(.05)
                load_save = browser.find_elements(By.CLASS_NAME, "option.smallFancyButton")

                browser.execute_script("arguments[0].click();", load_save[2])
                time.sleep(2)

                textarea = browser.find_element(By.ID, "textareaPrompt")

                with open('save.txt', 'w') as f:
                    f.write(textarea.text)

                count = 0

                browser.execute_script("arguments[0].click();", settings)
                time.sleep(0.04)
            except:
                pass


        end = time.time_ns()
        count += (end - start) / 1000000000
