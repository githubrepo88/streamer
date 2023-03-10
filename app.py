import requests
from flask import Flask
from flask import request
import re
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route('/getm3u8',methods=['GET'])
def getm3u8():
    source = request.url
    source = source.replace('https://1xstreamer.azurewebsites.net/getm3u8?source=', '')
    source = source.replace('%2F', '/')
    source = source.replace('%3F', '?')
    videoid = request.args.get("videoid")
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "tr-TR, tr;q = 0.9",
        "origin": "https://www.maltinok.com",
        "referer": "https://www.maltinok.com/",
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    ts = requests.get("http://1xstreamer.azurewebsites.net/getm3u8?source=https://edge10.xmediaget.com/hls-live/9510503/1/mediaplaylist.m3u8?s=a2f1854d23e4986571dd0883495a1580ffe58d4643e9ebe61e92bfe32a8df994&t=1672274057047&ai=3&av=1025&ui=0", headers=headers)
    tsal = ts.text
    tsal = tsal.replace(videoid+'_','https://1xstreamer.azurewebsites.net/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/'+videoid+'/1/'+videoid+'_')
    return tsal

@app.route('/getstream',methods=['GET'])
def getstream():
    param = request.args.get("param")
    if param == "getts":
        source = request.url
        source = source.replace('https://1xstreamer.azurewebsites.net/getstream?param=getts&source=','')
        source = source.replace('%2F','/')
        source = source.replace('%3F','?')
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'tr-TR,tr;q=0.9',
            'origin': 'https://www.maltinok.com',
            'referer': 'https://www.maltinok.com/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        ts = requests.get(source,headers=headers)
        return ts.content
    if param == "getm3u8":
        videoid = request.args.get("videoid")
        veriler = {"AppId": "3", "AppVer": "1025", "VpcVer": "1.0.11", "Language": "tr", "Token": "", "VideoId": videoid}
        r = requests.post("https://lite-1x163215.top/cinema",json=veriler)
        if "FullscreenAllowed" in r.text:
            veri = r.text
            veri = re.findall('"URL":"(.*?)"',veri)
            veri = veri[0].replace("\/", "/")
            veri = veri.replace('edge3','edge10')
            veri = veri.replace('edge4','edge10')
            veri = veri.replace('edge2','edge10')
            veri = veri.replace(':43434','')
            if "m3u8" in veri:
                return "https://1xstreamer.azurewebsites.net/getm3u8?source="+veri+'&videoid='+videoid
        else:
            return "Veri yok"

if __name__ == '__main__':
    app.run()

