import requests
from lxml import etree
import pandas as pd


def get_article_url(url):
    r = requests.get(url=url)
    tree = etree.HTML(r.text)
    info_url = tree.xpath('//ul[@class="feed-list-area feed-normal-list-area"]/li/article/a/@href')
    return info_url


def get_article_img(url):
    r = requests.get(url=url)
    tree = etree.HTML(r.text)
    article_img = tree.xpath('//ul[@class="feed-list-area feed-normal-list-area"]/li/article/a/img/@original')
    return article_img


def clean_url(urls):
    article_url = []
    for u in urls:
        url = r'http://' + u[2:]
        article_url.append(url)
    return article_url


def get_tittle(article_url):
    res = requests.get(article_url)
    tree = etree.HTML(res.text)
    tittle = tree.xpath('//div[@class="text"]/div[@class="text-title"]/h1[1]/text()')
    article_tittle = ''.join(tittle).split()[0]
    return article_tittle


def get_news_time(article_url):
    res = requests.get(article_url)
    tree = etree.HTML(res.text)
    time = tree.xpath('//div[@class="text"]/div[@class="text-title"]/div[@class="article-info"]/span[@id="news-time"]/text()')[0]
    return time


def get_source(article_url):
    res = requests.get(article_url)
    tree = etree.HTML(res.text)
    source = tree.xpath('//div[@class="text"]/div[@class="text-title"]/div[@class="article-info"]/span[@data-role="original-link"]/a/text()')[0]
    return source


def get_text(article_url):
    article_text = ''
    res = requests.get(article_url)
    tree = etree.HTML(res.text)
    text = tree.xpath('//div[@class="text"]/article[@class="article"]/p[not(@class or @data-role)]/span|//div[@class="text"]/article[@class="article"]/p[not(@class or @data-role)]/strong')
    for t in text:
        text_info = t.xpath('string(.)').split()
        if text_info != []:
            ss = "".join(text_info)
            article_text += ss
            article_text += '\n\n'
    return article_text


def get_img(article_url):
    res = requests.get(article_url)
    tree = etree.HTML(res.text)
    img = tree.xpath('//div[@class="text"]/article[@class="article"]/p/img/@src')
    return img


def save_excel(data, data2):
    df = pd.DataFrame(data)
    df2 = pd.DataFrame(data2)
    writer = pd.ExcelWriter('test.xlsx')
    df.to_excel(writer, '政知道')
    df2.to_excel(writer, '红星深度')
    writer.save()


def get_news_data(url):
    li = []
    urls = get_article_url(url)
    article_urls = clean_url(urls)
    article_img = get_article_img(url)
    for article_url, src in zip(article_urls, article_img):
        dic = {}
        tittle = get_tittle(article_url)
        time = get_news_time(article_url)
        source = get_source(article_url)
        article_src = src
        text = get_text(article_url)
        img = get_img(article_url)
        dic = {'标题': tittle, '时间': time, '来源': source, '正文': text, '标题图片': article_src, '正文图片': img}
        li.append(dic)
    return li


def main():
    url = 'http://mp.sohu.com/profile?xpt=c29odXptdGY4YWgydGdAc29odS5jb20'
    url2 = 'http://mp.sohu.com/profile?xpt=NjEwNTcxMzc2MUBzaW5hLnNvaHUuY29t'
    data = get_news_data(url)
    data2 = get_news_data(url2)
    save_excel(data, data2)



if __name__ == '__main__':
   main()
