# -*- coding: utf-8 -*-
import scrapy


class SpotsSpider(scrapy.Spider):
    name = "spots"
    allowed_domains = ["eiga.com"]
    start_urls = [
        'https://eiga.com/upcoming/',
    ]

    def parse(self, response):
        for spot_url in response.css("div.m_unit > h3 > a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(spot_url), callback=self.parse_spot_page)
        # next_page = response.css("li.next > a ::attr(href)").extract_first()
        # if next_page:
        #     yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_spot_page(self, response):
        item = {}
        product = response.css("div.moveInfoBox")
        item["title"] = product.css("h1 ::text").extract_first()
        item["date"] = product.css("span.opn_date > strong ::text").extract_first()
        item["checkin"] =product.css("div.mainBox > div.rateBox li#ci > a > strong ::text").extract_first()
        item["ranking"] =product.css("div.mainBox > div.rateBox li#rk > a > strong ::text").extract_first()
        # item['category'] = response.xpath(
        #     "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()"
        # ).extract_first()
        # item['description'] = response.xpath(
        #     "//div[@id='product_description']/following-sibling::p/text()"
        # ).extract_first()
        # item['price'] = response.css('p.price_color ::text').extract_first()
        yield item
