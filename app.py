import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="অধিরাজের ক্লাস ৩",
    page_icon="🎓",
    layout="wide",
)

st.markdown("""
<style>
  #MainMenu, header, footer { visibility: hidden; }
  .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
  [data-testid="stAppViewContainer"] { background: #07061a; }
</style>
""", unsafe_allow_html=True)

html_path = Path(__file__).parent / "data" / "main_app.html"
html_content = html_path.read_text(encoding="utf-8")
st.components.v1.html(html_content, height=880, scrolling=True)
