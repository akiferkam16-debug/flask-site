Kitaplık
/
app_admin_gizli.py


from flask import Flask, session, redirect, request, render_template_string, url_for
import os
import json

app = Flask(__name__) 
app.secret_key = os.environ.get("SECRET_KEY", "Erkam_Miknatis_Guvenli_Anahtar_2024") 

# --- Admin Ayarları ---
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD") 
DATA_FILE = "products.json"

# --- Başlangıç Ürün Veri Bankası ---
DEFAULT_DATA = {
    "yuvarlak": [
        {"id": 1, "name": "4x2 mm Yuvarlak", "file": "1.jpg", "price": 3.00},
        {"id": 2, "name": "8x3 mm Yuvarlak", "file": "2.jpg", "price": 6.00},
        {"id": 3, "name": "15x3 mm Yuvarlak", "file": "3.jpg", "price": 12.00},
        {"id": 4, "name": "10x5 mm Yuvarlak", "file": "10x5 12 tl.jpg", "price": 12.00},
        {"id": 5, "name": "18x2 mm Yuvarlak", "file": "7.jpg", "price": 14.00},
        {"id": 6, "name": "40x5 mm Yuvarlak", "file": "6.jpg", "price": 170.00},
        {"id": 7, "name": "12x2 mm Yuvarlak", "file": "19.jpg", "price": 6.24},
        {"id": 8, "name": "50x10 mm Yuvarlak", "file": "20.jpg", "price": 647.40}
    ],
    "dikdortgen": [
        {"id": 101, "name": "10x5x2 mm Dikdörtgen", "file": "4.jpg", "price": 6.00},
        {"id": 102, "name": "20x10x5 mm Dikdörtgen", "file": "20x10x5.jpg", "price": 9.00},
        {"id": 103, "name": "30x10x5 mm Dikdörtgen", "file": "30x10x5 77tl.jpg", "price": 11.00},
        {"id": 104, "name": "15x15x5 mm Dikdörtgen", "file": "15x15x5.jpg", "price": 14.00},
        {"id": 105, "name": "10x10x2 mm Dikdörtgen", "file": "21.jpg", "price": 20.00},
        {"id": 106, "name": "50x50x25 mm Dikdörtgen", "file": "22.jpg", "price": 1638.00}
    ],
    "halka": [
        {"id": 201, "name": "10x5 mm - 6/3 Havşa", "file": "havşa.jpg", "price": 23.00},
        {"id": 202, "name": "12x5 mm 8x4 - 8/4 Havşa", "file": "havşa2.jpg", "price": 25.00},
        {"id": 203, "name": "15x5 mm - 10/5,5 Havşa", "file": "23.jpg", "price": 33.52},
        {"id": 204, "name": "18x5 mm - 10/5,5 Havşa", "file": "24.jpg", "price": 42.00},
        {"id": 205, "name": "20x5 mm - 10/5,5 Havşa", "file": "25.jpg", "price": 56.16},
        {"id": 206, "name": "25x5 mm - 10/5,5 Havşa", "file": "26.jpg", "price": 72.00},
        {"id": 207, "name": "30x5 mm - 10/5 Havşa", "file": "27.jpg", "price": 84.00},
        {"id": 208, "name": "40x5 mm - 10/5 Havşa", "file": "28.jpg", "price": 179.40}
    ]
}

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DATA, f, ensure_ascii=False, indent=4)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_all_products_list():
    data = load_data()
    return data["yuvarlak"] + data["dikdortgen"] + data["halka"]

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

def get_common_styles():
    return """
    body { margin:0; font-family: 'Segoe UI', Arial, sans-serif; background:#f8f9fa; color: #333; }
    header { background:#fff; border-bottom: 3px solid #0b1a3d; position: sticky; top:0; z-index:1000; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 10px 0; }
    .header-container { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 5px 20px; }
    .logo h1 { color:#0b1a3d; margin:0; font-size: 24px; font-weight: 800; }
    .nav-right { display:flex; gap:10px; align-items:center; flex-wrap: wrap; }
    .search-form { display:flex; margin-left:10px; }
    .search-form input { padding:8px 12px; border:1px solid #ddd; border-radius:20px 0 0 20px; outline:none; width:150px; }
    .search-form button { padding:8px 15px; border:none; background:#0b1a3d; color:white; border-radius:0 20px 20px 0; cursor:pointer; }
    .nav-btn { text-decoration:none; font-weight:bold; padding:8px 15px; border-radius:20px; transition: 0.3s; color:#fff; font-size: 13px; white-space: nowrap; }
    .contact-btn { background:#27ae60; }
    .cart-btn { background:#0b1a3d; }
    
    .notice-bar { background: #fff3cd; color: #856404; padding: 12px; text-align: center; font-weight: 600; border-bottom: 1px solid #ffeeba; font-size: 14px; }
    .category-nav { display: flex; gap: 10px; margin-bottom: 20px; justify-content: center; flex-wrap: wrap; }
    .cat-link { background: #e9ecef; color: #0b1a3d; padding: 8px 16px; border-radius: 20px; text-decoration: none; font-weight: bold; font-size: 14px; }
    .cat-link:hover { background: #0b1a3d; color: white; }

    .products-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px; margin-bottom: 40px; }
    .product-card { background:#fff; padding:15px; border-radius:12px; text-align:center; transition: 0.3s; border: 1px solid #eee; display: flex; flex-direction: column; justify-content: space-between; }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    .product-card img { width:100%; height:180px; object-fit:contain; background: #fff; border-radius:8px; }
    .title { font-weight: bold; margin: 12px 0; height: 40px; overflow: hidden; color:#0b1a3d; font-size: 15px; }
    .price { color: #e67e22; font-size: 1.2em; font-weight: bold; margin-bottom:12px; }
    .add-btn { background:#0b1a3d; color:#fff; text-decoration:none; padding:10px; border-radius:6px; font-weight:bold; display: block; }
    .add-btn:hover { background:#ffd700; color:#0b1a3d; }
    
    /* Chrome, Safari, Edge, Opera numara oklarını gizle (temiz + - görünümü için) */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    /* Firefox numara oklarını gizle */
    input[type=number] {
        -moz-appearance: textfield;
    }

    .admin-table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border-radius: 8px; overflow: hidden; }
    .admin-table th, .admin-table td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
    .admin-table th { background: #0b1a3d; color: white; }
    .admin-table tr:hover { background: #f1f1f1; }
    .edit-btn { background: #f39c12; color: white; padding: 5px 10px; text-decoration: none; border-radius: 4px; font-size: 12px; }
    
    @media (max-width:768px) {
        .header-container { flex-direction: column; gap: 12px; padding: 10px; }
        .nav-right { width: 100%; justify-content: center; }
        .products-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; padding: 5px; }
        .product-card img { height: 130px; }
    }
    """

def get_cart():
    cart = session.get("cart", {})
    return cart if isinstance(cart, dict) else {}

def render_products(prod_list):
    if not prod_list:
        return "<p style='color:black;'>Ürün bulunamadı.</p>"
    html = ""
    for p in prod_list:
        price_formatted = f"{float(p['price']):,.2f} TL"
        html += f"""
        <div class="product-card">
            <img src="/static/{p['file']}" alt="{p['name']}">
            <div>
                <div class="title">{p['name']}</div>
                <div class="price">{price_formatted}</div>
                <a class="add-btn" href="/add_to_cart/{p['id']}">Sepete Ekle</a>
            </div>
        </div>
        """
    return html

@app.route("/")
def index():
    data = load_data()
    all_content = f"""
    <div class="notice-bar">
        ⚠️ <strong>Bilgilendirme:</strong> Sitemizde numunelik (tekli/perakende düşük tutarlı) satışı bulunmamaktadır. <strong>Minimum sepet tutarı 100 TL'dir.</strong>
    </div>
    
    <div class="category-nav">
        <a href="#yuvarlak" class="cat-link">🔵 Yuvarlak Mıknatıslar</a>
        <a href="#dikdortgen" class="cat-link">🟩 Dikdörtgen Mıknatıslar</a>
        <a href="#havsali" class="cat-link">⭕ Havşalı Mıknatıslar</a>
    </div>

    <div id="yuvarlak" class="products-section">
        <h2 style="background:#0b1a3d; color:white; padding:12px; border-radius:8px; font-size:1.2em;">Yuvarlak Mıknatıslar</h2>
        <div class="products-grid">{render_products(data["yuvarlak"])}</div>
    </div>
    <div id="dikdortgen" class="products-section">
        <h2 style="background:#0b1a3d; color:white; padding:12px; border-radius:8px; font-size:1.2em;">Dikdörtgen Mıknatıslar</h2>
        <div class="products-grid">{render_products(data["dikdortgen"])}</div>
    </div>
    <div id="havsali" class="products-section">
        <h2 style="background:#0b1a3d; color:white; padding:12px; border-radius:8px; font-size:1.2em;">Halka (Havşalı) Mıknatıslar</h2>
        <div class="products-grid">{render_products(data["halka"])}</div>
    </div>
    """
    return render_template_string(f"""
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
    all_products = get_all_products_list()
    filtered = [p for p in all_products if query in p['name'].lower()]
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
            <br><a href="/" style="color:#0b1a3d; font-weight:bold; text-decoration:none;">⬅️ Geri Dön</a>
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
        </style>
    </head>
    <body>
        {get_header_html()}
        <div class="contact-box">
            <h2 style="color:#0b1a3d;">İletişim Bilgilerimiz</h2>
             <p><strong>☎️ Sabit Tel:</strong> Kullanımda Değil</p>
            <p><strong>💬 WhatsApp:</strong> +90 536 274 59 99</p>
             <p><strong>✉️ E-mail:</strong> Kullanımda Değil</p>
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
        all_products = get_all_products_list()
        p = next((item for item in all_products if item["id"] == product_id), None)
        if p:
            cart[str_id] = {"id": p["id"], "name": p["name"], "price": float(p["price"]), "quantity": 1}
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("cart_page"))

@app.route("/update_cart", methods=["POST"])
def update_cart():
    cart = get_cart()
    for key in request.form:
        if key.startswith("qty_"):
            prod_id = key.split("_")[1]
            if prod_id in cart:
                try:
                    new_qty = int(request.form.get(key))
                    if new_qty > 0:
                        cart[prod_id]['quantity'] = new_qty
                    else:
                        del cart[prod_id]
                except ValueError:
                    pass
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("cart_page"))

@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = get_cart()
    str_id = str(product_id)
    if str_id in cart:
        del cart[str_id]
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("cart_page"))

@app.route("/cart")
def cart_page():
    cart = get_cart()
    items_html = ""
    total = 0.0
    whatsapp_text = "Merhaba, Erkam Mıknatıs'tan şu siparişi vermek istiyorum:%0A"

    for k, v in cart.items():
        price_val = float(v["price"])
        sub = price_val * v["quantity"]
        total += sub
        whatsapp_text += f"- {v['name']} x {v['quantity']} Adet = {sub:,.2f} TL%0A"
        
        items_html += f"""
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #eee; padding:15px 0; gap:10px; flex-wrap:wrap;">
            <div style="flex:2; min-width:150px;"><b>{v['name']}</b><br><small>{price_val:,.2f} TL / Adet</small></div>
            <div style="flex:1; text-align:center; display:flex; align-items:center; justify-content:center; gap:2px;">
                <button type="button" onclick="changeQty('{v['id']}', -1)" style="background:#e0e0e0; border:none; padding:8px 12px; font-weight:bold; border-radius:4px 0 0 4px; cursor:pointer;">-</button>
                <input type="number" id="qty_input_{v['id']}" name="qty_{v['id']}" value="{v['quantity']}" min="1" style="width:60px; padding:7px 2px; text-align:center; border:1px solid #ccc; font-weight:bold; outline:none;">
                <button type="button" onclick="changeQty('{v['id']}', 1)" style="background:#e0e0e0; border:none; padding:8px 12px; font-weight:bold; border-radius:0 4px 4px 0; cursor:pointer;">+</button>
                <a href="/remove_from_cart/{v['id']}" style="text-decoration:none; background:#ff4d4d; color:white; padding:7px 10px; border-radius:5px; font-size:12px; margin-left:5px;" title="Ürünü Sil">🗑️</a>
            </div>
            <div style="flex:1; text-align:right; font-weight:bold; color:#e67e22; min-width:90px;">{sub:,.2f} TL</div>
        </div>"""

    whatsapp_text += f"%0AToplam Tutar: {total:,.2f} TL"

    checkout_button = ""
    if total >= 100.0:
        checkout_button = f'<a href="https://wa.me/905362745999?text={whatsapp_text}" style="text-decoration:none; background:#28a745; color:white; padding:15px; border-radius:8px; font-weight:bold; text-align:center; display:block;">✅ WhatsApp ile Siparişi Tamamla</a>'
    else:
        missing = 100.0 - total
        checkout_button = f'<div style="background:#f8d7da; color:#721c24; padding:12px; border-radius:8px; text-align:center; font-weight:bold;">⚠️ Minimum sepet tutarı 100 TL\'dir. Sepete {missing:,.2f} TL daha ürün eklemelisiniz.</div>'

    return render_template_string(f"""
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sepetim - Erkam Mıknatıs</title>
        <style>{get_common_styles()}</style>
        <script>
            function changeQty(id, val) {{
                let input = document.getElementById('qty_input_' + id);
                let currentVal = parseInt(input.value) || 1;
                let newVal = currentVal + val;
                if (newVal < 1) newVal = 1;
                input.value = newVal;
            }}
        </script>
    </head>
    <body>
        {get_header_html()}
        <div style="max-width:700px; margin:20px auto; background:white; padding:20px; border-radius:15px; box-shadow:0 5px 15px rgba(0,0,0,0.1);">
            <h1>🛒 Sepetiniz</h1>
            <form action="/update_cart" method="POST">
                {items_html if items_html else "<p>Sepetiniz boş.</p>"}
                {"" if not items_html else '<div style="margin-top:15px; text-align:right;"><button type="submit" style="background:#27ae60; color:white; border:none; padding:10px 20px; border-radius:5px; font-weight:bold; cursor:pointer; font-size:14px;">💾 Kaydet</button></div>'}
            </form>
            <div style="text-align:right; margin-top:20px;">
                <h3>Toplam: {total:,.2f} TL</h3>
            </div>
            <div style="display:flex; flex-direction:column; gap:10px; margin-top:20px;">
                {checkout_button}
                <a href="/" style="text-decoration:none; color:#0b1a3d; font-weight:bold; text-align:center; display:block; margin-top:5px;">⬅️ Alışverişe Devam Et</a>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route("/erkam-yonetim/login", methods=["GET", "POST"])
def admin_login():
    error = ""
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin_panel"))
        else:
            error = "Hatalı şifre!"
            
    return render_template_string(f"""
    <html>
    <head><meta charset="utf-8"><title>Admin Girişi</title><style>{get_common_styles()}</style></head>
    <body>
        {get_header_html()}
        <div style="max-width:400px; margin:50px auto; background:white; padding:30px; border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.1); text-align:center;">
            <h2>Admin Girişi</h2>
            <p style="color:red;">{error}</p>
            <form method="POST">
                <input type="password" name="password" placeholder="Şifre" style="width:100%; padding:10px; margin-bottom:15px; border:1px solid #ccc; border-radius:5px;" required>
                <button type="submit" style="background:#0b1a3d; color:white; border:none; padding:10px 20px; width:100%; border-radius:5px; cursor:pointer;">Giriş Yap</button>
            </form>
        </div>
    </body></html>
    """)

@app.route("/erkam-yonetim/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("index"))

@app.route("/erkam-yonetim")
def admin_panel():
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))
        
    data = load_data()
    
    def generate_table(category_key, title):
        rows = ""
        for p in data[category_key]:
            rows += f"""
            <tr>
                <td>{p['id']}</td>
                <td>{p['name']}</td>
                <td>{float(p['price']):,.2f} TL</td>
                <td>{p['file']}</td>
                <td><a href="/erkam-yonetim/edit/{category_key}/{p['id']}" class="edit-btn">✏️ Düzenle</a></td>
            </tr>
            """
        return f"""
        <h3 style="margin-top:30px; color:#0b1a3d;">{title}</h3>
        <table class="admin-table">
            <tr><th>ID</th><th>Ürün Adı</th><th>Fiyat</th><th>Görsel Dosyası</th><th>İşlem</th></tr>
            {rows}
        </table>
        """

    html = f"""
    <html>
    <head><meta charset="utf-8"><title>Admin Paneli</title><style>{get_common_styles()}</style></head>
    <body>
        {get_header_html()}
        <div style="max-width:1200px; margin:20px auto; padding:20px; background:white; border-radius:10px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h2>⚙️ Ürün Yönetim Paneli</h2>
                <a href="/erkam-yonetim/logout" style="color:red; text-decoration:none; font-weight:bold;">🚪 Çıkış Yap</a>
            </div>
            <p>Buradan ürün bilgilerini değiştirebilirsiniz. Değişiklikler anında sitede güncellenir.</p>
            
            {generate_table("yuvarlak", "Yuvarlak Mıknatıslar")}
            {generate_table("dikdortgen", "Dikdörtgen Mıknatıslar")}
            {generate_table("halka", "Halka (Havşalı) Mıknatıslar")}
            
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/erkam-yonetim/edit/<category>/<int:product_id>", methods=["GET", "POST"])
def edit_product(category, product_id):
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))
        
    data = load_data()
    if category not in data:
        return "Geçersiz kategori."
        
    product_idx = next((index for (index, d) in enumerate(data[category]) if d["id"] == product_id), None)
    if product_idx is None:
        return "Ürün bulunamadı."
        
    product = data[category][product_idx]
    
    if request.method == "POST":
        try:
            new_price = float(request.form.get("price").replace(",", "."))
        except:
            new_price = product["price"]

        data[category][product_idx]["name"] = request.form.get("name")
        data[category][product_idx]["price"] = new_price
        data[category][product_idx]["file"] = request.form.get("file")
        
        save_data(data)
        return redirect(url_for("admin_panel"))

    return render_template_string(f"""
    <html>
    <head><meta charset="utf-8"><title>Ürün Düzenle</title><style>{get_common_styles()}</style></head>
    <body>
        {get_header_html()}
        <div style="max-width:500px; margin:50px auto; background:white; padding:30px; border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.1);">
            <h2 style="color:#0b1a3d;">✏️ Ürün Düzenle</h2>
            <form method="POST">
                <div style="margin-bottom:15px;">
                    <label style="font-weight:bold;">Ürün Adı:</label>
                    <input type="text" name="name" value="{product['name']}" style="width:100%; padding:10px; margin-top:5px; border:1px solid #ccc; border-radius:5px;" required>
                </div>
                <div style="margin-bottom:15px;">
                    <label style="font-weight:bold;">Fiyat (Sadece sayı girin, Örn: 15.00):</label>
                    <input type="text" name="price" value="{product['price']}" style="width:100%; padding:10px; margin-top:5px; border:1px solid #ccc; border-radius:5px;" required>
                </div>
                <div style="margin-bottom:25px;">
                    <label style="font-weight:bold;">Görsel Dosya Adı (Örn: 1.jpg):</label>
                    <input type="text" name="file" value="{product['file']}" style="width:100%; padding:10px; margin-top:5px; border:1px solid #ccc; border-radius:5px;" required>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <a href="/erkam-yonetim" style="background:#ccc; color:black; padding:10px 20px; text-decoration:none; border-radius:5px;">İptal</a>
                    <button type="submit" style="background:#27ae60; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">💾 Kaydet</button>
                </div>
            </form>
        </div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(debug=True)
