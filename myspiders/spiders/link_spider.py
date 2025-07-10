import scrapy
import re

class LinkSpiderSpider(scrapy.Spider):
    name = "link_spider"
    start_urls = [
        "https://www.bonyadvokala.com/مشاوره-حقوقی/question?page=8210"
    ]
    max_page = 24000  # Upper limit to prevent infinite crawling

    def parse(self, response):
        self.logger.info(f"Parsing URL: {response.url}")

        try:
            links = response.xpath("//a[contains(@class, 'hover:text-blue-600') and contains(@class, 'text-gray-900')]/@href").getall()
            link_count = len(links)
            self.logger.info(f"Found {link_count} links on this page.")

            for link in links:
                yield {'link': link}

        except Exception as e:
            self.logger.error(f"Error extracting links: {e}")

        # Try normal next page
        try:
            next_page = response.xpath("//a[@class='page-link' and @rel='next']/@href").get()
            if next_page:
                page_number = self.extract_page_number(next_page)
                if page_number and page_number <= self.max_page:
                    self.logger.info(f"Following next page: {next_page}")
                    yield response.follow(next_page, callback=self.parse)
                    return
                else:
                    self.logger.info(f"Reached or exceeded max page ({self.max_page}), stopping.")
                    return
        except Exception as e:
            self.logger.error(f"Error getting next page link: {e}")

        # Fallback pagination
        try:
            current_page = self.extract_page_number(response.url)
            if current_page:
                next_fallback_page = current_page + 2
                if next_fallback_page > self.max_page:
                    self.logger.info(f"Fallback page {next_fallback_page} exceeds max ({self.max_page}), stopping.")
                    return
                fallback_url = re.sub(r'page=\d+', f'page={next_fallback_page}', response.url)
                self.logger.warning(f"Falling back to: {fallback_url}")
                yield response.follow(fallback_url, callback=self.parse)
        except Exception as e:
            self.logger.error(f"Fallback pagination failed: {e}")

    def extract_page_number(self, url):
        """Extracts the page number from a URL using regex"""
        match = re.search(r'page=(\d+)', url)
        return int(match.group(1)) if match else None
