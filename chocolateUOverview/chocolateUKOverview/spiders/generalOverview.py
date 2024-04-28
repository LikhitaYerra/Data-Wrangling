import scrapy
import json

class GeneralOverviewSpider(scrapy.Spider):
    name = "generalOverview"
    allowed_domains = ["www.chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk"]

    def parse(self, response):
        products = response.css('.product-item')

        # Extract prices and filter out non-numeric values
        prices = [float(product.css('span.price').re_first(r'\d+\.\d+')) for product in products if product.css('.product-item__label-list span::text')]

        if prices:
            # Calculate min, max, and mean
            min_price = min(prices)
            max_price = max(prices)
            mean_price = sum(prices) / len(prices)

            # Log the statistics
            self.log(f'Min Price: {min_price}, Max Price: {max_price}, Mean Price: {mean_price}')

            # Prepare structured data for sold out products
            sold_out_products = []
            for product in products:
                if product.css('.product-item__label-list span::text'):
                    product_name = product.css('a.product-item-meta__title::text').get().strip()
                    product_price = float(product.css('span.price').re_first(r'\d+\.\d+'))
                    product_url = 'https://www.chocolate.co.uk' + product.css('div.product-item-meta a::attr(href)').get()

                    sold_out_products.append({
                        'Name': product_name,
                        'Price': product_price,
                        'URL': product_url
                    })

            # Save sold out products in a JSON file
            with open('sold_out_products.json', 'w') as json_file:
                json.dump(sold_out_products, json_file, indent=2)




            



