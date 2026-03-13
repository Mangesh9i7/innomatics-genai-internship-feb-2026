from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

 #  Temporary data — acting as our database for now ===========================================================================
products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
{'id': 2, 'name': 'Notebook',       'price':  99,  'category': 'Stationery',  'in_stock': True },
{'id': 3, 'name': 'USB Hub',        'price': 799,  'category': 'Electronics', 'in_stock': False},
{'id': 4, 'name': 'Pen Set',        'price':  49,  'category': 'Stationery',  'in_stock': True },
{'id': 5, 'name': 'Desk Lamp',      'price': 1299, 'category': 'Electronics', 'in_stock': True },
{'id': 6, 'name': 'Stapler',        'price': 199,  'category': 'Stationery',  'in_stock': True },
{'id': 7, 'name': 'Portable Charger','price': 1599,'category': 'Electronics', 'in_stock': False },
]

feedback = []
orders = []
order_id_counter = 1


# ══ PYDANTIC MODELS ═══════════════════════════════════════════════════════════════
class OrderRequest(BaseModel):
    customer_name     :    str = Field(..., min_length=2)
    product_id        :    int = Field(..., gt=0)
    quantity          :    int = Field(..., gt=0, le=100)
    delivery_address  :    str = Field(..., min_length=10)

class CustomerFeedback(BaseModel):
    customer_name :     str = Field(..., min_length=2, max_length=100)
    product_id    :     int = Field(..., gt=0)
    rating        :     int = Field(..., ge=1, le=5)
    comment       :     Optional[str]   = Field(None, max_length=300)

class OrderItems(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int   = Field(..., gt=0)

class BulkOrder(BaseModel):
    company_name  :   str = Field(..., min_length=2)
    contact_email :   str = Field(..., min_length=5)
    items         :   List[OrderItems] = Field(..., min_items=1)

class OneOrder(BaseModel):
    product_id: int
    quantity: int

# ══ HELPER FUNCTIONS ══════════════════════════════════════════════════════════════
def filter_products_logic(category=None, min_price=None, max_price=None, in_stock=None):
    """Apply filters and return matching products."""
    result = products
    if category is not None:
        result = [p for p in result if p['category'] == category]
    if min_price is not None:
        result = [p for p in result if p['price'] >= min_price]   # ✅ min_price filter
    if max_price is not None:
        result = [p for p in result if p['price'] <= max_price]
    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
    return result

# -------------------------------------------------------------------------------
#                             DAY 1 ENDPOINTS
# -----------------------------------------------------------------------------------------------------


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
# @app.get('/products/{product_id}')
# def get_product(product_id: int):
#     for product in products:
#         if product['id'] == product_id:
#             return {'product': product}
#     return {'error': 'Product not found'}

# ---------------------------------------------------------
#                   DAY 2 PRACTICE TASKS 
# ---------------------------------------------------------

# Endpoint - Filter Products by Minimum Price
@app.get('/products/filter')
def filter_products(
    category:  str  = Query(None, description='Electronics or Stationery'),
    min_price: int  = Query(None, description='Minimum price'),
    max_price: int  = Query(None, description='Maximum price'),
    in_stock:  bool = Query(None, description='True = in stock only'),
):
    result = filter_products_logic(category, min_price, max_price, in_stock)
    return {'filtered_products': result, 'count': len(result)}

# Endpoint - Get Only the Price of a Product
@app.get("/products/{product_id}/price")
def get_price(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return{"name": product["name"], "price": product["price"]}
    return{"error": "Product not found"}

# Endpoint - POST + Pydantic- Accept Customer Feedback
@app.post("/feedback")
def product_feedback(data: CustomerFeedback):
    feedback.append(data.dict())
    return {
        "message": "Feedback Submitted",
        "feedback": data.dict(),
        "total_feedback": len(feedback)   
    }

# Endpoint - Build a Product Summary Dashboard

# When you want to see the result of this routes.
# Then Please Comment [/products/{product_id] this route .
# If not then you can't see the summery becouse of fix and variable routes. Above route is variable route and this route is fix but this is questrion in 2nd task 
#  so i can't place the variable route bellow this . Thankyou for your considaration .

@app.get("/products/summery")
def product_summary():
    in_stock   = [p for p in products if p["in_stock"]]
    out_stock  = [p for p in products if not p["in_stock"]]
    expensive  = max(products, key=lambda p: p["price"])
    cheapest   = min(products, key=lambda p: p["price"])
    categories = list(set(p["category"] for p in products))
    return {
        "total_products":     len(products),
        "in_stock_count":     len(in_stock),
        "out_of_stock_count": len(out_stock),
        "most_expensive":     {"name": expensive["name"], "price": expensive["price"]},
        "cheapest":           {"name": cheapest["name"],  "price": cheapest["price"]},
        "categories":         categories,
    }

# Endpoint -  Validate & Place a Bulk Order
@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):
    confirmed, failed, grand_total = [], [], 0
    for item in order.items:
        product = next((p for p in products if p["id"] == item.product_id), None)
        if not product:
            failed.append({"product_id": item.product_id, "reason": "Product not found"})
        elif not product["in_stock"]:
            failed.append({"product_id": item.product_id, "reason": f"{product['name']} is out of stock"})
        else:
            subtotal = product["price"] * item.quantity
            grand_total += subtotal
            confirmed.append({"product": product["name"], "qty": item.quantity, "subtotal": subtotal})
    return {"company": order.company_name, "confirmed": confirmed,
            "failed": failed, "grand_total": grand_total}

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            return order
    return {"error": "Order not found"}

@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = "confirmed"
            return {"message": "Order confirmed successfully", "order": order}
            
    return {"error": "Order not found"}

# Endpoint - ⭐ Bonus: Order Status Tracker
@app.post("/orders")
def create_order(order: OneOrder):
    global order_id_counter
    
    new_order = {
        "order_id": order_id_counter,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "pending" 
    }
    
    orders.append(new_order)
    order_id_counter += 1
    return new_order

# Endpoint — GET: Return one order by ID
@app.get("/orders/{order_id}")
def get_new_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            return order
    return {"error": "Order not found"}

# Endpoint — PATCH: Confirm an order
@app.patch("/orders/{order_id}/confirm")
def confirm_new_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = "confirmed" 
            return {"message": "Order confirmed successfully", "order": order}
    return {"error": "Order not found"}