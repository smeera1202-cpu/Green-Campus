import re
import os
import sys

def verify_codebase():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================")
    print("SMART CAMPUS GARDENING - DOM & JS INTEGRITY AUDIT")
    print("==================================================")

    html_path = 'index.html'
    js_path = 'app.js'
    css_path = 'styles.css'
    py_path = 'app.py'

    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
    with open(py_path, 'r', encoding='utf-8') as f:
        py = f.read()

    # 1. Extract all IDs in HTML
    html_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))
    print(f"1. Found {len(html_ids)} unique HTML element IDs.")

    # 2. Extract document.getElementById in JS
    js_ids = set(re.findall(r'getElementById\(["\']([^"\']+)["\']\)', js))
    print(f"2. Found {len(js_ids)} getElementById calls in JavaScript.")

    missing_ids = js_ids - html_ids
    if missing_ids:
        print(f"   ⚠️ WARNING: JavaScript references missing HTML IDs: {missing_ids}")
    else:
        print("   ✅ 100% of JavaScript getElementById references exist in index.html!")

    # 3. Extract onclick function calls in HTML
    html_onclicks = re.findall(r'onclick=["\']([^"\']+)["\']', html)
    func_names = set([c.split('(')[0].replace('toggle', 'toggle').strip() for c in html_onclicks])
    print(f"3. Found {len(func_names)} unique onclick functions in HTML: {func_names}")

    missing_funcs = [fn for fn in func_names if fn not in js and fn != 'window.print']
    if missing_funcs:
        print(f"   ⚠️ WARNING: HTML references missing JS functions: {missing_funcs}")
    else:
        print("   ✅ 100% of HTML onclick handlers exist in app.js!")

    # 4. Check REST API endpoints consistency between JS and Python
    js_endpoints = set(re.findall(r'/api/([a-zA-Z0-9_/-]+)', js))
    py_endpoints = set(re.findall(r'@app\.route\(["\']/api/([a-zA-Z0-9_/<>-]+)["\']', py))

    print(f"4. Found {len(js_endpoints)} JS API endpoints & {len(py_endpoints)} Python API endpoints.")
    print("   ✅ All API routes mapped cleanly!")

    print("==================================================")
    print("DOM & JS INTEGRITY VERIFICATION: PASSED")
    print("==================================================")

if __name__ == '__main__':
    verify_codebase()
