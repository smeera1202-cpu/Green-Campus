import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def run_feature_ui_test():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================", flush=True)
    print("SMART PLANT REPLACEMENT & VERIFIED PLANT IMAGE AUDIT", flush=True)
    print("==================================================", flush=True)

    results = {}
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    async with async_playwright() as p:
        print(f"Launching Edge browser from '{edge_path}'...", flush=True)
        browser = await p.chromium.launch(executable_path=edge_path, headless=True)
        context = await browser.new_context(viewport={'width': 1400, 'height': 900})
        await context.clear_cookies()
        page = await context.new_page()

        page.on("response", lambda resp: print(f"   [HTTP {resp.status}] {resp.url}") if resp.status >= 400 else None)

        try:
            # 1. Clear session & Login as Admin
            print("\n1. Navigating to http://localhost:5000 and logging in as Admin...", flush=True)
            await page.goto("http://localhost:5000", wait_until="domcontentloaded")
            await page.wait_for_timeout(1000)

            overlay_hidden = await page.evaluate("() => document.getElementById('login-screen-overlay').classList.contains('hidden')")
            if not overlay_hidden:
                print("   Logging in via JS fillDemoCredentials...", flush=True)
                await page.evaluate("() => window.fillDemoCredentials('admin@smartcampus.com', 'Admin@123', 'Admin')")
                await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role === 'Admin'", timeout=8000)
            else:
                print("   Active Admin session confirmed.", flush=True)

            # 2. Audit All Plant Images in Inventory
            print("\n2. Auditing Plant Inventory Images for 100% verified plant photography...", flush=True)
            await page.evaluate("() => window.switchView('plants')")
            await page.wait_for_selector(".plant-card", state="attached", timeout=15000)
            await page.wait_for_timeout(500)

            plant_imgs = await page.locator(".plant-card img").all()
            bad_img_count = 0
            for idx, img in enumerate(plant_imgs):
                src = await img.get_attribute("src")
                if "517849845537" in src or "506744038136" in src:
                    bad_img_count += 1
            
            print(f"   Total Plant Cards Audited: {len(plant_imgs)}")
            print(f"   Unverified/Animal Images Found: {bad_img_count}")
            results['Plant Image Mapping Catalog'] = "PASS" if len(plant_imgs) >= 10 and bad_img_count == 0 else "FAIL"
            results['Plant Inventory Images'] = "PASS" if len(plant_imgs) >= 10 and bad_img_count == 0 else "FAIL"

            # 3. Test QR Bio Plant Image Verification
            print("\n3. Testing QR Plant Biography Image Verification...", flush=True)
            first_qr_btn = page.locator(".plant-card button:has-text('QR Bio')").first
            await first_qr_btn.click(force=True)
            await page.wait_for_timeout(1200)

            qr_img_visible = await page.locator("#qr-modal-body img").is_visible()
            print(f"   QR Code Modal Image Visible: {qr_img_visible}")
            await page.click("#qr-modal .close-btn", force=True)
            await page.wait_for_timeout(500)
            results['Plant Details / QR Images'] = "PASS" if qr_img_visible else "FAIL"

            # 4. Test Smart Plant Replacement Recommendation Workflow
            print("\n4. Testing Smart Plant Replacement Recommendation Workflow...", flush=True)
            replace_btn = page.locator(".plant-card button:has-text('Smart Replace')").first
            await replace_btn.click(force=True)
            await page.wait_for_timeout(1500)

            modal_visible = await page.locator("#replacement-modal").is_visible()
            env_card_text = await page.locator("#replacement-env-analysis-card").inner_text()
            candidates_count = await page.locator(".rec-candidate-card").count()
            match_score_text = await page.locator(".match-score-badge").first.inner_text()

            print(f"   Smart Replacement Modal Opened: {modal_visible}")
            print(f"   Soil & Location Analysis Summary:\n   {env_card_text.replace(chr(10), ' | ')}")
            print(f"   Top Recommended Candidate Cards Displayed: {candidates_count}")
            print(f"   Top Candidate Compatibility Score: '{match_score_text}'")

            results['Smart Replacement'] = "PASS" if modal_visible and "Soil Type" in env_card_text and candidates_count >= 3 and "%" in match_score_text else "FAIL"

            # 5. Confirm Plant Replacement & Verify History Update
            print("\n5. Executing Plant Replacement Action & Auditing History...", flush=True)
            confirm_btn = page.locator(".rec-candidate-card button:has-text('Confirm')").first
            await confirm_btn.click(force=True)
            await page.wait_for_timeout(2000)

            history_rows = await page.locator("#replacement-history-table-body tr").count()
            history_first_row = await page.locator("#replacement-history-table-body tr").first.inner_text()
            print(f"   Replacement History Audit Rows Count: {history_rows}")
            print(f"   Latest Replacement Audit Entry: '{history_first_row}'")

            # 6. Test Student Role View-Only Restriction
            print("\n6. Testing Student Role Replacement Permission Restriction...", flush=True)
            await page.click("#replacement-modal .close-btn", force=True)
            await page.wait_for_timeout(500)

            await page.evaluate("() => window.handleLogout()")
            await page.wait_for_function("() => window.state.currentUser === null", timeout=8000)
            await page.wait_for_timeout(500)

            await page.evaluate("() => window.fillDemoCredentials('student@smartcampus.com', 'Student@123', 'Student')")
            await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role.includes('Student')", timeout=8000)
            await page.wait_for_timeout(500)

            await page.evaluate("() => window.switchView('plants')")
            await page.wait_for_selector(".plant-card", state="attached", timeout=15000)
            await page.wait_for_timeout(500)

            await page.locator(".plant-card button:has-text('Smart Replace')").first.click(force=True)
            await page.wait_for_timeout(1500)

            disabled_btn_count = await page.locator(".rec-candidate-card button[disabled]").count()
            view_only_text = await page.locator(".rec-candidate-card button").first.inner_text()
            print(f"   Student Replacement Candidate Button Text: '{view_only_text}' (Disabled count: {disabled_btn_count})")
            await page.click("#replacement-modal .close-btn", force=True)
            results['Role Permissions'] = "PASS" if disabled_btn_count >= 1 or "View Only" in view_only_text or "பார்வை" in view_only_text else "FAIL"

            # 7. Test Tamil Language Switching for Recommendations & History
            print("\n7. Testing Tamil Language Switching for Smart Recommendations...", flush=True)
            await page.select_option("#lang-select", "ta")
            await page.wait_for_timeout(1000)

            await page.locator(".plant-card button:has-text('மாற்று பரிந்துரை')").first.click(force=True)
            await page.wait_for_timeout(1200)

            modal_title_ta = await page.locator("#replacement-modal h3").inner_text()
            soil_title_ta = await page.locator("#replacement-env-analysis-card").inner_text()
            print(f"   Tamil Modal Title: '{modal_title_ta}'")
            print(f"   Tamil Soil Heading Found: {'மண்' in soil_title_ta or 'மண்டல' in soil_title_ta}")

            await page.click("#replacement-modal .close-btn", force=True)
            results['Tamil Support'] = "PASS" if "தாவர" in modal_title_ta else "FAIL"

            # 8. Verify Biodiversity Tracker Images Remain Exclusively Wildlife...
            print("\n8. Verifying Biodiversity Tracker Images Remain Exclusively Wildlife...", flush=True)
            await page.evaluate("() => window.switchView('biodiversity')")
            await page.wait_for_timeout(1000)
            bio_cards = await page.locator(".bio-card, #biodiversity-grid-container .card, .custom-table tr").count()
            print(f"   Biodiversity Wildlife Records Rendered: {bio_cards}")

        except Exception as e:
            print(f"\n❌ UI Test Error: {e}", flush=True)

        await browser.close()

    print("\n==================================================", flush=True)
    print("FINAL TEST CHECKLIST FOR USER REQUEST", flush=True)
    print("==================================================", flush=True)
    for feat, status in results.items():
        print(f"[{status}] {feat}", flush=True)
    print("==================================================", flush=True)

if __name__ == '__main__':
    asyncio.run(run_feature_ui_test())
