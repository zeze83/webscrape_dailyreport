from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def crawl_static_website(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        
        # Wait for the page to fully load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[.//h3[contains(@class, 'ng-binding')]]")))
        
        # Find all <a> elements that contain <h3> elements
        a_elements = driver.find_elements(By.XPATH, "//a[.//h3[contains(@class, 'ng-binding')]]")
        links = []

        for a in a_elements:
            href = a.get_attribute('href')
            if href:
                links.append(href)
                print(f"Found link: {href}")

        return links

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        driver.quit()

def crawl_content_from_links(links):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    all_titles = []

    try:
        for link in links:
            driver.get(link)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'ng-binding')))

            # Extracting content, e.g., h1 titles, or whatever you need
            titles = driver.find_elements(By.CLASS_NAME, 'ng-binding')  # Modify the selector as needed
            page_titles = [title.text.strip() for title in titles]
            all_titles.extend(page_titles)
            print(f"Extracted from {link}: {page_titles}")

    except Exception as e:
        print(f"An error occurred while crawling content: {e}")
    finally:
        driver.quit()
    
    return all_titles

def generate_summary(titles):
    summary = "今日总结:\n"
    for i, title in enumerate(titles, 1):
        summary += f"{i}. {title}\n"
    return summary

# URL for static scraping
static_url = 'https://www.modaily.cn/amucsite/web/index.html#/home'
print("Extracting H3 Links:")
links = crawl_static_website(static_url)
print("Extracting Content from Links:")
titles = crawl_content_from_links(links)
summary = generate_summary(titles)
print(summary)

# Save the summary to a file
with open('daily_summary.txt', 'w', encoding='utf-8') as file:
    file.write(summary)
