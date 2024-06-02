from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def crawl_static_website(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        
        # Wait for the page to fully load
        time.sleep(10)
        
        # Get page source after JavaScript has rendered
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        titles = soup.find_all('h3', class_='ng-binding')  # Confirm the class name
        if not titles:
            print("No titles found.")
        else:
            for title in titles:
                print(title.text.strip())

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

# URLs for static scraping
static_url = 'https://www.modaily.cn/amucsite/web/index.html#/home'
print("Static Website Titles:")
crawl_static_website(static_url)