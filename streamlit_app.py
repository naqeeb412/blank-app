import streamlit as st

# ============================================================
# NAQclinixAI
# Intelligent Dentistry, Perfect Harmony
# ============================================================

st.set_page_config(
    page_title="NAQclinixAI",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded",
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

st.sidebar.title("NAQclinixAI")

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
st.sidebar.caption("NAQclinixAI")
st.sidebar.caption("DentoFacial-HarmonizeAI")
st.sidebar.caption("Version 1.0")

# ============================================================
# Dashboard
# ============================================================

if menu == "Dashboard":

    st.header("Clinical Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Patients", "0")

    with col2:
        st.metric("Analyses", "0")

    with col3:
        st.metric("Smile Designs", "0")

    with col4:
        st.metric("Reports", "0")

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

# ============================================================
# Patient
# ============================================================

elif menu == "Patient":

    st.header("👤 Patient Management")

    st.subheader("New Patient")

    col1, col2 = st.columns(2)

    with col1:
        patient_name = st.text_input("Patient Name")
        patient_id = st.text_input("Patient ID")

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

    notes = st.text_area("Clinical Notes")

    if st.button("Save Patient", type="primary"):
        if patient_name.strip():
            st.success(f"Patient '{patient_name}' saved successfully.")
        else:
            st.warning("Please enter the patient name.")

# ============================================================
# Facial Analysis
# ============================================================

elif menu == "Facial Analysis":

    st.header("📐 Facial Analysis")

    st.write(
        "AI dentofacial analysis module — prepared for facial "
        "landmarks, proportions and harmony measurements."
    )

    st.subheader("Analysis Framework")

    measurements = [
        "Bizygomatic Width",
        "Total Facial Height",
        "Lower Facial Height",
        "Facial Proportions",
        "Facial Symmetry",
        "Facial Harmony",
    ]

    for item in measurements:
        st.checkbox(item, value=False)

    st.info(
        "AI landmark detection and quantitative facial analysis "
        "will be integrated in the next development stage."
    )

# ============================================================
# Smile Design
# ============================================================

elif menu == "Smile Design":

    st.header("😁 AI Smile Design")

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
            f"{len(selected)} smile-design components selected."
        )

# ============================================================
# Clinical Diagnosis
# ============================================================

elif menu == "Clinical Diagnosis":

    st.header("🩺 Clinical Diagnosis")

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

    if st.button("Generate Assessment", type="primary"):
        st.info(
            f"Clinical assessment module selected: {diagnosis_type}"
        )

# ============================================================
# Reports
# ============================================================

elif menu == "Reports":

    st.header("📄 Clinical Reports")

    st.write(
        "Clinical report generation will be connected to "
        "patient data, measurements and AI analysis."
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

    if st.button("Prepare Report"):
        st.success(
            f"Report preparation started: {report_type}"
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
        ["English", "Arabic"],
    )

    st.selectbox(
        "Interface",
        ["Clinical", "Research", "Developer"],
    )

    st.divider()

    st.caption(
        "NAQclinixAI — Intelligent Dentistry, Perfect Harmony"
    )
