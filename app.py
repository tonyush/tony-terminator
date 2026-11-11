"""TONY終結者 (Retirement & Wealth Dashboard) — 主程式入口。

啟動：streamlit run app.py
"""

import streamlit as st

from utils import ui

st.set_page_config(
    page_title="TONY終結者 | Retirement & Wealth Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ui.inject_theme()

pages = [
    st.Page(item["path"], title=item["title"], url_path=item["slug"], default=bool(item["default"]))
    for item in ui.NAV_ITEMS
]
current = st.navigation(pages, position="hidden")

ui.render_header()
ui.render_nav(pages)

current.run()
