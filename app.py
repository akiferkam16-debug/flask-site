import os
from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "gizli-anahtar-buraya"

# --- Veritabanı Ayarları (Klasik ve Kesin Çözüm) ---
db_url = os.environ.get("DATABASE_URL", "sqlite:///products.db")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Veritabanı Modeli ---
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(250), nullable=True)
    description = db.Column(db.Text, nullable=True)

with app.app_context():
    db.create_all()

# --- Ortak Stil ve Header Fonksiyonu ---
def get_header_html():
    return """
    <header style="background:#111; color:#fff; padding:15px 30px; display:flex; justify-content:space-between; align-items:center;">
        <h1 style="margin:0; font-size:20px;"><a href="/" style="color:#fff; text-decoration:none;">Erkam Mıknatıs</a></h1>
        <nav>
            <a href="/" style="color:#ddd; text-decoration:none; margin-left:20px;">Ana Sayfa</a>
            <a href="/cart" style="color:#ddd; text-decoration:none; margin-left:20px;">Sepetim</a>
        </nav>
    </header>
    """

# --- Sepet Fonksiyonu ---
def get_cart():
    cart = session.get("cart", {})
    return cart if isinstance(cart, dict) else {}

# --- Müşteri Route'ları ---
@app.route("/")
def index():
    category = request.args.get("category")
    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    
    html = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Erkam Mıknatıs - Ürünler</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin:0; padding:0; background:#f4f4f4; }}
            .container {{ width: 80%; margin: 20px auto; }}
            .products-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; }}
            .product-card {{ background: #fff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center; }}
            .product-card img {{ max-width: 100%; height: 150px; object-fit: cover; border-radius: 4px; }}
            .btn {{ background: #007bff; color: white; padding: 8px 15px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; margin-top: 10px; }}
            .btn:hover {{ background: #0056b3; }}
            .categories {{ margin-bottom: 20px; text-align: center; }}
            .categories a {{ margin: 0 10px; text-decoration: none; color: #007bff; font-weight: bold; }}
        </style>
    </head>
    <body>
        {get_header_html()}
        <div class="container">
            <h2 style="text-align:center;">Ürünlerimiz</h2>
            <div class="categories">
                <a href="/">Tümü</a>
                <a href="/?category=neodimyum">Neodimyum Mıknatıs</a>
                <a href="/?category=surgu">Sürgü Mıknatıs</a>
            </div>
            <div class="products-grid">
    """
    for p in products:
        img_tag = f'<img src="{p.image}" alt="{p.name}">' if p.image else '<div style="height:150px; background:#eee; line-height:150px; color:#888;">Resim Yok</div>'
        html += f"""
                <div class="product-card">
                    {img_tag}
                    <h3>{p.name}</h3>
                    <p style="color:green; font-weight:bold;">{p.price} TL</p>
                    <a href="/product/{p.id}" class="btn">İncele</a>
                </div>
        """
    html += """
            </div>
        </div>
    </body>
    </html>
    """
    return html

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    p = Product.query.get_or_404(product_id)
    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head><title>{p.name} - Erkam Mıknatıs</title></head>
    <body style="font-family:Arial, sans-serif; background:#f4f4f4; margin:0;">
        {get_header_html()}
        <div style="width:60%; margin:30px auto; background:#fff; padding:20px; border-radius:8px;">
            <h2>{p.name}</h2>
            <p style="color:green; font-size:20px; font-weight:bold;">{p.price} TL</p>
            <p>{p.description or 'Açıklama bulunmuyor.'}</p>
            <form action="/add-to-cart/{p.id}" method="POST">
                <button type="submit" style="background:green; color:#fff; padding:10px 20px; border:none; border-radius:4px; cursor:pointer;">Sepete Ekle</button>
            </form>
            <br><a href="/">← Ana Sayfaya Dön</a>
        </div>
    </body>
    </html>
    """

@app.route("/add-to-cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    cart = get_cart()
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session["cart"] = cart
    return redirect(url_for("cart_page"))

@app.route("/cart")
def cart_page():
    cart = get_cart()
    total = 0
    items_html = ""
    for pid_str, qty in cart.items():
        p = Product.query.get(int(pid_str))
        if p:
            subtotal = p.price * qty
            total += subtotal
            items_html += f"<li>{p.name} - {qty} Adet x {p.price} TL = <b>{subtotal} TL</b></li>"

    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head><title>Sepetim - Erkam Mıknatıs</title></head>
    <body style="font-family:Arial, sans-serif; background:#f4f4f4; margin:0;">
        {get_header_html()}
        <div style="width:60%; margin:30px auto; background:#fff; padding:20px; border-radius:8px;">
            <h2>Alışveriş Sepetiniz</h2>
            <ul>{items_html if items_html else "Sepetiniz boş."}</ul>
            <h3>Toplam Tutar: {total} TL</h3>
            <a href="/" style="background:#007bff; color:#fff; padding:8px 15px; text-decoration:none; border-radius:4px; display:inline-block;">Alışverişe Devam Et</a>
        </div>
    </body>
    </html>
    """

# --- GİZLİ YÖNETİCİ (ADMIN) ROUTE'LARI ---
@app.route("/erkam-ozel-yonetim-2026", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == "erkam2026*": # Yönetici şifren (İstediğin gibi değiştirebilirsin)
            session["is_admin"] = True
            return redirect(url_for("admin_panel"))
        return "Hatalı Şifre!", 403
    return """
    <form method="POST" style="width:300px; margin:100px auto; font-family:Arial;">
        <h3>Yönetici Girişi</h3>
        <input type="password" name="password" placeholder="Şifre" style="width:100%; padding:8px; margin-bottom:10px;">
        <button type="submit" style="width:100%; padding:8px; background:#000; color:#fff; border:none;">Giriş Yap</button>
    </form>
    """

@app.route("/erkam-panel-yonetimi", methods=["GET", "POST"])
def admin_panel():
    if not session.get("is_admin"):
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name")
        price = float(request.form.get("price", 0))
        category = request.form.get("category")
        image = request.form.get("image")
        description = request.form.get("description")
        
        new_p = Product(name=name, price=price, category=category, image=image, description=description)
        db.session.add(new_p)
        db.session.commit()
        return redirect(url_for("admin_panel"))

    products = Product.query.all()
    rows = ""
    for p in products:
        rows += f"<tr><td>{p.id}</td><td>{p.name}</td><td>{p.price} TL</td><td>{p.category}</td><td><a href='/admin/delete/{p.id}' style='color:red;'>Sil</a></td></tr>"

    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head><title>Admin Paneli</title></head>
    <body style="font-family:Arial, sans-serif; background:#f4f4f4; padding:20px;">
        <h2>Admin Paneli - Ürün Yönetimi</h2>
        <a href="/admin-logout" style="color:red; font-weight:bold;">Çıkış Yap</a> | <a href="/">Ana Sayfa</a>
        <hr>
        <h3>Yeni Ürün Ekle</h3>
        <form method="POST" style="background:#fff; padding:15px; border-radius:5px; width:400px; display:flex; flex-direction:column; gap:10px;">
            <input type="text" name="name" placeholder="Ürün Adı" required style="padding:8px;">
            <input type="number" step="0.01" name="price" placeholder="Fiyat (TL)" required style="padding:8px;">
            <input type="text" name="category" placeholder="Kategori (örn: neodimyum)" required style="padding:8px;">
            <input type="text" name="image" placeholder="Resim URL'si" style="padding:8px;">
            <textarea name="description" placeholder="Ürün Açıklaması" style="padding:8px;"></textarea>
            <button type="submit" style="background:green; color:#fff; padding:10px; border:none; cursor:pointer;">Ürünü Ekle</button>
        </form>
        <hr>
        <h3>Mevcut Ürünler</h3>
        <table border="1" cellpadding="10" style="background:#fff; border-collapse:collapse; width:100%;">
            <tr><th>ID</th><th>Ürün Adı</th><th>Fiyat</th><th>Kategori</th><th>İşlem</th></tr>
            {rows}
        </table>
    </body>
    </html>
    """

@app.route("/admin/delete/<int:id>")
def admin_delete(id):
    if not session.get("is_admin"):
        return redirect(url_for("index"))
    p = Product.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for("admin_panel"))

@app.route("/admin-logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
