from selenium import webdriver
import time


PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
driver = webdriver.Chrome(PATH)

driver.get('https://mycares.net')
# time.sleep(20)