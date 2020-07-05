from bs4 import BeautifulSoup as bs
import lxml
import re
from enum import Enum
from config import BASE_URL
import pandas as pd

class TagName(Enum):
    TEXT = 'text'
    HREF = 'href'
    CLASS = 'class'

class Soup():
    def __init__(self, file_name):
        self.file_name = file_name
        self.soup = self._read_html(file_name)
        
    def _read_html(self, file_name):
        with open(file_name, 'r') as f1:
            html = f1.read()
            soup = bs(html, 'html.parser')
        return soup

    def _strip_price(self, raw_str):
        regex = re.compile("\$\d+\.\d+")
        return (regex.findall(raw_str)[0])

    def _strip_rating(self, raw_str):
        regex = re.compile("\d+")
        return (regex.findall(raw_str)[0])

    def _extractData(self, attr, dataKind):
        if (dataKind == TagName.TEXT):
            return attr.text
        elif (dataKind == TagName.CLASS):
            return attr[dataKind.value][1]
        elif (dataKind == TagName.HREF):
            return attr[dataKind.value]

    def select_products(self, attri_kind, class_name):
        products = self.soup.findAll(attri_kind, {"class": class_name})
        names = []
        prices = []
        ratings = []
        href_strs = []
        for product in products:
            raw_name_strs = BSsoup.select_by_class(product, "div", class_name_product_name, TagName.TEXT)
            name = BSsoup.refine_str(raw_name_strs, "name")
            names.append(name)
            raw_price_strs = BSsoup.select_by_class(product, "div", class_name_price, TagName.TEXT)
            price = BSsoup.refine_str(raw_price_strs, "price")
            prices.append(price)
            raw_rating_strs = BSsoup.select_by_class(product, "div", class_name_rating, TagName.CLASS)
            rating = BSsoup.refine_str(raw_rating_strs, "rating")
            ratings.append(rating)
            href_str = BSsoup.select_by_class(product, "a", class_name_href, TagName.HREF)
            href_strs.append(href_str)

        return names, prices, ratings, href_strs

    def select_by_class(self, product, attri_kind, class_name, TagName):
        attris = product.findAll(attri_kind, {"class": class_name})
        raw_strs = []
        for attr in attris:
            raw_strs.append(self._extractData(attr, TagName))
        return raw_strs

    def refine_str(self, raw_strs, kind):
        refined_strs = []
        for raw_str in raw_strs:
            if (kind=="price"):
                refined_str = self._strip_price(raw_str)
            elif(kind == "rating"):
                refined_str = self._strip_rating(raw_str)
            else:
                #no need to refine
                refined_str = raw_str
            refined_strs.append(refined_str)
        return refined_strs

if __name__ =='__main__':
    class_name_product = "flex flex-column justify-between lh-title w-100"
    class_name_product_name = "lh-title normal f5 fw3 fw2-ns tc4-body"
    class_name_price = "flex flex-column items-stretch"
    class_name_rating = re.compile("star-rating star-rating-[0-9]")
    class_name_href = "js-product-link theme-grey-dark db"

    filename = "raw_html.html"
    BSsoup = Soup(filename)
    names, prices, ratings, href_strs = BSsoup.select_products("div", class_name_product)
    
    df = pd.DataFrame()
    df['name'] = [name[0] for name in names]
    df['prices'] = [price[0] for price in prices]
    df['ratings'] = [rating[0] if len(rating)>0 else '' for rating in ratings]
    df['product_url'] = [BASE_URL+url[0] for url in href_strs]
    df.to_csv("results.csv")
