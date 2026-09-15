import streamlit as st
from datetime import datetime

# ============================================================
# NAQclinixAI
# Intelligent Dentistry, Perfect Harmony
# Version 1.1
# ============================================================

st.set_page_config(
    page_title="NAQclinixAI",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# Session State
# ============================================================

if "patients" not in st.session_state:
    st.session_state.patients = []

if "active_patient_id" not in st.session_state:
    st.session_state.active_patient_id = None


# ============================================================
# Helper Functions
# ============================================================

def get_active_patient():
    for patient in st.session_state.patients:
        if patient["id"] == st.session_state.active_patient_id:
            return patient
    return None


def patient_exists(patient_id):
    return any(
        patient["id"] == patient_id
        for patient in st.session_state.patients
    )


# ============================================================
# Header
# ============================================================

st.title("🦷 NAQclinixAI")
st.subheader("Intelligent Dentistry, Perfect Harmony")

st.write(
    "AI-powered dentofacial analysis and clinical decision support "
    "for modern aesthetic dentistry."
)

st.divider()


# ============================================================
# Sidebar
# ============================================================

st.sidebar.title("🦷 NAQclinixAI")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Patient",
        "Facial Analysis",
        "Smile Design",
        "Clinical Diagnosis",
        "Reports",
        "Settings",
    ],
)

st.sidebar.divider()

# ============================================================
# Active Patient
# ============================================================

active_patient = get_active_patient()

if active_patient:
    st.sidebar.success(
        f"Active Patient\n\n"
        f"👤 {active_patient['name']}\n\n"
        f"ID: {active_patient['id']}"
    )
else:
    st.sidebar.info("No active patient selected.")

st.sidebar.divider()

st.sidebar.caption("NAQclinixAI")
st.sidebar.caption("DentoFacial-HarmonizeAI")
st.sidebar.caption("Version 1.1")


# ============================================================
# Dashboard
# ============================================================

if menu == "Dashboard":

    st.header("📊 Clinical Dashboard")

    total_patients = len(st.session_state.patients)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Patients", total_patients)

    with col2:
        st.metric("Analyses", 0)

    with col3:
        st.metric("Smile Designs", 0)

    with col4:
        st.metric("Reports", 0)

    st.divider()

    st.subheader("Clinical Workflow")

    st.info(
        """
        NAQclinixAI clinical workflow:

        1. Patient Registration
        2. Clinical Data Collection
        3. Facial & Smile Analysis
        4. Diagnosis & Measurements
        5. AI-Assisted Treatment Planning
        6. Smile Design
        7. Clinical Report
        """
    )

    if active_patient:
        st.subheader("Current Patient")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.write("**Name**")
            st.write(active_patient["name"])

        with c2:
            st.write("**Patient ID**")
            st.write(active_patient["id"])

        with c3:
            st.write("**Age**")
            st.write(active_patient["age"])


# ============================================================
# Patient Management
# ============================================================

elif menu == "Patient":

    st.header("👤 Patient Management")

    tab1, tab2 = st.tabs(
        ["➕ New Patient", "📋 Patient Records"]
    )

    # --------------------------------------------------------
    # New Patient
    # --------------------------------------------------------

    with tab1:

        st.subheader("Register New Patient")

        col1, col2 = st.columns(2)

        with col1:

            patient_name = st.text_input(
                "Patient Name",
                placeholder="Enter full patient name",
            )

            patient_id = st.text_input(
                "Patient ID",
                placeholder="Example: NAQ-0001",
            )

            patient_phone = st.text_input(
                "Phone",
                placeholder="Optional",
            )

        with col2:

            patient_age = st.number_input(
                "Age",
                min_value=0,
                max_value=120,
                value=25,
            )

            patient_sex = st.selectbox(
                "Sex",
                ["Male", "Female", "Other"],
            )

        notes = st.text_area(
            "Clinical Notes",
            placeholder="Enter initial clinical notes...",
        )

        if st.button(
            "💾 Save Patient",
            type="primary",
            use_container_width=True,
        ):

            if not patient_name.strip():
                st.warning("Please enter the patient name.")

            elif not patient_id.strip():
                st.warning("Please enter a Patient ID.")

            elif patient_exists(patient_id.strip()):
                st.error(
                    "This Patient ID already exists. "
                    "Please use a unique ID."
                )

            else:

                new_patient = {
                    "id": patient_id.strip(),
                    "name": patient_name.strip(),
                    "age": patient_age,
                    "sex": patient_sex,
                    "phone": patient_phone.strip(),
                    "notes": notes.strip(),
                    "created_at": datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                }

                st.session_state.patients.append(
                    new_patient
                )

                st.session_state.active_patient_id = (
                    new_patient["id"]
                )

                st.success(
                    f"Patient '{new_patient['name']}' "
                    "was registered successfully."
                )

    # --------------------------------------------------------
    # Patient Records
    # --------------------------------------------------------

    with tab2:

        st.subheader("Patient Records")

        if not st.session_state.patients:

            st.info(
                "No patients have been registered yet."
            )

        else:

            for patient in st.session_state.patients:

                with st.container(border=True):

                    c1, c2, c3, c4 = st.columns(
                        [3, 2, 1, 1]
                    )

                    with c1:
                        st.write(
                            f"**{patient['name']}**"
                        )
                        st.caption(
                            f"Patient ID: {patient['id']}"
                        )

                   
