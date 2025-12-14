from flask import Flask, session, redirect, request, render_template_string, url_for

app = Flask(__name__)
# Gizli anahtar: Uygulama çalışırken oturum (session) verilerini şifrelemek için kullanılır.
app.secret_key = "4416"

# Google doğrulama (değişiklik yok)
@app.route('/google522b3008e358c667.html')
def google_verify():
    return "google-site-verification: google522b3008e358c667.html"


# --- Ürün Verileri ---
# Ürün verileri aynı bırakılmıştır
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

@app.route("/")
def index():
    # Ürün kartları HTML'ini oluşturma kısmı aynı kalmıştır.
    product_html = ""
    for p in products:
        product_html += f"""
        <div class="product-card">
            <img src="/static/{p['file']}" alt="{p['name']}">
            <div class="title">{p['name']}</div>
            <div class="price">{p['price']}</div>
            <a class="add-btn" href="{url_for('add_to_cart', product_id=p['id'])}">Sepete Ekle</a>
        </div>
        """

    rectangle_html = ""
    for p in rectangle_products:
        rectangle_html += f"""
        <div class="product-card">
            <img src="/static/{p['file']}" alt="{p['name']}">
            <div class="title">{p['name']}</div>
            <div class="price">{p['price']}</div>
            <a class="add-btn" href="{url_for('add_to_cart', product_id=p['id'])}">Sepete Ekle</a>
        </div>
        """

    # Mantıksal olarak ayrılmış ürün bloklarını birleştirme
    all_products_content = f"""
    <a id="yuvarlak"></a>
    <div class="products-section">
        <h2>Yuvarlak Ürünler</h2>
        <div class="products-grid">
            {product_html}
        </div>
    </div>

    <a id="dikdortgen"></a>
    <div class="products-section">
        <h2>Dikdörtgen Ürünler</h2>
        <div class="products-grid">
            {rectangle_html}
        </div>
    </div>
    """

    # --- HTML Şablonu (Tekrar Kullanılabilir ve Düzeltilmiş) ---
    return render_template_string(f"""
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="google-site-verification" content="z32f-tdI6mzvK-nC_96Q8POA6Hwmia2kqVMh-L9dEq4" />
        <title>Erkam Mıknatıs</title>
        <link rel="icon" href="/static/favicon.png" sizes="192x192">
        <link rel="apple-touch-icon" href="/static/favicon.png">
        <meta name="description" content="Erkam Mıknatıs: Yuvarlak, dikdörtgen, halka ve özel mıknatıs çeşitleri. Uygun fiyat, hızlı kargo, güvenilir hizmet.">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="author" content="Erkam Mıknatıs">
        <meta name="robots" content="index, follow">

        <style>
            /* Genel Stil Düzeltmeleri */
            body {{
                margin:0;
                font-family: Arial, sans-serif;
                background:#fff;
                color:#000;
                display:flex;
                flex-direction:column;
                min-height:100vh;
            }}
            
            /* Header */
            header {{
                display:flex;
                justify-content:space-between;
                align-items:center;
                padding:10px 20px;
                background:#f8f8f8; /* Header için arka plan eklendi */
                border-bottom: 1px solid #eee;
            }}
            .logo {{
                text-align:center;
                flex:1;
            }}
            .logo img {{ max-height:60px; }}
            .logo h1 {{
                margin:5px 0 0 0;
                font-size:28px;
                color:#0b1a3d; /* Logo rengi */
            }}
            .cart-link {{
                color:#0b1a3d; /* Sepet linki rengi düzeltildi */
                text-decoration:none;
                font-weight:bold;
                transition: all 0.2s ease;
                padding: 8px 12px;
                border: 1px solid #0b1a3d;
                border-radius: 4px;
            }}
            .cart-link:hover {{
                transform: scale(1.05);
                background: #0b1a3d;
                color: #ffd700;
            }}
            
            /* Main & Layout Düzeltmesi */
            main {{
                flex:1;
                padding:20px;
            }}
            .page-layout {{
                display: flex; /* Ana hatayı çözen satır: Flexbox ile yan yana düzenleme */
                gap: 20px;
                align-items: flex-start; /* İçeriğin yukarıdan başlaması */
                max-width: 1200px;
                margin: 0 auto;
            }}
            .category-sidebar {{
                width: 250px; /* Sabit genişlik */
                padding: 15px;
                background: #f4f4f4;
                border-radius: 8px;
                position: sticky; /* Sayfa kayarken menünün görünür kalması */
                top: 20px;
            }}
            .category-sidebar h3 {{
                color: #0b1a3d;
                border-bottom: 2px solid #ddd;
                padding-bottom: 10px;
                margin-top: 0;
            }}
            .category-sidebar a {{
                display: block;
                padding: 8px 0;
                text-decoration: none;
                color: #555;
                font-weight: bold;
                transition: color 0.2s;
            }}
            .category-sidebar a:hover {{
                color: #ffd700;
                background: #0b1a3d;
                padding-left: 10px;
                border-radius: 4px;
            }}
            
            .content {{
                flex: 1; /* Geri kalan tüm alanı kaplar */
                min-width: 0; /* Flexbox düzeltmesi */
            }}
            
            /* Ürün Bölümleri (Stiller aynı bırakıldı) */
            .products-section {{
                background:#0b1a3d;
                padding:20px;
                border-radius:12px;
                margin-top:15px;
            }}
            .products-section h2 {{
                text-align:center;
                margin-bottom:20px;
                color:#ffd700;
            }}
            .products-grid {{
                display:grid;
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); /* Daha duyarlı ızgara */
                gap:20px;
                justify-items:center;
            }}
            /* ... Diğer ürün kartı stilleri aynı kalmıştır ... */
            .product-card {{
                background:#222;
                border-radius:12px;
                padding:12px;
                width:200px; /* Genişlik artırıldı */
                text-align:center;
                box-shadow:0 4px 12px rgba(0,0,0,0.5);
                transition: transform 0.3s, box-shadow 0.3s;
                color:#fff;
            }}
            .product-card:hover {{
                transform: translateY(-8px) scale(1.03);
                box-shadow:0 10px 20px rgba(0,0,0,0.7);
            }}
            .product-card img {{
                max-width:100%;
                height:150px; /* Sabit yükseklik eklendi */
                object-fit: cover; /* Resmi sığdırma */
                border-radius:6px;
                margin-bottom:8px;
                transition: transform 0.3s;
            }}
            .title {{ font-weight:bold; margin-bottom:4px; }}
            .price {{ color:#ffd700; margin-bottom:8px; font-size: 1.2em; }}
            .add-btn {{
                background:#ffd700;
                color:#111;
                text-decoration:none;
                padding:8px 16px;
                border-radius:6px;
                font-weight:bold;
                display:inline-block;
                transition: all 0.3s ease;
            }}
            .add-btn:hover {{
                background:#ffea00;
                transform: scale(1.05);
            }}

            /* Footer */
            footer {{
                background:#1a1a1a;
                text-align:center;
                padding:14px 0;
                font-size:14px;
                color:#bbb;
                margin-top: auto; /* Footer'ı sayfanın altına iter */
            }}
        </style>
    </head>
    <body>
        <p style="display:none;">
            Erkam Mıknatıs, yuvarlak ve dikdörtgen mıknatıs satışında uzmanlaşmış bir firmadır.
        </p>

        <header>
            <a class="cart-link" href="{url_for('cart_page')}">🛒 Sepeti Görüntüle</a>
            <div class="logo">
                <h1>Erkam Mıknatıs</h1>
            </div>
            <div style="width:100px;"></div>
        </header>

        <main>
            <div class="page-layout">
                <aside class="category-sidebar">
                    <h3>Kategoriler</h3>
                    <a href="#yuvarlak">Yuvarlak Ürünler</a>
                    <a href="#dikdortgen">Dikdörtgen Ürünler</a>
                </aside>

                <div class="content">
                    {all_products_content} 
                </div> 
            </div> 
        </main>
        
        <footer>
            &copy; 2025 Erkam Mıknatıs. Tüm hakları saklıdır.
        </footer>
    </body>
    </html>
    """, product_html=product_html, rectangle_html=rectangle_html) # Bu satır aslında artık gereksiz çünkü yukarıda hepsi birleştirildi

# --- Sepete ekleme, Sepeti görüntüle, Sepetten sil fonksiyonları aynı kalmıştır ---

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", [])
    for product in products + rectangle_products:
        if product["id"] == product_id:
            # Ürünün sadece ID'sini ve ismini eklemek yerine, tam objeyi eklemek daha iyi
            cart.append(product)
            break
    session["cart"] = cart
    return redirect("/cart")

@app.route("/cart")
def cart_page():
    cart = session.get("cart", [])
    cart_html = ""
    total = 0.0
    for idx, item in enumerate(cart):
        try:
            # TL formatından float'a dönüştürme daha sağlam yapıldı
            price_str = item["price"].replace(" TL", "").replace(",", ".")
            price = float(price_str)
        except ValueError:
            price = 0.0 # Eğer fiyat hatalıysa 0 kabul et
            
        total += price
        cart_html += f"""
        <li style='font-size:18px; margin:10px 0; display:flex; justify-content: space-between; align-items: center;'>
            <span>{item['name']} - {item['price']}</span>
            <a href='{url_for('remove_from_cart', index=idx)}' style='color:#ffd700; text-decoration:none; font-weight:bold;'>❌ Sil</a>
        </li>
        """
    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Sepetiniz</title>
        <style>
            body {{ background:#0b1a3d; color:#fff; font-family:Arial; text-align:center; padding:30px; min-height:100vh; display:flex; flex-direction:column; }}
            h1 {{ color:#ffd700; }}
            ul {{ list-style:none; padding:0; max-width:600px; margin:20px auto; text-align:left; background:#1e2a4a; padding:20px; border-radius:10px; }}
            .total {{ font-size:24px; font-weight:bold; margin-top:20px; color:#ffd700; }}
            a {{ color:#ffd700; text-decoration:underline; font-size:18px; transition:0.2s; }}
            a:hover {{ color:#ffea00; }}
            .checkout-btn {{ margin-top:20px; padding:10px 20px; font-size:20px; background:green; color:#fff; border:none; border-radius:8px; cursor:pointer; transition:0.3s; display:inline-block; }}
            .checkout-btn:hover {{ background:darkgreen; transform:scale(1.05); }}
        </style>
    </head>
    <body>
        <h1>🛒 Sepetiniz</h1>
        <ul>{cart_html if cart_html else '<li>Sepetinizde ürün bulunmamaktadır.</li>'}</ul>
        <p class="total">Toplam: {total:.2f} TL</p>
        <div>
            <p><a href="/">⬅️ Alışverişe Geri Dön</a></p>
            <a class="checkout-btn" href="#">💳 Sepeti Onayla</a>
        </div>
    </body>
    </html>
    """

@app.route("/remove_from_cart/<int:index>")
def remove_from_cart(index):
    cart = session.get("cart", [])
    if 0 <= index < len(cart):
        cart.pop(index)
        session["cart"] = cart
    return redirect("/cart")

if __name__=="__main__":
    # Üretim ortamında 'debug=True' kullanılmamalıdır.
    app.run(debug=True)
