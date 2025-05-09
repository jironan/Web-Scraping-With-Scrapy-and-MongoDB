import scrapy
from books.items import BooksItem


class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def start_requests(self):
       for url in self.start_urls:
              yield scrapy.Request(url=url, 
                                   callback=self.parse, 
                                   errback=self.log_error)

    def log_error(self, failure):
        self.logger.error(f"Error occurred: {failure}")

     # parse default callback`method for the spider
    def parse(self, response):
        """
        @url https://books.toscrape.com
        @returns items 20 20
        @returns request 1 50
        @scrapes url title price

        """


        for books in response.css("article.product_pod"):
            item = BooksItem()
            item["url"] = books.css("h3 a::attr(href)").get()
            item["title"] = books.css("h3 a::attr(title)").get()
            item["price"] = books.css("div p.price_color::text").get()
            yield item

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(
                f"Navigating to next page: {next_page_url}."
            )
            yield scrapy.Request(url=next_page_url, 
                                 callback=self.parse,
                                 errback=self.log_error
                                 )
