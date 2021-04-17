'''
Author: yuan
Date: 2021-04-14 03:24:59
LastEditTime: 2021-04-17 01:23:11
FilePath: /line-chatbot/my_dict.py
'''


class MyDict:
    news = '即時新聞'

    ptt_beauty = 'PTT表特版'
    ptt_soft_job = '軟體'
    ptt_tech_job = '工作'
    gossiping = '即時廢文'

    movie = '近期上映電影'
    netflix = 'Netflix近期上映'

    technews = '科技快報'

    oil_price = '油價查詢'

    rate = '匯率查詢'

    beverage = '飲料菜單'

    @classmethod
    def show_attribute(cls):
        return [
            cls.news, cls.ptt_beauty,
            cls.ptt_soft_job, cls.ptt_tech_job,
            cls.gossiping, cls.movie,
            cls.netflix, cls.technews,
            cls.oil_price, cls.rate,
            cls.beverage]
