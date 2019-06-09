# -*- coding: utf-8 -*-
import time
import requests
import datetime
import pandas as pd
from fake_useragent import UserAgent


"""
分析思路：
    在芒果TV网页版打开第7期节目，等待广告加载完毕，同时打开chrome开发者工具的network选项卡。由于请求很多，
    而且随着时间推移，会越来越多。所以我采取了先清空再等待的方式。发现前面大多加载的都是图片，自然这不是我们的目标。
    过了一会儿之后，发现一条可疑的请求，点击一看，真的出现了弹幕内容。interval是60，猜测可能是表示一个间隔，每60s会有一个新的请求。
    于是使用filter过滤了以“rdb”开头的请求，发现这些都是弹幕，而且next都是60000的倍数，猜测表示的是60000毫秒，也就是60秒。
"""


def get_data():
    ua = UserAgent()
    url = "https://galaxy.bz.mgtv.com/rdbarrage"
    content = {'id': [], 'type': [], 'uid': [], 'content': [], 'add_time': [], 'ups': []}
    count = 0
    print("爬取开始时间：{0}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    for i in range(0, 91):
        querystring = {"version": "2.0.0", "vid": "5767813", "cid": "328724", "time": i * 60000}
        headers = {
            'User-Agent': ua.random
        }
        try:
            response = requests.request("GET", url, headers=headers, params=querystring).json()
            items = response['data']['items']
            if items is None:
                print("爬取完毕！弹幕数量{0}".format(count))
                break
            else:
                for item in items:
                    # 弹幕id
                    content['id'].append(item.get('id'))
                    # 弹幕类型
                    content['type'].append(item.get('type'))
                    # 用户id
                    content['uid'].append(item.get('uid'))
                    # 弹幕内容
                    content['content'].append(item.get('content'))
                    # 弹幕时间
                    content['add_time'].append(item.get('time'))
                    # 弹幕点赞数
                    content['ups'].append(item.get('up', 0))
                    count = count + 1

                    print("爬取第{0}分钟的弹幕...，当前弹幕数量{1}".format(i + 1, count))
                time.sleep(5)
        except:
            print("第{}分钟弹幕爬取失败!当前弹幕数量{}".format(i + 1, count))
            continue

        rdb_df = pd.DataFrame(content)
        # 内容里包含中文，encoding='utf_8_sig'
        rdb_df.to_csv('barrage_content.csv', index=None, encoding='utf_8_sig')


if __name__ == '__main__':
    get_data()

