'''
Author: yuan
Date: 2021-04-15 04:08:41
LastEditTime: 2021-04-17 15:58:28
FilePath: /line-chatbot/task.py
'''

from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod
import requests
import time
import logging
from collections import namedtuple



class Crawler(metaclass=ABCMeta):

    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    over_18 = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        'cookie': 'over18=1'
    }
    rs = requests.session()

    def __init__(self, target_url, method='get'):
        self.url = target_url
        self.soup = self.analyze(method)

    def analyze(self, method):
        if method == 'get':
            res = Crawler.rs.get(self.url, verify=False,
                                 headers=Crawler.headers)
        else:  # post

            res = Crawler.rs.get(self.url, verify=False,
                                 headers=Crawler.over_18)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        return soup

    @abstractmethod
    def parser(self):
        pass


class Ptt(Crawler):
    ArticleInfo = namedtuple('ArticleInfo', ['title', 'url', 'rate'])

    parser_page = 2
    item_number = 15
    @staticmethod
    def crawler_info(res):
        soup = BeautifulSoup(res.text, 'html.parser')
        articles = []

        for r_ent in soup.find_all('div', class_='r-ent'):
            try:
                link = r_ent.find('a')['href']
                if link:
                    title = r_ent.find(class_='title').text.strip()
                    rate = r_ent.find(class_='nrec').text
                    url = 'https://www.ptt.cc' + link
                    print(title, rate)
                    if rate:
                        rate = 100 if rate.startswith('爆') else rate
                        rate = -1 * \
                            int(rate[1]) if rate.startswith('X') else rate
                    else:
                        rate = 0
                    articles.append(Ptt.ArticleInfo(title, url, rate))
            except Exception as e:
                print('本文已被刪除', e)
        return articles

    @staticmethod
    def get_all_index(soup, url, parser_page):
        last_page = soup.select('.btn.wide')[1]['href']  # 上一頁

        print(f"last_page:{last_page}\n")
        max_page = Ptt.get_max_Page(last_page)
        return (
            url.format(page)
            for page in range(max_page - parser_page + 1, max_page + 1, 1)
        )

    @staticmethod
    def get_max_Page(soup):
        start_index = soup.find('index')
        end_index = soup.find('.html')
        page_number = soup[start_index + 5: end_index]
        print(f'page_number: {page_number}')
        return int(page_number) + 1

    # def parser(self):
    #     print(f"url:\t{self.url}, parser_page:\t:{self.parser_page}")
    #     # url = self.url
    #     index_seqs = Ptt.get_all_index(
    #         self.soup, self.url, self.parser_page)  # iterator
    #     articles = []
    #     for page in index_seqs:
    #         print(f"page:\t{page}")
    #         try:
    #             res = Crawler.rs.get(page, verify=False,
    #                                  headers=Crawler.headers)
    #             res.raise_for_status()
    #         except requests.exceptions.ConnectionError:
    #             logging.error('Connection error')
    #         else:
    #             articles += Ptt.crawler_info(res)
    #         time.sleep(0.05)
    #     result = ''
    #     for index, article in enumerate(reversed(articles)):
    #         if index == Ptt.item_number:
    #             break
    #         result += f"[{article.rate} push] {article.title}\n{article.url}\n\n"

    #     return result


class News(Crawler):
    target_url = 'https://news.tvbs.com.tw/realtime'

    def __init__(self):
        super().__init__(News.target_url)

    def parser(self):
        content = ''
        for index, data in enumerate(self.soup.select('article div.list li')):
            if index == 12:
                break
            detail = data.find('h2', class_='txt')
            if detail:
                content += '{}\n{}\n\n'.format(
                    detail.text,
                    'https://news.tvbs.com.tw/' + data.find('a')['href'])

        return content


class PttBeauty(Crawler):
    # parser_page = 2  # crawler count
    # push_rate = 10  # 推文
    target_url = 'https://www.ptt.cc/bbs/Beauty/index.html'
    url = 'https://www.ptt.cc/bbs/Beauty/index{}.html'

    def __init__(self):
        super().__init__(PttBeauty.target_url, 'post')

    def parser(self):
        index_seqs = Ptt.get_all_index(
            self.soup, url, PttBeauty.parser_page)
        articles = []
        for page in index_seqs:
            try:
                res = Crawler.rs.get(page, verify=False, headers=Crawler.over_18)
                res.raise_for_status()
            except requests.exceptions.ConnectionError:
                logging.error('Connection error')
            else:
                articles += Ptt.crawler_info(res)
            time.sleep(0.05)

        result = ''
        for index, article in enumerate(reversed(articles)):
            if index == 15:
                break
            result += f"[{article.rate} push] {article.title}\n{article.url}\n\n"

        return result


class PttGossiping(Crawler):
    target_url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
    parser_page = 5  # crawler count
    url = 'https://www.ptt.cc/bbs/Gossiping/index{}.html'

    def __init__(self):
        super().__init__(PttGossiping.target_url, 'post')

    def parser(self):
        
        index_seqs = Ptt.get_all_index(
            self.soup, url, PttGossiping.parser_page)
        articles = []
        for page in index_seqs:
            try:
                res = Crawler.rs.get(page, verify=False, headers=Crawler.over_18)
                res.raise_for_status()
            except requests.exceptions.ConnectionError:
                logging.error('Connection error')
            else:
                articles += Ptt.crawler_info(res)
            time.sleep(0.05)

        result = ''
        for index, article in enumerate(reversed(articles)):
            if index == 15:
                break
            result += f"[{article.rate} push] {article.title}\n{article.url}\n\n"

        return result


class PttSoftJob(Crawler):
    target_url = 'https://www.ptt.cc/bbs/Soft_Job/index.html'
    parser_page = 3  # crawler count
    url = 'https://www.ptt.cc/bbs/Soft_Job/index{}.html'
        
    def __init__(self):
        super().__init__(PttSoftJob.target_url)

    def parser(self):
        index_seqs = Ptt.get_all_index(
            self.soup, url, PttTechJob.parser_page)  # iterator
        articles = []
        for page in index_seqs:
            print(page)
            try:
                res = Crawler.rs.get(page, verify=False,
                                     headers=Crawler.headers)
                res.raise_for_status()
            except requests.exceptions.ConnectionError:
                logging.error('Connection error')
            else:
                articles += Ptt.crawler_info(res)
            time.sleep(0.05)
        result = ''
        for index, article in enumerate(reversed(articles)):
            if index == 15:
                break
            result += '[{} push] {}\n{}\n\n'.format(
                article.rate, article.title, article.url)

        return result


class PttTechJob(Ptt):
    target_url = 'https://www.ptt.cc/bbs/Tech_Job/index.html'
    parser_page = 3  # crawler count
    # push_rate = 10
    url = 'https://www.ptt.cc/bbs/Tech_Job/index{}.html'
        
    def __init__(self):
        super().__init__(PttTechJob.target_url)

    def parser(Crawler):
        
        index_seqs = Ptt.get_all_index(
            self.soup, url, PttTechJob.parser_page)  # iterator
        articles = []
        for page in index_seqs:
            try:
                res = Crawler.rs.get(page, verify=False,
                                     headers=Crawler.headers)
                res.raise_for_status()
            except requests.exceptions.ConnectionError:
                logging.error('Connection error')
            else:
                articles += Ptt.crawler_info(res)
            time.sleep(0.05)
        result = ''
        for index, article in enumerate(reversed(articles)):
            if index == 15:
                break
            result += '[{} push] {}\n{}\n\n'.format(
                article.rate, article.title, article.url)

        return result


class Movie(Crawler):

    target_url = 'https://movies.yahoo.com.tw/'

    def __init__(self):
        super().__init__(Movie.target_url)

    def parser(self):
        content = ''
        for index, data in enumerate(self.soup.select('div.movielist_info_inner')):
            if index == 5:
                return content
            details = data.findChild('h2').findChild('a')
            title = details['data-ga'].split(',')[-1].replace("]", "")
            link = details['href']
            content += '{}\n{}\n'.format(title.replace("'", ""), link)
        return content


class Netflix(Crawler):
    target_url = 'https://www.netflix.com/tw/browse/genre/839338'

    def __init__(self):
        super().__init__(Netflix.target_url)

    def parser(self):
        content = ''
        sections = '.nm-collections-row'
        movie_list = []
        try:
            for data in self.soup.select(sections):
                genre = data.find('h2', class_='nm-collections-row-name').text
                if genre == '最新發行':
                    print(genre)
                    # movies = data.find('div', class_='nm-content-horizontal-row')
                    for m in data.find_all('li', class_='nm-content-horizontal-row-item'):
                        # a_movie = m.find('li', class_='nm-content-horizontal-row-item')
                        if m:
                            a_movie = m.find(
                                'a', class_='nm-collections-title nm-collections-link')
                            if a_movie:
                                a_movie_title = a_movie.find(
                                    'span', class_='nm-collections-title-name').text
                                if a_movie_title:
                                    a_url = a_movie['href']
                                    movie_list.append({
                                        'genre': genre,
                                        'name': a_movie_title,
                                        'url': a_url
                                    })
                                    content += f'{a_movie_title}\n{a_url}\n'
                                if len(movie_list) >= 10:
                                    break
                else:
                    print(f'{genre} is pass')

        except Exception as e:
            print('---------------------------------------')
            print(e)
        finally:
            print(movie_list)
            gere = {}
            for mv in movie_list:
                if mv['genre'] not in gere:
                    gere[mv['genre']] = 1
                else:
                    gere[mv['genre']] += 1
            print(gere)

            return content


class Technews(Crawler):
    target_url = 'https://technews.tw/'

    def __init__(self):
        super().__init__(Technews.target_url)

    def parser(self):
        content = ''
        for index, data in enumerate(self.soup.select('article div h1.entry-title a')):
            if index == 12:
                break
            content += '{}\n{}\n\n'.format(data.text, data['href'])
        return content


class OilPrice(Crawler):
    # target_url = 'https://gas.goodlife.tw/'
    target_url = 'https://toolbxs.com/zh-TW/detector/gasoline_price'

    def __init__(self):
        super().__init__(OilPrice.target_url)

    def parser(self):
        content = ''
        data = self.soup.find('div', class_='col-lg-8 order-1 order-sm-2')
        # parser oil price prediction
        title = data.findChild('h1').text
        prediction = data.findChild('p', class_='prediction').text

        # parser oil prices 92/95/98 ....
        prices = data.findChild(
            'div', class_='price_table current_week_price_table').find('table')

        for d in prices.find_all('thead'):
            content += f'{d.text}'
            content += f'\n'
        for d in prices.find('tbody'):
            content += f'{d.text}'
            content += f'\n'
        content += f'\n'
        # content += f'{prices}'
        content += f'{title} {prediction}'
        return content


class Rate(Crawler):

    target_url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'

    info = namedtuple('info',
                      ['currency', 'cash_buy', 'cash_sell', 'sight_buy', 'sight_sell'])

    def __init__(self):
        super().__init__(Rate.target_url)

    def parser(self):
        content = ''
        head = self.soup.select('div.container thead')

        for tr in self.soup.select('div.container tbody tr'):
            ret = []
            cur = tr.find('div', class_='hidden-phone print_show').text.strip()
            cur_buy = tr.find_all(
                'td', class_='rate-content-cash text-right print_hide')
            ret.append(cur)
            for c in cur_buy:
                ret.append(c['data-table'])
                ret.append(c.text.strip())
            sight = tr.find_all(
                'td', class_='rate-content-sight text-right print_hide')
            for s in sight:
                ret.append(s['data-table'])
                ret.append(s.text.strip())
            c = ' '.join(r for r in ret)
            content += ''.join(f'{c}\n\n')
        return content


class Beverage():
    menu = {
        'coco菜單': 'https://cdn.changing.ai/3685e330ec5277a9dd5661c61f2bc55811f5a628/1610091221313-a457d8-63-6d0-cdf3-a6602148f252',  # coco menu
        '50嵐菜單': 'https://icard.ai/_next/image?url=https://cdn.changing.ai/3685e330ec5277a9dd5661c61f2bc55811f5a628/1603163827149-c8d51a7-bbdd-bb33-f4b7-64225037cb7a&w=1200&q=75',  # 50


        '白巷子菜單': 'https://cdn.walkerland.com.tw/images/upload/poi/p100452/m61096/3a710164218c896c4f85341d7bd945e1e4a452ea.jpg',  # 白巷子
        '迷客夏菜單': 'https://www.milkshoptea.com/upload/price/2104090829390000002.jpg',  # 迷客夏

        # COMEBUY
        'COMEBUY菜單': 'http://www.comebuy2002.com.tw/upload/%E5%A4%A7%E9%BA%A52020DM(%E4%B8%80%E8%88%AC)-21x14_85cm-02.jpg',
        '清心菜單': 'https://www.chingshin.tw/upload/price/1907171531260000001.jpg',  # 清心

        '麻古菜單': 'https://twcoupon.com/images/menu/p_maculife_n.jpg',  # 麻古
        '鮮茶道菜單': 'https://twcoupon.com/images/menu/p_presotea.jpg',  # 鮮茶道
        '大苑子菜單': 'https://twcoupon.com/images/menu/p_dayungstea_n.jpg',  # 大苑子
    }

    def parser(self, b):
        return self.menu.get(b, '暫無菜單')
