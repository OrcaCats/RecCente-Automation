#simple moudle downloader
#add cross-platofrm capability
import ModLoad
depen = ['selenium',
       'cryptography',
       'webdriver-manager',
       'schedule',
       'mouse'
       ]
#ModLoad.importDependencies(depen)

import os
import json
import time
import base64
import schedule
import datetime
import selenium
import pyautogui
import random as r
import undetected_chromedriver as uc
from cryptography.fernet import Fernet
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#custom module imports
import ParisCrypts as crypt
import Scheduler as sched

url = [
       "https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=e288ed98-37d9-df59-7981-f5b1ef1bb9d7&occurrenceDate=20240530",
       "https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=c914f521-f459-c203-28c3-8536cab22143&occurrenceDate=20240527",
       'https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=158b12cd-c312-fcd9-d6c9-91b9db2665ba&occurrenceDate=20240528',
       'https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=db1b10c3-c74c-496b-a154-961dbd3a9839&occurrenceDate=20240527'
       ]
debug = False


class BadmintonRegBot:
    def __init__(self, password):
        try:
            saltf = open('salt.txt', 'r')
            if debug:
                print('sucess open salt')
            salt = base64.urlsafe_b64decode(saltf.read().encode('utf-8'))
            if debug:
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
                'cardName':self.encry.encrypt(str(input('Enter your credit card name: '))),
                'cardNumb':self.encry.encrypt(str(input('Enter your credit card number: '))),
                'cardExpM':self.encry.encrypt(str(input('Enter the expiry month(1-12): '))),
                'cardExpY':self.encry.encrypt(str(input('Enter card expiry year(2XXX): '))),
                'cardCvvB':self.encry.encrypt(str(input('Card Cvv (XXX): '))),
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
        self.cardmont = data['cardExpM']
        self.cardyear = data['cardExpY']
        self.cardcvvb = data['cardCvvB']
        self.regiMemb = data['regiMemb']
        if debug:
           print(self.cardcvcb)

    def navigate(self):
        driver = uc.Chrome()
        driver.maximize_window()
        driver.get(url[2]) #add date funct
        #time.sleep(10)
        regiTag = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.bm-button.bm-book-button')))
        #regiTag = driver.find_element(By.CSS_SELECTOR, '.bm-button.bm-book-button')
        regiTag.click()
        time.sleep(2)
        LogInEmlIn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, 'emailid')))
        LogInEmlIn.send_keys(self.encry.decrypt(self.MySEmail))
        time.sleep(2)
        LogInPslIn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'loginradius-login-password')))
        LogInPslIn.send_keys(self.encry.decrypt(self.password))
        time.sleep(2)
        SignInBtn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'loginradius-validate-login')))
        SignInBtn.click()
        time.sleep(2)
        try:
            memberBtn = driver.find_element(By.ID, WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, f"//label[text()='{self.encry.decrypt(self.regiMemb)}']"))).get_attribute("for"))
        except:
            memberBtn = driver.find_element(By.ID, WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, f"//label[text()='{self.encry.decrypt(self.regiMemb) + ' (You)'}']"))).get_attribute("for"))
        memberBtn.click()
        time.sleep(2)
        contBtn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Next']"))) 
        contBtn.click()
        nextBtn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Add to Cart' and @class='bm-button']")))
        position = nextBtn.location
        x = position['x']
        y = position['y']
        print(f'Element position: x={x}, y={y}')
        size = nextBtn.size
        width = size['width']
        height = size['height']
        print(f'Element size: width={width}, height={height}')
        x = position['x'] + size['width'] / 2
        y = position['y'] + size['height'] / 2
        time.sleep(1)
        pyautogui.moveTo(x, y+70)
        pyautogui.click()

        time.sleep(2)
        #checkout
        driver.switch_to.frame(WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe.online-store'))))
        cardNameF = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-bind*="floatingLabel: creditCard.nameOnCard"][class*="floating-label transform empty"]')))
        cardNameF.send_keys(self.encry.decrypt(self.cardname))
        time.sleep(2)
        cardNumbF = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-bind*="floatingLabel: creditCard.cardNumber"][class*="floating-label transform empty"]')))
        cardNumbF.send_keys(self.encry.decrypt(self.cardnumb))
        time.sleep(2)
        select = Select(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'section'))).find_elements(By.TAG_NAME, 'select')[0])
        select.select_by_value(self.encry.decrypt(self.cardmont))
        select = Select(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'section'))).find_elements(By.TAG_NAME, 'select')[1])
        select.select_by_value(self.encry.decrypt(self.cardyear))
        '''
        cardExpMo = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-bind*="floatingLabel: creditCard.expiryMonth"][class*="floating-label transform empty"]')))
        selectEXM = Select(self.encry.decrypt(self.cardmont))
        time.sleep(2)
        cardExpMo = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-bind*="floatingLabel: creditCard.expiryYear"][class*="floating-label transform empty"]')))
        selectEXM = Select(self.encry.decrypt(self.cardyear))'''
        time.sleep(2)
        try:
            cardCVV = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-bind*="floatingLabel: {}"][class*="floating-label transform empty"]')))
            print('cvv selected')
            cardCVV.send_keys(self.encry.decrypt(self.cardcvvb))
            print('cvv success')
        except:
            print(6)
            pass
        time.sleep(2)

        time.sleep(6000)
        driver.quit()
    
    def simClickID(self, tag):
        time.sleep(2)
        nextBtn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, tag)))
        position = nextBtn.location
        x = position['x']
        y = position['y']
        print(f'Element position: x={x}, y={y}')
        size = nextBtn.size
        width = size['width']
        height = size['height']
        print(f'Element size: width={width}, height={height}')
        x = position['x'] + size['width'] / 2
        y = position['y'] + size['height'] / 2
        time.sleep(1)
        pyautogui.moveTo(x, y+70)
        pyautogui.click()

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
