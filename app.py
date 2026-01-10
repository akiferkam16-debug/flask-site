from flask import Flask, session, redirect, request, render_template_string, url_for
import os

# -------------------------------------------------------------------
# 1. FLASK UYGULAMASININ TANIMLANMASI 
app = Flask(__name__) 
app.secret_key = os.environ.get("SECRET_KEY", "CokUzunVeGuvensizVarsayilanAnahtar12345") 
# -------------------------------------------------------------------

# --- Ürün Verileri ---
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

# Arama için tüm ürünler
all_products_list = products + rectangle_products + ring_products

# --- Ana Sayfa Route'u ---
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
                <a class="add-btn" href="{url_for('add_to_cart', product_id=p['id'])}">Sepete Ekle</a>
            </div>
            """
        return html
    
    product_html = create_product_html(products)
    rectangle_html = create_product_html(rectangle_products)
    ring_html = create_product_html(ring_products)

    all_products_content = f"""
    <a id="yuvarlak"></a>
    <div class="products-section">
        <h2>Yuvarlak Ürünler</h2>
        <div class="products-grid"> {product_html} </div>
    </div>
    <a id="dikdortgen"></a>
    <div class="products-section">
        <h2>Dikdörtgen Ürünler</h2>
        <div class="products-grid"> {rectangle_html} </div>
    </div>
    <a id="havsali"></a>
    <div class="products-section">
        <h2>Halka (Havşalı) Ürünler</h2>
        <div class="products-grid"> {ring_html} </div>
    </div>
    """

    return render_template_string(f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Erkam Mıknatıs</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ margin:0; font-family: Arial, sans-serif; background:#fff; color:#000; display:flex; flex-direction:column; min-height:100vh; }}
            header {{ display:flex; justify-content:space-between; align-items:center; padding:10px 20px; background:#f8f8f8; border-bottom: 1px solid #eee; }}
            .logo {{ text-align:center; flex:1; }}
            .logo h1 {{ margin:5px 0 0 0; font-size:28px; color:#0b1a3d; }}
            .cart-link {{ color:#0b1a3d; text-decoration:none; font-weight:bold; padding: 8px 12px; border: 1px solid #0b1a3d; border-radius: 4px; transition: all 0.2s; }}
            .cart-link:hover {{ background: #0b1a3d; color: #ffd700; }}
            main {{ flex:1; padding:20px 0; }}
            .page-layout {{ display: flex; gap: 20px; max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
            .category-sidebar {{ width: 250px; padding: 15px; background: #f4f4f4; border-radius: 8px; position: sticky; top: 20px; }}
            .category-sidebar a {{ display: block; padding: 8px 0; text-decoration: none; color: #555; font-weight: bold; }}
            .category-sidebar a:hover {{ color: #ffd700; background: #0b1a3d; padding-left: 10px; border-radius: 4px; }}
            .products-section {{ background:#0b1a3d; padding:20px; border-radius:12px; margin-top:15px; color: #fff; }}
            .products-section h2 {{ text-align:center; margin-bottom:20px; color:#ffd700; }}
            .products-grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap:20px; justify-items:center; }}
            .product-card {{ background:#222; border-radius:12px; padding:12px; width:200px; text-align:center; transition: transform 0.3s; color:#fff; }}
            .product-card img {{ max-width:100%; height:150px; object-fit: cover; border-radius:6px; margin-bottom:8px; }}
            .title {{ font-weight:bold; margin-bottom:4px; }}
            .price {{ color:#ffd700; margin-bottom:8px; font-size: 1.2em; }}
            .add-btn {{ background:#ffd700; color:#111; text-decoration:none; padding:8px 16px; border-radius:6px; font-weight:bold; display:inline-block; }}
            footer {{ background:#1a1a1a; text-align:center; padding:14px 0; color:#bbb; margin-top: auto; }}
            
            @media (max-width: 768px) {{
                header {{ flex-direction: column; }}
                .page-layout {{ flex-direction: column; padding: 0 10px; }}
                .category-sidebar {{ width: 100%; position: static; text-align: right; }}
                .products-section {{ background: none; color: #000; }}
                .products-section h2 {{ color: #0b1a3d; text-align: left; border-bottom: 2px solid #0b1a3d; }}
                .products-grid {{ grid-template-columns: repeat(2, 1fr); gap: 10px; }}
                .product-card {{ width: 100%; background: #fff; color: #000; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                .product-card img {{ height: 100px; }}
                .price {{ color: #E60000; }}
            }}
        </style>
    </head>
    <body>
        <header>
            <a class="cart-link" href="{url_for('cart_page')}">🛒 Sepeti Görüntüle</a>
            <div class="logo"><h1>Erkam Mıknatıs</h1></div>
            <div style="width:100px;"></div>
        </header>
        <main>
            <div class="page-layout">
                <aside class="category-sidebar">
                    <h3>Kategoriler</h3>
                    <a href="#yuvarlak">Yuvarlak Ürünler</a>
                    <a href="#dikdortgen">Dikdörtgen Ürünler</a>
                    <a href="#havsali">Halka (Havşalı) Ürünler</a>
                </aside>
                <div class="content">{all_products_content}</div>
            </div>
        </main>
        <footer>&copy; 2025 Erkam Mıknatıs. Tüm hakları saklıdır.</footer>
    </body>
    </html>
    """)

# --- YENİ SEPET MANTIĞI ---

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    # Sepeti sözlük olarak tut: {"id": miktar}
    cart = session.get("cart", {})
    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + 1
    session["cart"] = cart
    return redirect(url_for('cart_page'))

@app.route("/update_cart/<int:product_id>/<action>")
def update_cart(product_id, action):
    cart = session.get("cart", {})
    pid = str(product_id)
    if pid in cart:
        if action == "increase":
            cart[pid] += 1
        elif action == "decrease":
            cart[pid] -= 1
            if cart[pid] <= 0:
                cart.pop(pid)
    session["cart"] = cart
    return redirect(url_for('cart_page'))

@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart
    return redirect(url_for('cart_page'))

@app.route("/cart")
def cart_page():
    cart = session.get("cart", {})
    cart_html = ""
    total = 0.0
    
    for pid, quantity in cart.items():
        product = next((p for p in all_products_list if str(p["id"]) == pid), None)
        if product:
            try:
                price_float = float(product["price"].replace(" TL", "").replace(",", "."))
                item_total = price_float * quantity
                total += item_total
                
                cart_html += f"""
                <li class="cart-item">
                    <div class="item-info">
                        <span class="item-name">{product['name']}</span>
                        <span class="item-price">{product['price']}</span>
                    </div>
                    <div class="qty-controls">
                        <a href="{url_for('update_cart', product_id=product['id'], action='decrease')}" class="qty-btn">-</a>
                        <span class="qty-val">{quantity} Adet</span>
                        <a href="{url_for('update_cart', product_id=product['id'], action='increase')}" class="qty-btn">+</a>
                    </div>
                    <div class="item-subtotal">{item_total:.2f} TL</div>
                    <a href='{url_for('remove_from_cart', product_id=product['id'])}' class="remove-btn">❌</a>
                </li>
                """
            except: continue

    return render_template_string(f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Sepetiniz</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ background:#0b1a3d; color:#fff; font-family:Arial, sans-serif; text-align:center; padding:20px; min-height:100vh; }}
            .cart-container {{ background:#1e2a4a; padding:25px; border-radius:10px; max-width:650px; width: 95%; margin: 20px auto; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
            h1 {{ color:#ffd700; }}
            ul {{ list-style:none; padding:0; }}
            .cart-item {{ display:flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid #334466; gap: 10px; }}
            .item-info {{ flex: 2; text-align: left; }}
            .qty-controls {{ flex: 1.5; display: flex; align-items: center; justify-content: center; gap: 8px; background: #2c3e50; padding: 5px; border-radius: 5px; }}
            .qty-btn {{ color: #ffd700; text-decoration: none; font-weight: bold; font-size: 18px; width: 25px; }}
            .item-subtotal {{ flex: 1.5; text-align: right; color: #ffd700; font-weight: bold; }}
            .remove-btn {{ color:red; text-decoration:none; margin-left: 10px; }}
            .total {{ font-size:24px; font-weight:bold; margin-top:20px; color:#ffd700; border-top: 2px solid #ffd700; padding-top:15px; }}
            .checkout-btn {{ background:green; color:#fff; padding:12px; border-radius:8px; text-decoration:none; display:inline-block; width:100%; margin-top:20px; font-weight:bold; }}
            @media (max-width: 480px) {{
                .cart-item {{ flex-direction: column; }}
                .qty-controls {{ margin: 10px 0; }}
            }}
        </style>
    </head>
    <body>
        <div class="cart-container">
            <h1>🛒 Sepetiniz</h1>
            <ul>{cart_html if cart_html else '<li>Sepetiniz boş.</li>'}</ul>
            <p class="total">Toplam: {total:.2f} TL</p>
            <div class="actions">
                <a href="/" style="color:#fff; text-decoration:none; display:block; margin-bottom:10px;">⬅️ Alışverişe Geri Dön</a>
                <a class="checkout-btn" href="#">💳 Sepeti Onayla</a>
            </div>
        </div>
    </body>
    </html>
    """)

if __name__=="__main__":
    app.run(debug=True)
