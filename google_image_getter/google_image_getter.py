import json
import os
import sys
import re
import urllib3
from apiclient.discovery import build
import pprint
import shutil

# dict型
import key

# google custom searchで画像検索してくる　keyword = 検索単語　n = 個数
# 画像のurlを配列で返す
def search_images(keyword, n = 10):

    apikey = key.key['apikey']
    engine_id = key.key['cx']

    service = build("customsearch","v1",developerKey=apikey)
    now = 1
    image_url =[]

    if n < 10:
        n = 10

    while n > 0:
        res = service.cse().list(
            q = keyword,
            searchType = "image",
            start = now,
            #cr = "JP"
            cx = engine_id 
            ).execute()

        json_str = json.dumps(res)
        j = json.loads(json_str)
        for x in j['items']:
            image_url += [x['link']]

        now += 10
        n -= 10
    
    return image_url

#画像をpwdに(存在しなければ)keywordディレクトリを作成し保存する
#名前はアドレスの最後列(あれなんていうんだ) e.g. http://example.com/kawaii_onnnanoko.jpg -> kawaii_onnnanoko.jpg
def download_images(keyword, image_url):
    http = urllib3.PoolManager()
    prog = re.compile(".*/(.*)")

    if os.path.exists(keyword) == False:
        os.mkdir(keyword)

    for x in image_url:
        try:
            res = http.request("GET",x,preload_content=False)
            regres = prog.search(x)
            file_name = regres.group(1)
            img_file = open(keyword + "\\" + file_name, "wb")
            shutil.copyfileobj(res,img_file)
            img_file.close()
        except:
            continue

def _main():

    keyword = "アニメ"        
    image_url = search_images(keyword,30)
    download_images(keyword, image_url)


if __name__ == '__main__':
    _main()