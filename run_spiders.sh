#!/bin/sh
mkdir -p logs
mkdir -p data

echo "🕷️ Starting link_spider. Logging to link_spider.log"
scrapy crawl link_spider -o data/urls.json > logs/link_spider.log 2>&1 &
LINK_SPIDER_PID=$!

echo "⏳ Waiting 6 hours before running detail_spider..."
sleep 21600

echo "🚀 Starting detail_spider. Logging to detail_spider.log"
scrapy crawl detail_spider -o data/details.json > logs/detail_spider.log 2>&1 &

wait
echo "✅ All spiders finished." >> logs/run_status.log