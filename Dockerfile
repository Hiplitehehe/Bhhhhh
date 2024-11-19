FROM scrapinghub/scrapy:latest

WORKDIR /usr/src/app
COPY . .

RUN pip install -r requirements.txt

CMD ["scrapy", "crawl", "myspider"]
