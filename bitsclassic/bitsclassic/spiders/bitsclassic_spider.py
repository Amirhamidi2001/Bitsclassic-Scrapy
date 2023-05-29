from pathlib import Path
from scrapy import FormRequest
import scrapy
import re
import json
import requests
from scrapy.selector import Selector
from selenium import webdriver
from time import sleep

from bitsclassic.items import BitsclassicItem


# class BitsclassicSpider(scrapy.Spider):
#     name = "bitsclassic"
#     start_urls = ["https://bitsclassic.com/fa/product/1511202-Cutting-Blade"]

#     def parse(self, response):
#         filename = f"product.html"
#         Path(filename).write_bytes(response.body)
#         self.log(f"Saved file {filename}")


class BitsclassicSpider(scrapy.Spider):
    name = "bitsclassic"
    start_urls = ['https://bitsclassic.com/fa']

    def parse(self, response):
        """
        This method is the default callback function for the initial request.
        """
        category_urls = response.css('ul.children a::attr(href)').getall()[1:]
        for category_url in category_urls:
            yield scrapy.Request(category_url, callback=self.parse_category)

    def parse_category(self, response):
        """
        This method is the callback function for category page requests..
        """
        url = "https://bitsclassic.com/fa/Product/ProductList"
        category_id = re.search(r"/(\d+)-", response.url).group(1)
        num_products = 1000
        data = {
            'Cats': str(category_id),
            'Size': str(num_products)
        }
        response = requests.post(url, data=data)
        response_dict = json.loads(response.text)
        html = response_dict.get('Html', '')
        product_urls = re.findall(r'href="([^"]+)" class="imageWrap"', html)
        for product_url in product_urls:
            yield scrapy.Request(product_url, callback=self.parse_product)

    def parse_product(self, response):
        """
        This method is the callback function for the product page requests.
        """
        # Extract data from the response using XPath or CSS selectors
        title = response.css('p[itemrolep="name"]::text').get()
        url = response.url
        categories = response.xpath('//div[@class="con-main"]//a/text()').getall()
        price = response.xpath('//div[@id="priceBox"]//span[@data-role="price"]/text()').get()

        # Process the extracted data
        if price is not None:
            price = price.strip()
            product_exist = True
        else:
            price = None
            product_exist = False

        # Create a new item with the extracted data
        item = BitsclassicItem()
        item["title"] = title.strip()
        item["categories"] = [category.strip() for category in categories][3:6]
        item["product_exist"] = product_exist
        item["price"] = price
        item["url"] = response.url
        item["domain"] = "bitsclassic.com/fa"

        # Yield the item to pass it to the next pipeline stage for further processing
        yield item


# class BitsclassicSpider(scrapy.Spider):
#     name = "bitsclassic"
#     start_urls = ['https://bitsclassic.com/fa']

#     def parse(self, response):
#         """
#         This method is the default callback function that will be
#         executed when the spider starts crawling the website.
#         """
#         category_urls = response.css('ul.children a::attr(href)').getall()[1:]
#         for category_url in category_urls:
#             yield scrapy.Request(category_url, callback=self.parse_category)

#     def parse_category(self, response):
#         """
#         This method is the callback function for the category requests.
#         """
#         category_id = re.search(r"/(\d+)-", response.url).group(1)
#         num_products = 1000

#         # Create the form data for the POST request
#         form_data = {
#             'Cats': str(category_id),
#             'Size': str(num_products)
#         }

#         # Send a POST request to retrieve the product list
#         yield FormRequest(
#             url='https://bitsclassic.com/fa/Product/ProductList',
#             method='POST',
#             formdata=form_data,
#             callback=self.parse_page
#         )

#     def parse_page(self, response):
#         """
#         This method is the callback function for the product page requests.
#         """
#         # Extract data from the response using XPath or CSS selectors
#         title = response.css('p[itemrolep="name"]::text').get()
#         url = response.url
#         categories = response.xpath('//div[@class="con-main"]//a/text()').getall()
#         price = response.xpath('//div[@id="priceBox"]//span[@data-role="price"]/text()').get()

#         # Process the extracted data
#         if price is not None:
#             price = price.strip()
#             product_exist = True
#         else:
#             price = None
#             product_exist = False

#         # Create a new item with the extracted data
#         item = BitsclassicItem()
#         item["title"] = title.strip()
#         item["categories"] = categories[3:-1]
#         item["product_exist"] = product_exist
#         item["price"] = price
#         item["url"] = response.url
#         item["domain"] = "bitsclassic.com/fa"

#         # Yield the item to pass it to the next pipeline stage for further processing
#         yield item


# class BitsclassicSpider(scrapy.Spider):
#     name = "bitsclassic"
#     start_urls = ['https://bitsclassic.com/fa']

#     def parse(self, response):
#         # Extract category URLs
#         category_urls = response.css('ul.children a::attr(href)').getall()[1:]

#         # Extract product URLs from category URLs using Selenium
#         for category_url in category_urls:
#             driver = webdriver.Firefox()
#             driver.get(category_url)
#             sleep(10)
#             sel = Selector(text=driver.page_source)
#             product_urls = sel.xpath('//div[contains(@class, "productBox")]/div[@class="inner"]/div[@class="productInfo tooltipWrap"]/div[@class="productTitle"]/a/@href').getall()
#             driver.quit()

#             for product_url in product_urls:
#                 yield scrapy.Request(product_url, callback=self.parse_product)

#     def parse_product(self, response):
#         """
#         This method is the callback function for the product page requests.
#         """
#         # Extract data from the response using XPath or CSS selectors
#         title = response.css('p[itemrolep="name"]::text').get()
#         url = response.url
#         categories = response.xpath('//div[@class="con-main"]//a/text()').getall()
#         price = response.xpath('//div[@id="priceBox"]//span[@data-role="price"]/text()').get()

#         # Process the extracted data
#         if price is not None:
#             price = price.strip()
#             product_exist = True
#         else:
#             price = None
#             product_exist = False

#         # Create a new item with the extracted data
#         item = BitsclassicItem()
#         item["title"] = title.strip()
#         item["categories"] = categories[3:-1]
#         item["product_exist"] = product_exist
#         item["price"] = price
#         item["url"] = response.url
#         item["domain"] = "bitsclassic.com/fa"

#         # Yield the item to pass it to the next pipeline stage for further processing
#         yield item


# class CategorySpider(scrapy.Spider):
#     name = 'category'
#     start_urls = ['https://bitsclassic.com/fa']

#     def parse(self, response):
#         category_urls = response.css('ul.children a::attr(href)').getall()[1:]
#         for category_url in category_urls:
#             yield {
#                 'category_url': category_url
#             }


# class DetailSpider(scrapy.Spider):
#     name = "detail"
#     start_urls = ["https://bitsclassic.com/fa/product/1511072-ROUND-NOSE-BIT"]

#     def parse(self, response):

#         # Extract data from the response using XPath or CSS selectors
#         title = response.css('p[itemrolep="name"]::text').get()
#         url = response.url
#         categories = response.xpath('//div[@class="con-main"]//a/text()').getall()
#         price = response.xpath('//div[@id="priceBox"]//span[@data-role="price"]/text()').get()
#         if price is not None:
#             price = price.strip()
#             product_exist = True
#         else:
#             price = None
#             product_exist = False

#         # Create a new item with the extracted data
#         item = BitsclassicItem()
#         item["title"] = title.strip()
#         item["categories"] = categories[3:-1]
#         item["product_exist"] = product_exist
#         item["price"] = price
#         item["url"] = response.url
#         item["domain"] = "bitsclassic.com/fa"
#         yield item
