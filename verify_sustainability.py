import asyncio
import sys
from playwright.async_api import async_playwright

async def test_sustainability_page():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================", flush=True)
    print("VERIFYING SUSTAINABILITY PAGE LOAD & API RESPONSE", flush=True)
    print("==================================================", flush=True)

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    async with async_playwright() as p:
        print("Launching Edge browser...", flush=True)
        browser = await p.chromium.launch(executable_path=edge_path, headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto("http://localhost:5000")
            await page.wait_for_timeout(1000)

            # Switch view to sustainability
            print("Switching view to 'sustainability'...", flush=True)
            await page.evaluate("() => window.switchView('sustainability')")
            await page.wait_for_timeout(2000)

            # Check rendered content
            content_text = await page.locator("#main-content-view").inner_text()
            print("Rendered Content Summary:\n", content_text[:300])

            content_lower = content_text.lower()
            assert "sustainability" in content_lower or "சுற்றுச்சூழல்" in content_text, "Title not found"
            assert "trees" in content_lower or "மரங்கள்" in content_text, "KPI card missing"
            assert "error loading sustainability stats" not in content_lower, "Error text displayed on page!"

            canvas_count = await page.locator("#sustCarbonChart").count()
            print(f"Carbon Offset Chart canvas count: {canvas_count}")
            assert canvas_count == 1, "Chart canvas #sustCarbonChart not found"

            # Direct API test
            api_res = await page.evaluate("""async () => {
                const res = await fetch('/api/sustainability');
                return {
                    status: res.status,
                    contentType: res.headers.get('content-type'),
                    data: await res.json()
                };
            }""")
            print("\nDirect /api/sustainability API Response:", api_res)

            assert api_res['status'] == 200, "API status not 200"
            assert "application/json" in api_res['contentType'], "API Content-Type is not JSON"
            assert "history" in api_res['data'], "Missing 'history' in API data"
            assert "total_trees" in api_res['data'], "Missing 'total_trees' in API data"

            print("\n✅ SUSTAINABILITY PAGE & API VERIFICATION SUCCESSFUL!")

        except Exception as e:
            print(f"\n❌ Verification Error: {e}", flush=True)
            sys.exit(1)

        finally:
            await browser.close()

if __name__ == '__main__':
    asyncio.run(test_sustainability_page())
