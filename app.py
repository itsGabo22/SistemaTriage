import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from src.models.hospital import Hospital
from src.models.doctor import Doctor
from src.mock_generator import generate_mock_patients
from src.analytics import ReportGenerator

# Page Configuration
st.set_page_config(
    page_title="HOSPITAL DASHBOARD | Urgencias",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Global Styles */
    .stApp {
        background: radial-gradient(circle at top right, #f8f9fa 0%, #e3f2fd 100%);
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        animation: fadeInDown 0.8s ease-out;
    }
    
    /* Card Styles */
    .card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1), 0 0 0 1px rgba(255,255,255,0.2);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.5s;
    }
    
    .card:hover::before {
        left: 100%;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15), 0 0 0 1px rgba(255,255,255,0.3);
    }
    
    /* UCI Bed Styles */
    .uci-bed {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255,255,255,0.3);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .uci-bed::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .uci-bed:hover::before {
        opacity: 1;
    }
    
    .uci-bed.occupied {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        border-color: #ee5a24;
        color: white;
        animation: pulse-red 2s infinite;
    }
    
    .uci-bed.free {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a3aa 100%);
        border-color: #44a3aa;
        color: white;
        animation: pulse-green 2s infinite;
    }
    
    .uci-bed:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 24px rgba(0,0,0,0.2);
    }
    
    /* Priority Pills */
    .priority-pill {
        padding: 4px 12px;
        border-radius: 20px;
        color: white;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .priority-pill:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.9) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255,255,255,0.3) !important;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Input Field Styles */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(255,255,255,0.9) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Table Styles */
    .dataframe {
        background: rgba(255,255,255,0.9) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a3aa 100%) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #48dbfb 0%, #0abde3 100%) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse-red {
        0%, 100% {
            box-shadow: 0 0 0 0 rgba(238, 90, 36, 0.7);
        }
        50% {
            box-shadow: 0 0 0 10px rgba(238, 90, 36, 0);
        }
    }
    
    @keyframes pulse-green {
        0%, 100% {
            box-shadow: 0 0 0 0 rgba(68, 163, 170, 0.7);
        }
        50% {
            box-shadow: 0 0 0 10px rgba(68, 163, 170, 0);
        }
    }
    
    /* Divider Styles */
    hr {
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent) !important;
        height: 2px !important;
        border: none !important;
    }
    
    /* Enhanced spacing and layout */
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .timeline-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(248,249,250,0.95) 100%);
    }
    
    .hospital-operations {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        margin-bottom: 1.5rem;
    }
    
    .waiting-room-section {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        margin-top: 1.5rem;
    }
    
    .patient-management {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        margin-bottom: 1.5rem;
    }
    
    .staff-search-section {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        margin-top: 1.5rem;
    }
    
    /* Section headers */
    h3 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.2);
    }
    
    h4 {
        color: #2c3e50;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Enhanced UCI beds spacing */
    .uci-bed {
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .uci-bed:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 30px rgba(0,0,0,0.2);
    }
    
    /* Better table styling */
    .dataframe {
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1) !important;
    }
    
    /* Form enhancements */
    .stForm {
        background: rgba(255,255,255,0.5);
        padding: 1rem;
        border-radius: 15px;
        border: 1px solid rgba(102,126,234,0.2);
    }
    
    /* Section dividers */
    hr {
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent) !important;
        height: 1px !important;
        border: none !important;
        margin: 2rem 0 !important;
    }
    
    /* Container spacing */
    .stContainer {
        margin-bottom: 2rem !important;
    }

    /* Expander Styles */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Responsive Design */
    @media (max-width: 1200px) {
        .main .block-container {
            max-width: 95%;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .main-header {
            font-size: 2.5rem;
        }
    }
    
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        
        .main-header {
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        
        .card {
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .uci-bed {
            height: 90px;
            padding: 0.5rem;
            font-size: 0.8rem;
        }
        
        .metrics-container {
            gap: 0.5rem;
        }
        
        .chart-container {
            height: 250px !important;
        }
    }
    
    @media (max-width: 480px) {
        .main-header {
            font-size: 1.5rem;
        }
        
        .card {
            padding: 0.75rem;
        }
        
        .uci-bed {
            height: 80px;
            padding: 0.3rem;
            font-size: 0.7rem;
        }
        
        .stButton > button {
            padding: 0.4rem 1rem !important;
            font-size: 0.9rem !important;
        }
        
        .priority-pill {
            font-size: 0.65rem;
            padding: 2px 8px;
        }
        
        .chart-container {
            height: 200px !important;
        }
    }
    
    /* Hide scrollbar for cleaner look */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Mobile sidebar adjustments */
    @media (max-width: 768px) {
        .css-1d391kg {
            width: 100% !important;
            max-width: 300px !important;
        }
        
        .css-1lcbmhc {
            flex-direction: column !important;
        }
        
        .element-container {
            width: 100% !important;
        }
    }
    
    /* Responsive grid for UCI beds */
    @media (max-width: 1200px) {
        .uci-beds-grid {
            grid-template-columns: repeat(3, 1fr) !important;
            gap: 0.5rem;
        }
    }
    
    @media (max-width: 768px) {
        .uci-beds-grid {
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 0.3rem;
        }
    }
    
    @media (max-width: 480px) {
        .uci-beds-grid {
            grid-template-columns: 1fr 1fr !important;
            gap: 0.2rem;
        }
    }
    
    /* Responsive metrics cards */
    @media (max-width: 768px) {
        .metrics-card {
            min-height: 120px !important;
        }
        
        .metrics-card h2 {
            font-size: 1.5rem !important;
        }
        
        .metrics-card h3 {
            font-size: 1.2rem !important;
        }
    }
    
    @media (max-width: 480px) {
        .metrics-card {
            min-height: 100px !important;
            padding: 0.75rem !important;
        }
        
        .metrics-card h2 {
            font-size: 1.2rem !important;
        }
        
        .metrics-card h3 {
            font-size: 1rem !important;
        }
        
        .metrics-card p {
            font-size: 0.8rem !important;
        }
    }
    
    /* Chart responsive adjustments */
    .js-plotly-plot {
        width: 100% !important;
    }
    
    .plotly {
        width: 100% !important;
    }
    
    /* Table responsive */
    @media (max-width: 768px) {
        .dataframe {
            font-size: 0.8rem;
        }
        
        .dataframe th, .dataframe td {
            padding: 0.3rem !important;
        }
    }
    
    @media (max-width: 480px) {
        .dataframe {
            font-size: 0.7rem;
        }
        
        .dataframe th, .dataframe td {
            padding: 0.2rem !important;
        }
    }
    
    /* Expander responsive */
    @media (max-width: 480px) {
        .streamlit-expanderHeader {
            font-size: 0.9rem !important;
            padding: 0.5rem !important;
        }
    }
    
    /* Form responsive */
    @media (max-width: 480px) {
        .stForm {
            gap: 0.5rem !important;
        }
        
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select {
            font-size: 0.9rem !important;
            padding: 0.4rem !important;
        }
    }
</style>

<script>
    // Detect screen width and store in session state
    function updateScreenWidth() {
        const width = window.innerWidth;
        if (window.parent && window.parent.postMessage) {
            window.parent.postMessage({
                type: 'screen_width',
                width: width
            }, '*');
        }
    }
    
    // Update on load and resize
    updateScreenWidth();
    window.addEventListener('resize', updateScreenWidth);
</script>
""", unsafe_allow_html=True)

# Initialize Session State
if 'hospital' not in st.session_state:
    st.session_state.hospital = Hospital()
    # Add initial doctors
    st.session_state.hospital.add_doctor(Doctor(101, "Gabriel Garcia", "Cardiologia"))
    st.session_state.hospital.add_doctor(Doctor(102, "Maria Lopez", "Pediatria"))
    st.session_state.hospital.add_doctor(Doctor(103, "Juan Perez", "Cirugia"))
    # Initialize Analytics
    st.session_state.reporter = ReportGenerator()

# Initialize feedback system
if 'notifications' not in st.session_state:
    st.session_state.notifications = []

def show_notification(message, type_msg="success"):
    """Show animated notification"""
    notification = {
        'message': message,
        'type': type_msg,
        'timestamp': time.time()
    }
    st.session_state.notifications.append(notification)
    
def create_occupancy_chart():
    """Create UCI occupancy chart"""
    occupied = sum(1 for bed in hospital.uci_beds if bed)
    free = 15 - occupied
    
    fig = go.Figure(data=[go.Pie(
        labels=['Ocupadas', 'Libres'],
        values=[occupied, free],
        hole=0.6,
        marker_colors=['#ff6b6b', '#4ecdc4'],
        textinfo='label+percent',
        textfont_size=14,
        hovertemplate='<b>%{label}</b><br>Camas: %{value}<br>Porcentaje: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': f'🏥 Ocupación UCI: {occupied}/15',
            'x': 0.5,
            'font': {'size': 20, 'color': '#667eea'}
        },
        font=dict(family="Inter", size=12),
        showlegend=True,
        height=300,
        margin=dict(t=50, b=20, l=20, r=20)
    )
    
    return fig

def create_triage_chart():
    """Create triage distribution chart"""
    triage_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for patient in hospital.all_patients.values():
        triage_counts[patient.triage_lvl] += 1
    
    # Add waiting room patients
    waiting_list = hospital.waiting_room.to_list()
    for patient in waiting_list:
        triage_counts[patient.triage_lvl] += 1
    
    colors = ['#ee5a24', '#feca57', '#48dbfb', '#0abde3', '#006ba6']
    labels = ['T1 - Emergencia', 'T2 - Urgencia', 'T3 - Urgencia Menor', 'T4 - No Urgente', 'T5 - Consulta']
    
    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=list(triage_counts.values()),
            marker_color=colors,
            text=list(triage_counts.values()),
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Pacientes: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': '📊 Distribución de Triage',
            'x': 0.5,
            'font': {'size': 20, 'color': '#667eea'}
        },
        xaxis_title="Nivel de Triage",
        yaxis_title="Número de Pacientes",
        font=dict(family="Inter", size=12),
        height=300,
        margin=dict(t=50, b=60, l=40, r=20),
        showlegend=False
    )
    
    return fig

def create_timeline_chart():
    """Create patient timeline chart"""
    import datetime
    
    # Get real data from hospital system
    total_patients = len(hospital.all_patients)
    
    # Create hourly distribution based on actual registered patients
    hours = list(range(24))
    
    if total_patients == 0:
        # No patients registered - show all zeros
        patients_per_hour = [0] * 24
    else:
        # Distribute registered patients throughout the day (simplified logic)
        # In a real system, you'd track registration timestamps
        patients_per_hour = [0] * 24
        
        # Distribute patients based on typical hospital patterns
        # Morning: 6-12, Afternoon: 12-18, Evening: 18-24, Night: 0-6
        morning_hours = list(range(6, 13))    # 6 AM to 12 PM
        afternoon_hours = list(range(12, 19))  # 12 PM to 6 PM  
        evening_hours = list(range(19, 24))    # 7 PM to 12 AM
        night_hours = list(range(0, 6))        # 12 AM to 6 AM
        
        # Weight distribution (more patients during peak hours)
        weights = {
            'morning': 0.35,    # 35% of patients
            'afternoon': 0.30,  # 30% of patients
            'evening': 0.25,    # 25% of patients
            'night': 0.10       # 10% of patients
        }
        
        # Calculate patient counts per period
        morning_count = int(total_patients * weights['morning'])
        afternoon_count = int(total_patients * weights['afternoon'])
        evening_count = int(total_patients * weights['evening'])
        night_count = total_patients - morning_count - afternoon_count - evening_count
        
        # Distribute patients within each period
        for hour in morning_hours:
            if morning_count > 0:
                patients_per_hour[hour] = min(morning_count // len(morning_hours) + (1 if hour == morning_hours[0] else 0), morning_count)
        
        for hour in afternoon_hours:
            if afternoon_count > 0:
                patients_per_hour[hour] = min(afternoon_count // len(afternoon_hours) + (1 if hour == afternoon_hours[0] else 0), afternoon_count)
        
        for hour in evening_hours:
            if evening_count > 0:
                patients_per_hour[hour] = min(evening_count // len(evening_hours) + (1 if hour == evening_hours[0] else 0), evening_count)
        
        for hour in night_hours:
            if night_count > 0:
                patients_per_hour[hour] = min(night_count // len(night_hours) + (1 if hour == night_hours[0] else 0), night_count)
    
    fig = go.Figure(data=[
        go.Scatter(
            x=hours,
            y=patients_per_hour,
            mode='lines+markers',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8, color='#764ba2'),
            hovertemplate='<b>Hora: %{x}:00</b><br>Pacientes: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': f'⏰ Flujo de Pacientes (24h) - Total: {total_patients}',
            'x': 0.5,
            'font': {'size': 20, 'color': '#667eea'}
        },
        xaxis_title="Hora del Día",
        yaxis_title="Pacientes Registrados",
        font=dict(family="Inter", size=12),
        height=300,
        margin=dict(t=50, b=60, l=60, r=20),
        showlegend=False
    )
    
    return fig

def display_notifications():
    """Display recent notifications"""
    if st.session_state.notifications:
        st.markdown("### 🔔 Notificaciones Recientes")
        for notif in st.session_state.notifications[-3:]:  # Show last 3
            if notif['type'] == 'success':
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #4ecdc4 0%, #44a3aa 100%); 
                           color: white; padding: 10px; border-radius: 10px; margin: 5px 0;">
                    ✅ {notif['message']}
                </div>
                """, unsafe_allow_html=True)
            elif notif['type'] == 'error':
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                           color: white; padding: 10px; border-radius: 10px; margin: 5px 0;">
                    ❌ {notif['message']}
                </div>
                """, unsafe_allow_html=True)
            elif notif['type'] == 'warning':
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%); 
                           color: white; padding: 10px; border-radius: 10px; margin: 5px 0;">
                    ⚠️ {notif['message']}
                </div>
                """, unsafe_allow_html=True)

# Initialize feedback system
if 'notifications' not in st.session_state:
    st.session_state.notifications = []

def show_notification(message, type_msg="success"):
    """Show animated notification"""
    notification = {
        'message': message,
        'type': type_msg,
        'timestamp': time.time()
    }
    st.session_state.notifications.append(notification)
    
def create_occupancy_chart():
    """Create UCI occupancy chart"""
    occupied = sum(1 for bed in hospital.uci_beds if bed)
    free = 15 - occupied
    
    fig = go.Figure(data=[go.Pie(
        labels=['Ocupadas', 'Libres'],
        values=[occupied, free],
        hole=0.6,
        marker_colors=['#ff6b6b', '#4ecdc4'],
        textinfo='label+percent',
        textfont_size=14,
        hovertemplate='<b>%{label}</b><br>Camas: %{value}<br>Porcentaje: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': f'🏥 Ocupación UCI: {occupied}/15',
            'x': 0.5,
            'font': {'size': 20, 'color': '#667eea'}
        },
        font=dict(family="Inter", size=12),
        showlegend=True,
        height=300,
        margin=dict(t=50, b=20, l=20, r=20)
    )
    
    return fig

def create_triage_chart():
    """Create triage distribution chart"""
    triage_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for patient in hospital.all_patients.values():
        triage_counts[patient.triage_lvl] += 1
    
    # Add waiting room patients
    waiting_list = hospital.waiting_room.to_list()
    for patient in waiting_list:
        triage_counts[patient.triage_lvl] += 1
    
    colors = ['#ee5a24', '#feca57', '#48dbfb', '#0abde3', '#006ba6']
    labels = ['T1 - Emergencia', 'T2 - Urgencia', 'T3 - Urgencia Menor', 'T4 - No Urgente', 'T5 - Consulta']
    
    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=list(triage_counts.values()),
            marker_color=colors,
            text=list(triage_counts.values()),
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Pacientes: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': '📊 Distribución de Triage',
            'x': 0.5,
            'font': {'size': 20, 'color': '#667eea'}
        },
        xaxis_title="Nivel de Triage",
        yaxis_title="Número de Pacientes",
        font=dict(family="Inter", size=12),
        height=300,
        margin=dict(t=50, b=60, l=40, r=20),
        showlegend=False
    )
    
    return fig

def create_timeline_chart():
    """Create patient timeline chart"""
    import datetime
    
    # Get real data from hospital system
    total_patients = len(hospital.all_patients)
    
    # Create hourly distribution based on actual registered patients
    hours = list(range(24))
    
    if total_patients == 0:
        # No patients registered - show all zeros
        patients_per_hour = [0] * 24
    else:
        # Distribute registered patients throughout the day (simplified logic)
        # In a real system, you'd track registration timestamps
        patients_per_hour = [0] * 24
        
        # Distribute patients based on typical hospital patterns
        # Morning: 6-12, Afternoon: 12-18, Evening: 18-24, Night: 0-6
        morning_hours = list(range(6, 13))    # 6 AM to 12 PM
        afternoon_hours = list(range(12, 19))  # 12 PM to 6 PM  
        evening_hours = list(range(19, 24))    # 7 PM to 12 AM
        night_hours = list(range(0, 6))        # 12 AM to 6 AM
        
        # Weight distribution (more patients during peak hours)
        weights = {
            'morning': 0.35,    # 35% of patients
            'afternoon': 0.30,  # 30% of patients
            'evening': 0.25,    # 25% of patients
            'night': 0.10       # 10% of patients
        }
        
        # Calculate patient counts per period
        morning_count = int(total_patients * weights['morning'])
        afternoon_count = int(total_patients * weights['afternoon'])
        evening_count = int(total_patients * weights['evening'])
        night_count = total_patients - morning_count - afternoon_count - evening_count
        
        # Distribute patients within each period
        for hour in morning_hours:
            if morning_count > 0:
                patients_per_hour[hour] = min(morning_count // len(morning_hours) + (1 if hour == morning_hours[0] else 0), morning_count)
        
        for hour in afternoon_hours:
            if afternoon_count > 0:
                patients_per_hour[hour] = min(afternoon_count // len(afternoon_hours) + (1 if hour == afternoon_hours[0] else 0), afternoon_count)
        
        for hour in evening_hours:
            if evening_count > 0:
                patients_per_hour[hour] = min(evening_count // len(evening_hours) + (1 if hour == evening_hours[0] else 0), evening_count)
        
        for hour in night_hours:
            if night_count > 0:
                patients_per_hour[hour] = min(night_count // len(night_hours) + (1 if hour == night_hours[0] else 0), night_count)
    
    fig = go.Figure(data=[
        go.Scatter(
            x=hours,
            y=patients_per_hour,
            mode='lines+markers',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8, color='#764ba2'),
            hovertemplate='<b>Hora: %{x}:00</b><br>Pacientes: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': f'⏰ Flujo de Pacientes (24h) - Total: {total_patients}',
            'x': 0.5,
            'font': {'size': 20, 'color': '#667eea'}
        },
        xaxis_title="Hora del Día",
        yaxis_title="Pacientes Registrados",
        font=dict(family="Inter", size=12),
        height=300,
        margin=dict(t=50, b=60, l=60, r=20),
        showlegend=False
    )
    
    return fig

def display_notifications():
    """Display recent notifications"""
    if st.session_state.notifications:
        st.markdown("### 🔔 Notificaciones Recientes")
        for notif in st.session_state.notifications[-3:]:  # Show last 3
            if notif['type'] == 'success':
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #4ecdc4 0%, #44a3aa 100%); 
                           color: white; padding: 10px; border-radius: 10px; margin: 5px 0;">
                    ✅ {notif['message']}
                </div>
                """, unsafe_allow_html=True)
            elif notif['type'] == 'error':
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                           color: white; padding: 10px; border-radius: 10px; margin: 5px 0;">
                    ❌ {notif['message']}
                </div>
                """, unsafe_allow_html=True)
            elif notif['type'] == 'warning':
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%); 
                           color: white; padding: 10px; border-radius: 10px; margin: 5px 0;">
                    ⚠️ {notif['message']}
                </div>
                """, unsafe_allow_html=True)

hospital = st.session_state.hospital

# Sidebar: Registration and Navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/822/822118.png", width=80)
    st.title("Admin Hospital")
    
    with st.expander("📝 Registro de Paciente", expanded=True):
        p_id = st.text_input("Identificación (ID)")
        p_name = st.text_input("Nombre Completo")
        p_triage = st.select_slider("Nivel de Triage", options=[1, 2, 3, 4, 5])
        
        if st.button("Registrar Paciente", type="primary"):
            if p_id and p_name:
                hospital.register_patient(p_id, p_name, p_triage)
                show_notification(f"Paciente {p_name} registrado correctamente con triage {p_triage}", "success")
            else:
                show_notification("Por favor completa todos los campos", "warning")

        result = hospital.undo_last_action()
        if result:
            msg = result if isinstance(result, str) else result.get('action', 'Acción revertida')
            show_notification(f"Éxito: {msg}", "success")
            st.rerun()
        else:
            show_notification("No hay acciones para deshacer", "error")

    st.divider()
    st.subheader("💾 Gestión de Datos")
    if st.button("💾 Guardar Estado"):
        hospital.save_to_file()
        st.success("Hospital guardado.")
    
    if st.button("📂 Cargar Estado"):
        new_hospital = Hospital.load_from_file()
        if new_hospital:
            st.session_state.hospital = new_hospital
            st.rerun()

    st.divider()
    st.subheader("🧪 Pruebas y Simulación")
    if st.button("🚀 Generar 10 Pacientes (Mock)"):
        new_patients = generate_mock_patients(10)
        for p_data in new_patients:
            # Register in hospital
            hospital.register_patient(p_data["id"], p_data["name"], p_data["triage_level"])
        st.success("10 pacientes generados y encolados!")
        st.rerun()

    st.divider()
    st.subheader("👨‍⚕️ Personal de Turno")
    for doc in hospital.medical_staff:
        st.write(f"- {doc}")

# Main Layout
st.markdown("<h1 class='main-header'>🏥 Centro de Triage Urgencias V1</h1>", unsafe_allow_html=True)

# Notifications Section (Top)
with st.container():
    display_notifications()

# KPI Metrics Section
with st.container():
    st.markdown("### 📊 Métricas Principales")
    
    # Create a more spacious layout for metrics
    col_metrics1, col_metrics2, col_metrics3, col_metrics4 = st.columns(4, gap="medium")
    
    with col_metrics1:
        total_patients = len(hospital.all_patients)
        st.markdown(f"""
        <div class="card metrics-card" style="text-align: center; min-height: 140px;">
            <h3 style="color: #667eea; margin: 0; font-size: 2rem;">👥</h3>
            <h2 style="margin: 10px 0; color: #1a1a1a; font-size: 2.5rem;">{total_patients}</h2>
            <p style="margin: 0; color: #666; font-weight: 500;">Total Pacientes</p>
        </div>
        """, unsafe_allow_html=True)

    with col_metrics2:
        occupied_beds = sum(1 for bed in hospital.uci_beds if bed)
        st.markdown(f"""
        <div class="card metrics-card" style="text-align: center; min-height: 140px;">
            <h3 style="color: #ff6b6b; margin: 0; font-size: 2rem;">🛏️</h3>
            <h2 style="margin: 10px 0; color: #1a1a1a; font-size: 2.5rem;">{occupied_beds}/15</h2>
            <p style="margin: 0; color: #666; font-weight: 500;">Camas Ocupadas</p>
        </div>
        """, unsafe_allow_html=True)

    with col_metrics3:
        waiting_count = len(hospital.waiting_room.to_list())
        st.markdown(f"""
        <div class="card metrics-card" style="text-align: center; min-height: 140px;">
            <h3 style="color: #feca57; margin: 0; font-size: 2rem;">⏳</h3>
            <h2 style="margin: 10px 0; color: #1a1a1a; font-size: 2.5rem;">{waiting_count}</h2>
            <p style="margin: 0; color: #666; font-weight: 500;">En Espera</p>
        </div>
        """, unsafe_allow_html=True)

    with col_metrics4:
        staff_count = len(hospital.medical_staff)
        st.markdown(f"""
        <div class="card metrics-card" style="text-align: center; min-height: 140px;">
            <h3 style="color: #4ecdc4; margin: 0; font-size: 2rem;">👨‍⚕️</h3>
            <h2 style="margin: 10px 0; color: #1a1a1a; font-size: 2.5rem;">{staff_count}</h2>
            <p style="margin: 0; color: #666; font-weight: 500;">Personal Médico</p>
        </div>
        """, unsafe_allow_html=True)

# Analytics Section
st.markdown("---")
st.markdown("### 📈 Análisis y Estadísticas")

with st.container():
    # Charts in a more organized layout
    col_chart1, col_chart2 = st.columns(2, gap="large")
    
    with col_chart1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_occupancy = create_occupancy_chart()
        st.plotly_chart(fig_occupancy, width='stretch', config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_chart2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_triage = create_triage_chart()
        st.plotly_chart(fig_triage, width='stretch', config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

# Timeline Section
st.markdown("---")
st.markdown("### ⏰ Flujo de Pacientes (24h)")

with st.container():
    st.markdown('<div class="chart-container timeline-container">', unsafe_allow_html=True)
    fig_timeline = create_timeline_chart()
    st.plotly_chart(fig_timeline, width='stretch', config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

# Hospital Operations Section
st.markdown("---")
st.markdown("### 🏥 Operaciones Hospitalarias")

# Responsive layout for different screen sizes
if st.session_state.get('screen_width', 1200) < 768:
    col1, col2 = st.columns(1, gap="medium")
else:
    col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.markdown('<div class="hospital-operations">', unsafe_allow_html=True)
    st.markdown("#### 🛏️ Disponibilidad Camas UCI")
    
    # Responsive bed layout with better spacing
    if st.session_state.get('screen_width', 1200) > 1200:
        beds_cols = st.columns(5, gap="small")
        cols_per_row = 5
    elif st.session_state.get('screen_width', 1200) > 768:
        beds_cols = st.columns(3, gap="small")
        cols_per_row = 3
    else:
        beds_cols = st.columns(2, gap="small")
        cols_per_row = 2
    
    for i in range(15):
        col_idx = i % cols_per_row
        with beds_cols[col_idx]:
            bed_status = hospital.uci_beds[i]
            if bed_status:
                st.markdown(f"""
                <div class="uci-bed occupied">
                    <small style="font-weight: 600;">Cama {i+1}</small>
                    <b style="font-size: 0.9rem;">{bed_status.name}</b>
                    <small style="opacity: 0.9;">ID: {bed_status.id}</small>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Dar Alta #{i+1}", key=f"dch_{i}"):
                    hospital.discharge_patient(i)
                    st.rerun()
            else:
                st.markdown(f"""
                <div class="uci-bed free">
                    <small style="font-weight: 600;">Cama {i+1}</small>
                    <b style="font-size: 0.9rem;">Disponible</b>
                </div>
                """, unsafe_allow_html=True)
        # Add spacing after every row
        if (i+1) % cols_per_row == 0:
            st.markdown('<br style="line-height: 10px;">', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Waiting Room Section
    st.markdown('<div class="waiting-room-section">', unsafe_allow_html=True)
    st.markdown("#### 🏠 Sala de Espera General (Prioridad 4-5)")
    
    waiting_list = hospital.waiting_room.to_list()
    if waiting_list:
        # Create a better styled table
        data = []
        for idx, p in enumerate(waiting_list):
            data.append({
                "#": idx + 1,
                "ID": p.id,
                "Nombre": p.name,
                "Prioridad": f"P{p.triage_lvl}",
                "Estado": "Esperando"
            })
        
        # Custom styled dataframe
        st.dataframe(data, use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);">
            <h4 style="color: #6c757d; margin: 0;">📋</h4>
            <p style="color: #6c757d; margin: 10px 0 0 0;">No hay pacientes en sala de espera</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="patient-management">', unsafe_allow_html=True)
    st.markdown("#### 📋 Gestión de Pacientes")
    
    # Patient selection and history
    all_p_names = [p.name for p in hospital.all_patients.values()]
    if all_p_names:
        selected_p_name = st.selectbox("Seleccionar Paciente para ver Historial", [""] + all_p_names)
        
        if selected_p_name:
            selected_p = next(p for p in hospital.all_patients.values() if p.name == selected_p_name)
            
            # Patient status card
            st.markdown(f"""
            <div class="card" style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); margin-bottom: 1rem;">
                <h5 style="color: #1565c0; margin: 0;">📄 Estado del Paciente</h5>
                <p style="color: #1565c0; font-weight: 600; margin: 5px 0;">{selected_p.status}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Intervention form
            with st.form("add_intervention", clear_on_submit=True):
                st.markdown("**➕ Añadir Intervención**")
                interv = st.text_input("Intervención (Ej: Rayos X, Análisis)")
                if st.form_submit_button("Registrar Intervención"):
                    if interv:
                        selected_p.add_intervention(interv)
                        # Index for O(1) Search
                        if 'reporter' in st.session_state:
                            st.session_state.reporter.index_intervention(selected_p.name, interv)
                        show_notification(f"Intervención '{interv}' añadida a {selected_p_name}", "success")
                    else:
                        show_notification("Por favor ingrese una intervención", "warning")
            
            # History section
            st.markdown("**📜 Historial Médico**")
            history = selected_p.history.to_list()
            if history:
                for idx, item in enumerate(history):
                    st.markdown(f"""
                    <div style="background: rgba(102, 126, 234, 0.1); padding: 8px; border-radius: 8px; margin: 5px 0; border-left: 3px solid #667eea;">
                        <small style="color: #667eea; font-weight: 600;">#{idx+1}</small>
                        <span style="margin-left: 10px;">{item}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 1rem; color: #6c757d;">
                    <small>Sin intervenciones registradas</small>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 2rem;">
            <h4 style="color: #6c757d; margin: 0;">👥</h4>
            <p style="color: #6c757d; margin: 10px 0 0 0;">No hay pacientes registrados</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Staff search section
    st.markdown('<div class="staff-search-section">', unsafe_allow_html=True)
    st.markdown("#### 🔍 Búsqueda de Personal")
    
    search_q = st.text_input("Buscar por especialidad:")
    if search_q:
        results = [d for d in hospital.medical_staff if search_q.lower() in d.specialty.lower()]
        if results:
            for doctor in results:
                st.markdown(f"""
                <div class="card" style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); margin: 8px 0; padding: 12px;">
                    <h6 style="color: #6a1b9a; margin: 0;">👨‍⚕️ {doctor.name}</h6>
                    <small style="color: #6a1b9a;">🏥 {doctor.specialty}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 1rem; color: #6c757d;">
                <small>No se encontraron resultados</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Show all staff
        for doctor in hospital.medical_staff:
            st.markdown(f"""
            <div class="card" style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); margin: 8px 0; padding: 12px;">
                <h6 style="color: #2e7d32; margin: 0;">👨‍⚕️ {doctor.name}</h6>
                <small style="color: #2e7d32;">🏥 {doctor.specialty}</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Cristian's Advanced Search Integration
    st.markdown('<div class="staff-search-section" style="margin-top: 2rem; border-top: 4px solid #764ba2;">', unsafe_allow_html=True)
    st.markdown("#### 🔬 Búsqueda Avanzada de Intervenciones (O(1))")
    st.markdown("<small>Motor de búsqueda por Hash-Map optimizado para reportes hospitalarios.</small>", unsafe_allow_html=True)
    
    search_int = st.text_input("🔍 Buscar pacientes por diagnóstico/intervención:", placeholder="Ej: Rayos X, Cirugía...")
    if search_int:
        if 'reporter' in st.session_state:
            matches = st.session_state.reporter.get_patients_by_intervention(search_int)
            if matches:
                st.info(f"📍 Pacientes encontrados: {', '.join(matches)}")
            else:
                st.warning("No se encontraron pacientes con ese registro.")
    st.markdown('</div>', unsafe_allow_html=True)
# Footer
st.markdown("---")
st.markdown('<div style="text-align: center; padding: 2rem; color: #6c757d;">', unsafe_allow_html=True)
st.caption("🏥 Sistema de Triage Hospitalario - Desarrollado para el taller de Estructuras de Datos")
st.markdown('</div>', unsafe_allow_html=True)
