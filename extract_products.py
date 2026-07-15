#!/usr/bin/env python3
"""
استخراج صور المنتجات وبياناتها من ملف Excel الخاص بـ Kleane
"""
import openpyxl
import os
import json
import zipfile
import re

EXCEL_FILE = "Kleane translated AR.xlsx"
OUTPUT_IMG_DIR = "product_images"
OUTPUT_JSON = "products_data.json"

def detect_category(code, name_ar, desc_ar):
    name = (name_ar or "").lower()
    desc = (desc_ar or "").lower()
    if any(x in name for x in ["قطني", "قطنية", "قطن"]):
        return "مماسح قطنية"
    if any(x in name for x in ["مايكروفايبر", "ألياف دقيقة"]):
        return "مماسح مايكروفايبر"
    if any(x in name for x in ["غيار", "بديل"]):
        return "قطع غيار"
    if any(x in desc for x in ["قطني", "قطنية"]):
        return "مماسح قطنية"
    if "بديل" in desc or "غيار" in desc:
        return "قطع غيار"
    return "مماسح مسطحة"

def get_price_ils(price_rmb):
    try:
        price = float(price_rmb) * 5.5
        return round(price), round(price * 1.35)
    except:
        return 20, 27

def extract_images(xlsx_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    image_map = {}
    with zipfile.ZipFile(xlsx_path, 'r') as z:
        img_files = [f for f in z.namelist() if f.startswith('xl/media/')]
        print(f"Found {len(img_files)} media files")
        for img_file in img_files:
            filename = os.path.basename(img_file)
            out_path = os.path.join(output_dir, filename)
            with z.open(img_file) as src, open(out_path, 'wb') as dst:
                dst.write(src.read())
        
        drawing_files = [f for f in z.namelist() if 'drawing' in f.lower() and f.endswith('.xml')]
        rels_files   = [f for f in z.namelist() if 'drawing' in f.lower() and f.endswith('.rels')]
        print(f"Drawing files: {drawing_files}")
        
        for df in drawing_files:
            content = z.read(df).decode('utf-8', errors='ignore')
            rows = re.findall(r'<xdr:from>.*?<xdr:row>(\d+)</xdr:row>.*?</xdr:from>', content, re.DOTALL)
            rids = re.findall(r'r:embed="(rId\d+)"', content)
            for rf in rels_files:
                rels = z.read(rf).decode('utf-8', errors='ignore')
                rid_map = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
                for row, rid in zip(rows, rids):
                    if rid in rid_map:
                        img_filename = os.path.basename(rid_map[rid])
                        image_map[int(row)] = img_filename
    print(f"Mapped {len(image_map)} images to rows")
    return image_map

def main():
    print("استخراج الصور...")
    image_map = extract_images(EXCEL_FILE, OUTPUT_IMG_DIR)
    
    print("قراءة بيانات المنتجات...")
    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb.active
    
    products = []
    pid = 1
    for row_idx, row in enumerate(ws.iter_rows(min_row=4, values_only=True), start=4):
        code = row[1]
        if not code:
            continue
        name_en  = str(row[2] or "").strip()
        price_rmb= row[8]
        color    = str(row[15] or "").strip()
        desc_ar  = str(row[19] or "").strip()
        name_ar  = str(row[20] or "").strip()
        if not name_ar and not name_en:
            continue
        
        final_name = name_ar if name_ar else name_en
        final_desc = desc_ar if desc_ar else str(row[4] or "").strip()
        price, old_price = get_price_ils(price_rmb)
        category = detect_category(code, name_ar, desc_ar)
        
        # Try multiple row offsets for image mapping
        img_file = None
        for offset in [row_idx-1, row_idx, row_idx-2, row_idx-3]:
            if offset in image_map:
                img_file = image_map[offset]
                break
        
        if img_file:
            img_path = f"product_images/{img_file}"
        else:
            fallback = {"مماسح مسطحة":"prod_flat.jpg","مماسح قطنية":"prod_cotton.jpg","قطع غيار":"prod_micro_refill.jpg","مماسح مايكروفايبر":"prod_spin.jpg"}
            img_path = fallback.get(category, "prod_flat.jpg")
        
        products.append({
            "id": pid,
            "code": str(code).strip(),
            "name": final_name,
            "name_en": name_en,
            "desc": final_desc,
            "cat": category,
            "img": img_path,
            "price": price,
            "oldPrice": old_price,
            "badge": "",
            "stars": round(4.5 + (pid % 5) * 0.1, 1),
            "reviews": 50 + (pid * 13 % 250),
            "color": color,
            "inStock": True,
        })
        pid += 1
    
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    
    print(f"\nتم استخراج {len(products)} منتج → {OUTPUT_JSON}")
    with_img = sum(1 for p in products if "product_images" in p["img"])
    print(f"صور مستخرجة: {with_img} | احتياطية: {len(products)-with_img}")
    cats = {}
    for p in products:
        cats[p["cat"]] = cats.get(p["cat"], 0) + 1
    print("الفئات:", cats)

if __name__ == "__main__":
    main()
