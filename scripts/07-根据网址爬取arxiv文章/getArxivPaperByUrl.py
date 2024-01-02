import re

import logging
import random
import time

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

# log config
FORMAT = '[%(levelname)s %(asctime)s] %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger("Get arxiv paper")
logger.setLevel(logging.INFO)


def get_one_page(url):
	# 爬前睡一会，太频繁会被远程服务器拒绝连接
    time.sleep(1 + random.uniform(0, 10))
    response = requests.get(url, headers=headers)
    logger.info(f"status code: {response.status_code}")

    while response.status_code == 403 or response.status_code == 10054:
        time.sleep(500 + random.uniform(0, 500))
        response = requests.get(url)
        logger.info(f"status code: {response.status_code}")

    if response.status_code == 200:
        return response.text

    return None

def extract_year_month_from_arxiv_url(url):
    # 使用正则表达式匹配年份和月份
    match = re.search(r'/(\d{2})(\d{2})\.\d+', url)
    if match:
        year = '20' + match.group(1)
        month = match.group(2)
        return year, month
    else:
        return None, None


def download_arxiv_paper(url):
    
    year, month = extract_year_month_from_arxiv_url(url)
    # 获取 HTML 页面
    response = get_one_page(url)
    soup = BeautifulSoup(response, 'html.parser')
    
    title = str(soup.find('h1', class_='title mathjax').text)[6:].replace(':', '-')
    logger.info("paper title: " + title)
    
    # 提取标题
    title = f"[{year}-{month}] "  + title + '.pdf'
    logger.info("final title: " + title)

    # 构建 PDF 下载链接
    pdf_url = url.replace('abs', 'pdf') + '.pdf'

    # 下载 PDF
    pdf_response = requests.get(pdf_url)

    # 保存 PDF 到本地
    with open(title, 'wb') as f:
        f.write(pdf_response.content)

    logger.info(f'File saved as {title}')


if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, help="paper url, like 'https://arxiv.org/abs/2201.03545'")
    args = parser.parse_args()
    
    download_arxiv_paper(args.url)
