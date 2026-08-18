import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def run_interactive_verification_audit():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================", flush=True)
    print("INTERACTIVE STAFF/ADMIN VERIFICATION WORKFLOW AUDIT", flush=True)
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
            # STEP 1: Student Login -> Upload Activity Proof -> Pending (0 pts)
            # -------------------------------------------------------------
            print("\n1. Logging in as Student & Uploading Activity Proof...", flush=True)
            await page.goto("http://localhost:5000")
            await page.wait_for_timeout(1500)

            await page.evaluate("() => window.fillDemoCredentials('student@smartcampus.com', 'Student@123', 'Student')")
            await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role.includes('Student')", timeout=8000)
            await page.wait_for_timeout(1000)

            await page.evaluate("() => window.switchView('volunteers')")
            await page.wait_for_timeout(1500)

            # Submit Activity Proof using Student's actual session credentials
            claim_res_1 = await page.evaluate("""async () => {
                const u = window.state.currentUser || {};
                const res = await fetch('/api/volunteers/claim', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        title: 'Main Quad Eco Weeding Drive',
                        volunteer_id: u.id || 3,
                        volunteer_name: u.name || 'Student Volunteer Demo',
                        description: 'Cleaned weeds and applied organic mulch around rose bed.',
                        proof_photo: 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600',
                        zone_id: 1,
                        role: 'Student Volunteer'
                    })
                });
                return await res.json();
            }""")

            print(f"   Student Upload Response: {claim_res_1}")
            activity_id_1 = claim_res_1.get('id')
            status_1 = claim_res_1.get('status')

            # Verify Student UI layout: Approve/Reject controls MUST NOT exist
            approve_btn_student_count = await page.locator("button:has-text('Approve & Award Points')").count()
            queue_card_student = await page.locator(".card:has-text('Pending Reward Verification Queue')").count()

            print(f"   Student UI - Approve Buttons Count: {approve_btn_student_count}")
            print(f"   Student UI - Queue Card Count: {queue_card_student}")

            results['Student Upload Returns Pending Verification'] = "PASS" if status_1 == 'Pending Verification' else "FAIL"
            results['Student UI Hides Approve Buttons'] = "PASS" if approve_btn_student_count == 0 else "FAIL"
            results['Student UI Hides Queue Card'] = "PASS" if queue_card_student == 0 else "FAIL"

            await page.evaluate("() => window.handleLogout()")
            await page.wait_for_timeout(1000)

            # -------------------------------------------------------------
            # STEP 2: Staff Login -> Open Queue -> Click APPROVE
            # -------------------------------------------------------------
            print(f"\n2. Logging in as Staff/Gardener & Approving Activity #{activity_id_1}...", flush=True)
            await page.evaluate("() => window.fillDemoCredentials('staff@smartcampus.com', 'Staff@123', 'Staff')")
            await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role.includes('Staff')", timeout=8000)
            await page.wait_for_timeout(1000)

            await page.evaluate("() => window.switchView('volunteers')")
            await page.wait_for_timeout(1500)

            staff_queue_card = await page.locator(".card:has-text('Pending Reward Verification Queue')").count()
            approve_btn_staff = page.locator(f"button[onclick*='verifyStudentSubmission({activity_id_1}, \\'approve\\')']")
            approve_btn_count = await approve_btn_staff.count()

            print(f"   Staff UI - Verification Queue Visible: {staff_queue_card > 0}")
            print(f"   Staff UI - Approve Button Clickable for #{activity_id_1}: {approve_btn_count > 0}")

            results['Staff Queue Card Visible'] = "PASS" if staff_queue_card > 0 else "FAIL"
            results['Staff Approve Button Rendered'] = "PASS" if approve_btn_count > 0 else "FAIL"

            # Execute Click on Approve Button in DOM
            print(f"   Clicking 'Approve & Award Points' button for Activity #{activity_id_1} in browser...", flush=True)
            await approve_btn_staff.click()
            await page.wait_for_timeout(2000)

            # Verify DB record updated status = 'Approved' and points = 50
            updated_act_1 = await page.evaluate(f"""async () => {{
                const res = await fetch('/api/volunteers/activities?role=Staff');
                const list = await res.json();
                return list.find(a => a.id === {activity_id_1});
            }}""")

            print(f"   Updated Activity Record after Staff Approval: {updated_act_1}")
            results['Staff Approve Action Updates DB Status'] = "PASS" if updated_act_1 and updated_act_1.get('status') == 'Approved' and updated_act_1.get('points') == 50 else "FAIL"

            await page.evaluate("() => window.handleLogout()")
            await page.wait_for_timeout(1000)

            # -------------------------------------------------------------
            # STEP 3: Student Re-Login -> Verify Points & Approved Status
            # -------------------------------------------------------------
            print("\n3. Re-logging in as Student & Verifying Points Credited...", flush=True)
            await page.evaluate("() => window.fillDemoCredentials('student@smartcampus.com', 'Student@123', 'Student')")
            await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role.includes('Student')", timeout=8000)
            await page.wait_for_timeout(1500)

            await page.evaluate("() => window.switchView('volunteers')")
            await page.wait_for_timeout(2000)

            my_act_1 = await page.evaluate(f"""async () => {{
                const res = await fetch('/api/volunteers/activities?role=Student%20Volunteer');
                const list = await res.json();
                return list.find(a => a.id === {activity_id_1});
            }}""")
            
            print(f"   Student View Activity Record: {my_act_1}")

            has_approved_status = my_act_1 and my_act_1.get('status') == 'Approved'
            has_credited_pts = my_act_1 and my_act_1.get('points') == 50

            print(f"   Student UI - Approved Status Verified: {has_approved_status}")
            print(f"   Student UI - Credited +50 pts Verified: {has_credited_pts}")

            results['Student Sees Approved Status & +50 Points'] = "PASS" if has_approved_status and has_credited_pts else "FAIL"

            await page.evaluate("() => window.handleLogout()")
            await page.wait_for_timeout(1000)

            # -------------------------------------------------------------
            # STEP 4: Student Upload 2nd Submission -> Staff Click REJECT
            # -------------------------------------------------------------
            print("\n4. Testing Second Submission & Staff REJECT Workflow...", flush=True)
            await page.evaluate("() => window.fillDemoCredentials('student@smartcampus.com', 'Student@123', 'Student')")
            await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role.includes('Student')", timeout=8000)
            await page.wait_for_timeout(1000)

            claim_res_2 = await page.evaluate("""async () => {
                const u = window.state.currentUser || {};
                const res = await fetch('/api/volunteers/claim', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        title: 'Duplicate Photo Upload Test',
                        volunteer_id: u.id || 3,
                        volunteer_name: u.name || 'Student Volunteer Demo',
                        description: 'Unverified photo test for rejection.',
                        proof_photo: 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=600',
                        zone_id: 2,
                        role: 'Student Volunteer'
                    })
                });
                return await res.json();
            }""")

            activity_id_2 = claim_res_2.get('id')
            print(f"   Second Upload Submission ID: #{activity_id_2}")

            await page.evaluate("() => window.handleLogout()")
            await page.wait_for_timeout(1000)

            # Staff Login & Click Reject Button
            await page.evaluate("() => window.fillDemoCredentials('staff@smartcampus.com', 'Staff@123', 'Staff')")
            await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role.includes('Staff')", timeout=8000)
            await page.wait_for_timeout(1000)

            await page.evaluate("() => window.switchView('volunteers')")
            await page.wait_for_timeout(1500)

            reject_btn_staff = page.locator(f"button[onclick*='verifyStudentSubmission({activity_id_2}, \\'reject\\')']")
            reject_btn_count = await reject_btn_staff.count()
            print(f"   Staff UI - Reject Button Clickable for #{activity_id_2}: {reject_btn_count > 0}")

            if reject_btn_count > 0:
                print(f"   Clicking 'Reject (0 Points)' button for Activity #{activity_id_2} in browser...", flush=True)
                await reject_btn_staff.click()
                await page.wait_for_timeout(2000)

            updated_act_2 = await page.evaluate(f"""async () => {{
                const res = await fetch('/api/volunteers/activities?role=Staff');
                const list = await res.json();
                return list.find(a => a.id === {activity_id_2});
            }}""")

            print(f"   Updated Activity Record after Staff Rejection: {updated_act_2}")
            results['Staff Reject Action Updates DB Status & 0 Points'] = "PASS" if updated_act_2 and updated_act_2.get('status') == 'Rejected' and updated_act_2.get('points') == 0 else "FAIL"

            await page.evaluate("() => window.handleLogout()")
            await page.wait_for_timeout(1000)

            # -------------------------------------------------------------
            # STEP 5: Admin Role Test Separately
            # -------------------------------------------------------------
            print("\n5. Testing Admin Role Verification & Forbidden Self-Submission...", flush=True)
            await page.evaluate("() => window.fillDemoCredentials('admin@smartcampus.com', 'Admin@123', 'Admin')")
            await page.wait_for_function("() => window.state.currentUser && window.state.currentUser.role === 'Admin'", timeout=8000)
            await page.wait_for_timeout(1000)

            admin_claim_forbidden = await page.evaluate("""async () => {
                const res = await fetch('/api/volunteers/claim', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title: 'Admin Self Claim Test', role: 'Admin' })
                });
                return res.status;
            }""")

            print(f"   Admin calling POST /api/volunteers/claim HTTP Status: {admin_claim_forbidden}")
            results['Admin Blocked from Submitting Activity Proof'] = "PASS" if admin_claim_forbidden == 403 else "FAIL"

        except Exception as e:
            print(f"\n❌ Verification Workflow Audit Error: {e}", flush=True)

        await browser.close()

    print("\n==================================================", flush=True)
    print("FINAL TEST CHECKLIST: STAFF/ADMIN VERIFICATION WORKFLOW", flush=True)
    print("==================================================", flush=True)
    for feat, status in results.items():
        print(f"[{status}] {feat}", flush=True)
    print("==================================================", flush=True)

if __name__ == '__main__':
    asyncio.run(run_interactive_verification_audit())
