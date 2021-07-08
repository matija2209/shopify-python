from shopify import Shopify
import utils,pandas as pd,json,requests,os
from dotenv import dotenv_values, load_dotenv
load_dotenv()

def delete_unfulfilled_orders():
    sh = Shopify()
    orders = sh.get_orders()
    print(f"deleting {len(orders)} orders\n")
    if not orders:
        return None
    for order in orders:
        if order['tags'] == 'imported':
            sh.delete_order(order['id'])


def pages():
    sh = Shopify()
    sh.get_all_pages()

def save_all_products():
    countries = ['UK','EU']
    for country in countries:
        sh = Shopify(version=country)
        all_products = sh.get_all_products()
        utils.save_to_csv(all_products,f'products_data_{country}.csv')

def update_oss_products():
    countries = ['UK','EU']
    for country in countries:
        sh = Shopify(version=country)
        # df = pd.read_csv('OOS notice on Shopify - data.csv')
        url = f"{os.getenv(f'SPREADSHEET_URL_{country}')}/gviz/tq?tqx=out:csv&tq&"
        r = requests.get(url)
        data = r.text
        with open(f"data_{country}.csv",mode="w") as file:
            file.write(data)
        df = pd.read_csv(f'data_{country}.csv')
        json_file = df[['new_body_html','id']].to_json(orient="records")
        data = json.loads(json_file)
        for product in data:
            id = product['id']
            desc = product['new_body_html']
            sh.update_product_desc(id,desc)

if __name__ == '__main__':
    update_oss_products()
    # save_all_products()
    # pages()
    # delete_unfulfilled_orders()
    # answer = input("""What process do you want to run?\nInput one of the following numbers to begin one of the corresponding processes.\n-------\n
    # 1 - delete all orders\n""")
    # if answer == 1 or str(answer) == '1':
    #     delete_unfulfilled_orders()
    # else: 
    #     print("not a valid answer.")