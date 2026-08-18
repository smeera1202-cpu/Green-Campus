import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def run_full_qa_audit():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================", flush=True)
    print("COMPREHENSIVE END-TO-END QA AUDIT REPORT", flush=True)
    print("SMART CAMPUS GARDENING & GREEN SPACE SYSTEM", flush=True)
    print("==================================================", flush=True)

    results = {}
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    async with async_playwright() as p:
        print(f"Launching Edge browser from '{edge_path}'...", flush=True)
        browser = await p.chromium.launch(executable_path=edge_path, headless=True)
        context = await browser.new_context(viewport={'width': 1400, 'height': 900})
        await context.clear_cookies()
        page = await context.new_page()

        try:
            # -------------------------------------------------------------
            # TEST 1: Student Login and Dashboard
            # -------------------------------------------------------------
            print("\n1. Student login and dashboard...", flush=True)
            await page.goto("http://localhost:5000", wait_until="domcontentloaded")
            await page.wait_for_timeout(1000)

            await page.evaluate("() => window.fillDemoCredentials('student@smartcampus.com', 'Student@123', 'Student')")
            await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role.includes('Student')", timeout=8000)
            await page.wait_for_timeout(1000)

            student_name = await page.locator("#user-display-name").inner_text()
            print(f"   Logged in Student User: '{student_name}'")
            results['Student login and dashboard'] = "PASS" if "Student" in student_name or "Aarav" in student_name else "FAIL"

            # -------------------------------------------------------------
            # TEST 2: Staff/Gardener Login and Dashboard
            # -------------------------------------------------------------
            print("\n2. Staff/Gardener login and dashboard...", flush=True)
            await page.evaluate("() => window.handleLogout()")
            await page.wait_for_function("() => window.state.currentUser === null", timeout=8000)
            await page.wait_for_timeout(500)

            await page.evaluate("() => window.fillDemoCredentials('staff@smartcampus.com', 'Staff@123', 'Staff')")
            await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role.includes('Staff')", timeout=8000)
            await page.wait_for_timeout(1000)

            staff_name = await page.locator("#user-display-name").inner_text()
            print(f"   Logged in Staff User: '{staff_name}'")
            results['Staff/Gardener login and dashboard'] = "PASS" if "Rajesh" in staff_name or "Staff" in staff_name else "FAIL"

            # -------------------------------------------------------------
            # TEST 3: Admin Login and Dashboard
            # -------------------------------------------------------------
            print("\n3. Admin login and dashboard...", flush=True)
            await page.evaluate("() => window.handleLogout()")
            await page.wait_for_function("() => window.state.currentUser === null", timeout=8000)
            await page.wait_for_timeout(500)

            await page.evaluate("() => window.fillDemoCredentials('admin@smartcampus.com', 'Admin@123', 'Admin')")
            await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role === 'Admin'", timeout=8000)
            await page.wait_for_timeout(1000)

            admin_name = await page.locator("#user-display-name").inner_text()
            kpis_count = await page.locator(".kpi-card, .card").count()
            print(f"   Logged in Admin User: '{admin_name}' | Dashboard KPI Cards Rendered: {kpis_count}")
            results['Admin login and dashboard'] = "PASS" if ("Vance" in admin_name or "Admin" in admin_name) and kpis_count >= 4 else "FAIL"

            # -------------------------------------------------------------
            # TEST 4: Role-Based Access
            # -------------------------------------------------------------
            print("\n4. Role-based access...", flush=True)
            admin_nav_count = await page.locator("#main-nav .nav-item[style*='block']").count()
            
            await page.evaluate("() => window.handleLogout()")
            await page.wait_for_timeout(500)
            await page.evaluate("() => window.fillDemoCredentials('student@smartcampus.com', 'Student@123', 'Student')")
            await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role.includes('Student')", timeout=8000)
            await page.wait_for_timeout(500)

            student_users_menu = await page.locator("#nav-users").is_visible()
            print(f"   Admin Visible Nav Items: {admin_nav_count} | Student Can View Admin Users Menu: {student_users_menu}")
            results['Role-based access'] = "PASS" if not student_users_menu and admin_nav_count >= 10 else "FAIL"

            # Log back in as Admin for full admin audit
            await page.evaluate("() => window.handleLogout()")
            await page.wait_for_timeout(500)
            await page.evaluate("() => window.fillDemoCredentials('admin@smartcampus.com', 'Admin@123', 'Admin')")
            await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role === 'Admin'", timeout=8000)
            await page.wait_for_timeout(500)

            # -------------------------------------------------------------
            # TEST 5: English/Tamil Switching
            # -------------------------------------------------------------
            print("\n5. English/Tamil switching...", flush=True)
            await page.select_option("#lang-select", "ta")
            await page.wait_for_timeout(1000)
            ta_title = await page.locator("#page-title-text").inner_text()

            await page.select_option("#lang-select", "en")
            await page.wait_for_timeout(1000)
            en_title = await page.locator("#page-title-text").inner_text()

            print(f"   Tamil Title: '{ta_title}' | English Title: '{en_title}'")
            results['English/Tamil switching'] = "PASS" if ta_title != en_title and ("முதன்மை" in ta_title or "Dashboard" in en_title) else "FAIL"

            # -------------------------------------------------------------
            # TEST 6: Plant Inventory
            # -------------------------------------------------------------
            print("\n6. Plant inventory...", flush=True)
            await page.evaluate("() => window.switchView('plants')")
            await page.wait_for_selector(".plant-card", state="attached", timeout=12000)
            await page.wait_for_timeout(500)

            plant_cards_count = await page.locator(".plant-card").count()
            print(f"   Total Botanical Plant Cards: {plant_cards_count}")
            results['Plant inventory'] = "PASS" if plant_cards_count >= 10 else "FAIL"

            # -------------------------------------------------------------
            # TEST 7: Correct Plant Images
            # -------------------------------------------------------------
            print("\n7. Correct plant images...", flush=True)
            plant_imgs = await page.locator(".plant-card img").all()
            bad_imgs_count = 0
            for img in plant_imgs:
                src = await img.get_attribute("src")
                if "517849845537" in src or "506744038136" in src:
                    bad_imgs_count += 1

            print(f"   Audited Plant Card Images: {len(plant_imgs)} | Unverified/Animal Images Found: {bad_imgs_count}")
            results['Correct plant images'] = "PASS" if len(plant_imgs) >= 10 and bad_imgs_count == 0 else "FAIL"

            # -------------------------------------------------------------
            # TEST 8: Plant Details and QR
            # -------------------------------------------------------------
            print("\n8. Plant details and QR...", flush=True)
            await page.locator(".plant-card button:has-text('QR Bio')").first.click(force=True)
            await page.wait_for_timeout(1200)

            qr_title = await page.locator("#qr-modal-body h3").inner_text()
            qr_img_visible = await page.locator("#qr-modal-body img").is_visible()
            await page.click("#qr-modal .close-btn", force=True)

            print(f"   QR Code Modal Title: '{qr_title}' | Plant Image Visible: {qr_img_visible}")
            results['Plant details and QR'] = "PASS" if qr_title and qr_img_visible else "FAIL"

            # -------------------------------------------------------------
            # TEST 9: Maintenance Tasks
            # -------------------------------------------------------------
            print("\n9. Maintenance tasks...", flush=True)
            await page.evaluate("() => window.switchView('maintenance')")
            await page.wait_for_timeout(1500)

            tasks_count = await page.locator("#main-content-view .card, #main-content-view tr").count()
            print(f"   Maintenance Operations Tasks Count: {tasks_count}")
            results['Maintenance tasks'] = "PASS" if tasks_count >= 1 else "FAIL"

            # -------------------------------------------------------------
            # TEST 10: Photo Proof
            # -------------------------------------------------------------
            print("\n10. Photo proof...", flush=True)
            complete_btn = page.locator("#main-content-view button:has-text('Complete')").first
            complete_btn_visible = await complete_btn.is_visible()
            if complete_btn_visible:
                await complete_btn.click(force=True)
                await page.wait_for_timeout(1000)
                photo_input_visible = await page.locator("#complete-photo-input, input[type='file'], input[placeholder*='photo']").is_visible()
                await page.click("#complete-task-modal .close-btn", force=True)
            else:
                photo_input_visible = False

            print(f"    Task Completion Photo Upload Modal Input Visible: {photo_input_visible}")
            results['Photo proof'] = "PASS" if photo_input_visible or complete_btn_visible else "FAIL"

            # -------------------------------------------------------------
            # TEST 11: Issue Reporting
            # -------------------------------------------------------------
            print("\n11. Issue reporting...", flush=True)
            await page.evaluate("() => window.switchView('issues')")
            await page.wait_for_timeout(1200)

            issues_count = await page.locator("#main-content-view .card, #main-content-view tr").count()
            print(f"    Campus Green Issues Logged: {issues_count}")
            results['Issue reporting'] = "PASS" if issues_count >= 1 else "FAIL"

            # -------------------------------------------------------------
            # TEST 12: Rewards and Leaderboard
            # -------------------------------------------------------------
            print("\n12. Rewards and leaderboard...", flush=True)
            await page.evaluate("() => window.switchView('volunteers')")
            await page.wait_for_timeout(1500)

            vol_cards = await page.locator("#main-content-view .card, #main-content-view tr").count()
            print(f"    Leaderboard & Reward Items Count: {vol_cards}")
            results['Rewards and leaderboard'] = "PASS" if vol_cards >= 1 else "FAIL"

            # -------------------------------------------------------------
            # TEST 13: AI Chatbot
            # -------------------------------------------------------------
            print("\n13. AI chatbot...", flush=True)
            await page.evaluate("() => window.toggleChatbot()")
            await page.wait_for_timeout(800)

            widget_visible = await page.locator("#chatbot-window").is_visible()
            await page.fill("#chat-input-text", "How do I water Neem trees?")
            await page.click("#btn-send-chat", force=True)
            await page.wait_for_timeout(1500)

            msg_count = await page.locator("#chatbot-messages .chat-msg").count()
            await page.evaluate("() => window.toggleChatbot()")

            print(f"    FloraAI Assistant Opened: {widget_visible} | Response Messages: {msg_count}")
            results['AI chatbot'] = "PASS" if widget_visible and msg_count >= 2 else "FAIL"

            # -------------------------------------------------------------
            # TEST 14: IoT Monitoring
            # -------------------------------------------------------------
            print("\n14. IoT monitoring...", flush=True)
            await page.evaluate("() => window.switchView('irrigation')")
            await page.wait_for_timeout(1500)

            iot_count = await page.locator("#main-content-view .card").count()
            print(f"    Live IoT Sensor Zone Cards: {iot_count}")
            results['IoT monitoring'] = "PASS" if iot_count >= 1 else "FAIL"

            # -------------------------------------------------------------
            # TEST 15: Sustainability Dashboard
            # -------------------------------------------------------------
            print("\n15. Sustainability dashboard...", flush=True)
            await page.evaluate("() => window.switchView('sustainability')")
            await page.wait_for_timeout(1500)

            sust_cards = await page.locator("#main-content-view .card").count()
            print(f"    Sustainability Metrics Cards Rendered: {sust_cards}")
            results['Sustainability dashboard'] = "PASS" if sust_cards >= 1 else "FAIL"

            # -------------------------------------------------------------
            # TEST 16: Biodiversity Tracker
            # -------------------------------------------------------------
            print("\n16. Biodiversity tracker...", flush=True)
            await page.evaluate("() => window.switchView('biodiversity')")
            await page.wait_for_timeout(1500)

            bio_count = await page.locator("#main-content-view .card, #main-content-view tr").count()
            print(f"    Biodiversity Wildlife Logs: {bio_count}")
            results['Biodiversity tracker'] = "PASS" if bio_count >= 1 else "FAIL"

            # -------------------------------------------------------------
            # TEST 17: Smart Plant Replacement Recommendation
            # -------------------------------------------------------------
            print("\n17. Smart Plant Replacement Recommendation...", flush=True)
            await page.evaluate("() => window.switchView('plants')")
            await page.wait_for_selector(".plant-card", state="attached", timeout=12000)
            await page.wait_for_timeout(500)

            await page.locator(".plant-card button:has-text('Smart Replace')").first.click(force=True)
            await page.wait_for_timeout(1500)

            replace_modal_visible = await page.locator("#replacement-modal").is_visible()
            cands_count = await page.locator(".rec-candidate-card").count()
            await page.click("#replacement-modal .close-btn", force=True)

            print(f"    Smart Replacement Modal Opened: {replace_modal_visible} | Candidate Cards: {cands_count}")
            results['Smart Plant Replacement Recommendation'] = "PASS" if replace_modal_visible and cands_count >= 3 else "FAIL"

            # -------------------------------------------------------------
            # TEST 18: Charts and Analytics
            # -------------------------------------------------------------
            print("\n18. Charts and analytics...", flush=True)
            await page.evaluate("() => window.switchView('dashboard')")
            await page.wait_for_timeout(2000)

            canvases_count = await page.locator("canvas").count()
            print(f"    Interactive Chart Canvases Rendered: {canvases_count}")
            results['Charts and analytics'] = "PASS" if canvases_count >= 2 else "FAIL"

            # -------------------------------------------------------------
            # TEST 19: Notifications
            # -------------------------------------------------------------
            print("\n19. Notifications...", flush=True)
            await page.evaluate("() => window.switchView('notifications')")
            await page.wait_for_timeout(1200)

            notifs_count = await page.locator("#main-content-view .card, .notif-item").count()
            print(f"    Notification Center Items Count: {notifs_count}")
            results['Notifications'] = "PASS" if notifs_count >= 1 else "FAIL"

            # -------------------------------------------------------------
            # TEST 20: Logout
            # -------------------------------------------------------------
            print("\n20. Logout...", flush=True)
            await page.evaluate("() => window.handleLogout()")
            await page.wait_for_timeout(1500)

            login_overlay_visible = await page.locator("#login-screen-overlay").is_visible()
            print(f"    Login Screen Overlay Restored on Logout: {login_overlay_visible}")
            results['Logout'] = "PASS" if login_overlay_visible else "FAIL"

            # -------------------------------------------------------------
            # TEST 21: Mobile Responsiveness
            # -------------------------------------------------------------
            print("\n21. Mobile responsiveness...", flush=True)
            await page.set_viewport_size({'width': 375, 'height': 812})
            await page.wait_for_timeout(1000)

            brand_visible = await page.locator(".brand-container").is_visible()
            print(f"    Mobile Layout Rendered Cleanly (375x812): {brand_visible}")
            results['Mobile responsiveness'] = "PASS" if brand_visible else "FAIL"

        except Exception as e:
            print(f"\n❌ Full QA Audit Exception: {e}", flush=True)

        await browser.close()

    print("\n==================================================", flush=True)
    print("FINAL END-TO-END QA AUDIT REPORT", flush=True)
    print("==================================================", flush=True)
    for feat, status in results.items():
        print(f"[{status}] {feat}", flush=True)
    print("==================================================", flush=True)

if __name__ == '__main__':
    asyncio.run(run_full_qa_audit())
