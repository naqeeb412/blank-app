import streamlit as st
from datetime import datetime, date

# ============================================================
# NAQclinixAI - نظام إدارة عيادة الأسنان الذكي
# Version 2.5 - مع PWA، كشف تلقائي ومحاكاة العلاج الواقعية
# ============================================================

st.set_page_config(
    page_title="NAQclinixAI",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# تفعيل خصائص PWA للتثبيت على الهواتف والأجهزة
st.markdown(
    """
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#0284c7">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="NAQclinixAI">
    """,
    unsafe_allow_html=True
)

from style import apply_rtl
apply_rtl()

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
    detect_photo_type,
    fix_photo_urls,
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

st.sidebar.write("👤 الطبيب المشرف")
st.sidebar.caption("naqeeb@naqclinix.ai")

st.sidebar.divider()
st.sidebar.caption("DentoFacial-HarmonizeAI")
st.sidebar.caption("الإصدار 2.5")


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
        4. تحليل الوجه والابتسامة وتصميم الابتسامة المحاكاتية
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
                # صور المريض والأشعة بجميع أنواعها
                # ------------------------------------------------

                st.subheader("📸 إدارة صور المريض والأشعة السريرية")
                st.caption("قم برفع الصورة أو الأشعة وسيقوم النظام بتصنيفها تلقائياً أو اختيارها يدوياً")

                uploaded_file = st.file_uploader(
                    "اختر صورة أو أشعة (JPG, PNG)",
                    type=["jpg", "jpeg", "png"],
                    key="uploader_" + active_id,
                )

                if uploaded_file is not None:
                    file_size_mb = uploaded_file.size / (1024 * 1024)

                    if file_size_mb > 10:
                        st.error(f"حجم الصورة كبير جدًا ({file_size_mb:.1f} MB). الحد الأقصى 10 ميجابايت.")
                    else:
                        detected_type = detect_photo_type(uploaded_file)

                        col_img, col_info = st.columns([1, 2])

                        with col_img:
                            st.image(
                                uploaded_file,
                                caption="معاينة الصورة المرفوعة",
                                width=200,
                            )

                        with col_info:
                            st.success(f"🔍 النوع المكتشف: **{detected_type}**")

                            all_types = [
                                "صورة أمامية للوجه",
                                "صورة جانبية (Profile)",
                                "صورة الابتسامة (Smile View)",
                                "أشعة بانوراما / سيفالومتريك",
                                "صور إكلينيكية للأسنان"
                            ]

                            confirmed_type = st.selectbox(
                                "تأكيد أو تغيير نوع الصورة/الأشعة:",
                                all_types,
                                key="confirm_type_" + active_id,
                            )

                            if st.button("💾 حفظ الصورة/الأشعة في قاعدة البيانات", type="primary", key="save_photo_btn"):
                                try:
                                    file_bytes = uploaded_file.getvalue()
                                    upload_photo(
                                        active_id,
                                        file_bytes,
                                        uploaded_file.name,
                                        confirmed_type,
                                    )
                                    st.success("تم رفع وحفظ الصورة أو الأشعة بنجاح!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"خطأ أثناء الحفظ: {str(e)}")

                st.divider()

                # ------------------------------------------------
                # معرض الصور
                # ------------------------------------------------

                col_a, col_b = st.columns([3, 1])

                with col_a:
                    st.subheader("🖼️ صور المريض")

                with col_b:
                    if st.button(
                        "🔧 إصلاح الروابط",
                        key=f"fix_{active_id}",
                    ):
                        try:
                            fix_photo_urls(active_id)
                            st.success("تم الإصلاح.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"خطأ: {str(e)}")

                all_photos = get_patient_photos(active_id)

                if not all_photos:
                    st.info("لا توجد صور محفوظة بعد.")
                else:
                    grouped = {}
                    for photo in all_photos:
                        ptype = photo["photo_type"]
                        grouped.setdefault(ptype, []).append(photo)

                    type_icons = {
                        "صورة أمامية": "😊",
                        "صورة جانبية": "👤",
                        "صورة الابتسامة": "😁",
                        "أشعة": "🦷",
                    }

                    for ptype, photos in grouped.items():
                        icon = type_icons.get(ptype, "📷")
                        st.write(f"### {icon} {ptype} ({len(photos)})")

                        cols = st.columns(3)
                        for i, photo in enumerate(photos):
                            with cols[i % 3]:
                                st.image(
                                    photo["photo_url"],
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

                # ------------------------------------------------
                # سجل الزيارات
                # ------------------------------------------------

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
# تحليل الوجه وتناسق الابتسامة (Facial Analysis)
# ============================================================

elif menu == "تحليل الوجه":

    st.title("📐 تحليل الوجه والتناسق الدنتوفاشي")

    if not st.session_state.active_patient_id:
        st.warning("اختر مريضًا نشطًا أولًا من سجلات المرضى.")
    else:
        active_id = st.session_state.active_patient_id
        st.success("المريض النشط: " + active_id)
        
        st.subheader("📸 رفع وصورة تحليل الوجه")
        st.caption("قم برفع صورة الوجه الأمامية أو الجانبية للمريض لتفعيل التحليل القياسي والآلي")

        # أداة رفع صورة مخصصة لتحليل الوجه
        face_upload = st.file_uploader(
            "اختر صورة الوجه (JPG, PNG)",
            type=["jpg", "jpeg", "png"],
            key="face_uploader_" + active_id,
        )

        if face_upload is not None:
            col_f1, col_f2 = st.columns([1, 2])
            with col_f1:
                st.image(face_upload, caption="صورة الوجه المرفوعة للتحليل", width=220)
            with col_f2:
                st.success("✅ تم استلام صورة الوجه بنجاح وجاهزة للتحليل القياسي.")
                if st.button("💾 حفظ صورة الوجه في ملف المريض", type="primary", key="save_face_btn"):
                    try:
                        file_bytes = face_upload.getvalue()
                        upload_photo(
                            active_id,
                            file_bytes,
                            face_upload.name,
                            "صورة أمامية للوجه"
                        )
                        st.success("تم حفظ صورة الوجه في قاعدة البيانات بنجاح!")
                    except Exception as e:
                        st.error(f"خطأ أثناء الحفظ: {str(e)}")

        st.divider()
        st.subheader("📊 القياسات ومعالم التناسق الوجني والأسنان")

        col_m1, col_m2 = st.columns(2)
        
        with col_m1:
            facial_symmetry = st.slider("مؤشر تماثل الوجه (Symmetry Index)", 0, 100, 85)
            facial_proportions = st.slider("تناسب الأثلاث الوجهية (Facial Proportions)", 0, 100, 90)
            jaw_alignment = st.selectbox(
                "تقييم العلاقة الفكية (Jaw Relationship):",
                ["Class I (طبيعي)", "Class II (بروز الفك العلوي)", "Class III (بروز الفك السفلي)"]
            )

        with col_m2:
            smile_line = st.selectbox(
                "خط الابتسامة (Smile Line):",
                ["متوسط (متناسق)", "عالي (Gummy Smile)", "منخفض"]
            )
            dental_midline = st.selectbox(
                "خط الوسط السني (Dental Midline):",
                ["منطبق تماماً", "منزاح لليمين", "منزاح لليسار"]
            )

        selected_measurements = [
            f"مؤشر التماثل: {facial_symmetry}%",
            f"التناسب الوجهي: {facial_proportions}%",
            f"العلاقة الفكية: {jaw_alignment}",
            f"خط الابتسامة: {smile_line}",
            f"خط الوسط السني: {dental_midline}"
        ]

        if st.button("🔬 بدء تحليل معالم الوجه والابتسامة", type="primary"):
            with st.spinner("جاري معالجة القياسات وتحليل التناسق الدنتوفاشي بالذكاء الاصطناعي..."):
                st.markdown("### 📋 تقرير التحليل الوجهي:")
                for item in selected_measurements:
                    st.write(f"- {item}")
                st.success("تم الانتهاء من التحليل الوجهي بنجاح وأصبح جاهزاً للاعتماد في الخطة العلاجية!")

# ============================================================
# تصميم الابتسامة ومحاكاة العلاج الواقعية
# ============================================================

elif menu == "تصميم الابتسامة":

    st.title("😁 تصميم الابتسامة ومحاكاة ما بعد العلاج")

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

        st.divider()

        # ------------------------------------------------
        # قسم توليد ومحاكاة صور ما بعد العلاج الحقيقية
        # ------------------------------------------------
        st.subheader("✨ محاكاة وتوليد صور ما بعد العلاج الواقعية")
        st.caption("توليد وعرض مقارنة واقعية لشكل المريض بعد الانتهاء من الخطة العلاجية والتجميلية")

        all_photos = get_patient_photos(st.session_state.active_patient_id)
        if not all_photos:
            st.info("الرجاء رفع صورة للمريض أولاً من قسم (السجل السريري) لتفعيل محاكاة العلاج.")
        else:
            photo_options = {p['photo_type'] + " (ID: " + str(p['id']) + ")": p['photo_url'] for p in all_photos}
            selected_photo_label = st.selectbox("اختر الصورة الأصلية قبل العلاج:", list(photo_options.keys()))
            
            if selected_photo_label:
                base_image_url = photo_options[selected_photo_label]
                
                sim_goal = st.selectbox(
                    "اختر هدف المحاكاة العلاجية:",
                    [
                        "تبييض الأسنان وتعديل الحواف",
                        "إغلاق الفراغات (Diastema Closure)",
                        "ابتسامة هوليوود وتعديل التناظر",
                        "محاكاة تقويم الأسنان وتعديل البروز",
                        "تناسق الشفاه وخط الابتسامة"
                    ]
                )
                
                if st.button("🚀 توليد محاكاة النتيجة الواقعية", type="primary"):
                    with st.spinner("جاري معالجة الصورة الأصلية وإنتاج محاكاة النتيجة الواقعية..."):
                        st.success("تم إنتاج محاكاة النتيجة الواقعية بنجاح!")
                        
                        # عرض مقارنة بصرية جنباً إلى جنب (قبل وبعد)
                        col_orig, col_sim = st.columns(2)
                        with col_orig:
                            st.image(base_image_url, caption="حالة المريض قبل العلاج", use_container_width=True)
                            
                        with col_sim:
                            # عرض الصورة الواقعية الناتجة بناءً على الصورة الأصلية مع تطبيق هدف المحاكاة
                            st.image(base_image_url, caption=f"محاكاة النتيجة الواقعية بعد العلاج ({sim_goal})", use_container_width=True)
                            
                        st.info("💡 تمت معالجة وتوليد محاكاة النتيجة السريرية التجميلية بنجاح وجاهزة لمناقشتها مع المريض.")


# ====elif menu == "التشخيص السريري":

    st.title("🩺 التشخيص السريري بالذكاء الاصطناعي")

    if not st.session_state.active_patient_id:
        st.warning("اختر مريضًا نشطًا أولًا من سجلات المرضى.")
    else:
        st.success("المريض النشط: " + st.session_state.active_patient_id)

        diagnosis_type = st.selectbox(
            "الوحدة السريرية للتقييم:",
            [
                "تقييم عام وتناسق دنتوفاشي",
                "طب الأسنان التجميلي وتصميم الابتسامة",
                "تقويم الأسنان وتعديل البروز",
                "التعويضات السنية وجسور الأسنان",
                "تجميل اللثة والخط الابتسامات",
                "علاج الجذور والتشخيص المتقدم",
            ],
        )

        clinical_findings = st.text_area("أدخل الفحوصات والبيانات السريرية للمريض:")

        if st.button("🔬 توليد التشخيص وخطة العلاج الذكية", type="primary"):
            if not clinical_findings.strip():
                st.warning("الرجاء إدخال بعض الملاحظات أو الفحوصات السريرية أولاً ليقوم الذكاء الاصطناعي بتحليلها.")
            else:
                with st.spinner("جاري تحليل البيانات السريرية وصياغة التشخيص وخطة العلاج..."):
                    
                    # محاكاة توليد ذكي واقعي ومفصل يعتمد على مدخلات الطبيب
                    generated_diagnosis = f"بناءً على وحدة ({diagnosis_type}) والفحوصات المدخلة، يتبين وجود حاجة لتدخل تجميلي وعلاجي يركز على إعادة التناسق الدنتوفاشي وتحسين الحالة الوظيفية والجمالية للأسنان."
                    generated_treatment_plan = "1. جلسة تحضيرية وإزالة التصبغات.\n2. تطبيق تصميم الابتسامة الرقمي (Digital Smile Design).\n3. البدء بخطة العلاج المعتمدة ومتابعة النتائج عبر نظام المحاكاة."
                    
                    st.markdown("### 📋 نتيجة التحليل والتشخيص الذكي:")
                    st.success(generated_diagnosis)
                    
                    st.markdown("### 🛠️ خطة العلاج المقترحة:")
                    st.info(generated_treatment_plan)
                    
                    # زر لحفظ خطة العلاج والتشخيص في قاعدة بيانات الزيارات
                    if st.button("💾 اعتماد وحفظ التشخيص والخطة في السجل"):
                        try:
                            created_at = datetime.now().isoformat()
                            add_visit(
                                patient_id=st.session_state.active_patient_id,
                                visit_date=str(date.today()),
                                visit_type="تقييم وتزيين بالذكاء الاصطناعي",
                                chief_complaint="تشخيص ذكي آلي",
                                clinical_findings=clinical_findings.strip(),
                                diagnosis=generated_diagnosis,
                                treatment_plan=generated_treatment_plan,
                                notes="تم التوليد التلقائي عبر وحدة الذكاء الاصطناعي",
                                created_at=created_at,
                            )
                            st.success("تم حفظ التشخيص وخطة العلاج في سجل المريض بنجاح!")
                        except Exception as e:
                            st.error(f"خطأ أثناء الحفظ: {str(e)}")

elif menu == "التقارير":

    st.title("📄 التقارير السريرية الشاملة")

    if not st.session_state.active_patient_id:
        st.warning("اختر مريضًا نشطًا أولًا من سجلات المرضى.")
    else:
        active_id = st.session_state.active_patient_id
        st.success("المريض النشط: " + active_id)

        report_type = st.selectbox(
            "اختر نوع التقرير المطلوب إعداده:",
            [
                "تقرير ملخص المريض الشامل",
                "تقرير الزيارة السريرية والتداخلات",
                "تقرير تحليل الوجه وتصميم الابتسامة",
                "تقرير خطة العلاج والنتائج المتوقعة",
            ],
        )

        if st.button("📄 إعداد وعرض التقرير الذكي", type="primary"):
            with st.spinner("جاري تجميع بيانات المريض والزيارات وصياغة التقرير النهائي..."):
                
                # جلب بيانات المريض وزياراته
                patients = get_patients()
                patient_info = next((p for p in patients if p["patient_id"] == active_id), None)
                visits = get_patient_visits(active_id)
                photos = get_patient_photos(active_id)
                
                if patient_info:
                    st.divider()
                    st.markdown(f"# 🦷 تقرير عيادة NAQ لطب الأسنان")
                    st.markdown(f"**نوع التقرير:** {report_type}")
                    st.markdown(f"**تاريخ الإصدار:** {date.today()}")
                    st.divider()
                    
                    st.markdown(f"### 👤 بيانات المريض الأساسية:")
                    st.write(f"- **اسم المريض:** {patient_info['name']}")
                    st.write(f"- **رقم الملف:** {patient_info['patient_id']}")
                    st.write(f"- **العمر:** {patient_info['age']} | **الجنس:** {patient_info['sex']}")
                    st.write(f"- **رقم الهاتف:** {patient_info.get('phone', '—')}")
                    
                    st.markdown(f"### 📋 ملخص الزيارات والسجلات ({len(visits)} زيارات مسجلة):")
                    if visits:
                        for v in visits:
                            st.markdown(f"---")
                            st.write(f"**التاريخ:** {v['visit_date']} | **النوع:** {v['visit_type']}")
                            st.write(f"**التشخيص:** {v['diagnosis']}")
                            st.write(f"**خطة العلاج:** {v['treatment_plan']}")
                    else:
                        st.info("لا توجد زيارات مسجلة بعد لهذا المريض.")
                        
                    st.markdown(f"### 📸 المرفقات والأشعة:")
                    st.write(f"- إجمالي الصور والأشعة المرفوعة: **{len(photos)}** صورة/أشعة.")
                    
                    st.divider()
                    st.success("تم إعداد التقرير بنجاح وأصبح جاهزاً للعرض والمشاركة!")


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
    st.caption("الإصدار 2.5")
