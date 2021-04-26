import requests, json, time, re, random, os, pandas as pd
from dotenv import dotenv_values, load_dotenv
import urllib.parse as urlparse
from urllib.parse import parse_qs
load_dotenv()


class Shopify:
    api_key = os.getenv('SHOPIFY_API_KEY')
    api_password = os.getenv('SHOPIFY_API_PW')
    shopify_domain = os.getenv('SHOPIFY_DOMAIN')
    api_version = '2021-04'
    base_url = f"https://{api_key}:{api_password}@{shopify_domain}.myshopify.com/admin/api/{api_version}/"

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'limit': "250"
        }

    def get_all_products(self):
        api_endpoint = "products.json"
        r = requests.get(url=self.base_url + api_endpoint,
                         headers=self.headers)
        data = r.json()
        return data['products']

    def get_all_variants(self, product_id):
        api_endpoint = f"products/{product_id}/variants.json"
        r = requests.get(url=self.base_url + api_endpoint,
                         headers=self.headers)
        data = r.json()
        return data['variants']

    def update_variant_price(self, variant_id, new_price):
        api_endpoint = f"variants/{variant_id}.json"
        data = {
            "variant": {
                "id": int(variant_id),
                "price": new_price
            }
        }
        r = requests.put(url=self.base_url + api_endpoint,
                         data=json.dumps(data), headers=self.headers)
        return r.status_code

    # https://shopify.dev/docs/admin-api/rest/reference/orders/order#index-2021-04
    def get_orders(self):
        api_endpoint = f"orders.json"
        params = {
            'status' : 'any'
        }
        orders = list()
        r = requests.get(url=self.base_url + api_endpoint,headers=self.headers,params=params)
        if not r.links:
            return orders
        next_url = r.links["next"]["url"]
        orders.append(r.json()['orders'])

        parsed = urlparse.urlparse(next_url)
        page_about = parse_qs(parsed.query)['page_info']

        while True:
            params = {'page_info' : page_about[0]}
            
            r = requests.get(url=self.base_url + api_endpoint,headers=self.headers,params=params)

            if r.status_code == 200:
                orders.append(r.json()['orders'])
            else:
                raise Exception("not rerieved")
            try:
                next_url = r.links["next"]["url"]
            except:
                break
        return [x for x in orders for x in x]


    def delete_order(self,sh_order_id):
        api_endpoint = f"orders/{sh_order_id}.json"
        r = requests.delete(url=self.base_url + api_endpoint,headers=self.headers)
        if r.status_code == 200:
            print(f"{sh_order_id} deleted...")
            return True
        elif r.status_code == 422:
            print("order cannot be deleted. Not allowed by Shopify ",sh_order_id )
        else:
            raise Exception("not deleted")

# products = sh.get_all_products()
# products_variants = list()
# for product in products:
#     product_variants = sh.get_all_variants(product["id"])
#     [products_variants.append(variant) for variant in product_variants]

# pd.DataFrame(products_variants).to_csv("products_variants.csv")

# new_prices = pd.read_csv('new_prices.csv', converters={i: str for i in range(0, 100)})
# for new_price in new_prices.iterrows():
#     variant_id = new_price[1]['variant_id']
#     price = new_price[1]['new_price']
#     sh.update_variant_price(variant_id,price)
