#simple moudle downloader
#add cross-platofrm capability
import ModLoad
depen = ['selenium',
       'cryptography',
       'webdriver-manager',
       'schedule'
       ]
#ModLoad.importDependencies(depen)
import os
import json
import time
import base64
import schedule
import datetime
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
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
        try:
            saltf = open('salt.txt', 'r')
            print('sucess open salt')
            salt = base64.urlsafe_b64decode(saltf.read().encode('utf-8'))
            print(salt)
        except:
            salt = None
        self.encry = crypt.StringEncryptor(password, input('Regen Salt(true/false): ').lower(), salt)
        preset = 'EncryPrst.json'
        #write create file
        overwrite = input("Overwrite preset(true/false): ")
        if overwrite.lower() == 'true':
            data = {
                'MySEmail':self.encry.encrypt(str(input('Enter MySurrey email: '))),
                'password':self.encry.encrypt(str(input('Enter MySurrey password: '))),
                'cardName':self.encry.encrypt(str(input('Enter your credit card number: '))),
                'cardNumb':self.encry.encrypt(str(input('Enter your credit card name: '))),
                'cardExpd':self.encry.encrypt(str(input('Enter the expiry date (mm/yy): '))),
                'cardExpm':self.encry.encrypt(str(input('Enter card expird month(1-12): '))),
                'cardCvcB':self.encry.encrypt(str(input('Enter your credit card cvc: '))),
                'regiMemb':self.encry.encrypt(str(input('Enter member: ')))
            }
            with open(preset, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print(f"File created and data saved: {preset}")

        #open read file
        with open(preset, 'r') as json_file:
            data = json.load(json_file)
        self.MySEmail = data['MySEmail']
        self.password = data['password']
        self.cardname = data['cardName']
        self.cardnumb = data['cardNumb']
        self.carddate = data['cardExpd']
        self.cardmont = data['cardExpm']
        self.cardcvcb = data['cardCvcB']
        self.regiMemb = data['regiMemb']
        if debug:
           print(self.cardcvcb)

    def navigate(self):
        driver = webdriver.Chrome()
        driver.get(url[1]) #add date funct
        #time.sleep(10)
        regiTag = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.bm-button.bm-book-button')))
        #regiTag = driver.find_element(By.CSS_SELECTOR, '.bm-button.bm-book-button')
        regiTag.click()
        #time.sleep(5)
        LogInEmlIn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, 'emailid')))
        LogInEmlIn.send_keys(self.encry.decrypt(self.MySEmail))
        LogInPslIn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'loginradius-login-password')))
        LogInPslIn.send_keys(self.encry.decrypt(self.password))
        SignInBtn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'loginradius-validate-login')))
        SignInBtn.click()
        memberBtn = driver.find_element(By.ID, WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, f"//label[text()='{self.encry.decrypt(self.regiMemb)}']"))).get_attribute("for"))
        memberBtn.click()
        contBtn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Next']"))) 
        try :
            contBtn.click()
        except:
            time.sleep(1000)
        nextBtn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'bm-button')))
        nextBtn.click()
        #checkout card
        cardNameF = WebDriverWait(DRIVER, 20).until(EC.element_to_be_clickable((By.ID, 'credit-card-holder-name-151')))
        cardNameF.send_keys(self.encry.decrypt(self.cardname))
        cardNumbF = WebDriverWait(DRIVER, 20).until(EC.element_to_be_clickable((By.ID, 'credit-card-holder-number-151')))
        cardNumbF.send_keys(self.encry.decrypt(self.cardnumb))

        #checkout billing

        time.sleep(6000)
        driver.quit()

class OverArch:
    def __init__(self):
        #self.password = input('password: ')
        self.BadRB =BadmintonRegBot(self.password)
    def FridayBadmintonLoop(self):
        #loope weekly tues 7:15pm
        self.sch = sched.Scheduler()
        self.sch.schedule_task('sunday', '14:24', 3, 'seconds', self.BadRB.navigate)

'''
r = OverArch()
r.FridayBadmintonLoop()
'''
b = BadmintonRegBot('p')
b.navigate()
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