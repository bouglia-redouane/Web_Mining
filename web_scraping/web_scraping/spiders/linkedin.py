import scrapy
from web_scraping.items import PostItem
import httpx
from bs4 import BeautifulSoup
from lxml import html


class LinkedinSpider(scrapy.Spider):
    name = "linkedin"
    countrys = [
        'France',
        'Canada',
        'United%20Kingdom',
        'Maroc',
        'United%20States',
        'South%20Africa',
        'Saudi%20Arabia',
        'United%20Arab%20Emirates'
    ]
    def start_requests(self):
        for country in self.countrys:
            url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=&location={country}&f_JT=T&f_TPR=r2592000"
            yield scrapy.Request(url, meta={'dont_redirect': True, 'country': country, 'current_url':url, 'nb': 1})

    def parse(self, response):
        posts = response.xpath('//li')
        if response.status == 429:
            self.logger.warning("Access denied: %s", response.url)
        for post in posts:
            job_url = post.xpath('div/a[contains(@class , "base-card__full-link")]/@href').get()
            date = post.xpath('//time[@class = "job-search-card__listdate--new"]/@datetime').get()
            yield scrapy.Request(job_url, callback=self.parse_post, meta=dict(dont_redirect= True, dont_retry= True, date=date, country=response.meta['country']))
        if response.meta['nb'] < 38:
            next_url = response.meta['current_url']+'&start='+str(25*response.meta['nb'])
            yield scrapy.Request(next_url, callback=self.parse, meta=dict(dont_redirect= True, country= response.meta['country'], current_url=response.meta['current_url'], nb= response.meta['nb']+1))
    def parse_post(self, resp):
        if resp.status == 429 :
            self.logger.warning("Access denied: %s", resp.url)
            with (httpx.Client() as client):
                response = client.get(resp.url)
            if response.status_code == 200:
                postItem = PostItem()
                soup = BeautifulSoup(response.text, 'html.parser')
                lxml_element = html.fromstring(str(soup))
                postItem['job_title'] = " ".join(lxml_element.xpath('//h1[contains(@class, "top-card-layout__title")]/text()'))
                postItem['job_url'] = resp.url
                postItem['date'] = resp.meta['date']
                postItem['company'] = " ".join(lxml_element.xpath('//a[contains(@class , "topcard__org-name-link")]/text()'))
                postItem['company_url'] = " ".join(lxml_element.xpath('//a[contains(@class , "topcard__org-name-link")]/@href'))
                postItem['location'] = " ".join(lxml_element.xpath('//span[contains(@class , "topcard__flavor--bullet")]/text()'))+f'/ {resp.meta["country"]}'
                postItem['job_description'] = " ".join(lxml_element.xpath('//div[contains(@class, "show-more-less-html__markup")]/text()'))
                yield postItem
        else:
            postItem = PostItem()
            postItem['date'] = resp.meta['date']
            postItem['job_title'] = resp.xpath('//h1[contains(@class, "top-card-layout__title")]/text()').get()
            postItem['job_url'] = resp.url
            postItem['company'] = resp.xpath('//a[contains(@class , "topcard__org-name-link")]/text()').get()
            postItem['company_url'] = resp.xpath('//a[contains(@class , "topcard__org-name-link")]/@href').get()
            postItem['location'] = resp.xpath('//span[contains(@class , "topcard__flavor--bullet")]/text()').get()+f'/ {resp.meta["country"]}'
            postItem['job_description'] = " ".join(resp.xpath('//div[contains(@class, "show-more-less-html__markup")]/text()').getall())
            yield postItem


