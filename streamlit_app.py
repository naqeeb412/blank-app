import streamlit as st

# إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="تطبيقي الجديد",
    page_icon="✨",
    layout="wide"
)

# عنوان الصفحة
st.title("✨ مرحباً بك في تطبيقك الجديد")
st.write("هذه صفحة فارغة جاهزة لإضافة عناصرك وأكوادك البرمجية.")

# مثال على زر تفاعلي بسيط
if st.button("اضغط هنا"):
    st.success("تم النقر بنجاح!")
