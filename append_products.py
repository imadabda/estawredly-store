import pandas as pd
import re
import random

file = "Kleane translated AR.xlsx"
df = pd.read_excel(file, skiprows=2)

products = df.iloc[10:20]
new_items = []

for idx, row in products.iterrows():
    name = str(row.iloc[2]).strip() if not pd.isna(row.iloc[2]) else "منتج تنظيف"
    desc = str(row.iloc[3]).strip() if not pd.isna(row.iloc[3]) else "أدوات تنظيف عالية الجودة."
    code = str(row.iloc[1]).strip() if not pd.isna(row.iloc[1]) else ""
    price_rmb = row.iloc[8] if not pd.isna(row.iloc[8]) else 0
    try:
        price_ils = int(float(price_rmb) * 2)
        if price_ils < 5: price_ils = 15
    except:
        price_ils = 25
        
    old_price = int(price_ils * 1.3)
    stars = round(random.uniform(4.5, 4.9), 1)
    reviews = random.randint(50, 300)
    badge = random.choice(["", "new", "hot"])
    
    cat = "مماسح مسطحة"
    img = "prod_flat.jpg"
    
    if "refill" in name.lower() or "布" in desc:
        cat = "قطع غيار"
        if "microfiber" in name.lower() or "细纤维" in desc:
            img = "prod_micro_refill.jpg"
        else:
            img = "prod_cotton_refill.jpg"
    else:
        if "cotton" in name.lower() or "棉" in desc:
            cat = "مماسح قطنية"
            img = "prod_cotton_mop.jpg"
        elif "microfiber" in name.lower() or "细纤维" in desc:
            cat = "مماسح مايكروفايبر"
            img = "prod_micro_flat.jpg"
            
    p_id = idx + 1
    
    item_str = f'    {{"id": {p_id}, "name": "{name}", "desc": "{desc}", "cat": "{cat}", "code": "{code}", "img": "{img}", "price": {price_ils}, "oldPrice": {old_price}, "badge": "{badge}", "stars": {stars}, "reviews": {reviews}}},'
    new_items.append(item_str)

with open('main.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Find where PRODUCTS.all array ends or insert right after the last item
insert_pos = js_content.find('  ],\n  flash:')
if insert_pos != -1:
    before = js_content[:insert_pos]
    after = js_content[insert_pos:]
    new_js = before + '\n' + '\n'.join(new_items) + '\n' + after
    with open('main.js', 'w', encoding='utf-8') as f:
        f.write(new_js)
    print("Successfully appended new products to main.js")
else:
    print("Could not find the insertion point in main.js")
