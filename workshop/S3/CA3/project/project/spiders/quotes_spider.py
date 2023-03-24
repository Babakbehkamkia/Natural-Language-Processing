from pathlib import Path

import jmespath
import scrapy
from scrapy.crawler import CrawlerProcess
import json
from csv import writer

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://songsara.net/117646/',
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
        with open('D:/term 8/nlp/workshop/s3/data.csv', 'a') as f_object:
            writer_object = writer(f_object)
            if info:
                songs = response.xpath('//ul[has-class("audioplayer-audios")]//li')
                artists = response.xpath('//div[has-class("AR-Si")]//a')
                for song in songs:
                    L = []
                    music_name = song.attrib.get('data-title', '')
                    album_name = song.attrib.get('data-album', '')
                    artist_name = song.attrib.get('data-artist', '')
                    file_urls = song.attrib.get('data-src', '')
                    L.append(music_name, album_name, artist_name, file_urls)
                    writer_object.writerow(L)
            f_object.close()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(QuotesSpider)
process.start()