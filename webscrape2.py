from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def crawl_static_website(url, click_selector=None):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        
        # Wait for the page to fully load
        time.sleep(10)
        
        # If click_selector is provided, click the element to navigate
        if click_selector:
            try:
                element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, click_selector)))
                element.click()
                time.sleep(10)  # Wait for the new page to load
            except Exception as e:
                print(f"An error occurred while clicking: {e}")
        
        # Find all titles using Selenium
        titles = driver.find_elements(By.CLASS_NAME, 'ng-binding')
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

# URL for static scraping
static_url = 'https://www.modaily.cn/amucsite/web/index.html#/home'
# Selector for the element to click (modify as needed)
click_selector = '.some-css-selector'  # Change this to the actual selector
print("Static Website Titles:")
titles = crawl_static_website(static_url, click_selector)
summary = generate_summary(titles)
print(summary)

# Save the summary to a file
with open('daily_summary.txt', 'w', encoding='utf-8') as file:
    file.write(summary)
