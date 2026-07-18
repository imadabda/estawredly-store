import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("object-fit:cover", "object-fit:contain")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Image object-fit fixed")
