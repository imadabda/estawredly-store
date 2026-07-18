import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix html, body
content = re.sub(r'html\{.*?\}', "html{font-size:15px;scroll-behavior:smooth;overflow-x:hidden;width:100%;max-width:100vw}", content)
content = re.sub(r'body\{.*?\}', "body{font-family:'Tajawal',sans-serif;direction:rtl;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden;width:100%;max-width:100vw;margin:0;padding:0}", content)

# Fix sidebar CSS for mobile
new_sidebar_mobile = """@media(max-width:900px){
  .sidebar{position:fixed;inset:0 auto 0 auto;right:-280px;width:280px;z-index:200;transition:right .3s ease;transform:none}
  .sidebar.open{right:0;transform:none}
  .sb-close-btn{display:flex;align-items:center;justify-content:center}
}"""
content = re.sub(r'@media\(max-width:900px\)\{\s*\.sidebar\{position:fixed;.*?\}\s*\.sidebar\.open\{.*?\}\s*\.sb-close-btn\{.*?\}\s*\}', new_sidebar_mobile, content, flags=re.DOTALL)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Zoom and overflow fixed")
