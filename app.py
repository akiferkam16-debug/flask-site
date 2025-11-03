from flask import Flask, session, redirect, request, render_template_string, url_for

app = Flask(__name__)
app.secret_key = "4416"

@app.route('/google522b3008e358c667.html')
def google_verify():
    return "google-site-verification: google522b3008e358c667.html"


# --- Yuvarlak ürünler ---
products = [
    {"id": 1, "name": "4x2 mm Yuvarlak", "file": "1.jpg", "price": "3.00 TL"},
    {"id": 2, "name": "8x3 mm Yuvarlak", "file": "2.jpg", "price": "6.00 TL"},
    {"id": 3, "name": "15x3 mm Yuvarlak", "file": "3.jpg", "price": "12.00 TL"},
    {"id": 4, "name": "10x5 mm Yuvarlak", "file": "10x5 12 tl.jpg", "price": "12.00 TL"},
    {"id": 5, "name": "18x2 mm Yuvarlak", "file": "7.jpg", "price": "14.00 TL"},
    {"id": 6, "name": "40x5 mm Yuvarlak", "file": "6.jpg", "price": "170.00 TL"},
]

# --- Dikdörtgen ürünler ---
rectangle_products = [
    {"id": 101, "name": "10x5x2 mm Dikdörtgen", "file": "4.jpg", "price": "6.00 TL"},
    {"id": 102, "name": "20x10x5 mm Dikdörtgen", "file": "20x10x5.jpg", "price": "9.00 TL"},
    {"id": 103, "name": "30x10x5 mm Dikdörtgen", "file": "30x10x5 77tl.jpg", "price": "11.00 TL"},
    {"id": 104, "name": "15x15x5 mm Dikdörtgen", "file": "15x15x5.jpg", "price": "14.00 TL"},
]

@app.route("/")
def index():
    # Yuvarlak ürünler HTML
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

    # Dikdörtgen ürünler HTML
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

    return f"""
    <html>
    <head>
        <meta charset="utf-8">
         <meta name="google-site-verification" content="z32f-tdI6mzvK-nC_96Q8POA6Hwmia2kqVMh-L9dEq4" />

        <title>Erkam Mıknatıs</title>
        <style>
            body {{
                margin:0;
                font-family: Arial, sans-serif;
                background:#111;
                color:#fff;
                display:flex;
                flex-direction:column;
                min-height:100vh;
            }}
            header {{
                display:flex;
                justify-content:space-between;
                align-items:center;
                padding:10px 20px;
            }}
            .logo {{
                text-align:center;
                flex:1;
            }}
            .logo img {{
                max-height:60px;
            }}
            .logo h1 {{
                margin:5px 0 0 0;
                font-size:28px;
            }}
            .cart-link {{
                color:#ffd700;
                text-decoration:none;
                font-weight:bold;
                transition: all 0.2s ease;
            }}
            .cart-link:hover {{
                transform: scale(1.1);
                color:#ffea00;
            }}
            main {{
                flex:1;
                padding:20px;
            }}
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
                grid-template-columns: repeat(2, 1fr);
                gap:20px;
                justify-items:center;
            }}
            .product-card {{
                background:#222;
                border-radius:12px;
                padding:12px;
                width:180px;
                text-align:center;
                box-shadow:0 4px 12px rgba(0,0,0,0.5);
                transition: transform 0.3s, box-shadow 0.3s;
            }}
            .product-card:hover {{
                transform: translateY(-8px) scale(1.05);
                box-shadow:0 10px 20px rgba(0,0,0,0.7);
            }}
            .product-card img {{
                max-width:100%;
                border-radius:6px;
                margin-bottom:8px;
                transition: transform 0.3s;
            }}
            .product-card img:hover {{
                transform: scale(1.05);
            }}
            .title {{ font-weight:bold; margin-bottom:4px; }}
            .price {{ color:#cfcfcf; margin-bottom:8px; }}
            .add-btn {{
                background:#ffd700;
                color:#111;
                text-decoration:none;
                padding:6px 12px;
                border-radius:6px;
                font-weight:bold;
                display:inline-block;
                transition: all 0.3s ease;
            }}
            .add-btn:hover {{
                background:#ffea00;
                transform: scale(1.05);
            }}
            .checkout-btn {{
                background:green;
                color:#fff;
                text-decoration:none;
                padding:8px 16px;
                border-radius:6px;
                font-weight:bold;
                display:inline-block;
                margin-top:15px;
                transition: all 0.3s ease;
            }}
            .checkout-btn:hover {{
                background:darkgreen;
                transform: scale(1.05);
            }}
            footer {{
                background:#1a1a1a;
                text-align:center;
                padding:14px 0;
                font-size:14px;
                color:#bbb;
            }}
        </style>
    </head>
    <body>
        <header>
            <a class="cart-link" href="/cart">🛒 Sepeti Görüntüle</a>
            <div class="logo">
                <img src="/static/logo.jpg" alt="Logo">
                <h1>Erkam Mıknatıs</h1>
            </div>
            <div style="width:100px;"></div>
        </header>
        <main>
            <!-- Yuvarlak Ürünler -->
            <div class="products-section">
                <h2>Yuvarlak Ürünler</h2>
                <div class="products-grid">
                    {product_html}
                </div>
            </div>

            <!-- Dikdörtgen Ürünler -->
            <div class="products-section">
                <h2>Dikdörtgen Ürünler</h2>
                <div class="products-grid">
                    {rectangle_html}
                </div>
            </div>
        </main>
    </body>
    </html>
    """

# --- Sepete ekleme ---
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", [])
    for product in products + rectangle_products:
        if product["id"] == product_id:
            cart.append(product)
            break
    session["cart"] = cart
    return redirect("/cart")

# --- Sepeti görüntüle ---
@app.route("/cart")
def cart_page():
    cart = session.get("cart", [])
    cart_html = ""
    total = 0
    for idx, item in enumerate(cart):
        price = float(item["price"].replace(" TL","").replace(",",".")) 
        total += price
        cart_html += f"""
        <li style='font-size:18px; margin:10px 0; display:flex; justify-content: space-between; align-items: center;'>
            <span>{item['name']} - {item['price']}</span>
            <a href='{url_for('remove_from_cart', index=idx)}' style='color:red; text-decoration:none; font-weight:bold;'>❌ Sil</a>
        </li>
        """
    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Sepetiniz</title>
        <style>
            body {{ background:#333; color:#fff; font-family:Arial; text-align:center; padding:30px; }}
            ul {{ list-style:none; padding:0; max-width:500px; margin:0 auto; text-align:left; }}
            .total {{ font-size:22px; font-weight:bold; margin-top:20px; }}
            a {{ color:yellow; text-decoration:underline; font-size:18px; transition:0.2s; }}
            a:hover {{ color:#ff0; }}
            .checkout-btn {{ margin-top:20px; padding:10px 20px; font-size:20px; background:green; color:#fff; border:none; border-radius:8px; cursor:pointer; transition:0.3s; display:inline-block; }}
            .checkout-btn:hover {{ background:darkgreen; transform:scale(1.05); }}
        </style>
    </head>
    <body>
        <h1>🛒 Sepetiniz</h1>
        <ul>{cart_html if cart_html else '<li>Sepet boş.</li>'}</ul>
        <p class="total">Toplam: {total:.2f} TL</p>
        <div>
            <p><a href="/">⬅️ Alışverişe Geri Dön</a></p>
            <a class="checkout-btn" href="#">💳 Sepeti Onayla</a>
        </div>
    </body>
    </html>
    """

# --- Sepetten sil ---
@app.route("/remove_from_cart/<int:index>")
def remove_from_cart(index):
    cart = session.get("cart", [])
    if 0 <= index < len(cart):
        cart.pop(index)
        session["cart"] = cart
    return redirect("/cart")

if __name__=="__main__":
    app.run(debug=True)
