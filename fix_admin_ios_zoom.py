import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

ios_fix = """
@media(max-width:900px){
  input, select, textarea { font-size: 16px !important; }
}
"""
content = content.replace("</style>", ios_fix + "\n</style>")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("iOS input zoom fix applied")
