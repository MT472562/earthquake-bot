import json
import datetime
import time
import requests
import tweepy


def post():
    time.sleep(3)
    now = datetime.datetime.now() - datetime.timedelta(seconds=1)
    Y, m, d, H, M, S = now.strftime("%Y %m %d %H %M %S").split()
    requests_time = f"{Y}{m}{d}{H}{M}{S}"
    jsonurl = ("http://www.kmoni.bosai.go.jp/webservice/hypo/eew/{0}.json".format(requests_time))
    # jsonurl = "http://www.kmoni.bosai.go.jp/webservice/hypo/eew/20230417022555.json"
    # jsonurl="http://www.kmoni.bosai.go.jp/webservice/hypo/eew/20230417022907.json"
    jsonurls = requests.get(jsonurl)
    text = jsonurls.text
    data = json.loads(text)
    json.dumps(data)
    ms = data["result"]["message"]

    return data, ms


def create_text(data):
    origin_num = data['origin_time']
    earthquaketype = data['alertflg']
    report_time = data['report_time']
    report_num = data['report_num']
    region_name = data['region_name']
    depth = data['depth']
    magunitude = data['magunitude']
    calcintensity = data['calcintensity']
    latitude = data['latitude']
    longitude = data['longitude']
    final_report = data["is_final"]
    map_url = "https://www.google.co.jp/maps/place/{0},{1}/@{0},{1},7z/".format(latitude, longitude)

    if report_num == 1:
        type_text = "地震情報　初報"
    elif final_report:
        type_text = "地震情報　最終報"
    else:
        type_text = "地震情報第{0}報".format(report_num)

    out_text = type_text + "\n" + report_time[5:] + "時点での情報です。" \
               + "\n【" + region_name + "】で地震が発生しました。" \
               + "\n震源の深さは" + depth \
               + "\n地震の規模はM" + magunitude + "です。" \
               + "\n震度は" + calcintensity + "です。\n" + map_url

    return out_text, magunitude, calcintensity



def magirawashili_api():
    COSUMER_KEY = 'jzgYvpAhMqouIMVaw7Dt1xFc6'
    COSUMER_SECRET = 'jDOCW4mJ6FZqKGx2Q9KkCBQW26FPOeEosxOeQm6Tp7jvUfhqGC'
    ACCESS_TOKEN = '1208654375356227584-RpXPkSsb9GXlyx12S213CzWojRE4bT'
    ACCESS_TOKEN_SECRET = 'maCB0lL4zD08Lko2A7LX6arMSwontgnLUl3LxpngsBZxe'
    client = tweepy.Client(
        consumer_key=COSUMER_KEY,
        consumer_secret=COSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    return client


def bot_api():
    COSUMER_KEY = '233xR6fJzL1q3zsv0sr5IfDdO'
    COSUMER_SECRET = 'vxDCY8YsovjPU2BJHK9S9qnXJ34qmiDU5UqFkrhbXaW8pRejYM'
    ACCESS_TOKEN = '1403836122715672580-qhGKrU1yJwdZNpvEPRdzJHiofHagUI'
    ACCESS_TOKEN_SECRET = 'bnd8CfNLmgdE2iUlmw9KG6VkpbPyppdf5xgGq5g9oJsPm'
    client = tweepy.Client(
        consumer_key=COSUMER_KEY,
        consumer_secret=COSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    return client


def fast_twwet(text_data):
    client = magirawashili_api()
    client.create_tweet(text=str(text_data))

    client = bot_api()
    client.create_tweet(text=str(text_data))



while True:
    try:
        data, ms = post()
        if ms == "":
            out_text, magunitude, calcintensity = create_text(data)

        if float(magunitude) >= 5 or int(calcintensity) >= 4:
            print(out_text)
            fast_twwet(out_text)
        else:
            print("地震の規模がM５以下または震度４以下のため、Tweetはしません")
            print(out_text)
            pass
    except:
        pass


