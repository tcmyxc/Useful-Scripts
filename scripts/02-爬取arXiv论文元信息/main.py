# -*- coding: utf-8 -*-
# from https://zhuanlan.zhihu.com/p/86763203，自己略作修改
import logging
import random
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

# log config
logging.basicConfig()
logger = logging.getLogger("[arXiv papers]")
logger.setLevel(logging.INFO)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


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


def main():
    years = [
        (0, 17),
        (1, 18),
        (2, 19),
        (3, 20),
        (4, 21),
        (5, 22),
    ]
    # 这些领域每年发的文章数目
    cs_year_papers = [30698, 41547, 55044, 71468, 77512, 6477]
    cs_cv_year_papers = [5704, 8606, 11601, 15326, 17223, 1284]
    cs_lg_year_papers = [5232, 10485, 19239, 25876, 26466, 1129]
    step = 2000
    for (idx, year) in years:
        items = []
        logger.info(f"year: {year}, total papers: {cs_cv_year_papers[idx]}")
        for start in range(0, cs_cv_year_papers[idx], step):
            logger.info(f"page: {start}")
            # 构造 URL
            url = f'https://arxiv.org/list/cs.CV/{year}?skip={start}&show={step}'
            # 爬数据
            html = get_one_page(url)
            # 解析数据
            soup = BeautifulSoup(html, features='html.parser')
            content = soup.dl
            # date = soup.find('h3')
            list_ids = content.find_all('a', title='Abstract')
            list_title = content.find_all('div', class_='list-title mathjax')
            list_authors = content.find_all('div', class_='list-authors')
            list_subjects = content.find_all('div', class_='list-subjects')

            for i, paper in enumerate(zip(list_ids, list_title, list_authors, list_subjects)):
                items.append([str(paper[0].text).split(":")[1],
                              str(paper[1].text)[7:],
                              str(paper[2].text)[10:],
                              str(paper[3].text)[10:]])
        
        # 写数据，写之前会去下重
        name = ['id', 'title', 'authors', 'subjects']
        paper = pd.DataFrame(columns=name, data=items)
        paper = paper.drop_duplicates("id",inplace=False)  # 去重
        paper.to_csv(f'20{year}_all.csv')

        # 根据关键词再过滤一次，然后再保存
        key_words = ["Long-Tailed"]
        selected_papers = paper[paper['title'].str.contains(key_words[0], case=False)]
        selected_papers = selected_papers.drop_duplicates("id",inplace=False)  # 去重
        selected_papers.to_csv(f'20{year}.csv')


if __name__ == '__main__':
    main()
