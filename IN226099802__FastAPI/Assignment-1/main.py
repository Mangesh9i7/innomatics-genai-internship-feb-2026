from fastapi import FastAPI, Query
app = FastAPI()

 #  Temporary data — acting as our database for now 
products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
{'id': 2, 'name': 'Notebook',       'price':  99,  'category': 'Stationery',  'in_stock': True },
{'id': 3, 'name': 'USB Hub',        'price': 799,  'category': 'Electronics', 'in_stock': False},
{'id': 4, 'name': 'Pen Set',        'price':  49,  'category': 'Stationery',  'in_stock': True },
{'id': 5, 'name': 'Desk Lamp',      'price': 1299, 'category': 'Electronics', 'in_stock': True },
{'id': 6, 'name': 'Stapler',        'price': 199,  'category': 'Stationery',  'in_stock': True },
{'id': 7, 'name': 'Portable Charger','price': 1599,'category': 'Electronics', 'in_stock': False },
]

 #  Endpoint — Home 
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}

 #  Endpoint — Return all products 
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

@app.get('/products/filter')
def filter_products(
    category:  str  = Query(None, description='Electronics or Stationery'),
    max_price: int  = Query(None, description='Maximum price'),
    in_stock:  bool = Query(None, description='True = in stock only')
):
    
    result = products          # start with all products

    if category:
        result = [p for p in result if p['category'] == category]
    if max_price:
        result = [p for p in result if p['price'] <= max_price]
    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
    return {'filtered_products': result, 'count': len(result)}

# Endpoint  - Return product thhat are in stock
@app.get("/products/instock")
def get_in_stock():
    list = [p for p in products if p["in_stock"]]
    return {"in_stock_products": list, "count": len(list)}

# Endpoint - Return the summery of E-commerce store
@app.get("/store/summary")
def app_summary():
    in_stock_count = len([p for p in products if p["in_stock"]])
    out_of_stock_count = len(products) - in_stock_count
    categories = list(set([p['category'] for p in products]))
    return {
        "store_name": "E-commerce Store", "total_products": len(products), "in_stock": in_stock_count, "out_of_stock": out_of_stock_count,"categories": categories
    }
# Endpoint  — Return product by its category
@app.get('/products/category/{product_category}')
def get_product(product_category: str):
    list = [p for p in products if p['category'] == product_category]
    if list:
        return {"products": list, "count": len(list)}
    return {"error": "No products found in this category"}

# Endpoint - search product by keyword
@app.get("/products/search/{keyword}")
def search_product(keyword: str):
    matches = [p for p in products if keyword.lower() in p["name"].lower()]
    if matches:
        return {
          "keyword": keyword, "results": matches, "total_matches": len(matches)
        }
    else:
        return{"message": "No products matched your search"}
    
# Endpoint - Show Cheapest & Most Expensive Product    
@app.get("/products/deals")
def get_deals():
    lowest_priced_item = min(products, key=lambda p: p["price"])
    highest_priced_item = max(products, key=lambda p: p["price"])
    return {
        "best_deal": lowest_priced_item,
        "premium_pick": highest_priced_item
    }    

# Endpoint  — Return one product by its ID 
@app.get('/products/{product_id}')
def get_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return {'product': product}
    return {'error': 'Product not found'}