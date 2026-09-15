import streamlit as st
from datetime import datetime

from database import (
    initialize_database,
    add_patient,
    get_patients,
    patient_exists,
)

# ============================================================
# NAQclinixAI
# Intelligent Dentistry, Perfect Harmony
# Version 1.2
# ============================================================

st.set_page_config(
    page_title="NAQclinixAI",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# Initialize Database
# ============================================================

initialize_database()

# ============================================================
# Session State
# ============================================================

if "active_patient_id" not in st.session_state:
    st.session_state.active_patient_id = None


# ============================================================
# Load Patients
# ============================================================

patients = get_patients()


def get_active_patient():
    for patient in patients:
        if patient["patient_id"] == st.session_state.active_patient_id:
            return patient
    return None


active_patient = get_active_patient()


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

if active_patient:

    st.sidebar.success(
        f"ACTIVE PATIENT\n\n"
        f"👤 {active_patient['name']}\n\n"
        f"ID: {active_patient['patient_id']}"
    )

else:

    st.sidebar.info(
        "No active patient selected."
    )

st.sidebar.divider()

st.sidebar.caption("NAQclinixAI")
st.sidebar.caption("DentoFacial-HarmonizeAI")
st.sidebar.caption("Version 1.2")


# ============================================================
# Dashboard
# ============================================================

if menu == "Dashboard":

    st.header("📊 Clinical Dashboard")

    total_patients = len(patients)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Patients",
            total_patients
        )

    with col2:
        st.metric(
            "Analyses",
            0
        )

    with col3:
        st.metric(
            "Smile Designs",
            0
        )

    with col4:
        st.metric(
            "Reports",
            0
        )

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
            st.write(active_patient["patient_id"])

        with c3:
            st.write("**Age**")
            st.write(active_patient["age"])


# ============================================================
# Patient Management
# ============================================================

elif menu == "Patient":

    st.header("👤 Patient Management")

    tab1, tab2 = st.tabs(
        [
            "➕ New Patient",
            "📋 Patient Records",
        ]
    )

    # ========================================================
    # New Patient
    # ========================================================

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
                [
                    "Male",
                    "Female",
                    "Other",
                ],
            )

        clinical_notes = st.text_area(
            "Clinical Notes",
            placeholder="Enter initial clinical notes...",
        )

        st.divider()

        if st.button(
            "💾 Save Patient",
            type="primary",
            use_container_width=True,
        ):

            clean_name = patient_name.strip()
            clean_id = patient_id.strip()
            clean_phone = patient_phone.strip()
            clean_notes = clinical_notes.strip()

            if not clean_name:

                st.warning(
                    "Please enter the patient name."
                )

            elif not clean_id:

                st.warning(
                    "Please enter a Patient ID."
                )

            elif patient_exists(clean_id):

                st.error(
                    "This Patient ID already exists. "
                    "Please use a unique ID."
                )

            else:

                created_at = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                add_patient(
                    patient_id=clean_id,
                    name=clean_name,
                    age=patient_age,
                    sex=patient_sex,
                    phone=clean_phone,
                    clinical_notes=clean_notes,
                    created_at=created_at,
                )

                st.session_state.active_patient_id = clean_id

                st.success(
                    f"Patient '{clean_name}' "
                    "was saved successfully."
                )

                st.rerun()

    # ========================================================
    # Patient Records
    # ========================================================

    with tab2:

        st.subheader("Patient Records")

        patients = get_patients()

        if not patients:

            st.info(
                "No patients have been registered yet."
            )

        else:

            st.write(
                f"**Total Patients: {len(patients)}**"
            )

            st.divider()

            for patient in patients:

                with st.container(border=True):

                    c1, c2, c3, c4 = st.columns(
                        [3, 2, 1, 1]
                    )

                    with c1:

                        st.write(
                            f"**{patient['name']}**"
                        )

                        st.caption(
                            f"Patient ID: "
                            f"{patient['patient_id']}"
                        )

                    with c2:

                        st.write(
                            f"Age: {patient['age']}"
                        )

                        st.write(
                            f"Sex: {patient['sex']}"
                        )

                    with c3:

                        if st.button(
                            "Select",
                            key=f"select_{patient['patient_id']}",
                        ):

                            st.session_state.active_patient_id = (
                                patient["patient_id"]
                            )

                            st.rerun()

                    with c4:

                        if (
                            st.session_state.active_patient_id
                            == patient["patient_id"]
                        ):

                            st.success("ACTIVE")


# ============================================================
# Facial Analysis
# ============================================================

elif menu == "Facial Analysis":

    st.header("📐 Facial Analysis")

    if not active_patient:

        st.warning(
            "Please select a patient before starting "
            "facial analysis."
        )

    else:

        st.success(
            f"Active Patient: "
            f"{active_patient['name']} "
            f"({active_patient['patient_id']})"
        )

        st.write(
            "AI dentofacial analysis module — prepared "
            "for facial landmarks, proportions and "
            "harmony measurements."
        )

        st.subheader(
            "Analysis Framework"
        )

        measurements = [
            "Bizygomatic Width",
            "Total Facial Height",
            "Lower Facial Height",
            "Facial Proportions",
            "Facial Symmetry",
            "Facial Harmony",
        ]

        for item in measurements:

            st.checkbox(
                item,
                key=f"facial_{item}",
            )

        st.info(
            "AI landmark detection and quantitative "
            "facial analysis will be integrated "
            "in the next development stage."
        )


# ============================================================
# Smile Design
# ============================================================

elif menu == "Smile Design":

    st.header("😁 AI Smile Design")

    if not active_patient:

        st.warning(
            "Please select a patient before starting "
            "smile design."
        )

    else:

        st.success(
            f"Active Patient: "
            f"{active_patient['name']} "
            f"({active_patient['patient_id']})"
        )

        st.write(
            "Facially driven smile design workspace."
        )

        options = [
            "Digital Smile Design",
            "Tooth Proportion Analysis",
            "Smile Line",
            "Gingival Display",
            "Incisal Position",
            "Dental Midline",
        ]

        selected = st.multiselect(
            "Select analysis components",
            options,
        )

        if selected:

            st.success(
                f"{len(selected)} "
                "smile-design components selected."
            )


# ============================================================
# Clinical Diagnosis
# ============================================================

elif menu == "Clinical Diagnosis":

    st.header("🩺 Clinical Diagnosis")

    if not active_patient:

        st.warning(
            "Please select a patient before entering "
            "clinical diagnosis."
        )

    else:

        st.success(
            f"Active Patient: "
            f"{active_patient['name']} "
            f"({active_patient['patient_id']})"
        )

        diagnosis_type = st.selectbox(
            "Clinical Module",
            [
                "General Assessment",
                "Aesthetic Dentistry",
                "Orthodontics",
                "Prosthodontics",
                "Gingival Aesthetics",
                "Endodontics",
            ],
        )

        findings = st.text_area(
            "Clinical Findings",
            placeholder="Enter clinical findings...",
        )

        if st.button(
            "Generate Assessment",
            type="primary",
        ):

            st.info(
                f"Clinical assessment module selected: "
                f"{diagnosis_type}"
            )

            if findings.strip():

                st.write(
                    "### Clinical Findings"
                )

                st.write(findings)


# ============================================================
# Reports
# ============================================================

elif menu == "Reports":

    st.header("📄 Clinical Reports")

    if not active_patient:

        st.warning(
            "Please select a patient before generating "
            "a clinical report."
        )

    else:

        st.success(
            f"Report Patient: "
            f"{active_patient['name']} "
            f"({active_patient['patient_id']})"
        )

        report_type = st.selectbox(
            "Report Type",
            [
                "Patient Summary",
                "Facial Analysis Report",
                "Smile Design Report",
                "Treatment Planning Report",
            ],
        )

        if st.button(
            "Prepare Report",
            type="primary",
        ):

            st.success(
                f"Report preparation started: "
                f"{report_type}"
            )

            st.write("### Patient")

            st.write(
                f"**Name:** "
                f"{active_patient['name']}"
            )

            st.write(
                f"**Patient ID:** "
                f"{active_patient['patient_id']}"
            )

            st.write(
                f"**Age:** "
                f"{active_patient['age']}"
            )

            st.write(
                f"**Sex:** "
                f"{active_patient['sex']}"
            )


# ============================================================
# Settings
# ============================================================

elif menu == "Settings":

    st.header("⚙️ Settings")

    st.subheader("Application")

    st.text_input(
        "Clinic Name",
        value="NAQ Dental Clinic",
    )

    st.selectbox(
        "Language",
        [
            "English",
            "Arabic",
        ],
    )

    st.selectbox(
        "Interface",
        [
            "Clinical",
            "Research",
            "Developer",
        ],
    )

    st.divider()

    st.subheader("System Information")

    st.write(
        "**Application:** NAQclinixAI"
    )

    st.write(
        "**Platform:** Streamlit"
    )

    st.write(
        "**Database:** SQLite"
    )

    st.write(
        "**Architecture:** DentoFacial-HarmonizeAI"
    )

    st.write(
        "**Version:** 1.2"
    )

    st.divider()

    st.caption(
        "NAQclinixAI — Intelligent Dentistry, Perfect Harmony"
    )
