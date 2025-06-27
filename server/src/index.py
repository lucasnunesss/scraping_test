from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_product_url(product_id, page):
    return f"https://www.amazon.com.br/s?k={product_id}&s=exact-aware-popularity-rank&page={page}&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2KED4ENTQXZPY&qid=1743884423&sprefix=ps4%2Caps%2C251"

def get_items(product_id):
    items_product = []
    url = get_product_url(product_id, 1)

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://www.amazon.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Pragma": "no-cache",
        "TE": "Trailers",
        "Upgrade-Insecure-Requests": "1"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    list_items = soup.select('[role="listitem"]')

    for item in list_items:
        title = item.select_one('[data-cy="title-recipe"] a h2 span')
        price = item.select_one('[data-cy="price-recipe"] .a-offscreen')
        image = item.select_one('.s-image')

        if title and price and image:
            items_product.append({
                "name": title.get_text(strip=True),
                "price": price.get_text(strip=True),
                "img": image['src']
            })

    return items_product

@app.route('/busca/<string:product_id>', methods=['GET'])
def search(product_id):
    try:
        data = get_items(product_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000)
