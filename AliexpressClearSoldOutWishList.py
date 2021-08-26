#!/usr/bin/env python2.6
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
import time
from lxml import html
from lxml import etree
from tqdm import tqdm

myUser = "[username/email]"
myPassword = "[password]"

urls = list()

def getDriver(proxy=False,headless=True):
	if proxy:
		proxy = "172.16.0.1:80"
		firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
		firefox_capabilities['marionette'] = True
		firefox_capabilities['proxy'] = {
			"proxyType": "MANUAL",
			"httpProxy": proxy,
			"ftpProxy": proxy,
			"sslProxy": proxy
		}
		if headless:
			options = FirefoxOptions()
			options.add_argument("--headless")
			return webdriver.Firefox(capabilities=firefox_capabilities,options=options)
		return webdriver.Firefox(capabilities=firefox_capabilities)
	else:
		if headless:
			options = FirefoxOptions()
			options.add_argument("--headless")
			return webdriver.Firefox(options=options)
		return webdriver.Firefox()

driver = getDriver(proxy=False,headless=False)
driver.maximize_window()
driver.get('https://login.aliexpress.com/')
#Login
element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "fm-login-id")))
element = driver.find_element_by_id("fm-login-id")
element.send_keys(myUser)
element = driver.find_element_by_id("fm-login-password")
element.send_keys(myPassword)
driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/button").click()

driver.switch_to.default_content()
element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "nav-user-account")))

for i in  tqdm(range(1,51,1)):
    driver.get('https://my.aliexpress.com/wishlist/wish_list_product_list.htm?&currentGroupId=0&page='+str(i))
    links = driver.find_elements_by_xpath('/html/body/div[4]/div[2]/div[2]/ul/li[@class="product sold-out util-clearfix js-product"]/div[2]/p/a')

    for a in links:
        urls.append(a.get_attribute("href"))

for u in  tqdm(urls):
    print(u)
    driver.get(u)
