import unittest
from scrapy.http import HtmlResponse,Request
from books.spiders.book import BookSpider
from books.items import BooksItem

class BookSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = BookSpider()
        self.example_html = """
              <html>
                <body>
                    <article class="product_pod">
                        <h3><a title="Book 1" href="catalogue/book_1/index.html">Book 1</a></h3>
                        <p class="price_color">£10.00</p>
                    </article>
                    <article class="product_pod">
                        <h3><a title="Book 2" href="catalogue/book_2/index.html">Book 2</a></h3>
                        <p class="price_color">£15.00</p>
                    </article>
                    <li class="next">
                        <a href="page_2.html">next</a>
                    </li>
                </body>
            </html>
        """
        self.response = HtmlResponse(
            url="https://books.toscrape.com",
            body=self.example_html,
            encoding="utf-8"
        )


    def test_parse_scrape_all_items(self):
        """Test the parse method to ensure it scrapes all items correctly."""
        results = list(self.spider.parse(self.response))

        # There should be two book items and one pagination request
        book_items = [item for item in results if isinstance(item, BooksItem)]
        pagination_requests = [
            item for item in results if isinstance(item, Request)
        ]

        self.assertEqual(len(book_items), 2)
        self.assertEqual(len(pagination_requests), 1)

    def test_parse_scrapes_correct_book_information(self):
        """Test the parse method to ensure it scrapes the correct book information."""
        pass

    def test_parese_creates_pagination_requests(self):
        """Test the parse method to ensure it creates pagination requests."""
        pass

if __name__ == "__main__":
    unittest.main()