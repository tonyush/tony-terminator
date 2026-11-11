"""共用 UI 元件：深色主題 CSS、Header、頂部導覽列、含跨頁同步的輸入元件。"""

from __future__ import annotations

import base64
from typing import Any, Sequence

import streamlit as st

from utils import math_models as mm
from utils import state

NAV_ITEMS: list[dict[str, str]] = [
    {"path": "pages/1_life.py", "title": "人生終結者", "slug": "life", "default": "1"},
    {"path": "pages/2_ledger.py", "title": "記帳面板", "slug": "ledger", "default": ""},
    {"path": "pages/3_control.py", "title": "調控面板", "slug": "control", "default": ""},
    {"path": "pages/4_dashboard.py", "title": "數據面板", "slug": "dashboard", "default": ""},
    {"path": "pages/5_funds.py", "title": "資金面板", "slug": "funds", "default": ""},
]

COLOR_TAGS: dict[str, str] = {
    "🔴 紅": "#EF4444",
    "🟠 橙": "#F97316",
    "🟡 黃": "#EAB308",
    "🟢 綠": "#22C55E",
    "🔵 藍": "#3B82F6",
    "🟣 紫": "#A855F7",
    "⚪ 灰": "#9CA3AF",
}

CHART_COLORS = ["#F5B942", "#2DD4BF", "#60A5FA", "#F472B6", "#A78BFA", "#FB923C"]

LOGO_SVG = """
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>
  <defs>
    <linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>
      <stop offset='0' stop-color='#FFD27A'/><stop offset='1' stop-color='#E08A1E'/>
    </linearGradient>
  </defs>
  <path d='M32 4 56 13v18c0 14-10 24-24 29C18 55 8 45 8 31V13z' fill='#0F1A2E' stroke='url(#g)' stroke-width='3'/>
  <path d='M19 25h26M32 25v21' stroke='url(#g)' stroke-width='5' stroke-linecap='round'/>
  <path d='M20 41l8-7 6 4 10-12' fill='none' stroke='#2DD4BF' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/>
</svg>
"""

CSS = """
<style>
:root {
  --bg: #0B1220; --panel: #121B2E; --panel-2: #172238; --line: #243049;
  --text: #E6EAF2; --muted: #8C98B0; --gold: #F5B942; --teal: #2DD4BF; --red: #F87171;
}
.stApp { background: radial-gradient(1200px 600px at 10% -10%, #14213D 0%, var(--bg) 55%); }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1.4rem; max-width: 1200px; }

/* Header */
.tony-header { display:flex; align-items:center; gap:14px; margin-bottom:.9rem; }
.tony-header img { width:52px; height:52px; filter: drop-shadow(0 4px 12px rgba(245,185,66,.35)); }
.tony-header .t1 { font-size:1.65rem; font-weight:800; letter-spacing:.04em; color:var(--text); line-height:1.1; }
.tony-header .t2 { font-size:.82rem; color:var(--muted); letter-spacing:.12em; }

/* Top nav (st.page_link) */
a[data-testid="stPageLink-NavLink"] {
  justify-content:center; text-align:center; border:1px solid var(--line); border-radius:10px;
  background: var(--panel); padding:.7rem .4rem; transition: all .15s ease;
}
a[data-testid="stPageLink-NavLink"] p { font-weight:700; letter-spacing:.06em; color:var(--muted); }
a[data-testid="stPageLink-NavLink"]:hover { border-color: var(--gold); background: var(--panel-2); }
a[data-testid="stPageLink-NavLink"]:hover p { color: var(--text); }
a[data-testid="stPageLink-NavLink"][aria-current="page"] {
  background: linear-gradient(135deg,#F5B942,#E08A1E); border-color: transparent;
  box-shadow: 0 6px 18px rgba(245,185,66,.25);
}
a[data-testid="stPageLink-NavLink"][aria-current="page"] p { color:#1A1203; }
.nav-divider { height:1px; background: var(--line); margin: .9rem 0 1.2rem; }

/* Cards (Google Form style) */
[class*="st-key-card-"] {
  background: var(--panel); border:1px solid var(--line); border-top:5px solid var(--gold);
  border-radius:12px; padding:1.1rem 1.3rem .8rem; margin-bottom:.4rem;
  box-shadow: 0 8px 24px rgba(0,0,0,.25);
}
[class*="st-key-card-teal"] { border-top-color: var(--teal); }
[class*="st-key-card-red"] { border-top-color: var(--red); }
[class*="st-key-card-blue"] { border-top-color: #60A5FA; }
.card-title { font-size:1.1rem; font-weight:700; color:var(--text); margin:0 0 .15rem; }
.card-sub { font-size:.82rem; color:var(--muted); margin-bottom:.6rem; }
.hint { font-size:.74rem; color:#6F7B94; margin:-.55rem 0 .9rem .1rem; }

/* Metric cards */
.mcard {
  background: var(--panel); border:1px solid var(--line); border-left:4px solid var(--gold);
  border-radius:12px; padding:1rem 1.1rem; height:100%; margin-bottom:.8rem;
  box-shadow: 0 6px 18px rgba(0,0,0,.22);
}
.mcard.teal { border-left-color: var(--teal); } .mcard.red { border-left-color: var(--red); }
.mcard.blue { border-left-color:#60A5FA; }
.mcard .lbl { color:var(--muted); font-size:.82rem; letter-spacing:.06em; }
.mcard .val { color:var(--text); font-size:1.65rem; font-weight:800; margin:.15rem 0; }
.mcard .sub { color:#6F7B94; font-size:.74rem; }

/* Benefit cards */
.benefit {
  background: linear-gradient(135deg,#1B2540,#121B2E); border:1px solid #3A4668; border-radius:14px;
  padding:1.2rem 1.3rem; height:100%;
}
.benefit.locked { opacity:.55; filter: grayscale(.6); }
.benefit .badge { display:inline-block; font-size:.7rem; padding:.15rem .6rem; border-radius:999px;
  background:rgba(245,185,66,.15); color:var(--gold); border:1px solid rgba(245,185,66,.4); margin-bottom:.5rem; }
.benefit .big { font-size:2.2rem; font-weight:800; color:var(--gold); }
.benefit .desc { color:var(--muted); font-size:.85rem; }

.section-title { font-size:1.2rem; font-weight:700; color:var(--text); margin:1.2rem 0 .6rem; }
.pill { display:inline-block; padding:.1rem .6rem; border-radius:999px; font-size:.78rem; color:#0B1220; font-weight:700; }
.ledger-row { display:flex; align-items:center; gap:.7rem; padding:.55rem .2rem; border-bottom:1px solid var(--line); }
</style>
"""


def inject_theme() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def render_header() -> None:
    logo_b64 = base64.b64encode(LOGO_SVG.encode()).decode()
    st.markdown(
        f"""
        <div class="tony-header">
          <img src="data:image/svg+xml;base64,{logo_b64}" alt="TONY終結者 Logo"/>
          <div>
            <div class="t1">TONY終結者</div>
            <div class="t2">RETIREMENT &amp; WEALTH DASHBOARD</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_nav(pages: Sequence[Any]) -> None:
    cols = st.columns(len(pages), gap="small")
    for col, page in zip(cols, pages):
        with col:
            st.page_link(page, label=page.title, width="stretch")
    st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 版面小元件
# ---------------------------------------------------------------------------


def card(name: str, accent: str = "gold"):
    """Google 表單風格卡片容器。accent: gold / teal / red / blue。"""
    return st.container(border=False, key=f"card-{accent}-{name}")


def card_title(title: str, subtitle: str = "") -> None:
    st.markdown(f'<div class="card-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="card-sub">{subtitle}</div>', unsafe_allow_html=True)


def metric_card(label: str, value: str, sub: str = "", accent: str = "gold") -> None:
    st.markdown(
        f'<div class="mcard {accent}"><div class="lbl">{label}</div>'
        f'<div class="val">{value}</div><div class="sub">{sub or "&nbsp;"}</div></div>',
        unsafe_allow_html=True,
    )


def fmt_money(value: float) -> str:
    return f"NT$ {value:,.0f}"


def median_hint(field_key: str, note: str = "") -> None:
    """欄位下方較小、較淡的中位數說明文字 (數據來自 math_models)。"""
    name, unit = mm.MEDIAN_FIELDS[field_key]
    median = mm.get_median(field_key, state.get("occupation"))
    if median is None:
        text = "待填入"
    elif unit == "元":
        text = f"{median:,.0f} 元"
    else:
        text = f"{median:g} {unit}"
    prefix = f"{note}　|　" if note else ""
    st.markdown(f'<div class="hint">{prefix}{name}中位數：{text}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 具跨頁同步的輸入元件
# ---------------------------------------------------------------------------


def num_input(label: str, key: str, *, hint: bool = True, note: str = "", **kwargs: Any) -> Any:
    state.bind(key)
    value = st.number_input(label, key=key, **kwargs)
    state.commit(key)
    if hint and key in mm.MEDIAN_FIELDS:
        median_hint(key, note)
    return value


def money_input(label: str, key: str, **kwargs: Any) -> Any:
    return num_input(label, key, min_value=0, step=1000, format="%d", **kwargs)


def pct_input(label: str, key: str, **kwargs: Any) -> Any:
    return num_input(label, key, min_value=0.0, max_value=100.0, step=0.1, format="%.1f", **kwargs)


def slider(label: str, key: str, min_value: Any, max_value: Any, *, hint: bool = True, **kwargs: Any) -> Any:
    state.bind(key)
    value = st.slider(label, min_value, max_value, key=key, **kwargs)
    state.commit(key)
    if hint and key in mm.MEDIAN_FIELDS:
        median_hint(key)
    return value


def checkbox(label: str, key: str, **kwargs: Any) -> bool:
    state.bind(key)
    value = st.checkbox(label, key=key, **kwargs)
    state.commit(key)
    return value


def select(label: str, key: str, options: Sequence[Any], **kwargs: Any) -> Any:
    state.bind(key)
    value = st.selectbox(label, options, key=key, **kwargs)
    state.commit(key)
    return value
