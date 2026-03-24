import streamlit as st
import pandas as pd
from src.models.hospital import Hospital
from src.models.doctor import Doctor

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
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .main-header {
        color: #1e3a8a;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .uci-bed {
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.5rem;
        text-align: center;
        height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .uci-bed.occupied {
        background-color: #fee2e2;
        border-color: #ef4444;
    }
    .uci-bed.free {
        background-color: #f0fdf4;
        border-color: #22c55e;
    }
    .priority-pill {
        padding: 2px 10px;
        border-radius: 9999px;
        color: white;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'hospital' not in st.session_state:
    st.session_state.hospital = Hospital()
    # Add initial doctors
    st.session_state.hospital.add_doctor(Doctor(101, "Gabriel Garcia", "Cardiologia"))
    st.session_state.hospital.add_doctor(Doctor(102, "Maria Lopez", "Pediatria"))
    st.session_state.hospital.add_doctor(Doctor(103, "Juan Perez", "Cirugia"))

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
                st.success(f"Paciente {p_name} registrado correctamente.")
            else:
                st.warning("Por favor completa los campos.")

    if st.button("↩️ Deshacer Última Acción"):
        result = hospital.undo_last_action()
        if result:
            st.info(f"Se revirtió la acción: {result['action']}")
        else:
            st.error("No hay acciones para deshacer.")

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
    st.subheader("👨‍⚕️ Personal de Turno")
    for doc in hospital.medical_staff:
        st.write(f"- {doc}")

# Main Layout
st.markdown("<h1 class='main-header'>🏥 Centro de Triage Urgencias V1</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🛏️ Disponibilidad Camas UCI (Array)")
    beds_cols = st.columns(5)
    for i in range(15):
        col_idx = i % 5
        with beds_cols[col_idx]:
            bed_status = hospital.uci_beds[i]
            if bed_status:
                st.markdown(f"""
                <div class="uci-bed occupied">
                    <small>Cama {i+1}</small>
                    <b>{bed_status.name}</b>
                    <small>ID: {bed_status.id}</small>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Dar Alta #{i+1}", key=f"dch_{i}"):
                    hospital.discharge_patient(i)
                    st.rerun()
            else:
                st.markdown(f"""
                <div class="uci-bed free">
                    <small>Cama {i+1}</small>
                    <b>Disponible</b>
                </div>
                """, unsafe_allow_html=True)
        # Add spacing after every row
        if (i+1) % 5 == 0:
            st.write("")

    st.divider()
    st.subheader("🏠 Sala de Espera General - P4/P5 (Cola)")
    waiting_list = hospital.waiting_room.to_list()
    if waiting_list:
        data = []
        for p in waiting_list:
            data.append({"ID": p.id, "Nombre": p.name, "Prioridad": p.triage_lvl})
        st.table(data)
    else:
        st.info("No hay pacientes en sala de espera.")

with col2:
    st.subheader("📋 Registro de Intervenciones (Linked List)")
    all_p_names = [p.name for p in hospital.all_patients.values()]
    selected_p_name = st.selectbox("Seleccionar Paciente para ver Historial", [""] + all_p_names)
    
    if selected_p_name:
        selected_p = next(p for p in hospital.all_patients.values() if p.name == selected_p_name)
        st.info(f"**Estado:** {selected_p.status}")
        
        with st.form("add_intervention"):
            interv = st.text_input("Nueva Intervención (Ej: Rayos X)")
            if st.form_submit_button("Añadir al Historial"):
                selected_p.add_intervention(interv)
                st.success("Intervención registrada.")
        
        st.write("**Historial Médico (Secuencial):**")
        history = selected_p.history.to_list()
        if history:
            for idx, item in enumerate(history):
                st.markdown(f"{idx+1}. ➔ `{item}`")
        else:
            st.write("Sin intervenciones registradas.")

    st.divider()
    st.subheader("🔍 Buscador de Personal (Native List)")
    search_q = st.text_input("Buscar doctor por especialidad:")
    if search_q:
        results = [d for d in hospital.medical_staff if search_q.lower() in d.specialty.lower()]
        for r in results:
            st.write(f"- {r}")

st.divider()
st.caption("Desarrollado para el taller de Estructuras de Datos.")
