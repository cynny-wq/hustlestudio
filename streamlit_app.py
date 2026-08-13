import streamlit as st

# 1. CORE PAGE CONFIGURATION
st.set_page_config(
    page_title="Hustle Studio",
    page_icon="🚀",
    layout="centered"
)

# 2. CUSTOM MOBILE-FIRST STYLING
st.markdown("""
    <style>
    /* Expands buttons to full-width and adds padding for mobile thumb tapping */
    div.stButton > button:first-child {
        width: 100%;
        padding: 14px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    /* Styles the custom notification box for results cards */
    .result-card {
        background-color: #f8f9fa;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 16px;
        border-left: 5px solid #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Hustle Studio")

st.success(
    "📱 **Hustler Tip:** Want this as a phone app? Tap your browser settings "
    "(3 dots) and click **'Add to Home Screen'** to get an instant shortcut icon on your phone!"
)

st.markdown("Standalone digital tools designed to help Kenyan content creators grow fast.")

# 3. INITIALIZE PERSISTENT WORKSPACE STATE ENGINE
if "workspace_data" not in st.session_state:
    st.session_state.workspace_data = {
        "hooks": [],
        "script": "",
        "captions": "",
        "current_topic": ""
    }
