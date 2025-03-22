#member prototype
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver (for example, using Chrome)
driver = webdriver.Chrome()

# Open the webpage
driver.get("https://cityofsurrey.perfectmind.com/23615/Menu/BookMe4EventParticipants?eventId=c1087d89-b663-f5f3-c8b2-c1c667771425&occurrenceDate=20240527&widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&locationId=a89fe9f3-5ece-4158-a87d-c61ec1e99601&waitListMode=False")

# Wait until the element is present
wait = WebDriverWait(driver, 10)
label_element = wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Micah Hou (You)']")))

# Find the corresponding checkbox input using the label element
checkbox_id = label_element.get_attribute("for")
micah_hou_checkbox = driver.find_element(By.ID, checkbox_id)

# Click the checkbox
micah_hou_checkbox.click()

# Close the WebDriver
driver.quit()