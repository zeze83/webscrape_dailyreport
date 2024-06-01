############################################################
import requests
from bs4 import BeautifulSoup

# 定义爬取函数
def crawl_website(url):
    # 发送GET请求
    response = requests.get(url)
    
    # 检查响应状态码
    if response.status_code == 200:
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        # 文章标题在class为title的标签下?
        titles = soup.find_all('h2', class_='title')
        for title in titles:
            print(title.text)
    else:
        print("Failed to retrieve page.")

# 调用爬取函数
url = 'https://www.modaily.cn/amucsite/web/index.html#/home'
crawl_website(url)

############################################################

from selenium import webdriver
from selenium.webdriver.common.by import By

# 设置 ChromeDriver 路径
chrome_driver_path = "/path/to/chromedriver"

# 创建 Chrome WebDriver 对象
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式，不打开浏览器窗口
options.add_argument('--disable-gpu')  # 禁用 GPU 加速
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

# 打开 Google Drive 页面
driver.get('https://drive.google.com')

# 登录到你的 Google 账号
# 请按照你的具体情况自行实现登录过程

# 导航到你要爬取的页面
# 请按照你的具体需求导航到你想要爬取的页面

# 获取所有链接的文本内容
links = driver.find_elements(By.TAG_NAME, 'a')
for link in links:
    print(link.text)

# 关闭 WebDriver 对象
driver.quit()

############################################################

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
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
    titles = soup.find_all('h3', class_='title')
    if not titles:
        print("No titles found.")
    for title in titles:
        print(title.text.strip())

def crawl_dynamic_website(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        
        # Implement login if necessary
        # Example:
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys("your-email")
        # driver.find_element(By.ID, "identifierNext").click()
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("your-password")
        # driver.find_element(By.ID, "passwordNext").click()

        # Add a delay to ensure page loads completely
        time.sleep(5)
        
        links = driver.find_elements(By.TAG_NAME, 'a')
        for link in links:
            print(link.text.strip())

    finally:
        driver.quit()

# URLs for static and dynamic scraping
static_url = 'https://www.modaily.cn/amucsite/web/index.html#/home'
dynamic_url = 'https://drive.google.com'

# Crawl the static website
print("Static Website Titles:")
crawl_static_website(static_url)

# Crawl the dynamic website
print("\nDynamic Website Links:")
crawl_dynamic_website(dynamic_url)
