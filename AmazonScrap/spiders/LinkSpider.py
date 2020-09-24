import scrapy
from urllib.parse import urlencode
from urllib.parse import urljoin
import re
import json

class LinkSpider(scrapy.Spider):
    name = "Amazon" 

    def start_requests(self):
        Item = getattr(self, 'item', None)
        Url = 'https://www.amazon.in/s?' + urlencode({'k': Item})

        yield scrapy.Request(url=Url, callback=self.parse)

    def parse(self, response):
        products = response.xpath('//*[@data-asin]')

        for product in products:
            asin = product.xpath('@data-asin').extract_first()
            product_url = f"https://www.amazon.in/dp/{asin}"
            yield scrapy.Request(url=product_url, callback=self.parse_product, meta={'asin':asin})



        # # follow links to product page
        # for href in something:
            # yield scrapy.Request(response.urljoin(href), callback=self.parse_product)

        # #follow pagination links
        # next_page = response.css()
        # if next_page is not None:
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback=self.parse)

    def parse_product(self, response):
        asin = response.meta['asin']
        title = response.xpath('//*[@id="productTitle"]/text()').extract_first()
        product_description = response.xpath('//*[@id="productDescription"]/p/text()').extract_first()
        print(title, product_description)
        
