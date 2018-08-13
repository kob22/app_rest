from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import time
from app.models import Category, Product
from app import app, db
def scrape():

    urls = ['https://www.aliexpress.com/category/200002279/pendant-lights/2.html?site=glo&SortType=total_tranpro_desc&tag=']
    ua = UserAgent()
    header = {'User-Agent':str(ua.firefox)}
    all_products = []
    all_det_products = []
    print(urls)

    for url in urls:
        r = requests.get(url, headers=header)
        soup =BeautifulSoup(r.text, "html.parser")
        for product in soup.findAll("a", "product", href=True):

            all_products.append(product['href'].replace("//", "https://").split("?")[0])
        for single_product in all_products[:10]:
            if not Product.query.filter_by(link=single_product).first():
                r = requests.get(single_product, headers=header)
                time.sleep(5)
                soup = BeautifulSoup(r.text, "html.parser")
                product = Product()

                product.link = single_product
                product.name = soup.find("h1", {"class": "product-name"}).text
                product.rating = float(soup.find("span", {'itemprop': 'ratingValue'}).text)
                product.votes = int(soup.find("span", {'itemprop': 'reviewCount'}).text)
                product.orders = int(soup.find("span", {'class': 'order-num'}).text.split(" ")[0])
                price_reg = soup.find("span", {'id': 'j-sku-price'}).text.split("-")
                if len(price_reg) > 1:
                    product.reg_low_price = float(price_reg[0])
                    product.reg_high_price = float(price_reg[1])
                else:
                    product.reg_low_price = float(price_reg[0])
                    product.reg_high_price = None
                if soup.find("span", {'id': 'j-sku-discount-price'}):
                    price_discount = soup.find("span", {'id': 'j-sku-discount-price'}).text.split("-")
                    if len(price_reg) > 1:
                        product.dis_low_price = float(price_discount[0])
                        product.dis_high_price = float(price_discount[1])
                    else:
                        product.dis_low_price = float(price_discount[0])
                        product.dis_high_price = None

                cat_name = soup.find("div", {"class": "ui-breadcrumb"}).find("h2").text
                cat_name_find = Category.query.filter(Category.name==cat_name).first()
                if cat_name_find:

                    product.category = cat_name_find
                else:
                    print("aa")
                    product.category = Category(name=cat_name)
                product.img_link = soup.find("a", {"class": "ui-image-viewer-thumb-frame"}).find("img")['src']
                print(product)
                db.session.add(product)

                db.session.commit()





scrape()