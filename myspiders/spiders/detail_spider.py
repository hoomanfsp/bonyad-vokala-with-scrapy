import scrapy
import json
from urllib.parse import quote

class BonyadDetailSpider(scrapy.Spider):
    name = "detail_spider"

    def start_requests(self):
        with open("data/urls.json", "r", encoding="utf-8") as f:
            urls = json.load(f)
            for item in urls:
                yield scrapy.Request(item["link"], callback=self.parse_question)

    def parse_question(self, response):
        container = response.css("div.item__content.flex.p-16")
        question_title = container.css("h1.body__title::text").get()
        question_body = container.css("p.body__summary::text").get()

        answer_divs = response.css("div[itemtype='https://schema.org/Answer']")
        answers = []
        except_ids = []

        for div in answer_divs:
            answer_text = div.css("p.content__body::text").get()
            if answer_text:
                answers.append(answer_text.strip())
            aid = div.attrib.get("data-id")
            if aid:
                except_ids.append(aid)

        # If we have answers from the main page, yield them immediately
        if answers:
            yield {
                "url": response.url,
                "question_title": question_title,
                "question_body": question_body,
                "answers": answers
            }

        # Extract slug from URL
        question_slug = response.url.split("/question/")[-1].rstrip("/")
        encoded_slug = quote(question_slug, safe='')

        # Build load more API request
        except_query = "&".join([f"except_ids[{i}]={aid}" for i, aid in enumerate(except_ids)])
        api_url = f"https://www.bonyadvokala.com/api/v1/faq/questions/{encoded_slug}/answers?per_page=50&out_type=html&{except_query}"

        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Referer": response.url,
            "Accept": "application/json, text/plain, */*"
        }

        yield scrapy.Request(
            url=api_url,
            headers=headers,
            callback=self.parse_api_answers,
            meta={
                "question_title": question_title,
                "question_body": question_body,
                "answers": answers,
                "url": response.url
            },
            errback=self.handle_api_error
        )

    def parse_api_answers(self, response):
        prev_answers = response.meta["answers"]
        api_new_answers = response.css("p.content__body::text").getall()
        all_answers = prev_answers + [a.strip() for a in api_new_answers if a.strip()]

        yield {
            "url": response.meta["url"],
            "question_title": response.meta["question_title"],
            "question_body": response.meta["question_body"],
            "answers": all_answers
        }

    def handle_api_error(self, failure):
        # If API call fails, we still have the data from the main page
        if failure.value.response.status == 422:
            # This is expected - API returns 422 for some requests
            # The data was already yielded in parse_question
            pass
        else:
            # Log other errors
            self.logger.error(f"API request failed: {failure.value}")
