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
     {"id": 7, "name": "12x2 mm Yuvarlak", "file": "19.jpg", "price": "6.24 TL"},
     {"id": 8, "name": "50x10 mm Yuvarlak", "file": "20.jpg", "price": "647.40 TL"},
]
rectangle_products = [
    {"id": 101, "name": "10x5x2 mm Dikdörtgen", "file": "4.jpg", "price": "6.00 TL"},
    {"id": 102, "name": "20x10x5 mm Dikdörtgen", "file": "20x10x5.jpg", "price": "9.00 TL"},
    {"id": 103, "name": "30x10x5 mm Dikdörtgen", "file": "30x10x5 77tl.jpg", "price": "11.00 TL"},
    {"id": 104, "name": "15x15x5 mm Dikdörtgen", "file": "15x15x5.jpg", "price": "14.00 TL"},
     {"id": 105, "name": "10x10x2 mm Dikdörtgen", "file": "21.jpg", "price": "20.00 TL"},
    {"id": 106, "name": "50x50x25 mm Dikdörtgen", "file": "22.jpg", "price": "1.638.00 TL"},
]
ring_products = [
    {"id": 201, "name": "10x5 mm - 6/3 Havşa", "file": "havşa.jpg", "price": "23.00 TL"},
    {"id": 202, "name": "12x5 mm 8x4 - 8/4 Havşa", "file": "havşa2.jpg", "price": "25.00 TL"},
      {"id": 203, "name": "15x5 mm  - 10/5,5 Havşa", "file": "23.jpg", "price": "33.52 TL"}
]

all_products_list = products + rectangle_products + ring_products

# --- Ortak Stil ve Header Fonksiyonu ---
def get_header_html():
    return """
    <header>
        <div class="header-container">
            <div class="logo">
                <a href="/" style="text-decoration:none;"><h1>Erkam Mıknatıs</h1></a>
            </div>
            
            <div class="nav-right">
                <a class="nav-btn contact-btn" href="/iletisim">📞 İletişim</a>
                <a class="nav-btn cart-btn" href="/cart">🛒 Sepet</a>
                <form action="/search" method="GET" class="search-form">
                    <input type="text" name="q" placeholder="Ürün ara..." required>
                    <button type="submit">🔍</button>
                </form>
            </div>
        </div>
    </header>
    """
def get_footer_html():
    return """
    <footer class="footer">
        <div class="footer-inner">
            <h3>Ödeme Yöntemlerimiz</h3>
            <div class="payment-methods">
                <img src="/static/bonus.png" alt="Bonus">
                <img src="/static/axess.png" alt="Axess">
                <img src="/static/cardfinans.png" alt="CardFinans">
                <img src="/static/maximum.png" alt="Maximum">
                <img src="/static/paraf.png" alt="Paraf">
                <img src="/static/world.png" alt="World">
            </div>
            <p class="footer-copy">© 2026 Erkam Mıknatıs • Tüm Hakları Saklıdır</p>
        </div>
    </footer>
    """
def get_common_styles():
    return """
    body { margin:0; font-family: 'Segoe UI', Arial, sans-serif; background:#f8f9fa; color: #333; }
    
    /* --- HEADER & NAV --- */
    header { 
        background:#fff; 
        border-bottom: 3px solid #0b1a3d; 
        position: sticky; 
        top:0; 
        z-index:1000; 
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        padding: 10px 0;
    }
    .header-container {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 20px;
    }
    .logo h1 { color:#0b1a3d; margin:0; font-size: 24px; font-weight: 800; }
    .nav-right { display:flex; gap:10px; align-items:center; }
    
    .search-form { display:flex; margin-left:10px; }
    .search-form input { 
        padding:8px 12px; 
        border:1px solid #ddd; 
        border-radius:20px 0 0 20px; 
        outline:none; 
        width:150px; 
    }
    .search-form button { 
        padding:8px 15px; border:none; background:#0b1a3d; color:white; border-radius:0 20px 20px 0; cursor:pointer; 
    }

    .nav-btn { text-decoration:none; font-weight:bold; padding:8px 15px; border-radius:20px; transition: 0.3s; color:#fff; font-size: 13px; white-space: nowrap; }
    .contact-btn { background:#27ae60; }
    .cart-btn { background:#0b1a3d; }
    
    /* --- ÜRÜN KARTLARI --- */
    .products-grid { 
        display: grid; 
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); 
        gap: 20px; 
        margin-bottom: 40px;
    }
    .product-card { 
        background:#fff; 
        padding:15px; 
        border-radius:12px; 
        text-align:center; 
        transition: 0.3s; 
        border: 1px solid #eee; 
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    .product-card img { width:100%; height:180px; object-fit:contain; background: #fff; border-radius:8px; }
    .title { font-weight: bold; margin: 12px 0; height: 40px; overflow: hidden; color:#0b1a3d; font-size: 15px; }
    .price { color: #e67e22; font-size: 1.2em; font-weight: bold; margin-bottom:12px; }
    .add-btn { background:#0b1a3d; color:#fff; text-decoration:none; padding:10px; border-radius:6px; font-weight:bold; }
    .add-btn:hover { background:#ffd700; color:#0b1a3d; }

    /* --- MOBIL ÖZEL AYARLAR (KUSURSUZ GÖRÜNÜM) --- */
    @media (max-width:768px) {
        .header-container { flex-direction: column; gap: 12px; padding: 10px; }
        .nav-right { width: 100%; justify-content: center; }
        .logo h1 { font-size: 22px; }
        
        /* Mobilde ürünleri 2'li yan yana yap (daha modern durur) */
        .products-grid { 
            grid-template-columns: repeat(2, 1fr); 
            gap: 10px; 
            padding: 5px;
        }
        .product-card { padding: 10px; }
        .product-card img { height: 130px; }
        .title { font-size: 13px; height: 35px; margin: 8px 0; }
        .price { font-size: 1em; }
        .add-btn { font-size: 12px; padding: 8px; }
        
        /* Arama kutusunu mobilde biraz daha daralt */
        .search-form input { width: 100px; }
        .nav-btn { padding: 8px 12px; font-size: 12px; }
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
            <div>
                <div class="title">{p['name']}</div>
                <div class="price">{p['price']}</div>
                <a class="add-btn" href="/add_to_cart/{p['id']}">Sepete Ekle</a>
            </div>
        </div>
        """
    return html

# --- Route'lar ---

@app.route("/")
def index():
    all_content = f"""
    <div id="yuvarlak" class="products-section">
        <h2 style="background:#0b1a3d; color:white; padding:12px; border-radius:8px; font-size:1.2em;">Yuvarlak Mıknatıslar</h2>
        <div class="products-grid">{render_products(products)}</div>
    </div>
    <div id="dikdortgen" class="products-section">
        <h2 style="background:#0b1a3d; color:white; padding:12px; border-radius:8px; font-size:1.2em;">Dikdörtgen Mıknatıslar</h2>
        <div class="products-grid">{render_products(rectangle_products)}</div>
    </div>
    <div id="havsali" class="products-section">
        <h2 style="background:#0b1a3d; color:white; padding:12px; border-radius:8px; font-size:1.2em;">Halka (Havşalı) Mıknatıslar</h2>
        <div class="products-grid">{render_products(ring_products)}</div>
    </div>
    """
    return render_template_string(f"""
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Erkam Mıknatıs | Kaliteli Mıknatısın Adresi</title>
        <style>{get_common_styles()}</style>
    </head>
    <body>
        {get_header_html()}
        <div style="max-width:1200px; margin:20px auto; padding:0 15px;">
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
            <h2 style="border-bottom:2px solid #0b1a3d; padding-bottom:10px;">"{query}" Sonuçları ({len(filtered)})</h2>
            <div class="products-grid">{render_products(filtered)}</div>
            <br><a href="/" style="color:#0b1a3d; font-weight:bold; text-decoration:none; display:inline-block; margin-bottom:30px;">⬅️ Mağazaya Geri Dön</a>
        </div>
    </body>
    </html>
    """)

@app.route("/iletisim")
def contact():
    return render_template_string(f"""
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>İletişim - Erkam Mıknatıs</title>
        <style>
            {get_common_styles()}
            .contact-box {{ max-width:500px; margin:40px auto; background:#fff; padding:30px; border-radius:15px; text-align:center; box-shadow:0 5px 15px rgba(0,0,0,0.1); border:1px solid #eee; }}
            .contact-item {{ margin: 20px 0; font-size: 1.1em; }}
        </style>
    </head>
    <body>
        {get_header_html()}
        <div class="contact-box">
            <h2 style="color:#0b1a3d;">İletişim Bilgilerimiz</h2>
            <div class="contact-item"><strong>📞 Sabit:</strong><br> Kullanımda Değil</div>
            <div class="contact-item"><strong>💬 WhatsApp:</strong><br> +90 530 946 62 44</div>
            <div class="contact-item"><strong>📧 E-posta:</strong><br> Kullanımda Değil</div>
            <a href="/" style="display:inline-block; margin-top:20px; color:#0b1a3d; font-weight:bold; text-decoration:none;">⬅️ Alışverişe Dön</a>
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
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #eee; padding:15px 0;">
            <div style="flex:2; font-size:14px;"><b>{v['name']}</b></div>
            <div style="flex:1; text-align:center; display:flex; align-items:center; justify-content:center; gap:8px;">
                <a href="/remove_from_cart/{v['id']}" style="text-decoration:none; width:25px; height:25px; line-height:25px; background:#eee; color:black; border-radius:50%; display:inline-block;">-</a>
                <span>{v['quantity']}</span>
                <a href="/add_to_cart/{v['id']}" style="text-decoration:none; width:25px; height:25px; line-height:25px; background:#eee; color:black; border-radius:50%; display:inline-block;">+</a>
            </div>
            <div style="flex:1; text-align:right; font-weight:bold; color:#e67e22;">{sub:.2f} TL</div>
        </div>"""

    return render_template_string(f"""
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sepetim - Erkam Mıknatıs</title>
        <style>{get_common_styles()}</style>
    </head>
    <body>
        {get_header_html()}
        <div style="max-width:600px; margin:20px auto; background:white; padding:20px; border-radius:15px; box-shadow:0 5px 15px rgba(0,0,0,0.1);">
            <h1 style="color:#0b1a3d; border-bottom:2px solid #eee; padding-bottom:10px;">🛒 Sepetiniz</h1>
            {items_html if items_html else "<p style='text-align:center; padding:20px;'>Sepetiniz şu an boş.</p>"}
            <div style="text-align:right; margin-top:20px;">
                <span style="font-size:1.2em;">Genel Toplam:</span>
                <h2 style="color:#e67e22; margin:5px 0;">{total:.2f} TL</h2>
            </div>
            <div style="display:flex; flex-direction:column; gap:10px; margin-top:20px;">
                <a href="#" style="text-decoration:none; background:#28a745; color:white; padding:15px; border-radius:8px; font-weight:bold; text-align:center; font-size:1.1em;">✅ Siparişi Tamamla</a>
                <a href="/" style="text-decoration:none; color:#0b1a3d; font-weight:bold; padding:12px; border:2px solid #0b1a3d; border-radius:8px; text-align:center;">⬅️ Alışverişe Devam Et</a>
            </div>
        </div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(debug=True)
