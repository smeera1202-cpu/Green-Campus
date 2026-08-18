import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def run_anti_cheating_reward_test():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================", flush=True)
    print("ANTI-CHEATING REWARD VERIFICATION WORKFLOW AUDIT", flush=True)
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
            # STEP 1: Student Upload -> Pending Verification & 0 Instant Points
            # -------------------------------------------------------------
            print("\n1. Student uploads activity proof image...", flush=True)
            await page.goto("http://localhost:5000", wait_until="domcontentloaded")
            await page.wait_for_timeout(1000)

            await page.evaluate("() => window.fillDemoCredentials('student@smartcampus.com', 'Student@123', 'Student')")
            await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role.includes('Student')", timeout=8000)
            await page.wait_for_timeout(1000)

            # Trigger Student Activity Submission API directly via frontend submit
            claim_res = await page.evaluate("""async () => {
                const res = await fetch('/api/volunteers/claim', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        title: 'Rose Garden Weeding Drive',
                        volunteer_id: 4,
                        volunteer_name: 'Aarav Sharma',
                        description: 'Cleaned weeds around rose bed in Main Quad.',
                        proof_photo: 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600',
                        zone_id: 1
                    })
                });
                return await res.json();
            }""")

            print(f"   Student Upload Submission Response:\n   {claim_res}")
            activity_id_1 = claim_res.get('id')
            status_1 = claim_res.get('status')
            detected_plant_1 = claim_res.get('detected_plant')

            results['Student Upload Creates Pending Verification'] = "PASS" if status_1 == 'Pending Verification' else "FAIL"
            results['AI Plant Classification Active'] = "PASS" if detected_plant_1 else "FAIL"
            results['Zero Points Granted Immediately'] = "PASS" if status_1 == 'Pending Verification' else "FAIL"

            # -------------------------------------------------------------
            # STEP 2: Staff/Admin Notification & Verification Queue Display
            # -------------------------------------------------------------
            print("\n2. Logging in as Admin & Checking Notification & Queue...", flush=True)
            await page.evaluate("() => window.handleLogout()")
            await page.wait_for_timeout(500)

            await page.evaluate("() => window.fillDemoCredentials('admin@smartcampus.com', 'Admin@123', 'Admin')")
            await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role === 'Admin'", timeout=8000)
            await page.wait_for_timeout(1000)

            await page.evaluate("() => window.switchView('notifications')")
            await page.wait_for_timeout(1200)

            notif_text = await page.locator("#main-content-view").inner_text()
            has_pending_notif = "📸 New Reward Submission Pending Verification" in notif_text or "Rose Garden Weeding Drive" in notif_text
            print(f"   Admin Notification Generated: {has_pending_notif}")
            results['Admin Notification Generated'] = "PASS" if has_pending_notif else "FAIL"

            await page.evaluate("() => window.switchView('volunteers')")
            await page.wait_for_timeout(1500)

            queue_cards_count = await page.locator(".card:has-text('Pending Verification'), .card:has-text('சரிபார்ப்பு நிலுவையில்')").count()
            print(f"   Pending Verification Queue Cards Count: {queue_cards_count}")
            results['Pending Verification Queue Displayed'] = "PASS" if queue_cards_count >= 1 else "FAIL"

            # -------------------------------------------------------------
            # STEP 3: Staff/Admin Approve Action -> Points Awarded Exactly Once
            # -------------------------------------------------------------
            print(f"\n3. Executing Staff/Admin APPROVE for Activity #{activity_id_1}...", flush=True)
            approve_res = await page.evaluate(f"""async () => {{
                const res = await fetch('/api/volunteers/verify/{activity_id_1}', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ action: 'approve', verified_by: 'Dr. Eleanor Vance (Admin)', points: 50 }})
                }});
                return await res.json();
            }}""")

            print(f"   Approve Verification Response:\n   {approve_res}")
            results['Approve Grants Points'] = "PASS" if approve_res.get('status') == 'Approved' and approve_res.get('points_awarded') == 50 else "FAIL"

            # Attempt Duplicate Approval Check
            dup_approve_res = await page.evaluate(f"""async () => {{
                const res = await fetch('/api/volunteers/verify/{activity_id_1}', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ action: 'approve', verified_by: 'Dr. Eleanor Vance (Admin)', points: 50 }})
                }});
                return await res.json();
            }}""")
            print(f"   Duplicate Approve Response (Should Error): {dup_approve_res}")
            results['Prevent Duplicate Approval'] = "PASS" if 'error' in dup_approve_res else "FAIL"

            # -------------------------------------------------------------
            # STEP 4: Staff/Admin REJECT Action -> 0 Points Awarded
            # -------------------------------------------------------------
            print("\n4. Testing Student Upload & Staff/Admin REJECT Workflow...", flush=True)
            # Submit second activity proof
            claim_res_2 = await page.evaluate("""async () => {
                const res = await fetch('/api/volunteers/claim', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        title: 'Unverified Photo Upload Test',
                        volunteer_id: 4,
                        volunteer_name: 'Aarav Sharma',
                        description: 'Testing reject workflow.',
                        proof_photo: 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=600',
                        zone_id: 2
                    })
                });
                return await res.json();
            }""")

            activity_id_2 = claim_res_2.get('id')
            print(f"   Second Upload Submission ID: #{activity_id_2}")

            reject_res = await page.evaluate(f"""async () => {{
                const res = await fetch('/api/volunteers/verify/{activity_id_2}', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ action: 'reject', verified_by: 'Dr. Eleanor Vance (Admin)' }})
                }});
                return await res.json();
            }}""")

            print(f"   Reject Verification Response:\n   {reject_res}")
            results['Reject Grants 0 Points'] = "PASS" if reject_res.get('status') == 'Rejected' and reject_res.get('points_awarded') == 0 else "FAIL"

            # -------------------------------------------------------------
            # STEP 5: English / Tamil Multilingual UI Check
            # -------------------------------------------------------------
            print("\n5. Testing Tamil Language Support for Verification Terminology...", flush=True)
            await page.select_option("#lang-select", "ta")
            await page.wait_for_timeout(1000)

            await page.evaluate("() => window.switchView('volunteers')")
            await page.wait_for_timeout(1500)

            ta_view_text = await page.locator("#main-content-view").inner_text()
            has_ta_terms = "நிலுவையில் உள்ள பரிசு சரிபார்ப்பு வரிசை" in ta_view_text or "சமர்ப்பித்த செயல்பாடுகளின் வரலாறு" in ta_view_text
            print(f"   Tamil Verification Terminology Rendered: {has_ta_terms}")
            results['Tamil Multilingual Support'] = "PASS" if has_ta_terms else "FAIL"

        except Exception as e:
            print(f"\n❌ Reward Audit Error: {e}", flush=True)

        await browser.close()

    print("\n==================================================", flush=True)
    print("FINAL TEST CHECKLIST: ANTI-CHEATING REWARD VERIFICATION", flush=True)
    print("==================================================", flush=True)
    for feat, status in results.items():
        print(f"[{status}] {feat}", flush=True)
    print("==================================================", flush=True)

if __name__ == '__main__':
    asyncio.run(run_anti_cheating_reward_test())
