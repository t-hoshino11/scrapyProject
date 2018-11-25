# -*- coding: utf-8 -*-
import scrapy


class SpotsSpider(scrapy.Spider):
    name = "spots"
    allowed_domains = ["tabelog.com"]
    start_urls = [
        # 横浜中華街
        'https://tabelog.com/kanagawa/A1401/A140105/',
        # 品川
        # 'https://tabelog.com/tokyo/A1314/A131403/',
    ]

    def parse(self, response):
        for spot_url in response.css("div.list-rst__rst-name > a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(spot_url), callback=self.parse_spot_page)
        next_page = response.css("li.c-pagination__item > a.c-pagination__arrow--next ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_spot_page(self, response):
        item = {}
        product = response.css("div#container")
        item["name"] = product.css("h2.display-name > span ::text").extract_first()
        item["score"] = product.css("b.c-rating__val > span ::text").extract_first()
        item["score_dinner"] = product.css("div.rdheader-rating__time > span.rdheader-rating__time-icon--dinner > em ::text").extract_first()
        item["score_lunch"] = product.css("div.rdheader-rating__time > span.rdheader-rating__time-icon--lunch > em ::text").extract_first()
        item["reviewCount"] = product.css("span.rdheader-rating__review-target > a > em ::text").extract_first()
        item["budget_dinner"] = product.css("div.rdheader-budget > p.rdheader-budget__icon--dinner > span.rdheader-budget__price > a ::text").extract_first()
        item["budget_lunch"] = product.css("div.rdheader-budget > p.rdheader-budget__icon--lunch > span.rdheader-budget__price > a ::text").extract_first()
        item["genre"] = product.css("div.rstinfo-table > table.rstinfo-table__table > tbody > tr > td > span ::text").extract_first()
        yield item
