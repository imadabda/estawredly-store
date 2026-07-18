import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Give stat-users an id
content = content.replace('<div class="stat-val">1,247</div>', '<div class="stat-val" id="stat-users">1,247</div>')

# Update JS in updateStats()
new_stats = """  const psEl = document.getElementById('products-subtitle');
  if(psEl) psEl.textContent = `${adminProducts.length} منتج إجمالاً، ${adminProducts.filter(p=>p.active!==false).length} منشور`;
  const usersCount = (typeof Store !== 'undefined') ? Store.getUsers().length : 0;
  const suEl = document.getElementById('stat-users');
  if(suEl) suEl.textContent = usersCount;
"""
content = re.sub(r'const psEl = document\.getElementById\(\'products-subtitle\'\);.*?if\(psEl\).*?;\n', new_stats, content, flags=re.DOTALL)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Stats hooked up")
