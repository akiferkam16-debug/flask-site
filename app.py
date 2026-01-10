from flask import Flask, session, redirect, request, render_template_string, url_for
import os

app = Flask(__name__) 
app.secret_key = os.environ.get("SECRET_KEY", "Erkam_Miknatis_Guvenli_Anahtar_2024") 

# --- Ürün Veri Bankası ---
products = [
    {"id": 1, "name": "4x2 mm Yuvarlak", "file": "1.jpg", "price": "3.00 TL"},
    {"id": 2, "name": "8x3 mm Yuvarlak", "file": "2.jpg", "price": "6.00 TL"},
    {"id": 3, "name": "15x3 mm Yuvarlak", "file": "3.jpg", "price": "12.00 TL"},
    {"id": 4, "name": "10x5 mm Yuvarlak", "file": "10x5 12 tl.jpg", "price": "12.00 TL"},
    {"id": 5, "name": "18x2 mm Yuvarlak", "file": "7.jpg", "price": "14.00 TL"},
    {"id": 6, "name": "40x5 mm Yuvarlak", "file": "6.jpg", "price": "170.00 TL"},
]
rectangle_products = [
    {"id": 101, "name": "10x5x2 mm Dikdörtgen", "file": "4.jpg", "price": "6.00 TL"},
    {"id": 102, "name": "20x10x5 mm Dikdörtgen", "file": "20x10x5.jpg", "price": "9.00 TL"},
    {"id": 103, "name": "30x10x5 mm Dikdörtgen", "file": "30x10x5 77tl.jpg", "price": "11.00 TL"},
    {"id": 104, "name": "15x15x5 mm Dikdörtgen", "file": "15x15x5.jpg", "price": "14.00 TL"},
]
ring_products = [
    {"id": 201, "name": "10x5 mm - 6/3 Havşa", "file": "havşa.jpg", "price": "23.00 TL"},
    {"id": 202, "name": "12x5 mm 8x4 - 8/4 Havşa", "file": "havşa2.jpg", "price": "25.00 TL"},
]

# --- Sepet Güvenlik Kontrolü ---
def get_cart():
    cart = session.get("cart", {})
    if not isinstance(cart, dict):
        cart = {}
    return cart

# --- Ana Sayfa ---
@app.route("/")
def index():
    def create_product_html(prod_list):
        html = ""
        for p in prod_list:
            html += f"""
            <div class="product-card">
                <img src="/static/{p['file']}" alt="{p['name']}">
                <div class="title">{p['name']}</div>
                <div class="price">{p['price']}</div>
                <a class="add-btn" href="/add_to_cart/{p['id']}">Sepete Ekle</a>
            </div>
            """
        return html
    
    all_content = f"""
    <a id="yuvarlak"></a>
    <div class="products-section"><h2>Yuvarlak Ürünler</h2><div class="products-grid">{create_product_html(products)}</div></div>
    <a id="dikdortgen"></a>
    <div class="products-section"><h2>Dikdörtgen Ürünler</h2><div class="products-grid">{create_product_html(rectangle_products)}</div></div>
    <a id="havsali"></a>
    <div class="products-section"><h2>Halka (Havşalı) Ürünler</h2><div class="products-grid">{create_product_html(ring_products)}</div></div>
    """

    return render_template_string(f"""
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Erkam Mıknatıs</title>
        <style>
            body {{ margin:0; font-family: 'Segoe UI', Arial, sans-serif; background:#f4f4f4; }}
            header {{ display:flex; justify-content:space-between; align-items:center; padding:15px 30px; background:#fff; border-bottom: 3px solid #0b1a3d; position: sticky; top:0; z-index:100; }}
            .logo h1 {{ color:#0b1a3d; margin:0; font-size: 24px; }}
            .cart-link {{ color:#fff; background:#0b1a3d; text-decoration:none; font-weight:bold; padding:10px 20px; border-radius:30px; transition: 0.3s; }}
            .cart-link:hover {{ background:#ffd700; color:#0b1a3d; }}
            
            .page-layout {{ display: flex; gap: 20px; max-width: 1200px; margin: 20px auto; padding: 0 20px; }}
            .category-sidebar {{ width: 220px; background:#fff; padding:20px; border-radius:12px; height: fit-content; border: 1px solid #ddd; position: sticky; top: 90px; }}
            .category-sidebar a {{ display:block; padding:10px 0; text-decoration:none; color:#0b1a3d; font-weight:bold; border-bottom:1px solid #eee; }}
            
            .products-section {{ background:#0b1a3d; padding:25px; border-radius:15px; margin-bottom:30px; color:#fff; }}
            
            /* ÜRÜN DİZİLİMİ - 3'LÜ VE YAN YANA */
            .products-grid {{ 
                display: grid; 
                grid-template-columns: repeat(3, 1fr); /* BURASI 3'LÜ YAPAR */
                gap: 20px; 
            }}
            
            .product-card {{ background:#fff; padding:15px; border-radius:12px; text-align:center; color:#000; transition: 0.3s; }}
            .product-card:hover {{ transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }}
            .product-card img {{ width:100%; height:150px; object-fit:cover; border-radius:8px; }}
            .title {{ font-weight: bold; margin: 10px 0; height: 40px; overflow: hidden; }}
            .price {{ color: #e67e22; font-size: 1.1em; font-weight: bold; }}
            .add-btn {{ background:#0b1a3d; color:#fff; text-decoration:none; padding:10px; border-radius:6px; display:block; margin-top:10px; font-weight:bold; }}
            .add-btn:hover {{ background:#ffd700; color:#0b1a3d; }}

            @media (max-width:992px) {{ .products-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
            @media (max-width:768px) {{ .page-layout {{ flex-direction:column; }} .category-sidebar {{ width: 100%; position:static; }} .products-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
        </style>
    </head>
    <body>
        <header>
            <a class="cart-link" href="/cart">🛒 Sepetim</a>
            <div class="logo"><h1>Erkam Mıknatıs</h1></div>
            <div style="width:100px;"></div>
        </header>
        <div class="page-layout">
            <aside class="category-sidebar">
                <a href="#yuvarlak">🔵 Yuvarlak</a>
                <a href="#dikdortgen">⬛ Dikdörtgen</a>
                <a href="#havsali">⭕ Halka</a>
            </aside>
            <main style="flex:1;">{all_content}</main>
        </div>
    </body>
    </html>
    """)

# --- Sepet Fonksiyonları ---
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    cart = get_cart()
    str_id = str(product_id)
    if str_id in cart:
        cart[str_id]['quantity'] += 1
    else:
        all_prods = products + rectangle_products + ring_products
        p = next((item for item in all_prods if item["id"] == product_id), None)
        if p:
            cart[str_id] = {"id": p["id"], "name": p["name"], "price": p["price"], "quantity": 1}
    session["cart"] = cart
    session.modified = True
    return redirect("/cart")

@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = get_cart()
    str_id = str(product_id)
    if str_id in cart:
        if cart[str_id]['quantity'] > 1:
            cart[str_id]['quantity'] -= 1
        else:
            del cart[str_id]
    session["cart"] = cart
    session.modified = True
    return redirect("/cart")

@app.route("/cart")
def cart_page():
    cart = get_cart()
    items_html = ""
    total = 0.0
    for k, v in cart.items():
        price = float(v["price"].split()[0].replace(",", "."))
        sub = price * v["quantity"]
        total += sub
        items_html += f"""
        <div style="display:flex; justify-content:space-between; border-bottom:1px solid #eee; padding:15px 0; align-items:center;">
            <div style="flex:2;">
                <span style="font-weight:bold; color:#0b1a3d;">{v['name']}</span>
            </div>
            <div style="flex:1; display:flex; align-items:center; justify-content:center; gap:10px;">
                <a href="/remove_from_cart/{v['id']}" style="background:#f0f2f5; color:#000; padding:5px 10px; text-decoration:none; border-radius:4px; font-weight:bold;">-</a>
                <strong>{v['quantity']}</strong>
                <a href="/add_to_cart/{v['id']}" style="background:#f0f2f5; color:#000; padding:5px 10px; text-decoration:none; border-radius:4px; font-weight:bold;">+</a>
            </div>
            <div style="flex:1; text-align:right; font-weight:bold;">{sub:.2f} TL</div>
        </div>"""

    return render_template_string(f"""
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ background:#f0f2f5; font-family: sans-serif; padding:20px; }}
            .cart-box {{ max-width:600px; margin:auto; background:#fff; padding:30px; border-radius:15px; box-shadow:0 10px 25px rgba(0,0,0,0.1); }}
            h1 {{ border-bottom:2px solid #0b1a3d; padding-bottom:10px; color:#0b1a3d; }}
            .back-link {{ 
                display:inline-block; margin-top:20px; color:#0b1a3d; text-decoration:none; 
                font-weight:bold; padding:10px 15px; border:2px solid #0b1a3d; border-radius:8px; transition: 0.3s;
            }}
            .back-link:hover {{ background:#0b1a3d; color:#fff; }}
            .checkout-btn {{ display:block; background:#28a745; color:#fff; text-align:center; padding:15px; border-radius:8px; text-decoration:none; margin-top:20px; font-weight:bold; }}
        </style>
    </head>
    <body>
        <div class="cart-box">
            <h1>🛒 Sepetiniz</h1>
            {items_html if items_html else "<p>Sepetiniz boş.</p>"}
            <h2 style="text-align:right; color:#0b1a3d;">Toplam: {total:.2f} TL</h2>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <a href="/" class="back-link">⬅️ Alışverişe Geri Dön</a>
                <a href="#" class="checkout-btn">Tamamla</a>
            </div>
        </div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(debug=True)
    
