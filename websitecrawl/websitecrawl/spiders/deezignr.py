import scrapy
import os
import html2text
from urllib.parse import urljoin


class DeezignrSpider(scrapy.Spider):
    name = "deezignr"
    allowed_domains = ["deezignr.com"]
    start_urls = ["https://www.deezignr.com/collections/all"]

    def __init__(self, *args, **kwargs):
        super(DeezignrSpider, self).__init__(*args, **kwargs)

        # Create the output folder if it doesn't exist
        if not os.path.exists("output"):
            os.makedirs("output")

        # Initialize the html2text converter
        self.h = html2text.HTML2Text()
        self.h.ignore_links = True
        self.h.ignore_images = True
        self.h.ignore_tables = True
        self.h.ignore_emphasis = True
        self.h.ignore_anchors = True
        self.h.body_width = 0

    def parse(self, response):
        # Convert the HTML content to plain text
        text = self.h.handle(response.body.decode("utf-8"))
        text = text.replace("\n", " ")
        # Clean up the text
        text = text.strip()

        # Determine the filename based on the URL
        url = response.url.strip("/")
        # Generate a random filename using hash of the url
        filename = f"output/{hash(url)}.txt"

        # Write the text to the file
        with open(filename, "w") as f:
            f.write(text)

        # Follow links to other pages
        for link in response.xpath('//*[@id="product-grid"]/li[*]/link'):
            href = link.get()
            if href.startswith("/products/"):
                # Join the relative URL with the base URL of the current page
                url = urljoin(response.url, href)
                yield scrapy.Request(url, callback=self.parse)
