import os, glob

pwa_head = """  <link rel="manifest" href="manifest.json" />
  <meta name="theme-color" content="#3b82f6" />
  <link rel="apple-touch-icon" href="logo.jpg" />"""

pwa_script = """<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('sw.js').then(reg => {
        console.log('SW registered: ', reg.scope);
      }).catch(err => {
        console.log('SW registration failed: ', err);
      });
    });
  }
</script>"""

for file in glob.glob("*.html"):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "manifest.json" not in content:
        content = content.replace("</head>", pwa_head + "\n</head>")
    if "serviceWorker" not in content:
        content = content.replace("</body>", pwa_script + "\n</body>")
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Added PWA to {file}")
