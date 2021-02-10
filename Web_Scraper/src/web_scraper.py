import bs4
from urllib.request import urlopen as request
from bs4 import BeautifulSoup as soup
import csv

url = 'https://www.newegg.com/p/pl?d=graphics+cards'

# opening connection, grabbing the page
client = request(url)
page_html = client.read()
client.close()

# does html parsing
page_soup = soup(page_html, 'html.parser')

# grabs each product
cells = page_soup.find_all("div", attrs={"class": "item-cell"})

with open('graphics_cards.csv', mode='w', newline='') as graphics_cards_file:
    file_writer = csv.writer(graphics_cards_file)
    file_writer.writerow(['Brand', 'Product Name', 'Price', 'Shipping'])
    for cell in cells:
        # checking to see if cell is an advertisement, if
        # condition is true, then cell is not an advertisement
        # and we can execute the code below without an error
        if cell.find("div", attrs={"class": "txt-ads-link"}) == None:
            try:
                # obtaining the brand name
                brand_tag = cell.find_all("div", attrs={"class": "item-branding"})
                brand_name = brand_tag[0].img["title"]

                # obtaining the product name
                title_tag = cell.find_all("a", attrs={"class": "item-title"})
                product_name = title_tag[0].text

                # checking for promo situations (out of stock, limited time offer) 
                if cell.find_all("p", attrs={"class": "item-promo"}) != []:
                    # obtaining the price info
                    promo_tag = cell.find_all("p", attrs={"class": "item-promo"})
                    promo_info = promo_tag[0].text

                    if promo_info == "OUT OF STOCK":
                        pricing_info = promo_info
                        shipping_tag = cell.find_all("a", attrs={"class": "shipped-by-newegg"})
                        shipping_info = shipping_tag[0].text
                    else: # handles limited time offer
                        price_tag = cell.find_all("li", attrs={"class": "price-current"})
                        dollar_sign = price_tag[0].text[0]
                        dollars = price_tag[0].strong.text
                        cents = price_tag[0].sup.text

                        pricing_info = dollar_sign + dollars + cents + ', ' + promo_info

                        shipping_tag = cell.find_all("li", attrs={"class": "price-ship"})
                        shipping_info = shipping_tag[0].text
                else:
                    # obtaining the price info
                    price_tag = cell.find_all("li", attrs={"class": "price-current"})
                    dollar_sign = price_tag[0].text[0]
                    dollars = price_tag[0].strong.text
                    cents = price_tag[0].sup.text
                    pricing_info = dollar_sign + dollars + cents

                    # obtaining the shipping info
                    shipping_tag = cell.find_all("li", attrs={"class": "price-ship"})
                    shipping_info = shipping_tag[0].text
                
                file_writer.writerow([brand_name, product_name, pricing_info, shipping_info])
            except Exception as error:
                print(f'Error that occurred: {error.__class__.__name__}')
                print(f'Error message: {error}')
                print(f'Cell where error occurred: {cell}')
                print()
