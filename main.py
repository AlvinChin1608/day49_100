from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time

# Load environment variables from the .env file
load_dotenv("./vars/.env")

YOUR_EMAIL = os.getenv("linkedln_email")
YOUR_PASSWORD = os.getenv("linkedln_password")

def abort_application(driver):
    try:
        # Click Close Button
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "artdeco-modal__dismiss"))
        )
        close_button.click()
        time.sleep(2)

        # Click Discard Button
        discard_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn"))
        )
        discard_button.click()
    except NoSuchElementException:
        print("No close/discard button found, moving on.")

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3923831221&f_AL=true&geoId=102454443&keywords=python%20developer&location=Singapore&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true")

# Wait for the sign-in button to be clickable and click it
sign_in = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/a[1]'))
)
sign_in.click()

# Sign in
email_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "username"))
)
email_field.send_keys(YOUR_EMAIL)

password_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "password"))
)
password_field.send_keys(YOUR_PASSWORD)
password_field.send_keys(Keys.ENTER)

# Wait for the job listings to load
all_listings = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container--clickable"))
)

# Save the jobs
for listing in all_listings:
    print("Opening Listing")
    listing.click()
    time.sleep(2)
    try:
        # Click to save jobs button
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[6]/div/button'))
        )
        save_button.click()
    except NoSuchElementException:
        abort_application(driver)
        print("No save button, skipped.")
        continue

time.sleep(5)
driver.quit()
