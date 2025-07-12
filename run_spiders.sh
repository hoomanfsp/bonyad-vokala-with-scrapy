#!/bin/sh
mkdir -p logs
mkdir -p data
echo " Starting link_spider. Logging to link_spider.log"
scrapy crawl link_spider -o data/urls.json > logs/link_spider.log 2>&1
echo " Link spider finished. Starting detail_spider..."
echo " Starting detail_spider. Logging to detail_spider.log"
scrapy crawl detail_spider -o data/details.json > logs/detail_spider.log 2>&1
echo " All spiders finished." >> logs/run_status.log