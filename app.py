from flask import Flask, session, redirect, request, render_template_string, url_for
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "CokUzunVeGuvensizVarsayilanAnahtar12345")

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

# Tüm ürünlerin tek listede birleşimi (Arama kolaylığı için)
all_products = products + rectangle_products + ring_products

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

    return render_template_string(f"""
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Erkam Mıknatıs</title>
        <style>
            body {{ margin:0; font-family: Arial, sans-serif; background:#fff; color:#000; display:flex; flex-direction:column; min-height:100vh; }}
            header {{ display:flex; justify-content:space-between; align-items:center; padding:10px 20px; background:#f8f8f8; border-bottom: 1px solid #eee; }}
            .logo h1 {{ margin:0; font-size:28px; color:#0b1a3d; }}
            .cart-link {{ color:#0b1a3d; text-decoration:none; font-weight:bold; padding: 8px 12px; border: 1px solid #0b1a3d; border-radius: 4px; }}
            .page-layout {{ display: flex; gap: 20px; max-width: 1200px; margin: 20px auto; padding: 0 20px; }}
            .category-sidebar {{ width: 250px; padding: 15px; background: #f4f4f4; border-radius: 8px; position: sticky; top: 20px; }}
            .category-sidebar a {{ display: block; padding: 8px 0; text-decoration: none; color: #555; font-weight: bold; }}
            .products-section {{ background:#0b1a3d; padding:20px; border-radius:12px; margin-bottom:20px; color: #fff; }}
            .products-grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap:20px; }}
            .product-card {{ background:#222; border-radius:12px; padding:12px; text-align:center; color:#fff; }}
            .product-card img {{ width:100%; height:150px; object-fit: cover; border-radius:6px; }}
            .price {{ color:#ffd700; font-size: 1.2em; margin: 10px 0; }}
            .add-btn {{ background:#ffd700; color:#111; text-decoration:none; padding:8px 16px; border-radius:6px; font-weight:bold; }}
            @media (max-width: 768px) {{
                .page-layout {{ flex-direction: column; }}
                .category-sidebar {{ width: 100%; position: static; }}
                .products-grid {{ grid-template-columns: repeat(2, 1fr); }}
            }}
        </style>
    </head>
    <body>
        <header>
            <a class="cart-link" href="{url_for('cart_page')}">🛒 Sepeti Görüntüle</a>
            <div class="logo"><h1>Erkam Mıknatıs</h1></div>
            <div style="width:100px;"></div>
        </header>
        <main class="page-layout">
            <aside class="category-sidebar">
                <h3>Kategoriler</h3>
                <a href="#yuvarlak">Yuvarlak</a>
                <a href="#dikdortgen">Dikdörtgen</a>
                <a href="#havsali">Halka (Havşalı)</a>
            </aside>
            <div class="content">
                <section id="yuvarlak" class="products-section">
                    <h2>Yuvarlak Ürünler</h2>
                    <div class="products-grid">{product_html}</div>
                </section>
                <section id="dikdortgen" class="products-section">
                    <h2>Dikdörtgen Ürünler</h2>
                    <div class="products-grid">{rectangle_html}</div>
                </section>
                <section id="havsali" class="products-section">
                    <h2>Halka (Havşalı) Ürünler</h2>
                    <div class="products-grid">{ring_html}</div>
                </section>
            </div>
        </main>
    </body>
    </html>
    """)

# --- Sepet Mantığı (Güncellendi) ---
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
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
    cart_items_html = ""
    total_price = 0.0

    for pid, quantity in cart.items():
        product = next((p for p in all_products if str(p["id"]) == pid), None)
        if product:
            price_val = float(product["price"].replace(" TL", "").replace(",", "."))
            item_total = price_val * quantity
            total_price += item_total
            cart_items_html += f"""
            <li class="cart-item">
                <div class="item-name">{product['name']}</div>
                <div class="qty-controls">
                    <a href="{url_for('update_cart', product_id=product['id'], action='decrease')}" class="qty-btn">-</a>
                    <span class="qty-text">{quantity} Adet</span>
                    <a href="{url_for('update_cart', product_id=product['id'], action='increase')}" class="qty-btn">+</a>
                </div>
                <div class="item-subtotal">{item_total:.2f} TL</div>
                <a href="{url_for('remove_from_cart', product_id=product['id'])}" class="remove-link">❌</a>
            </li>
            """

    return render_template_string(f"""
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sepetiniz</title>
        <style>
            body {{ background:#0b1a3d; color:#fff; font-family:Arial, sans-serif; padding:20px; }}
            .cart-container {{ background:#1e2a4a; padding:20px; border-radius:10px; max-width:600px; margin:auto; }}
            h1 {{ color:#ffd700; text-align:center; }}
            ul {{ list-style:none; padding:0; }}
            .cart-item {{ display:flex; justify-content:space-between; align-items:center; padding:15px 0; border-bottom:1px solid #334466; gap:10px; }}
            .item-name {{ flex:2; text-align:left; }}
            .qty-controls {{ flex:1; display:flex; align-items:center; gap:10px; }}
            .qty-btn {{ background:#ffd700; color:#000; text-decoration:none; padding:2px 8px; border-radius:4px; font-weight:bold; }}
            .item-subtotal {{ flex:1; text-align:right; font-weight:bold; color:#ffd700; }}
            .remove-link {{ text-decoration:none; }}
            .total-section {{ text-align:center; margin-top:20px; font-size:24px; color:#ffd700; border-top:2px solid #ffd700; padding-top:10px; }}
            .back-btn {{ display:block; text-align:center; margin-top:20px; color:#fff; text-decoration:none; opacity:0.8; }}
            @media (max-width: 480px) {{
                .cart-item {{ flex-direction: column; text-align: center; }}
                .item-name {{ text-align:center; }}
            }}
        </style>
    </head>
    <body>
        <div class="cart-container">
            <h1>🛒 Sepetiniz</h1>
            <ul>
                {cart_items_html if cart_items_html else "<p style='text-align:center;'>Sepetiniz boş.</p>"}
            </ul>
            {f'<div class="total-section">Toplam: {total_price:.2f} TL</div>' if cart else ""}
            <a href="/" class="back-btn">⬅️ Alışverişe Devam Et</a>
            {f'<button style="width:100%; padding:15px; margin-top:20px; background:green; color:white; border:none; border-radius:8px; font-size:18px; cursor:pointer;">Siparişi Onayla</button>' if cart else ""}
        </div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(debug=True)
