from shopify import Shopify
import utils,pandas as pd,json,requests,os,re
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

def add_alt_name_to_images():
    
    alt_data = requests.get('https://docs.google.com/spreadsheets/d/1iWzI46xmwv0WTjqKXDfthBlEd50NwVpqW-zzb25LF04/gviz/tq?tqx=out:csv&tq&')
    data = alt_data.text
    with open("data_alt.csv",mode="w") as file:
        file.write(data)
    df = pd.read_csv('data_alt.csv',encoding='cp1252')
    json_file = df[['article_id','src','alt name']].to_json(orient="records")
    data = json.loads(json_file)
    get_pages = utils.process_alt()
    pages = None
    for alt_data in data:
        pages = get_pages(alt_data)
    sh = Shopify()
    for page in pages:
        sh.update_page(page)


def save_all_products():
    countries = ['UK','EU']
    for country in countries:
        sh = Shopify(version=country)
        all_products = sh.get_all_products()
        utils.save_to_csv(all_products,f'products_data_{country}.csv')

def remove_spam_comments():
    sh = Shopify(version="UK")
    comments = sh.get_all_comments_per_blog()
    spam = list(filter(lambda x: bool(re.search('zomail|dating',x['email'])),comments))
    for s in spam:
        sh.remove_comment(s['id'])

def update_oss_products():

    sh = Shopify()
    # df = pd.read_csv('OOS notice on Shopify - data.csv')
    url = f"{os.getenv('SPREADSHEET_URL')}/gviz/tq?tqx=out:csv&tq&"
    r = requests.get(url)
    data = r.text
    with open("data.csv",mode="w") as file:
        file.write(data)
    df = pd.read_csv('data.csv',encoding='cp1252')
    json_file = df[['new_body_html','id']].to_json(orient="records")
    data = json.loads(json_file)
    for product in data:
        id = product['id']
        desc = product['new_body_html']
        sh.update_product_desc(id,desc)


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

def get_orders_ids_names():
    countries = ['UK','EU']
    for country in countries:
        sh = Shopify(version=country)
        orders = sh.get_orders()
        pairs = list(map(lambda x: {'id':x['id'],'name':x['name']},orders))
        df = pd.DataFrame(pairs).to_csv(f'{country}_ids_names.csv',index=False)

if __name__ == '__main__':
    get_orders_ids_names()
    # update_oss_products()
    # remove_spam_comments()
    # save_all_products()
    # pages()
    # delete_unfulfilled_orders()
    # answer = input("""What process do you want to run?\nInput one of the following numbers to begin one of the corresponding processes.\n-------\n
    # 1 - delete all orders\n""")
    # if answer == 1 or str(answer) == '1':
    #     delete_unfulfilled_orders()
    # else: 
    #     print("not a valid answer.")