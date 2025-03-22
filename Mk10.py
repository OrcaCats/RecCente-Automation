import os
import sys
import json
import time
import base64
import easyocr
import pyautogui
import random as r
from PIL import ImageGrab
import undetected_chromedriver as uc
from cryptography.fernet import Fernet
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
'''
#System path append for importing from other dirs
sys.path.append("WebAutomation")
'''
# Custom module imports, ParisCrypts, 
import ParisCrypts as crypt

# Define URLs
url = [
    "https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=611034e3-724a-4362-b3fc-45e1ce932c37&occurrenceDate=20240613",
    "https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=95c2b0f6-fcd8-fa67-6de2-c15a03cd4fc1&occurrenceDate=20240609",
    'https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=1e1495fe-a10c-42e8-aa51-808680e293c2&occurrenceDate=20240604'
]

debug = False
emuPsn = True

def move_text_on_screen(text, delay=1):
    def find_text_coordinates(image_path, text):
        reader = easyocr.Reader(['en'])
        results = reader.readtext(image_path)
        for (bbox, word, confidence) in results:
            if word.lower() == text.lower():
                (top_left, top_right, bottom_right, bottom_left) = bbox
                return (top_left, top_right, bottom_right, bottom_left)
        return None

    screenshot = pyautogui.screenshot()
    screenshot_path = 'TempScreenshot.png'
    screenshot.save(screenshot_path)

    coordinates = find_text_coordinates(screenshot_path, text)

    if coordinates:
        (top_left, top_right, bottom_right, bottom_left) = coordinates
        center_x = int((top_left[0] + bottom_right[0]) / 2)
        center_y = int((top_left[1] + bottom_right[1]) / 2)
        pyautogui.moveTo(center_x, center_y, duration=delay)
        print(f"'{text}': {center_x}, {center_y}")
    else:
        print(f"'{text}' not found on the screen")

def EmuWait():
    if emuPsn:
        time.sleep(r.uniform(0.5, 2.0))

class BadmintonRegBot:
    def __init__(self, password):
        try:
            with open('salt.txt', 'r') as saltf:
                salt = base64.urlsafe_b64decode(saltf.read().encode('utf-8'))
                if debug:
                    print('Successfully opened salt', salt)
        except FileNotFoundError:
            salt = None
        self.encry = crypt.StringEncryptor(password, input('Regen Salt(true/false): ').lower(), salt)
        self.load_or_create_preset()

    def load_or_create_preset(self):
        preset = 'EncryPrst.json'
        overwrite = input("Overwrite preset(true/false): ")
        if overwrite.lower() == 'true':
            data = {
                'MySEmail': self.encry.encrypt(input('Enter MySurrey email: ')),
                'password': self.encry.encrypt(input('Enter MySurrey password: ')),
                'cardName': self.encry.encrypt(input('Enter your credit card name: ')),
                'cardNumb': self.encry.encrypt(input('Enter your credit card number: ')),
                'cardExpM': self.encry.encrypt(input('Enter the expiry month(1-12): ')),
                'cardExpY': self.encry.encrypt(input('Enter card expiry year(2XXX): ')),
                'cardCvvB': self.encry.encrypt(input('Card Cvv (XXX): ')),
                'regiMemb': self.encry.encrypt(input('Enter member: ')),
                'billadrs': self.encry.encrypt(input('Enter your billing address: ')),
                'billcity': self.encry.encrypt(input('Enter your billing city: ')),
                'billcout': self.encry.encrypt(input('Enter the country: ')),
                'billprov': self.encry.encrypt(input('Enter the province (British Columbia): ')),
                'pstlcode': self.encry.encrypt(input('Postal Code: '))
            }
            with open(preset, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print(f"File created and data saved: {preset}")

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
        
        self.billAdrs = data['billadrs']
        self.billCity = data['billcity']
        self.billCout = data['billcout']
        self.billProv = data['billprov']
        self.pstlCode = data['pstlcode']
        print(self.encry.decrypt(self.billAdrs))

    def navigate(self):
        driver = uc.Chrome()
        driver.maximize_window()
        driver.get(url[0])  # Add date functionality as needed

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.bm-button.bm-book-button'))).click()
        EmuWait()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, 'emailid'))).send_keys(self.encry.decrypt(self.MySEmail))
        EmuWait()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'loginradius-login-password'))).send_keys(self.encry.decrypt(self.password))
        EmuWait()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'loginradius-validate-login'))).click()
        EmuWait()

        wait = WebDriverWait(driver, 20)
        try:
            memberBtn = driver.find_element(By.ID, wait.until(EC.presence_of_element_located((By.XPATH, f"//label[text()='{self.encry.decrypt(self.regiMemb)}']"))).get_attribute("for"))
        except:
            memberBtn = driver.find_element(By.ID, wait.until(EC.presence_of_element_located((By.XPATH, f"//label[text()='{self.encry.decrypt(self.regiMemb) + ' (You)'}']"))).get_attribute("for"))

        memberBtn.click()
        EmuWait()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Next']"))).click()

        move_text_on_screen('Next')
        pyautogui.click()

        EmuWait()

        # Checkout process
        driver.switch_to.frame(WebDriverWait(driver, 2000).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe.online-store'))))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-bind*="floatingLabel: creditCard.nameOnCard"][class*="floating-label transform empty"]'))).send_keys(self.encry.decrypt(self.cardname))
        EmuWait()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-bind*="floatingLabel: creditCard.cardNumber"][class*="floating-label transform empty"]'))).send_keys(self.encry.decrypt(self.cardnumb))
        EmuWait()
        select = Select(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'section'))).find_elements(By.TAG_NAME, 'select')[0])
        select.select_by_value(self.encry.decrypt(self.cardmont))
        select = Select(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'section'))).find_elements(By.TAG_NAME, 'select')[1])
        select.select_by_value(self.encry.decrypt(self.cardyear))
        EmuWait()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))).send_keys(self.encry.decrypt(self.cardcvvb))
        EmuWait()

        # Billing address
        billing_address_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"][data-bind*="floatingLabel: creditCard.billingAddress.street"][class*="floating-label transform empty"]'))
        )
        billing_address_field.send_keys(self.encry.decrypt(self.billAdrs))
        EmuWait()
        billing_city_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"][data-bind*="floatingLabel: creditCard.billingAddress.city"][class*="floating-label transform empty"]'))
        )
        billing_city_field.send_keys(self.encry.decrypt(self.billCity))
        EmuWait()
        billing_state_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"][data-bind*="floatingLabel: creditCard.billingAddress.state"][class*="floating-label transform empty"]'))
        )
        billing_state_field.select_by_value(self.encry.decrypt(self.billProv))
        EmuWait()
        billing_postal_code_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"][data-bind*="floatingLabel: creditCard.billingAddress.postalCode"][class*="floating-label transform empty"]'))
        )
        billing_postal_code_field.send_keys(self.encry.decrypt(self.pstlCode))
        EmuWait()
        billing_country_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"][data-bind*="floatingLabel: creditCard.billingAddress.country"][class*="floating-label transform empty"]'))
        )
        billing_country_field.select_by_value(self.encry.decrypt(self.billCout))
        EmuWait()

        print("Process completed")
        time.sleep(6000)
        driver.quit()

# Example usage
b = BadmintonRegBot(input('password: '))
try:
    b.navigate()
except Exception as e:
    print(f"An error occurred: {e}")