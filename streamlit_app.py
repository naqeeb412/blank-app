import streamlit as st
from datetime import datetime, date

from database import (
    initialize_database,
    add_patient,
    get_patients,
    patient_exists,
    add_visit,
    get_patient_visits,
)

# ============================================================
# NAQclinixAI
# Intelligent Dentistry, Perfect Harmony
# Version 1.3
# ============================================================

st.set_page_config(
    page_title="NAQclinixAI",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize database
initialize_database()

# ============================================================
# SESSION STATE
# ============================================================

if "active_patient_id" not in st.session_state:
    st.session_state.active_patient_id = None


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🦷 NAQclinixAI")
st.sidebar.caption("Intelligent Dentistry, Perfect Harmony")

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

if st.session_state.active_patient_id:
    st.sidebar.success(
        "Active Patient: "
        + st.session_state.active_patient_id
    )
else:
    st.sidebar.info("No active patient")

st.sidebar.divider()
st.sidebar.caption("DentoFacial-HarmonizeAI")
st.sidebar.caption("Version 1.3")


# ============================================================
# DASHBOARD
# ============================================================

if menu == "Dashboard":

    st.title("🦷 NAQclinixAI")
    st.subheader("Clinical Dashboard")

    patients = get_patients()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Patients", len(patients))

    with col2:
        st.metric("Clinical Visits", "—")

    with col3:
        st.metric("Analyses", "—")

    with col4:
        st.metric("Reports", "—")

    st.divider()

    st.subheader("Clinical Workflow")

    st.info(
        """
        1. Patient Registration
        2. Clinical Patient Record
        3. Clinical Visit
        4. Facial & Smile Analysis
        5. Clinical Diagnosis
        6. Treatment Planning
        7. Clinical Report
        """
    )

    if st.session_state.active_patient_id:
        st.success(
            "Active patient: "
            + st.session_state.active_patient_id
        )


# ============================================================
# PATIENT
# ============================================================

elif menu == "Patient":

    st.title("👤 Patient Management")

    tab1, tab2, tab3 = st.tabs(
        [
            "New Patient",
            "Patient Records",
            "Clinical Record",
        ]
    )

    # ========================================================
    # NEW PATIENT
    # ========================================================

    with tab1:

        st.subheader("Register New Patient")

        col1, col2 = st.columns(2)

        with col1:

            patient_name = st.text_input(
                "Patient Name"
            )

            patient_id = st.text_input(
                "Patient ID",
                placeholder="Example: NAQ-0002"
            )

            patient_phone = st.text_input(
                "Phone"
            )

        with col2:

            patient_age = st.number_input(
                "Age",
                min_value=0,
                max_value=120,
                value=25
            )

            patient_sex = st.selectbox(
                "Sex",
                [
                    "Male",
                    "Female",
                    "Other",
                ]
            )

        clinical_notes = st.text_area(
            "Initial Clinical Notes"
        )

        if st.button(
            "Save Patient",
            type="primary"
        ):

            if not patient_name.strip():

                st.warning(
                    "Please enter the patient name."
                )

            elif not patient_id.strip():

                st.warning(
                    "Please enter the Patient ID."
                )

            elif patient_exists(
                patient_id.strip()
            ):

                st.error(
                    "This Patient ID already exists."
                )

            else:

                created_at = datetime.now().isoformat()

                add_patient(
                    patient_id=patient_id.strip(),
                    name=patient_name.strip(),
                    age=patient_age,
                    sex=patient_sex,
                    phone=patient_phone.strip(),
                    clinical_notes=clinical_notes.strip(),
                    created_at=created_at,
                )

                st.session_state.active_patient_id = (
                    patient_id.strip()
                )

                st.success(
                    "Patient saved successfully."
                )

                st.rerun()

    # ========================================================
    # PATIENT RECORDS
    # ========================================================

    with tab2:

        st.subheader("Patient Records")

        patients = get_patients()

        if not patients:

            st.info(
                "No patients registered yet."
            )

        else:

            for patient in patients:

                with st.container(border=True):

                    col1, col2, col3 = st.columns(
                        [3, 2, 1]
                    )

                    with col1:

                        st.markdown(
                            "### "
                            + patient["name"]
                        )

                        st.caption(
                            "Patient ID: "
                            + patient["patient_id"]
                        )

                    with col2:

                        st.write(
                            "Age: "
                            + str(patient["age"])
                        )

                        st.write(
                            "Sex: "
                            + str(patient["sex"])
                        )

                    with col3:

                        if st.button(
                            "Select",
                            key=(
                                "select_"
                                + patient["patient_id"]
                            ),
                        ):

                            st.session_state.active_patient_id = (
                                patient["patient_id"]
                            )

                            st.rerun()

                        if (
                            st.session_state.active_patient_id
                            == patient["patient_id"]
                        ):

                            st.success("ACTIVE")

    # ========================================================
    # CLINICAL RECORD
    # ========================================================

    with tab3:

        st.subheader("Clinical Patient Record")

        active_id = st.session_state.active_patient_id

        if not active_id:

            st.warning(
                "Select a patient first from Patient Records."
            )

        else:

            patients = get_patients()

            active_patient = None

            for patient in patients:

                if patient["patient_id"] == active_id:

                    active_patient = patient
                    break

            if active_patient:

                st.markdown(
                    "## 👤 "
                    + active_patient["name"]
                )

                st.caption(
                    "Patient ID: "
                    + active_patient["patient_id"]
                )

                visits = get_patient_visits(
                    active_id
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Age",
                        active_patient["age"]
                    )

                with col2:

                    st.metric(
                        "Sex",
                        active_patient["sex"]
                    )

                with col3:

                    st.metric(
                        "Visits",
                        len(visits)
                    )

                st.divider()

                # ------------------------------------------------
                # NEW CLINICAL VISIT
                # ------------------------------------------------

                st.subheader("➕ New Clinical Visit")

                visit_date = st.date_input(
                    "Visit Date",
                    value=date.today()
                )

                visit_type = st.selectbox(
                    "Visit Type",
                    [
                        "Initial Examination",
                        "Follow-up",
                        "Emergency",
                        "Aesthetic Consultation",
                        "Orthodontic Consultation",
                        "Prosthodontic Consultation",
                        "Treatment Visit",
                        "Review",
                        "Other",
                    ]
                )

                chief_complaint = st.text_area(
                    "Chief Complaint"
                )

                clinical_findings = st.text_area(
                    "Clinical Findings"
                )

                diagnosis = st.text_area(
                    "Diagnosis"
                )

                treatment_plan = st.text_area(
                    "Treatment Plan"
                )

                visit_notes = st.text_area(
                    "Visit Notes"
                )

                if st.button(
                    "Save Clinical Visit",
                    type="primary"
                ):

                    created_at = datetime.now().isoformat()

                    add_visit(
                        patient_id=active_id,
                        visit_date=str(visit_date),
                        visit_type=visit_type,
                        chief_complaint=chief_complaint.strip(),
                        clinical_findings=clinical_findings.strip(),
                        diagnosis=diagnosis.strip(),
                        treatment_plan=treatment_plan.strip(),
                        notes=visit_notes.strip(),
                        created_at=created_at,
                    )

                    st.success(
                        "Clinical visit saved successfully."
                    )

                    st.rerun()

                st.divider()

                # ------------------------------------------------
                # VISIT HISTORY
                # ------------------------------------------------

                st.subheader("📋 Visit History")

                visits = get_patient_visits(
                    active_id
                )        """
        1. Patient Registration
        2. Clinical Patient Record
        3. Clinical Visit
        4. Facial & Smile Analysis
        5. Clinical Diagnosis
        6. Treatment Planning
        7. Clinical Report
        """
    )

    if st.session_state.active_patient_id:

        st.success(
            f"Active patient: {st.session_state.active_patient_id}"
        )


# ============================================================
# PATIENT
# ============================================================

elif menu == "Patient":

    st.title("👤 Patient Management")

    tab1, tab2, tab3 = st.tabs(
        [
            "New Patient",
            "Patient Records",
            "Clinical Record",
        ]
    )

    # ========================================================
    # NEW PATIENT
    # ========================================================

    with tab1:

        st.subheader("Register New Patient")

        col1, col2 = st.columns(2)

        with col1:

            patient_name = st.text_input(
                "Patient Name"
            )

            patient_id = st.text_input(
                "Patient ID",
                placeholder="Example: NAQ-0002"
            )

            patient_phone = st.text_input(
                "Phone"
            )

        with col2:

            patient_age = st.number_input(
                "Age",
                min_value=0,
                max_value=120,
                value=25
            )

            patient_sex = st.selectbox(
                "Sex",
                [
                    "Male",
                    "Female",
                    "Other",
                ]
            )

        clinical_notes = st.text_area(
            "Initial Clinical Notes"
        )

        if st.button(
            "Save Patient",
            type="primary"
        ):

            if not patient_name.strip():

                st.warning(
                    "Please enter the patient name."
                )

            elif not patient_id.strip():

                st.warning(
                    "Please enter the Patient ID."
                )

            elif patient_exists(
                patient_id.strip()
            ):

                st.error(
                    "This Patient ID already exists."
                )

            else:

                created_at = datetime.now().isoformat()

                add_patient(
                    patient_id=patient_id.strip(),
                    name=patient_name.strip(),
                    age=patient_age,
                    sex=patient_sex,
                    phone=patient_phone.strip(),
                    clinical_notes=clinical_notes.strip(),
                    created_at=created_at,
                )

                st.session_state.active_patient_id = (
                    patient_id.strip()
                )

                st.success(
                    f"Patient '{patient_name}' saved successfully."
                )

                st.rerun()

    # ========================================================
    # PATIENT RECORDS
    # ========================================================

    with tab2:

        st.subheader("Patient Records")

        patients = get_patients()

        if not patients:

            st.info(
                "No patients registered yet."
            )

        else:

            for
