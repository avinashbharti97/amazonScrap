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

        next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        if next_page:
            url = urljoin("https://www.amazon.in",next_page)
            yield scrapy.Request(url=url, callback=self.parse)


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
        bullet_points = response.xpath('//*[@id="feature-bullets"]//li/span/text()').extract()
        image = re.search('"large":"(.*?)"',response.text).groups()[0]
        rating = response.xpath('//*[@id="acrPopover"]/@title').extract_first()
        number_of_reviews = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first()
        price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()

        if not price:
            price = response.xpath('//*[@data-asin-price]/@data-asin-price').extract_first() or \
                    response.xpath('//*[@id="price_inside_buybox"]/text()').extract_first()
        # print(title, product_description, image, rating, number_of_reviews, price, bullet_points)
        yield {
                'asin':asin,
                'Title':title,
                'Description': product_description,
                'Bullets': bullet_points,
                'Image': image,
                'Rating': rating,
                'No of Reviews': number_of_reviews,
                'Price': price
                }
       












