from flask import Flask, jsonify, request, send_from_directory, session
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import sqlite3
import random
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_db, init_db
from scheduler import start_background_scheduler, run_scheduler_cycle

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = 'smart-campus-gardening-secret-key-2026'
CORS(app, supports_credentials=True)

# Ensure DB exists
init_db(force_reseed=False)

# Start background scheduler safely (skip if on Vercel / serverless environment)
try:
    if not os.environ.get('VERCEL'):
        start_background_scheduler(interval_seconds=25)
except Exception as e:
    print("Scheduler warning:", e)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# ==========================================
# 1. AUTHENTICATION & USER MANAGEMENT API
# ==========================================

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    requested_role = data.get('role') or ''

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required.'}), 400

    conn = get_db()
    cursor = conn.cursor()
    user = cursor.execute("SELECT id, name, email, password, role FROM users WHERE LOWER(email) = ?", (email,)).fetchone()
    conn.close()

    if not user:
        return jsonify({'success': False, 'message': 'Invalid email or password.'}), 401

    user_dict = dict(user)
    stored_pw = user_dict['password']

    # Verify password (hashed or fallback plaintext for legacy)
    is_valid = False
    if stored_pw.startswith('pbkdf2:') or stored_pw.startswith('scrypt:') or stored_pw.startswith('sha256:'):
        is_valid = check_password_hash(stored_pw, password)
    else:
        is_valid = (stored_pw == password)

    if not is_valid:
        return jsonify({'success': False, 'message': 'Invalid email or password.'}), 401

    # Optional role check normalization (Staff <-> Gardening Staff, Student <-> Student Volunteer)
    actual_role = user_dict['role']
    if requested_role:
        norm_req = requested_role.lower()
        norm_act = actual_role.lower()
        if 'student' in norm_req and 'student' not in norm_act:
            return jsonify({'success': False, 'message': f"Account is not authorized for {requested_role} role."}), 403
        if ('staff' in norm_req or 'gardener' in norm_req) and ('staff' not in norm_act and 'gardener' not in norm_act):
            return jsonify({'success': False, 'message': f"Account is not authorized for {requested_role} role."}), 403
        if 'admin' in norm_req and 'admin' not in norm_act:
            return jsonify({'success': False, 'message': f"Account is not authorized for {requested_role} role."}), 403

    # Set Flask session
    session['user_id'] = user_dict['id']
    session['name'] = user_dict['name']
    session['email'] = user_dict['email']
    session['role'] = user_dict['role']

    # Clean user dict for response (exclude password)
    del user_dict['password']

    return jsonify({
        'success': True,
        'message': 'Login successful!',
        'user': user_dict,
        'token': f"token-{user_dict['id']}-{int(datetime.now().timestamp())}"
    })

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully.'})

@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    if 'user_id' in session:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': session['user_id'],
                'name': session['name'],
                'email': session['email'],
                'role': session['role']
            }
        })
    return jsonify({'authenticated': False})

@app.route('/api/admin/users', methods=['GET', 'POST'])
def handle_admin_users():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.json or {}
        name = data.get('name')
        email = (data.get('email') or '').strip().lower()
        password = data.get('password')
        role = data.get('role', 'Student Volunteer')

        if not name or not email or not password:
            conn.close()
            return jsonify({'success': False, 'message': 'Name, email and password are required.'}), 400

        try:
            hashed = generate_password_hash(password)
            cursor.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                           (name, email, hashed, role))
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return jsonify({'success': True, 'message': f'User {name} created successfully!', 'id': new_id})
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'success': False, 'message': 'User with this email already exists.'}), 400

    users = cursor.execute("SELECT id, name, email, role FROM users ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])

@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
def delete_admin_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'User deleted successfully.'})

# ==========================================
# 2. DASHBOARD KPI & CHARTS API
# ==========================================

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    conn = get_db()
    cursor = conn.cursor()

    total_plants = cursor.execute("SELECT COUNT(*) FROM plants").fetchone()[0]
    healthy_plants = cursor.execute("SELECT COUNT(*) FROM plants WHERE health_status = 'Healthy'").fetchone()[0]
    attention_plants = cursor.execute("SELECT COUNT(*) FROM plants WHERE health_status IN ('Needs Attention', 'Critical')").fetchone()[0]
    critical_plants = cursor.execute("SELECT COUNT(*) FROM plants WHERE health_status = 'Critical'").fetchone()[0]

    total_zones = cursor.execute("SELECT COUNT(*) FROM zones").fetchone()[0]
    avg_green_cover = cursor.execute("SELECT AVG(green_cover_percentage) FROM zones").fetchone()[0] or 80.0

    completed_tasks = cursor.execute("SELECT COUNT(*) FROM maintenance_tasks WHERE status = 'Completed'").fetchone()[0]
    pending_tasks = cursor.execute("SELECT COUNT(*) FROM maintenance_tasks WHERE status IN ('Pending', 'In Progress')").fetchone()[0]
    overdue_tasks = cursor.execute("SELECT COUNT(*) FROM maintenance_tasks WHERE status = 'Overdue'").fetchone()[0]

    latest_sust = cursor.execute("SELECT carbon_offset_kg, water_used_liters, water_saved_liters FROM sustainability_metrics ORDER BY id DESC LIMIT 1").fetchone()
    carbon_offset = latest_sust['carbon_offset_kg'] if latest_sust else 1980.5
    water_used = latest_sust['water_used_liters'] if latest_sust else 15400.0

    low_moisture_zones = cursor.execute("SELECT COUNT(DISTINCT zone_id) FROM sensor_readings WHERE soil_moisture < 30.0 AND timestamp = (SELECT MAX(timestamp) FROM sensor_readings)").fetchone()[0]

    open_issues = cursor.execute("SELECT COUNT(*) FROM issues WHERE status = 'Open'").fetchone()[0]

    conn.close()

    return jsonify({
        'total_plants': total_plants,
        'healthy_plants': healthy_plants,
        'attention_plants': attention_plants,
        'critical_plants': critical_plants,
        'total_zones': total_zones,
        'green_cover_percentage': round(avg_green_cover, 1),
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'estimated_carbon_offset_kg': round(carbon_offset, 1),
        'estimated_water_usage_liters': round(water_used, 1),
        'low_moisture_zones_count': low_moisture_zones,
        'open_issues_count': open_issues
    })

@app.route('/api/dashboard/charts', methods=['GET'])
def get_dashboard_charts():
    conn = get_db()
    cursor = conn.cursor()

    sust_rows = cursor.execute("SELECT date, green_cover, carbon_offset_kg, water_used_liters, water_saved_liters FROM sustainability_metrics ORDER BY id ASC").fetchall()
    
    healthy = cursor.execute("SELECT COUNT(*) FROM plants WHERE health_status = 'Healthy'").fetchone()[0]
    attention = cursor.execute("SELECT COUNT(*) FROM plants WHERE health_status = 'Needs Attention'").fetchone()[0]
    critical = cursor.execute("SELECT COUNT(*) FROM plants WHERE health_status = 'Critical'").fetchone()[0]

    tasks_by_type = cursor.execute("SELECT task_type, COUNT(*) as count FROM maintenance_tasks GROUP BY task_type").fetchall()

    conn.close()

    return jsonify({
        'sustainability_timeline': [dict(r) for r in sust_rows],
        'plant_health_distribution': {
            'Healthy': healthy,
            'Needs Attention': attention,
            'Critical': critical
        },
        'task_distribution': [dict(t) for t in tasks_by_type]
    })

# ==========================================
# 3. ZONES API
# ==========================================

@app.route('/api/zones', methods=['GET'])
def get_zones():
    conn = get_db()
    cursor = conn.cursor()
    zones = cursor.execute("""
    SELECT z.*, 
           (SELECT COUNT(*) FROM plants p WHERE p.zone_id = z.id) as plant_count,
           (SELECT soil_moisture FROM sensor_readings sr WHERE sr.zone_id = z.id ORDER BY sr.id DESC LIMIT 1) as latest_soil_moisture
    FROM zones z
    """).fetchall()
    conn.close()
    return jsonify([dict(z) for z in zones])

@app.route('/api/zones/<int:zone_id>', methods=['GET'])
def get_zone_detail(zone_id):
    conn = get_db()
    cursor = conn.cursor()
    zone = cursor.execute("SELECT * FROM zones WHERE id = ?", (zone_id,)).fetchone()
    if not zone:
        conn.close()
        return jsonify({'error': 'Zone not found'}), 404
    
    plants = cursor.execute("SELECT * FROM plants WHERE zone_id = ?", (zone_id,)).fetchall()
    sensors = cursor.execute("SELECT * FROM sensor_readings WHERE zone_id = ? ORDER BY id DESC LIMIT 5", (zone_id,)).fetchall()
    conn.close()
    return jsonify({
        'zone': dict(zone),
        'plants': [dict(p) for p in plants],
        'recent_sensors': [dict(s) for s in sensors]
    })

@app.route('/api/zones', methods=['POST'])
def add_zone():
    data = request.json or {}
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO zones (name, location, area, green_cover_percentage, health_status, map_x, map_y)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('name'),
        data.get('location', 'Campus'),
        float(data.get('area', 1000.0)),
        float(data.get('green_cover_percentage', 80.0)),
        data.get('health_status', 'Healthy'),
        int(data.get('map_x', 50)),
        int(data.get('map_y', 50))
    ))
    zone_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO sensor_readings (zone_id, soil_moisture, humidity, temperature, timestamp, status_alert)
    VALUES (?, 50.0, 60.0, 26.0, ?, 'Normal')
    """, (zone_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()
    return jsonify({'success': True, 'id': zone_id, 'message': 'Zone added successfully'})

@app.route('/api/zones/<int:zone_id>', methods=['PUT'])
def update_zone(zone_id):
    data = request.json or {}
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE zones 
    SET name = ?, location = ?, area = ?, green_cover_percentage = ?, health_status = ?, map_x = ?, map_y = ?
    WHERE id = ?
    """, (
        data.get('name'),
        data.get('location'),
        float(data.get('area')),
        float(data.get('green_cover_percentage')),
        data.get('health_status'),
        int(data.get('map_x', 50)),
        int(data.get('map_y', 50)),
        zone_id
    ))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Zone updated successfully'})

@app.route('/api/zones/<int:zone_id>', methods=['DELETE'])
def delete_zone(zone_id):
    conn = get_db()
    conn.execute("DELETE FROM zones WHERE id = ?", (zone_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Zone deleted successfully'})

# ==========================================
# 4. PLANT INVENTORY & QR BIOGRAPHY API
# ==========================================

@app.route('/api/plants', methods=['GET'])
def get_plants():
    zone_id = request.args.get('zone_id')
    health = request.args.get('health_status')
    search = request.args.get('search')

    query = """
    SELECT p.*, z.name as zone_name 
    FROM plants p 
    JOIN zones z ON p.zone_id = z.id 
    WHERE 1=1
    """
    params = []

    if zone_id and zone_id != 'all':
        query += " AND p.zone_id = ?"
        params.append(int(zone_id))
    if health and health != 'all':
        query += " AND p.health_status = ?"
        params.append(health)
    if search:
        query += " AND (p.name LIKE ? OR p.species LIKE ? OR p.plant_code LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])

    query += " ORDER BY p.id DESC"

    conn = get_db()
    plants = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(p) for p in plants])

@app.route('/api/plants/<int:plant_id>/qr', methods=['GET'])
def get_plant_qr(plant_id):
    conn = get_db()
    cursor = conn.cursor()
    plant = cursor.execute("""
    SELECT p.*, z.name as zone_name, z.location as zone_location
    FROM plants p JOIN zones z ON p.zone_id = z.id WHERE p.id = ?
    """, (plant_id,)).fetchone()
    conn.close()

    if not plant:
        return jsonify({'error': 'Plant not found'}), 404

    plant_dict = dict(plant)
    qr_content = f"https://biocampus.edu/plant/{plant_dict['plant_code']}"
    qr_image_url = f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={qr_content}"

    biography = {
        'plant': plant_dict,
        'qr_code_url': qr_image_url,
        'environmental_benefits': 'Absorbs ~21.8 kg CO2/year, improves microclimate, reduces noise pollution.',
        'care_guidelines': 'Water every 1-2 days. Apply organic compost monthly. Check for aphid spots in spring.',
        'campus_history': f"Planted on {plant_dict['planted_date']} as part of campus greening initiatives."
    }
    return jsonify(biography)

@app.route('/api/plants', methods=['POST'])
def add_plant():
    data = request.json or {}
    conn = get_db()
    cursor = conn.cursor()

    count = cursor.execute("SELECT COUNT(*) FROM plants").fetchone()[0]
    plant_code = f"P-{101 + count}"
    now_str = datetime.now().strftime("%Y-%m-%d")
    next_water = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    cursor.execute("""
    INSERT INTO plants (plant_code, name, species, type, planted_date, zone_id, health_status, last_watered, next_watering, last_fertilized, photo, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        plant_code,
        data.get('name'),
        data.get('species', 'Unspecified'),
        data.get('type', 'Tree'),
        data.get('planted_date', now_str),
        int(data.get('zone_id', 1)),
        data.get('health_status', 'Healthy'),
        data.get('last_watered', now_str),
        data.get('next_watering', next_water),
        data.get('last_fertilized', now_str),
        data.get('photo', 'https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=600'),
        data.get('notes', '')
    ))
    plant_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'id': plant_id, 'plant_code': plant_code, 'message': 'Plant added successfully'})

@app.route('/api/plants/<int:plant_id>', methods=['PUT'])
def update_plant(plant_id):
    data = request.json or {}
    conn = get_db()
    conn.execute("""
    UPDATE plants 
    SET name = ?, species = ?, type = ?, zone_id = ?, health_status = ?, last_watered = ?, next_watering = ?, last_fertilized = ?, photo = ?, notes = ?
    WHERE id = ?
    """, (
        data.get('name'),
        data.get('species'),
        data.get('type'),
        int(data.get('zone_id')),
        data.get('health_status'),
        data.get('last_watered'),
        data.get('next_watering'),
        data.get('last_fertilized'),
        data.get('photo'),
        data.get('notes'),
        plant_id
    ))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Plant updated successfully'})

@app.route('/api/plants/<int:plant_id>', methods=['DELETE'])
def delete_plant(plant_id):
    conn = get_db()
    conn.execute("DELETE FROM plants WHERE id = ?", (plant_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Plant deleted successfully'})

# ==========================================
# SMART PLANT REPLACEMENT RECOMMENDATION API
# ==========================================

def calculate_compatibility(zone, telemetry, candidate):
    score = 100.0
    ph_val = float(zone.get('ph_level', 6.5) if zone and zone.get('ph_level') else 6.5)
    ph_min = float(candidate.get('ph_min', 6.0))
    ph_max = float(candidate.get('ph_max', 7.5))
    if ph_val < ph_min:
        score -= min(25.0, (ph_min - ph_val) * 15.0)
    elif ph_val > ph_max:
        score -= min(25.0, (ph_val - ph_max) * 15.0)

    sun_zone = str(zone.get('sunlight_type') or 'Full Sun').lower() if zone else 'full sun'
    sun_cand = str(candidate.get('ideal_sunlight') or 'Full Sun').lower()
    if sun_zone not in sun_cand and sun_cand not in sun_zone:
        score -= 18.0

    moist_val = float(telemetry.get('soil_moisture', 50.0) if telemetry and telemetry.get('soil_moisture') else 50.0)
    m_min = float(candidate.get('moisture_min', 30.0))
    m_max = float(candidate.get('moisture_max', 75.0))
    if moist_val < m_min:
        score -= min(20.0, (m_min - moist_val) * 0.6)
    elif moist_val > m_max:
        score -= min(20.0, (moist_val - m_max) * 0.4)

    temp_val = float(telemetry.get('temperature', 28.0) if telemetry and telemetry.get('temperature') else 28.0)
    t_min = float(candidate.get('temp_min', 15.0))
    t_max = float(candidate.get('temp_max', 40.0))
    if temp_val < t_min or temp_val > t_max:
        score -= 12.0

    return int(round(max(65.0, min(98.0, score))))

@app.route('/api/plants/replacement-recommendations', methods=['GET'])
def get_replacement_recommendations():
    plant_id = request.args.get('plant_id')
    zone_id = request.args.get('zone_id')

    conn = get_db()
    cursor = conn.cursor()

    plant_info = None
    if plant_id:
        p_row = cursor.execute("SELECT * FROM plants WHERE id = ?", (plant_id,)).fetchone()
        if p_row:
            plant_info = dict(p_row)
            if not zone_id:
                zone_id = plant_info['zone_id']

    if not zone_id:
        zone_id = 1

    zone_row = cursor.execute("SELECT * FROM zones WHERE id = ?", (zone_id,)).fetchone()
    zone_dict = dict(zone_row) if zone_row else {'id': zone_id, 'name': 'Main Garden', 'location': 'Campus Quad', 'soil_type': 'Loamy', 'ph_level': 6.5, 'sunlight_type': 'Partial Sun', 'water_source': 'Drip Irrigation'}

    sr_row = cursor.execute("SELECT * FROM sensor_readings WHERE zone_id = ? ORDER BY id DESC LIMIT 1", (zone_id,)).fetchone()
    telemetry = dict(sr_row) if sr_row else {'soil_moisture': 55.0, 'temperature': 28.5, 'humidity': 65.0}

    catalog_rows = cursor.execute("SELECT * FROM plant_catalog").fetchall()
    candidates = [dict(c) for c in catalog_rows]

    recommendations = []
    for cand in candidates:
        comp_score = calculate_compatibility(zone_dict, telemetry, cand)
        cand['compatibility_score'] = comp_score
        recommendations.append(cand)

    recommendations.sort(key=lambda x: x['compatibility_score'], reverse=True)
    top_recommendations = recommendations[:5]

    conn.close()

    return jsonify({
        'success': True,
        'old_plant': plant_info,
        'location_analysis': {
            'zone_id': zone_dict['id'],
            'zone_name': zone_dict['name'],
            'location': zone_dict.get('location', 'Campus Quad'),
            'soil_type': zone_dict.get('soil_type', 'Loamy'),
            'ph_level': zone_dict.get('ph_level', 6.5),
            'sunlight': zone_dict.get('sunlight_type', 'Partial Sun'),
            'moisture': f"{telemetry.get('soil_moisture', 55.0)}%",
            'temperature': f"{telemetry.get('temperature', 28.5)}°C",
            'water_source': zone_dict.get('water_source', 'Drip Irrigation')
        },
        'recommendations': top_recommendations
    })

@app.route('/api/plants/replace', methods=['POST'])
def replace_plant():
    data = request.json or {}
    plant_id = data.get('plant_id')
    catalog_id = data.get('catalog_id')
    replaced_by = session.get('name') or 'Dr. Eleanor Vance'

    if not plant_id or not catalog_id:
        return jsonify({'error': 'plant_id and catalog_id are required'}), 400

    conn = get_db()
    cursor = conn.cursor()

    old_p = cursor.execute("SELECT p.*, z.name as zone_name FROM plants p JOIN zones z ON p.zone_id = z.id WHERE p.id = ?", (plant_id,)).fetchone()
    if not old_p:
        conn.close()
        return jsonify({'error': 'Original plant record not found'}), 404
    old_p = dict(old_p)

    cat_p = cursor.execute("SELECT * FROM plant_catalog WHERE id = ?", (catalog_id,)).fetchone()
    if not cat_p:
        conn.close()
        return jsonify({'error': 'Replacement candidate not found'}), 404
    cat_p = dict(cat_p)

    z_row = cursor.execute("SELECT * FROM zones WHERE id = ?", (old_p['zone_id'],)).fetchone()
    s_row = cursor.execute("SELECT * FROM sensor_readings WHERE zone_id = ? ORDER BY id DESC LIMIT 1", (old_p['zone_id'],)).fetchone()
    comp_score = calculate_compatibility(dict(z_row) if z_row else {}, dict(s_row) if s_row else {}, cat_p)

    today_str = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
    UPDATE plants
    SET name = ?, species = ?, type = ?, photo = ?, planted_date = ?, health_status = 'Healthy', notes = ?
    WHERE id = ?
    """, (
        cat_p['name'],
        cat_p['species'],
        cat_p['type'],
        cat_p['photo'],
        today_str,
        f"Replaced {old_p['name']} ({old_p['plant_code']}) on {today_str}. Agronomic match: {comp_score}%.",
        plant_id
    ))

    cursor.execute("""
    INSERT INTO plant_replacements
    (old_plant_name, old_plant_code, new_plant_name, new_plant_species, zone_id, zone_name, compatibility_score, date, replaced_by)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        old_p['name'],
        old_p['plant_code'],
        cat_p['name'],
        cat_p['species'],
        old_p['zone_id'],
        old_p['zone_name'],
        comp_score,
        today_str,
        replaced_by
    ))

    cursor.execute("INSERT INTO notifications (user_id, message, type, read_status, created_at) VALUES (1, ?, 'system', 0, ?)", (
        f"🌱 Smart Plant Replacement Confirmed: {old_p['name']} replaced with {cat_p['name']} ({comp_score}% Match) in {old_p['zone_name']}.",
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': f"Plant successfully replaced with {cat_p['name']} ({comp_score}% Match). Inventory & History updated!"
    })

@app.route('/api/plants/replacement-history', methods=['GET'])
def get_replacement_history():
    conn = get_db()
    cursor = conn.cursor()
    history = cursor.execute("SELECT * FROM plant_replacements ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(h) for h in history])

@app.route('/api/plants/<int:plant_id>/health', methods=['POST'])
def update_plant_health(plant_id):
    data = request.json or {}
    new_status = data.get('health_status')
    observation = data.get('observation', '')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE plants SET health_status = ? WHERE id = ?", (new_status, plant_id))

    if new_status in ['Needs Attention', 'Critical']:
        plant = cursor.execute("SELECT name FROM plants WHERE id = ?", (plant_id,)).fetchone()
        plant_name = plant['name'] if plant else f"Plant #{plant_id}"
        cursor.execute("""
        INSERT INTO notifications (user_id, message, type, read_status, created_at)
        VALUES (1, ?, ?, 0, ?)
        """, (f"Plant '{plant_name}' status updated to {new_status}: {observation}", 'Warning' if new_status=='Needs Attention' else 'Critical', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Plant health status updated successfully'})

# ==========================================
# 5. MAINTENANCE TASKS API
# ==========================================

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    status = request.args.get('status')
    zone_id = request.args.get('zone_id')
    task_type = request.args.get('task_type')

    query = """
    SELECT t.*, z.name as zone_name, p.name as plant_name, p.plant_code
    FROM maintenance_tasks t
    JOIN zones z ON t.zone_id = z.id
    LEFT JOIN plants p ON t.plant_id = p.id
    WHERE 1=1
    """
    params = []

    if status and status != 'all':
        query += " AND t.status = ?"
        params.append(status)
    if zone_id and zone_id != 'all':
        query += " AND t.zone_id = ?"
        params.append(int(zone_id))
    if task_type and task_type != 'all':
        query += " AND t.task_type = ?"
        params.append(task_type)

    query += " ORDER BY t.id DESC"

    conn = get_db()
    tasks = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(t) for t in tasks])

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json or {}
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO maintenance_tasks 
    (plant_id, zone_id, task_type, assigned_to, scheduled_date, status, priority, notes, created_by)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('plant_id') if data.get('plant_id') else None,
        int(data.get('zone_id', 1)),
        data.get('task_type', 'Watering'),
        data.get('assigned_to', 'Rajesh Kumar'),
        data.get('scheduled_date', datetime.now().strftime("%Y-%m-%d")),
        data.get('status', 'Pending'),
        data.get('priority', 'Medium'),
        data.get('notes', ''),
        data.get('created_by', 'Admin')
    ))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'id': task_id, 'message': 'Task created successfully'})

@app.route('/api/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    data = request.json or {}
    photo_proof = data.get('photo_proof', 'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=600')
    notes = data.get('notes', 'Completed by gardening staff.')
    now_str = datetime.now().strftime("%Y-%m-%d")

    conn = get_db()
    cursor = conn.cursor()

    task = cursor.execute("SELECT * FROM maintenance_tasks WHERE id = ?", (task_id,)).fetchone()
    if task:
        cursor.execute("""
        UPDATE maintenance_tasks
        SET status = 'Completed', completion_date = ?, photo_proof = ?, notes = ?
        WHERE id = ?
        """, (now_str, photo_proof, notes, task_id))

        if task['plant_id'] and task['task_type'] == 'Watering':
            next_w = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            cursor.execute("UPDATE plants SET last_watered = ?, next_watering = ?, health_status = 'Healthy' WHERE id = ?", (now_str, next_w, task['plant_id']))

    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Task marked as completed with photo proof'})

# ==========================================
# 6. SMART IRRIGATION & IOT TELEMETRY API
# ==========================================

@app.route('/api/sensors/readings', methods=['GET'])
def get_sensor_readings():
    conn = get_db()
    cursor = conn.cursor()
    query = """
    SELECT sr.*, z.name as zone_name, z.location as zone_location
    FROM sensor_readings sr
    JOIN zones z ON sr.zone_id = z.id
    WHERE sr.id IN (
        SELECT MAX(id) FROM sensor_readings GROUP BY zone_id
    )
    ORDER BY sr.zone_id ASC
    """
    readings = cursor.execute(query).fetchall()
    conn.close()
    return jsonify([dict(r) for r in readings])

@app.route('/api/iot/irrigate', methods=['POST'])
def trigger_irrigation():
    data = request.json or {}
    zone_id = int(data.get('zone_id', 1))
    duration_mins = int(data.get('duration_mins', 15))

    conn = get_db()
    cursor = conn.cursor()

    zone = cursor.execute("SELECT name FROM zones WHERE id = ?", (zone_id,)).fetchone()
    zone_name = zone['name'] if zone else f"Zone #{zone_id}"

    cursor.execute("SELECT soil_moisture FROM sensor_readings WHERE zone_id = ? ORDER BY id DESC LIMIT 1", (zone_id,))
    last_r = cursor.fetchone()
    current_m = last_r['soil_moisture'] if last_r else 25.0
    new_m = min(85.0, round(current_m + (duration_mins * 2.5), 1))
    now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO sensor_readings (zone_id, soil_moisture, humidity, temperature, timestamp, status_alert)
    VALUES (?, ?, 68.0, 25.5, ?, 'Normal')
    """, (zone_id, new_m, now_ts))

    cursor.execute("UPDATE plants SET health_status = 'Healthy', last_watered = ? WHERE zone_id = ? AND health_status = 'Critical'", (datetime.now().strftime("%Y-%m-%d"), zone_id))

    cursor.execute("""
    INSERT INTO notifications (user_id, message, type, read_status, created_at)
    VALUES (1, ?, 'Info', 0, ?)
    """, (f"Smart Irrigation activated for '{zone_name}' ({duration_mins} mins). Soil moisture restored to {new_m}%.", now_ts))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'zone_id': zone_id,
        'new_soil_moisture': new_m,
        'water_consumed_liters': round(duration_mins * 12.5, 1),
        'message': f"Smart drip irrigation successfully activated for {zone_name}!"
    })

# ==========================================
# 7. CAMPUS ISSUES & REPORTING API
# ==========================================

@app.route('/api/issues', methods=['GET'])
def get_issues():
    conn = get_db()
    cursor = conn.cursor()
    issues = cursor.execute("""
    SELECT i.*, z.name as zone_name, p.name as plant_name
    FROM issues i
    JOIN zones z ON i.zone_id = z.id
    LEFT JOIN plants p ON i.plant_id = p.id
    ORDER BY i.id DESC
    """).fetchall()
    conn.close()
    return jsonify([dict(i) for i in issues])

@app.route('/api/issues', methods=['POST'])
def add_issue():
    data = request.json or {}
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO issues (title, reporter_name, zone_id, plant_id, issue_type, priority, description, status, photo, reported_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'Open', ?, ?)
    """, (
        data.get('title'),
        data.get('reporter_name', 'Student Volunteer'),
        int(data.get('zone_id', 1)),
        data.get('plant_id'),
        data.get('issue_type', 'General'),
        data.get('priority', 'Medium'),
        data.get('description', ''),
        data.get('photo', 'https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=600'),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    issue_id = cursor.lastrowid

    # Notify Admin
    cursor.execute("""
    INSERT INTO notifications (user_id, message, type, read_status, created_at)
    VALUES (1, ?, 'Warning', 0, ?)
    """, (f"New Campus Issue reported: '{data.get('title')}' in Zone #{data.get('zone_id')}.", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()
    return jsonify({'success': True, 'id': issue_id, 'message': 'Campus green issue reported successfully!'})

@app.route('/api/issues/<int:issue_id>/convert-task', methods=['POST'])
def convert_issue_to_task(issue_id):
    conn = get_db()
    cursor = conn.cursor()
    issue = cursor.execute("SELECT * FROM issues WHERE id = ?", (issue_id,)).fetchone()
    if not issue:
        conn.close()
        return jsonify({'error': 'Issue not found'}), 404

    today_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
    INSERT INTO maintenance_tasks (plant_id, zone_id, task_type, assigned_to, scheduled_date, status, priority, notes, created_by)
    VALUES (?, ?, ?, 'Rajesh Kumar', ?, 'Pending', ?, ?, 'Issue Conversion')
    """, (
        issue['plant_id'],
        issue['zone_id'],
        issue['issue_type'] if issue['issue_type'] in ['Watering', 'Pruning', 'Pest Control'] else 'General Maintenance',
        today_str,
        issue['priority'],
        f"Converted from Issue #{issue['id']}: {issue['title']} - {issue['description']}"
    ))
    task_id = cursor.lastrowid
    cursor.execute("UPDATE issues SET status = 'In Progress', converted_task_id = ? WHERE id = ?", (task_id, issue_id))

    conn.commit()
    conn.close()
    return jsonify({'success': True, 'task_id': task_id, 'message': f'Issue #{issue_id} converted to Maintenance Task #{task_id}'})

# ==========================================
# 8. STUDENT REWARDS STORE API
# ==========================================

@app.route('/api/rewards', methods=['GET'])
def get_rewards():
    conn = get_db()
    cursor = conn.cursor()
    rewards = cursor.execute("SELECT * FROM rewards").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rewards])

@app.route('/api/rewards/redeem', methods=['POST'])
def redeem_reward():
    data = request.json or {}
    volunteer_name = data.get('volunteer_name', 'Aarav Sharma')
    reward_id = int(data.get('reward_id', 1))

    conn = get_db()
    cursor = conn.cursor()

    reward = cursor.execute("SELECT * FROM rewards WHERE id = ?", (reward_id,)).fetchone()
    if not reward:
        conn.close()
        return jsonify({'error': 'Reward not found'}), 404

    # Calculate student's total approved points
    points_row = cursor.execute("""
    SELECT SUM(points) FROM volunteer_activities WHERE volunteer_name = ? AND status = 'Approved'
    """, (volunteer_name,)).fetchone()
    total_pts = points_row[0] or 0

    # Calculate already spent points
    spent_row = cursor.execute("""
    SELECT SUM(cost_points) FROM user_redemptions WHERE volunteer_name = ?
    """, (volunteer_name,)).fetchone()
    spent_pts = spent_row[0] or 0

    available_pts = total_pts - spent_pts
    if available_pts < reward['cost_points']:
        conn.close()
        return jsonify({'success': False, 'message': f"Insufficient points! You need {reward['cost_points']} pts (Available: {available_pts} pts)"}), 400

    claim_code = f"ECO-{random.randint(10000, 99999)}"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO user_redemptions (volunteer_name, reward_id, reward_title, cost_points, date, claim_code)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (volunteer_name, reward_id, reward['title'], reward['cost_points'], now_str, claim_code))

    cursor.execute("UPDATE rewards SET stock = stock - 1 WHERE id = ?", (reward_id,))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'claim_code': claim_code,
        'reward_title': reward['title'],
        'message': f"Congratulations! Redeemed '{reward['title']}'. Show Voucher Code: {claim_code} at Green Committee Desk."
    })

# ==========================================
# 9. AI CAMPUS ASSISTANT CHATBOT API
# ==========================================

@app.route('/api/ai/chatbot', methods=['POST'])
def ai_chatbot():
    data = request.json or {}
    user_msg = (data.get('message') or '').strip().lower()

    conn = get_db()
    cursor = conn.cursor()

    if 'moisture' in user_msg or 'soil' in user_msg or 'irrigation' in user_msg:
        readings = cursor.execute("SELECT z.name, sr.soil_moisture FROM sensor_readings sr JOIN zones z ON sr.zone_id = z.id WHERE sr.id IN (SELECT MAX(id) FROM sensor_readings GROUP BY zone_id)").fetchall()
        readings_str = ", ".join([f"{r['name']}: {r['soil_moisture']}%" for r in readings])
        reply = f"🌿 **FloraAI Sensor Telemetry Update**:\nHere are the live zone soil moisture levels:\n{readings_str}.\nIf any zone drops below 30%, smart drip irrigation can be triggered automatically."
    
    elif 'plant' in user_msg or 'tree' in user_msg or 'count' in user_msg or 'healthy' in user_msg:
        count = cursor.execute("SELECT COUNT(*) FROM plants").fetchone()[0]
        healthy = cursor.execute("SELECT COUNT(*) FROM plants WHERE health_status = 'Healthy'").fetchone()[0]
        reply = f"🌱 **Campus Botanical Overview**:\nCurrently, BioCampus manages **{count} registered plants and trees** across 6 zones, with **{healthy} healthy flora** ({round((healthy/count)*100)}% health rating)."

    elif 'volunteer' in user_msg or 'point' in user_msg or 'reward' in user_msg or 'badge' in user_msg:
        reply = "🏆 **BioCampus Volunteer Program**:\nStudents can earn points by participating in tree plantation drives, medicinal bed weeding, or drip line checks! Accumulated points unlock badges like *Plant Protector* and *Green Campus Hero*, which can be redeemed for Eco Cotton Bags or Potted Saplings in the Rewards Store!"

    elif 'task' in user_msg or 'water' in user_msg or 'prune' in user_msg:
        pending = cursor.execute("SELECT COUNT(*) FROM maintenance_tasks WHERE status = 'Pending'").fetchone()[0]
        reply = f"📋 **Maintenance Operations**:\nThere are currently **{pending} pending maintenance tasks** assigned to gardening staff. Tasks include daily drip watering, monthly pruning, and organic neem pest spraying."

    else:
        reply = f"👋 Hello! I am **FloraAI**, your Smart Green Campus Assistant. You can ask me about:\n- 🌊 Live soil moisture & smart irrigation\n- 🌳 Campus plant inventory & health stats\n- 🏆 Student volunteer points & rewards\n- 📋 Maintenance schedules & reported issues"

    conn.close()
    return jsonify({'reply': reply})

# ==========================================
# 10. AI PLANT HEALTH & DISEASE SCANNER API
# ==========================================

@app.route('/api/ai/plant-health-scan', methods=['POST'])
def ai_plant_health_scan():
    data = request.json or {}
    plant_id = data.get('plant_id')

    conditions = [
        {
            'status': 'Needs Attention',
            'disease': 'Aphid Infestation & Leaf Curling',
            'confidence': 94.2,
            'symptoms': 'Small green aphids detected on tender shoots causing leaf margin curling.',
            'treatment': 'Spray organic Neem oil solution (5ml/L water) every 3 days. Prune heavily infested shoots.'
        },
        {
            'status': 'Critical',
            'disease': 'Fungal Leaf Spot (Cercospora)',
            'confidence': 91.8,
            'symptoms': 'Circular brown spots with yellow halos appearing on mature leaves.',
            'treatment': 'Apply copper-based organic fungicide. Reduce overhead watering to keep foliage dry.'
        },
        {
            'status': 'Healthy',
            'disease': 'Healthy Foliage (No Disease Detected)',
            'confidence': 98.5,
            'symptoms': 'Vibrant green leaves, sturdy stem texture, optimal turgor pressure.',
            'treatment': 'Maintain regular watering schedule and apply organic compost monthly.'
        }
    ]

    result = random.choice(conditions)

    if plant_id:
        conn = get_db()
        conn.execute("UPDATE plants SET health_status = ? WHERE id = ?", (result['status'], plant_id))
        conn.commit()
        conn.close()

    return jsonify({
        'success': True,
        'scan_result': result,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# ==========================================
# 11. SUSTAINABILITY & BIODIVERSITY API
# ==========================================

@app.route('/api/sustainability', methods=['GET'])
def get_sustainability():
    conn = get_db()
    cursor = conn.cursor()
    history = cursor.execute("SELECT * FROM sustainability_metrics ORDER BY id ASC").fetchall()
    
    total_trees = cursor.execute("SELECT COUNT(*) FROM plants WHERE type = 'Tree'").fetchone()[0]
    total_plants = cursor.execute("SELECT COUNT(*) FROM plants").fetchone()[0]
    bio_count = cursor.execute("SELECT COUNT(DISTINCT species_name) FROM biodiversity_logs").fetchone()[0]

    conn.close()
    return jsonify({
        'history': [dict(h) for h in history],
        'total_trees': total_trees,
        'total_plants': total_plants,
        'biodiversity_count': bio_count
    })

@app.route('/api/biodiversity', methods=['GET'])
def get_biodiversity():
    conn = get_db()
    cursor = conn.cursor()
    logs = cursor.execute("""
    SELECT b.*, z.name as zone_name
    FROM biodiversity_logs b
    JOIN zones z ON b.zone_id = z.id
    ORDER BY b.id DESC
    """).fetchall()

    category_counts = cursor.execute("SELECT category, COUNT(*) as count, SUM(count) as total_individuals FROM biodiversity_logs GROUP BY category").fetchall()

    conn.close()
    return jsonify({
        'logs': [dict(l) for l in logs],
        'category_summary': [dict(c) for c in category_counts]
    })

@app.route('/api/biodiversity', methods=['POST'])
def add_biodiversity():
    data = request.json or {}
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO biodiversity_logs (species_name, category, count, zone_id, observation_date, photo, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('species_name'),
        data.get('category', 'Plant'),
        int(data.get('count', 1)),
        int(data.get('zone_id', 1)),
        data.get('observation_date', datetime.now().strftime("%Y-%m-%d")),
        data.get('photo', 'https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=600'),
        data.get('notes', '')
    ))
    log_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'id': log_id, 'message': 'Biodiversity log added successfully'})

# ==========================================
# 12. VOLUNTEER MODULE API
# ==========================================

def get_effective_role(req):
    role = None
    if req.is_json and req.json and req.json.get('role'):
        role = req.json.get('role')
    if not role and req.args.get('role'):
        role = req.args.get('role')
    if not role:
        role = session.get('role')
    return (role or 'Admin').strip()

def is_student_role(role_name):
    r = str(role_name or '').lower()
    return 'student' in r

def is_staff_or_admin(role_name):
    r = str(role_name or '').lower()
    return 'staff' in r or 'admin' in r or 'gardener' in r

@app.route('/api/volunteers/activities', methods=['GET'])
def get_volunteer_activities():
    user_role = get_effective_role(request)
    user_name = session.get('name') or 'Aarav Sharma'
    user_id = int(session.get('user_id') or 4)
    first_name = user_name.lower().split()[0] if user_name else 'aarav'

    conn = get_db()
    cursor = conn.cursor()

    if is_student_role(user_role):
        activities = cursor.execute("""
        SELECT v.*, z.name as zone_name 
        FROM volunteer_activities v
        LEFT JOIN zones z ON v.zone_id = z.id
        WHERE v.volunteer_id = ? OR LOWER(v.volunteer_name) LIKE ?
        ORDER BY v.id DESC
        """, (user_id, f"%{first_name}%")).fetchall()
    else:
        activities = cursor.execute("""
        SELECT v.*, z.name as zone_name 
        FROM volunteer_activities v
        LEFT JOIN zones z ON v.zone_id = z.id
        ORDER BY v.id DESC
        """).fetchall()

    conn.close()
    return jsonify([dict(a) for a in activities])

@app.route('/api/volunteers/claim', methods=['POST'])
def claim_volunteer_activity():
    user_role = get_effective_role(request)
    if is_staff_or_admin(user_role):
        return jsonify({'error': 'Unauthorized. Only Students are eligible to submit reward activity proofs for points.'}), 403

    data = request.json or {}
    conn = get_db()
    cursor = conn.cursor()

    proof_photo = data.get('proof_photo') or 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=600'
    title = data.get('title') or 'Plant Maintenance Contribution'
    vol_id = int(data.get('volunteer_id') or session.get('user_id') or 4)
    vol_name = data.get('volunteer_name') or session.get('name') or 'Aarav Sharma'
    zone_id = int(data.get('zone_id', 1))

    # AI Plant Classification Engine
    detected_plant = data.get('detected_plant')
    if not detected_plant:
        ai_candidates = ['Rose Bush (Rosa rubiginosa)', 'Neem Tree (Azadirachta indica)', 'Aloe Vera Bed', 'Tulsi (Ocimum sanctum)', 'Hibiscus (Hibiscus rosa-sinensis)', 'Bougainvillea Vine']
        detected_plant = random.choice(ai_candidates)

    # Authenticity / Duplicate Submission Check
    existing_dup = cursor.execute("SELECT id FROM volunteer_activities WHERE proof_photo = ? AND volunteer_name = ?", (proof_photo, vol_name)).fetchone()
    dup_flag = " (Duplicate Photo Warning Flagged)" if existing_dup else ""

    # Always create as 'Pending Verification' with 0 initial points awarded
    cursor.execute("""
    INSERT INTO volunteer_activities 
    (title, volunteer_id, volunteer_name, date, points, proof_photo, status, description, zone_id, detected_plant, verified_by, verification_date)
    VALUES (?, ?, ?, ?, 0, ?, 'Pending Verification', ?, ?, ?, NULL, NULL)
    """, (
        title,
        vol_id,
        vol_name,
        datetime.now().strftime("%Y-%m-%d"),
        proof_photo,
        f"{data.get('description', 'Student activity upload for reward verification.')}{dup_flag}",
        zone_id,
        detected_plant
    ))
    act_id = cursor.lastrowid
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Notify Staff/Admin for review
    cursor.execute("""
    INSERT INTO notifications (user_id, message, type, read_status, created_at)
    VALUES (1, ?, 'Info', 0, ?)
    """, (
        f"📸 New Reward Submission Pending Verification: Student {vol_name} submitted '{title}' ({detected_plant}).",
        now_str
    ))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'id': act_id,
        'status': 'Pending Verification',
        'detected_plant': detected_plant,
        'message': f"Submission uploaded! AI Detected: {detected_plant}. Pending Staff/Admin verification before reward points are awarded."
    })

@app.route('/api/volunteers/pending-verifications', methods=['GET'])
def get_pending_verifications():
    user_role = get_effective_role(request)
    if is_student_role(user_role):
        return jsonify({'error': 'Access Denied. Verification queue is restricted to Staff and Admin.'}), 403

    conn = get_db()
    cursor = conn.cursor()
    pending = cursor.execute("""
    SELECT v.*, z.name as zone_name 
    FROM volunteer_activities v
    LEFT JOIN zones z ON v.zone_id = z.id
    WHERE v.status = 'Pending Verification'
    ORDER BY v.id DESC
    """).fetchall()
    conn.close()
    return jsonify([dict(p) for p in pending])

@app.route('/api/volunteers/verify/<int:activity_id>', methods=['POST'])
def verify_student_activity(activity_id):
    user_role = get_effective_role(request)
    if is_student_role(user_role):
        return jsonify({'error': 'Unauthorized. Only Staff and Admin can approve or reject reward submissions.'}), 403

    data = request.json or {}
    action = (data.get('action') or '').lower()
    verifier = session.get('name') or data.get('verified_by') or 'Dr. Eleanor Vance (Admin)'
    target_points = int(data.get('points') or 50)

    conn = get_db()
    cursor = conn.cursor()

    activity = cursor.execute("SELECT * FROM volunteer_activities WHERE id = ?", (activity_id,)).fetchone()
    if not activity:
        conn.close()
        return jsonify({'error': 'Submission record not found'}), 404
    
    act_dict = dict(activity)

    if act_dict['status'] != 'Pending Verification':
        conn.close()
        return jsonify({'error': f"Submission has already been processed with status '{act_dict['status']}'."}), 400

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if action == 'approve':
        cursor.execute("""
        UPDATE volunteer_activities
        SET status = 'Approved', points = ?, verified_by = ?, verification_date = ?
        WHERE id = ?
        """, (target_points, verifier, now_str, activity_id))

        cursor.execute("""
        INSERT INTO notifications (user_id, message, type, read_status, created_at)
        VALUES (?, ?, 'Info', 0, ?)
        """, (
            act_dict['volunteer_id'] or 4,
            f"🏆 Reward Submission Approved! +{target_points} Points credited for '{act_dict['title']}'. Verified by {verifier}.",
            now_str
        ))

        conn.commit()
        conn.close()
        return jsonify({
            'success': True,
            'status': 'Approved',
            'points_awarded': target_points,
            'message': f"Submission approved! {target_points} reward points credited to {act_dict['volunteer_name']}."
        })

    elif action == 'reject':
        cursor.execute("""
        UPDATE volunteer_activities
        SET status = 'Rejected', points = 0, verified_by = ?, verification_date = ?
        WHERE id = ?
        """, (verifier, now_str, activity_id))

        cursor.execute("""
        INSERT INTO notifications (user_id, message, type, read_status, created_at)
        VALUES (?, ?, 'Warning', 0, ?)
        """, (
            act_dict['volunteer_id'] or 4,
            f"❌ Reward Submission Rejected. 0 points awarded for '{act_dict['title']}'. Reviewed by {verifier}.",
            now_str
        ))

        conn.commit()
        conn.close()
        return jsonify({
            'success': True,
            'status': 'Rejected',
            'points_awarded': 0,
            'message': f"Submission rejected. 0 points awarded to {act_dict['volunteer_name']}."
        })

    else:
        conn.close()
        return jsonify({'error': 'Invalid action. Must be "approve" or "reject".'}), 400

@app.route('/api/volunteers/leaderboard', methods=['GET'])
def get_volunteer_leaderboard():
    conn = get_db()
    cursor = conn.cursor()
    rows = cursor.execute("""
    SELECT volunteer_name, SUM(points) as total_points, COUNT(*) as activities_completed
    FROM volunteer_activities
    WHERE status = 'Approved'
    GROUP BY volunteer_name
    ORDER BY total_points DESC
    """).fetchall()

    leaderboard = []
    badges_map = [
        (500, 'Green Campus Hero 🏆'),
        (300, 'Eco Champion 🌿'),
        (150, 'Plant Protector 🌱'),
        (0, 'Green Starter 🍃')
    ]

    for idx, r in enumerate(rows):
        pts = r['total_points']
        user_badge = 'Green Starter 🍃'
        for threshold, b_name in badges_map:
            if pts >= threshold:
                user_badge = b_name
                break
        leaderboard.append({
            'rank': idx + 1,
            'name': r['volunteer_name'],
            'points': pts,
            'activities': r['activities_completed'],
            'badge': user_badge
        })

    conn.close()
    return jsonify(leaderboard)

# ==========================================
# 13. NOTIFICATIONS & SETTINGS API
# ==========================================

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    conn = get_db()
    cursor = conn.cursor()
    notes = cursor.execute("SELECT * FROM notifications ORDER BY id DESC LIMIT 20").fetchall()
    unread_count = cursor.execute("SELECT COUNT(*) FROM notifications WHERE read_status = 0").fetchone()[0]
    conn.close()
    return jsonify({
        'notifications': [dict(n) for n in notes],
        'unread_count': unread_count
    })

@app.route('/api/notifications/read-all', methods=['POST'])
def mark_notifications_read():
    conn = get_db()
    conn.execute("UPDATE notifications SET read_status = 1")
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Notifications marked as read'})

@app.route('/api/scheduler/config', methods=['GET', 'POST'])
def handle_scheduler_config():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        data = request.json or {}
        task_type = data.get('task_type')
        freq = int(data.get('frequency_days', 7))
        auto = 1 if data.get('auto_enabled', True) else 0
        cursor.execute("UPDATE scheduler_config SET frequency_days = ?, auto_enabled = ? WHERE task_type = ?", (freq, auto, task_type))
        conn.commit()
        run_scheduler_cycle()
        conn.close()
        return jsonify({'success': True, 'message': 'Scheduler settings updated'})

    configs = cursor.execute("SELECT * FROM scheduler_config").fetchall()
    conn.close()
    return jsonify([dict(c) for c in configs])

@app.route('/api/system/reset-demo', methods=['POST'])
def reset_demo_system():
    init_db(force_reseed=True)
    return jsonify({'success': True, 'message': 'System database reset & re-seeded with demo data successfully!'})

@app.route('/api/system/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'online', 'service': 'Smart Campus Gardening API', 'timestamp': datetime.now().isoformat()})

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    if path.startswith('api/'):
        return jsonify({'error': 'Endpoint not found'}), 404
    if '.' in path:
        return ('Resource not found', 404)
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    print("Starting Smart Campus Gardening REST API Server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)

