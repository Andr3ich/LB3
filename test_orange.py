import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login_success(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/")
    wait = WebDriverWait(driver, 30)

    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    
    username_field.send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.TAG_NAME, "button").click()
    
    wait.until(EC.url_contains("dashboard"))
    assert "dashboard" in driver.current_url

def test_login_failure(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/")
    wait = WebDriverWait(driver, 30)
    
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    username_field.send_keys("Invalid")
    driver.find_element(By.NAME, "password").send_keys("wrong123")
    driver.find_element(By.TAG_NAME, "button").click()
    
    error_msg = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "oxd-alert-content-text")))
    assert error_msg.text == "Invalid credentials"

def test_navigation_admin(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/")
    wait = WebDriverWait(driver, 30)
    
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    username_field.send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.TAG_NAME, "button").click()
    
    admin_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Admin']")))
    admin_menu.click()
    
    header = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h6")))
    assert header.text == "Admin"
