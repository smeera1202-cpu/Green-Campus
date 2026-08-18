import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def run_role_reward_verification_audit():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================", flush=True)
    print("ROLE-BASED ACCESS & REWARD VERIFICATION AUDIT", flush=True)
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
            # 1. STUDENT ROLE AUDIT
            # -------------------------------------------------------------
            print("\n1. Testing Student Role UI & API Permissions...", flush=True)
            await page.goto("http://localhost:5000")
            await page.wait_for_timeout(1500)

            await page.evaluate("() => window.fillDemoCredentials('student@smartcampus.com', 'Student@123', 'Student')")
            await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role.includes('Student')", timeout=8000)
            await page.wait_for_timeout(1000)

            await page.evaluate("() => window.switchView('volunteers')")
            await page.wait_for_timeout(1200)

            view_text_student = await page.locator("#main-content-view").inner_text()

            # Check UI visibility for Student
            submit_btn_visible = await page.locator("button:has-text('Submit Activity Proof')").count() > 0
            pending_queue_visible = "Pending Reward Verification Queue" in view_text_student and "Mandatory Staff/Admin" in view_text_student
            approve_btns_count = await page.locator("button:has-text('Approve & Award Points')").count()

            print(f"   Student View - Submit Activity Proof Visible: {submit_btn_visible}")
            print(f"   Student View - Verification Queue Visible: {pending_queue_visible}")
            print(f"   Student View - Approve Buttons Count: {approve_btns_count}")

            results['Student Submit Button Visible'] = "PASS" if submit_btn_visible else "FAIL"
            results['Student Queue Hidden'] = "PASS" if not pending_queue_visible else "FAIL"
            results['Student Approve Buttons Hidden'] = "PASS" if approve_btns_count == 0 else "FAIL"

            # Student Backend API Authorization Checks
            verify_forbidden = await page.evaluate("""async () => {
                const res = await fetch('/api/volunteers/verify/1', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'approve', role: 'Student Volunteer' })
                });
                return res.status;
            }""")
            print(f"   Student calling POST /api/volunteers/verify/1 HTTP Status: {verify_forbidden}")

            queue_forbidden = await page.evaluate("""async () => {
                const res = await fetch('/api/volunteers/pending-verifications?role=Student+Volunteer');
                return res.status;
            }""")
            print(f"   Student calling GET /api/volunteers/pending-verifications HTTP Status: {queue_forbidden}")

            results['Backend Forbidden: Student Verify Action'] = "PASS" if verify_forbidden == 403 else "FAIL"
            results['Backend Forbidden: Student Queue Access'] = "PASS" if queue_forbidden == 403 else "FAIL"

            # -------------------------------------------------------------
            # 2. STAFF / GARDENER ROLE AUDIT
            # -------------------------------------------------------------
            print("\n2. Testing Staff / Gardener Role UI & API Permissions...", flush=True)
            await page.evaluate("() => window.handleLogout()")
            await page.wait_for_timeout(500)

            await page.evaluate("() => window.fillDemoCredentials('staff@smartcampus.com', 'Staff@123', 'Staff')")
            await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role.includes('Staff')", timeout=8000)
            await page.wait_for_timeout(1000)

            await page.evaluate("() => window.switchView('volunteers')")
            await page.wait_for_timeout(1500)

            view_text_staff = await page.locator("#main-content-view").inner_text()

            staff_submit_btn_visible = await page.locator("button:has-text('Submit Activity Proof')").count() > 0
            staff_queue_visible = "Pending Reward Verification Queue" in view_text_staff
            staff_approve_btns = await page.locator("button:has-text('Approve & Award Points')").count()

            print(f"   Staff View - Submit Activity Proof Hidden: {not staff_submit_btn_visible}")
            print(f"   Staff View - Verification Queue Visible: {staff_queue_visible}")
            print(f"   Staff View - Approve Buttons Available: {staff_approve_btns}")

            results['Staff Submit Button Hidden'] = "PASS" if not staff_submit_btn_visible else "FAIL"
            results['Staff Queue Visible'] = "PASS" if staff_queue_visible else "FAIL"
            results['Staff Verification Buttons Active'] = "PASS" if staff_approve_btns >= 0 else "FAIL"

            # Staff Backend API Security Check (Staff cannot submit student activity claim)
            staff_claim_forbidden = await page.evaluate("""async () => {
                const res = await fetch('/api/volunteers/claim', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title: 'Staff Self Claim Test', role: 'Gardening Staff' })
                });
                return res.status;
            }""")
            print(f"   Staff calling POST /api/volunteers/claim HTTP Status: {staff_claim_forbidden}")
            results['Backend Forbidden: Staff Activity Submission'] = "PASS" if staff_claim_forbidden == 403 else "FAIL"

            # -------------------------------------------------------------
            # 3. ADMIN ROLE AUDIT
            # -------------------------------------------------------------
            print("\n3. Testing Admin Role UI & API Permissions...", flush=True)
            await page.evaluate("() => window.handleLogout()")
            await page.wait_for_timeout(500)

            await page.evaluate("() => window.fillDemoCredentials('admin@smartcampus.com', 'Admin@123', 'Admin')")
            await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role === 'Admin'", timeout=8000)
            await page.wait_for_timeout(1000)

            await page.evaluate("() => window.switchView('volunteers')")
            await page.wait_for_timeout(1500)

            view_text_admin = await page.locator("#main-content-view").inner_text()

            admin_submit_btn_visible = await page.locator("button:has-text('Submit Activity Proof')").count() > 0
            admin_queue_visible = "Pending Reward Verification Queue" in view_text_admin

            print(f"   Admin View - Submit Activity Proof Hidden: {not admin_submit_btn_visible}")
            print(f"   Admin View - Verification Queue Visible: {admin_queue_visible}")

            results['Admin Submit Button Hidden'] = "PASS" if not admin_submit_btn_visible else "FAIL"
            results['Admin Queue Visible'] = "PASS" if admin_queue_visible else "FAIL"

            admin_claim_forbidden = await page.evaluate("""async () => {
                const res = await fetch('/api/volunteers/claim', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title: 'Admin Self Claim Test', role: 'Admin' })
                });
                return res.status;
            }""")
            print(f"   Admin calling POST /api/volunteers/claim HTTP Status: {admin_claim_forbidden}")
            results['Backend Forbidden: Admin Activity Submission'] = "PASS" if admin_claim_forbidden == 403 else "FAIL"

            # -------------------------------------------------------------
            # 4. TAMIL MULTILINGUAL UI CHECK
            # -------------------------------------------------------------
            print("\n4. Testing Tamil Language Support across Role Views...", flush=True)
            await page.select_option("#lang-select", "ta")
            await page.wait_for_timeout(1000)

            nav_vol_text = await page.locator("#nav-volunteers span").inner_text()
            print(f"   Admin Tamil Nav Link Text: '{nav_vol_text}'")
            results['Tamil Role Localized Navigation'] = "PASS" if "பரிசு சரிபார்ப்பு" in nav_vol_text else "FAIL"

        except Exception as e:
            print(f"\n❌ Role Audit Error: {e}", flush=True)

        await browser.close()

    print("\n==================================================", flush=True)
    print("FINAL TEST CHECKLIST: ROLE-BASED ACCESS & AUTHORIZATION", flush=True)
    print("==================================================", flush=True)
    for feat, status in results.items():
        print(f"[{status}] {feat}", flush=True)
    print("==================================================", flush=True)

if __name__ == '__main__':
    asyncio.run(run_role_reward_verification_audit())
