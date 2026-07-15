import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add CSS
css_add = """
.admin-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.6);backdrop-filter:blur(3px);z-index:199;opacity:0;visibility:hidden;transition:var(--t)}
.admin-overlay.open{opacity:1;visibility:visible}
.sb-close-btn{display:none;position:absolute;left:15px;top:25px;font-size:18px;color:var(--text);background:var(--bg3);border:none;border-radius:8px;width:32px;height:32px;cursor:pointer}
@media(max-width:900px){
  .sidebar{position:fixed;inset:0 auto 0 auto;right:0;width:280px;z-index:200;transform:translateX(100%)}
  .sidebar.open{transform:translateX(0)}
  .sb-close-btn{display:flex;align-items:center;justify-content:center}
}
"""

# Remove old media query
content = re.sub(r'@media\(max-width:900px\)\{\s*\.sidebar\{.*?\}\s*\.sidebar\.open\{.*?\}\s*\}', css_add, content, flags=re.DOTALL)

# Add Overlay and close btn
html_add = """<!-- LAYOUT -->
<div class="admin-overlay" id="admin-overlay" onclick="toggleAdminSidebar()"></div>
<div class="admin-layout">"""

content = content.replace("<!-- LAYOUT -->\n<div class=\"admin-layout\">", html_add)

close_btn = """      <div>
        <div class="sb-logo-text">إستوردلي</div>
        <div class="sb-logo-sub">ADMIN PANEL</div>
      </div>
      <button class="sb-close-btn" onclick="toggleAdminSidebar()">✕</button>"""

content = re.sub(r'<div>\s*<div class="sb-logo-text">إستوردلي</div>\s*<div class="sb-logo-sub">ADMIN PANEL</div>\s*</div>', close_btn, content)

# update menu button onclick
content = content.replace("onclick=\"document.getElementById('sidebar').classList.toggle('open')\"", "onclick=\"toggleAdminSidebar()\"")

# add toggle script
script_add = """<script>
function toggleAdminSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
  document.getElementById('admin-overlay').classList.toggle('open');
}
"""
content = content.replace("<script>", script_add, 1)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Admin HTML updated for mobile!")
