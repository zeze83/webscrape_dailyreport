from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time


def crawl_static_website(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=options
    )
    
    try:
        driver.get(url) 

        # Wait for the page to fully load
        time.sleep(5)
        
        # Find all titles using Selenium
        titles = driver.find_elements(By.XPATH, "//h3[@class='ng-binding']")
        if not titles:
            print("No titles found.")
            return []
        else:
            output_titles = [title.text.strip() for title in titles]
            
            for title in titles:
                # Click on the title element
                title.click()

                # Switch to the new tab
                driver.switch_to.window(driver.window_handles[1])
                
                # Wait for the new page to load
                time.sleep(10)
                # Log the URL of the new page
                print("Open the title page...")
                print(driver.current_url)

                # Get the contents of the new page
                contents = driver.find_elements(By.XPATH, "//div[@class='ng-binding']/p")
                print("\n".join([content.text for content in contents][1:]))
                
                driver.close()

                # Optionally, switch back to the first window
                driver.switch_to.window(driver.window_handles[0])

            return output_titles

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
print("Static Website Titles:")
titles = crawl_static_website(static_url)
summary = generate_summary(titles)
print(summary)

# Save the summary to a file
with open('daily_summary.txt', 'w', encoding='utf-8') as file:
    file.write(summary)
