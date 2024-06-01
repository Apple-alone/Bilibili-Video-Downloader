#如果有问题请联系我邮箱aotu013@163.com
#本程序不可用于非法活动

import json
import re
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED

import requests
from tqdm import tqdm

import os

print("Made by Apple-alone")
print("Apple-alone's email aotu013@163.com")
print("Follow My Github: https://github.com/Apple-alone")
print("不要多次使用本软件")
print("不能下载番剧（悲）")

desktop_path = os.path.expanduser("~/Desktop")
folder_name = "Bilibili Video"
folder_path = os.path.join(desktop_path, folder_name)

if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print("视频将保存在桌面上的Bilibili Video文件夹中")
else:
    print("已发现桌面已有Bilibili Video文件夹，不再创建该文件夹，并自动下载到该文件夹中")
BilibiliVideo = input("请输入哔哩哔哩视频链接：")
url = BilibiliVideo
def get_response(html_url,stream=False):
    headers = {
        "referer": "https://www.bilibili.com",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.get(html_url, headers=headers,stream=stream)
    return response

def get_url(html_url):
    r = get_response(html_url)
    a = re.search(r"window\.__INITIAL_STATE__=(.*?)};",r.text).group(1)
    json_data = json.loads(a + "}")
    video_data = json_data["videoData"]
    avid = str(video_data["aid"])
    qn = "112"
    urls = []


    for p in video_data["pages"]:
        cid = str(p["cid"])
        title = str(p["part"])
        if len(video_data["pages"]) == 1:
            title = str(video_data["title"])
        urls.append({
            "title": title,
            "url": "https://api.bilibili.com/x/player/playurl?cid=" + cid + "&avid=" + avid + "&an="
        })
    return urls

def save(video_url,video_size,title):
    video_res = get_response(video_url, True)
    print("（Made by Apple-alone）已获得视频下载链接"+video_url)
    with open(r"C:\\Users\Administrator\Desktop\Bilibili Video\\" + title + ".mp4","wb")as fd:
        for c in tqdm(iterable=video_res.iter_content(),total=video_size,unit="b",desc=None):
            fd.write(c)


def a_single_download(info):
    apple = get_response(info["url"])
    json_data = json.loads(apple.text)
    video_url = json_data["data"]["durl"][0]["url"]
    video_size = json_data["data"]["durl"][0]["size"]
    if "" in info["title"]:
        save(video_url,video_size,info["title"])

def concurrent_download(base_infos):
    executor = ThreadPoolExecutor(max_workers=10)
    futur_taske = [executor.submit(a_single_download, info) for info in base_infos]
    wait(futur_taske,return_when=ALL_COMPLETED)

if __name__ == "__main__":
    base_infos = get_url(url)
    concurrent_download(base_infos)