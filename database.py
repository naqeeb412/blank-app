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
    try:
        res = sb.table("patients").select("*").execute()
        return res.data or []
    except Exception as e:
        st.error(f"Supabase Error: {str(e)}")
        return []


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

    # تحويل النوع العربي إلى مفتاح آمن
    type_map = {
        "صورة أمامية": "front",
        "صورة جانبية": "side",
        "صورة الابتسامة": "smile",
        "أشعة": "xray",
        "أخرى": "other",
    }
    type_key = type_map.get(photo_type, "other")

    # تنظيف اسم الملف من المسافات والأحرف العربية
    import re
    from datetime import datetime
    safe_name = re.sub(r"[^a-zA-Z0-9._-]", "_", file_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # مسار آمن بالكامل بالإنجليزية
    path = f"{patient_id}/{type_key}_{timestamp}_{safe_name}"

    sb.storage.from_("patient-photos").upload(
        path, file_bytes, {"content-type": "image/jpeg"}
    )
    url = sb.storage.from_("patient-photos").get_public_url(path)
    add_photo(patient_id, photo_type, url)
    return url
    

def delete_photo(photo_id, photo_url):
    sb = get_supabase()
    # استخراج مسار الصورة من الرابط
    if "/patient-photos/" in photo_url:
        path = photo_url.split("/patient-photos/")[-1]
        try:
            sb.storage.from_("patient-photos").remove([path])
        except Exception:
            pass
    sb.table("photos").delete().eq("id", photo_id).execute()




def detect_photo_type(uploaded_file):
    """
    كشف نوع الصورة تلقائيًا:
    - أشعة: صورة رمادية (أبيض وأسود)
    - ابتسامة: اسم الملف يحتوي smile
    - جانبية: اسم الملف يحتوي side/profile
    - أمامية: الافتراضي
    """
    import io
    from PIL import Image

    try:
        filename = uploaded_file.name.lower()

        # 1. اسم الملف
        if any(k in filename for k in [
            "xray", "x-ray", "x_ray", "radiograph",
            "radiology", "أشعة", "اشعه",
        ]):
            return "أشعة"

        if any(k in filename for k in [
            "smile", "ابتسام", "سن",
        ]):
            return "صورة الابتسامة"

        if any(k in filename for k in [
            "side", "profile", "جانب", "جانبي",
        ]):
            return "صورة جانبية"

        if any(k in filename for k in [
            "front", "frontal", "امام", "أمام",
        ]):
            return "صورة أمامية"

        # 2. تحليل الصورة
        img = Image.open(io.BytesIO(uploaded_file.getvalue()))
        img_rgb = img.convert("RGB")

        # هل الصورة رمادية؟ (مؤشر أشعة)
        sample = img_rgb.resize((50, 50))
        pixels = list(sample.getdata())

        is_grayscale = all(
            abs(p[0] - p[1]) < 15 and abs(p[1] - p[2]) < 15
            for p in pixels
        )

        if is_grayscale:
            return "أشعة"

        # 3. نسبة الأبعاد
        width, height = img.size
        ratio = height / width

        if ratio > 1.4:
            return "صورة جانبية"

        # 4. الافتراضي
        return "صورة أمامية"

    except Exception:
        return "صورة أمامية"
