from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient


def get_dict_letters():
    letter_dict = {}
    letter_dict['contact'] = driver.find_element_by_class_name("letter-contact").text
    letter_dict['date'] = driver.find_element_by_class_name("letter__date").text
    letter_dict['text'] = driver.find_element_by_class_name("letter__body").text
    return letter_dict

client = MongoClient('localhost', 27017)
db = client['letters']
letters_post = db.jobs

driver = webdriver.Chrome(executable_path='./chromedriver.exe')

driver.get('https://mail.ru/')

letters= []

elem = driver.find_element_by_xpath("//input[@name='login']")
elem.send_keys('study.ai_172')

elem.send_keys(Keys.ENTER)
time.sleep(2)
elem = driver.find_element_by_xpath("//input[@name='password']")
elem.send_keys('NextPassword172???')
time.sleep(2)
elem.send_keys(Keys.ENTER)
link_list = []
wait = WebDriverWait(driver,10)
time.sleep(10)
links = driver.find_elements_by_class_name('llc_normal')
for link in links:
    link_list.append(link.get_attribute('href'))
driver.get(link_list[0])
# пыталась реализовать прокрутку но не смогла
# подсмотрела в объяснении с пролистыванием писем
while True:
    try:
        wait = WebDriverWait(driver,5)
        button = wait.until(EC.element_to_be_clickable((By.XPATH,".//span[contains(""@class,'arrow-down')]")))
        letters.append(get_dict_letters())
        button.click()
    except:
        print('Конец')
        break

for let in letters:
    letters_post.insert_One(let)
