import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
from extract import Soup, TagName
import time
from config import BASE_URL, HOME, FILENAME

#setup driver
options = Options()
options.add_argument('window-size=1080x1080')
options.add_argument("--lang=en-US,en")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36")

driver = webdriver.Chrome("./chromedriver",options=options)

#TESTING
#anti-detecting crawl https://stackoverflow.com/questions/47374913/how-do-i-mimic-or-set-plugin-for-chrome-headless
# driver.get('https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html')
# driver.save_screenshot("screenshot5.png")
# driver.close()


#store web page
driver.get(BASE_URL+HOME)
soup = bs(driver.page_source, 'html.parser')
with open(FILENAME, "w") as f1:
    f1.write(str(soup))

#store cookies
#ref: https://stackoverflow.max-everyday.com/2019/04/python-selenium-how-to-save-and-load-cookies/
pickle.dump(driver.get_cookies(), open("cookies.pkl","wb"))
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

#close the modal dialog
#chrome extension: X_path finder
time.sleep(3)
driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/button").click()

#get product urls
BSsoup = Soup(FILENAME)
class_name_href = "js-product-link theme-grey-dark db"
# href_strs = BSsoup.select_by_class("a", class_name_href, TagName.HREF)

#find product url
time.sleep(2)
elem = driver.find_element_by_css_selector("div[class='w-100']>a")
driver.execute_script("window.scrollTo(0, 500)") 

#click
time.sleep(2)
elem.click()
#FAILED

# driver.close()