from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

def scrape():

    url = ['https://www.aliexpress.com/item/S-XXL-Women-Elegant-Dress-Crochet-Lace-Chiffon-Beach-Dress-2018-Sexy-Sleeveless-Long-Party-Maxi/32855018609.html?spm=2114.search0103.3.18.4ac33d37L7tQww&ws_ab_test=searchweb0_0,searchweb201602_5_10152_10151_10065_10344_10068_10342_10343_10340_10341_312_10696_10084_5723616_10083_10618_10304_10307_10820_10301_10821_5011415_10843_10059_5011315_100031_10103_10624_10623_10622_10621_10620_528,searchweb201603_55,ppcSwitch_5&algo_expid=ca50d7f2-a8b5-410e-8cf7-fd9ca77f7aec-2&algo_pvid=ca50d7f2-a8b5-410e-8cf7-fd9ca77f7aec&transAbTest=ae803_2&priceBeautifyAB=0']
    ua = UserAgent()
    header = {'User-Agent':str(ua.firefox)}
    product = {}
    r = requests.get(url[0], headers=header)
    soup =BeautifulSoup(r.text, "html.parser")
    product['product_name'] = soup.find("h1", {"class": "product-name"} ).text
    product['rating'] = float(soup.find("span", {'itemprop': 'ratingValue'}).text)
    product['votes'] = int(soup.find("span", {'itemprop': 'reviewCount'}).text)
    product['orders'] = int(soup.find("span", {'class': 'order-num'}).text.split(" ")[0])
    price_reg = soup.find("span", {'id': 'j-sku-price'}).text.split("-")
    if len(price_reg) > 1:
        product['reg_low_price'] = float(price_reg[0])
        product['reg_high_price'] = float(price_reg[1])
    else:
        product['reg_low_price'] = float(price_reg[0])
        product['reg_high_price'] = None
    if soup.find("span", {'id': 'j-sku-discount-price'}):
        price_discount = soup.find("span", {'id': 'j-sku-discount-price'}).text.split("-")
        if len(price_reg) > 1:
            product['dis_low_price'] = float(price_discount[0])
            product['dis_high_price'] = float(price_discount[1])
        else:
            product['dis_low_price'] = float(price_discount[0])
            product['dis_high_price'] = ''
    product['dis_low_price'] = None
    product['dis_high_price'] = None
    product['category'] = soup.find("div", {"class": "ui-breadcrumb"}).find("h2").text
    product['img_link'] = soup.find("a", {"class": "ui-image-viewer-thumb-frame"}).find("img")['src']
    print(product)

scrape()

