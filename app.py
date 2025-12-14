# --- Ana Sayfa Route'u (YENİ MOBİL UYUM KURALLARI İLE GÜNCELLENDİ) ---
@app.route("/")
def index():
    def create_product_html(prod_list):
        """Ürün listesinden HTML kartlarını oluşturur."""
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

    # Ürün bloklarını content div'i içine girecek şekilde birleştirme
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
            /* --- Genel Stil (Masaüstü) --- */
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
                background:#f8f8f8; 
                border-bottom: 1px solid #eee;
            }}
            .logo {{
                text-align:center;
                flex:1;
            }}
            .logo h1 {{
                margin:5px 0 0 0;
                font-size:28px;
                color:#0b1a3d;
            }}
            .cart-link {{
                color:#0b1a3d;
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
            
            /* Ana Düzen (page-layout) - Masaüstü görünümü */
            main {{
                flex:1;
                padding:20px 0; 
            }}
            .page-layout {{
                display: flex; 
                gap: 20px;
                align-items: flex-start; 
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 20px; 
            }}
            .category-sidebar {{
                width: 250px; 
                padding: 15px;
                background: #f4f4f4;
                border-radius: 8px;
                position: sticky; 
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
                transition: color 0.2s, background 0.2s, padding 0.2s;
            }}
            .category-sidebar a:hover {{
                color: #ffd700;
                background: #0b1a3d;
                padding-left: 10px;
                border-radius: 4px;
            }}
            
            .content {{
                flex: 1; 
                min-width: 0; 
            }}
            
            /* Ürün Kartları - Masaüstü */
            .products-section {{
                background:#0b1a3d; /* Lacivert kutu */
                padding:20px;
                border-radius:12px;
                margin-top:15px;
                color: #fff;
            }}
            .products-section h2 {{
                text-align:center;
                margin-bottom:20px;
                color:#ffd700;
            }}
            .products-grid {{
                display:grid;
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); 
                gap:20px;
                justify-items:center;
            }}
            .product-card {{
                background:#222;
                border-radius:12px;
                padding:12px;
                width:200px; 
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
                height:150px; 
                object-fit: cover; 
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
                margin-top: auto;
            }}


            /* ------------------------------------------------------------------- */
            /* --- MOBİL UYUMLULUK (RESPONSIVE DESIGN) BAŞLANGIÇ --- */
            @media (max-width: 768px) {{
                /* 1. Header Düzenlemesi */
                header {{
                    flex-direction: column; 
                    padding: 10px;
                }}
                .logo {{
                    order: -1; 
                    margin-bottom: 10px;
                }}
                .cart-link {{
                    order: 1; 
                    margin-top: 10px;
                }}
                .logo h1 {{
                    font-size: 24px;
                }}
                header div[style="width:100px;"] {{
                    display: none;
                }}

                /* 2. Ana Sayfa Düzenlemesi (page-layout) */
                .page-layout {{
                    flex-direction: column; 
                    gap: 15px;
                    padding: 0 10px; 
                }}

                /* 3. Kategori Menüsü (Sidebar) DÜZELTİLDİ */
                .category-sidebar {{
                    width: 100%; 
                    position: static; 
                    padding: 10px; 
                    background: #f8f8f8; /* Beyaz/açık arka plan */
                    border: 1px solid #ddd;
                    border-radius: 8px;
                }}
                .category-sidebar h3 {{
                    color: #0b1a3d;
                    text-align: center;
                    margin-bottom: 5px;
                    border-bottom: none;
                }}
                /* Telefon için: Kategoriler sağda alt alta (float ile) */
                .category-sidebar a {{
                    display: block; 
                    padding: 4px 0;
                    margin: 2px 0;
                    text-align: right; /* Sağa yaslama */
                    color: #0b1a3d;
                    border: none;
                }}
                .category-sidebar a:hover {{
                    background: #eee;
                    padding-right: 5px; 
                    padding-left: 0; 
                }}
                
                /* 4. Ürün Bölümleri DÜZELTİLDİ (Lacivert Kutular Silindi) */
                .products-section {{
                    background: none; /* Lacivert kutu kaldırıldı */
                    padding: 0;
                    border-radius: 0;
                    margin-top: 15px;
                    color: #000; /* Yazı rengi siyaha çevrildi */
                }}
                .products-section h2 {{
                    color: #0b1a3d; /* Başlık rengi */
                    text-align: left;
                    margin-bottom: 15px;
                    padding-left: 5px;
                    border-bottom: 2px solid #0b1a3d;
                    padding-bottom: 5px;
                }}
                
                /* 5. Ürün Izgarası DÜZELTİLDİ (İkili İkili Düzen) */
                .products-grid {{
                    grid-template-columns: repeat(2, 1fr); /* İkili Sütun */
                    gap: 10px; /* Boşluk azaltıldı */
                }}
                
                /* Ürün kartının stilini mobil için sadeleştirme */
                .product-card {{
                    width: 100%; /* Sütun genişliğini doldur */
                    padding: 8px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    background: #fff; /* Arka plan beyaz */
                    color: #000; /* Yazı rengi siyah */
                }}
                .product-card:hover {{
                    transform: none; /* Hover efekti kaldırıldı */
                    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                }}
                .product-card img {{
                    height: 100px; /* Küçük resimler */
                }}
                .price {{
                    color: #E60000; /* Fiyatı daha görünür bir renge çevirebiliriz */
                    font-size: 1em;
                }}
                .add-btn {{
                    padding: 4px 8px;
                    font-size: 0.9em;
                }}
            }}
            /* --- MOBİL UYUMLULUK SONU --- */
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
    """, all_products_content=all_products_content)


# --- Sepete ekleme, Sepeti görüntüle, Sepetten sil fonksiyonları aynı kalmıştır ---
# ... (Diğer fonksiyonlar yukarıdaki son tam kodda olduğu gibi kalır) ...
# (Yer kaplamaması için bu kısım burada tekrar edilmemiştir.)

# if __name__=="__main__":
#     app.run(debug=True)
