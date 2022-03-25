# -*- coding: utf-8 -*-
from fake_useragent import UserAgent
from scraper_api import ScraperAPIClient
import scrapy
import pandas as pd

API_KEY = 'ENTER_YOUR_SCRAPER_API_KEY'
client = ScraperAPIClient(API_KEY)

ua = UserAgent(verify_ssl=False)

class EtherscanSpider(scrapy.Spider):
    name = 'etherscan'
    hd = {'User-Agent': ua.Random}
    c = {'ASP.NET_SessionId': '242qg1rtdknr4txnfl14c4sb'}
    def start_requests(self):
        url = 'https://etherscan.io/labelcloud'
        yield scrapy.Request(url,headers=self.hd,cookies = self.c)
        
    def parse(self, response):
        lables = response.css('.dropdown-menu>a::attr(href)').getall()
        for lable in lables:
            yield scrapy.Request(client.scrapyGet(url=response.urljoin(lable)),callback=self.addresses,headers=self.hd,cookies = self.c)
            
    def addresses(self,response):
        table = pd.read_html(response.css('table').get())
        for record in table[0].to_dict('records'):
            yield record