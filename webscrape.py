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
        titles = category_div.find_all('h2', class_='title')
        for title in titles:
            print(title.text)
    else:
        print("Failed to retrieve page.")

# 调用爬取函数
url = 'https://www.modaily.cn/amucsite/web/index.html#/home'
crawl_website(url)
