from urllib import request

import requests
import time
import csv
import random
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

iterate = 0

def parse_pages(url, num, iterate):
    response = requests.get(url=url, headers=headers)
    #save to html
    print('iterate '+str(iterate))
    iterate +=1
    html = getHtml(url)
    saveHtml('No. '+str(iterate)+' page', html)


    soup = BeautifulSoup(response.text, 'lxml')
    result_list = soup.find_all('h2', class_='title')
    print('title count'+str(len(result_list)))
    for result in result_list:
        # 标题
        title = result.find('a', class_='jobtitle turnstileLink').text.strip()
        results = [title]
        with open('indeed.csv', 'a', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f)
            w.writerow(results)



    #pagination

    pagination = soup.find_all('div', class_='pagination')
    '''
    pages = pagination[0].find_all('a')
    print(pages)
    print('page tag count: '+str(len(pages)))
    print("next page is")
    print(pages[len(pages)-1].get('href'))
    next_page_href = "https://ca.indeed.com/"
    next_page_href += pages[len(pages) - 1].get('href')
    '''
    if pagination != 0:
        num += 1
        print('Page' + str(num) + ' crawled！')
        # 3-60秒之间随机暂停
        time.sleep(random.randint(10, 20))
        search_index = url.find('start=')
        print('search index'+str(search_index))
        parse_pages(url[0:search_index+5]+str(iterate*10), num, iterate)
    else:
        print('All pages have been crawled！')


def saveHtml(file_name, file_content):
    #    注意windows文件命名的禁用符，比如 /
    with open(file_name.replace('/', '_') + ".html", "wb") as f:
        #   写文件用bytes而不是str，所以要转码
        f.write(file_content)



def getHtml(url):
    html = request.urlopen(url).read()
    return html


if __name__ == '__main__':
    with open('indeed.csv', 'a', newline='', encoding='utf-8-sig') as fp:
        writer = csv.writer(fp)
    start_num = 0
    start_url = 'https://ca.indeed.com/jobs?q=Java&l=Ottawa%2C+ON&radius=100&start=10'
    parse_pages(start_url, start_num, 0)



