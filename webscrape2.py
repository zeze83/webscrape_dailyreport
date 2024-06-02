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
            return []
        else:
            return [title.text.strip() for title in titles]

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        driver.quit()

def generate_summary(titles):
    summary = "今日总结:\n"
    for i, title in enumerate(titles, 1):
        summary += f"{i}. {title}\n"
    return summary

# URLs for static and dynamic scraping
static_url = 'https://www.modaily.cn/amucsite/web/index.html#/home'
dynamic_url = 'https://drive.google.com'

# Credentials for login
email = 'ippolitbattyp97@gmail.com'
password = 'pwawkiv8992y'

# URLs for static scraping
static_url = 'https://www.modaily.cn/amucsite/web/index.html#/home'
print("Static Website Titles:")
crawl_static_website(static_url) 
summary = generate_summary(crawl_static_website(static_url))
print(summary)

# Save the summary to a file
with open('daily_summary.txt', 'w', encoding='utf-8') as file:
    file.write(summary)
