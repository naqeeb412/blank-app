import streamlit as st


def apply_rtl():
    st.markdown("""
    <style>
    /* اتجاه عربي شامل */
    .stApp, section.main, section[data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }

    /* العناوين */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        direction: rtl;
        text-align: right;
    }

    /* حقول الإدخال */
    input, textarea, select {
        direction: rtl !important;
        text-align: right !important;
    }

    /* الأزرار */
    .stButton button {
        direction: rtl;
        font-family: 'Tajawal', 'Cairo', sans-serif;
    }

    /* القائمة الجانبية */
    section[data-testid="stSidebar"] * {
        direction: rtl;
        text-align: right;
    }

    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        direction: rtl;
    }

    /* الجداول والبطاقات */
    [data-testid="stMetric"] {
        direction: rtl;
        text-align: right;
    }

    /* خط عربي جميل */
    html, body, [class*="css"] {
        font-family: 'Tajawal', 'Cairo', 'Segoe UI', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)
