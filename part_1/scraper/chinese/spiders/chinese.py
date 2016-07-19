# -*- coding: utf-8
import abc

#we import scrapy
import  scrapy

#we use html2text to the extract text from the HTML documents
import html2text
converter = html2text.HTML2Text()
converter.ignore_links = True
converter.ignore_images = True

class WebsiteSpider(scrapy.Spider):

    """
    Each spider class inherits from scrapy.Spider
    """

    @abc.abstractmethod
    def parse_content(self, response):
        pass

    def parse(self, response):
        """
        This function gets called for each documents that the spider crawls.

        It returns a generator that returns both results and new requests
        that the crawler should follow...
        """

        #we parse the content and yield all returned items
        for result in self.parse_content(response):
            yield result

        #we fetch all links in the given document
        for href in response.css("a::attr('href')"):
            #we extract the URL...
            url = response.urljoin(href.extract())
            #...and return it
            yield scrapy.Request(url, self.parse)


class WikipediaSpider(WebsiteSpider):

    name = 'wikipedia'

    #we are only interested in Chinese Wikipedia articles
    #in case you're wondering: ZH means Zhōngwén (中文)
    allowed_domains = ['zh.wikipedia.org']
    #we start right on the landing page
    start_urls = ['https://zh.wikipedia.org/']

    def parse_content(self, response):
        """
        For Wikipedia articles, we extract the title (which is in an <h1> element
        with ID 'firstHeading') and the text (which is in a <div> element with
        ID 'mw-content-text')
        """

        categories = []
        try:
            category_links = response.selector.xpath("//div[@class='mw-normal-catlinks']//a/@title")
            categories = [link.extract() for link in category_links]
        except:
            pass

        item = {
            'categories' : categories,
            'url' : str(response.url),
            'title' : response.selector.xpath("//h1[@id='firstHeading']/text()").extract()[0],
            'text' :  converter.handle(response.selector.xpath("//div[@id='mw-content-text']").extract()[0])
        }
        return [item]


class ChinaDailySpider(WebsiteSpider):

    """
    This crawler fetches articles from the ChinaDaily website.
    """

    #we can call it with "scrapy crawl china_daily"
    name = 'china_daily'

    #only documents from this domain are of interest to us
    #(China Daily also has an English offering that we don't want to scrape)
    allowed_domains = ['china.chinadaily.com.cn']
    #we start right from the main page
    start_urls = ['http://china.chinadaily.com.cn/']

    def parse_content(self, response):
        """
        We extract the text that is in the <div> element with class 'container-left2'
        (which is the main text of the article on the website) 
        """

        categories = []
        try:
            category_links = response.selector.xpath("//div[@class='da-bre']//a/text()")
            categories = [link.extract() for link in category_links]
        except:
            pass

        try:
            item = {
                'categories' : categories,
                'url' : str(response.url),
                'text' :  converter.handle(response.selector.xpath("//div[@class='container-left2']").extract()[0])
            }
            return [item]
        except:
            return []
