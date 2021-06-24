import json
import random
import re
import time
import requests
import werobot
from lxml import etree
from werobot.replies import ArticlesReply, Article, ImageReply, TextReply, MusicReply

robot = werobot.WeRoBot(token='******')


# 订阅后的回复
@robot.subscribe
def subscribe():
    return "***欢迎关注KanoChyan[愉快][愉快][愉快]***\n" \
           "-->输入任意内容开始与我聊天！\n" \
           "-->输入'博客'关注我的博客！\n" \
           "-->输入'音乐'为小主送上舒缓的歌曲！\n" \
           "-->输入'天气'告诉你最近的天气情况！\n" \
           "-->输入'图片'来随机一张二次元图吧！\n" \
           "-->输入'笑话'或'段子'给你讲一段笑话！\n" \
           "-->输入'邀请'邀请你的好朋友来关注我吧！\n" \
           "-->输入'帮助'或'？'可再次显示此信息\n"


# 关键字 博客 回复
@robot.filter('二维码', '邀请', 'yq', 'qrcode', 'invite')
def invite(message):
    reply = ArticlesReply(message=message)
    article = Article(
        title="邀请方式",
        description="邀请链接及二维码",
        img="https://cdn.jsdelivr.net/gh/MissingLilith/Image-Hosting-Service/qrcode_for_gh_c5bba9b1cd24_344.jpg",
        url="https://cdn.jsdelivr.net/gh/MissingLilith/Image-Hosting-Service/qrcode_for_gh_c5bba9b1cd24_344.jpg"
    )
    reply.add_article(article)
    return reply


# 获取邀请链接
@robot.filter('博客', 'blog')
def blog(message):
    reply = ArticlesReply(message=message)
    article = Article(
        title="ねこちゃんの小站",
        description="ねこちゃんの个人博客",
        img="https://cdn.jsdelivr.net/gh/MissingLilith/Image-Hosting-Service/qrcode_missinglilith.github.io.png",
        url="https://missinglilith.github.io/"
    )
    reply.add_article(article)
    return reply


# 用户发送图片
@robot.image
def blog(message, session):
    # print("msg", message.img)
    # print(type(message))
    # print(type(message.img))
    # print(message.__dict__)
    print("\n" + message.MediaId)
    changdu = str(len(session))
    session[changdu] = message.MediaId
    reply = ImageReply(message=message, media_id=message.MediaId)
    return reply


# 随机一首音乐
def music_data():
    music_list = [
        ['童话镇', '陈一发儿', 'https://e.coka.la/wlae62.mp3', 'https://e.coka.la/wlae62.mp3'],
        ['都选C', '缝纫机乐队', 'https://files.catbox.moe/duefwe.mp3', 'https://files.catbox.moe/duefwe.mp3'],
        ['精彩才刚刚开始', '易烊千玺', 'https://e.coka.la/PdqQMY.mp3', 'https://e.coka.la/PdqQMY.mp3']
    ]
    num = random.randint(0, 2)
    return music_list[num]


# 匹配 音乐 回复一首歌
@robot.filter(re.compile(".*?音乐.*?"), re.compile(".*?歌曲.*?"), 'music')
def music(message):
    # reply = TextReply(message=message, content=music_data())
    # reply = MusicReply(message=message,source='https://www.kugou.com/song/#hash=D4EB517A405FCDF0286AA9A4487BBCE1&album_id=10409377')
    return music_data()
    # return reply


# 从目标网站爬取笑话
# 匹配 笑话 回复一个笑话
@robot.filter(re.compile(".*?笑话.*?"), re.compile(".*?段子.*?"), 'joke')
def get_joke():
    url = "http://www.qiushibaike.com/text/page/" + str(random.randint(1, 5))
    r = requests.get(url)
    tree = etree.HTML(r.text)
    contentlist = tree.xpath('//div[@class="content"]/span')
    jokes = []
    for content in contentlist:
        content = content.xpath('string(.)')  # string() 函数将所有子文本串联起来，# 必须传递单个节点，而不是节点集。
        if '查看全文' in content:  # 忽略包含“查看原文”笑话
            continue
        jokes.append(content)
    joke = jokes[random.randint(1, len(jokes))].strip()
    return "讲个段子：\n" + joke


# 匹配 天气 回复天气信息
@robot.filter(re.compile(".*?天气.*?"), 'weather')
def weather():
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=武汉'
    f = requests.get(url)
    # print(f.text)
    jsons = json.loads(f.text)
    # print(jsons['data']['forecast'])
    for i in jsons['data']['forecast']:
        return "武汉天气：\n" + i['date'] + "\n" + i['type'] + "\t" + i['fengxiang'] + "\n" + i['high'] + i['low']


@robot.filter(re.compile(".*?图片.*?"), 'pic', 'picture')
def picture(message):
    num = random.randint(1, 40)
    reply = ArticlesReply(message=message)
    article = Article(
        title="随机图片",
        description="KanoChyan的图库",
        img="https://cdn.jsdelivr.net/gh/MissingLilith/Image-Hosting-Service/wx/{}.png".format(num),
        url="https://cdn.jsdelivr.net/gh/MissingLilith/Image-Hosting-Service/wx/{}.png".format(num)
    )
    reply.add_article(article)
    return reply


@robot.filter(re.compile(".*?你好.*?"), 'Hi', 'hi', 'Hello', 'hello', '嗨')
def hello():
    return "你好！这里是KanoChyan！来和我玩吧~"


@robot.filter('bye', '再见', '拜拜')
def bye():
    return "再见！下次再来玩吧~"


@robot.filter('help', '?', '？', '帮助')
def help():
    return "***欢迎关注KanoChyan[愉快][愉快][愉快]***\n" \
           "-->输入任意内容开始与我聊天！\n" \
           "-->输入'博客'关注我的博客！\n" \
           "-->输入'音乐'为小主送上舒缓的歌曲！\n" \
           "-->输入'天气'告诉你最近的天气情况！\n" \
           "-->输入'图片'来随机一张二次元图吧！\n" \
           "-->输入'笑话'或'段子'给你讲一段笑话！\n" \
           "-->输入'邀请'邀请你的好朋友来关注我吧！\n" \
           "-->输入'帮助'或'？'可再次显示此信息\n"


# 文字智能回复
@robot.text
def replay(msg):
    # print(msg.content)
    # curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # response = get_response(msg.content)
    # print(
    #     curtime + '  公众号(机器人)' + ':' + response)
    # return response
    return msg.content[::-1]


# 让服务器监听在 0.0.0.0:80
robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
