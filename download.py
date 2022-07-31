# from open1 import*
import json
import time
import requests
import subprocess
import os
import pyperclip
import re
# 变量提前定义
path = os.getcwd()
os.chdir(path)

# 变量提前定义
# header['cookie'] = get_cookie()\

qxd = {
    '240P': 6,
    '360P': 16,
    '480P': 32,
    '720P': 64,
    '720P60': 74,
    '1080P': 80,
    '1080P+': 112,
    '1080P60': 116,
    '4K': 120
}
setting = {}
setting['qxd'] = qxd["1080P"]
sess = requests.session()
'''
检测登录状态
https://api.bilibili.com/x/web-interface/nav
'''

class DownloadErr(Exception):
    def __init__(self, message):
        self.message = message
def get_bv_from_url(text):
    pattern = re.compile(r'https://www.bilibili.com/video/(.+)?\?.*')
    bv = re.findall(pattern, text)
    print(bv)
    return bv[0]
# get_bv_from_url('https://www.bilibili.com/video/BV1K5411S7UM?spm_id_from=333.851.b_7265636f6d6d656e64.6')


def get_user_info(headers):
    class LoginError(Exception):
        def __init__(self, message):
            self.message = message

    url = 'https://api.bilibili.com/x/web-interface/nav'
    session = sess
    response = session.get(url, headers=headers)
    response.encoding = 'utf-8'
    response.raise_for_status()
    resp = response.json()
    if not resp['data']['isLogin']:
        raise LoginError('isLogin is False')
    return resp


def get_cid(bv, headers):
    __url = "https://api.bilibili.com/x/web-interface/view"
    data = {
        'bvid': bv,
    }
    resp = requests.get(__url, headers=headers, params=data)
    resp.encoding = 'utf-8'
    resp.raise_for_status()
    json_response = resp.json()
    return_text = []
    # print(json_response)
    for i in json_response['data']['pages']:
        return_text.append(i['cid'])
    return return_text
def get_video_info(bv, headers):
    def get_cid():
        __url = "https://api.bilibili.com/x/web-interface/view"
        data = {
            'bvid': bv,
        }
        resp = requests.get(__url, headers=headers, params=data)
        resp.encoding = 'utf-8'
        resp.raise_for_status()
        json_response = resp.json()
        return_text = []
        # print(json_response)
        try:
            for i in json_response['data']['pages']:
                return_text.append(i['cid'])
        except:
            return_text.append(json_response['data']['cid'])
        return return_text

    cidlist = get_cid()
    if len(cidlist) == 1:
        cid = cidlist[0]
        _url = 'http://api.bilibili.com/x/player/playurl'
        _params = {
            'bvid': bv,
            'cid': cid,
            'fnval': '16',
        }
        session = sess
        try:
            response = session.get(_url, params=_params, headers=headers)
        except requests.exceptions.ConnectionError as ce:
            raise DownloadErr(f"错误：{ce}")
        response.encoding = 'utf-8'
        response.raise_for_status()
        resp = response.json()
        return resp
    else:
        cid1 = cidlist
        retlist = []
        for cid in cid1:
            _url = 'http://api.bilibili.com/x/player/playurl'
            _params = {
                'bvid': bv,
                'cid': cid,
                'fnval': '16',
            }
            session = sess
            response = session.get(_url, params=_params, headers=headers)
            response.encoding = 'utf-8'
            response.raise_for_status()
            resp = response.json()
            retlist.append(resp)
        return retlist


def get_video_title_or_desc(bv, headers):
    url = 'https://api.bilibili.com/x/web-interface/view'
    data = {
        'bvid': bv,
    }
    resp = requests.get(url, headers=headers, params=data)
    resp.encoding = 'utf-8'
    resp.raise_for_status()
    json_response = resp.json()
    return {'title': json_response['data']['title'], 'desc': json_response['data']['desc']}


def download(json, bv, page=1, name=None):
    if name is None:
        name = bv
    ds = fr"""{path}\bin\aria2c -s 16 --dir=.\temp\ -D -o "{name}.m4s" "{json}" --referer=https://www.bilibili.com/video/{bv}?p={page}"""
    subprocess.call(ds)
    return {'filename': name+'.m4s', 'name': name}


def download_music(json, bv, page=1, name=None):
    if name is None:
        name = bv
    ds = fr"""{path}\bin\aria2c -s 16 --dir=.\temp\ -D -o "{name}.mp3" "{json}" --referer=https://www.bilibili.com/video/{bv}?p={page}"""
    subprocess.call(ds)
    return {'filename': name+'.mp3', 'name': name}


def clean(filename):
    subprocess.call(f"del {path}\\temp\\{filename}", shell=True)


def download_video(bv, headers, page=1):
    try:
        json1 = get_video_info(bv, headers)
    except KeyError:
        return 1
    a = ''
    list1 = []
    # try:
    #     for i in range(1, page):
    #         list1.append(download(json[i], bv, i))
    # except:
    #     a = download(json, bv, page)
    try:
        if type(json1) == type([1, 2, 3]):
            url = json1[0]['data']['dash']['video'][0]['baseUrl']
            title = get_video_title_or_desc(bv, headers=headers)['title']
            a = download(url, bv, page, name=title)
            url=json1[0]['data']['dash']['audio'][0]['baseUrl']
            b=download_music(
                url, bv, page, name=title)
        else:
            url = json1['data']['dash']['video'][0]['baseUrl']
            title = get_video_title_or_desc(bv, headers=headers)['title']
            a = download(url, bv, page, name=title)
            url = json1['data']['dash']['audio'][0]['baseUrl']
            b = download_music(
                url, bv, page, name=title)
    except:
        with open('test.json', 'w') as f:
            json.dump(json1, f)
        return 1
    # 调用ffmpeg
    # 输入命令像这样: ffmpeg -y -i  D:\\ffmpeg_test\\1.webm  -r 30  D:\\ffmpeg_test\\1.mp4
    # 这里就是将1.webm的视频转成每秒30帧的视频1.mp4。这里指定1.mp4的绝对路径，如果不指定的话则生成的视频文件会落到当前ffmpeg命令的执行目录下。
    # 以上语句来自https://cloud.tencent.com/developer/article/1877108
    process = subprocess.call(
        f"{path}\\bin\\ffmpeg -i \"{path}\\temp\\{a['filename']}\" -i \"{path}\\temp\\{b['filename']}\" -c:v copy -c:a aac -strict experimental \"{path}\\video\\{a['name']}.mp4\"", shell=True)
    # 删除临时文件
    clean(a['filename'])
    clean(b['filename'])
    return process


def kill():
    subprocess.call(f"taskkill /F /PID aria2c.exe")
    subprocess.call(f"taskkill /F /PID ffmpeg.exe")


# test
# download_video('BV1Gf4y1o7jY', headers=header)
