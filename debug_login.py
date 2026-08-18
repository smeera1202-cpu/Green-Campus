import asyncio
from playwright.async_api import async_playwright

async def debug_login():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=edge_path, headless=True)
        page = await browser.new_page()
        await page.goto("http://localhost:5000")
        await page.wait_for_timeout(2000)

        overlay_style = await page.evaluate("() => document.getElementById('login-screen-overlay').className")
        print("Overlay ClassName:", overlay_style)
        
        user_role = await page.evaluate("() => document.getElementById('user-display-role').textContent")
        print("User Display Role:", user_role)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(debug_login())
