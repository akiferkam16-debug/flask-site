from flask import Flask, session, redirect, request, render_template_string, url_for
import os

app = Flask(__name__) 
app.secret_key = os.environ.get("SECRET_KEY", "Erkam_Miknatis_2026_Ozel_Anahtar") 

# --- Ürün Veri Bankası (Teknik Detaylar Dahil) ---
all_products = [
    {"id": 1, "name": "4x2 mm Yuvarlak", "file": "1.jpg", "price": "3.00 TL", "guc": "0.5 kg", "isi": "80°C", "kaplama": "Nikel"},
    {"id": 2, "name": "8x3 mm Yuvarlak", "file": "2.jpg", "price": "6.00 TL", "guc": "1.2 kg", "isi": "80°C", "kaplama": "Nikel"},
    {"id": 3, "name": "15x3 mm Yuvarlak", "file": "3.jpg", "price": "12.00 TL", "guc": "3.5 kg", "isi": "80°C", "kaplama": "Nikel"},
    {"id": 4, "name": "10x5 mm Yuvarlak", "file": "10x5 12 tl.jpg", "price": "12.00 TL", "guc": "2.8 kg", "isi": "80°C", "kaplama": "Nikel"},
    {"id": 5, "name": "18x2 mm Yuvarlak", "file": "7.jpg", "price": "14.00 TL", "guc": "2.1 kg", "isi": "80°C", "kaplama": "Nikel"},
    {"id": 101, "name": "10x5x2 mm Dikdörtgen", "file": "4.jpg", "price": "6.00 TL", "guc": "1.0 kg", "isi": "80°C", "kaplama": "Nikel"},
    {"id": 102, "name": "20x10x5 mm Dikdörtgen", "file": "20x10x5.jpg", "price": "9.00 TL", "guc": "6.5 kg", "isi": "80°C", "kaplama": "Nikel"},
    {"id": 201, "name": "10x5 mm Havşa", "file": "havşa.jpg", "price": "23.00 TL", "guc": "2.0 kg", "isi": "80°C", "kaplama": "Nikel"}
]

# --- Yardımcı Fonksiyonlar ---
def get_cart():
    cart = session.get("cart", {})
    return cart if isinstance(cart, dict) else {}

def get_common_styles():
    return """
    body { margin:0; font-family: 'Segoe UI', sans-serif; background:#f0f2f5; color:#333; }
    header { display:flex; justify-content:space-between; align-items:center; padding:15px 5%; background:#fff; border-bottom:3px solid #0b1a3d; position:sticky; top:0; z-index:1000; }
    .logo h1 { color:#0b1a3d; margin:0; font-size:24px; }
    .nav-btns { display:flex; gap:10px; }
    .nav-link { text-decoration:none; padding:10px 20px; border-radius:25px; font-weight:bold; font-size:14px; color:white; transition:0.3s; }
    .btn-green { background:#27ae60; }
    .btn-blue { background:#0b1a3d; }
    .btn-green:hover { background:#2ecc71; }
    .search-bar { background:#0b1a3d; padding:20px; text-align:center; }
    .search-bar input { width:50%; padding:12px 25px; border-radius:30px; border:none; font-size:16px; outline:none; }
    .container { max-width:1200px; margin:20px auto; padding:0 20px; }
    .grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap:25px; }
    .card { background:#fff; border-radius:15px; overflow:hidden; border:1px solid #ddd; transition:0.3s; text-align:center; padding:15px; }
    .card:hover { transform:translateY(-5px); box-shadow:0 10px 20px rgba(0,0,0,0.1); }
    .card img { width:100%; height:200px; object-fit:cover; border-radius:10px; }
    .card h3 { margin:15px 0 5px; font-size:18px; color:#0b1a3d; height:45px; overflow:hidden; }
    .price { color:#e67e22; font-size:20px; font-weight:bold; margin-bottom:15px; }
    .btn-action { display:block; text-decoration:none; padding:10px; border-radius:8px; font-weight:bold; margin-top:10px; }
    .btn-details { background:#f8f9fa; color:#333; border:1px solid #ccc; }
    .btn-add { background:#0b1a3d; color:white; }
    .tech-table { width:100%; border-collapse:collapse; margin:20px 0; }
    .tech-table td { padding:10px; border-bottom:1px solid #eee; text-align:left; }
    .tech-table b { color:#0b1a3d; }
    @media (max-width:768px) { .search-bar input { width:90%; } header { flex-direction:column; gap:15px; text-align:center; } }
    """

# --- Sayfalar ---

@app.route("/")
def index():
    query = request.args.get("q", "").lower()
    filtered = [p for p in all_products if query in p['name'].lower()]
    
    products_html = ""
    for p in filtered:
        products_html += f"""
        <div class="card">
            <img src="/static/{p['file']}" alt="{p['name']}">
            <h3>{p['name']}</h3>
            <div class="price">{p['price']}</div>
            <a href="/urun/{p['id']}" class="btn-action btn-details">🔍 Teknik Detaylar</a>
            <a href="/add_to_cart/{p['id']}" class="btn-action btn-add">🛒 Sepete Ekle</a>
        </div>
        """

    return render_template_string(f"""
    <html>
    <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Erkam Mıknatıs | Neodyum Mıknatıs Dünyası</title><style>{get_common_styles()}</style></head>
    <body>
        <header>
            <div class="nav-btns">
                <a href="/iletisim" class="nav-link btn-green">📞 İletişim</a>
                <a href="/cart" class="nav-link btn-blue">🛒 Sepetim</a>
            </div>
            <div class="logo"><h1>Erkam Mıknatıs</h1></div>
            <div style="width:100px;"></div>
        </header>
        <div class="search-bar">
            <form action="/"><input type="text" name="q" placeholder="Ölçü veya model ara (Örn: 10x5)..." value="{query}"></form>
        </div>
        <div class="container"><div class="grid">{products_html if products_html else "<p>Ürün bulunamadı.</p>"}</div></div>
    </body>
    </html>
    """)

@app.route("/urun/<int:product_id>")
def product_detail(product_id):
    p = next((item for item in all_products if item["id"] == product_id), None)
    if not p: return redirect("/")
    
    return render_template_string(f"""
    <html>
    <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{p['name']} Detayları</title><style>{get_common_styles()}</style></head>
    <body>
        <header>
            <a href="/" class="nav-link btn-blue" style="background:#f4f4f4; color:#333;">⬅️ Geri Dön</a>
            <div class="logo"><h1>Ürün Özellikleri</h1></div>
            <div style="width:100px;"></div>
        </header>
        <div class="container" style="max-width:900px; background:white; padding:40px; border-radius:20px; margin-top:40px; display:flex; gap:40px; flex-wrap:wrap; justify-content:center;">
            <div style="flex:1; min-width:300px;"><img src="/static/{p['file']}" style="width:100%; border-radius:15px; box-shadow:0 5px 15px rgba(0,0,0,0.1);"></div>
            <div style="flex:1; min-width:300px;">
                <h2>{p['name']}</h2>
                <div class="price" style="font-size:28px;">{p['price']}</div>
                <table class="tech-table">
                    <tr><td><b>Mıknatıs Tipi</b></td><td>Neodyum (N35)</td></tr>
                    <tr><td><b>Çekim Gücü</b></td><td>{p['guc']}</td></tr>
                    <tr><td><b>Çalışma Isısı</b></td><td>{p['isi']} Max</td></tr>
                    <tr><td><b>Kaplama Türü</b></td><td>{p['kaplama']}</td></tr>
                </table>
                <a href="/add_to_cart/{p['id']}" class="btn-action btn-add" style="font-size:18px; padding:15px;">🛒 Sepete Ekle</a>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route("/iletisim")
def contact():
    return render_template_string(f"""
    <html>
    <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>İletişim | Erkam Mıknatıs</title><style>{get_common_styles()}</style></head>
    <body>
        <header><a href="/" class="nav-link btn-blue">⬅️ Ana Sayfa</a><div class="logo"><h1>İletişim</h1></div><div style="width:80px;"></div></header>
        <div class="container" style="max-width:600px; background:white; padding:40px; border-radius:20px; text-align:center; margin-top:50px;">
            <h2 style="color:#0b1a3d;">Bize Ulaşın</h2>
            <div style="margin:30px 0; font-size:18px; line-height:2;">
                <p><b>☎️ Sabit Hat:</b> <br><a href="tel:+902120000000" style="color:#27ae60; text-decoration:none;">0212 XXX XX XX</a></p>
                <p><b>📱 GSM / WhatsApp:</b> <br><a href="https://wa.me/905XXXXXXXXX" style="color:#27ae60; text-decoration:none;">05XX XXX XX XX</a></p>
                <p><b>📧 Gmail:</b> <br><a href="mailto:erkammiknatis@gmail.com" style="color:#27ae60; text-decoration:none;">erkammiknatis@gmail.com</a></p>
            </div>
            <p style="color:#777; font-size:14px;">Hafta içi 09:00 - 18:00 arası hizmet vermekteyiz.</p>
        </div>
    </body>
    </html>
    """)

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    cart = get_cart()
    str_id = str(product_id)
    p = next((item for item in all_products if item["id"] == product_id), None)
    if p:
        if str_id in cart: cart[str_id]['quantity'] += 1
        else: cart[str_id] = {"id": p["id"], "name": p["name"], "price": p["price"], "quantity": 1}
    session["cart"] = cart
    session.modified = True
    return redirect("/cart")

@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = get_cart()
    str_id = str(product_id)
    if str_id in cart:
        if cart[str_id]['quantity'] > 1: cart[str_id]['quantity'] -= 1
        else: del cart[str_id]
    session["cart"] = cart
    session.modified = True
    return redirect("/cart")

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
        <div style="display:flex; justify-content:space-between; align-items:center; padding:15px 0; border-bottom:1px solid #eee;">
            <div style="flex:2;"><b>{v['name']}</b></div>
            <div style="flex:1; text-align:center;">
                <a href="/remove_from_cart/{v['id']}" style="text-decoration:none; padding:5px 10px; background:#eee; color:black; border-radius:5px;">-</a>
                <span style="margin:0 10px;">{v['quantity']}</span>
                <a href="/add_to_cart/{v['id']}" style="text-decoration:none; padding:5px 10px; background:#eee; color:black; border-radius:5px;">+</a>
            </div>
            <div style="flex:1; text-align:right;">{sub:.2f} TL</div>
        </div>"""

    return render_template_string(f"""
    <html>
    <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sepetim | Erkam Mıknatıs</title><style>{get_common_styles()}</style></head>
    <body>
        <header><a href="/" class="nav-link btn-blue">⬅️ Alışverişe Dön</a><div class="logo"><h1>Sepetiniz</h1></div><div style="width:100px;"></div></header>
        <div class="container" style="max-width:700px; background:white; padding:30px; border-radius:20px; margin-top:30px; box-shadow:0 10px 20px rgba(0,0,0,0.05);">
            {items_html if items_html else "<p style='text-align:center;'>Sepetiniz boş.</p>"}
            <div style="text-align:right; margin-top:25px; border-top:2px solid #0b1a3d; padding-top:15px;">
                <h2 style="color:#0b1a3d;">Toplam: {total:.2f} TL</h2>
                <a href="#" class="btn-action btn-add" style="padding:15px; font-size:18px;">✅ Siparişi Onayla</a>
            </div>
        </div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(debug=True)
