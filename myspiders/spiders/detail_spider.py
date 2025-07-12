import scrapy
import json

class BonyadSimpleSpider(scrapy.Spider):
    name = "detail_spider"

    def start_requests(self):
        with open("data/urls.json", "r", encoding="utf-8") as f:
            urls = json.load(f)
            for item in urls:
                yield scrapy.Request(item["link"], callback=self.parse)

    def parse(self, response):
        container = response.css("div.item__content.flex.p-16")

        question_title = container.css("h1.body__title::text").get()
        question_body = container.css("p.body__summary::text").get()

        answers = response.css("div[itemtype='https://schema.org/Answer'] p.content__body::text").getall()
        answers = [a.strip() for a in answers if a.strip()]

        yield {
           ### "url": response.url,
            "question_title": question_title,
            "question_body": question_body,
            "answers": answers
        }
