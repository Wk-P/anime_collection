import requests, json
from http.cookies import SimpleCookie
import datetime

# test
# url = "https://space.bilibili.com/44629592"
# url1 = "https://passport.bilibili.com/x/passport-login/web/cookie/info?csrf=13e45769eebcec84ab9feb62e419bb68"
# url2 = "https://api.bilibili.com/x/space/navnum?mid=44629592"
# url3 = "https://space.bilibili.com/44629592/bangumi"
# url4 = "https://api.bilibili.com/x/space/bangumi/follow/list?type=1&follow_status=0&pn=1&ps=15&vmid=44629592&ts=1692115454699"

# 追番数据请求地址
pn = 1
url5 = f"https://api.bilibili.com/x/space/bangumi/follow/list?type=1&follow_status=0&pn={pn}&ps=15&vmid=44629592" # pn 为页数 ps 为个数

# 读取本地cookies文件
cookies_file_path = "./spider/files/cookies_str.txt"
cookies_str = ""
with open(cookies_file_path, 'r') as f:
    cookies_str = f.read()

# Cookies 转换
cookies = SimpleCookie()
cookies.load(cookies_str)

cookies_dict = {cookie.key: cookie.value for cookie in cookies.values()}

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ko;q=0.5,ja;q=0.4",
    "Origin": "https://space.bilibili.com",
    "Referer": "https://space.bilibili.com/44629592",
    "Sec-Ch-Ua-Platform": "Windows",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Cookie": cookies_str

}

# 发送请求

# 获取总量
response_prev = requests.get(url=url5, headers=headers)
response_prev = response_prev.json()

if response_prev['message'] == "用户隐私设置未公开":
    print("请及时更换Cookies")
    exit(1)

pn_max = response_prev['data']['total'] / 15 + 1

img_file_path = "./anime/anime_collection/static/files/img/"


with open('./spider/files/collection_update_time.json', 'w', encoding='utf-8') as fi, open('./anime/anime_collection/static/files/json/collection.json', 'w', encoding='utf-8') as fo:
    json_data = list()
    while pn <= pn_max:
        # 重设url5
        url5 = f"https://api.bilibili.com/x/space/bangumi/follow/list?type=1&follow_status=0&pn={pn}&ps=15&vmid=44629592"
        response = requests.get(url=url5, headers=headers)
        if response.status_code == 200:
            response = response.json()
            json_data.extend(response['data']['list'])
            pn += 1

    # 获取到json数据写入文件    
    json.dump(json_data, fo, indent=4, ensure_ascii=False)
    print("Server File Writing Finished!")
    
    json.dump({'Update Time':  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, fi, indent=4, ensure_ascii=False)
    print("Local File Writing Finished!")


    img_data = [] 
    for item in json_data:
        img_data = {"name": item['title'], "url": item['cover']} 
        img_file_name =  f"{img_data['name']}.png"
        with open(img_file_path + img_file_name, 'wb') as imf:
            response = requests.get(img_data['url'])
            if response.status_code == 200:
                imf.write(response.content)
                print(f"Image downloaded and saved as {img_file_path + img_file_name}")
            else:
                print("Failed to download image")