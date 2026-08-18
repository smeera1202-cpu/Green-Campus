import asyncio
from playwright.async_api import async_playwright

async def debug_console():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=edge_path, headless=True)
        page = await browser.new_page()

        page.on("console", lambda msg: print(f"CONSOLE [{msg.type}]: {msg.text}"))
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))

        await page.goto("http://localhost:5000")
        await page.wait_for_timeout(3000)

        window_keys = await page.evaluate("() => Object.keys(window).filter(k => k.startsWith('open') || k.startsWith('switch') || k.startsWith('render'))")
        print("Exported Window Functions:", window_keys)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(debug_console())
