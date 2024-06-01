import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def crawl_static_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    titles = soup.find_all('h3', class_='ng-binding')  # Updated class name
    if not titles:
        print("No titles found.")
    else:
        for title in titles:
            print(title.text.strip())

def crawl_dynamic_website(url, email, password):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        
        # Login to Google account
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys(email)
        driver.find_element(By.ID, "identifierNext").click()
        
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
        driver.find_element(By.ID, "passwordNext").click()
        
        # Add a delay to ensure page loads completely
        time.sleep(10)
        
        links = driver.find_elements(By.TAG_NAME, 'a')
        if not links:
            print("No links found.")
        else:
            for link in links:
                print(link.text.strip())

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

# URLs for static and dynamic scraping
static_url = 'https://www.modaily.cn/amucsite/web/index.html#/home'
dynamic_url = 'https://drive.google.com'

# Credentials for login
email = 'ippolitbattyp97@gmail.com'
password = 'pwawkiv8992y'

# Crawl the static website
print("Static Website Titles:")
crawl_static_website(static_url)

# Crawl the dynamic website
print("\nDynamic Website Links:")
crawl_dynamic_website(dynamic_url, email, password)
