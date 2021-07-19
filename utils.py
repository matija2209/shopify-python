import pandas as pd
from bs4 import BeautifulSoup
from shopify import Shopify


def save_to_csv(data,name):
    pd.DataFrame(data).to_csv(name)

def process_alt():
    sh = Shopify()
    pages = sh.get_all_pages()
    
    def whola(alt_data):
        id = alt_data['article_id']
        src = alt_data['src']
        alt = alt_data['alt name']
        matched_data = list(filter(lambda x: x['id']==id,pages))
        page_html = matched_data[0]['body_html']
        soup = BeautifulSoup(page_html)
        imgs = soup.find_all('img')

        for img in imgs:
            if not img['src'] == src:
                continue
            img['alt'] = alt
        for page in pages:
            if not page['id'] == id:
                continue
            page['body_html'] = str(soup)
        return pages
    return whola
