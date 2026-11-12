"""TONY終結者 (Retirement & Wealth Dashboard) — 主程式入口。

啟動：streamlit run app.py
"""

import streamlit as st

from utils import state, ui
from utils.i18n import _

# 先補齊 st.session_state 的預設值 (language / user_profile / accounting_logs)，避免任何頁面出現 KeyError
state.init_session_state()

st.set_page_config(
    page_title=_("TONY終結者 | Retirement & Wealth Dashboard"),
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

header_col, language_col = st.columns([4, 1.3], vertical_alignment="center")
with header_col:
    ui.render_header()
with language_col:
    ui.render_language_toggle()
ui.render_nav(pages, current)

current.run()
