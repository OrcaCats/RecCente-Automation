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
       "https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=c914f521-f459-c203-28c3-8536cab22143&occurrenceDate=20240527"
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
                'cardExpM':self.encry.encrypt(str(input('Enter the expiry month(1-12): '))),
                'cardExpY':self.encry.encrypt(str(input('Enter card expiry year: '))),
                'cardCvcB':self.encry.encrypt(str(input('Card Cvc: '))),
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
        self.cardcvcb = data['cardCvcB']
        self.regiMemb = data['regiMemb']
        if debug:
           print(self.cardcvcb)

    def navigate(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
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
        #try :
        print(contBtn)
        contBtn.click()
        #except:
        
        time.sleep(10)
        nextBtn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'bm-button')))
        nextBtn.click()
        #checkout card
        cardNameF = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'credit-card-holder-name-151')))
        cardNameF.send_keys(self.encry.decrypt(self.cardname))
        cardNumbF = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'credit-card-holder-number-151')))
        cardNumbF.send_keys(self.encry.decrypt(self.cardnumb))
        cardExpMo = WebDriverWait(driver, 20).until(EC.element_to_be_selected((By.ID, 'expiry-month-151')))
        selectEXM = Select(cardExpDa)
        selectEXM.select_by_value(self.encry.decrypt(self.cardmont))
        cardExpYr = WebDriverWait(driver, 20).until(EC.element_to_be_selected((By.ID, 'expiry-month-151')))
        selectEXY = Select(cardExpDa)
        selectEXY.select_by_value(self.encry.decrypt(self.cardyear))
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
