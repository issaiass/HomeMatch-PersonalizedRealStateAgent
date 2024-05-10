
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import argparse
import os
import logging
import sys

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

class FrameLoader:
    def __init__(self, webdir):
        self.webdir = webdir

    def list_files(self):
        return os.listdir(self.webdir)

    def read_webpage(self, webpage=None):
        path = os.path.join(self.webdir, webpage)
        with open(path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            soup = BeautifulSoup(html_content, features='html.parser')
        return soup

    def build_imglinks(self, soup):
        imgs = soup.find_all('img')
        list_imgs = [img.get('src') for img in imgs]
        list_imgs = list(filter(lambda x: x.endswith('true'), list_imgs))
        list_imgs = list(map(lambda x: x.split('?')[0], list_imgs))
        list_imgs = list(map(lambda x: {'links': x}, list_imgs))
        return pd.json_normalize(list_imgs)        

    def build_descriptions(self, soup):
        imgs = soup.find_all('img')
        descriptions = [img.get('alt') for img in imgs]
        descriptions = list(filter(lambda x: x is not None, descriptions))
        descriptions = list(filter(lambda x: len(x)>20, descriptions))
        descriptions = list(map(lambda x: {'description':x}, descriptions))
        return pd.json_normalize(descriptions)

    def build_home_descriptions(self, soup):
        anchors = soup.find_all('a')
        anchor_texts = [anchor.text for anchor in anchors]
        anchor_texts = list(filter(lambda x: len(x) > 40, anchor_texts))
        anchor_texts = list(map(lambda x: {'apartment_description': x}, anchor_texts))
        return pd.json_normalize(anchor_texts)

    def build_home_locations(self, soup):
        div_list = soup.find_all('h2')
        locations_list = [dvlst.text.split(',')[0] for dvlst in div_list]
        locations_list = list(map(lambda x: {'neighborhood': x}, locations_list))
        return pd.json_normalize(locations_list)        
    
    def build_home_info(self, soup):
        info_texts = soup.find_all('h3')
        span_texts = [info_text.find_all('span') for info_text in info_texts]
        span_texts = list(filter(lambda x: len(x) > 0, span_texts))
        span_type = ['sqm', 'room', 'bathroom', 'parking']
        span_texts = [[int(span.text.split(' ')[0]) for span in span_text] for span_text in span_texts]
        span_texts = list(map(lambda x: dict(zip(span_type, x)), span_texts))
        return pd.json_normalize(span_texts).fillna(0) # sometimes there are no parkings

    def build_home_prices(self, soup):
        info_price = soup.find_all('div')
        info_price = [price.text for price in info_price]
        info_price = [re.findall(r'(?<!USD\s)(USD\s*\d{1,3}(?:,\d{3})*)(?:\.\d{1,2})?(?!\d)', price) for price in info_price]
        info_price = list(filter(lambda x: x is not None, info_price))
        info_price = [[price.split('USD')[1].replace(',', '').strip() for price in info] for info in info_price]
        info_price = list(filter(lambda x: len(x) > 0, info_price))
        info_price = list(filter(lambda x: int(x) > 5000, info_price[0]))
        info_price = list(map(lambda x: {'price': int(x)}, info_price))
        return pd.json_normalize(info_price)

    def compile_and_save(self, *args, path, output_format='csv'):
        if output_format=='xlsx':
            pd.concat([*args], axis=1).to_excel(path, index=False, sheet_name='HomeMatch')
        if output_format=='csv':
            pd.concat([*args], axis=1).to_csv(path, header=True, index=False)
        if output_format=='parquet':
            pd.concat([*args], axis=1).to_parquet(path, index=False)            

    def build_documents(self, webpages, output_folder, output_format):
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        for n, webpage in enumerate(webpages):
            logger.info(f"processing {webpage}")
            path = os.path.join(output_folder, f'document{n:02}.{output_format}')
            
            soup = self.read_webpage(webpage)
            imglinks = self.build_imglinks(soup)
            descriptions = self.build_descriptions(soup)
            home_descriptions = self.build_home_descriptions(soup)
            home_info = self.build_home_info(soup)
            home_locations = self.build_home_locations(soup)
            home_prices = self.build_home_prices(soup)
            self.compile_and_save(imglinks, descriptions, home_descriptions, home_info, home_locations, home_prices, path=path, output_format=output_format)
         
def main(args):
    webdir, output_folder, output_format = args.webdir, args.output_folder, args.output_format
    fl = FrameLoader(webdir)
    webpages = fl.list_files()
    fl.build_documents(webpages=webpages, output_folder=output_folder, output_format=output_format)


if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description='builds a dataframe of the webpages selected')
    parser.add_argument('-w', '--webdir', type=str, default='webpages')
    parser.add_argument('-o', '--output-folder', type=str, default='documents')
    parser.add_argument('-f', '--output-format', type=str, default='csv')

    args = parser.parse_args()
    main(args)
