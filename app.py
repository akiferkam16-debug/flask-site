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

all_products_list = products + rectangle_products + ring_products

# --- Ortak Stil ve Header Fonksiyonu ---
def get_header_html():
    return """
    <header>
        <div class="nav-controls">
            <a class="nav-btn contact-btn" href="/iletisim">📞 İletişim</a>
            <a class="nav-btn cart-btn" href="/cart">🛒 Sepetim</a>
            <form action="/search" method="GET" class="search-form">
                <input type="text" name="q" placeholder="Ürün ara..." required>
                <button type="submit">🔍</button>
            </form>
        </div>
        <div class="logo"><a href="/" style="text-decoration:none;"><h1>Erkam Mıknatıs</h1></a></div>
        <div style="width:100px;" class="desktop-spacer"></div>
    </header>
    """

def get_common_styles():
    return """
    body { margin:0; font-family: 'Segoe UI', Arial, sans-serif; background:#f4f4f4; color: #333; }
    header { display:flex; justify-content:space-between; align-items:center; padding:15px 30px; background:#fff; border-bottom: 3px solid #0b1a3d; position: sticky; top:0; z-index:1000; }
    .nav-controls { display:flex; gap:10px; align-items:center; }
    .search-form { display:flex; margin-left:10px; }
    .search-form input { padding:8px 12px; border:1px solid #ddd; border-radius:20px 0 0 20px; outline:none; width:150px; }
    .search-form button { padding:8px 15px; border:none; background:#0b1a3d; color:white; border-radius:0 20px 20px 0; cursor:pointer; }
    .logo h1 { color:#0b1a3d; margin:0; font-size: 24px; }
    .nav-btn { text-decoration:none; font-weight:bold; padding:10px 20px; border-radius:30px; transition: 0.3s; color:#fff; font-size: 14px; }
    .contact-btn { background:#27ae60; }
    .cart-btn { background:#0b1a3d; }
    .cart-btn:hover { background:#ffd700; color:#0b1a3d; }
    
    .products-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px; }
    .product-card { background:#fff; padding:15px; border-radius:12px; text-align:center; transition: 0.3s; border: 1px solid #eee; }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    .product-card img { width:100%; height:160px; object-fit:cover; border-radius:8px; }
    .title { font-weight: bold; margin: 10px 0; height: 40px; overflow: hidden; color:#0b1a3d; }
    .price { color: #e67e22; font-size: 1.1em; font-weight: bold; margin-bottom:10px; }
    .add-btn { background:#0b1a3d; color:#fff; text-decoration:none; padding:10px; border-radius:6px; display:block; font-weight:bold; }
    .add-btn:hover { background:#ffd700; color:#0b1a3d; }

    @media (max-width:768px) { 
        header { flex-direction: column; padding: 10px; }
        .nav-controls { width: 100%; justify-content: center; flex-wrap: wrap; }
        .search-form input { width: 100px; }
        .desktop-spacer { display:none; }
    }
    """

# --- Yardımcı Fonksiyonlar ---
def get_cart():
    cart = session.get("cart", {})
    return cart if isinstance(cart, dict) else {}

def render_products(prod_list):
    if not prod_list:
        return "<p style='color:black;'>Ürün bulunamadı.</p>"
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

# --- Route'lar ---

@app.route("/")
def index():
    all_content = f"""
    <div id="yuvarlak" class="products-section">
        <h2 style="background:#0b1a3d; color:white; padding:10px; border-radius:8px;">Yuvarlak Ürünler</h2>
        <div class="products-grid">{render_products(products)}</div>
    </div>
    <div id="dikdortgen" class="products-section" style="margin-top:40px;">
        <h2 style="background:#0b1a3d; color:white; padding:10px; border-radius:8px;">Dikdörtgen Ürünler</h2>
        <div class="products-grid">{render_products(rectangle_products)}</div>
    </div>
    <div id="havsali" class="products-section" style="margin-top:40px;">
        <h2 style="background:#0b1a3d; color:white; padding:10px; border-radius:8px;">Halka (Havşalı) Ürünler</h2>
        <div class="products-grid">{render_products(ring_products)}</div>
    </div>
    """
    return render_template_string(f"""
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Erkam Mıknatıs - Ana Sayfa</title>
        <style>{get_common_styles()}</style>
    </head>
    <body>
        {get_header_html()}
        <div style="max-width:1200px; margin:20px auto; padding:0 20px;">
            {all_content}
        </div>
    </body>
    </html>
    """)

@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    filtered = [p for p in all_products_list if query in p['name'].lower()]
    return render_template_string(f"""
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Arama: {query}</title>
        <style>{get_common_styles()}</style>
    </head>
    <body>
        {get_header_html()}
        <div style="max-width:1200px; margin:20px auto; padding:0 20px;">
            <h2>"{query}" için arama sonuçları ({len(filtered)})</h2>
            <div class="products-grid">{render_products(filtered)}</div>
            <br><a href="/" style="color:#0b1a3d; font-weight:bold;">⬅️ Tüm Ürünlere Dön</a>
        </div>
    </body>
    </html>
    """)

@app.route("/iletisim")
def contact():
    return render_template_string(f"""
    <html>
    <head>
        <meta charset="utf-8"><title>İletişim</title>
        <style>
            {get_common_styles()}
            .contact-box {{ max-width:500px; margin:50px auto; background:#fff; padding:30px; border-radius:15px; text-align:center; box-shadow:0 5px 15px rgba(0,0,0,0.1); }}
        </style>
    </head>
    <body>
        {get_header_html()}
        <div class="contact-box">
            <h2>İletişim Bilgilerimiz</h2>
            <p><strong>Sabit:</strong> 0212 635 70 22</p>
            <p><strong>WhatsApp:</strong> 0538 647 20 45</p>
            <p><strong>E-posta:</strong> erkammiknatis@gmail.com</p>
            <a href="/" style="display:inline-block; margin-top:20px; color:#0b1a3d; font-weight:bold; text-decoration:none;">⬅️ Mağazaya Dön</a>
        </div>
    </body>
    </html>
    """)

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    cart = get_cart()
    str_id = str(product_id)
    if str_id in cart:
        cart[str_id]['quantity'] += 1
    else:
        p = next((item for item in all_products_list if item["id"] == product_id), None)
        if p:
            cart[str_id] = {"id": p["id"], "name": p["name"], "price": p["price"], "quantity": 1}
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("cart_page"))

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
    return redirect(url_for("cart_page"))

@app.route("/cart")
def cart_page():
    cart = get_cart()
    items_html = ""
    total = 0.0
    for k, v in cart.items():
        price_val = float(v["price"].split()[0].replace(",", "."))
        sub = price_val * v["quantity"]
        total += sub
        items_html += f"""
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #eee; padding:10px 0;">
            <div style="flex:2;"><b>{v['name']}</b></div>
            <div style="flex:1; text-align:center;">
                <a href="/remove_from_cart/{v['id']}" style="text-decoration:none; padding:5px 10px; background:#eee; color:black; border-radius:4px;">-</a>
                <span style="margin:0 10px;">{v['quantity']}</span>
                <a href="/add_to_cart/{v['id']}" style="text-decoration:none; padding:5px 10px; background:#eee; color:black; border-radius:4px;">+</a>
            </div>
            <div style="flex:1; text-align:right;">{sub:.2f} TL</div>
        </div>"""

    return render_template_string(f"""
    <html>
    <head><meta charset="utf-8"><title>Sepetim</title><style>{get_common_styles()}</style></head>
    <body>
        {get_header_html()}
        <div style="max-width:600px; margin:30px auto; background:white; padding:30px; border-radius:15px; box-shadow:0 5px 15px rgba(0,0,0,0.1);">
            <h1>🛒 Sepetiniz</h1>
            {items_html if items_html else "<p>Sepetiniz şu an boş.</p>"}
            <hr>
            <h2 style="text-align:right;">Toplam: {total:.2f} TL</h2>
            <div style="display:flex; justify-content:space-between; margin-top:20px;">
                <a href="/" style="text-decoration:none; color:#0b1a3d; font-weight:bold; padding:10px; border:2px solid #0b1a3d; border-radius:8px;">⬅️ Alışverişe Devam</a>
                <a href="#" style="text-decoration:none; background:#28a745; color:white; padding:10px 20px; border-radius:8px; font-weight:bold;">✅ Siparişi Tamamla</a>
            </div>
        </div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(debug=True)
