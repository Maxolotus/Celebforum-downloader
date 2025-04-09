from lxml import html
import downloader
import requests
import json
import os

if not os.path.exists("config.json"):
    with open("config.json", "w") as f:
        f.write('''
{
    "xf_csrf":	"",
    "xf_session":	"",
    "xf_user":""
}
''')
        f.flush()
        f.close()
        print("The config.json was now created fill if you want to download something else than Pictures ;)")
        exit(-1)
else:
    data = json.load(open("config.json", "r"))



# user must contain the whole name: Example: feedeline.7495
def getUser(name, threads=2, pics=True, bunk=True, saint=True, waittime=4):
    url = f"https://celebforum.to/threads/{name}"
    req = requests.get(url, cookies=data)
    folder = name.split('.')[0]
    searcher = html.fromstring(req.text)
    tmp = searcher.xpath('//li[@class="pageNav-page "]/a')
    pages = 1 if len(tmp) < 1 else int(tmp[0].text_content())
    for i in range(1, pages+ 1):
        req = requests.get(f'{url}/page-{i}', cookies=data)
        searcher = html.fromstring(req.text)
        pictures = getPictures(searcher) if pics else []
        bunkr = getBunkr(searcher) if bunk else []
        saints = getSaint(searcher) if saint else []
        print(f"DOWNLOADING PICTURES OF PAGE-{i} WITH {len(pictures)} PICTURES!")
        downloader.download_files(pictures, folder, threads, cookies=data, celeb=True, waittime=waittime)
        print(f"DOWNLOADING BUNKR-VIDEOS OF PAGE-{i} WITH {len(bunkr)} VIDEOS!")
        downloader.download_files(bunkr, folder, threads, waittime=waittime)
        print(f"DOWNLOADING SAINTS-VIDEOS OF PAGE-{i} WITH {len(saints)} VIDEOS!")
        downloader.download_files(saints, folder, threads, headers=getSaintHeaders(), waittime=waittime)


def getRaw(searcher, xpath, attribute):
    tmp = searcher.xpath(xpath)
    raws = []
    for raw in tmp:
        raws.append(raw.get(attribute))
    return raws

def getPictures(searcher):
    return getRaw(searcher, '//div[@class="bbWrapper"]/a[@class="js-lbImage"]', 'href')

def getSaint(searcher):
    liste = getRaw(searcher, '//iframe[@class="saint-iframe"]', 'src')
    saints = []
    for saint in liste:
        req = requests.get(saint)
        ss = html.fromstring(req.text)
        tmp = ss.xpath('//source')
        for link in tmp:
            saints.append(link.get('src'))         
    return saints            

def getBunkr(searcher):
    liste = getRaw(searcher, '//span[@data-s9e-mediaembed="bunkr"]/a', 'href')
    bunkr = []
    for link in liste:
        req = requests.get(link)
        if req.status_code == 404:
            continue
        elif req.status_code != 200:
            print("Something MIGHT be wrong! Contact the Admin or Debug it yourself!")

        ss = html.fromstring(req.text)
        tmp = ss.xpath('//media-player[@id="player"]')
        for video in tmp:
            bunkr.append(video.get('src'))           
    return bunkr            

def getBasicHeaders():
    return {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/123.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
    "DNT": "1",  # Do Not Track
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "image",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
    }


def getSaintHeaders():
    return {
    "accept": "*/*",
    "accept-language": "de-DE,de;q=0.7",
    "origin": "https://saint2.pk",
    "priority": "i",
    "range": "bytes=0-",
    "referer": "https://saint2.pk/",
    "sec-ch-ua": '"Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "video",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

if __name__ == "__main__":
    # if you want to use it via code and not main.py you can do that!
    # but please only in this if statement. Gracias!
    print(end="")
