from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime

# Function to get the current timestamp
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Constants:
LINKEDIN_LOGIN_URL = "https://www.linkedin.com/login"
FILTER_SEARCH_URL = "https://www.linkedin.com/jobs/search/?currentJobId=3813109947&f_AL=true&f_E=2%2C3&f_JT=F%2CC&f_SB2=4&f_WT=2&keywords=python&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R"

linkedin_dictionary = {
    "email": "YOUROWNEMAIL",
    "linkedin_password": "YOUROWNPASSWORD",
    # Other dictionary items...
}

# Setup webdriver
def setup_chrome_driver_for_selenium():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(LINKEDIN_LOGIN_URL)
    return driver

# Define the safe_click_easy_apply function here
def safe_click_easy_apply(driver, css_selector, max_retries=3):
    """
    Attempts to click the 'Easy Apply' button, with retries for stale elements.
    """
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
        print(f"{get_timestamp()}: Successfully clicked the 'Easy Apply' button.")
    except TimeoutException as e:
        print(f"{get_timestamp()}: Timeout while waiting for the 'Easy Apply' button. {e}")
    except StaleElementReferenceException as e:
        if max_retries > 0:
            print(f"{get_timestamp()}: Encountered a stale element, retrying... {e}")
            time.sleep(1)  # Brief pause to let the page stabilize
            safe_click_easy_apply(driver, css_selector, max_retries-1)
        else:
            print(f"{get_timestamp()}: Failed to click 'Easy Apply' after retries. {e}")

# Continue with the setup
driver = setup_chrome_driver_for_selenium()

# Login procedure
def login_to_linkedin(driver, email, password):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(email)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "password"))).send_keys(password + Keys.ENTER)
    print(f"{get_timestamp()}: Successfully logged in.")

login_to_linkedin(driver, linkedin_dictionary["email"], linkedin_dictionary["linkedin_password"])

print(f"{get_timestamp()}: Navigating to the filter search URL.")
driver.get(FILTER_SEARCH_URL)

# Click the "easy apply" filter button
try:
    easy_apply_filter_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Easy Apply filter.']"))
    )
    easy_apply_filter_button.click()
    print(f"{get_timestamp()}: Easy apply filter applied.")
except TimeoutException:
    print(f"{get_timestamp()}: Easy apply filter button was not clickable.")

# Maximize window or set a specific size
def maximize_a_window():
    try:
        driver.maximize_window()
        print(f"{get_timestamp()}: Window maximized successfully.")
    except Exception as e:
        print(f"{get_timestamp()}: Initial maximize window failed. Adjusting the window a different way: {e}")
        driver.set_window_size(1920, 1080)

maximize_a_window()

# Implement the safe_click_easy_apply function instead of direct element interaction
job_card_container_css = "li.job-card-container__apply-method.job-card-container__footer-item.inline-flex.align-items-center"
safe_click_easy_apply(driver, job_card_container_css)

# Optionally, close the browser at the end of the session
# driver.quit()
