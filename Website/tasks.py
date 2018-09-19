import json
from pprint import pprint
from time import time

import asks
import moment
import requests
import trio
from pyquery import PyQuery as jq

from Common.CompanyWeChat import WechatReports
from Common.Config import WechatConf
from Website.models import EarthquakeCase
from django.db import IntegrityError

asks.init('trio')
MaxNum = 1
Session = asks.Session() #初始化访问类
Session.headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Host": "www.ceic.ac.cn",
    "Pragma": "no-cache",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://news.ceic.ac.cn/index.html",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
} # 定义访问类header
uri = "http://127.0.0.1:1087" #代理接口
Session.proxes = {
    "https":uri,
    "http":uri
} # 定义访问类代理
WECHATBOT = WechatReports(WechatConf) # 初始化公众号机器人


async def item(Page, send=False):
    """新数据截取

        Args:
            Page: 页数
            send: 是否发送
    
    """
    global MaxNum
    Key = "jQuery"
    URL = f"http://www.ceic.ac.cn/ajax/speedsearch?num=6&&page={Page}&&callback={Key}&_={int(time())}"
    try:
        resp = await Session.get(URL)
        jsondata = json.loads(resp.text.replace(f'{Key}(', '')[:-1])
        save(jsondata['shuju'], send)
        MaxNum = jsondata['num']
    except Exception as e:
        await Session.get(f"http://zblank.com/?key=EarthquakeCase-SendERROR: {str(e)} {type(e)}")

def save(datas, send=False):
    """数据留存并根据可否成功存储发送推送信息

        Args:
            datas: 数据集
            send: 是否发送
    """
    for data in datas:
        res = dict(zip(["Level", "Time",  "Latitede", "Longitude", "Deep",
                        "Adress"], [data[key] for key in ['M', 'O_TIME', 'EPI_LAT', 'EPI_LON', 'EPI_DEPTH', 'LOCATION_C']]))
        try:
            EarthquakeCase.objects.create(**res)
            if send:
                Location = f"{res.get('Latitede','')},{res.get('Longitude','')}"
                WECHATBOT.Data_send(MsgType="textcard", Content={
                    "title": f"{res.get('Adress','')}", "description": f"""<div class="gray">{res.get('Time',moment.now())}</div><br/><div class="info">Level:  {res.get('Level')}</div><br/><div class="info">Deep:  {res.get('Deep','')}km</div><br/><br/><div class="highlight">Location:  {Location}</div>""", "url": f"https://www.google.com/maps/search/{Location}"}, SendNow=True, AppId="1000004")
        except IntegrityError:
            pass
        except Exception:
            raise


async def init():
    """初始化运行
        
    """
    async with trio.open_nursery() as nursery:
        nursery.start_soon(item,  MaxNum)

    async with trio.open_nursery() as nursery:
        for page in range(1, MaxNum+1):
            nursery.start_soon(item,  page)


async def update():
    """更新数据方法

    """
    await Session.get("http://zblank.com/?key=EarthquakeCaseupdate")
    async with trio.open_nursery() as nursery:
        nursery.start_soon(item,  1, True)


def getUpdateData():
    """定时更新

    """
    trio.run(update)


def getBaseData():
    """初始化
    
    """
    trio.run(init)


# getBaseData()
