from flask import Flask, session, redirect, request, render_template_string, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__) 
app.secret_key = os.environ.get("SECRET_KEY", "Erkam_Miknatis_Guvenli_Anahtar_2024") 
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Erkam_Guvenli_Sifre_99!_2026")

# --- Veritabanı Ayarları ---
db_url = os.environ.get("DATABASE_URL", "sqlite:///products.db")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Veritabanı Modeli ---
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    file = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(50), nullable=False)

# --- Başlangıç Verileri ---
DEFAULT_PRODUCTS = [
    (1, 'yuvarlak', '4x2 mm Yuvarlak', '1.jpg', '3.00 TL'),
    (2, 'yuvarlak', '8x3 mm Yuvarlak', '2.jpg', '6.00 TL'),
    (3, 'yuvarlak', '15x3 mm Yuvarlak', '3.jpg', '12.00 TL'),
    (4, 'yuvarlak', '10x5 mm Yuvarlak', '10x5 12 tl.jpg', '12.00 TL'),
    (5, 'yuvarlak', '18x2 mm Yuvarlak', '7.jpg', '14.00 TL'),
    (6, 'yuvarlak', '40x5 mm Yuvarlak', '6.jpg', '170.00 TL'),
    (7, 'yuvarlak', '12x2 mm Yuvarlak', '19.jpg', '6.24 TL'),
    (8, 'yuvarlak', '50x10 mm Yuvarlak', '20.jpg', '647.40 TL'),
    
    (101, 'dikdortgen', '10x5x2 mm Dikdörtgen', '4.jpg', '6.00 TL'),
    (102, 'dikdortgen', '20x10x5 mm Dikdörtgen', '20x10x5.jpg', '9.00 TL'),
    (103, 'dikdortgen', '30x10x5 mm Dikdörtgen', '30x10x5 77tl.jpg', '11.00 TL'),
    (104, 'dikdortgen', '15x15x5 mm Dikdörtgen', '15x15x5.jpg', '14.00 TL'),
    (105, 'dikdortgen', '10x10x2 mm Dikdörtgen', '21.jpg', '20.00 TL'),
    (106, 'dikdortgen', '50x50x25 mm Dikdörtgen', '22.jpg', '1.638.00 TL'),
    
    (201, 'halka', '10x5 mm - 6/3 Havşa', 'havşa.jpg', '23.00 TL'),
    (202, 'halka', '12x5 mm 8x4 - 8/4 Havşa', 'havşa2.jpg', '25.00 TL'),
    (203, 'halka', '15x5 mm - 10/5,5 Havşa', '23.jpg', '33.52 TL'),
    (204, 'halka', '18x5 mm - 10/5,5 Havşa', '24.jpg', '42.00 TL'),
    (205, 'halka', '20x5 mm - 10/5,5 Havşa', '25.jpg', '56.16 TL'),
    (206, 'halka', '25x5 mm - 10/5,5 Havşa', '26.jpg', '72.00 TL'),
    (207, 'halka', '30x5 mm - 10/5 Havşa', '27.jpg', '84.00 TL'),
    (208, 'halka', '40x5 mm - 10/5 Havşa', '28.jpg', '179.40 TL')
]

with app.app_context():
    db.create_all()
    if Product.query.count() == 0:
        for p_id, p_cat, p_name, p_file, p_price in DEFAULT_PRODUCTS:
            new_product = Product(id=p_id, category=p_cat, name=p_name, file=p_file, price=p_price)
            db.session.add(new_product)
        db.session.commit()

# --- Ortak Stil ve Header Fonksiyonu (Admin Butonu Kaldırıldı) ---
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
    .products-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px; margin-bottom: 40px; }
    .product-card { background:#fff; padding:15px; border-radius:12px; text-align:center; transition: 0.3s; border: 1px solid #eee; display: flex; flex-direction: column; justify-content: space-between; }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    .product-card img { width:100%; height:180px; object-fit:contain; background: #fff; border-radius:8px; }
    .title { font-weight: bold; margin: 12px 0; height: 40px; overflow: hidden; color:#0b1a3d; font-size: 15px; }
    .price { color: #e67e22; font-size: 1.2em; font-weight: bold; margin-bottom:12px; }
    .add-btn { background:#0b1a3d; color:#fff; text-decoration:none; padding:10px; border-radius:6px; font-weight:bold; }
    .add-btn:hover { background:#ffd700; color:#0b1a3d; }
    
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

def render_products(prod_list):
    if not prod_list:
        return "<p style='color:black;'>Ürün bulunamadı.</p>"
    html = ""
    for p in prod_list:
        html += f"""
        <div class="product-card">
            <img src="/static/{p.file}" alt="{p.name}">
            <div>
                <div class="title">{p.name}</div>
                <div class="price">{p.price}</div>
                <a class="add-btn" href="/add_to_cart/{p.id}">Sepete Ekle</a>
            </div>
        </div>
        """
    return html

def get_cart():
    cart = session.get("cart", {})
    return cart if isinstance(cart, dict) else {}

# --- Müşteri (Önyüz) Route'ları ---

@app.route("/")
def index():
    yuvarlak_list = Product.query.filter_by(category='yuvarlak').all()
    dikdortgen_list = Product.query.filter_by(category='dikdortgen').all()
    halka_list = Product.query.filter_by(category='halka').all()
    
    all_content = f"""
    <div id="yuvarlak" class="products-section">
        <h2 style="background:#0b1a3d; color:white; padding:12px; border-radius:8px; font-size:1.2em;">Yuvarlak Mıknatıslar</h2>
        <div class="products-grid">{render_products(yuvarlak_list)}</div>
    </div>
    <div id="dikdortgen" class="products-section">
        <h2 style="background:#0b1a3d; color:white; padding:12px; border-radius:8px; font-size:1.2em;">Dikdörtgen Mıknatıslar</h2>
        <div class="products-grid">{render_products(dikdortgen_list)}</div>
    </div>
    <div id="havsali" class="products-section">
        <h2 style="background:#0b1a3d; color:white; padding:12px; border-radius:8px; font-size:1.2em;">Halka (Havşalı) Mıknatıslar</h2>
        <div class="products-grid">{render_products(halka_list)}</div>
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
    filtered = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
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
        p = Product.query.get(product_id)
        if p:
            cart[str_id] = {"id": p.id, "name": p.name, "price": p.price, "quantity": 1}
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
        try:
            price_val = float(v["price"].replace(" TL", "").replace(".", "").replace(",", "."))
        except:
            price_val = 0.0
        
        sub = price_val * v["quantity"]
        total += sub
        items_html += f"""
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #eee; padding:15px 0;">
            <div style="flex:2;"><b>{v['name']}</b></div>
            <div style="flex:1; text-align:center;">
                <a href="/remove_from_cart/{v['id']}" style="text-decoration:none; padding:5px 10px; background:#eee; color:black; border-radius:5px;">-</a>
                <span style="margin:0 10px;">{v['quantity']}</span>
                <a href="/add_to_cart/{v['id']}" style="text-decoration:none; padding:5px 10px; background:#eee; color:black; border-radius:5px;">+</a>
            </div>
            <div style="flex:1; text-align:right; font-weight:bold; color:#e67e22;">{sub:,.2f} TL</div>
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
            <h1>🛒 Sepetiniz</h1>
            {items_html if items_html else "<p>Sepetiniz boş.</p>"}
            <div style="text-align:right; margin-top:20px;">
                <h3>Toplam: {total:,.2f} TL</h3>
            </div>
            <div style="display:flex; flex-direction:column; gap:10px; margin-top:20px;">
                <a href="https://wa.me/90536274599" style="text-decoration:none; background:#28a745; color:white; padding:15px; border-radius:8px; font-weight:bold; text-align:center;">✅ WhatsApp ile Siparişi Tamamla</a>
                <a href="/" style="text-decoration:none; color:#0b1a3d; font-weight:bold; text-align:center;">⬅️ Alışverişe Devam Et</a>
            </div>
        </div>
    </body>
    </html>
    """)

# --- GİZLİ YÖNETİCİ (ADMIN) ROUTE'LARI (Tamamen Maskelendi) ---

@app.route("/erkam-ozel-yonetim-2026", methods=["GET", "POST"])
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
    <head><meta charset="utf-8"><title>404 Not Found</title><style>{get_common_styles()}</style></head>
    <body>
        <div style="max-width:400px; margin:100px auto; background:white; padding:30px; border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.1); text-align:center;">
            <h2>Giriş</h2>
            <p style="color:red;">{error}</p>
            <form method="POST">
                <input type="password" name="password" placeholder="Güvenlik Anahtarı" style="width:100%; padding:10px; margin-bottom:15px; border:1px solid #ccc; border-radius:5px;" required>
                <button type="submit" style="background:#0b1a3d; color:white; border:none; padding:10px 20px; width:100%; border-radius:5px; cursor:pointer;">Yetkiyi Doğrula</button>
            </form>
        </div>
    </body></html>
    """)

@app.route("/erkam-cikis")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("index"))

@app.route("/erkam-panel-yonetimi")
def admin_panel():
    if not session.get("is_admin"):
        return redirect(url_for("index")) # Yetkisiz biri gelirse doğrudan ana sayfaya atar, hata bile vermez!
        
    def generate_table(category_key, title):
        products = Product.query.filter_by(category=category_key).all()
        rows = ""
        for p in products:
            rows += f"""
            <tr>
                <td>{p.id}</td>
                <td>{p.name}</td>
                <td>{p.price}</td>
                <td>{p.file}</td>
                <td><a href="/erkam-urun-duzenle/{p.id}" class="edit-btn">✏️ Düzenle</a></td>
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
    <head><meta charset="utf-8"><title>Yönetim Paneli</title><style>{get_common_styles()}</style></head>
    <body>
        <header><div class="header-container"><div class="logo"><h1>Gizli Yönetim Paneli</h1></div></div></header>
        <div style="max-width:1200px; margin:20px auto; padding:20px; background:white; border-radius:10px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h2>⚙️ Ürün Yönetim Masası</h2>
                <div>
                    <a href="/" style="color:#0b1a3d; text-decoration:none; font-weight:bold; margin-right:20px;">🌐 Siteye Git</a>
                    <a href="/erkam-cikis" style="color:red; text-decoration:none; font-weight:bold;">🚪 Güvenli Çıkış</a>
                </div>
            </div>
            <p>Bu alan tamamen gizlidir. Sadece sizin tarayıcı oturumunuza özel olarak açık tutulur.</p>
            
            {generate_table("yuvarlak", "Yuvarlak Mıknatıslar")}
            {generate_table("dikdortgen", "Dikdörtgen Mıknatıslar")}
            {generate_table("halka", "Halka (Havşalı) Mıknatıslar")}
            
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/erkam-urun-duzenle/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    if not session.get("is_admin"):
        return redirect(url_for("index"))
        
    product = Product.query.get_or_404(product_id)
    
    if request.method == "POST":
        product.name = request.form.get("name")
        product.price = request.form.get("price")
        product.file = request.form.get("file")
        db.session.commit()
        return redirect(url_for("admin_panel"))

    return render_template_string(f"""
    <html>
    <head><meta charset="utf-8"><title>Ürün Düzenle</title><style>{get_common_styles()}</style></head>
    <body>
        <div style="max-width:500px; margin:50px auto; background:white; padding:30px; border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.1);">
            <h2 style="color:#0b1a3d;">✏️ Ürün Düzenle</h2>
            <form method="POST">
                <div style="margin-bottom:15px;">
                    <label style="font-weight:bold;">Ürün Adı:</label>
                    <input type="text" name="name" value="{product.name}" style="width:100%; padding:10px; margin-top:5px; border:1px solid #ccc; border-radius:5px;" required>
                </div>
                <div style="margin-bottom:15px;">
                    <label style="font-weight:bold;">Fiyat (Örn: 15.00 TL):</label>
                    <input type="text" name="price" value="{product.price}" style="width:100%; padding:10px; margin-top:5px; border:1px solid #ccc; border-radius:5px;" required>
                </div>
                <div style="margin-bottom:25px;">
                    <label style="font-weight:bold;">Görsel Dosya Adı (Örn: 1.jpg):</label>
                    <input type="text" name="file" value="{product.file}" style="width:100%; padding:10px; margin-top:5px; border:1px solid #ccc; border-radius:5px;" required>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <a href="/erkam-panel-yonetimi" style="background:#ccc; color:black; padding:10px 20px; text-decoration:none; border-radius:5px;">İptal</a>
                    <button type="submit" style="background:#27ae60; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">💾 Kaydet</button>
                </div>
            </form>
        </div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(debug=True)
