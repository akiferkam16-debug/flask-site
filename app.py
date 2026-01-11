from flask import Flask, session, redirect, request, render_template_string, url_for
import os

app = Flask(__name__) 
app.secret_key = os.environ.get("SECRET_KEY", "Erkam_Miknatis_2024_Guvenli") 

# --- Gelişmiş Ürün Veri Bankası (Teknik Detaylar Eklendi) ---
# Tip: Y=Yuvarlak, D=Dikdörtgen, H=Halka
all_products = [
    {"id": 1, "type": "Y", "name": "4x2 mm Yuvarlak", "file": "1.jpg", "price": "3.00 TL", "guc": "0.5 kg", "kaplama": "Nikel", "isi": "80°C"},
    {"id": 2, "type": "Y", "name": "8x3 mm Yuvarlak", "file": "2.jpg", "price": "6.00 TL", "guc": "1.2 kg", "kaplama": "Nikel", "isi": "80°C"},
    {"id": 3, "type": "Y", "name": "15x3 mm Yuvarlak", "file": "3.jpg", "price": "12.00 TL", "guc": "3.5 kg", "kaplama": "Nikel", "isi": "80°C"},
    {"id": 4, "type": "Y", "name": "10x5 mm Yuvarlak", "file": "10x5 12 tl.jpg", "price": "12.00 TL", "guc": "2.8 kg", "kaplama": "Nikel", "isi": "80°C"},
    {"id": 101, "type": "D", "name": "10x5x2 mm Dikdörtgen", "file": "4.jpg", "price": "6.00 TL", "guc": "1.0 kg", "kaplama": "Nikel", "isi": "80°C"},
    {"id": 102, "type": "D", "name": "20x10x5 mm Dikdörtgen", "file": "20x10x5.jpg", "price": "9.00 TL", "guc": "6.5 kg", "kaplama": "Nikel", "isi": "80°C"},
    {"id": 201, "type": "H", "name": "10x5 mm Havşa", "file": "havşa.jpg", "price": "23.00 TL", "guc": "2.0 kg", "kaplama": "Nikel", "isi": "80°C"},
]

# --- Yardımcı Fonksiyonlar ---
def get_cart():
    cart = session.get("cart", {})
    return cart if isinstance(cart, dict) else {}

def get_common_styles():
    return """
    body { margin:0; font-family: 'Segoe UI', sans-serif; background:#f4f4f4; }
    header { display:flex; justify-content:space-between; align-items:center; padding:15px 30px; background:#fff; border-bottom: 3px solid #0b1a3d; position: sticky; top:0; z-index:100; }
    .logo h1 { color:#0b1a3d; margin:0; font-size: 22px; }
    .nav-group { display:flex; gap:10px; }
    .nav-btn { text-decoration:none; color:#fff; padding:8px 15px; border-radius:20px; font-weight:bold; font-size:13px; }
    .search-container { background:#0b1a3d; padding:15px; text-align:center; }
    .search-input { padding:10px; width:60%; border-radius:25px; border:none; outline:none; font-size:16px; }
    .products-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; padding:20px; max-width:1200px; margin:auto; }
    .product-card { background:#fff; padding:15px; border-radius:12px; text-align:center; transition: 0.3s; border:1px solid #ddd; }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    .product-card img { width:100%; height:180px; object-fit:cover; border-radius:8px; }
    .price { color: #e67e22; font-size: 1.2em; font-weight: bold; margin:10px 0; }
    .btn-detail { background:#34495e; color:white; text-decoration:none; padding:8px; display:block; border-radius:5px; margin-bottom:5px; font-size:13px; }
    .btn-add { background:#0b1a3d; color:white; text-decoration:none; padding:8px; display:block; border-radius:5px; font-weight:bold; }
    .tech-table { width:100%; border-collapse:collapse; margin-top:15px; font-size:14px; }
    .tech-table td { border:1px solid #eee; padding:8px; text-align:left; }
    .tech-table tr:nth-child(even) { background:#f9f9f9; }
    """

# --- Rotalar ---
@app.route("/")
def index():
    query = request.args.get("q", "").lower()
    # Arama Filtrelemesi
    filtered = [p for p in all_products if query in p['name'].lower()]
    
    product_html = ""
    for p in filtered:
        product_html += f"""
        <div class="product-card">
            <img src="/static/{p['file']}" alt="{p['name']}">
            <div style="font-weight:bold; margin:10px 0; height:40px;">{p['name']}</div>
            <div class="price">{p['price']}</div>
            <a href="/urun/{p['id']}" class="btn-detail">🔍 Teknik Özellikler</a>
            <a href="/add_to_cart/{p['id']}" class="btn-add">🛒 Sepete Ekle</a>
        </div>
        """

    return render_template_string(f"""
    <html>
    <head>
        <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Erkam Mıknatıs</title>
        <style>{get_common_styles()}</style>
    </head>
    <body>
        <header>
            <div class="nav-group">
                <a href="/iletisim" class="nav-btn" style="background:#27ae60;">📞 İletişim</a>
                <a href="/cart" class="nav-btn" style="background:#0b1a3d;">🛒 Sepet</a>
            </div>
            <div class="logo"><h1>Erkam Mıknatıs</h1></div>
            <div style="width:80px;"></div>
        </header>
        <div class="search-container">
            <form action="/">
                <input type="text" name="q" class="search-input" placeholder="Örn: 10x5, Yuvarlak, Mıknatıs ara..." value="{query}">
            </form>
        </div>
        <main class="products-grid">
            {product_html if product_html else "<p style='grid-column:1/-1; text-align:center;'>Ürün bulunamadı.</p>"}
        </main>
    </body>
    </html>
    """)

@app.route("/urun/<int:product_id>")
def product_detail(product_id):
    p = next((item for item in all_products if item["id"] == product_id), None)
    if not p: return redirect("/")
    
    return render_template_string(f"""
    <html>
    <head>
        <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            {get_common_styles()}
            .detail-container {{ max-width:800px; margin:30px auto; background:#fff; padding:20px; border-radius:15px; display:flex; gap:30px; box-shadow:0 10px 20px rgba(0,0,0,0.1); }}
            @media (max-width:600px) {{ .detail-container {{ flex-direction:column; }} }}
        </style>
    </head>
    <body>
        <header>
            <a href="/" style="text-decoration:none; color:#0b1a3d; font-weight:bold;">⬅️ Geri Dön</a>
            <div class="logo"><h1>Ürün Detayı</h1></div>
            <div style="width:50px;"></div>
        </header>
        <div class="detail-container">
            <div style="flex:1;"><img src="/static/{p['file']}" style="width:100%; border-radius:10px;"></div>
            <div style="flex:1;">
                <h2>{p['name']}</h2>
                <div class="price" style="font-size:2em;">{p['price']}</div>
                <table class="tech-table">
                    <tr><td><b>Malzeme</b></td><td>Neodyum</td></tr>
                    <tr><td><b>Çekim Gücü</b></td><td>{p['guc']}</td></tr>
                    <tr><td><b>Kaplama</b></td><td>{p['kaplama']}</td></tr>
                    <tr><td><b>Çalışma Isısı</b></td><td>{p['isi']}</td></tr>
                </table>
                <br>
                <a href="/add_to_cart/{p['id']}" class="btn-add" style="font-size:18px; padding:15px;">🛒 Sepete Ekle</a>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route("/iletisim")
def contact():
    # Önceki kodundaki iletişim sayfası buraya gelecek (Aynen koruyabilirsin)
    return "İletişim Sayfası (Burayı önceki kodunla doldurabilirsin)"

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

@app.route("/cart")
def cart_page():
    # Önceki kodundaki sepet sayfası yapısını buraya ekleyebilirsin
    return "Sepet Sayfası"

if __name__ == "__main__":
    app.run(debug=True)
