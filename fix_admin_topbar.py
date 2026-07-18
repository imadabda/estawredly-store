import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

css_topbar_fix = """
@media(max-width:900px){
  .topbar { padding: 12px; gap: 8px; flex-wrap: wrap; }
  .topbar-search { order: 3; max-width: 100%; min-width: 100%; margin-top: 5px; }
  .tp-name, .topbar-divider { display: none; }
  .topbar-right { margin-right: auto; gap: 4px; }
}
"""
content = content.replace("</style>", css_topbar_fix + "\n</style>")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Topbar CSS fixed")
