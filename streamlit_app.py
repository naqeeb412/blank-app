import streamlit as st
from datetime import datetime, date

# ============================================================
# NAQclinixAI - نظام إدارة عيادة الأسنان الذكي
# Version 2.3 - مع رفع الصور وحفظها عبر رابط
# ============================================================

st.set_page_config(
    page_title="NAQclinixAI",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded",
)

from style import apply_rtl
apply_rtl()

# ============================================================
# تسجيل الدخول
# ============================================================

if not st.user.is_logged_in:
    st.title("🦷 NAQclinixAI")
    st.subheader("طب أسنان ذكي، انسجام مثالي")
    st.write("الرجاء تسجيل الدخول للوصول إلى لوحة التحكم")

    if st.button("🔐 تسجيل الدخول عبر Google", type="primary"):
        st.login()

    st.stop()

# ============================================================
# قاعدة البيانات
# ============================================================

from database import (
    initialize_database,
    add_patient,
    get_patients,
    patient_exists,
    add_visit,
    get_patient_visits,
    upload_photo,
    get_patient_photos,
    delete_photo,
    add_photo,
)

initialize_database()

# ============================================================
# حالة الجلسة
# ============================================================

if "active_patient_id" not in st.session_state:
    st.session_state.active_patient_id = None


# ============================================================
# الشريط الجانبي
# ============================================================

st.sidebar.title("🦷 NAQclinixAI")
st.sidebar.caption("طب أسنان ذكي، انسجام مثالي")

menu = st.sidebar.radio(
    "القائمة الرئيسية",
    [
        "لوحة التحكم",
        "المرضى",
        "تحليل الوجه",
        "تصميم الابتسامة",
        "التشخيص السريري",
        "التقارير",
        "الإعدادات",
    ],
)

st.sidebar.divider()

if st.session_state.active_patient_id:
    st.sidebar.success(
        "المريض النشط: " + st.session_state.active_patient_id
    )
else:
    st.sidebar.info("لا يوجد مريض نشط")

st.sidebar.divider()

st.sidebar.write(f"👤 {st.user.name}")
st.sidebar.caption(st.user.email)

if st.sidebar.button("🚪 تسجيل الخروج"):
    st.logout()

st.sidebar.divider()
st.sidebar.caption("DentoFacial-HarmonizeAI")
st.sidebar.caption("الإصدار 2.3")


# ============================================================
# لوحة التحكم
# ============================================================

if menu == "لوحة التحكم":

    st.title("🦷 NAQclinixAI")
    st.subheader("لوحة التحكم السريرية")

    patients = get_patients()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("المرضى", len(patients))
    with col2:
        st.metric("الزيارات", "—")
    with col3:
        st.metric("التحليلات", "—")
    with col4:
        st.metric("التقارير", "—")

    st.divider()
    st.subheader("مسار العمل السريري")

    st.info(
        """
        1. تسجيل مريض جديد
        2. السجل السريري للمريض
        3. الزيارة السريرية
        4. تحليل الوجه والابتسامة
        5. التشخيص السريري
        6. خطة العلاج
        7. التقرير السريري
        """
    )

    if st.session_state.active_patient_id:
        st.success(
            "المريض النشط: " + st.session_state.active_patient_id
        )


# ============================================================
# المرضى
# ============================================================

elif menu == "المرضى":

    st.title("👤 إدارة المرضى")

    tab1, tab2, tab3 = st.tabs(
        ["مريض جديد", "سجلات المرضى", "السجل السريري"]
    )

    with tab1:

        st.subheader("تسجيل مريض جديد")

        col1, col2 = st.columns(2)

        with col1:
            patient_name = st.text_input("اسم المريض")
            patient_id = st.text_input(
                "رقم المريض",
                placeholder="مثال: NAQ-0002"
            )
            patient_phone = st.text_input("رقم الهاتف")

        with col2:
            patient_age = st.number_input(
                "العمر", min_value=0, max_value=120, value=25
            )
            patient_sex = st.selectbox(
                "الجنس", ["ذكر", "أنثى", "آخر"]
            )

        clinical_notes = st.text_area("ملاحظات سريرية أولية")

        if st.button("💾 حفظ المريض", type="primary"):

            if not patient_name.strip():
                st.warning("الرجاء إدخال اسم المريض.")

            elif not patient_id.strip():
                st.warning("الرجاء إدخال رقم المريض.")

            elif patient_exists(patient_id.strip()):
                st.error("رقم المريض مسجل مسبقًا.")

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

                st.session_state.active_patient_id = patient_id.strip()
                st.success("تم حفظ المريض بنجاح.")
                st.rerun()

    with tab2:

        st.subheader("سجلات المرضى")

        patients = get_patients()

        if not patients:
            st.info("لا يوجد مرضى مسجلون بعد.")
        else:
            for patient in patients:
                with st.container(border=True):

                    col1, col2, col3 = st.columns([3, 2, 1])

                    with col1:
                        st.markdown("### " + patient["name"])
                        st.caption(
                            "رقم المريض: " + patient["patient_id"]
                        )

                    with col2:
                        st.write("العمر: " + str(patient["age"]))
                        st.write("الجنس: " + str(patient["sex"]))

                    with col3:
                        if st.button(
                            "اختيار",
                            key="select_" + patient["patient_id"],
                        ):
                            st.session_state.active_patient_id = (
                                patient["patient_id"]
                            )
                            st.rerun()

                        if (
                            st.session_state.active_patient_id
                            == patient["patient_id"]
                        ):
                            st.success("نشط")

    with tab3:

        st.subheader("السجل السريري للمريض")

        active_id = st.session_state.active_patient_id

        if not active_id:
            st.warning("اختر مريضًا أولًا من سجلات المرضى.")
        else:
            patients = get_patients()
            active_patient = None

            for patient in patients:
                if patient["patient_id"] == active_id:
                    active_patient = patient
                    break

            if active_patient:

                st.markdown("## 👤 " + active_patient["name"])
                st.caption(
                    "رقم المريض: " + active_patient["patient_id"]
                )

                visits = get_patient_visits(active_id)

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("العمر", active_patient["age"])
                with col2:
                    st.metric("الجنس", active_patient["sex"])
                with col3:
                    st.metric("الزيارات", len(visits))

                st.divider()

                # ------------------------------------------------
                # زيارة سريرية جديدة
                # ------------------------------------------------

                st.subheader("➕ زيارة سريرية جديدة")

                visit_date = st.date_input(
                    "تاريخ الزيارة", value=date.today()
                )

                visit_type = st.selectbox(
                    "نوع الزيارة",
                    [
                        "فحص أولي",
                        "متابعة",
                        "طارئة",
                        "استشارة تجميلية",
                        "استشارة تقويم",
                        "استشارة تعويضات",
                        "زيارة علاجية",
                        "مراجعة",
                        "أخرى",
                    ],
                )

                chief_complaint = st.text_area("الشكوى الرئيسية")
                clinical_findings = st.text_area("الفحوصات السريرية")
                diagnosis = st.text_area("التشخيص")
                treatment_plan = st.text_area("خطة العلاج")
                visit_notes = st.text_area("ملاحظات الزيارة")

                if st.button("💾 حفظ الزيارة", type="primary"):

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

                    st.success("تم حفظ الزيارة بنجاح.")
                    st.rerun()

                st.divider()

                # ------------------------------------------------
                # صور المريض
                # ------------------------------------------------

                st.subheader("📸 صور المريض")
                st.caption(
                    "ارفع صورة من الجهاز أو الصق رابط صورة مباشر"
                )

                photo_tabs = st.tabs(
                    [
                        "😊 أمامية",
                        "👤 جانبية",
                        "😁 ابتسامة",
                        "🦷 أشعة",
                    ]
                )

                photo_types = [
                    "صورة أمامية",
                    "صورة جانبية",
                    "صورة الابتسامة",
                    "أشعة",
                ]

                for tab, ptype in zip(photo_tabs, photo_types):
                    with tab:

                        # الطريقة 1: رفع صورة
                        st.write("**الطريقة 1: رفع صورة من الجهاز**")

                        uploaded_file = st.file_uploader(
                            f"ارفع {ptype}",
                            type=["jpg", "jpeg", "png"],
                            key=f"uploader_{active_id}_{ptype}",
                        )

                        if uploaded_file is not None:
                            file_size_mb = uploaded_file.size / (1024 * 1024)

                            if file_size_mb > 10:
                                st.error(
                                    f"حجم الصورة كبير جدًا ({file_size_mb:.1f} MB)"
                                )
                            else:
                                st.info(
                                    f"حجم الصورة: {file_size_mb:.2f} MB"
                                )
                                st.image(
                                    uploaded_file,
                                    caption="معاينة",
                                    width=200,
                                )

                                if st.button(
                                    f"💾 حفظ {ptype}",
                                    type="primary",
                                    key=f"save_{active_id}_{ptype}",
                                ):
                                    try:
                                        file_bytes = uploaded_file.getvalue()
                                        upload_photo(
                                            active_id,
                                            file_bytes,
                                            uploaded_file.name,
                                            ptype,
                                        )
                                        st.success("تم رفع الصورة بنجاح.")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"خطأ: {str(e)}")

                        st.divider()

                        # الطريقة 2: رابط صورة
                        st.write("**الطريقة 2: لصق رابط صورة مباشر**")

                        url_input = st.text_input(
                            f"رابط {ptype}",
                            placeholder="https://example.com/photo.jpg",
                            key=f"url_{active_id}_{ptype}",
                        )

                        if url_input and st.button(
                            f"💾 حفظ من الرابط",
                            key=f"save_url_{active_id}_{ptype}",
                        ):
                            try:
                                add_photo(active_id, ptype, url_input)
                                st.success("تم حفظ الرابط بنجاح.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"خطأ: {str(e)}")

                        st.divider()

                        # عرض الصور المحفوظة
                        st.write(f"**صور {ptype} المحفوظة:**")

                        all_photos = get_patient_photos(active_id)
                        filtered = [
                            p for p in all_photos
                            if p["photo_type"] == ptype
                        ]

                        if not filtered:
                            st.info("لا توجد صور بعد.")
                        else:
                            cols = st.columns(3)
                            for i, photo in enumerate(filtered):
                                with cols[i % 3]:
                                    st.image(
                                        photo["photo_url"],
                                        caption=photo["photo_type"],
                                        use_container_width=True,
                                    )

                                    if st.button(
                                        "🗑️ حذف",
                                        key=f"del_{photo['id']}",
                                    ):
                                        try:
                                            delete_photo(
                                                photo["id"],
                                                photo["photo_url"],
                                            )
                                            st.success("تم الحذف.")
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"خطأ: {str(e)}")

                st.divider()

                # معرض شامل
                st.subheader("🖼️ جميع صور المريض")

                all_photos = get_patient_photos(active_id)

                if not all_photos:
                    st.info("لا توجد صور محفوظة بعد.")
                else:
                    st.caption(f"المجموع: {len(all_photos)} صورة")
                    cols = st.columns(4)
                    for i, photo in enumerate(all_photos):
                        with cols[i % 4]:
                            st.image(
                                photo["photo_url"],
                                caption=photo["photo_type"],
                                use_container_width=True,
                            )

                st.divider()

                # سجل الزيارات
                st.subheader("📋 سجل الزيارات")

                visits = get_patient_visits(active_id)

                if not visits:
                    st.info("لا توجد زيارات مسجلة بعد.")
                else:
                    for visit in visits:
                        title = (
                            str(visit["visit_date"])
                            + " — "
                            + str(visit["visit_type"])
                        )

                        with st.expander(title):
                            st.write("**الشكوى الرئيسية:**")
                            st.write(visit["chief_complaint"] or "—")
                            st.write("**الفحوصات السريرية:**")
                            st.write(visit["clinical_findings"] or "—")
                            st.write("**التشخيص:**")
                            st.write(visit["diagnosis"] or "—")
                            st.write("**خطة العلاج:**")
                            st.write(visit["treatment_plan"] or "—")
                            st.write("**ملاحظات:**")
                            st.write(visit["notes"] or "—")


# ============================================================
# تحليل الوجه
# ============================================================

elif menu == "تحليل الوجه":

    st.title("📐 تحليل الوجه")

    if not st.session_state.active_patient_id:
        st.warning("اختر مريضًا نشطًا أولًا.")
    else:
        st.success(
            "المريض النشط: " + st.session_state.active_patient_id
        )
        st.subheader("إطار تحليل الوجه والأسنان")

        measurements = [
            "العرض الوجني",
            "الارتفاع الكلي للوجه",
            "ارتفاع الوجه السفلي",
            "تناسب الوجه",
            "تماثل الوجه",
            "انسجام الوجه",
        ]

        for item in measurements:
            st.checkbox(item, key="facial_" + item)

        st.info(
            "سيتم إضافة الكشف الآلي عن المعالم والتحليل الكمي "
            "للوجه في المرحلة التالية."
        )


# ============================================================
# تصميم الابتسامة
# ============================================================

elif menu == "تصميم الابتسامة":

    st.title("😁 تصميم الابتسامة بالذكاء الاصطناعي")

    if not st.session_state.active_patient_id:
        st.warning("اختر مريضًا نشطًا أولًا.")
    else:
        st.success(
            "المريض النشط: " + st.session_state.active_patient_id
        )

        options = [
            "التصميم الرقمي للابتسامة",
            "تحليل تناسب الأسنان",
            "خط الابتسامة",
            "ظهور اللثة",
            "موضع الحواف",
            "خط الوسط السني",
        ]

        selected = st.multiselect("اختر مكونات التحليل", options)

        if selected:
            st.success(str(len(selected)) + " مكونات مختارة.")


# ============================================================
# التشخيص السريري
# ============================================================

elif menu == "التشخيص السريري":

    st.title("🩺 التشخيص السريري")

    if not st.session_state.active_patient_id:
        st.warning("اختر مريضًا نشطًا أولًا.")
    else:
        st.success(
            "المريض النشط: " + st.session_state.active_patient_id
        )

        diagnosis_type = st.selectbox(
            "الوحدة السريرية",
            [
                "تقييم عام",
                "طب الأسنان التجميلي",
                "تقويم الأسنان",
                "التعويضات السنية",
                "تجميل اللثة",
                "علاج الجذور",
            ],
        )

        findings = st.text_area("الفحوصات السريرية")

        if st.button("🔬 توليد التقييم", type="primary"):
            st.info("الوحدة السريرية المختارة: " + diagnosis_type)


# ============================================================
# التقارير
# ============================================================

elif menu == "التقارير":

    st.title("📄 التقارير السريرية")

    if not st.session_state.active_patient_id:
        st.warning("اختر مريضًا نشطًا أولًا.")
    else:
        st.success(
            "المريض النشط: " + st.session_state.active_patient_id
        )

        report_type = st.selectbox(
            "نوع التقرير",
            [
                "ملخص المريض",
                "تقرير الزيارة السريرية",
                "تقرير تحليل الوجه",
                "تقرير تصميم الابتسامة",
                "تقرير خطة العلاج",
            ],
        )

        if st.button("📄 إعداد التقرير", type="primary"):
            st.success("بدأ إعداد التقرير: " + report_type)


# ============================================================
# الإعدادات
# ============================================================

elif menu == "الإعدادات":

    st.title("⚙️ الإعدادات")
    st.subheader("التطبيق")

    st.text_input("اسم العيادة", value="عيادة NAQ لطب الأسنان")

    st.selectbox("اللغة", ["العربية", "English"])
    st.selectbox("الواجهة", ["سريرية", "بحثية", "مطوّر"])

    st.divider()
    st.subheader("قاعدة البيانات")
    st.success("قاعدة بيانات Supabase — متصلة")

    st.caption("NAQclinixAI — طب أسنان ذكي، انسجام مثالي")
    st.caption("الإصدار 2.3")
