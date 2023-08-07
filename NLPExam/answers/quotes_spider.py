from pathlib import Path

import jmespath
import scrapy
from scrapy.crawler import CrawlerProcess
import json
from csv import writer
import pandas as pd
import openpyxl

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://meta.stackoverflow.com/questions/421831/temporary-policy-chatgpt-is-banned#:~:text=ChatGPT%20is%20an%20Artificial%20Intelligence,rules',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        Path(filename).write_bytes(response.body)
        self.log(f'Saved file {filename}')
        self.parse_post(response)

    def parse_post(self, response):
        """
        Parses a post page
        """
        if len(response.css(
                '.dl-box')) > 1:  # our spider does not support such pages with multiple music tracks like https://tinyurl.com/2p85b4hx
            return []

        schema_graph_data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').get())
        info = jmespath.search('"@graph"[?"@type"==\'Article\']|[0]', schema_graph_data)
        L = []
        if info:
            #songs = response.xpath('//ul[has-class("audioplayer-audios")]//li')
            answers = response.xpath('//div[has-class("s-prose js-post-body")]//p')
            print("answer: ", answers)
            print("====================")
            for ans in answers:
                print('-----------------------------')
                print(ans)
                L.append(ans)

        df = pd.DataFrame(L, columns=['answers'])
        df.to_csv('chart.csv', encoding='utf-8')


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(QuotesSpider)
process.start()