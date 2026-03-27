import json

def process_data(data):
    cats = []
    for block in data:
        if "categoria" in block:
            cats.append(block)
        elif "categorias_adicionales" in block:
            cats.extend(block["categorias_adicionales"])
    return cats

html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Menú Punto y Coma</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Montserrat:wght@300;400;500;600&display=swap');
        
        :root {
            --primary: #1c1c1c;
            --secondary: #9e7f4c; /* Elegant Gold */
            --bg: #fdfaf6; /* Classic paper */
            --line: #dcd1c2;
        }

        @page {
            size: A4;
            margin: 12mm; /* Minimal margins for print */
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Montserrat', sans-serif;
            background: #cdcdcd; /* Screen fallback background */
            color: var(--primary);
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
            margin: 0;
            padding: 0;
            /* Do not use display: flex on body for print */
        }

        .document-wrapper {
            background: var(--bg);
            /* A4 size */
            width: 210mm;
            min-height: 297mm;
            margin: 10mm auto; /* centers on screen */
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            position: relative;
            padding: 8mm;
            box-sizing: border-box;
        }

        /* Decorative border */
        .page-border {
            border: 1px solid var(--secondary);
            padding: 10mm;
            min-height: 275mm;
        }

        @media print {
            body { background: none; margin: 0; display: block; }
            .document-wrapper {
                margin: 0;
                box-shadow: none;
                width: 100%;
                min-height: auto;
                padding: 0; 
                height: auto;
                page-break-after: always;
            }
            .page-border {
                border: 0;
                padding: 0;
                min-height: auto;
                height: auto;
            }
        }

        .header {
            text-align: center;
            padding-bottom: 6mm;
            margin-bottom: 6mm;
            border-bottom: 1px solid var(--secondary);
            position: relative;
        }
        
        /* A subtle diamond ornament */
        .header::after {
            content: "◆";
            position: absolute;
            bottom: -9px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--bg);
            padding: 0 10px;
            font-size: 14px;
            color: var(--secondary);
        }

        h1 {
            font-family: 'Cormorant Garamond', serif;
            font-size: 38pt;
            letter-spacing: 6px;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 2mm;
            margin-top: 10mm; /* Extra space at top since we removed border padding in print */
        }

        h2.subtitle {
            font-size: 11pt;
            letter-spacing: 4px;
            color: var(--secondary);
            font-weight: 400;
            text-transform: uppercase;
        }

        .content {
            column-count: 2;
            column-gap: 12mm;
            /* Approximate remaining height of A4 minus margins and header */
            height: auto; 
        }

        .category {
            break-inside: avoid;
            page-break-inside: avoid;
            margin-bottom: 8mm;
        }

        .cat-title {
            font-family: 'Cormorant Garamond', serif;
            font-size: 15pt;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 1px;
            text-align: center;
            font-weight: 600;
            margin-bottom: 1mm;
        }
        
        .cat-divider {
            text-align: center;
            color: var(--secondary);
            margin-bottom: 4mm;
            font-size: 10pt;
            letter-spacing: 2px;
        }

        .item {
            margin-bottom: 3.5mm;
            break-inside: avoid;
            page-break-inside: avoid;
        }

        .item-top {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
        }

        .name-es {
            font-weight: 600;
            font-size: 9pt;
            letter-spacing: 0.5px;
        }

        .dots {
            flex-grow: 1;
            border-bottom: 1px dotted var(--line);
            margin: 0 3mm;
            position: relative;
            top: -4px;
        }

        .price {
            font-weight: 600;
            color: var(--secondary);
            font-size: 10pt;
        }

        .name-en {
            font-size: 7.5pt;
            color: #666;
            font-style: italic;
            margin-top: 1px;
        }

        .desc-es {
            font-size: 7.5pt;
            color: #444;
            margin-top: 1.5px;
            line-height: 1.3;
        }

        .desc-en {
            font-size: 7pt;
            color: #888;
            font-style: italic;
            margin-top: 1px;
            line-height: 1.3;
        }
        
        .footer {
            margin-top: auto;
            text-align: center;
            padding-top: 5mm;
            font-size: 8pt;
            color: #a0a0a0;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .banner {
            text-align: center;
            border: 1px solid var(--secondary);
            background-color: #fbf7f0;
            color: var(--primary);
            padding: 8px 15px;
            margin: 0 auto 5mm auto;
            font-size: 8.5pt;
            font-weight: 500;
            width: 85%;
            line-height: 1.4;
            break-inside: avoid;
        }

        .banner .eng {
            font-style: italic;
            color: #666;
            display: block;
            font-size: 7.5pt;
            margin-top: 2px;
        }
    </style>
</head>
<body>
    <div class="document-wrapper">
        <div class="page-border">
            <div class="header">
                <h1>PUNTO Y COMA</h1>
                <h2 class="subtitle">Cafetería & Restaurante</h2>
            </div>
            
            <div class="banner">
                Tostadas solo en horarios de desayuno de 7:00 a.m. a 11:00 a.m.
                <span class="eng">Toasts only during breakfast hours from 7:00 a.m. to 11:00 a.m.</span>
            </div>
            <div class="banner">
                <strong>Nota:</strong> Se cobrarán todos los ingredientes extras
                <span class="eng"><strong>Note:</strong> Extra ingredients will be charged</span>
            </div>

            <div class="content">
"""

def main():
    with open("c:/Users/USUARIO/Downloads/PUNTO Y COMA/carta.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    categories = process_data(data)
    
    html = html_template
    
    for cat in categories:
        html += f'                <div class="category">\n'
        html += f'                    <div class="cat-title">{cat["categoria"]}</div>\n'
        html += f'                    <div class="cat-divider">———</div>\n'
        
        for item in cat.get("items", []):
            name_es = item.get("nombre_es", "")
            name_en = item.get("nombre_en", "")
            price = item.get("precio_eur", "")
            if isinstance(price, (int, float)):
                price = f"{price:.2f}€"
            elif price is not None:
                price = str(price) + "€"
                
            desc_es = item.get("descripcion_es", "")
            desc_en = item.get("descripcion_en", "")
            
            html += f'                    <div class="item">\n'
            html += f'                        <div class="item-top">\n'
            html += f'                            <span class="name-es">{name_es}</span>\n'
            html += f'                            <span class="dots"></span>\n'
            html += f'                            <span class="price">{price}</span>\n'
            html += f'                        </div>\n'
            if name_en:
                html += f'                        <div class="name-en">{name_en}</div>\n'
            if desc_es:
                html += f'                        <div class="desc-es">{desc_es}</div>\n'
            if desc_en:
                html += f'                        <div class="desc-en">{desc_en}</div>\n'
            html += f'                    </div>\n'
            
        html += f'                </div>\n'
        
    html += """            </div>
            <div class="footer">IVA Incluido / Taxes Included</div>
        </div>
    </div>
</body>
</html>"""

    with open("c:/Users/USUARIO/Downloads/PUNTO Y COMA/carta.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    print("¡Carta HTML generada exitosamente en carta.html!")

if __name__ == "__main__":
    main()
