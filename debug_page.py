import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def debug_page_errors():
    sys.stdout.reconfigure(encoding='utf-8')
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=edge_path, headless=True)
        page = await browser.new_page()

        page.on("request", lambda req: print(f"[REQ] {req.method} {req.url}"))
        page.on("response", lambda res: print(f"[RES {res.status}] {res.url} ({res.headers.get('content-type', '')})"))
        page.on("pageerror", lambda err: print(f"[PAGE EXCEPTION] {err}"))

        print("Navigating to http://localhost:5000...")
        await page.goto("http://localhost:5000", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(debug_page_errors())
