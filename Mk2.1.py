import ModLoad
import time
depen = ['selenium',
       'cryptography'
       ]
ModLoad.importDependencies(depen)

import base64
import selenium
from selenium import webdriver
from cryptography.fernet import Fernet
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

url = [
       "https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=c1a62643-ec0e-a373-347f-14d0a91315fb&occurrenceDate=20240524",
       "https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=32db5eaa-69d6-f210-e8ce-40a81856dff7&occurrenceDate=20240524"
       ]

# Function to encrypt a string
def encrypt_string(input_string, key):
    cipher_suite = Fernet(key)
    encrypted_string = cipher_suite.encrypt(input_string.encode())
    return encrypted_string

# Function to decrypt a string
def decrypt_string(encrypted_string, key):
    cipher_suite = Fernet(key)
    decrypted_string = cipher_suite.decrypt(encrypted_string).decode()
    return decrypted_string

class StringEncryptor:
    def __init__(self, password: str, salt: bytes):
        self.key = self.generate_key(password, salt)
        self.cipher_suite = Fernet(self.key)

    def generate_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def encrypt_string(self, input_string: str) -> bytes:
        encrypted_string = self.cipher_suite.encrypt(input_string.encode())
        return encrypted_string

    def decrypt_string(self, encrypted_string: bytes) -> str:
        decrypted_string = self.cipher_suite.decrypt(encrypted_string).decode()
        return decrypted_string
class RegiBot:
       def __init__(self):
              self.password = input('set password: ')
              salt = b'\x00'*16
              kdf = PBKDF2HMAC(
                     algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=100000,
                     backend=default_backend()
              )
              self.key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
       

driver = webdriver.Chrome()
driver.get(url[1] )
time.sleep(10)
#anchor = driver.find_element(By.CLASS_NAME, 'bm-button bm-book-button')
#anchor.click()
anchor_tag = driver.find_element(By.CSS_SELECTOR, '.bm-button.bm-book-button')
anchor_tag.click()
time.sleep(5)
LogInEmlIn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'emailid')))
LogInEmlIn.send_keys('testa@g.vb')
LogInPslIn = driver.find_element(By.ID, 'loginradius-login-password')
LogInPslIn.send_keys('testa@g.vb')
SignInBtn =  driver.find_element(By.ID, 'loginradius-validate-login')
time.sleep(6000)
driver.quit()