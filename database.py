import sqlite3
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

import shutil

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "campus_gardening.db")

def get_db_path():
    # Handle read-only serverless environment like Vercel
    if os.environ.get('VERCEL') or not os.access(os.path.dirname(DB_PATH), os.W_OK):
        tmp_db = os.path.join("/tmp", "campus_gardening.db")
        if not os.path.exists(tmp_db) and os.path.exists(DB_PATH):
            try:
                shutil.copy2(DB_PATH, tmp_db)
            except Exception as e:
                print("Error copying DB to /tmp:", e)
        return tmp_db if os.path.exists(tmp_db) else DB_PATH
    return DB_PATH

def get_db():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force_reseed=False):
    db_path = get_db_path()
    if force_reseed and os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception as e:
            print("Error removing DB:", e)

    conn = get_db()
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')

    # Zones Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS zones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        area REAL NOT NULL,
        green_cover_percentage REAL NOT NULL,
        health_status TEXT NOT NULL,
        map_x INTEGER DEFAULT 0,
        map_y INTEGER DEFAULT 0,
        soil_type TEXT DEFAULT 'Loamy',
        ph_level REAL DEFAULT 6.5,
        sunlight_type TEXT DEFAULT 'Full Sun',
        water_source TEXT DEFAULT 'Drip Irrigation'
    )
    ''')

    # Plants Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS plants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plant_code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        species TEXT NOT NULL,
        type TEXT NOT NULL,
        planted_date TEXT NOT NULL,
        zone_id INTEGER NOT NULL,
        health_status TEXT NOT NULL,
        last_watered TEXT,
        next_watering TEXT,
        last_fertilized TEXT,
        photo TEXT,
        notes TEXT,
        FOREIGN KEY (zone_id) REFERENCES zones(id) ON DELETE CASCADE
    )
    ''')

    # Plant Catalog Table (Reference Replacement Candidates)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS plant_catalog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        species TEXT NOT NULL,
        type TEXT NOT NULL,
        ideal_soil TEXT NOT NULL,
        ph_min REAL NOT NULL,
        ph_max REAL NOT NULL,
        ideal_sunlight TEXT NOT NULL,
        moisture_min REAL NOT NULL,
        moisture_max REAL NOT NULL,
        temp_min REAL NOT NULL,
        temp_max REAL NOT NULL,
        water_req TEXT NOT NULL,
        maintenance_level TEXT NOT NULL,
        photo TEXT NOT NULL,
        why_explanation TEXT NOT NULL
    )
    ''')

    # Plant Replacements Audit Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS plant_replacements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        old_plant_name TEXT NOT NULL,
        old_plant_code TEXT NOT NULL,
        new_plant_name TEXT NOT NULL,
        new_plant_species TEXT NOT NULL,
        zone_id INTEGER NOT NULL,
        zone_name TEXT NOT NULL,
        compatibility_score INTEGER NOT NULL,
        date TEXT NOT NULL,
        replaced_by TEXT NOT NULL,
        FOREIGN KEY (zone_id) REFERENCES zones(id) ON DELETE CASCADE
    )
    ''')

    # MaintenanceTasks Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS maintenance_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plant_id INTEGER,
        zone_id INTEGER NOT NULL,
        task_type TEXT NOT NULL,
        assigned_to TEXT NOT NULL,
        scheduled_date TEXT NOT NULL,
        status TEXT NOT NULL,
        priority TEXT NOT NULL,
        completion_date TEXT,
        photo_proof TEXT,
        notes TEXT,
        created_by TEXT DEFAULT 'System',
        FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE SET NULL,
        FOREIGN KEY (zone_id) REFERENCES zones(id) ON DELETE CASCADE
    )
    ''')

    # SensorReadings Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        zone_id INTEGER NOT NULL,
        soil_moisture REAL NOT NULL,
        humidity REAL NOT NULL,
        temperature REAL NOT NULL,
        timestamp TEXT NOT NULL,
        status_alert TEXT NOT NULL,
        FOREIGN KEY (zone_id) REFERENCES zones(id) ON DELETE CASCADE
    )
    ''')

    # SustainabilityMetrics Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sustainability_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        green_cover REAL NOT NULL,
        carbon_offset_kg REAL NOT NULL,
        water_used_liters REAL NOT NULL,
        water_saved_liters REAL NOT NULL,
        trees_planted INTEGER NOT NULL,
        biodiversity_score INTEGER NOT NULL
    )
    ''')

    # VolunteerActivities Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS volunteer_activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        volunteer_id INTEGER,
        volunteer_name TEXT NOT NULL,
        date TEXT NOT NULL,
        points INTEGER NOT NULL,
        proof_photo TEXT,
        status TEXT NOT NULL,
        description TEXT NOT NULL,
        zone_id INTEGER,
        detected_plant TEXT,
        verified_by TEXT,
        verification_date TEXT,
        FOREIGN KEY (zone_id) REFERENCES zones(id) ON DELETE SET NULL
    )
    ''')

    try:
        cursor.execute("ALTER TABLE volunteer_activities ADD COLUMN detected_plant TEXT")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE volunteer_activities ADD COLUMN verified_by TEXT")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE volunteer_activities ADD COLUMN verification_date TEXT")
    except Exception:
        pass

    # BiodiversityLogs Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS biodiversity_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        species_name TEXT NOT NULL,
        category TEXT NOT NULL,
        count INTEGER NOT NULL,
        zone_id INTEGER NOT NULL,
        observation_date TEXT NOT NULL,
        photo TEXT,
        notes TEXT,
        FOREIGN KEY (zone_id) REFERENCES zones(id) ON DELETE CASCADE
    )
    ''')

    # Notifications Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT NOT NULL,
        type TEXT NOT NULL,
        read_status INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )
    ''')

    # SchedulerConfig Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scheduler_config (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_type TEXT UNIQUE NOT NULL,
        frequency_days INTEGER NOT NULL,
        last_run TEXT,
        auto_enabled INTEGER DEFAULT 1
    )
    ''')

    # Issues Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS issues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        reporter_name TEXT NOT NULL,
        zone_id INTEGER NOT NULL,
        plant_id INTEGER,
        issue_type TEXT NOT NULL,
        priority TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT DEFAULT 'Open',
        photo TEXT,
        reported_at TEXT NOT NULL,
        converted_task_id INTEGER,
        FOREIGN KEY (zone_id) REFERENCES zones(id) ON DELETE CASCADE,
        FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE SET NULL
    )
    ''')

    # Rewards Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rewards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        cost_points INTEGER NOT NULL,
        category TEXT NOT NULL,
        icon TEXT NOT NULL,
        stock INTEGER NOT NULL,
        description TEXT NOT NULL
    )
    ''')

    # User Redemptions Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_redemptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        volunteer_name TEXT NOT NULL,
        reward_id INTEGER NOT NULL,
        reward_title TEXT NOT NULL,
        cost_points INTEGER NOT NULL,
        date TEXT NOT NULL,
        claim_code TEXT NOT NULL,
        FOREIGN KEY (reward_id) REFERENCES rewards(id) ON DELETE CASCADE
    )
    ''')

    conn.commit()

    # Check if database is empty and seed data
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        seed_demo_data(conn)

    conn.close()

def seed_demo_data(conn):
    cursor = conn.cursor()
    now = datetime.now()

    # Seed Users
    users = [
        ('Admin Green Committee', 'admin@smartcampus.com', generate_password_hash('Admin@123'), 'Admin'),
        ('Gardening Staff Demo', 'staff@smartcampus.com', generate_password_hash('Staff@123'), 'Gardening Staff'),
        ('Student Volunteer Demo', 'student@smartcampus.com', generate_password_hash('Student@123'), 'Student Volunteer'),
        ('Dr. Eleanor Vance', 'admin@campus.edu', generate_password_hash('admin123'), 'Admin'),
        ('Rajesh Kumar', 'rajesh@campus.edu', generate_password_hash('staff123'), 'Gardening Staff'),
        ('Sarah Jenkins', 'sarah@campus.edu', generate_password_hash('staff123'), 'Gardening Staff'),
        ('Aarav Sharma', 'aarav@student.edu', generate_password_hash('student123'), 'Student Volunteer'),
        ('Priya Patel', 'priya@student.edu', generate_password_hash('student123'), 'Student Volunteer')
    ]
    cursor.executemany('INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)', users)

    # Seed Zones with Soil & Environmental Parameters
    zones = [
        (1, 'Main Garden & Amphitheater', 'Central Campus Quad', 4500.0, 88.5, 'Healthy', 25, 30, 'Loamy', 6.5, 'Partial Sun', 'Drip Irrigation'),
        (2, 'Academic Block Green Belt', 'North Wing', 3200.0, 74.0, 'Needs Attention', 60, 20, 'Clay Loam', 6.2, 'Full Sun', 'Manual Sprinkler'),
        (3, 'Central Library Plaza', 'East Wing', 2800.0, 82.0, 'Healthy', 75, 55, 'Sandy Loam', 7.0, 'Full Sun', 'Drip Irrigation'),
        (4, 'Hostel Complex Lawn', 'South Campus', 5100.0, 65.5, 'Critical', 35, 75, 'Clay', 5.8, 'Partial Sun', 'Manual Watering'),
        (5, 'Sports Ground & Tree Canopy', 'West Complex', 8500.0, 91.2, 'Healthy', 15, 65, 'Loamy', 6.8, 'Full Sun', 'Recycled Water Drip'),
        (6, 'Main Gate Entrance Avenue', 'Campus Entrance', 2100.0, 80.0, 'Healthy', 50, 45, 'Silty Loam', 6.6, 'Full Sun', 'Drip Irrigation')
    ]
    cursor.executemany('INSERT INTO zones (id, name, location, area, green_cover_percentage, health_status, map_x, map_y, soil_type, ph_level, sunlight_type, water_source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', zones)

    # Seed Plant Catalog (Replacement Candidates with Agronomic Requirements)
    catalog = [
        ('Hibiscus Rosa-Sinensis', 'Hibiscus rosa-sinensis', 'Flowering Shrub', 'Loamy / Well-drained', 6.0, 7.5, 'Full Sun / Partial Sun', 40.0, 75.0, 18.0, 36.0, 'Medium (2-3 times/week)', 'Low', 'https://images.unsplash.com/photo-1566835265538-4e56eb600867?w=600', 'Thrives in loamy soil (pH 6.0-7.5) with partial/full sun. Highly resilient to campus temperatures with high bloom yield.'),
        ('Jasmine Bush', 'Jasminum officinale', 'Climber / Shrub', 'Loamy / Sandy', 6.0, 7.2, 'Partial Sun', 45.0, 70.0, 15.0, 35.0, 'Medium', 'Medium', 'https://images.unsplash.com/photo-1508610048659-a06b669e3321?w=600', 'Extremely compatible with quad loamy soil (pH 6.5). Provides natural fragrance and low pest vulnerability.'),
        ('Red Rose Bush', 'Rosa rubiginosa', 'Flowering Shrub', 'Rich Loamy', 6.0, 6.8, 'Full Sun', 50.0, 75.0, 16.0, 32.0, 'High', 'Medium', 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600', 'Prefers sunny areas with pH 6.0-6.8. Excellent aesthetic enhancement for central quad borders.'),
        ('Neem Tree (Indian Lilac)', 'Azadirachta indica', 'Tree', 'Sandy / Loamy / All Soil', 5.5, 8.0, 'Full Sun', 25.0, 65.0, 15.0, 42.0, 'Low (Drought Tolerant)', 'Low', 'https://images.unsplash.com/photo-1600411833196-7c1f6b1a8b90?w=600', 'Outstanding hardiness. Thrives in wide pH range (5.5-8.0), acts as natural pest repellent and shade provider.'),
        ('Aloe Vera Medicinal Bed', 'Aloe barbadensis Miller', 'Medicinal Herb', 'Sandy / Well-drained', 6.0, 8.2, 'Full Sun / Partial Sun', 20.0, 50.0, 15.0, 40.0, 'Low', 'Low', 'https://images.unsplash.com/photo-1596547609652-9cf5d8d76921?w=600', 'Drought resilient succulent. Perfect match for library plaza sandy loam soil and sunny exposure.'),
        ('Mango Tree (Alphonso)', 'Mangifera indica', 'Fruit Tree', 'Deep Loamy', 5.5, 7.5, 'Full Sun', 35.0, 70.0, 20.0, 38.0, 'Medium', 'Medium', 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=600', 'Deep root canopy tree. Great for sports ground perimeter loamy soil with high carbon sequestration capability.'),
        ('Bougainvillea Hedge', 'Bougainvillea spectabilis', 'Flowering Shrub', 'Loamy / Well-drained', 5.5, 7.5, 'Full Sun', 30.0, 60.0, 20.0, 40.0, 'Low', 'Low', 'https://images.unsplash.com/photo-1596727147705-61a532a659bd?w=600', 'Vibrant flowering climber/hedge. Extremely low water requirement and highly tolerant to campus summer heat.'),
        ('Snake Plant Green Border', 'Sansevieria trifasciata', 'Indoor/Outdoor Shrub', 'Well-drained Loamy', 5.5, 7.5, 'Shade / Partial Sun', 25.0, 60.0, 15.0, 38.0, 'Low', 'Low', 'https://images.unsplash.com/photo-1599598425947-0206455429d5?w=600', 'Air-purifying foliage plant. Thrives in shaded corridor borders with low maintenance needs.'),
        ('Areca Palm Cluster', 'Dypsis lutescens', 'Palm Tree', 'Loamy / Moist Soil', 6.0, 7.0, 'Partial Sun', 45.0, 80.0, 18.0, 35.0, 'High', 'Medium', 'https://images.unsplash.com/photo-1598880940371-c756e015fea1?w=600', 'Lush tropical aesthetic palm cluster. Performs best with drip irrigation and partial sun exposure.'),
        ('Holy Basil (Tulsi Bed)', 'Ocimum sanctum', 'Medicinal Herb', 'Rich Loamy', 6.0, 7.5, 'Full Sun', 40.0, 70.0, 18.0, 38.0, 'Medium', 'Low', 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=600', 'Sacred Indian herb with high medicinal value. Highly compatible with quad loamy soil and daily sun.')
    ]
    cursor.executemany('''
    INSERT INTO plant_catalog 
    (name, species, type, ideal_soil, ph_min, ph_max, ideal_sunlight, moisture_min, moisture_max, temp_min, temp_max, water_req, maintenance_level, photo, why_explanation)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', catalog)

    # Seed Plants with 100% Verified Plant Photos (No Animals/WildLife)
    today_str = now.strftime("%Y-%m-%d")
    yesterday_str = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    two_days_ago = (now - timedelta(days=2)).strftime("%Y-%m-%d")
    three_days_ago = (now - timedelta(days=3)).strftime("%Y-%m-%d")
    next_water_str = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    overdue_water_str = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    last_fert_str = (now - timedelta(days=15)).strftime("%Y-%m-%d")

    plants = [
        ('P-101', 'Golden Tabebuia (Trumpet Tree)', 'Tabebuia chrysantha', 'Tree', '2023-03-15', 1, 'Healthy', today_str, next_water_str, last_fert_str, 'https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=600', 'Vibrant yellow blooms in spring. Provides shade for quad.'),
        ('P-102', 'Neem Tree (Indian Lilac)', 'Azadirachta indica', 'Tree', '2022-08-10', 1, 'Healthy', today_str, next_water_str, last_fert_str, 'https://images.unsplash.com/photo-1600411833196-7c1f6b1a8b90?w=600', 'Medicinal tree near amphitheater seating.'),
        ('P-103', 'Bougainvillea Hedge', 'Bougainvillea spectabilis', 'Shrub', '2023-01-20', 1, 'Healthy', yesterday_str, today_str, last_fert_str, 'https://images.unsplash.com/photo-1596727147705-61a532a659bd?w=600', 'Border hedge with pink and white bracts.'),
        ('P-104', 'Royal Palm Line A', 'Roystonea regia', 'Palm', '2021-11-05', 6, 'Healthy', today_str, next_water_str, last_fert_str, 'https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=600', 'Avenue tree lining main entrance drive.'),
        ('P-105', 'Jacaranda Tree', 'Jacaranda mimosifolia', 'Tree', '2022-04-18', 2, 'Needs Attention', two_days_ago, overdue_water_str, last_fert_str, 'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?w=600', 'Showing mild leaf wilting on lower branches.'),
        ('P-106', 'Korean Velvet Grass Lawn', 'Zoysia tenuifolia', 'Ground Cover', '2023-05-01', 3, 'Healthy', today_str, next_water_str, last_fert_str, 'https://images.unsplash.com/photo-1584467735871-8e85353a8413?w=600', 'Lush green lawn surrounding main library entrance.'),
        ('P-107', 'Gulmohar (Peacock Tree)', 'Delonix regia', 'Tree', '2021-06-25', 4, 'Critical', three_days_ago, overdue_water_str, last_fert_str, 'https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=600', 'Severe soil moisture deficit. Fungal leaf spots detected.'),
        ('P-108', 'Aloe Vera Medicinal Bed', 'Aloe barbadensis Miller', 'Medicinal Herb', '2023-09-12', 3, 'Healthy', yesterday_str, next_water_str, last_fert_str, 'https://images.unsplash.com/photo-1596547609652-9cf5d8d76921?w=600', 'Botanical research garden plot.'),
        ('P-109', 'Ashoka Tree Border', 'Polyalthia longifolia', 'Tree', '2022-01-15', 2, 'Healthy', today_str, next_water_str, last_fert_str, 'https://images.unsplash.com/photo-1448375240586-882707db888b?w=600', 'Tall acoustic barrier behind academic blocks.'),
        ('P-110', 'Frangipani (Plumeria)', 'Plumeria rubra', 'Flowering Tree', '2022-10-30', 3, 'Healthy', today_str, next_water_str, last_fert_str, 'https://images.unsplash.com/photo-1534067783941-51c9c23ecefd?w=600', 'Fragrant white-yellow blossoms outside library quiet reading zone.'),
        ('P-111', 'Banyan Tree (Heritage)', 'Ficus benghalensis', 'Tree', '2015-07-20', 5, 'Healthy', yesterday_str, next_water_str, last_fert_str, 'https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=600', '50-year-old campus landmark tree on sports ground perimeter.'),
        ('P-112', 'Snake Plant Green Border', 'Sansevieria trifasciata', 'Indoor/Outdoor Shrub', '2023-11-01', 2, 'Healthy', yesterday_str, next_water_str, last_fert_str, 'https://images.unsplash.com/photo-1599598425947-0206455429d5?w=600', 'Air-purifying border near academic block corridors.'),
        ('P-113', 'Hibiscus Rosa-Sinensis', 'Hibiscus rosa-sinensis', 'Flowering Shrub', '2023-04-14', 4, 'Needs Attention', two_days_ago, overdue_water_str, last_fert_str, 'https://images.unsplash.com/photo-1566835265538-4e56eb600867?w=600', 'Aphid infestation spotted on young flower buds.'),
        ('P-114', 'Holy Basil (Tulsi Bed)', 'Ocimum sanctum', 'Medicinal Herb', '2023-08-05', 1, 'Healthy', today_str, next_water_str, last_fert_str, 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=600', 'Campus herb garden section.'),
        ('P-115', 'Bamboo Canopy Line', 'Bambusa vulgaris', 'Bamboo', '2022-03-01', 5, 'Healthy', today_str, next_water_str, last_fert_str, 'https://images.unsplash.com/photo-1516205651411-aef33a44f7c2?w=600', 'Fast-growing green shield around basketball courts.'),
        ('P-116', 'Ficus Benjamina Topiary', 'Ficus benjamina', 'Shrub', '2023-02-18', 6, 'Healthy', today_str, next_water_str, last_fert_str, 'https://images.unsplash.com/photo-1512428559087-560fa5ceab42?w=600', 'Manicured ornamental topiary near gate.'),
        ('P-117', 'Areca Palm Cluster', 'Dypsis lutescens', 'Palm', '2023-06-10', 4, 'Needs Attention', two_days_ago, overdue_water_str, last_fert_str, 'https://images.unsplash.com/photo-1598880940371-c756e015fea1?w=600', 'Yellowing fronds due to low soil moisture.'),
        ('P-118', 'Jasmine Bush', 'Jasminum officinale', 'Climber', '2023-07-22', 1, 'Healthy', today_str, next_water_str, last_fert_str, 'https://images.unsplash.com/photo-1508610048659-a06b669e3321?w=600', 'Sweet scented climber on quad trellis.'),
        ('P-119', 'Copperpod Tree', 'Peltophorum pterocarpum', 'Tree', '2021-09-14', 5, 'Healthy', today_str, next_water_str, last_fert_str, 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600', 'Shade provider along stadium bleachers.'),
        ('P-120', 'Mint & Lemongrass Bed', 'Cymbopogon citratus', 'Medicinal Herb', '2023-10-04', 3, 'Healthy', today_str, next_water_str, last_fert_str, 'https://images.unsplash.com/photo-1603569283847-be29b8b3bf1d?w=600', 'Aromatic herb patch maintained by bio club.')
    ]
    cursor.executemany('''
    INSERT INTO plants 
    (plant_code, name, species, type, planted_date, zone_id, health_status, last_watered, next_watering, last_fertilized, photo, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', plants)

    # Seed Initial Plant Replacement History Audit Logs
    replacements = [
        ('Damaged Croton Shrub', 'P-099', 'Hibiscus Rosa-Sinensis', 'Hibiscus rosa-sinensis', 1, 'Main Garden & Amphitheater', 94, (now - timedelta(days=2)).strftime("%Y-%m-%d"), 'Rajesh Kumar'),
        ('Diseased Cypress Shrub', 'P-098', 'Jasmine Bush', 'Jasminum officinale', 1, 'Main Garden & Amphitheater', 91, (now - timedelta(days=5)).strftime("%Y-%m-%d"), 'Dr. Eleanor Vance')
    ]
    cursor.executemany('''
    INSERT INTO plant_replacements 
    (old_plant_name, old_plant_code, new_plant_name, new_plant_species, zone_id, zone_name, compatibility_score, date, replaced_by)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', replacements)

    # Seed Maintenance Tasks
    tasks = [
        (7, 4, 'Watering', 'Rajesh Kumar', today_str, 'Pending', 'Urgent', None, None, 'Hostel lawn Gulmohar tree critically dry.', 'System'),
        (5, 2, 'Watering', 'Sarah Jenkins', today_str, 'In Progress', 'High', None, None, 'Jacaranda tree watering & soil aeration.', 'Rajesh Kumar'),
        (13, 4, 'Pest Control', 'Rajesh Kumar', today_str, 'Pending', 'High', None, None, 'Apply organic neem spray for aphids on Hibiscus.', 'Dr. Eleanor Vance'),
        (1, 1, 'Watering', 'Sarah Jenkins', today_str, 'Completed', 'Medium', today_str, 'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=600', 'Drip irrigation completed for 35 mins.', 'System'),
        (6, 3, 'Pruning', 'Rajesh Kumar', yesterday_str, 'Completed', 'Low', yesterday_str, 'https://images.unsplash.com/photo-1592417817098-8f3d6ef23a81?w=600', 'Library lawn edge trimming & cleanup.', 'Sarah Jenkins'),
        (3, 1, 'Fertilizing', 'Sarah Jenkins', (now - timedelta(days=4)).strftime("%Y-%m-%d"), 'Completed', 'Medium', (now - timedelta(days=4)).strftime("%Y-%m-%d"), 'https://images.unsplash.com/photo-1611843467160-25afb8df1074?w=600', 'Organic compost applied to Bougainvillea.', 'Rajesh Kumar'),
        (17, 4, 'Watering', 'Rajesh Kumar', yesterday_str, 'Overdue', 'High', None, None, 'Areca palm cluster deep watering.', 'System'),
        (2, 1, 'General Maintenance', 'Sarah Jenkins', (now + timedelta(days=1)).strftime("%Y-%m-%d"), 'Pending', 'Low', None, None, 'Routine branch check and leaf clearing.', 'Dr. Eleanor Vance'),
        (11, 5, 'Pruning', 'Rajesh Kumar', (now + timedelta(days=2)).strftime("%Y-%m-%d"), 'Pending', 'Medium', None, None, 'Banyan tree lower branch trim for path clearance.', 'System'),
        (15, 5, 'Weeding', 'Sarah Jenkins', (now + timedelta(days=1)).strftime("%Y-%m-%d"), 'Pending', 'Low', None, None, 'Remove weeds along bamboo canopy root line.', 'System')
    ]
    cursor.executemany('''
    INSERT INTO maintenance_tasks 
    (plant_id, zone_id, task_type, assigned_to, scheduled_date, status, priority, completion_date, photo_proof, notes, created_by)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tasks)

    # Seed Sensor Readings
    sensor_data = [
        (1, 48.5, 62.0, 26.5, now.strftime("%Y-%m-%d %H:%M:%S"), 'Normal'),
        (2, 34.0, 58.5, 28.2, now.strftime("%Y-%m-%d %H:%M:%S"), 'Normal'),
        (3, 52.0, 65.0, 25.0, now.strftime("%Y-%m-%d %H:%M:%S"), 'Normal'),
        (4, 22.4, 45.0, 31.5, now.strftime("%Y-%m-%d %H:%M:%S"), 'Low Moisture - Watering Recommended'),
        (5, 55.8, 68.0, 24.8, now.strftime("%Y-%m-%d %H:%M:%S"), 'Normal'),
        (6, 42.0, 60.0, 27.0, now.strftime("%Y-%m-%d %H:%M:%S"), 'Normal')
    ]
    cursor.executemany('''
    INSERT INTO sensor_readings 
    (zone_id, soil_moisture, humidity, temperature, timestamp, status_alert)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', sensor_data)

    # Seed Sustainability Metrics
    sustainability_data = [
        ("2026-03-31", 76.5, 1420.0, 18500.0, 4200.0, 110, 78),
        ("2026-04-30", 78.2, 1510.0, 19200.0, 4800.0, 118, 81),
        ("2026-05-31", 79.5, 1600.0, 21000.0, 5400.0, 125, 84),
        ("2026-06-30", 81.0, 1720.0, 17500.0, 6100.0, 134, 88),
        ("2026-07-31", 82.4, 1850.0, 16800.0, 6900.0, 142, 92),
        (today_str, 84.1, 1980.5, 15400.0, 7450.0, 150, 96)
    ]
    cursor.executemany('''
    INSERT INTO sustainability_metrics 
    (date, green_cover, carbon_offset_kg, water_used_liters, water_saved_liters, trees_planted, biodiversity_score)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', sustainability_data)

    # Seed Volunteer Activities
    volunteers = [
        ('Campus Tree Plantation Drive', 4, 'Aarav Sharma', yesterday_str, 120, 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=600', 'Approved', 'Planted 15 native tree saplings along hostel green corridor.', 4, 'Neem Tree (Azadirachta indica)', 'Dr. Eleanor Vance', yesterday_str),
        ('Medicinal Herb Bed Weeding & Tagging', 5, 'Priya Patel', (now - timedelta(days=3)).strftime("%Y-%m-%d"), 80, 'https://images.unsplash.com/photo-1591857177580-dc82b9ac4e1e?w=600', 'Approved', 'Cleaned and labeled 20 medicinal plant species.', 3, 'Aloe Vera & Tulsi Bed', 'Dr. Eleanor Vance', (now - timedelta(days=3)).strftime("%Y-%m-%d")),
        ('Drip Irrigation Line Inspection', 4, 'Aarav Sharma', (now - timedelta(days=5)).strftime("%Y-%m-%d"), 100, 'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=600', 'Approved', 'Checked 40 drip nozzles for clogging in Main Quad.', 1, 'Rose & Cypress Hedge', 'Rajesh Kumar', (now - timedelta(days=5)).strftime("%Y-%m-%d")),
        ('Bird House Installation & Census', 5, 'Priya Patel', today_str, 0, 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600', 'Pending Verification', 'Installed 5 wooden bird nesting boxes in sports ground canopy.', 5, 'Royal Palm Canopy Flora', None, None)
    ]
    cursor.executemany('''
    INSERT INTO volunteer_activities 
    (title, volunteer_id, volunteer_name, date, points, proof_photo, status, description, zone_id, detected_plant, verified_by, verification_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', volunteers)

    # Seed Biodiversity Logs
    biodiversity = [
        ('Golden Tabebuia', 'Tree', 24, 1, today_str, 'https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=600', 'Flowering peak season.'),
        ('Asian Koel (Eudynamys scolopaceus)', 'Bird', 8, 5, today_str, 'https://images.unsplash.com/photo-1444464666168-49d633b86797?w=600', 'Sighted nesting in banyan canopy.'),
        ('Purple Sunbird (Cinnyris asiaticus)', 'Bird', 14, 1, yesterday_str, 'https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=600', 'Pollinating bougainvillea blossoms.'),
        ('Peacock Butterfly', 'Insect', 35, 3, today_str, 'https://images.unsplash.com/photo-1535083783855-76ae62b2914e?w=600', 'High activity around nectar flowering shrubs.'),
        ('Tulsi & Aloe Vera', 'Medicinal Plant', 45, 3, (now - timedelta(days=2)).strftime("%Y-%m-%d"), 'https://images.unsplash.com/photo-1596547609652-9cf5d8d76921?w=600', 'Cultivated for research and campus herbal tea dispensary.')
    ]
    cursor.executemany('''
    INSERT INTO biodiversity_logs 
    (species_name, category, count, zone_id, observation_date, photo, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', biodiversity)

    # Seed Notifications
    notifications = [
        (1, 'Hostel Area soil moisture dropped to 22.4% - Auto Irrigation Recommended!', 'Critical', 0, now.strftime("%Y-%m-%d %H:%M:%S")),
        (1, 'Plant P-107 (Gulmohar Tree) marked as Critical Health Status.', 'Warning', 0, (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")),
        (2, 'Task #7 (Watering Hostel Lawn) is Overdue!', 'Warning', 0, (now - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")),
        (4, 'Volunteer Activity "Bird House Installation" submitted for Admin review.', 'Info', 0, (now - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
    ]
    cursor.executemany('''
    INSERT INTO notifications 
    (user_id, message, type, read_status, created_at)
    VALUES (?, ?, ?, ?, ?)
    ''', notifications)

    # Seed Scheduler Config
    scheduler_configs = [
        ('Watering', 1, today_str, 1),
        ('Inspection', 7, today_str, 1),
        ('Pruning', 30, (now - timedelta(days=10)).strftime("%Y-%m-%d"), 1),
        ('Fertilizing', 15, (now - timedelta(days=5)).strftime("%Y-%m-%d"), 1)
    ]
    cursor.executemany('''
    INSERT INTO scheduler_config 
    (task_type, frequency_days, last_run, auto_enabled)
    VALUES (?, ?, ?, ?)
    ''', scheduler_configs)

    # Seed Issues
    issues = [
        ('Leaking Drip Irrigation Valve near Quad', 'Aarav Sharma', 1, 3, 'Water Leakage', 'High', 'Drip pipe joint cracked near bougainvillea bed.', 'Open', 'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=600', today_str, None),
        ('Broken Branch Hazard on Gulmohar Tree', 'Priya Patel', 4, 7, 'Branch Damage', 'Urgent', 'Storm damaged lower limb overhangs walkway.', 'Open', 'https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=600', yesterday_str, None)
    ]
    cursor.executemany('''
    INSERT INTO issues (title, reporter_name, zone_id, plant_id, issue_type, priority, description, status, photo, reported_at, converted_task_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', issues)

    # Seed Rewards
    rewards = [
        ('Eco-Friendly Organic Cotton Tote Bag', 100, 'Merchandise', 'fa-bag-shopping', 50, 'Sustainable campus tote with BioCampus logo.'),
        ('Potted Neem Sapling for Hostel Room', 150, 'Plant Sapling', 'fa-seedling', 30, 'Native medicinal sapling ready for pot planting.'),
        ('BioCampus Official Certificate of Merit', 200, 'Certificate', 'fa-certificate', 100, 'Verified green contribution certificate signed by Green Committee.'),
        ('Campus Green Hero Gold Medal & Plaque', 500, 'Award', 'fa-medal', 10, 'Prestigious annual campus sustainability honor.')
    ]
    cursor.executemany('''
    INSERT INTO rewards (title, cost_points, category, icon, stock, description)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', rewards)

    conn.commit()

if __name__ == '__main__':
    init_db(force_reseed=True)
    print("Database initialized & enhanced demo data seeded successfully!")
