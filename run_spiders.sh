#!/bin/bash

echo "Starting link_spider for 10 minutes..."
scrapy crawl link_spider &
LINK_SPIDER_PID=$! # Get the process ID of the link_spider

sleep 600 # Wait for 10 minutes (600 seconds)

echo "Starting detail_spider (both spiders will now run concurrently)..."
scrapy crawl detail_spider &

wait # Wait for all background processes to complete (i.e., both spiders)

echo "All spiders have finished."