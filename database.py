import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def get_supabase() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)


def _user_email():
    try:
        return st.user.email
    except Exception:
        return "unknown"


def initialize_database():
    pass


def add_patient(patient_id, name, age, sex, phone, clinical_notes, created_at):
    sb = get_supabase()
    sb.table("patients").insert({
        "patient_id": patient_id,
        "name": name,
        "age": age,
        "sex": sex,
        "phone": phone,
        "clinical_notes": clinical_notes,
        "created_at": created_at,
        "user_email": _user_email(),
    }).execute()


def get_patients():
    sb = get_supabase()
    res = sb.table("patients").select("*").eq(
        "user_email", _user_email()
    ).order("created_at", desc=True).execute()
    return res.data or []


def patient_exists(patient_id):
    sb = get_supabase()
    res = sb.table("patients").select("patient_id").eq(
        "patient_id", patient_id
    ).eq("user_email", _user_email()).execute()
    return len(res.data) > 0


def add_visit(patient_id, visit_date, visit_type, chief_complaint,
              clinical_findings, diagnosis, treatment_plan, notes, created_at):
    sb = get_supabase()
    sb.table("visits").insert({
        "patient_id": patient_id,
        "visit_date": visit_date,
        "visit_type": visit_type,
        "chief_complaint": chief_complaint,
        "clinical_findings": clinical_findings,
        "diagnosis": diagnosis,
        "treatment_plan": treatment_plan,
        "notes": notes,
        "created_at": created_at,
    }).execute()


def get_patient_visits(patient_id):
    sb = get_supabase()
    res = sb.table("visits").select("*").eq(
        "patient_id", patient_id
    ).order("visit_date", desc=True).execute()
    return res.data or []


def add_photo(patient_id, photo_type, photo_url):
    sb = get_supabase()
    sb.table("photos").insert({
        "patient_id": patient_id,
        "photo_type": photo_type,
        "photo_url": photo_url,
    }).execute()


def get_patient_photos(patient_id):
    sb = get_supabase()
    res = sb.table("photos").select("*").eq(
        "patient_id", patient_id
    ).order("uploaded_at", desc=True).execute()
    return res.data or []


def upload_photo(patient_id, file_bytes, file_name, photo_type):
    sb = get_supabase()
    path = f"{patient_id}/{photo_type}_{file_name}"
    sb.storage.from_("patient-photos").upload(
        path, file_bytes, {"content-type": "image/jpeg"}
    )
    url = sb.storage.from_("patient-photos").get_public_url(path)
    add_photo(patient_id, photo_type, url)
    return url
