import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

css_fix = """
@media(max-width:900px){
  .topbar { padding: 12px; gap: 8px; flex-wrap: wrap; }
  .topbar-search { order: 3; flex: 1 1 100%; max-width: 100%; margin-top: 5px; min-width: 0; }
  .tp-name, .topbar-divider { display: none; }
  .topbar-right { margin-right: auto; gap: 4px; }
  .stats-grid { grid-template-columns: 1fr !important; gap: 12px; }
  .content { padding: 16px; }
}
"""

# Replace the previous block I added
content = re.sub(r'@media\(max-width:900px\)\{\s*\.topbar\s*\{.*?\}\s*\}', css_fix, content, flags=re.DOTALL)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Overflow CSS fixed")
