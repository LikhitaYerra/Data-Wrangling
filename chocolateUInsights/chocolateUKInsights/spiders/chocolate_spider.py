import requests
from bs4 import BeautifulSoup

# Initialize the starting URL
url = 'https://www.chocolate.co.uk/collections/all'
list_of_urls = [url]
total_number_of_products = 0

# Main loop to navigate through pages
while list_of_urls:
    current_url = list_of_urls.pop(0)  # Take the first URL from the list

    # Make a request to the current URL
    response = requests.get(current_url)

    # Check if the request is successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the link to the next page, if available
        next_page = soup.select('a[rel="next"]')
        if len(next_page) > 0:
            next_url = 'https://www.chocolate.co.uk' + next_page[0]['href']
            list_of_urls.append(next_url)

        # Extract product information on the current page
        products = soup.select('.product-item__info')
        number_of_products = len(products)
        total_number_of_products += number_of_products

        print(f'Number of products on {current_url}: {number_of_products}')

        # Check if there are products before displaying information
        if number_of_products > 0:
            first_product = products[0]
            product_name = first_product.select_one('.product-item-meta__title').text.strip()
            product_price = first_product.select_one('.price-list .price').text.strip()

            # Display information about the first product
            print('First product information:')
            print(f'Product Name: {product_name}')
            print(f'Product Price: {product_price}')
            print('-' * 30)
    else:
        # Print an error message if the request is not successful
        print(f'Failed to retrieve data from {current_url}. Status code: {response.status_code}')

# End of loop
print(f'Total number of products across all pages: {total_number_of_products}')

    

