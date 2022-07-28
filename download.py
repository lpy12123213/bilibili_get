# from open1 import*
import time
import requests
import subprocess
import os
import pyperclip
import re
# 变量提前定义
path = os.getcwd()
os.chdir(path)
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44',
    'cookie': '_uuid=58E9F87D-9DF9-86910-D972-6102E4810EE72166149infoc; buvid3=C7D600BB-47C0-BCC4-9065-E11C902B271566461infoc; b_nut=1649515067; buvid4=FFAC8272-235A-96BD-D6EE-551C4D84EF7166461-022040922-+hGGnoawvNgIhx/+uEHLiElOrSLpLtIWWxgdx51sLIVZ4T78x4hr4w%3D%3D; nostalgia_conf=-1; CURRENT_BLACKGAP=0; buvid_fp_plain=undefined; blackside_state=0; rpdid=0zbfVGhipD|k9P7lIuA|1x1|3w1NDmsy; LIVE_BUVID=AUTO7716495683704445; fingerprint3=d4e5aed0143b24edfba50fc3ac142151; i-wanna-go-back=-1; CURRENT_QUALITY=80; fingerprint=c4e14d52aaa2f1a564f71c6b2d3d6c2d; SESSDATA=5afffe4d%2C1666185978%2C3c686%2A41; bili_jct=994a343f0f648982846ecb9ae5fd75a5; DedeUserID=450158456; DedeUserID__ckMd5=f1b89c51453a6646; sid=johfkykh; b_ut=5; buvid_fp=c4e14d52aaa2f1a564f71c6b2d3d6c2d; b_lsid=710E4C6F5_18051759290; bsource=search_bing; bp_video_offset_450158456=651968725507899400; PVID=1; innersign=0; CURRENT_FNVAL=80',
}
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
            for i in json_response['data']:
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
        response = session.get(_url, params=_params, headers=headers)
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
        json = get_video_info(bv, headers)
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
        url = json['data']['dash']['video'][0]['baseUrl']
        title = get_video_title_or_desc(bv, headers=headers)['title']
        a = download(url, bv, page, name=title)
        url=json['data']['dash']['audio'][0]['baseUrl']
        b=download_music(
            url, bv, page, name=title)
    except:
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
# download_video('BV1TE411h7vY', headers=header)
