/* ==========================================================================
   SMART CAMPUS GARDENING & GREEN SPACE MANAGEMENT SYSTEM
   Core JavaScript Engine (App State, Auth, Roles, API Integrations, Chatbot, QR, Multilingual)
   ========================================================================== */

const API_BASE = '/api';

// Multilingual Dictionary (EN, TA, ES, FR, HI, DE)
const i18n = {
  en: {
    brand_subtitle: "Smart Gardening",
    nav_dashboard: "Dashboard",
    nav_zones: "Zone Management",
    nav_plants: "Plant Inventory",
    nav_maintenance: "Maintenance Tasks",
    nav_calendar: "Checklist Calendar",
    nav_health: "Plant Health & AI Scan",
    nav_irrigation: "Smart Irrigation & IoT",
    nav_issues: "Reported Issues",
    nav_sustainability: "Sustainability",
    nav_biodiversity: "Biodiversity Tracker",
    nav_volunteers: "Student Hub & Rewards",
    nav_notifications: "Notifications",
    nav_settings: "Settings & API",
    lbl_role: "Role:",
    btn_report_issue: "Report Issue",
    btn_gardening_guide: "Gardening Guide",

    // Dashboard KPIs
    kpi_total_plants: "Total Plants & Trees",
    kpi_healthy_flora: "Healthy Flora",
    kpi_attention_needed: "Attention / Critical",
    kpi_green_cover: "Green Cover %",
    kpi_completed_tasks: "Completed Tasks",
    kpi_carbon_offset: "Carbon Offset",
    kpi_open_issues: "Open Issues",

    // Chatbot Pills
    pill_moisture: "💧 Soil Moisture",
    pill_stats: "🌱 Plant Stats",
    pill_rewards: "🏆 Rewards Info",

    // Smart Plant Replacement
    smart_plant_replacement: "Smart Plant Replacement Recommendation",
    recommended_plants: "Top Recommended Replacement Plants",
    compatibility_score: "Compatibility Score",
    soil_type: "Soil Type",
    soil_ph: "Soil pH",
    soil_moisture: "Soil Moisture",
    sunlight: "Sunlight",
    water_requirement: "Water Requirement",
    maintenance_level: "Maintenance Level",
    why_this_plant: "Why This Plant?",
    replacement_history: "Replacement History",
    old_plant: "Old Plant",
    new_plant: "New Plant",
    location: "Location",
    match_score: "Match Score",

    // Anti-Cheating Reward Verification
    pending_verification: "Pending Verification",
    btn_approve: "Approve & Award Points",
    btn_reject: "Reject (0 Points)",
    ai_detected_plant: "AI Detected Plant",
    verification_status: "Verification Status",
    pending_queue_title: "Pending Reward Verification Queue",
    pending_queue_desc: "Mandatory Staff/Admin anti-cheating review before reward points are credited.",
    student_id: "Student ID",

    // Guide Modal
    guide_title: "Campus Gardening & Organic Care Handbook",
    guide_sec1_title: "🌳 1. Campus Tree & Shrub Watering Guidelines",
    guide_sec1_desc: "Drip irrigation should be activated early morning (6:00 - 8:00 AM) to minimize evaporation. Maintain soil moisture levels between 40% and 65% for optimal root aeration.",
    guide_sec2_title: "✂️ 2. Pruning & Canopy Management",
    guide_sec2_desc: "Prune dead or diseased branches quarterly. Cut at a 45-degree angle 1/4 inch above healthy buds to encourage outward foliage growth.",
    guide_sec3_title: "🌿 3. Organic Pest Control (Neem Spray Recipe)",
    guide_sec3_desc: "Mix 5 ml of cold-pressed organic Neem oil and 2 ml of eco liquid soap in 1 Liter of warm water. Spray thoroughly on infected leaves to eliminate aphids and spider mites."
  },
  ta: {
    brand_subtitle: "ஸ்மார்ட் பூங்கா நிர்வாகம்",

    // Anti-Cheating Reward Verification
    pending_verification: "சரிபார்ப்பு நிலுவையில்",
    btn_approve: "ஒப்புதல் அளி & புள்ளிகள் வழங்கு",
    btn_reject: "நிராகரி (0 புள்ளிகள்)",
    ai_detected_plant: "AI கண்டறிந்த தாவரம்",
    verification_status: "சரிபார்ப்பு நிலை",
    pending_queue_title: "நிலுவையில் உள்ள பரிசு சரிபார்ப்பு வரிசை",
    pending_queue_desc: "புள்ளிகள் வழங்குவதற்கு முன் ஊழியர்/நிர்வாகி கட்டாய சரிபார்ப்பு.",
    student_id: "மாணவர் ID",
    nav_dashboard: "முதன்மை பலகை",
    nav_zones: "மண்டல நிர்வாகம்",
    nav_plants: "தாவரங்கள் பட்டியல்",
    nav_maintenance: "பராமரிப்பு பணிகள்",
    nav_calendar: "பணி அட்டவணை",
    nav_health: "தாவர ஆரோக்கியம் & AI சோதனை",
    nav_irrigation: "ஸ்மார்ட் பாசனம் & IoT",
    nav_issues: "பதிவுசெய்த புகார்கள்",
    nav_sustainability: "சுற்றுச்சூழல் நிலைத்தன்மை",
    nav_biodiversity: "பல்லுயிர் கண்காணிப்பு",
    nav_volunteers: "மாணவர் மையம் & பரிசுகள்",
    nav_notifications: "அறிவிப்புகள்",
    nav_settings: "அமைப்புகள் & API",
    lbl_role: "பங்கு:",
    btn_report_issue: "புகார் அளிக்கவும்",
    btn_gardening_guide: "தோட்டக்கலை வழிகாட்டி",

    // Dashboard KPIs
    kpi_total_plants: "மொத்த தாவரங்கள் & மரங்கள்",
    kpi_healthy_flora: "ஆரோக்கியமான தாவரங்கள்",
    kpi_attention_needed: "கவனம் / ஆபத்தான நிலை",
    kpi_green_cover: "பசுமை பரப்பு சதவீதம்",
    kpi_completed_tasks: "முடிக்கப்பட்ட பணிகள்",
    kpi_carbon_offset: "கார்பன் ஈடுசெய்யும் அளவு",
    kpi_open_issues: "நிலுவையில் உள்ள புகார்கள்",

    // Chatbot Pills
    pill_moisture: "💧 மண் ஈரப்பதம்",
    pill_stats: "🌱 தாவர விபரம்",
    pill_rewards: "🏆 புள்ளிகள் விபரம்",

    // Smart Plant Replacement
    smart_plant_replacement: "ஸ்மார்ட் தாவர மாற்று பரிந்துரை",
    recommended_plants: "பரிந்துரைக்கப்பட்ட தாவரங்கள்",
    compatibility_score: "பொருத்தமான மதிப்பெண்",
    soil_type: "மண் வகை",
    soil_ph: "மண் pH",
    soil_moisture: "மண் ஈரப்பதம்",
    sunlight: "சூரிய ஒளி",
    water_requirement: "நீர் தேவை",
    maintenance_level: "பராமரிப்பு நிலை",
    why_this_plant: "ஏன் இந்த தாவரம்?",
    replacement_history: "மாற்று வரலாறு",
    old_plant: "பழைய தாவரம்",
    new_plant: "புதிய தாவரம்",
    location: "இடம்",
    match_score: "பொருத்தமான மதிப்பெண்",

    // Guide Modal
    guide_title: "வளாக தோட்டக்கலை & இயற்கை பராமரிப்பு கையேடு",
    guide_sec1_title: "🌳 1. மரங்கள் மற்றும் புதர்களுக்கான நீர் பாசன வழிகாட்டுதல்",
    guide_sec1_desc: "காலை நேரத்தில் (6:00 - 8:00 AM) சொட்டுநீர் பாசனத்தை இயக்குவது நீராவியாவதை தடுக்கும். மண் ஈரப்பதத்தை 40% முதல் 65% வரை பராமரிக்கவும்.",
    guide_sec2_title: "✂️ 2. கிளை நறுக்குதல் நிர்வாகம்",
    guide_sec2_desc: "பாதிக்கப்பட்ட கிளைகளை காலாண்டுக்கு ஒருமுறை 45 டிகிரி கோணத்தில் வெட்டவும்.",
    guide_sec3_title: "🌿 3. இயற்கை பூச்சிக்கட்டுப்பாடு (வேப்ப எண்ணெய் கரைசல்)",
    guide_sec3_desc: "1 லிட்டர் வெதுவெதுப்பான நீரில் 5 மி.லி வேப்ப எண்ணெய் மற்றும் 2 மி.லி சோப்பு கரைசல் கலந்து தெளிக்கவும்."
  },
  es: {
    brand_subtitle: "Jardinería Inteligente",
    nav_dashboard: "Panel Principal",
    nav_zones: "Gestión de Zonas",
    nav_plants: "Inventario de Plantas",
    nav_maintenance: "Tareas de Mantenimiento",
    nav_calendar: "Calendario de Tareas",
    nav_health: "Salud e Inteligencia Artificial",
    nav_irrigation: "Riego Inteligente e IoT",
    nav_issues: "Problemas Reportados",
    nav_sustainability: "Sostenibilidad",
    nav_biodiversity: "Seguimiento de Biodiversidad",
    nav_volunteers: "Hub de Estudiantes y Premios",
    nav_notifications: "Notificaciones",
    nav_settings: "Configuración y API",
    lbl_role: "Rol:",
    btn_report_issue: "Reportar Problema",
    btn_gardening_guide: "Guía Jardinería",

    kpi_total_plants: "Plantas y Árboles Totales",
    kpi_healthy_flora: "Flora Saludable",
    kpi_attention_needed: "Atención / Crítico",
    kpi_green_cover: "% Cobertura Verde",
    kpi_completed_tasks: "Tareas Completadas",
    kpi_carbon_offset: "Compensación de Carbono",
    kpi_open_issues: "Problemas Abiertos",

    pill_moisture: "💧 Humedad del Suelo",
    pill_stats: "🌱 Estadísticas",
    pill_rewards: "🏆 Recompensas",

    guide_title: "Manual de Jardinería y Cuidado Orgánico",
    guide_sec1_title: "🌳 1. Pautas de Riego de Árboles y Arbustos",
    guide_sec1_desc: "Active el riego por goteo temprano por la mañana (6:00 - 8:00 AM). Mantenga la humedad del suelo entre el 40% y el 65%.",
    guide_sec2_title: "✂️ 2. Podas y Manejo de Dosel",
    guide_sec2_desc: "Pode ramas secas o enfermas trimestralmente en un ángulo de 45 grados.",
    guide_sec3_title: "🌿 3. Control Orgánico de Plagas (Aceite de Neem)",
    guide_sec3_desc: "Mezcle 5 ml de aceite de neem y 2 ml de jabón en 1 litro de agua tibia."
  },
  fr: {
    brand_subtitle: "Jardinage Intelligent",
    nav_dashboard: "Tableau de Bord",
    nav_zones: "Gestion des Zones",
    nav_plants: "Inventaire des Plantes",
    nav_maintenance: "Tâches d'Entretien",
    nav_calendar: "Calendrier des Tâches",
    nav_health: "Santé et Détection IA",
    nav_irrigation: "Irrigation Intelligente & IoT",
    nav_issues: "Signalements",
    nav_sustainability: "Durabilité",
    nav_biodiversity: "Suivi de la Biodiversité",
    nav_volunteers: "Espace Étudiants & Récompenses",
    nav_notifications: "Notifications",
    nav_settings: "Paramètres & API",
    lbl_role: "Rôle:",
    btn_report_issue: "Signaler un Problème",
    btn_gardening_guide: "Guide Jardinage",

    kpi_total_plants: "Plantes & Arbres Totaux",
    kpi_healthy_flora: "Flore en Bonne Santé",
    kpi_attention_needed: "Attention / Critique",
    kpi_green_cover: "% Couverture Verte",
    kpi_completed_tasks: "Tâches Terminées",
    kpi_carbon_offset: "Compensation Carbone",
    kpi_open_issues: "Signalements Ouverts",

    pill_moisture: "💧 Humidité du Sol",
    pill_stats: "🌱 Stats Plantes",
    pill_rewards: "🏆 Récompenses",

    guide_title: "Manuel de Jardinage et Soins Biologiques",
    guide_sec1_title: "🌳 1. Directives d'Arrosage des Arbres et Arbustes",
    guide_sec1_desc: "Activer l'irrigation au goutte-à-goutte tôt le matin (6h00 - 8h00). Maintenir l'humidité entre 40% et 65%.",
    guide_sec2_title: "✂️ 2. Taille et Gestion du Feuillage",
    guide_sec2_desc: "Tailler les branches mortes ou malades chaque trimestre à 45 degrés.",
    guide_sec3_title: "🌿 3. Lutte Biologique (Huile de Neem)",
    guide_sec3_desc: "Mélanger 5 ml d'huile de Neem et 2 ml de savon liquide dans 1 litre d'eau tiède."
  },
  hi: {
    brand_subtitle: "स्मार्ट गार्डनिंग",
    nav_dashboard: "डैशबोर्ड",
    nav_zones: "ज़ोन प्रबंधन",
    nav_plants: "पौधों की सूची",
    nav_maintenance: "रखरखाव कार्य",
    nav_calendar: "कार्य कैलेंडर",
    nav_health: "पौधों का स्वास्थ्य और AI जांच",
    nav_irrigation: "स्मार्ट सिंचाई और IoT",
    nav_issues: "दर्ज समस्याएं",
    nav_sustainability: "सतत विकास",
    nav_biodiversity: "जैव विविधता ट्रैकर",
    nav_volunteers: "छात्र हब और पुरस्कार",
    nav_notifications: "सूचनाएं",
    nav_settings: "सेटिंग्स और API",
    lbl_role: "भूमिका:",
    btn_report_issue: "समस्या दर्ज करें",
    btn_gardening_guide: "बागवानी मार्गदर्शिका",

    kpi_total_plants: "कुल पौधे और पेड़",
    kpi_healthy_flora: "स्वास्थ्य पौधे",
    kpi_attention_needed: "ध्यान / गंभीर स्थिति",
    kpi_green_cover: "हरियाली प्रतिशत",
    kpi_completed_tasks: "पूरे किए गए कार्य",
    kpi_carbon_offset: "कार्बन सिंक प्रभाव",
    kpi_open_issues: "दर्ज समस्याएं",

    pill_moisture: "💧 मिट्टी की नमी",
    pill_stats: "🌱 पौधे के आंकड़े",
    pill_rewards: "🏆 पुरस्कार विवरण",

    guide_title: "कैंपस बागवानी और जैविक देखभाल गाइड",
    guide_sec1_title: "🌳 1. पौधों और झाड़ियों की सिंचाई गाइडलाइंस",
    guide_sec1_desc: "सुबह 6:00 से 8:00 बजे के बीच ड्रिप सिंचाई चालू करें। मिट्टी में 40% से 65% नमी बनाए रखें।",
    guide_sec2_title: "✂️ 2. कटाई-छंटाई प्रबंधन",
    guide_sec2_desc: "सूखी या क्षतिग्रस्त शाखाओं को हर तीन महीने में 45 डिग्री के कोण पर काटें।",
    guide_sec3_title: "🌿 3. जैविक कीट नियंत्रण (नीम का तेल)",
    guide_sec3_desc: "1 लीटर गुनगुने पानी में 5 मिली नीम तेल और 2 मिली साबुन घोल मिलाकर छिड़कें।"
  },
  de: {
    brand_subtitle: "Intelligente Gartenarbeit",
    nav_dashboard: "Dashboard",
    nav_zones: "Zonenverwaltung",
    nav_plants: "Pflanzenbestand",
    nav_maintenance: "Wartungsaufgaben",
    nav_calendar: "Aufgabenkalender",
    nav_health: "Pflanzengesundheit & KI-Scan",
    nav_irrigation: "Intelligente Bewässerung & IoT",
    nav_issues: "Gemeldete Probleme",
    nav_sustainability: "Nachhaltigkeit",
    nav_biodiversity: "Biodiversitäts-Tracker",
    nav_volunteers: "Studenten-Hub & Belohnungen",
    nav_notifications: "Benachrichtigungen",
    nav_settings: "Einstellungen & API",
    lbl_role: "Rolle:",
    btn_report_issue: "Problem Melden",
    btn_gardening_guide: "Gartenhandbuch",

    kpi_total_plants: "Gesamte Pflanzen & Bäume",
    kpi_healthy_flora: "Gesunde Flora",
    kpi_attention_needed: "Achtung / Kritisch",
    kpi_green_cover: "Grünflächenanteil %",
    kpi_completed_tasks: "Erledigte Aufgaben",
    kpi_carbon_offset: "CO2-Kompensation",
    kpi_open_issues: "Offene Probleme",

    pill_moisture: "💧 Bodenfeuchtigkeit",
    pill_stats: "🌱 Pflanzenstatistik",
    pill_rewards: "🏆 Belohnungen",

    guide_title: "Campus Gartenbau & Organisches Pflegehandbuch",
    guide_sec1_title: "🌳 1. Bewässerungsrichtlinien für Bäume",
    guide_sec1_desc: "Tropfbewässerung früh morgens aktivieren. Bodenfeuchtigkeit zwischen 40% und 65% halten.",
    guide_sec2_title: "✂️ 2. Rückschnitt & Kronenpflege",
    guide_sec2_desc: "Trockene Äste vierteljährlich im 45-Grad-Winkel schneiden.",
    guide_sec3_title: "🌿 3. Biologische Schädlingsbekämpfung",
    guide_sec3_desc: "5ml Neemöl und 2ml Seife in 1 Liter warmem Wasser mischen."
  }
};

// Application State
const state = {
  currentUser: null,
  selectedRoleTab: 'Student',
  currentRole: 'Admin',
  currentView: 'dashboard',
  currentLang: 'en',
  theme: 'light',
  zones: [],
  plants: [],
  tasks: [],
  unreadNotifs: 0,
  charts: {}
};
window.state = state;

// ==========================================
// INITIALIZATION & EVENT LISTENERS
// ==========================================

async function initApp() {
  setupNavigation();
  setupRoleSwitcher();
  setupLangSwitcher();
  setupThemeToggle();
  setupFormSubmissions();

  await checkAuthSession();

  const currentHash = window.location.hash.replace('#', '') || 'dashboard';
  switchView(currentHash);

  fetchNotifications();
  setInterval(fetchNotifications, 20000);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}

// ==========================================
// ROLE-BASED AUTHENTICATION & LOGIN ENGINE
// ==========================================

async function checkAuthSession() {
  try {
    const res = await fetch(`${API_BASE}/auth/me`);
    const data = await res.json();
    if (data.authenticated && data.user) {
      state.currentUser = data.user;
      state.currentRole = data.user.role;
      hideLoginOverlay();
      applyRolePermissions(state.currentRole);
      return true;
    } else {
      showLoginOverlay();
      return false;
    }
  } catch (e) {
    showLoginOverlay();
    return false;
  }
}

function showLoginOverlay() {
  const overlay = document.getElementById('login-screen-overlay');
  if (overlay) overlay.classList.remove('hidden');
}

function hideLoginOverlay() {
  const overlay = document.getElementById('login-screen-overlay');
  if (overlay) overlay.classList.add('hidden');
}

function selectLoginRole(role) {
  state.selectedRoleTab = role;

  const buttons = document.querySelectorAll('#role-tabs-wrapper .role-tab-btn');
  buttons.forEach(btn => {
    if (btn.getAttribute('data-role') === role) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });

  const badge = document.getElementById('active-role-badge');
  const emailInput = document.getElementById('login-email');

  if (role === 'Student') {
    if (badge) {
      badge.className = 'badge badge-healthy';
      badge.innerHTML = '🎓 Student Portal Login';
    }
    if (emailInput) emailInput.placeholder = 'student@smartcampus.com';
  } else if (role === 'Staff') {
    if (badge) {
      badge.className = 'badge badge-attention';
      badge.innerHTML = '🧹 Staff / Gardener Portal Login';
    }
    if (emailInput) emailInput.placeholder = 'staff@smartcampus.com';
  } else if (role === 'Admin') {
    if (badge) {
      badge.className = 'badge badge-critical';
      badge.innerHTML = '🛡️ Admin Portal Login';
    }
    if (emailInput) emailInput.placeholder = 'admin@smartcampus.com';
  }

  hideLoginError();
}

function fillDemoCredentials(email, password, role) {
  selectLoginRole(role);
  document.getElementById('login-email').value = email;
  document.getElementById('login-password').value = password;
  const form = document.getElementById('login-form');
  if (form) form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
}

function togglePasswordVisibility() {
  const input = document.getElementById('login-password');
  const btn = document.getElementById('btn-toggle-pw');
  if (!input || !btn) return;
  if (input.type === 'password') {
    input.type = 'text';
    btn.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
  } else {
    input.type = 'password';
    btn.innerHTML = '<i class="fa-solid fa-eye"></i>';
  }
}

function showLoginError(msg) {
  const alert = document.getElementById('login-error-alert');
  const text = document.getElementById('login-error-text');
  if (alert && text) {
    text.textContent = msg || 'Invalid credentials or unauthorized role access.';
    alert.style.display = 'flex';
  }
}

function hideLoginError() {
  const alert = document.getElementById('login-error-alert');
  if (alert) alert.style.display = 'none';
}

async function handleLoginSubmit(e) {
  if (e) e.preventDefault();
  hideLoginError();

  const email = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-password').value.trim();
  const role = state.selectedRoleTab;

  const btn = document.getElementById('btn-login-submit');
  const originalHTML = btn ? btn.innerHTML : '';
  if (btn) btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Authenticating...';

  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, role })
    });
    const data = await res.json();

    if (btn) btn.innerHTML = originalHTML;

    if (data.success && data.user) {
      state.currentUser = data.user;
      state.currentRole = data.user.role;
      hideLoginOverlay();
      showToast(`Welcome back, ${data.user.name}!`, 'success');
      applyRolePermissions(state.currentRole);

      // Role Default View Redirect
      if (state.currentRole === 'Student Volunteer' || role === 'Student') {
        switchView('volunteers');
      } else if (state.currentRole === 'Gardening Staff' || role === 'Staff') {
        switchView('maintenance');
      } else {
        switchView('dashboard');
      }
    } else {
      showLoginError(data.message || 'Invalid email or password.');
    }
  } catch (err) {
    if (btn) btn.innerHTML = originalHTML;
    showLoginError('Network or server connection error.');
  }
}

async function handleLogout() {
  try {
    await fetch(`${API_BASE}/auth/logout`, { method: 'POST' });
  } catch (e) {}

  state.currentUser = null;
  showToast('Logged out successfully', 'info');
  showLoginOverlay();
}

function openForgotPasswordModal() {
  openModal('forgot-password-modal');
}

function handleForgotPasswordSubmit(e) {
  e.preventDefault();
  const email = document.getElementById('forgot-email-input').value;
  closeModal('forgot-password-modal');
  alert(`✅ Password reset authorization code has been dispatched to ${email}! Please check your campus email inbox.`);
}

// ==========================================
// ROLE PERMISSIONS & SIDEBAR MENU FILTERING
// ==========================================

function applyRolePermissions(role) {
  state.currentRole = role;

  const allowedViews = {
    'Student': ['dashboard', 'plants', 'issues', 'volunteers', 'calendar', 'health'],
    'Student Volunteer': ['dashboard', 'plants', 'issues', 'volunteers', 'calendar', 'health'],
    'Staff': ['dashboard', 'maintenance', 'calendar', 'health', 'irrigation', 'issues', 'plants', 'volunteers'],
    'Gardening Staff': ['dashboard', 'maintenance', 'calendar', 'health', 'irrigation', 'issues', 'plants', 'volunteers'],
    'Admin': ['dashboard', 'zones', 'plants', 'maintenance', 'calendar', 'health', 'irrigation', 'issues', 'sustainability', 'biodiversity', 'volunteers', 'users', 'notifications', 'settings']
  };

  const currentAllowed = allowedViews[role] || allowedViews['Admin'];

  document.querySelectorAll('#main-nav .nav-item').forEach(item => {
    const view = item.getAttribute('data-view');
    if (currentAllowed.includes(view)) {
      item.style.display = 'block';
    } else {
      item.style.display = 'none';
    }
  });

  const volNavItem = document.querySelector('#nav-volunteers span');
  if (volNavItem) {
    const isTa = state.currentLang === 'ta';
    if (role === 'Student' || role === 'Student Volunteer') {
      volNavItem.textContent = isTa ? 'மாணவர் மையம் & பரிசுகள்' : 'Student Hub & Rewards';
    } else {
      volNavItem.textContent = isTa ? 'பரிசு சரிபார்ப்பு' : 'Reward Verification';
    }
  }

  const roleSelect = document.getElementById('role-select');
  if (roleSelect) {
    const isStudent = role === 'Student Volunteer' || role === 'Student';
    const isStaff = role === 'Gardening Staff' || role === 'Staff';
    if (role === 'Admin') roleSelect.value = 'Admin';
    else if (isStaff) roleSelect.value = 'Gardening Staff';
    else if (isStudent) roleSelect.value = 'Student Volunteer';
  }

  updateUserBadge();
}

function updateUserBadge() {
  if (state.currentUser) {
    document.getElementById('user-display-name').textContent = state.currentUser.name;
    document.getElementById('user-display-role').textContent = state.currentUser.role;
    document.getElementById('user-avatar').textContent = (state.currentUser.name || 'U')[0].toUpperCase();
    return;
  }
  const nameMap = {
    'Admin': 'Dr. Eleanor Vance',
    'Gardening Staff': 'Rajesh Kumar',
    'Student Volunteer': 'Aarav Sharma'
  };
  document.getElementById('user-display-name').textContent = nameMap[state.currentRole] || 'User';
  document.getElementById('user-display-role').textContent = state.currentRole;
  document.getElementById('user-avatar').textContent = (nameMap[state.currentRole] || 'U')[0];
}

function setupNavigation() {
  const navItems = document.querySelectorAll('#main-nav .nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      const view = item.getAttribute('data-view');
      switchView(view);
    });
  });

  const notifBtn = document.getElementById('nav-notif-btn');
  if (notifBtn) {
    notifBtn.addEventListener('click', () => {
      switchView('notifications');
    });
  }
}

function setupRoleSwitcher() {
  const roleSelect = document.getElementById('role-select');
  if (!roleSelect) return;
  roleSelect.addEventListener('change', (e) => {
    state.currentRole = e.target.value;
    updateUserBadge();
    applyRolePermissions(state.currentRole);
    showToast(`Switched user role view to ${state.currentRole}`, 'info');
    switchView(state.currentView);
  });
  updateUserBadge();
}

function setupLangSwitcher() {
  const langSelect = document.getElementById('lang-select');
  if (!langSelect) return;
  langSelect.addEventListener('change', (e) => {
    state.currentLang = e.target.value;
    applyLanguageTranslations();
    showToast(`Language switched to ${langSelect.options[langSelect.selectedIndex].text}`, 'info');
    switchView(state.currentView);
  });
}

function applyLanguageTranslations() {
  const dict = i18n[state.currentLang] || i18n.en;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      el.textContent = dict[key];
    }
  });

  const botWelcome = document.getElementById('chat-welcome-msg');
  if (botWelcome) {
    if (state.currentLang === 'ta') {
      botWelcome.innerHTML = `👋 வணக்கம்! நான் <strong>FloraAI</strong>. வளாக மண் ஈரப்பதம், தாவர பராமரிப்பு மற்றும் புள்ளிகள் பற்றி கேளுங்கள்!`;
    } else if (state.currentLang === 'es') {
      botWelcome.innerHTML = `👋 ¡Hola! Soy <strong>FloraAI</strong>. Pregúntame sobre la humedad del suelo y el cuidado de plantas.`;
    } else if (state.currentLang === 'fr') {
      botWelcome.innerHTML = `👋 Bonjour! Je suis <strong>FloraAI</strong>. Posez-moi des questions sur l'humidité du sol.`;
    } else if (state.currentLang === 'hi') {
      botWelcome.innerHTML = `👋 नमस्ते! मैं <strong>FloraAI</strong> हूँ। मुझसे मिट्टी की नमी और पौधों के बारे में पूछें!`;
    } else if (state.currentLang === 'de') {
      botWelcome.innerHTML = `👋 Hallo! Ich bin <strong>FloraAI</strong>. Fragen Sie mich nach der Bodenfeuchtigkeit.`;
    } else {
      botWelcome.innerHTML = `👋 Hello! I am <strong>FloraAI</strong>. Ask me about live campus soil moisture, plant care guidelines, maintenance schedules, or volunteer rewards!`;
    }
  }

  applyRolePermissions(state.currentRole);
}

function setupThemeToggle() {
  const btn = document.getElementById('theme-toggle-btn');
  if (!btn) return;
  btn.addEventListener('click', () => {
    state.theme = state.theme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', state.theme);
    btn.innerHTML = state.theme === 'light' ? '<i class="fa-solid fa-moon"></i>' : '<i class="fa-solid fa-sun"></i>';
    showToast(`Switched to ${state.theme} mode`, 'info');
  });
}

function switchView(viewName) {
  window.switchView = switchView;
  state.currentView = viewName;

  document.querySelectorAll('#main-nav .nav-item').forEach(item => {
    if (item.getAttribute('data-view') === viewName) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  });

  const titleMapEn = {
    'dashboard': 'Dashboard & Campus Analytics',
    'zones': 'Campus Zone Management & Map',
    'plants': 'Plant & Botanical Inventory',
    'maintenance': 'Maintenance Task Operations',
    'calendar': 'Maintenance Checklist Calendar',
    'health': 'Plant Health & AI Scan',
    'irrigation': 'Smart Irrigation & IoT Telemetry',
    'issues': 'Reported Campus Green Issues',
    'sustainability': 'Campus Sustainability & Carbon Offset',
    'biodiversity': 'Campus Biodiversity Tracker',
    'volunteers': 'Student Volunteer Hub & Rewards Store',
    'users': 'Student & Staff User Management',
    'notifications': 'Notification Center',
    'settings': 'System Settings & REST API Config'
  };

  const titleMapTa = {
    'dashboard': 'முதன்மை பலகை & ஆய்வுத் தகவல்கள்',
    'zones': 'வளாக மண்டல நிர்வாகம் & வரைபடம்',
    'plants': 'தாவரங்கள் & தாவரவியல் பட்டியல்',
    'maintenance': 'பராமரிப்பு பணி நடவடிக்கைகள்',
    'calendar': 'பராமரிப்பு பணி அட்டவணை',
    'health': 'தாவர ஆரோக்கியம் & AI நோய் பரிசோதனை',
    'irrigation': 'ஸ்மார்ட் பாசனம் & IoT தரவுகள்',
    'issues': 'வளாக பூங்கா புகார்கள்',
    'sustainability': 'வளாக சுற்றுச்சூழல் நிலைத்தன்மை',
    'biodiversity': 'வளாக பல்லுயிர் கண்காணிப்பு',
    'volunteers': 'மாணவர் மையம் & பரிசுகள் அங்காடி',
    'users': 'பயனாளர்கள் நிர்வாகம்',
    'notifications': 'அறிவிப்புகள் மையம்',
    'settings': 'அமைப்புகள் & API நிர்வாகம்'
  };

  const titleMap = state.currentLang === 'ta' ? titleMapTa : titleMapEn;
  document.getElementById('page-title-text').textContent = titleMap[viewName] || 'Smart Campus Gardening';
  window.location.hash = viewName;

  destroyCharts();

  switch (viewName) {
    case 'dashboard': renderDashboard(); break;
    case 'zones': renderZones(); break;
    case 'plants': renderPlants(); break;
    case 'maintenance': renderMaintenance(); break;
    case 'calendar': renderCalendar(); break;
    case 'health': renderHealth(); break;
    case 'irrigation': renderIrrigation(); break;
    case 'issues': renderIssues(); break;
    case 'sustainability': renderSustainability(); break;
    case 'biodiversity': renderBiodiversity(); break;
    case 'volunteers': renderVolunteers(); break;
    case 'users': renderUserManagement(); break;
    case 'notifications': renderNotifications(); break;
    case 'settings': renderSettings(); break;
    default: renderDashboard(); break;
  }

  applyLanguageTranslations();
}

function destroyCharts() {
  Object.keys(state.charts).forEach(key => {
    if (state.charts[key] && typeof state.charts[key].destroy === 'function') {
      state.charts[key].destroy();
    }
  });
  state.charts = {};
}

// ==========================================
// 1. DASHBOARD VIEW
// ==========================================

async function renderDashboard() {
  const container = document.getElementById('main-content-view');
  const dict = i18n[state.currentLang] || i18n.en;
  container.innerHTML = `<div style="text-align:center; padding: 3rem;"><i class="fa-solid fa-spinner fa-spin fa-2x"></i><p>Loading Telemetry...</p></div>`;

  try {
    const [statsRes, chartsRes] = await Promise.all([
      fetch(`${API_BASE}/dashboard/stats`),
      fetch(`${API_BASE}/dashboard/charts`)
    ]);
    const stats = await statsRes.json();
    const chartsData = await chartsRes.json();

    let lowMoistureAlertHTML = '';
    if (stats.low_moisture_zones_count > 0) {
      const alertMsg = state.currentLang === 'ta' 
        ? `${stats.low_moisture_zones_count} மண்டலத்தில் மண் ஈரப்பதம் 30% க்கும் குறைவாக உள்ளது! நீர் பாய்ச்ச பரிந்துரைக்கப்படுகிறது.`
        : `${stats.low_moisture_zones_count} Zone(s) report moisture below 30%. Smart watering recommended.`;

      lowMoistureAlertHTML = `
      <div class="card" style="background: rgba(244, 63, 94, 0.1); border-color: rgba(244, 63, 94, 0.3); margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 1rem;">
          <i class="fa-solid fa-triangle-exclamation" style="font-size: 1.5rem; color: #f43f5e;"></i>
          <div>
            <h4 style="color: #be123c;">${state.currentLang==='ta'?'மண் ஈரப்பதம் எச்சரிக்கை!':'Soil Moisture Warning Detected!'}</h4>
            <p style="font-size: 0.85rem; color: var(--text-main);">${alertMsg}</p>
          </div>
        </div>
        <button class="btn btn-danger btn-sm" onclick="switchView('irrigation')"><i class="fa-solid fa-droplet"></i> Trigger Irrigation</button>
      </div>`;
    }

    container.innerHTML = `
      ${lowMoistureAlertHTML}

      <div class="grid-kpi">
        <div class="card kpi-card">
          <div class="kpi-info">
            <h3>${dict.kpi_total_plants}</h3>
            <div class="value">${stats.total_plants}</div>
            <div class="sub-text">${stats.total_zones} ${state.currentLang==='ta'?'வளாக மண்டலங்கள்':'Campus Zones'}</div>
          </div>
          <div class="kpi-icon green"><i class="fa-solid fa-tree"></i></div>
        </div>

        <div class="card kpi-card">
          <div class="kpi-info">
            <h3>${dict.kpi_healthy_flora}</h3>
            <div class="value">${stats.healthy_plants}</div>
            <div class="sub-text">${Math.round((stats.healthy_plants / stats.total_plants) * 100)}% ${state.currentLang==='ta'?'ஆரோக்கிய குறியீடு':'Health Index'}</div>
          </div>
          <div class="kpi-icon green"><i class="fa-solid fa-heart"></i></div>
        </div>

        <div class="card kpi-card">
          <div class="kpi-info">
            <h3>${dict.kpi_attention_needed}</h3>
            <div class="value" style="color: #f43f5e;">${stats.attention_plants}</div>
            <div class="sub-text">${stats.critical_plants} ${state.currentLang==='ta'?'ஆபத்தான நிலை':'Critical Status'}</div>
          </div>
          <div class="kpi-icon rose"><i class="fa-solid fa-hand-holding-droplet"></i></div>
        </div>

        <div class="card kpi-card">
          <div class="kpi-info">
            <h3>${dict.kpi_green_cover}</h3>
            <div class="value">${stats.green_cover_percentage}%</div>
            <div class="sub-text">${state.currentLang==='ta'?'இலக்கு: 85%':'Campus Target: 85%'}</div>
          </div>
          <div class="kpi-icon blue"><i class="fa-solid fa-leaf"></i></div>
        </div>

        <div class="card kpi-card">
          <div class="kpi-info">
            <h3>${dict.kpi_completed_tasks}</h3>
            <div class="value">${stats.completed_tasks}</div>
            <div class="sub-text">${stats.pending_tasks} ${state.currentLang==='ta'?'நிலுவை பணிகள்':'Pending Tasks'}</div>
          </div>
          <div class="kpi-icon green"><i class="fa-solid fa-circle-check"></i></div>
        </div>

        <div class="card kpi-card">
          <div class="kpi-info">
            <h3>${dict.kpi_carbon_offset}</h3>
            <div class="value">${stats.estimated_carbon_offset_kg} <span style="font-size:1rem;">kg</span></div>
            <div class="sub-text">${state.currentLang==='ta'?'மதிப்பிடப்பட்ட CO2 ஈர்ப்பு':'Estimated CO2 Absorption'}</div>
          </div>
          <div class="kpi-icon amber"><i class="fa-solid fa-smog"></i></div>
        </div>

        <div class="card kpi-card">
          <div class="kpi-info">
            <h3>${dict.kpi_open_issues}</h3>
            <div class="value" style="color:#f59e0b;">${stats.open_issues_count}</div>
            <div class="sub-text">${state.currentLang==='ta'?'பதிவான புகார்கள்':'Reported Concerns'}</div>
          </div>
          <div class="kpi-icon amber"><i class="fa-solid fa-circle-exclamation"></i></div>
        </div>
      </div>

      <div class="grid-2col">
        <div class="card">
          <h3 style="margin-bottom: 1rem;"><i class="fa-solid fa-chart-line" style="color: #10b981;"></i> ${state.currentLang==='ta'?'பசுமை பரப்பு & வளர்ச்சி வரைபடம்':'Green Cover & Canopy Growth Trend'}</h3>
          <canvas id="greenCoverChart" height="220"></canvas>
        </div>

        <div class="card">
          <h3 style="margin-bottom: 1rem;"><i class="fa-solid fa-chart-pie" style="color: #06b6d4;"></i> ${state.currentLang==='ta'?'தாவர ஆரோக்கிய விநியோகம்':'Plant Health Distribution'}</h3>
          <canvas id="plantHealthChart" height="220"></canvas>
        </div>
      </div>

      <div class="grid-2col">
        <div class="card">
          <h3 style="margin-bottom: 1rem;"><i class="fa-solid fa-faucet-drip" style="color: #3b82f6;"></i> ${state.currentLang==='ta'?'மாதாந்திர நீர் பயன்பாடு vs சேமிப்பு (லிட்டர்)':'Monthly Water Usage vs Water Saved (Liters)'}</h3>
          <canvas id="waterTrendChart" height="220"></canvas>
        </div>

        <div class="card">
          <h3 style="margin-bottom: 1rem;"><i class="fa-solid fa-list-check" style="color: #84cc16;"></i> ${state.currentLang==='ta'?'பணி வகைப்பாடு பிரிவுகள்':'Task Breakdown by Type'}</h3>
          <canvas id="taskTypeChart" height="220"></canvas>
        </div>
      </div>
    `;

    initDashboardCharts(chartsData);

  } catch (err) {
    container.innerHTML = `<div class="card"><p style="color:red;">Error loading dashboard: ${err.message}</p></div>`;
  }
}

function initDashboardCharts(data) {
  if (typeof Chart === 'undefined') return;

  const timeline = data.sustainability_timeline || [];
  const labels = timeline.map(t => t.date);

  const el1 = document.getElementById('greenCoverChart');
  if (el1) {
    const ctxGreen = el1.getContext('2d');
    state.charts.greenCoverChart = new Chart(ctxGreen, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Green Cover %',
          data: timeline.map(t => t.green_cover),
          borderColor: '#10b981',
          backgroundColor: 'rgba(16, 185, 129, 0.15)',
          fill: true,
          tension: 0.35,
          borderWidth: 3
        }]
      },
      options: { responsive: true, plugins: { legend: { display: false } } }
    });
  }

  const el2 = document.getElementById('plantHealthChart');
  if (el2) {
    const ctxHealth = el2.getContext('2d');
    const hDist = data.plant_health_distribution || {};
    const healthyLbl = state.currentLang === 'ta' ? 'ஆரோக்கியமானது' : 'Healthy';
    const attentionLbl = state.currentLang === 'ta' ? 'கவனம் தேவை' : 'Needs Attention';
    const criticalLbl = state.currentLang === 'ta' ? 'ஆபத்தான நிலை' : 'Critical';

    state.charts.plantHealthChart = new Chart(ctxHealth, {
      type: 'doughnut',
      data: {
        labels: [healthyLbl, attentionLbl, criticalLbl],
        datasets: [{
          data: [hDist.Healthy || 0, hDist['Needs Attention'] || 0, hDist.Critical || 0],
          backgroundColor: ['#10b981', '#f59e0b', '#f43f5e']
        }]
      },
      options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
    });
  }

  const el3 = document.getElementById('waterTrendChart');
  if (el3) {
    const ctxWater = el3.getContext('2d');
    state.charts.waterTrendChart = new Chart(ctxWater, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          { label: state.currentLang==='ta'?'பயன்படுத்திய நீர்':'Water Used', data: timeline.map(t => t.water_used_liters), backgroundColor: '#3b82f6' },
          { label: state.currentLang==='ta'?'சேமித்த நீர்':'Water Saved', data: timeline.map(t => t.water_saved_liters), backgroundColor: '#34d399' }
        ]
      },
      options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
    });
  }

  const el4 = document.getElementById('taskTypeChart');
  if (el4) {
    const ctxTasks = el4.getContext('2d');
    const tDist = data.task_distribution || [];
    state.charts.taskTypeChart = new Chart(ctxTasks, {
      type: 'polarArea',
      data: {
        labels: tDist.map(t => t.task_type),
        datasets: [{
          data: tDist.map(t => t.count),
          backgroundColor: ['#10b981', '#06b6d4', '#84cc16', '#f59e0b', '#8b5cf6', '#ec4899']
        }]
      },
      options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
    });
  }
}

// ==========================================
// 2. ZONE MANAGEMENT VIEW
// ==========================================

async function renderZones() {
  const container = document.getElementById('main-content-view');
  const dict = i18n[state.currentLang] || i18n.en;
  container.innerHTML = `<div style="text-align:center; padding: 3rem;"><i class="fa-solid fa-spinner fa-spin fa-2x"></i></div>`;

  try {
    const res = await fetch(`${API_BASE}/zones`);
    const zones = await res.json();
    state.zones = zones;

    const isAdmin = state.currentRole === 'Admin';

    let zonePinsHTML = zones.map(z => {
      const pinClass = z.health_status === 'Critical' ? 'critical' : '';
      return `
        <div class="map-zone-pin ${pinClass}" style="left: ${z.map_x}%; top: ${z.map_y}%;" onclick="viewZoneDetail(${z.id})">
          <div class="pin-pulse"></div>
          <span>${z.name}</span>
        </div>
      `;
    }).join('');

    let zoneCardsHTML = zones.map(z => {
      const badgeClass = z.health_status === 'Healthy' ? 'badge-healthy' : z.health_status === 'Needs Attention' ? 'badge-attention' : 'badge-critical';
      const statusText = state.currentLang==='ta' ? (z.health_status==='Healthy'?'ஆரோக்கியமானது':z.health_status==='Needs Attention'?'கவனம் தேவை':'ஆபத்தான நிலை') : z.health_status;
      const moisture = z.latest_soil_moisture !== null ? `${z.latest_soil_moisture}%` : 'N/A';
      return `
        <div class="card">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom: 0.75rem;">
            <div>
              <h3 style="font-size: 1.1rem; font-weight:700;">${z.name}</h3>
              <p style="font-size: 0.82rem; color: var(--text-muted);"><i class="fa-solid fa-location-dot"></i> ${z.location}</p>
            </div>
            <span class="badge ${badgeClass}">${statusText}</span>
          </div>

          <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin: 1rem 0; font-size: 0.85rem;">
            <div><strong>${state.currentLang==='ta'?'பரப்பளவு:':'Area:'}</strong> ${z.area} m²</div>
            <div><strong>${state.currentLang==='ta'?'பசுமை பரப்பு:':'Green Cover:'}</strong> ${z.green_cover_percentage}%</div>
            <div><strong>${state.currentLang==='ta'?'தாவரங்கள்:':'Total Plants:'}</strong> ${z.plant_count}</div>
            <div><strong>${state.currentLang==='ta'?'மண் ஈரப்பதம்:':'Soil Moisture:'}</strong> ${moisture}</div>
          </div>

          <div style="display:flex; gap: 0.5rem; justify-content: flex-end; margin-top: 1rem; border-top: 1px solid var(--border-color); padding-top: 0.75rem;">
            <button class="btn btn-secondary btn-sm" onclick="viewZoneDetail(${z.id})"><i class="fa-solid fa-eye"></i> View Plants</button>
            ${isAdmin ? `<button class="btn btn-secondary btn-sm" onclick="openEditZoneModal(${z.id})"><i class="fa-solid fa-pen"></i></button>` : ''}
            ${isAdmin ? `<button class="btn btn-danger btn-sm" onclick="deleteZone(${z.id})"><i class="fa-solid fa-trash"></i></button>` : ''}
          </div>
        </div>
      `;
    }).join('');

    container.innerHTML = `
      <div class="section-header">
        <div>
          <h2>${state.currentLang==='ta'?'வளாக பூங்கா மண்டலங்கள்':'Campus Green Space Zones'}</h2>
          <p style="font-size: 0.88rem; color: var(--text-muted);">${state.currentLang==='ta'?'வளாகத்தின் பூங்கா பிரிவுகள், பசுமை அடர்த்தி & வரைபடக் குறியீடுகள்.':'Manage campus garden sectors, canopy coverage & live health pins.'}</p>
        </div>
        ${isAdmin ? `<button class="btn btn-primary" onclick="openAddZoneModal()"><i class="fa-solid fa-plus"></i> Add New Zone</button>` : ''}
      </div>

      <div class="campus-map-wrapper">
        <h3 style="margin-bottom: 0.75rem;"><i class="fa-solid fa-map" style="color: #10b981;"></i> ${state.currentLang==='ta'?'வளாகத்தின் ஊடாடும் வரைபடம்':'Interactive Campus Sector Map'}</h3>
        <div class="campus-svg-map">
          ${zonePinsHTML}
        </div>
      </div>

      <div class="grid-3col">
        ${zoneCardsHTML}
      </div>
    `;

    const issueZoneInput = document.getElementById('issue-zone-input');
    if (issueZoneInput) issueZoneInput.innerHTML = zones.map(z => `<option value="${z.id}">${z.name}</option>`).join('');

  } catch (err) {
    container.innerHTML = `<p style="color:red;">Error loading zones: ${err.message}</p>`;
  }
}

async function viewZoneDetail(zoneId) {
  try {
    const res = await fetch(`${API_BASE}/zones/${zoneId}`);
    const data = await res.json();
    const zone = data.zone;
    const plants = data.plants;

    let plantsHTML = plants.map(p => `
      <tr>
        <td><strong>${p.plant_code}</strong></td>
        <td>${p.name}</td>
        <td><em>${p.species}</em></td>
        <td><span class="badge ${p.health_status==='Healthy'?'badge-healthy':'badge-critical'}">${p.health_status}</span></td>
        <td>${p.last_watered || 'N/A'}</td>
      </tr>
    `).join('');

    const modalHTML = `
      <div class="modal-backdrop active" id="zone-detail-modal">
        <div class="modal-card" style="max-width: 700px;">
          <div class="modal-header">
            <h3><i class="fa-solid fa-building-circle-check" style="color: #10b981;"></i> ${zone.name}</h3>
            <button class="close-btn" onclick="closeModal('zone-detail-modal')">&times;</button>
          </div>
          <p style="margin-bottom: 1rem; font-size: 0.9rem; color: var(--text-muted);">${zone.location} | Area: ${zone.area} sq m | Green Cover: ${zone.green_cover_percentage}%</p>
          
          <h4 style="margin-bottom: 0.5rem;">Flora Inventory (${plants.length} Plants)</h4>
          <div class="table-container">
            <table class="custom-table">
              <thead>
                <tr>
                  <th>Code</th>
                  <th>Name</th>
                  <th>Species</th>
                  <th>Health</th>
                  <th>Last Watered</th>
                </tr>
              </thead>
              <tbody>
                ${plantsHTML || '<tr><td colspan="5">No plants assigned to this zone.</td></tr>'}
              </tbody>
            </table>
          </div>
          <div style="margin-top: 1.5rem; text-align: right;">
            <button class="btn btn-secondary" onclick="closeModal('zone-detail-modal')">Close</button>
          </div>
        </div>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHTML);

  } catch (err) {
    showToast('Failed to load zone detail', 'error');
  }
}

// ==========================================
// 3. PLANT INVENTORY & QR BIOGRAPHY VIEW
// ==========================================

async function renderPlants() {
  const container = document.getElementById('main-content-view');
  const dict = i18n[state.currentLang] || i18n.en;
  container.innerHTML = `<div style="text-align:center; padding: 3rem;"><i class="fa-solid fa-spinner fa-spin fa-2x"></i></div>`;

  try {
    const [plantsRes, zonesRes] = await Promise.all([
      fetch(`${API_BASE}/plants`),
      fetch(`${API_BASE}/zones`)
    ]);
    const plants = await plantsRes.json();
    const zones = await zonesRes.json();
    state.plants = plants;
    state.zones = zones;

    const isAdmin = state.currentRole === 'Admin';
    const isStaff = state.currentRole === 'Gardening Staff' || state.currentRole === 'Staff';

    const zoneOptions = zones.map(z => `<option value="${z.id}">${z.name}</option>`).join('');

    let plantCardsHTML = plants.map(p => {
      const badgeClass = p.health_status === 'Healthy' ? 'badge-healthy' : p.health_status === 'Needs Attention' ? 'badge-attention' : 'badge-critical';
      const statusText = state.currentLang==='ta' ? (p.health_status==='Healthy'?'ஆரோக்கியமானது':p.health_status==='Needs Attention'?'கவனம் தேவை':'ஆபத்தான நிலை') : p.health_status;
      const verifiedPhoto = getVerifiedPlantImage(p.name, p.species, p.photo);
      return `
        <div class="card plant-card">
          <div class="plant-card-header">
            <img src="${verifiedPhoto}" alt="${p.name}" onerror="this.src='https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=600'">
            <span class="badge ${badgeClass}" style="position: absolute; top: 12px; right: 12px;">${statusText}</span>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:baseline;">
            <span style="font-size: 0.75rem; font-weight:700; color: var(--primary-600);">${p.plant_code}</span>
            <span style="font-size: 0.78rem; color: var(--text-muted);">${p.type}</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight:700; margin: 0.2rem 0;">${p.name}</h3>
          <p style="font-size: 0.82rem; font-style: italic; color: var(--text-muted); margin-bottom: 0.75rem;">${p.species}</p>
          
          <div style="font-size: 0.8rem; display:flex; flex-direction:column; gap: 0.35rem; border-top: 1px solid var(--border-color); padding-top: 0.65rem;">
            <div><i class="fa-solid fa-location-dot" style="color:#10b981;"></i> <strong>${state.currentLang==='ta'?'மண்டலம்:':'Zone:'}</strong> ${p.zone_name}</div>
            <div><i class="fa-solid fa-droplet" style="color:#3b82f6;"></i> <strong>${state.currentLang==='ta'?'கடைசியாக நீர் பாய்ச்சியது:':'Last Watered:'}</strong> ${p.last_watered || 'Today'}</div>
          </div>

          <div style="display:flex; gap: 0.4rem; justify-content: flex-end; margin-top: 1rem; flex-wrap: wrap;">
            <button class="btn btn-secondary btn-sm" onclick="openPlantQRModal(${p.id})"><i class="fa-solid fa-qrcode"></i> QR Bio</button>
            <button class="btn btn-primary btn-sm" onclick="openReplacementModal(${p.id})"><i class="fa-solid fa-arrows-rotate"></i> ${state.currentLang==='ta'?'மாற்று பரிந்துரை':'Smart Replace'}</button>
            <button class="btn btn-secondary btn-sm" onclick="openHealthModal(${p.id})"><i class="fa-solid fa-stethoscope"></i> Log Health</button>
            ${(isAdmin || isStaff) ? `<button class="btn btn-secondary btn-sm" onclick="openEditPlantModal(${p.id})"><i class="fa-solid fa-pen"></i></button>` : ''}
            ${isAdmin ? `<button class="btn btn-danger btn-sm" onclick="deletePlant(${p.id})"><i class="fa-solid fa-trash"></i></button>` : ''}
          </div>
        </div>
      `;
    }).join('');

    container.innerHTML = `
      <div class="section-header">
        <div>
          <h2>${state.currentLang==='ta'?'தாவரங்கள் & தாவரவியல் பட்டியல்':'Botanical & Plant Inventory'}</h2>
          <p style="font-size: 0.88rem; color: var(--text-muted);">${state.currentLang==='ta'?'வளாக மரங்கள், புதர்கள், மூலிகைகள் மற்றும் பராமரிப்பு அட்டவணை.':'Real-time database of campus trees, shrubs, flora health & care schedules.'}</p>
        </div>
        ${isAdmin ? `<button class="btn btn-primary" onclick="openAddPlantModal()"><i class="fa-solid fa-plus"></i> Add New Plant</button>` : ''}
      </div>

      <div class="card" style="margin-bottom: 1.5rem;">
        <div class="search-filter-bar">
          <div style="position: relative;">
            <i class="fa-solid fa-magnifying-glass" style="position: absolute; left: 12px; top: 12px; color: var(--text-muted);"></i>
            <input type="text" class="input-search" id="plant-search-input" placeholder="${state.currentLang==='ta'?'பெயர் அல்லது குறியீடு மூலம் தேடுக...':'Search by name, species or code...'}" onkeyup="filterPlants()">
          </div>

          <select class="select-filter" id="plant-zone-filter" onchange="filterPlants()">
            <option value="all">${state.currentLang==='ta'?'அனைத்து மண்டலங்கள்':'All Campus Zones'}</option>
            ${zoneOptions}
          </select>

          <select class="select-filter" id="plant-health-filter" onchange="filterPlants()">
            <option value="all">${state.currentLang==='ta'?'அனைத்து நிலைகள்':'All Health Statuses'}</option>
            <option value="Healthy">${state.currentLang==='ta'?'ஆரோக்கியமானது':'Healthy'}</option>
            <option value="Needs Attention">${state.currentLang==='ta'?'கவனம் தேவை':'Needs Attention'}</option>
            <option value="Critical">${state.currentLang==='ta'?'ஆபத்தான நிலை':'Critical'}</option>
          </select>
        </div>
      </div>

      <div class="plant-card-grid" id="plants-grid-container" style="margin-bottom: 2rem;">
        ${plantCardsHTML}
      </div>

      <!-- Replacement History Audit Log Table Section -->
      <div class="card">
        <h3 style="margin-bottom: 1rem; font-weight:700; display:flex; align-items:center; gap:0.5rem;">
          <i class="fa-solid fa-history" style="color:#10b981;"></i>
          <span>${state.currentLang==='ta'?'தாவர மாற்று வரலாறு':'Plant Replacement History Log'}</span>
        </h3>
        <div class="table-container">
          <table class="custom-table">
            <thead>
              <tr>
                <th>${state.currentLang==='ta'?'பழைய தாவரம்':'Old Plant'}</th>
                <th>${state.currentLang==='ta'?'புதிய தாவரம்':'New Plant'}</th>
                <th>${state.currentLang==='ta'?'இடம்':'Location / Zone'}</th>
                <th>${state.currentLang==='ta'?'பொருத்தமான மதிப்பெண்':'Match Score'}</th>
                <th>Date</th>
                <th>Replaced By</th>
              </tr>
            </thead>
            <tbody id="replacement-history-table-body">
              <tr><td colspan="6" style="text-align:center;">Loading replacement audit logs...</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    `;

    const pZoneInput = document.getElementById('plant-zone-input');
    if (pZoneInput) pZoneInput.innerHTML = zoneOptions;

    renderReplacementHistory();

  } catch (err) {
    container.innerHTML = `<p style="color:red;">Error loading plants: ${err.message}</p>`;
  }
}

async function openPlantQRModal(plantId) {
  openModal('qr-modal');
  const body = document.getElementById('qr-modal-body');
  body.innerHTML = `<i class="fa-solid fa-spinner fa-spin fa-2x"></i><p>Generating Scannable QR Biography...</p>`;

  try {
    const res = await fetch(`${API_BASE}/plants/${plantId}/qr`);
    const data = await res.json();
    const p = data.plant;

    body.innerHTML = `
      <div style="margin-bottom: 1rem;">
        <img src="${data.qr_code_url}" style="width:160px; height:160px; border-radius:12px; border:2px solid var(--primary-500); padding:5px;">
        <h3 style="margin-top:0.5rem; font-size:1.2rem;">${p.name}</h3>
        <p style="font-size:0.85rem; font-style:italic; color:var(--text-muted);">${p.species}</p>
        <span class="badge badge-healthy" style="margin-top:0.4rem;">${p.plant_code} | ${p.type}</span>
      </div>

      <div style="text-align:left; background:var(--primary-50); padding:1rem; border-radius:12px; font-size:0.85rem;">
        <p><strong><i class="fa-solid fa-leaf" style="color:#10b981;"></i> ${state.currentLang==='ta'?'மண்டலம்:':'Zone:'}</strong> ${p.zone_name} (${p.zone_location})</p>
        <p><strong><i class="fa-solid fa-calendar-check" style="color:#3b82f6;"></i> ${state.currentLang==='ta'?'நட்ட தேதி:':'Planted Date:'}</strong> ${p.planted_date}</p>
        <p style="margin-top:0.4rem;"><strong>🌱 ${state.currentLang==='ta'?'சுற்றுச்சூழல் நன்மை:':'Environmental Impact:'}</strong> ${data.environmental_benefits}</p>
        <p style="margin-top:0.4rem;"><strong>💧 ${state.currentLang==='ta'?'பராமரிப்பு குறிப்பு:':'Care Guidelines:'}</strong> ${data.care_guidelines}</p>
      </div>
    `;
  } catch (e) {
    body.innerHTML = `<p style="color:red;">Failed to generate QR Tag.</p>`;
  }
}

// ==========================================
// 4. MAINTENANCE TASKS VIEW
// ==========================================

async function renderMaintenance() {
  const container = document.getElementById('main-content-view');
  const dict = i18n[state.currentLang] || i18n.en;
  container.innerHTML = `<div style="text-align:center; padding: 3rem;"><i class="fa-solid fa-spinner fa-spin fa-2x"></i></div>`;

  try {
    const [tasksRes, zonesRes, plantsRes] = await Promise.all([
      fetch(`${API_BASE}/tasks`),
      fetch(`${API_BASE}/zones`),
      fetch(`${API_BASE}/plants`)
    ]);
    const tasks = await tasksRes.json();
    const zones = await zonesRes.json();
    const plants = await plantsRes.json();

    state.tasks = tasks;
    state.zones = zones;
    state.plants = plants;

    const isAdmin = state.currentRole === 'Admin';
    const isStaff = state.currentRole === 'Gardening Staff' || state.currentRole === 'Staff';

    let taskCardsHTML = tasks.map(t => {
      const statusBadge = t.status === 'Completed' ? 'badge-completed' : t.status === 'In Progress' ? 'badge-in-progress' : t.status === 'Overdue' ? 'badge-overdue' : 'badge-pending';
      const statusText = state.currentLang==='ta' ? (t.status==='Completed'?'முடிந்தது':t.status==='In Progress'?'செயல்பாட்டில்':t.status==='Overdue'?'காலாவதியானது':'நிலுவையில்') : t.status;
      const prioColor = t.priority === 'Urgent' ? '#f43f5e' : t.priority === 'High' ? '#f59e0b' : '#10b981';

      return `
        <div class="card">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom: 0.5rem;">
            <span class="badge ${statusBadge}">${statusText}</span>
            <span style="font-size: 0.75rem; font-weight:700; color: ${prioColor}; border: 1px solid ${prioColor}; padding: 2px 6px; border-radius: 4px;">${t.priority}</span>
          </div>

          <h3 style="font-size: 1.05rem; font-weight:700; margin-bottom: 0.2rem;">${t.task_type}</h3>
          <p style="font-size: 0.85rem; color: var(--text-muted);"><i class="fa-solid fa-location-dot"></i> Zone: ${t.zone_name} ${t.plant_name ? `(${t.plant_name})` : ''}</p>
          <p style="font-size: 0.82rem; margin: 0.5rem 0;"><strong>${state.currentLang==='ta'?'ஒதுக்கப்பட்டது:':'Assigned:'}</strong> ${t.assigned_to} | <strong>${state.currentLang==='ta'?'திட்டமிட்ட தேதி:':'Scheduled:'}</strong> ${t.scheduled_date}</p>
          <p style="font-size: 0.8rem; font-style: italic; color: var(--text-muted);">${t.notes}</p>

          ${t.photo_proof ? `<div style="margin-top:0.5rem;"><img src="${t.photo_proof}" style="width:100%; height:120px; object-fit:cover; border-radius:8px;"></div>` : ''}

          <div style="display:flex; gap: 0.5rem; justify-content: flex-end; margin-top: 1rem; border-top: 1px solid var(--border-color); padding-top: 0.65rem;">
            ${(isStaff || isAdmin) && t.status !== 'Completed' ? `<button class="btn btn-primary btn-sm" onclick="openCompleteTaskModal(${t.id})"><i class="fa-solid fa-check"></i> Complete & Photo Proof</button>` : ''}
          </div>
        </div>
      `;
    }).join('');

    container.innerHTML = `
      <div class="section-header">
        <div>
          <h2>${state.currentLang==='ta'?'தோட்டக்கலை & வளாக பராமரிப்பு பணிகள்':'Gardening & Campus Maintenance Tasks'}</h2>
          <p style="font-size: 0.88rem; color: var(--text-muted);">${state.currentLang==='ta'?'நீர் பாய்ச்சுதல், கிளை நறுக்குதல், உரம் இடுதல் பணிகளை நிர்வகிக்கவும்.':'Assign, track & execute watering, pruning, fertilizing & pest control activities.'}</p>
        </div>
        ${(isAdmin || isStaff) ? `<button class="btn btn-primary" onclick="openAddTaskModal()"><i class="fa-solid fa-plus"></i> Create Task</button>` : ''}
      </div>

      <div class="grid-3col">
        ${taskCardsHTML}
      </div>
    `;

    const tZoneInput = document.getElementById('task-zone-input');
    const tPlantInput = document.getElementById('task-plant-input');
    if (tZoneInput) tZoneInput.innerHTML = zones.map(z => `<option value="${z.id}">${z.name}</option>`).join('');
    if (tPlantInput) tPlantInput.innerHTML = `<option value="">Entire Zone (No specific plant)</option>` + plants.map(p => `<option value="${p.id}">${p.plant_code} - ${p.name}</option>`).join('');

  } catch (err) {
    container.innerHTML = `<p style="color:red;">Error loading tasks: ${err.message}</p>`;
  }
}

// ==========================================
// 5. MAINTENANCE CALENDAR VIEW
// ==========================================

async function renderCalendar() {
  const container = document.getElementById('main-content-view');
  container.innerHTML = `<div style="text-align:center; padding: 3rem;"><i class="fa-solid fa-spinner fa-spin fa-2x"></i></div>`;

  try {
    const res = await fetch(`${API_BASE}/tasks`);
    const tasks = await res.json();

    const todayStr = new Date().toISOString().split('T')[0];

    const todaysTasks = tasks.filter(t => t.scheduled_date === todayStr);
    const upcomingTasks = tasks.filter(t => t.scheduled_date > todayStr);
    const overdueTasks = tasks.filter(t => t.status === 'Overdue' || (t.scheduled_date < todayStr && t.status !== 'Completed'));

    container.innerHTML = `
      <div class="section-header">
        <div>
          <h2>${state.currentLang==='ta'?'பராமரிப்பு பணி அட்டவணை':'Maintenance Checklist Calendar'}</h2>
          <p style="font-size: 0.88rem; color: var(--text-muted);">${state.currentLang==='ta'?'தினசரி பணியாளர்கள் பணி அட்டவணை மற்றும் காலாவதியான பணிகள்.':'Daily staff schedules, upcoming care & overdue alerts.'}</p>
        </div>
      </div>

      <div class="grid-3col">
        <div class="card" style="border-top: 4px solid #10b981;">
          <h3 style="margin-bottom: 1rem;"><i class="fa-solid fa-calendar-day" style="color: #10b981;"></i> ${state.currentLang==='ta'?'இன்றைய பணிகள்':'Today\'s Schedule'} (${todaysTasks.length})</h3>
          <div style="display:flex; flex-direction:column; gap: 0.75rem;">
            ${todaysTasks.map(t => `
              <div style="padding:0.75rem; background:var(--bg-main); border-radius:8px; border-left: 3px solid #10b981;">
                <div style="font-size: 0.85rem; font-weight:700;">${t.task_type} - ${t.zone_name}</div>
                <div style="font-size: 0.78rem; color:var(--text-muted);">Assigned to: ${t.assigned_to}</div>
              </div>
            `).join('') || `<p style="font-size:0.85rem; color:var(--text-muted);">${state.currentLang==='ta'?'இன்று பணிகள் இல்லை.':'No tasks scheduled for today.'}</p>`}
          </div>
        </div>

        <div class="card" style="border-top: 4px solid #f43f5e;">
          <h3 style="margin-bottom: 1rem;"><i class="fa-solid fa-triangle-exclamation" style="color: #f43f5e;"></i> ${state.currentLang==='ta'?'காலாவதியான பணிகள்':'Overdue Maintenance'} (${overdueTasks.length})</h3>
          <div style="display:flex; flex-direction:column; gap: 0.75rem;">
            ${overdueTasks.map(t => `
              <div style="padding:0.75rem; background:rgba(244, 63, 94, 0.08); border-radius:8px; border-left: 3px solid #f43f5e;">
                <div style="font-size: 0.85rem; font-weight:700; color:#be123c;">${t.task_type} - ${t.zone_name}</div>
                <div style="font-size: 0.78rem; color:var(--text-muted);">Due: ${t.scheduled_date} | Staff: ${t.assigned_to}</div>
              </div>
            `).join('') || `<p style="font-size:0.85rem; color:var(--text-muted);">${state.currentLang==='ta'?'காலாவதியான பணிகள் எதுவும் இல்லை!':'Great job! No overdue tasks.'}</p>`}
          </div>
        </div>

        <div class="card" style="border-top: 4px solid #3b82f6;">
          <h3 style="margin-bottom: 1rem;"><i class="fa-solid fa-calendar-week" style="color: #3b82f6;"></i> ${state.currentLang==='ta'?'அடுத்த 7 நாட்கள் பணிகள்':'Upcoming Next 7 Days'} (${upcomingTasks.length})</h3>
          <div style="display:flex; flex-direction:column; gap: 0.75rem;">
            ${upcomingTasks.map(t => `
              <div style="padding:0.75rem; background:var(--bg-main); border-radius:8px;">
                <div style="font-size: 0.85rem; font-weight:700;">${t.task_type} - ${t.zone_name}</div>
                <div style="font-size: 0.78rem; color:var(--text-muted);">Date: ${t.scheduled_date}</div>
              </div>
            `).join('') || `<p style="font-size:0.85rem; color:var(--text-muted);">${state.currentLang==='ta'?'அடுத்தடுத்த பணிகள் இல்லை.':'No upcoming tasks scheduled.'}</p>`}
          </div>
        </div>
      </div>
    `;

  } catch (err) {
    container.innerHTML = `<p style="color:red;">Error loading calendar: ${err.message}</p>`;
  }
}

// ==========================================
// 6. PLANT HEALTH & AI DISEASE SCANNER VIEW
// ==========================================

async function renderHealth() {
  const container = document.getElementById('main-content-view');
  const dict = i18n[state.currentLang] || i18n.en;
  container.innerHTML = `<div style="text-align:center; padding: 3rem;"><i class="fa-solid fa-spinner fa-spin fa-2x"></i></div>`;

  try {
    const res = await fetch(`${API_BASE}/plants`);
    const plants = await res.json();
    state.plants = plants;

    const healthyList = plants.filter(p => p.health_status === 'Healthy');
    const attentionList = plants.filter(p => p.health_status === 'Needs Attention');
    const criticalList = plants.filter(p => p.health_status === 'Critical');

    container.innerHTML = `
      <div class="section-header">
        <div>
          <h2>${state.currentLang==='ta'?'தாவர ஆரோக்கியம் & AI சோதனை':'Campus Plant Health & AI Disease Scan'}</h2>
          <p style="font-size: 0.88rem; color: var(--text-muted);">${state.currentLang==='ta'?'இலை நோய், பூச்சி தாக்குதலை கண்டறிந்து AI சிகிச்சை குறிப்பு பெறலாம்.':'Identify wilt, pest attack, leaf spots & run instant AI disease analysis.'}</p>
        </div>
        <button class="btn btn-primary" onclick="openAIScannerModal()"><i class="fa-solid fa-microscope"></i> Run AI Disease Scanner</button>
      </div>

      <div class="grid-3col" style="margin-bottom:2rem;">
        <div class="card" style="border-left: 4px solid #10b981;">
          <h3>${state.currentLang==='ta'?'ஆரோக்கியமான தாவரங்கள்':'Healthy Flora'}</h3>
          <div style="font-size: 2rem; font-weight:800; color:#10b981;">${healthyList.length}</div>
          <p style="font-size: 0.8rem; color:var(--text-muted);">${state.currentLang==='ta'?'சிறந்த மண் ஈரப்பதம்.':'Optimal soil moisture.'}</p>
        </div>
        <div class="card" style="border-left: 4px solid #f59e0b;">
          <h3>${state.currentLang==='ta'?'கவனம் தேவை':'Needs Attention'}</h3>
          <div style="font-size: 2rem; font-weight:800; color:#f59e0b;">${attentionList.length}</div>
          <p style="font-size: 0.8rem; color:var(--text-muted);">${state.currentLang==='ta'?'நீர் அல்லது உரம் தேவை.':'Requires watering/nutrients.'}</p>
        </div>
        <div class="card" style="border-left: 4px solid #f43f5e;">
          <h3>${state.currentLang==='ta'?'ஆபத்தான நிலை':'Critical Health Alert'}</h3>
          <div style="font-size: 2rem; font-weight:800; color:#f43f5e;">${criticalList.length}</div>
          <p style="font-size: 0.8rem; color:var(--text-muted);">${state.currentLang==='ta'?'உடனடி கவனத்திற்கு.':'Immediate action required.'}</p>
        </div>
      </div>

      <div class="card">
        <h3 style="margin-bottom: 1rem;"><i class="fa-solid fa-notes-medical" style="color:#f43f5e;"></i> ${state.currentLang==='ta'?'பராமரிப்பு தேவைப்படும் தாவரங்கள்':'Plants Requiring Diagnostic Care'}</h3>
        <div class="table-container">
          <table class="custom-table">
            <thead>
              <tr>
                <th>Code</th>
                <th>Name</th>
                <th>Zone</th>
                <th>Status</th>
                <th>Notes</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              ${[...criticalList, ...attentionList].map(p => `
                <tr>
                  <td><strong>${p.plant_code}</strong></td>
                  <td>${p.name}</td>
                  <td>${p.zone_name}</td>
                  <td><span class="badge ${p.health_status==='Critical'?'badge-critical':'badge-attention'}">${p.health_status}</span></td>
                  <td>${p.notes}</td>
                  <td>
                    <button class="btn btn-secondary btn-sm" onclick="openHealthModal(${p.id})"><i class="fa-solid fa-pen"></i> Log Diagnosis</button>
                  </td>
                </tr>
              `).join('') || '<tr><td colspan="6">All campus plants are healthy!</td></tr>'}
            </tbody>
          </table>
        </div>
      </div>
    `;

    const scanPlantSelect = document.getElementById('scan-plant-select');
    if (scanPlantSelect) scanPlantSelect.innerHTML = plants.map(p => `<option value="${p.id}">${p.plant_code} - ${p.name}</option>`).join('');

  } catch (err) {
    container.innerHTML = `<p style="color:red;">Error loading plant health: ${err.message}</p>`;
  }
}

function openAIScannerModal() {
  const resContainer = document.getElementById('scan-result-container');
  if (resContainer) resContainer.style.display = 'none';
  openModal('ai-scanner-modal');
}

async function runAIPlantScan() {
  const plantId = document.getElementById('scan-plant-select').value;
  const container = document.getElementById('scan-result-container');
  if (container) {
    container.style.display = 'block';
    container.innerHTML = `<div style="text-align:center; padding:1.5rem;"><i class="fa-solid fa-spinner fa-spin fa-2x" style="color:#10b981;"></i><p>Scanning leaf cellular patterns via AI Neural Network...</p></div>`;
  }

  try {
    const res = await fetch(`${API_BASE}/ai/plant-health-scan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ plant_id: plantId })
    });
    const data = await res.json();
    const scan = data.scan_result;

    if (container) {
      container.innerHTML = `
        <div style="background:var(--primary-50); border:1px solid var(--primary-300); padding:1.25rem; border-radius:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
            <h4 style="color:#047857; font-weight:700;">🔍 ${scan.disease}</h4>
            <span class="badge badge-healthy">${scan.confidence}% Confidence</span>
          </div>
          <p style="font-size:0.85rem; margin:0.4rem 0;"><strong>Symptoms Detected:</strong> ${scan.symptoms}</p>
          <p style="font-size:0.85rem; color:#15803d; background:#dcfce7; padding:0.6rem; border-radius:8px; margin-top:0.5rem;">
            <strong>🌱 AI Organic Treatment Recipe:</strong> ${scan.treatment}
          </p>
        </div>
      `;
    }
    showToast('AI Scan Complete & Plant Health Record Updated!', 'success');
  } catch (e) {
    if (container) container.innerHTML = `<p style="color:red;">AI Scan error.</p>`;
  }
}

// ==========================================
// 7. SMART IRRIGATION & IOT TELEMETRY VIEW
// ==========================================

async function renderIrrigation() {
  const container = document.getElementById('main-content-view');
  const dict = i18n[state.currentLang] || i18n.en;
  container.innerHTML = `<div style="text-align:center; padding: 3rem;"><i class="fa-solid fa-spinner fa-spin fa-2x"></i></div>`;

  try {
    const res = await fetch(`${API_BASE}/sensors/readings`);
    const telemetry = await res.json();

    let telemetryCardsHTML = telemetry.map(t => {
      const isLow = t.soil_moisture < 30.0;
      const cardBorder = isLow ? 'border: 2px solid #f43f5e;' : 'border: 1px solid var(--border-color);';
      const waveHTML = isLow ? '<div class="water-wave"></div>' : '';
      const alertText = state.currentLang==='ta' ? (isLow?'குறைந்த ஈரப்பதம்':'இயல்பான நிலை') : t.status_alert;

      return `
        <div class="card water-flow-bg" style="${cardBorder}">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.75rem;">
            <h3 style="font-size: 1.1rem; font-weight:700;">${t.zone_name}</h3>
            <span class="badge ${isLow ? 'badge-critical' : 'badge-healthy'}">${alertText}</span>
          </div>

          <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5rem; text-align:center; margin: 1rem 0;">
            <div style="background:rgba(6, 182, 212, 0.1); padding:0.75rem; border-radius:8px;">
              <div style="font-size: 0.72rem; color:var(--text-muted);">${state.currentLang==='ta'?'மண் ஈரப்பதம்':'MOISTURE'}</div>
              <div style="font-size: 1.4rem; font-weight:800; color:#06b6d4;">${t.soil_moisture}%</div>
            </div>
            <div style="background:rgba(59, 130, 246, 0.1); padding:0.75rem; border-radius:8px;">
              <div style="font-size: 0.72rem; color:var(--text-muted);">${state.currentLang==='ta'?'ஈரப்பதம்':'HUMIDITY'}</div>
              <div style="font-size: 1.4rem; font-weight:800; color:#3b82f6;">${t.humidity}%</div>
            </div>
            <div style="background:rgba(245, 158, 11, 0.1); padding:0.75rem; border-radius:8px;">
              <div style="font-size: 0.72rem; color:var(--text-muted);">${state.currentLang==='ta'?'வெப்பநிலை':'TEMP'}</div>
              <div style="font-size: 1.4rem; font-weight:800; color:#f59e0b;">${t.temperature}°C</div>
            </div>
          </div>

          <p style="font-size:0.75rem; color:var(--text-muted); margin-bottom:1rem;">Sensor Node #IOT-Z${t.zone_id} | Last Sync: ${t.timestamp}</p>

          <button class="btn ${isLow ? 'btn-danger' : 'btn-primary'}" style="width:100%; justify-content:center;" onclick="triggerIrrigationZone(${t.zone_id})">
            <i class="fa-solid fa-droplet"></i> Trigger Smart Drip Irrigation
          </button>
          ${waveHTML}
        </div>
      `;
    }).join('');

    container.innerHTML = `
      <div class="section-header">
        <div>
          <h2>${state.currentLang==='ta'?'ஸ்மார்ட் பாசனம் & IoT மண் தரவுகள்':'Smart Irrigation & IoT Soil Telemetry'}</h2>
          <p style="font-size: 0.88rem; color: var(--text-muted);">${state.currentLang==='ta'?'நேரலை IoT மண் உணரி அளவீடுகள் மற்றும் தானியங்கி சொட்டுநீர் கட்டுப்பாடுகள்.':'Real-time IoT capacitive soil sensors, atmospheric readings & automated drip controls.'}</p>
        </div>
      </div>

      <div class="grid-3col">
        ${telemetryCardsHTML}
      </div>
    `;

  } catch (err) {
    container.innerHTML = `<p style="color:red;">Error loading telemetry: ${err.message}</p>`;
  }
}

async function triggerIrrigationZone(zoneId) {
  showToast(`Activating Smart Drip Valve for Zone #${zoneId}...`, 'info');
  try {
    const res = await fetch(`${API_BASE}/iot/irrigate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ zone_id: zoneId, duration_mins: 15 })
    });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      renderIrrigation();
    }
  } catch (err) {
    showToast('Failed to trigger irrigation', 'error');
  }
}

// ==========================================
// 8. CAMPUS REPORTED ISSUES VIEW
// ==========================================

async function renderIssues() {
  const container = document.getElementById('main-content-view');
  const dict = i18n[state.currentLang] || i18n.en;
  container.innerHTML = `<div style="text-align:center; padding: 3rem;"><i class="fa-solid fa-spinner fa-spin fa-2x"></i></div>`;

  try {
    const res = await fetch(`${API_BASE}/issues`);
    const issues = await res.json();

    const isAdmin = state.currentRole === 'Admin';
    const isStaff = state.currentRole === 'Gardening Staff' || state.currentRole === 'Staff';

    let issuesHTML = issues.map(i => {
      const prioColor = i.priority === 'Urgent' ? '#f43f5e' : i.priority === 'High' ? '#f59e0b' : '#10b981';
      const statusText = state.currentLang==='ta' ? (i.status==='Open'?'திறந்த நிலையில்':'முடிக்கப்பட்டது') : i.status;

      return `
        <div class="card" style="border-left: 4px solid ${prioColor};">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
            <span class="badge ${i.status==='Open'?'badge-critical':'badge-approved'}">${statusText}</span>
            <span style="font-size:0.75rem; font-weight:700; color:${prioColor};">${i.priority} Priority</span>
          </div>

          <h3 style="font-size:1.05rem; font-weight:700;">${i.title}</h3>
          <p style="font-size:0.82rem; color:var(--text-muted);"><i class="fa-solid fa-location-dot"></i> Zone: ${i.zone_name} | Reporter: ${i.reporter_name}</p>
          <p style="font-size:0.85rem; margin:0.5rem 0;">${i.description}</p>
          
          ${i.photo ? `<img src="${i.photo}" style="width:100%; height:120px; object-fit:cover; border-radius:8px; margin:0.5rem 0;">` : ''}

          <div style="display:flex; gap:0.5rem; justify-content:flex-end; margin-top:0.75rem; border-top:1px solid var(--border-color); padding-top:0.5rem;">
            ${(isAdmin || isStaff) && i.status === 'Open' ? `<button class="btn btn-primary btn-sm" onclick="convertIssueToTask(${i.id})"><i class="fa-solid fa-arrow-right-to-bracket"></i> Convert to Task</button>` : ''}
          </div>
        </div>
      `;
    }).join('');

    container.innerHTML = `
      <div class="section-header">
        <div>
          <h2>${state.currentLang==='ta'?'வளாக பூங்கா புகார்கள்':'Campus Reported Issues'}</h2>
          <p style="font-size: 0.88rem; color: var(--text-muted);">${state.currentLang==='ta'?'மாணவர்கள்/ஊழியர்கள் பதிவுசெய்த புகார்கள் மற்றும் அவற்றை பராமரிப்பு பணியாக மாற்றுதல்.':'View concerns reported by students/staff and convert them into actionable maintenance tasks.'}</p>
        </div>
        <button class="btn btn-danger" onclick="openModal('issue-modal')"><i class="fa-solid fa-plus"></i> Report New Issue</button>
      </div>

      <div class="grid-3col">
        ${issuesHTML || '<p>No active issues reported.</p>'}
      </div>
    `;

  } catch (err) {
    container.innerHTML = `<p style="color:red;">Error loading issues: ${err.message}</p>`;
  }
}

async function convertIssueToTask(issueId) {
  showToast('Converting Issue to Maintenance Task...', 'info');
  try {
    const res = await fetch(`${API_BASE}/issues/${issueId}/convert-task`, { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      renderIssues();
    }
  } catch (e) {
    showToast('Failed to convert issue', 'error');
  }
}

// ==========================================
// 9. SUSTAINABILITY DASHBOARD VIEW
// ==========================================

async function renderSustainability() {
  const container = document.getElementById('main-content-view');
  container.innerHTML = `<div style="text-align:center; padding: 3rem;"><i class="fa-solid fa-spinner fa-spin fa-2x"></i></div>`;

  try {
    const res = await fetch(`${API_BASE}/sustainability`);
    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`Server returned HTTP ${res.status}: ${errText.substring(0, 80)}`);
    }
    const contentType = res.headers.get('content-type') || '';
    if (!contentType.includes('application/json')) {
      const rawText = await res.text();
      throw new Error(`Invalid content-type (${contentType || 'non-JSON'}).`);
    }
    const data = await res.json();
    const historyList = Array.isArray(data.history) ? data.history : [];

    container.innerHTML = `
      <div class="section-header">
        <div>
          <h2>${state.currentLang==='ta'?'வளாக சுற்றுச்சூழல் நிலைத்தன்மை & கார்பன் அளவீடு':'Campus Sustainability & Carbon Offset'}</h2>
          <p style="font-size: 0.88rem; color: var(--text-muted);">${state.currentLang==='ta'?'கார்பன் ஈர்ப்பு மற்றும் நீர் சேமிப்பு அளவீடுகள்.':'Quantified environmental impact, carbon sequestration & water savings.'}</p>
        </div>
        <button class="btn btn-secondary" onclick="window.print()"><i class="fa-solid fa-print"></i> Export Impact Report</button>
      </div>

      <div class="grid-kpi">
        <div class="card kpi-card">
          <div class="kpi-info">
            <h3>${state.currentLang==='ta'?'பராமரிக்கப்படும் மரங்கள்':'Total Trees Maintained'}</h3>
            <div class="value">${data.total_trees !== undefined ? data.total_trees : 0}</div>
            <div class="sub-text">150+ Campus Trees</div>
          </div>
          <div class="kpi-icon green"><i class="fa-solid fa-tree"></i></div>
        </div>

        <div class="card kpi-card">
          <div class="kpi-info">
            <h3>${state.currentLang==='ta'?'பல்லுயிர் சிற்றினங்கள்':'Biodiversity Species'}</h3>
            <div class="value">${data.biodiversity_count !== undefined ? data.biodiversity_count : 0}</div>
            <div class="sub-text">Flora & Bird Species</div>
          </div>
          <div class="kpi-icon amber"><i class="fa-solid fa-feather"></i></div>
        </div>
      </div>

      <div class="card">
        <h3 style="margin-bottom:1rem;"><i class="fa-solid fa-chart-area" style="color:#10b981;"></i> ${state.currentLang==='ta'?'மொத்த கார்பன் ஈர்ப்பு அளவு (kg CO2e)':'Cumulative Carbon Sequestration (kg CO2e)'}</h3>
        <canvas id="sustCarbonChart" height="220"></canvas>
      </div>
    `;

    if (typeof Chart !== 'undefined' && historyList.length > 0) {
      const el = document.getElementById('sustCarbonChart');
      if (el) {
        const ctx = el.getContext('2d');
        state.charts.sustCarbonChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: historyList.map(h => h.date),
            datasets: [{
              label: 'Carbon Offset (kg)',
              data: historyList.map(h => h.carbon_offset_kg),
              borderColor: '#10b981',
              backgroundColor: 'rgba(16, 185, 129, 0.2)',
              fill: true
            }]
          },
          options: { responsive: true }
        });
      }
    }

  } catch (err) {
    container.innerHTML = `<p style="color:red;">Error loading sustainability stats: ${err.message}</p>`;
  }
}

// ==========================================
// 10. BIODIVERSITY TRACKER VIEW
// ==========================================

async function renderBiodiversity() {
  const container = document.getElementById('main-content-view');
  container.innerHTML = `<div style="text-align:center; padding: 3rem;"><i class="fa-solid fa-spinner fa-spin fa-2x"></i></div>`;

  try {
    const res = await fetch(`${API_BASE}/biodiversity`);
    const data = await res.json();

    let logsHTML = data.logs.map(l => `
      <div class="card">
        <img src="${l.photo}" style="width:100%; height:140px; object-fit:cover; border-radius:8px; margin-bottom:0.75rem;" onerror="this.src='https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=600'">
        <div style="display:flex; justify-content:space-between; align-items:baseline;">
          <h3 style="font-size: 1.05rem; font-weight:700;">${l.species_name}</h3>
          <span class="badge badge-healthy">${l.category}</span>
        </div>
        <p style="font-size: 0.85rem; color:var(--text-muted); margin:0.4rem 0;"><i class="fa-solid fa-location-dot"></i> Zone: ${l.zone_name} | Observed: ${l.count} count</p>
        <p style="font-size: 0.8rem; font-style:italic;">"${l.notes}"</p>
      </div>
    `).join('');

    container.innerHTML = `
      <div class="section-header">
        <div>
          <h2>${state.currentLang==='ta'?'வளாக பல்லுயிர் & பறவைகள் பதிவு':'Campus Biodiversity & Sightings Log'}</h2>
          <p style="font-size: 0.88rem; color: var(--text-muted);">${state.currentLang==='ta'?'நாட்டு மரங்கள், பூக்கும் தாவரங்கள் மற்றும் பட்டாம்பூச்சிகள் கண்காணிப்பு.':'Tracking native flora, flowering shrubs, birds & pollinator butterflies.'}</p>
        </div>
      </div>

      <div class="grid-3col">
        ${logsHTML}
      </div>
    `;

  } catch (err) {
    container.innerHTML = `<p style="color:red;">Error loading biodiversity: ${err.message}</p>`;
  }
}

// ==========================================
// 11. STUDENT VOLUNTEER & REWARDS STORE VIEW
// ==========================================

async function renderVolunteers() {
  const container = document.getElementById('main-content-view');
  const dict = i18n[state.currentLang] || i18n.en;
  container.innerHTML = `<div style="text-align:center; padding: 3rem;"><i class="fa-solid fa-spinner fa-spin fa-2x"></i></div>`;

  try {
    const isTa = state.currentLang === 'ta';
    const isAdmin = isUserAdmin();
    const isStaff = isUserStaff();
    const isStudent = !isAdmin && !isStaff;
    const currentRole = getCurrentRole();

    const [actRes, leaderRes, rewardsRes, zonesRes] = await Promise.all([
      fetch(`${API_BASE}/volunteers/activities?role=${encodeURIComponent(currentRole)}`),
      fetch(`${API_BASE}/volunteers/leaderboard`),
      fetch(`${API_BASE}/rewards`),
      fetch(`${API_BASE}/zones`)
    ]);
    const activities = await actRes.json();
    const leaderboard = await leaderRes.json();
    const rewards = await rewardsRes.json();
    const zones = await zonesRes.json();
    state.zones = zones;

    let leaderHTML = leaderboard.map(user => `
      <tr>
        <td><strong>#${user.rank}</strong></td>
        <td><strong>${user.name}</strong></td>
        <td><span class="badge badge-healthy">${user.badge}</span></td>
        <td>${user.activities} activities</td>
        <td style="color:#10b981; font-weight:800;">${user.points} pts</td>
      </tr>
    `).join('');

    let rewardsHTML = rewards.map(r => `
      <div class="card" style="display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
            <i class="fa-solid ${r.icon}" style="font-size:1.6rem; color:#10b981;"></i>
            <span style="font-size:0.9rem; font-weight:800; color:#10b981; background:rgba(16,185,129,0.12); padding:0.25rem 0.6rem; border-radius:999px;">${r.cost_points} pts</span>
          </div>
          <h3 style="font-size:1rem; font-weight:700;">${r.title}</h3>
          <p style="font-size:0.8rem; color:var(--text-muted); margin:0.4rem 0;">${r.description}</p>
        </div>
        ${isStudent ? `
          <button class="btn btn-primary btn-sm" style="margin-top:1rem; width:100%; justify-content:center;" onclick="redeemRewardItem(${r.id})">
            <i class="fa-solid fa-gift"></i> ${isTa ? 'பரிசைப் பெறு' : 'Redeem Gift'}
          </button>
        ` : `
          <div style="margin-top:1rem; font-size:0.78rem; color:var(--text-muted); text-align:center;">
            <i class="fa-solid fa-store"></i> ${isTa ? 'மாணவர் பரிசு அங்காடி' : 'Student Gift Catalog'}
          </div>
        `}
      </div>
    `).join('');

    let activityHistoryRows = (Array.isArray(activities) ? activities : []).map(a => {
      const statusBadge = a.status === 'Approved' ? 'badge-healthy' : a.status === 'Rejected' ? 'badge-critical' : 'badge-attention';
      const statusText = isTa ? (a.status === 'Approved' ? 'ஒப்புதல் அளிக்கப்பட்டது' : a.status === 'Rejected' ? 'நிராகரிக்கப்பட்டது' : 'சரிபார்ப்பு நிலுவையில்') : a.status;
      const ptsDisplay = a.status === 'Approved' ? `<strong style="color:#10b981;">+${a.points} pts</strong>` : `<span style="color:var(--text-muted);">0 pts</span>`;
      return `
        <tr>
          <td><strong>#${a.id}</strong></td>
          <td><strong>${a.title}</strong></td>
          <td>${a.volunteer_name}</td>
          <td><span style="font-size:0.8rem; font-weight:600; color:var(--primary-700);">🌱 ${a.detected_plant || 'Plant Classified'}</span></td>
          <td>${a.date}</td>
          <td><span class="badge ${statusBadge}">${statusText}</span></td>
          <td>${ptsDisplay}</td>
        </tr>
      `;
    }).join('');

    if (isStudent) {
      // ==========================================
      // STUDENT DASHBOARD UI
      // ==========================================
      container.innerHTML = `
        <div class="section-header">
          <div>
            <h2>${isTa ? 'மாணவர் தன்னார்வலர் மையம் & பரிசுகள் அங்காடி' : 'Student Green Volunteers & Rewards Store'}</h2>
            <p style="font-size: 0.88rem; color: var(--text-muted);">${isTa ? 'புள்ளிகள் பெறுங்கள், சுற்றுச்சூழல் பதக்கங்கள் வெல்லுங்கள்.' : 'Earn points, unlock eco badges & redeem green prizes.'}</p>
          </div>
          <button class="btn btn-primary" onclick="openModal('volunteer-modal')"><i class="fa-solid fa-award"></i> ${isTa ? 'செயல்பாட்டுச் சான்றை சமர்ப்பி' : 'Submit Activity Proof'}</button>
        </div>

        <div class="grid-2col" style="margin-bottom:2rem;">
          <div class="card">
            <h3 style="margin-bottom:1rem;"><i class="fa-solid fa-trophy" style="color:#f59e0b;"></i> ${isTa ? 'மாதாந்திர தரவரிசைப் பட்டியல்' : 'Monthly Eco Leaderboard'}</h3>
            <div class="table-container">
              <table class="custom-table">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Student</th>
                    <th>Badge Level</th>
                    <th>Activities</th>
                    <th>Points</th>
                  </tr>
                </thead>
                <tbody>
                  ${leaderHTML}
                </tbody>
              </table>
            </div>
          </div>

          <div>
            <h3 style="margin-bottom:1rem;"><i class="fa-solid fa-store" style="color:#10b981;"></i> ${isTa ? 'பசுமை பரிசுகள் அங்காடி' : 'Green Rewards Store'}</h3>
            <div class="grid-2col" style="gap:1rem;">
              ${rewardsHTML}
            </div>
          </div>
        </div>

        <!-- Student Submissions Table -->
        <div class="card">
          <h3 style="margin-bottom:1rem;"><i class="fa-solid fa-list-check" style="color:#3b82f6;"></i> ${isTa ? 'எனது செயல்பாட்டுச் சான்றுகள் & சரிபார்ப்பு நிலை' : 'My Submitted Activity Proofs & Status'}</h3>
          <div class="table-container">
            <table class="custom-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Activity Title</th>
                  <th>Student Volunteer</th>
                  <th>AI Detected Plant</th>
                  <th>Date</th>
                  <th>Verification Status</th>
                  <th>Points Awarded</th>
                </tr>
              </thead>
              <tbody>
                ${activityHistoryRows.length > 0 ? activityHistoryRows : `<tr><td colspan="7" style="text-align:center; color:var(--text-muted); padding:1.5rem;">${isTa ? 'சமர்ப்பித்த செயல்பாடுகள் எதுவுமில்லை.' : 'No activity submissions found. Click "Submit Activity Proof" to submit.'}</td></tr>`}
              </tbody>
            </table>
          </div>
        </div>
      `;
    } else {
      // ==========================================
      // STAFF / ADMIN DASHBOARD UI
      // ==========================================
      const pendingRes = await fetch(`${API_BASE}/volunteers/pending-verifications?role=${encodeURIComponent(currentRole)}`);
      const pendingItems = pendingRes.ok ? await pendingRes.json() : [];

      let pendingQueueHTML = pendingItems.map(p => `
        <div class="card" style="border-left:4px solid #f59e0b; margin-bottom:1rem;">
          <div style="display:flex; gap:1rem; align-items:center; flex-wrap:wrap;">
            <img src="${p.proof_photo || 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=600'}" style="width:90px; height:80px; object-fit:cover; border-radius:8px;" onerror="this.src='https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=600'">
            <div style="flex:1; min-width:200px;">
              <div style="display:flex; justify-content:space-between; align-items:baseline; flex-wrap:wrap; gap:0.5rem;">
                <h4 style="margin:0; font-size:1.05rem; font-weight:700;">${p.title}</h4>
                <span class="badge badge-attention"><i class="fa-solid fa-clock-rotate-left"></i> ${isTa ? 'சரிபார்ப்பு நிலுவையில்' : 'Pending Verification'}</span>
              </div>
              <p style="font-size:0.85rem; margin:0.3rem 0; color:var(--text-primary);">
                👤 <strong>${p.volunteer_name}</strong> (Student ID #${p.volunteer_id || 4}) | 📅 ${p.date}
              </p>
              <p style="font-size:0.82rem; margin:0.2rem 0; color:var(--primary-800); font-weight:600;">
                🤖 <strong>${isTa ? 'AI கண்டறிந்த தாவரம்:' : 'AI Detected Plant:'}</strong> ${p.detected_plant || 'Plant Species Classified'}
              </p>
              <p style="font-size:0.8rem; color:var(--text-muted); font-style:italic; margin:0.2rem 0;">"${p.description}"</p>
            </div>
            <div style="display:flex; flex-direction:column; gap:0.4rem;">
              <button class="btn btn-success btn-sm" onclick="verifyStudentSubmission(${p.id}, 'approve')">
                <i class="fa-solid fa-check"></i> ${isTa ? 'ஒப்புதல் அளி' : 'Approve & Award Points'}
              </button>
              <button class="btn btn-danger btn-sm" onclick="verifyStudentSubmission(${p.id}, 'reject')">
                <i class="fa-solid fa-xmark"></i> ${isTa ? 'நிராகரி' : 'Reject (0 Points)'}
              </button>
            </div>
          </div>
        </div>
      `).join('');

      container.innerHTML = `
        <div class="section-header">
          <div>
            <h2>${isTa ? 'மாணவர் பரிசு சரிபார்ப்பு & ஆய்வு வரிசை' : 'Student Reward Verification & Audit Queue'}</h2>
            <p style="font-size: 0.88rem; color: var(--text-muted);">${isTa ? 'புள்ளிகள் வழங்குவதற்கு முன் ஊழியர்/நிர்வாகி கட்டாய சரிபார்ப்பு பணிப்பகுதி.' : 'Staff & Admin verification workspace for student reward activity submissions.'}</p>
          </div>
          <div style="font-size:0.85rem; font-weight:600; color:var(--primary-800); background:rgba(16,185,129,0.1); padding:0.4rem 0.8rem; border-radius:6px;">
            <i class="fa-solid fa-user-shield"></i> ${isAdmin ? 'Admin Reviewer' : 'Staff Reviewer'} Mode
          </div>
        </div>

        <!-- Pending Reward Verification Queue Card -->
        <div class="card" style="margin-bottom:2rem; background:rgba(245, 158, 11, 0.05); border:1px solid rgba(245, 158, 11, 0.3);">
          <h3 style="margin-bottom:0.5rem; color:#b45309;"><i class="fa-solid fa-shield-halved" style="color:#f59e0b;"></i> ${isTa ? 'நிலுவையில் உள்ள பரிசு சரிபார்ப்பு வரிசை' : 'Pending Reward Verification Queue'}</h3>
          <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:1rem;">
            ${isTa ? 'புள்ளிகள் வழங்குவதற்கு முன் ஊழியர்/நிர்வாகி கட்டாய சரிபார்ப்பு.' : 'Mandatory Staff/Admin anti-cheating review before reward points are credited.'} (${pendingItems.length} ${isTa ? 'நிலுவையில்' : 'Pending Submissions'})
          </p>
          ${pendingItems.length > 0 ? pendingQueueHTML : `<p style="font-size:0.85rem; color:var(--text-muted); font-style:italic;"><i class="fa-solid fa-circle-check" style="color:#10b981;"></i> ${isTa ? 'நிலுவையில் உள்ள சரிபார்ப்புகள் எதுவும் இல்லை.' : 'All student submissions verified! No pending verifications in queue.'}</p>`}
        </div>

        <div class="grid-2col" style="margin-bottom:2rem;">
          <div class="card">
            <h3 style="margin-bottom:1rem;"><i class="fa-solid fa-trophy" style="color:#f59e0b;"></i> ${isTa ? 'மாதாந்திர தரவரிசைப் பட்டியல்' : 'Monthly Eco Leaderboard'}</h3>
            <div class="table-container">
              <table class="custom-table">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Student</th>
                    <th>Badge Level</th>
                    <th>Activities</th>
                    <th>Points</th>
                  </tr>
                </thead>
                <tbody>
                  ${leaderHTML}
                </tbody>
              </table>
            </div>
          </div>

          <div>
            <h3 style="margin-bottom:1rem;"><i class="fa-solid fa-store" style="color:#10b981;"></i> ${isTa ? 'பசுமை பரிசுகள் அங்காடி' : 'Green Rewards Store'}</h3>
            <div class="grid-2col" style="gap:1rem;">
              ${rewardsHTML}
            </div>
          </div>
        </div>

        <!-- All Submissions Audit History Table -->
        <div class="card">
          <h3 style="margin-bottom:1rem;"><i class="fa-solid fa-list-check" style="color:#3b82f6;"></i> ${isTa ? 'அனைத்து மாணவர் சமர்ப்பிப்புகள் & சரிபார்ப்பு வரலாறு' : 'All Student Submissions & Verification Audit History'}</h3>
          <div class="table-container">
            <table class="custom-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Activity Title</th>
                  <th>Student Volunteer</th>
                  <th>AI Detected Plant</th>
                  <th>Date</th>
                  <th>Verification Status</th>
                  <th>Points Awarded</th>
                </tr>
              </thead>
              <tbody>
                ${activityHistoryRows.length > 0 ? activityHistoryRows : `<tr><td colspan="7" style="text-align:center; color:var(--text-muted); padding:1.5rem;">${isTa ? 'சமர்ப்பித்த செயல்பாடுகள் எதுவுமில்லை.' : 'No activity submissions recorded.'}</td></tr>`}
              </tbody>
            </table>
          </div>
        </div>
      `;
    }

    const vZoneInput = document.getElementById('vol-zone-input');
    if (vZoneInput) vZoneInput.innerHTML = zones.map(z => `<option value="${z.id}">${z.name}</option>`).join('');

  } catch (err) {
    container.innerHTML = `<p style="color:red;">Error loading volunteer hub: ${err.message}</p>`;
  }
}

async function verifyStudentSubmission(activityId, action) {
  const verifierName = state.currentUser ? state.currentUser.name : (isUserAdmin() ? 'Dr. Eleanor Vance (Admin)' : 'Rajesh Kumar (Staff)');
  const currentRole = getCurrentRole();
  showToast(action === 'approve' ? 'Approving submission & awarding points...' : 'Rejecting submission...', 'info');

  try {
    const res = await fetch(`${API_BASE}/volunteers/verify/${activityId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: action, verified_by: verifierName, points: 50, role: currentRole })
    });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      renderVolunteers();
      if (typeof updateUnreadNotifBadge === 'function') updateUnreadNotifBadge();
    } else {
      showToast(data.error || data.message || 'Verification failed', 'error');
    }
  } catch (e) {
    showToast('Verification request failed', 'error');
  }
}

async function redeemRewardItem(rewardId) {
  const volunteerName = state.currentUser ? state.currentUser.name : 'Aarav Sharma';
  showToast('Processing Gift Redemption...', 'info');
  try {
    const res = await fetch(`${API_BASE}/rewards/redeem`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ volunteer_name: volunteerName, reward_id: rewardId })
    });
    const data = await res.json();
    if (data.success) {
      alert(`🎉 ${data.message}`);
      renderVolunteers();
    } else {
      showToast(data.message, 'error');
    }
  } catch (e) {
    showToast('Redemption error', 'error');
  }
}

// ==========================================
// 12. ADMIN STUDENT & STAFF USER MANAGEMENT VIEW
// ==========================================

async function renderUserManagement() {
  const container = document.getElementById('main-content-view');
  container.innerHTML = `<div style="text-align:center; padding: 3rem;"><i class="fa-solid fa-spinner fa-spin fa-2x"></i></div>`;

  try {
    const res = await fetch(`${API_BASE}/admin/users`);
    const users = await res.json();

    let userRowsHTML = users.map(u => {
      const badgeClass = u.role === 'Admin' ? 'badge-critical' : u.role === 'Gardening Staff' ? 'badge-attention' : 'badge-healthy';
      return `
        <tr>
          <td><strong>#${u.id}</strong></td>
          <td><strong>${u.name}</strong></td>
          <td>${u.email}</td>
          <td><span class="badge ${badgeClass}">${u.role}</span></td>
          <td>
            ${u.email.includes('smartcampus.com') ? '<span style="font-size:0.75rem; color:var(--text-muted);">System Demo Account</span>' : `<button class="btn btn-danger btn-sm" onclick="deleteUserAccount(${u.id})"><i class="fa-solid fa-trash"></i> Delete</button>`}
          </td>
        </tr>
      `;
    }).join('');

    container.innerHTML = `
      <div class="section-header">
        <div>
          <h2><i class="fa-solid fa-users-gear" style="color:#10b981;"></i> Student & Staff User Management</h2>
          <p style="font-size: 0.88rem; color: var(--text-muted);">Admin control portal for managing campus green volunteers and gardening staff credentials.</p>
        </div>
      </div>

      <div class="card">
        <div class="table-container">
          <table class="custom-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email Address</th>
                <th>Authorized Role</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              ${userRowsHTML}
            </tbody>
          </table>
        </div>
      </div>
    `;
  } catch (err) {
    container.innerHTML = `<p style="color:red;">Error loading users: ${err.message}</p>`;
  }
}

async function deleteUserAccount(userId) {
  if (!confirm('Are you sure you want to delete this user account?')) return;
  try {
    const res = await fetch(`${API_BASE}/admin/users/${userId}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      renderUserManagement();
    }
  } catch (e) {
    showToast('Failed to delete user', 'error');
  }
}

// ==========================================
// 13. NOTIFICATIONS VIEW
// ==========================================

async function renderNotifications() {
  const container = document.getElementById('main-content-view');
  container.innerHTML = `<div style="text-align:center; padding: 3rem;"><i class="fa-solid fa-spinner fa-spin fa-2x"></i></div>`;

  try {
    const res = await fetch(`${API_BASE}/notifications`);
    const data = await res.json();

    let notifHTML = data.notifications.map(n => {
      const typeColor = n.type === 'Critical' ? '#f43f5e' : n.type === 'Warning' ? '#f59e0b' : '#3b82f6';
      return `
        <div class="card" style="border-left: 4px solid ${typeColor}; margin-bottom: 0.75rem;">
          <div style="display:flex; justify-content:space-between;">
            <strong style="color: ${typeColor};">${n.type} Alert</strong>
            <span style="font-size: 0.75rem; color:var(--text-muted);">${n.created_at}</span>
          </div>
          <p style="font-size: 0.9rem; margin-top: 0.4rem;">${n.message}</p>
        </div>
      `;
    }).join('');

    container.innerHTML = `
      <div class="section-header">
        <div>
          <h2>${state.currentLang==='ta'?'அறிவிப்புகள் மையம்':'System Notifications & Alerts'}</h2>
          <p style="font-size: 0.88rem; color: var(--text-muted);">${state.currentLang==='ta'?'நேரலை IoT எச்சரிக்கைகள் மற்றும் பராமரிப்பு தகவல்கள்.':'Real-time IoT warnings, critical plant status updates & task alerts.'}</p>
        </div>
        <button class="btn btn-secondary" onclick="markAllNotifsRead()"><i class="fa-solid fa-check-double"></i> Mark All as Read</button>
      </div>

      <div style="max-width: 800px;">
        ${notifHTML || '<p>No notifications.</p>'}
      </div>
    `;

  } catch (err) {
    container.innerHTML = `<p style="color:red;">Error loading notifications: ${err.message}</p>`;
  }
}

async function fetchNotifications() {
  try {
    const res = await fetch(`${API_BASE}/notifications`);
    const data = await res.json();
    state.unreadNotifs = data.unread_count;
    const badge = document.getElementById('unread-notif-badge');
    if (badge) badge.textContent = state.unreadNotifs;
  } catch (e) {}
}

async function markAllNotifsRead() {
  await fetch(`${API_BASE}/notifications/read-all`, { method: 'POST' });
  fetchNotifications();
  renderNotifications();
}

// ==========================================
// 14. SETTINGS & SYSTEM RESET VIEW
// ==========================================

async function renderSettings() {
  const container = document.getElementById('main-content-view');
  
  container.innerHTML = `
    <div class="section-header">
      <div>
        <h2>${state.currentLang==='ta'?'அமைப்புகள் & சிஸ்டம் விபரம்':'System Settings & Config'}</h2>
        <p style="font-size: 0.88rem; color: var(--text-muted);">${state.currentLang==='ta'?'தானியங்கி பணி அட்டவணை இடைவெளி மற்றும் தரவுத்தள மறுஅமைவு.':'Scheduler frequency settings, REST API endpoints & demo data reset.'}</p>
      </div>
    </div>

    <div class="grid-2col">
      <div class="card">
        <h3><i class="fa-solid fa-clock-rotate-left" style="color:#10b981;"></i> ${state.currentLang==='ta'?'தானியங்கி பணி உருவாக்க இடைவெளி':'Auto-Task Scheduler Frequency'}</h3>
        <p style="font-size:0.85rem; color:var(--text-muted); margin: 0.5rem 0 1rem;">Configure recurring frequency days for automated maintenance task generation.</p>
        
        <div style="display:flex; flex-direction:column; gap:1rem;">
          <div>
            <label style="font-size:0.85rem; font-weight:600;">Watering Task Frequency (Days)</label>
            <input type="number" class="input-search" value="1" readonly style="width:100%; margin-top:0.3rem;">
          </div>
          <div>
            <label style="font-size:0.85rem; font-weight:600;">Weekly Inspection Frequency (Days)</label>
            <input type="number" class="input-search" value="7" readonly style="width:100%; margin-top:0.3rem;">
          </div>
          <div>
            <label style="font-size:0.85rem; font-weight:600;">Pruning Frequency (Days)</label>
            <input type="number" class="input-search" value="30" readonly style="width:100%; margin-top:0.3rem;">
          </div>
        </div>
      </div>

      <div class="card">
        <h3><i class="fa-solid fa-database" style="color:#f43f5e;"></i> ${state.currentLang==='ta'?'தரவுத்தள மறுஅமைவு (Reset)':'Reset System Demo Data'}</h3>
        <p style="font-size:0.85rem; color:var(--text-muted); margin: 0.5rem 0 1.5rem;">Instantly re-seed the SQLite database with full realistic campus demo data (zones, plants, tasks, telemetry).</p>
        
        <button class="btn btn-danger" onclick="resetDemoSystemData()"><i class="fa-solid fa-rotate"></i> ${state.currentLang==='ta'?'தரவுத்தளத்தை மறுஅமை செய்':'Reset Database to Demo State'}</button>
      </div>
    </div>
  `;
}

async function resetDemoSystemData() {
  if (!confirm('Re-seed the entire database to fresh demo state?')) return;
  showToast('Re-seeding database...', 'info');
  try {
    const res = await fetch(`${API_BASE}/system/reset-demo`, { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      switchView('dashboard');
    }
  } catch (err) {
    showToast('Failed to reset database', 'error');
  }
}

// ==========================================
// AI CHATBOT HANDLERS
// ==========================================

function toggleChatbot() {
  const win = document.getElementById('chatbot-window');
  if (win) win.classList.toggle('active');
}

function handleChatEnter(e) {
  if (e.key === 'Enter') {
    sendChatMessage();
  }
}

function sendChatPill(text) {
  document.getElementById('chat-input-text').value = text;
  sendChatMessage();
}

async function sendChatMessage() {
  const input = document.getElementById('chat-input-text');
  const msg = input.value.trim();
  if (!msg) return;

  const msgsContainer = document.getElementById('chatbot-messages');
  msgsContainer.innerHTML += `<div class="chat-msg user">${msg}</div>`;
  input.value = '';
  msgsContainer.scrollTop = msgsContainer.scrollHeight;

  try {
    const res = await fetch(`${API_BASE}/ai/chatbot`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg })
    });
    const data = await res.json();
    msgsContainer.innerHTML += `<div class="chat-msg bot">${data.reply.replace(/\n/g, '<br>')}</div>`;
    msgsContainer.scrollTop = msgsContainer.scrollHeight;
  } catch (e) {
    msgsContainer.innerHTML += `<div class="chat-msg bot">Error connecting to FloraAI backend.</div>`;
  }
}

// ==========================================
// MODAL HELPERS & ACTION FUNCTIONS
// ==========================================

function openAddZoneModal() {
  document.getElementById('zone-modal-title').textContent = state.currentLang==='ta' ? 'புதிய மண்டலம் சேர்க்க' : 'Add New Campus Zone';
  document.getElementById('zone-id-input').value = '';
  document.getElementById('zone-form').reset();
  openModal('zone-modal');
}

function openEditZoneModal(zoneId) {
  const z = state.zones.find(item => item.id === zoneId);
  if (!z) return;
  document.getElementById('zone-modal-title').textContent = state.currentLang==='ta' ? 'மண்டலம் திருத்த' : 'Edit Zone Details';
  document.getElementById('zone-id-input').value = z.id;
  document.getElementById('zone-name-input').value = z.name;
  document.getElementById('zone-location-input').value = z.location;
  document.getElementById('zone-area-input').value = z.area;
  document.getElementById('zone-green-input').value = z.green_cover_percentage;
  document.getElementById('zone-health-input').value = z.health_status;
  openModal('zone-modal');
}

async function deleteZone(zoneId) {
  if (!confirm('Delete this campus zone?')) return;
  const res = await fetch(`${API_BASE}/zones/${zoneId}`, { method: 'DELETE' });
  const data = await res.json();
  if (data.success) {
    showToast(data.message, 'success');
    renderZones();
  }
}

function openAddPlantModal() {
  document.getElementById('plant-modal-title').textContent = state.currentLang==='ta' ? 'புதிய தாவரம் சேர்க்க' : 'Add New Plant to Inventory';
  document.getElementById('plant-id-input').value = '';
  document.getElementById('plant-form').reset();
  openModal('plant-modal');
}

function openEditPlantModal(plantId) {
  const p = state.plants.find(item => item.id === plantId);
  if (!p) return;
  document.getElementById('plant-modal-title').textContent = state.currentLang==='ta' ? 'தாவர விபரம் திருத்த' : 'Edit Plant Details';
  document.getElementById('plant-id-input').value = p.id;
  document.getElementById('plant-name-input').value = p.name;
  document.getElementById('plant-species-input').value = p.species;
  document.getElementById('plant-type-input').value = p.type;
  document.getElementById('plant-zone-input').value = p.zone_id;
  document.getElementById('plant-date-input').value = p.planted_date;
  document.getElementById('plant-health-input').value = p.health_status;
  document.getElementById('plant-photo-input').value = p.photo;
  document.getElementById('plant-notes-input').value = p.notes;
  openModal('plant-modal');
}

async function deletePlant(plantId) {
  if (!confirm('Delete this plant record?')) return;
  const res = await fetch(`${API_BASE}/plants/${plantId}`, { method: 'DELETE' });
  const data = await res.json();
  if (data.success) {
    showToast(data.message, 'success');
    renderPlants();
  }
}

function openAddTaskModal() {
  document.getElementById('task-form').reset();
  openModal('task-modal');
}

function openCompleteTaskModal(taskId) {
  document.getElementById('complete-task-id-input').value = taskId;
  document.getElementById('complete-task-notes').value = '';
  openModal('complete-task-modal');
}

function openHealthModal(plantId) {
  const p = state.plants.find(item => item.id === plantId);
  if (!p) return;
  document.getElementById('health-plant-id').value = p.id;
  document.getElementById('health-plant-name').value = `${p.plant_code} - ${p.name}`;
  document.getElementById('health-status-select').value = p.health_status;
  document.getElementById('health-observation-text').value = p.notes || '';
  openModal('health-modal');
}

function filterPlants() {
  const query = (document.getElementById('plant-search-input')?.value || '').toLowerCase();
  const zoneFilter = document.getElementById('plant-zone-filter')?.value || 'all';
  const healthFilter = document.getElementById('plant-health-filter')?.value || 'all';

  const cards = document.querySelectorAll('#plants-grid-container .plant-card');
  cards.forEach((card, idx) => {
    const p = state.plants[idx];
    if (!p) return;
    const matchesQuery = p.name.toLowerCase().includes(query) || p.species.toLowerCase().includes(query) || p.plant_code.toLowerCase().includes(query);
    const matchesZone = zoneFilter === 'all' || p.zone_id.toString() === zoneFilter;
    const matchesHealth = healthFilter === 'all' || p.health_status === healthFilter;

    if (matchesQuery && matchesZone && matchesHealth) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}

// ==========================================
// FORM SUBMISSION HANDLERS & MODALS
// ==========================================

function setupFormSubmissions() {
  const issueForm = document.getElementById('issue-form');
  if (issueForm) {
    issueForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const body = {
        title: document.getElementById('issue-title-input').value,
        reporter_name: state.currentUser ? state.currentUser.name : document.getElementById('issue-reporter-input').value,
        zone_id: parseInt(document.getElementById('issue-zone-input').value),
        issue_type: document.getElementById('issue-type-input').value,
        priority: document.getElementById('issue-priority-input').value,
        description: document.getElementById('issue-desc-input').value,
        photo: document.getElementById('issue-photo-input').value
      };

      const res = await fetch(`${API_BASE}/issues`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await res.json();
      if (data.success) {
        showToast(data.message, 'success');
        closeModal('issue-modal');
        switchView('issues');
      }
    });
  }

  const zoneForm = document.getElementById('zone-form');
  if (zoneForm) {
    zoneForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const id = document.getElementById('zone-id-input').value;
      const body = {
        name: document.getElementById('zone-name-input').value,
        location: document.getElementById('zone-location-input').value,
        area: parseFloat(document.getElementById('zone-area-input').value),
        green_cover_percentage: parseFloat(document.getElementById('zone-green-input').value),
        health_status: document.getElementById('zone-health-input').value
      };

      const method = id ? 'PUT' : 'POST';
      const url = id ? `${API_BASE}/zones/${id}` : `${API_BASE}/zones`;

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await res.json();
      if (data.success) {
        showToast(data.message, 'success');
        closeModal('zone-modal');
        renderZones();
      }
    });
  }

  const plantForm = document.getElementById('plant-form');
  if (plantForm) {
    plantForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const id = document.getElementById('plant-id-input').value;
      const body = {
        name: document.getElementById('plant-name-input').value,
        species: document.getElementById('plant-species-input').value,
        type: document.getElementById('plant-type-input').value,
        zone_id: parseInt(document.getElementById('plant-zone-input').value),
        planted_date: document.getElementById('plant-date-input').value,
        health_status: document.getElementById('plant-health-input').value,
        photo: document.getElementById('plant-photo-input').value || 'https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=600',
        notes: document.getElementById('plant-notes-input').value
      };

      const method = id ? 'PUT' : 'POST';
      const url = id ? `${API_BASE}/plants/${id}` : `${API_BASE}/plants`;

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await res.json();
      if (data.success) {
        showToast(data.message, 'success');
        closeModal('plant-modal');
        renderPlants();
      }
    });
  }

  const taskForm = document.getElementById('task-form');
  if (taskForm) {
    taskForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const plantId = document.getElementById('task-plant-input').value;
      const body = {
        task_type: document.getElementById('task-type-input').value,
        zone_id: parseInt(document.getElementById('task-zone-input').value),
        plant_id: plantId ? parseInt(plantId) : null,
        assigned_to: document.getElementById('task-staff-input').value,
        priority: document.getElementById('task-priority-input').value,
        scheduled_date: document.getElementById('task-date-input').value,
        notes: document.getElementById('task-notes-input').value,
        created_by: state.currentUser ? state.currentUser.name : state.currentRole
      };

      const res = await fetch(`${API_BASE}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await res.json();
      if (data.success) {
        showToast(data.message, 'success');
        closeModal('task-modal');
        renderMaintenance();
      }
    });
  }

  const completeTaskForm = document.getElementById('complete-task-form');
  if (completeTaskForm) {
    completeTaskForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const taskId = document.getElementById('complete-task-id-input').value;
      const body = {
        notes: document.getElementById('complete-task-notes').value,
        photo_proof: document.getElementById('complete-task-photo').value
      };

      const res = await fetch(`${API_BASE}/tasks/${taskId}/complete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await res.json();
      if (data.success) {
        showToast(data.message, 'success');
        closeModal('complete-task-modal');
        renderMaintenance();
      }
    });
  }

  const healthForm = document.getElementById('health-form');
  if (healthForm) {
    healthForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const plantId = document.getElementById('health-plant-id').value;
      const body = {
        health_status: document.getElementById('health-status-select').value,
        observation: document.getElementById('health-observation-text').value
      };

      const res = await fetch(`${API_BASE}/plants/${plantId}/health`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await res.json();
      if (data.success) {
        showToast(data.message, 'success');
        closeModal('health-modal');
        renderHealth();
      }
    });
  }

  const volunteerForm = document.getElementById('volunteer-form');
  if (volunteerForm) {
    volunteerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const body = {
        title: document.getElementById('vol-title-input').value,
        volunteer_name: state.currentUser ? state.currentUser.name : document.getElementById('vol-name-input').value,
        volunteer_id: state.currentUser ? state.currentUser.id : 4,
        zone_id: parseInt(document.getElementById('vol-zone-input').value),
        points: parseInt(document.getElementById('vol-points-input').value),
        description: document.getElementById('vol-desc-input').value,
        proof_photo: document.getElementById('vol-photo-input').value,
        role: getCurrentRole()
      };

      const res = await fetch(`${API_BASE}/volunteers/claim`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await res.json();
      if (data.success) {
        showToast(data.message, 'success');
        closeModal('volunteer-modal');
        renderVolunteers();
      } else {
        showToast(data.error || data.message || 'Submission failed', 'error');
      }
    });
  }
}

function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.classList.add('active');
}

function closeModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.remove('active');
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<i class="fa-solid fa-circle-info"></i> <span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 4000);
}

// ==========================================================================
// SMART PLANT REPLACEMENT & VERIFIED PLANT CATALOG ENGINE
// ==========================================================================

const PLANT_IMAGE_CATALOG = {
  "Golden Tabebuia": "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=600",
  "Neem Tree": "https://images.unsplash.com/photo-1600411833196-7c1f6b1a8b90?w=600",
  "Bougainvillea": "https://images.unsplash.com/photo-1596727147705-61a532a659bd?w=600",
  "Royal Palm": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=600",
  "Jacaranda": "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?w=600",
  "Korean Velvet Grass": "https://images.unsplash.com/photo-1584467735871-8e85353a8413?w=600",
  "Gulmohar": "https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=600",
  "Aloe Vera": "https://images.unsplash.com/photo-1596547609652-9cf5d8d76921?w=600",
  "Ashoka Tree": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=600",
  "Frangipani": "https://images.unsplash.com/photo-1534067783941-51c9c23ecefd?w=600",
  "Plumeria": "https://images.unsplash.com/photo-1534067783941-51c9c23ecefd?w=600",
  "Banyan Tree": "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=600",
  "Snake Plant": "https://images.unsplash.com/photo-1599598425947-0206455429d5?w=600",
  "Hibiscus": "https://images.unsplash.com/photo-1566835265538-4e56eb600867?w=600",
  "Holy Basil": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=600",
  "Tulsi": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=600",
  "Bamboo": "https://images.unsplash.com/photo-1516205651411-aef33a44f7c2?w=600",
  "Ficus": "https://images.unsplash.com/photo-1512428559087-560fa5ceab42?w=600",
  "Areca Palm": "https://images.unsplash.com/photo-1598880940371-c756e015fea1?w=600",
  "Jasmine": "https://images.unsplash.com/photo-1508610048659-a06b669e3321?w=600",
  "Copperpod": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600",
  "Mint": "https://images.unsplash.com/photo-1603569283847-be29b8b3bf1d?w=600",
  "Lemongrass": "https://images.unsplash.com/photo-1603569283847-be29b8b3bf1d?w=600",
  "Rose": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600",
  "Mango": "https://images.unsplash.com/photo-1553279768-865429fa0078?w=600"
};

function getVerifiedPlantImage(name, species, currentPhoto) {
  const text = ((name || "") + " " + (species || "")).toLowerCase();
  for (const [key, verifiedUrl] of Object.entries(PLANT_IMAGE_CATALOG)) {
    if (text.includes(key.toLowerCase())) {
      return verifiedUrl;
    }
  }
  if (currentPhoto && !currentPhoto.includes('photo-1517849845537-4d257902454a') && !currentPhoto.includes('photo-1506744038136-46273834b3fb')) {
    return currentPhoto;
  }
  return "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=600";
}

function getCurrentRole() {
  if (state.currentUser && state.currentUser.role) return state.currentUser.role;
  return state.currentRole || 'Student';
}

function isUserAdmin() {
  const r = getCurrentRole();
  return r === 'Admin';
}

function isUserStaff() {
  const r = getCurrentRole();
  return r === 'Gardening Staff' || r === 'Staff' || r === 'Staff / Gardener';
}

async function openReplacementModal(plantId) {
  openModal('replacement-modal');
  const envCard = document.getElementById('replacement-env-analysis-card');
  const candContainer = document.getElementById('replacement-candidates-container');

  if (envCard) envCard.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing soil & environmental telemetry...`;
  if (candContainer) candContainer.innerHTML = `<i class="fa-solid fa-spinner fa-spin fa-2x"></i>`;

  try {
    const res = await fetch(`${API_BASE}/plants/replacement-recommendations?plant_id=${plantId}`);
    const data = await res.json();
    const loc = data.location_analysis;
    const recs = data.recommendations || [];
    const oldP = data.old_plant || {};

    const isTa = state.currentLang === 'ta';
    const isAdmin = isUserAdmin();
    const isStaff = isUserStaff();
    console.log('DEBUG openReplacementModal:', { isAdmin, isStaff, role: getCurrentRole(), currentUser: state.currentUser });

    if (envCard) {
      envCard.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.5rem; flex-wrap:wrap; gap:0.5rem;">
          <h4 style="margin:0; font-size:1rem; font-weight:700; color:var(--primary-800);">
            <i class="fa-solid fa-chart-simple"></i> ${isTa ? 'மண்டல சுற்றுச்சூழல் ஆய்வு' : 'Location Soil & Environmental Analysis'}: ${loc.zone_name}
          </h4>
          <span style="font-size:0.8rem; font-weight:600; color:var(--text-muted);">
            ${isTa ? 'அகற்றப்படும் தாவரம்:' : 'Removing:'} <strong>${oldP.name || 'Plant'}</strong> (${oldP.plant_code || ''})
          </span>
        </div>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 0.6rem; font-size: 0.82rem;">
          <div class="env-pill">🪴 <strong>${isTa ? 'மண் வகை:' : 'Soil Type:'}</strong> ${loc.soil_type}</div>
          <div class="env-pill">🧪 <strong>${isTa ? 'மண் pH:' : 'Soil pH:'}</strong> ${loc.ph_level}</div>
          <div class="env-pill">💧 <strong>${isTa ? 'ஈரப்பதம்:' : 'Moisture:'}</strong> ${loc.moisture}</div>
          <div class="env-pill">☀️ <strong>${isTa ? 'சூரிய ஒளி:' : 'Sunlight:'}</strong> ${loc.sunlight}</div>
          <div class="env-pill">🌡️ <strong>Temperature:</strong> ${loc.temperature}</div>
          <div class="env-pill">🚰 <strong>Watering:</strong> ${loc.water_source}</div>
        </div>
      `;
    }

    if (candContainer) {
      candContainer.innerHTML = recs.map(c => {
        const verifiedPhoto = getVerifiedPlantImage(c.name, c.species, c.photo);
        return `
          <div class="rec-candidate-card">
            <img src="${verifiedPhoto}" class="rec-plant-img" alt="${c.name}">
            <div style="flex:1;">
              <div style="display:flex; justify-content:space-between; align-items:baseline; flex-wrap:wrap; gap:0.4rem;">
                <h4 style="font-weight:700; font-size:1.05rem; margin:0; color:var(--text-primary);">${c.name} <span style="font-size:0.82rem; font-style:italic; color:var(--text-muted);">(${c.species})</span></h4>
                <span class="match-score-badge"><i class="fa-solid fa-circle-check"></i> ${c.compatibility_score}% ${isTa ? 'பொருத்தம்' : 'Match'}</span>
              </div>
              <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin-top:0.45rem;">
                <span class="env-pill">🪴 ${isTa ? 'மண்:' : 'Soil:'} ${c.ideal_soil}</span>
                <span class="env-pill">☀️ ${isTa ? 'சூரிய ஒளி:' : 'Sun:'} ${c.ideal_sunlight}</span>
                <span class="env-pill">💧 ${isTa ? 'நீர் தேவை:' : 'Water:'} ${c.water_req}</span>
                <span class="env-pill">✂️ ${isTa ? 'பராமரிப்பு:' : 'Maint:'} ${c.maintenance_level}</span>
              </div>
              <div class="why-plant-box">
                <strong>💡 ${isTa ? 'ஏன் இந்த தாவரம்?' : 'Why this plant?'}</strong> ${c.why_explanation}
              </div>
            </div>
            <div style="display:flex; align-items:center; align-self:center;">
              ${(isAdmin || isStaff) ? `
                <button class="btn btn-primary btn-sm" onclick="confirmPlantReplacement(${c.id}, ${plantId})">
                  <i class="fa-solid fa-check"></i> ${isTa ? 'மாற்று செய்க' : 'Confirm'}
                </button>
              ` : `
                <button class="btn btn-secondary btn-sm" disabled title="Student view only">
                  <i class="fa-solid fa-eye"></i> ${isTa ? 'பார்வை மட்டும்' : 'View Only'}
                </button>
              `}
            </div>
          </div>
        `;
      }).join('');
    }

  } catch (err) {
    if (candContainer) candContainer.innerHTML = `<p style="color:red;">Error fetching recommendations: ${err.message}</p>`;
  }
}

async function confirmPlantReplacement(catalogId, plantId) {
  try {
    const res = await fetch(`${API_BASE}/plants/replace`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ plant_id: plantId, catalog_id: catalogId })
    });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      closeModal('replacement-modal');
      renderPlants();
    } else {
      showToast(data.error || 'Failed to replace plant', 'error');
    }
  } catch (err) {
    showToast('Failed to execute plant replacement', 'error');
  }
}

async function renderReplacementHistory() {
  const tbody = document.getElementById('replacement-history-table-body');
  if (!tbody) return;
  try {
    const res = await fetch(`${API_BASE}/plants/replacement-history`);
    const history = await res.json();
    if (!history || history.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;">No plant replacements recorded yet.</td></tr>`;
      return;
    }
    const isTa = state.currentLang === 'ta';
    tbody.innerHTML = history.map(h => `
      <tr>
        <td><span style="color:#f43f5e; font-weight:700;"><i class="fa-solid fa-trash-can"></i> ${h.old_plant_name}</span> <small style="color:var(--text-muted);">(${h.old_plant_code})</small></td>
        <td><span style="color:#10b981; font-weight:700;"><i class="fa-solid fa-seedling"></i> ${h.new_plant_name}</span> <small style="font-style:italic;">(${h.new_plant_species})</small></td>
        <td>${h.zone_name}</td>
        <td><span class="match-score-badge" style="font-size:0.75rem; padding:0.15rem 0.5rem;"><i class="fa-solid fa-circle-check"></i> ${h.compatibility_score}%</span></td>
        <td>${h.date}</td>
        <td><span class="badge badge-healthy">${h.replaced_by}</span></td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="6" style="color:red; text-align:center;">Error loading replacement history</td></tr>`;
  }
}

// EXPORT TO WINDOW FOR GLOBAL EVENT HANDLERS & PLAYWRIGHT EVALUATION
window.initApp = initApp;
window.switchView = switchView;
window.openModal = openModal;
window.closeModal = closeModal;
window.selectLoginRole = selectLoginRole;
window.fillDemoCredentials = fillDemoCredentials;
window.togglePasswordVisibility = togglePasswordVisibility;
window.handleLoginSubmit = handleLoginSubmit;
window.handleLogout = handleLogout;
window.openForgotPasswordModal = openForgotPasswordModal;
window.handleForgotPasswordSubmit = handleForgotPasswordSubmit;
window.deleteUserAccount = deleteUserAccount;
window.openAddZoneModal = openAddZoneModal;
window.openEditZoneModal = openEditZoneModal;
window.deleteZone = deleteZone;
window.openAddPlantModal = openAddPlantModal;
window.openEditPlantModal = openEditPlantModal;
window.deletePlant = deletePlant;
window.openAddTaskModal = openAddTaskModal;
window.openCompleteTaskModal = openCompleteTaskModal;
window.openHealthModal = openHealthModal;
window.filterPlants = filterPlants;
window.openAIScannerModal = openAIScannerModal;
window.runAIPlantScan = runAIPlantScan;
window.triggerIrrigationZone = triggerIrrigationZone;
window.convertIssueToTask = convertIssueToTask;
window.redeemRewardItem = redeemRewardItem;
window.toggleChatbot = toggleChatbot;
window.sendChatMessage = sendChatMessage;
window.sendChatPill = sendChatPill;
window.viewZoneDetail = viewZoneDetail;
window.openPlantQRModal = openPlantQRModal;
window.openReplacementModal = openReplacementModal;
window.confirmPlantReplacement = confirmPlantReplacement;
window.renderReplacementHistory = renderReplacementHistory;
window.getVerifiedPlantImage = getVerifiedPlantImage;
window.verifyStudentSubmission = verifyStudentSubmission;
