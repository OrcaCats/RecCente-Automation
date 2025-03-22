#simple moudle downloader
#add cross-platofrm capability
import ModLoad
depen = ['selenium',
       'cryptography',
       'webdriver-manager',
       'schedule'
       ]
#ModLoad.importDependencies(depen)

import time
import base64
import schedule
import datetime
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cryptography.fernet import Fernet

#custom module imports
import ParisCrypts as crypt
import Scheduler as sched

url = [
       "https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=c1a62643-ec0e-a373-347f-14d0a91315fb&occurrenceDate=20240524",
       "https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=4eccf5ef-4b16-4e71-ae7d-ed4cdff075ac&occurrenceDate=20240527"
       ]
debug = True


class BadmintonRegBot:
    def __init__(self, password):
       self.encry = crypt.StringEncryptor(password)
       self.email = self.encry.encrypt(str(input('Enter MySurrey email: ')))
       self.password = self.encry.encrypt(str(input('Enter MySurrey password: ')))
       self.cardnum = self.encry.encrypt(str(input('Enter your credit card number: ')))
       self.cardnam = self.encry.encrypt(str(input('Enter your credit card name: ')))
       self.carddate = self.encry.encrypt(str(input('Enter the expiry date (mm/yy): ')))
       self.cardcvc = self.encry.encrypt(str(input('Enter your credit card cvc: '))) 
       if debug:
              print(self.cardcvc)

    def navigate(self):
       driver = webdriver.Chrome()
       driver.get(url[1]) #add date funct
       #time.sleep(10)
       regiTag = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.bm-button.bm-book-button')))
       #regiTag = driver.find_element(By.CSS_SELECTOR, '.bm-button.bm-book-button')
       regiTag.click()
       #time.sleep(5)
       LogInEmlIn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, 'emailid')))
       LogInEmlIn.send_keys(encry.decrypt(self.email))
       LogInPslIn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'loginradius-login-password')))
       LogInPslIn.send_keys(encry.decrypt(self.password))
       SignInBtn =  WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'loginradius-validate-login')))
       SignInBtn.click()
       time.sleep(6000)
       driver.quit()

class OverArch:
    def __init__(self):
        self.password = input('password: ')
        self.BadRB =BadmintonRegBot(self.password)
    def FridayBadmintonLoop(self):
        #loope weekly tues 7:15pm
        self.sch = sched.Scheduler()
        self.sch.schedule_task('sunday', '14:23', 3, 'seconds', self.BadRB.navigate)


r = OverArch()
r.FridayBadmintonLoop()
"""
time.sleep(10)
anchor_tag = driver.find_element(By.CSS_SELECTOR, '.bm-button.bm-book-button')
anchor_tag.click()
time.sleep(5)
LogInEmlIn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'emailid')))
LogInEmlIn.send_keys('testa@g.vb')
LogInPslIn = driver.find_element(By.ID, 'loginradius-login-password')
LogInPslIn.send_keys('testa@g.vb')
SignInBtn =  driver.find_element(By.ID, 'loginradius-validate-login')
time.sleep(6000)
driver.quit()"""