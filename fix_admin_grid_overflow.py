import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix CSS grid/flex min-width bug
fix_css = """
/* Fix CSS grid min-width: auto bug */
.main-area, .content, .charts-row, .table-card { min-width: 0; }
"""
content = content.replace("</style>", fix_css + "\n</style>")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Grid overflow fixed")
