'''
Author: yuan
Date: 2021-04-14 05:53:15
LastEditTime: 2021-04-17 15:50:43
FilePath: /line-chatbot/interface.py
'''

from linebot.models import (
    ImageSendMessage,
    TextSendMessage,
    TemplateSendMessage,
    MessageTemplateAction,
    ButtonsTemplate,
    CarouselColumn,
    MessageAction,


)
from my_dict import MyDict

from config import Config
from serve import (Beverage, Gossiping, Movie, Netflix, News, OilPrice,
                   PttBeauty, PttSoftJob, PttTechJob, Rate, Technews)

# from serve import


config = Config()
line_bot_api = config.line_bot_api


class Factory:
    def __init__(self, func=None, event=None):
        self.name = func.__name__
        self.event = event

    def reply_message(self, obj):
        line_bot_api.reply_message(self.event.reply_token, obj)


class Template_Factory:
    def __init__(self, func=None, event=None):
        self.name = func.__name__
        self.event = event

    def reply_message(self, obj):
        line_bot_api.reply_message(self.event.reply_token, obj)


# def start_template(self):
#     buttons_template = TemplateSendMessage(
#         alt_text='開始玩 template',
#         template=ButtonsTemplate(
#             title='選擇服務',
#             text='請選擇',
#             thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
#             actions=[
#                 MessageTemplateAction(
#                     label=MyDict.news_template,
#                     text=MyDict.news_template
#                 ),
#                 MessageTemplateAction(
#                     label=MyDict.movie_template,
#                     text=MyDict.movie_template
#                 ),
#                 MessageTemplateAction(
#                     label=MyDict.ptt_template,
#                     text=MyDict.ptt_template
#                 ),
#                 MessageTemplateAction(
#                     label=MyDict.beauty_template,
#                     text=MyDict.beauty_template
#                 )
#             ]
#         )
#     )
#     self.reply_message(buttons_template)


def tvbs_news(self):
    task = News()
    self.reply_message(TextSendMessage(text=task.parser()))


def ptt_beauty(self):
    task = PttBeauty()  # over 18
    self.reply_message(TextSendMessage(text=task.parser()))


def gossiping(self):
    task = Gossiping()  # over 18
    self.reply_message(TextSendMessage(text=task.parser()))


def ptt_soft_job(self):
    task = PttSoftJob()
    self.reply_message(TextSendMessage(text=task.parser()))


def ptt_tech_job(self):
    task = PttTechJob()
    self.reply_message(TextSendMessage(text=task.parser()))


def movie(self):
    task = Movie()
    self.reply_message(TextSendMessage(task.parser()))


def netflix(self):  # optimize
    task = Netflix()
    self.reply_message(TextSendMessage(task.parser()))


def tech_news(self):
    task = Technews()
    self.reply_message(TextSendMessage(task.parser()))


def oil_price(self):
    task = OilPrice()
    self.reply_message(TextSendMessage(task.parser()))


def rate(self):  # not finish
    task = Rate()
    self.reply_message(TextSendMessage(task.parser()))


# def beverage(self):  # reply menu image and beverage price
#     task = Beverage()
#     url = task.parser(self.event.message.text)
#     self.reply_message(ImageSendMessage(
#         original_content_url=url, preview_image_url=_url))


def beverage_50lan(self):
    task = Beverage()
    url = task.parser(self.event.message.text)
    self.reply_message(ImageSendMessage(
        original_content_url=url, preview_image_url=url))


def beverage_coco(self):
    task = Beverage()
    url = task.parser(self.event.message.text)
    self.reply_message(ImageSendMessage(
        original_content_url=url, preview_image_url=url))


def beverage_whitealley(self):
    task = Beverage()
    url = task.parser(self.event.message.text)
    self.reply_message(ImageSendMessage(
        original_content_url=url, preview_image_url=url))


def beverage_milkshop(self):
    task = Beverage()
    url = task.parser(self.event.message.text)
    self.reply_message(ImageSendMessage(
        original_content_url=url, preview_image_url=url))


def beverage_chingshin(self):
    task = Beverage()
    url = task.parser(self.event.message.text)
    self.reply_message(ImageSendMessage(
        original_content_url=url, preview_image_url=url))


def beverage_maculife(self):
    task = Beverage()
    url = task.parser(self.event.message.text)
    self.reply_message(ImageSendMessage(
        original_content_url=url, preview_image_url=url))


def beverage_presotea(self):
    task = Beverage()
    url = task.parser(self.event.message.text)
    self.reply_message(ImageSendMessage(
        original_content_url=url, preview_image_url=url))


def beverage_dayungs(self):
    task = Beverage()
    url = task.parser(self.event.message.text)
    self.reply_message(ImageSendMessage(
        original_content_url=url, preview_image_url=url))


def start_template(self):
    buttons_template = TemplateSendMessage(
        alt_text='開始玩 template',
        template=ButtonsTemplate(
            title='選擇服務',
            text='另外提供油價查詢 匯率查詢',
            thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
            actions=[
                MessageTemplateAction(
                    label=MyDict.news_template,
                    text=MyDict.news_template
                ),
                MessageTemplateAction(
                    label=MyDict.movie_template,
                    text=MyDict.movie_template
                ),
                MessageTemplateAction(
                    label=MyDict.ptt_template,
                    text=MyDict.ptt_template
                ),
                MessageTemplateAction(
                    label=MyDict.beverage_template,
                    text=MyDict.beverage_template
                )
            ]
        )
    )
    self.reply_message(buttons_template)


def ptt_template(self):
    buttons_template = TemplateSendMessage(
        alt_text='看廢文 template',
        template=ButtonsTemplate(
            title='你媽知道你在看廢文嗎',
            text='請選擇',
            # thumbnail_image_url='https://i.imgur.com/ocmxAdS.jpg',
            actions=[
                MessageTemplateAction(
                    label=MyDict.ptt_beauty,
                    text=MyDict.ptt_beauty
                ),
                MessageTemplateAction(
                    label=MyDict.gossiping,
                    text=MyDict.gossiping
                ),
                MessageTemplateAction(
                    label=MyDict.ptt_soft_job,
                    text=MyDict.ptt_soft_job
                ),
                MessageTemplateAction(
                    label=MyDict.ptt_tech_job,
                    text=MyDict.ptt_tech_job
                )
            ]
        )
    )
    self.reply_message(buttons_template)


def news_template(self):
    buttons_template = TemplateSendMessage(
        alt_text='新聞 template',
        template=ButtonsTemplate(
            title='新聞類型',
            text='請選擇',
            thumbnail_image_url='https://i.imgur.com/vkqbLnz.png',
            actions=[
                MessageTemplateAction(
                    label=MyDict.tvbs_news,
                    text=MyDict.tvbs_news
                ),
                MessageTemplateAction(
                    label=MyDict.tech_news,
                    text=MyDict.tech_news
                )
            ]
        )
    )
    self.reply_message(buttons_template)


def movie_template(self):
    buttons_template = TemplateSendMessage(
        alt_text='電影 template',
        template=ButtonsTemplate(
            title='服務類型',
            text='請選擇',
            thumbnail_image_url='https://i.imgur.com/sbOTJt4.png',
            actions=[
                MessageTemplateAction(
                    label=MyDict.movie,
                    text=MyDict.movie
                ),
                MessageTemplateAction(
                    label=MyDict.netflix,
                    text=MyDict.netflix
                )
            ]
        )
    )
    self.reply_message(buttons_template)


def beverage_template(self):
    buttons_template = TemplateSendMessage(
        alt_text='飲料 template',
        template=ButtonsTemplate(  # Buttons template最多可以有4個Action項目
            title='哪一家菜單',
            text='請選擇',
            thumbnail_image_url='https://i.imgur.com/GZiqoVo.jpg',
            actions=[
                MessageTemplateAction(
                    label=MyDict.beverage_template1,
                    text=MyDict.beverage_template1
                ),
                MessageTemplateAction(
                    label=MyDict.beverage_template2,
                    text=MyDict.beverage_template2
                )
            ]
        )
    )
    self.reply_message(buttons_template)


def beverage_template1(self):
    buttons_template = TemplateSendMessage(
        alt_text='飲料 template',
        template=ButtonsTemplate(  # Buttons template最多可以有4個Action項目
            title='哪一家菜單',
            text='請選擇',
            thumbnail_image_url='https://i.imgur.com/GZiqoVo.jpg',
            actions=[
                MessageTemplateAction(
                    label=MyDict.beverage_50lan,
                    text=MyDict.beverage_50lan
                ),
                MessageTemplateAction(
                    label=MyDict.beverage_coco,
                    text=MyDict.beverage_coco
                ),
                MessageTemplateAction(
                    label=MyDict.beverage_whitealley,
                    text=MyDict.beverage_whitealley
                ),
                MessageTemplateAction(
                    label=MyDict.beverage_milkshop,
                    text=MyDict.beverage_milkshop
                )
            ]
        )
    )
    self.reply_message(buttons_template)


def beverage_template2(self):
    buttons_template = TemplateSendMessage(
        alt_text='飲料 template',
        template=ButtonsTemplate(  # Buttons template最多可以有4個Action項目
            title='哪一家菜單',
            text='請選擇',
            thumbnail_image_url='https://i.imgur.com/GZiqoVo.jpg',
            actions=[
                MessageTemplateAction(
                    label=MyDict.beverage_chingshin,
                    text=MyDict.beverage_chingshin
                ),
                MessageTemplateAction(
                    label=MyDict.beverage_maculife,
                    text=MyDict.beverage_maculife
                ),
                MessageTemplateAction(
                    label=MyDict.beverage_presotea,
                    text=MyDict.beverage_presotea
                ),
                MessageTemplateAction(
                    label=MyDict.beverage_dayungs,
                    text=MyDict.beverage_dayungs
                )
            ]
        )
    )
    self.reply_message(buttons_template)
