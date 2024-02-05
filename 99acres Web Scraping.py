import time
import timeit
import pandas as pd
import requests
from requests import get
from bs4 import BeautifulSoup
from itertools import cycle
import traceback
import warnings
# from ballyregan import ProxyFetcher
# from ballyregan.models import Protocols, Anonymities

# from proxies import proxies

warnings.filterwarnings("ignore")

API_KEY = "df0c28136840161a0c799a33dc618c84"

# fetcher = ProxyFetcher(debug=True)

"""headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "none",
    "Accept-Language": "en-US,en;q=0.8",
    "Connection": "keep-alive",
}"""


def property_nane(soupy_object):  # return house or property name
    try:
        name = soupy_object.find("span", attrs={"class": "undefined"}).text
    except:
        name = None
    return name


def total_price(soupy_object):  # return total price of property
    try:
        price = soupy_object.find("span", attrs={"id": "pdPrice2"}).text
    except:
        price = None
    return price


def rate_sqft(soupy_object):  # return total price of property
    try:
        rate = soupy_object.find("div", attrs={"id": "pricePerUnitArea"}).text.split(
            " "
        )[1]
    except:
        rate = None
    return rate


def area_type(soupy_object):  # return area parameters
    try:
        areatyp = soupy_object.find("div", attrs={"id": "factArea"}).text
    except:
        areatyp = None
    return areatyp


def bedroom_count(soupy_object):  # return number of bedrooms
    try:
        bedroom = soupy_object.find("span", attrs={"id": "bedRoomNum"}).text.split(" ")[
            0
        ]
    except:
        bedroom = None
    return bedroom


def bathroom_count(soupy_object):  # return number of bathrooms
    try:
        bathroom = soupy_object.find("span", attrs={"id": "bathroomNum"}).text.split(
            " "
        )[0]
    except:
        bathroom = None
    return bathroom


def floor_num(soupy_object):  # return number of floor
    try:
        floornum = soupy_object.find("span", attrs={"id": "floorNumLabel"}).text.split(
            " "
        )[0]
    except:
        floornum = None
    return floornum


def property_age(soupy_object):  # return age of property
    try:
        age = soupy_object.find("span", attrs={"id": "agePossessionLbl"}).text
    except:
        age = None
    return age


def availability(soupy_object):  # return area parameters
    try:
        avail = soupy_object.find("span", attrs={"id": "Availability_Lbl"}).text
    except:
        avail = None
    return avail


def area(soupy_object):
    try:
        avail = soupy_object.find("span", attrs={"id": "Area_Lb1"}).text
    except:
        avail = None
    return avail


cities = {
    "arunachal": "229",
    "meghalaya": "241",
    "manipur": "240",
    "sikkim": "247",
    "tripura": "248",
    "assam": "230",
    "patna": "71",
    "amravati": "456",
    "raipur": "75",
    "panaji": "80",
    "gandhinagar": "46",
    "chandigarh": "73",
    "shimla": "109",
    "ranchi": "117",
    "bangalore": "20",
    "trivandum": "138",
    "bhopal": "140",
    "mumbai": "12",
    "nagaland": "243",
    "bhubaneshwar": "162",
    "chandigarh": "73",
    "jaipur": "177",
    "chennai": "32",
    "hyderabad": "38",
    "agartala": "195",
    "dehradun": "211",
    "lucknow": "205",
    "kolkata": "25",
}

data_list = []

"""def get_response(url):
    proxies = {
        "http": f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001'
    }
    i = 0
    response = None
    while response is None:
        try:
            print("attempt #", i)
            i+=1
            time.sleep(1)
            response = get(url, proxies=proxies)
            if (
                    response is not None
                    and response.status_code == 200
                    and response.text.find("Security Checkup") == -1
                ):
                    break
        except Exception as e:
            print(type(e))
            print(str(e))

    return response"""


blocked_proxies = []


"""
def get_proxy():
    proxy = fetcher.get(
        limit=1,
        protocols=[Protocols.HTTP, Protocols.HTTPS],
        anonymities=[
            Anonymities.ELITE,
            Anonymities.ANONYMOUS,
            Anonymities.TRANSPARENT,
            Anonymities.UNKNOWN,
        ],
    )[0]
    while proxy in blocked_proxies:
        proxy = fetcher.get(
            limit=1,
            protocols=[Protocols.HTTP, Protocols.HTTPS],
            anonymities=[
                Anonymities.ELITE,
                Anonymities.ANONYMOUS,
                Anonymities.TRANSPARENT,
                Anonymities.UNKNOWN,
            ],
        )[0]
    return proxy

proxy = get_proxy()
"""

proxies = []


def fetch_proxies():
    global proxies
    response_text = requests.get(
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=in&ssl=all&anonymity=all"
    ).text
    proxies = [line.strip() for line in response_text.split("\n") if line.strip()]


def get_proxy():
    while len(proxies) == 0:
        fetch_proxies()
        time.sleep(10)

    return proxies[0]


def get_response(url):
    proxy = None
    while proxy is None or proxy in blocked_proxies:
        proxy = get_proxy()
        if proxy in blocked_proxies:
            del proxies[0]

    response = None
    i = 1
    while True:
        print("attempt # ", i)
        i += 1
        try:
            print("trying proxy", proxy)
            response = get(
                url,
                proxies={"http": proxy, "https": proxy},
                timeout=10,
            )
            if (
                response is not None
                and response.status_code == 200
                and response.text.find("Security checkup") == -1
            ):
                break
            else:
                blocked_proxies.append(proxies[0])
                del proxies[0]
                while proxy in blocked_proxies:
                    proxy = get_proxy()
        except Exception as e:
            print(type(e))
            print(str(e))
            blocked_proxies.append(proxies[0])
            del proxies[0]
            while proxy in blocked_proxies:
                proxy = get_proxy()

    return response


df = pd.DataFrame()


def get_all(city):
    print("city:", city)
    timestart = timeit.default_timer()
    url = f"https://www.99acres.com/search/property/buy/cityname?city={cities[city]}&keyword=city-name&preference=S&area_unit=1&res_com=R"
    req = get_response(url)
    soup = BeautifulSoup(req.content, "html.parser")
    links = soup.find_all("a", attrs={"class": "body_med srpTuple__propertyName"})
    print("got city search results")
    print("links:", len(links))

    for i, item in enumerate(links):
        print("link number", i)
        data_url = item.get("href")
        request = get_response(data_url)
        soup_get = BeautifulSoup(request.content, "html.parser")
        name = property_nane(soup_get)
        price = total_price(soup_get)
        rate = rate_sqft(soup_get)
        areatyp = area_type(soup_get)
        bedroom = bedroom_count(soup_get)
        bathroom = bathroom_count(soup_get)
        floornum = floor_num(soup_get)
        age = property_age(soup_get)
        avail = availability(soup_get)
        area = area(soup_get)
        data = {
            "Property_Name": name,
            "Location": city,
            "Price": price,
            "Rate_SqFt": rate,
            "Area_Tpye": areatyp,
            "Bedroom": bedroom,
            "Bathroom": bathroom,
            "Floor_No": floornum,
            "Property_Age": age,
            "Availability": avail,
            "Area_SqFt": area,
        }
        data_list.append(data)
        df = pd.DataFrame(data_list)
        df.to_csv("Datasets/Raw_Property.csv", index_label=False)


for city in cities:
    get_all(city)
