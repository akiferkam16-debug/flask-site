from flask import Flask, session, redirect, request, render_template_string, url_for
import os

# -------------------------------------------------------------------
# 1. FLASK UYGULAMASININ TANIMLANMASI 
app = Flask(__name__) 
# SECRET_KEY, session kullanıldığı için kritik.
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

# Google doğrulama endpoint'i
@app.route('/google522b3008e358c667.html')
def google_verify():
    return "google-site-verification: google522b3008e358c667.html"

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
        <div class="products-grid">{product_html}</div>
    </div>
    <a id="dikdortgen"></a>
    <div class="products-section">
        <h2>Dikdörtgen Ürünler</h2>
        <div class="products-grid">{rectangle_html}</div>
    </div>
    <a id="havsali"></a>
    <div class="products-section">
        <h2>Halka (Havşalı) Ürünler</h2>
        <div class="products-grid">{ring_html}</div>
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
            .cart-link {{ color:#0b1a3d; text-decoration:none; font-weight:bold; padding: 8px 12px; border: 1px solid #0b1a3d; border-radius: 4px; transition: 0.2s; }}
            .cart-link:hover {{ background: #0b1a3d; color: #ffd700; }}
            main {{ flex:1; padding:20px 0; }}
            .page-layout {{ display: flex; gap: 20px; max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
            .category-sidebar {{ width: 250px; padding: 15px; background: #f4f4f4; border-radius: 8px; position: sticky; top: 20px; }}
            .category-sidebar a {{ display: block; padding: 8px 0; text-decoration: none; color: #555; font-weight: bold; }}
            .category-sidebar a:hover {{ color: #0b1a3d; }}
            .content {{ flex: 1; min-width: 0; }}
            .products-section {{ background:#0b1a3d; padding:20px; border-radius:12px; margin-top:15px; color: #fff; }}
            .products-section h2 {{ text-align:center; margin-bottom:20px; color:#ffd700; }}
            .products-grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap:20px; justify-items:center; }}
            .product-card {{ background:#222; border-radius:12px; padding:12px; width:200px; text-align:center; box-shadow:0 4px 12px rgba(0,0,0,0.5); transition: 0.3s; color:#fff; }}
            .product-card:hover {{ transform: translateY(-8px); }}
            .product-card img {{ max-width:100%; height:150px; object-fit: cover; border-radius:6px; margin-bottom:8px; }}
            .title {{ font-weight:bold; margin-bottom:4px; min-height: 40px; }}
            .price {{ color:#ffd700; margin-bottom:8px; font-size: 1.2em; }}
            .add-btn {{ background:#ffd700; color:#111; text-decoration:none; padding:8px 16px; border-radius:6px; font-weight:bold; display:inline-block; }}
            footer {{ background:#1a1a1a; text-align:center; padding:14px 0; font-size:14px; color:#bbb; margin-top: auto; }}
            @media (max-width: 768px) {{
                header {{ flex-direction: column; padding: 10px; }}
                .page-layout {{ flex-direction: column; padding: 0 10px; }}
                .category-sidebar {{ width: 100%; position: static; }}
                .products-section {{ background: none; color: #000; padding: 0; }}
                .products-section h2 {{ color: #0b1a3d; border-bottom: 2px solid #0b1a3d; text-align: left; padding-bottom: 5px; }}
                .products-grid {{ grid-template-columns: repeat(2, 1fr); gap: 10px; }}
                .product-card {{ width: 100%; background: #fff; color: #000; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                .product-card img {{ height: 100px; }}
                .price {{ color: #E60000; }}
            }}
        </style>
    </head>
    <body>
        <header>
            <a class="cart-link" href="{{ url_for('cart_page') }}">🛒 Sepeti Görüntüle</a>
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

# --- SEPET FONKSİYONLARI ---

def get_clean_cart():
    """Sepeti her zaman sözlük olarak döndüren yardımcı fonksiyon."""
    cart = session.get("cart", {})
    if not isinstance(cart, dict):
        cart = {}
    return cart

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    cart = get_clean_cart()
    str_id = str(product_id)
    
    if str_id in cart:
        cart[str_id]['quantity'] += 1
    else:
        all_prods = products + rectangle_products + ring_products
        product = next((p for p in all_prods if p["id"] == product_id), None)
        if product:
            cart[str_id] = {
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": 1
            }
    
    session["cart"] = cart
    session.modified = True
    return redirect(url_for('cart_page'))

@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = get_clean_cart()
    str_id = str(product_id)
    
    if str_id in cart:
        if cart[str_id]['quantity'] > 1:
            cart[str_id]['quantity'] -= 1
        else:
            del cart[str_id]
            
    session["cart"] = cart
    session.modified = True
    return redirect(url_for('cart_page'))

# --- Sepeti Görüntüle ---
@app.route("/cart")
def cart_page():
    cart = get_clean_cart()
    cart_items_html = ""
    grand_total = 0.0
    
    for item_id, item in cart.items():
        try:
            # Fiyatı sayıya çevir: "12.00 TL" -> 12.0
            price_val = float(item["price"].split()[0].replace(",", "."))
            subtotal = price_val * item["quantity"]
            grand_total += subtotal
        except:
            subtotal = 0.0
            
        cart_items_html += f"""
        <li class="cart-item">
            <div class="item-details">
                <span class="item-name">{item['name']}</span>
                <span class="item-price">{item['price']}</span>
            </div>
            <div class="quantity-controls">
                <a href="{url_for('remove_from_cart', product_id=item['id'])}" class="qty-btn">-</a>
                <span class="qty-num">{item['quantity']}</span>
                <a href="{url_for('add_to_cart', product_id=item['id'])}" class="qty-btn">+</a>
            </div>
            <div class="item-subtotal">{subtotal:.2f} TL</div>
        </li>
        """

    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Sepetiniz</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ background:#0b1a3d; color:#fff; font-family:Arial, sans-serif; text-align:center; padding:20px; }}
            .cart-container {{ background:#1e2a4a; padding:25px; border-radius:10px; max-width:600px; width: 95%; margin: 20px auto; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
            h1 {{ color:#ffd700; margin-top:0; }}
            ul {{ list-style:none; padding:0; margin:0; }}
            .cart-item {{ border-bottom: 1px solid #334466; padding: 15px 0; display: flex; justify-content: space-between; align-items: center; }}
            .item-details {{ text-align: left; flex: 1; }}
            .item-name {{ display: block; font-weight: bold; font-size: 1.1em; }}
            .item-price {{ color: #ffd700; font-size: 0.9em; }}
            .quantity-controls {{ display: flex; align-items: center; gap: 15px; margin: 0 20px; }}
            .qty-btn {{ background: #ffd700; color: #000; text-decoration: none; padding: 5px 12px; border-radius: 4px; font-weight: bold; }}
            .qty-num {{ font-size: 1.2em; font-weight: bold; min-width: 25px; }}
            .item-subtotal {{ font-weight: bold; color: #ffd700; width: 80px; text-align: right; }}
            .total {{ font-size:24px; font-weight:bold; margin-top:20px; padding-top: 15px; border-top: 2px solid #ffd700; color:#ffd700; text-align: right; }}
            .actions {{ margin-top: 30px; }}
            .back-btn {{ color: #fff; text-decoration: none; display: inline-block; margin-bottom: 20px; }}
            .checkout-btn {{ background:green; color:#fff; text-decoration:none; padding:15px 25px; border-radius:8px; display:block; font-size:20px; font-weight:bold; transition:0.3s; }}
            .checkout-btn:hover {{ background:darkgreen; transform:scale(1.02); }}
            @media (max-width: 480px) {{
                .cart-item {{ flex-direction: column; text-align: center; gap: 10px; }}
                .item-details {{ text-align: center; }}
                .item-subtotal {{ text-align: center; width: 100%; }}
            }}
        </style>
    </head>
    <body>
        <div class="cart-container">
            <h1>🛒 Sepetiniz</h1>
            <ul>{cart_items_html if cart_items_html else '<li>Sepetiniz şu an boş.</li>'}</ul>
            {f'<p class="total">Genel Toplam: {grand_total:.2f} TL</p>' if cart_items_html else ''}
            <div class="actions">
                <a href="/" class="back-btn">⬅️ Alışverişe Geri Dön</a>
                <a class="checkout-btn" href="#">💳 Sepeti Onayla</a>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
            
