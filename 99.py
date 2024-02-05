from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from stem import Signal
from stem.control import Controller
import requests
import time 
from selenium.webdriver.common.by import By
import csv
import re
def change_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        response = requests.get("http://httpbin.org/ip", proxies={"http": "socks5://localhost:9050", "https": "socks5://localhost:9050"})
        print(response.json()["origin"])
        return response.json()["origin"]
def convert_price(price_str):
    if price_str == "Price on Request":
        return 0  # Set price as 0 for "Price on Request"

    match = re.match(r"₹\s*([\d,.]+)\s*-\s*([\d,.]+)\s*(\w+)", price_str)
    if match:
        lower = float(match.group(1).replace(",", ""))
        upper = float(match.group(2).replace(",", ""))
        unit = match.group(3).strip().lower()

        if unit == "l":
            return (lower + upper) / 2  # Average for lakhs
        elif unit == "cr":
            return (lower + upper) * 100  # Multiply by 100 for crores

    match = re.match(r"₹\s*([\d,.]+)\s*(\w+)", price_str)
    if match:
        price = float(match.group(1).replace(",", ""))
        unit = match.group(2).strip().lower()

        if unit == "l":
            return price  # Price in lakhs
        elif unit == "cr":
            return price * 100  # Price in crores

    return None  

def convert_sqft(sqft_str):
    match = re.match(r"(\d+(?:,\d+)?(?:\.\d+)?)\s*-\s*(\d+(?:,\d+)?(?:\.\d+)?)\s*sq\.ft\.|\b(\d+(?:,\d+)?(?:\.\d+)?)\s*sq\.ft\.", sqft_str)
    if match:
        if match.group(3):  # Single value (e.g., "1,540 sq.ft.")
            sqft = float(match.group(3).replace(",", ""))
        else:  # Range format (e.g., "533 - 703 sq.ft.")
            lower = float(match.group(1).replace(",", ""))
            upper = float(match.group(2).replace(",", ""))
            sqft = (lower + upper) / 2
        return sqft
    return None


url="https://www.99acres.com/property-in-mumbai-ffid-page-"
file=open('scraped_data.csv','a')
count=0
city={
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
k=0
z=0
writer=csv.writer(file)
for i in range(1,101):
    with open('count.txt','r') as x:
        count=int(x.readline())
    print("Currently Scraping Page No: "+str(count))
    proxy_options = Options()
    proxy_options.headless=True
    proxy_options.set_preference("permissions.default.image", 2)
    proxy_options.add_argument("--proxy-server=socks5://localhost:9050".format(change_tor_ip()))
    geckodriver_path = "/home/ubuntu/geckodriver"
    driver = webdriver.Firefox(options=proxy_options)
    driver.get(url+str(count))

    # Find a specific element on the page
    body_element = driver.find_element(By.TAG_NAME, "body")
    # Scroll to the end of the page
    body_element.send_keys(Keys.END)
    time.sleep(3)
    print(driver.current_url)
    if driver.current_url=="https://www.99acres.com/load/verifycaptcha":
        print("GOt into captch exitting")
        exit(1) 
    soup = BeautifulSoup(driver.page_source, "html.parser")
    #print(soup)
    cards = soup.find_all("div", {'class':"projectTuple__cardWrap"})
    try:
        for card in cards:
        
            i_card=card.find(id=True)
            i1_card=i_card.find(class_=True)
            i2_card=i1_card.find_all("div")
            i3_card=i2_card[2]
            i4_card=i3_card.find_all("div")
            if len(i4_card)==0:
                continue
            i5_card=i4_card[0]
            #extracting property name
            property_name=i5_card.find("a").text.strip()
            #print(property_name.text.strip())
            #extracting typesof rooms available 
            room_container=i5_card.find("div",{"class":"carousel__slidingBox"})
            containers_x=room_container.find_all("div",recursive=False)
            # containers_x_y=containers_x.find_all(recursive=False)
            for container in containers_x:
                No_of_bhk=container.find("span",{"class":"list_header_semiBold configurationCards__configBandLabel"}).text.strip()
                sqft=container.find("span",{"class":"caption_subdued_medium configurationCards__cardAreaSubHeadingOne"}).text.strip()
                price=container.find("span",{"class":"list_header_semiBold configurationCards__cardPriceHeading"}).text.strip()
                pattern = r"(\d+(?:,\d+)?(?:\.\d+)?)\s*-\s*(\d+(?:,\d+)?(?:\.\d+)?)\s*sq\.ft\.|\b(\d+(?:,\d+)?(?:\.\d+)?)\s*sq\.ft\."
                match = re.match(pattern, sqft)
                no_of_bhk_int=''.join(filter(str.isdigit,No_of_bhk))
                if no_of_bhk_int.isdigit():
                    No_of_bhk=no_of_bhk_int
                else:
                    No_of_bhk=No_of_bhk
                no_of_bathrooms=No_of_bhk
                sqft=convert_sqft(sqft)
                price=convert_price(price)
                ratepersqft=price/sqft
                list=[property_name,city,No_of_bhk,no_of_bathrooms,sqft,price,ratepersqft]
                print(list)
                writer.writerow(list)
                print("Inserted a record Record no: "+str(z))
                z=z+1  
            k=k+1
    finally:        
        print(k)
        print(z)
        driver.quit()
        with open('count.txt','w') as x:
            x.write(str(count+1))
    



