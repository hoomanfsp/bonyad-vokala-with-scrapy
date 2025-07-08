import scrapy
import json

class LinkSpiderSpider(scrapy.Spider):
    name = "link_spider"
    start_urls = ["https://www.bonyadvokala.com/%D9%85%D8%B4%D8%A7%D9%88%D8%B1%D9%87-%D8%AD%D9%82%D9%88%D9%82%DB%8C/question?page=1"]

    def parse(self, response):
        try:
            for respons in response.xpath("//a[contains(@class, 'hover:text-blue-600') and contains(@class, 'text-gray-900')]/@href").getall() :    
                yield{
                    'link' : respons,

                }
        except Exception as e:
            self.logger.error(f"Error extracting link: {e}")
#        rooms = response.xpath("//a[contains(@class, 'hover:text-blue-600') and contains(@class, 'text-gray-900')]/@href").get()
        
        next_page = response.xpath("//a[@class='page-link' and @rel='next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


















"""        #  CHANGE THIS SELECTOR
        links = response.css("div.item a::attr(href)").getall()

        for link in links:
            yield {"url": response.urljoin(link)}

        #  CHANGE THIS PAGINATION SELECTOR
        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
"""