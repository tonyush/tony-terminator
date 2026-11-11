"""記帳面板 — 條列式記帳與月收支圓餅圖。"""

import uuid

import plotly.graph_objects as go
import streamlit as st

from utils import math_models as mm
from utils import state, ui

CATEGORIES = ["餐飲", "交通", "居住", "醫療", "保險", "娛樂", "教育", "薪資", "投資", "其他"]

st.markdown("### 記帳面板")
st.caption("左側為你的日常記帳；右側圓餅圖會自動帶入【人生終結者】的月收支。")

entries = state.ledger()


def _add_entry() -> None:
    amount = st.session_state.get("lg_amount", 0)
    if not amount:
        return
    state.ledger().append(
        {
            "id": uuid.uuid4().hex[:8],
            "color": st.session_state["lg_color"],
            "category": st.session_state["lg_category"],
            "desc": st.session_state["lg_desc"].strip(),
            "amount": amount,
            "kind": st.session_state["lg_kind"],
        }
    )
    st.session_state["lg_desc"] = ""
    st.session_state["lg_amount"] = 0


def _delete_entry(entry_id: str) -> None:
    state._store()["ledger"] = [e for e in state.ledger() if e["id"] != entry_id]


left, right = st.columns([1.15, 1], gap="large")

with left:
    with ui.card("ledger-add", "gold"):
        ui.card_title("新增一筆", "顏色標籤可用來自訂分群，例如紅色代表必要支出")
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            st.selectbox("顏色標籤", list(ui.COLOR_TAGS), key="lg_color")
        with c2:
            st.selectbox("標籤類別", CATEGORIES, key="lg_category")
        with c3:
            st.radio("收支", ["支出", "收入"], key="lg_kind", horizontal=True)
        c4, c5 = st.columns([2, 1])
        with c4:
            st.text_input("文字描述", key="lg_desc", placeholder="例如：午餐、水電費")
        with c5:
            st.number_input("金額", key="lg_amount", min_value=0, step=100, format="%d")
        st.button("＋ 新增記帳", on_click=_add_entry, type="primary")

    with ui.card("ledger-list", "teal"):
        ui.card_title("記帳明細", f"共 {len(entries)} 筆")
        if not entries:
            st.info("還沒有任何記帳紀錄，從上方新增第一筆吧。")
        for entry in reversed(entries):
            c1, c2, c3, c4 = st.columns([0.8, 3, 1.6, 0.9], vertical_alignment="center")
            color = ui.COLOR_TAGS.get(entry["color"], "#9CA3AF")
            c1.markdown(
                f'<span class="pill" style="background:{color}">{entry["category"]}</span>',
                unsafe_allow_html=True,
            )
            c2.markdown(entry["desc"] or "—")
            sign, tone = ("+", "#2DD4BF") if entry["kind"] == "收入" else ("-", "#F87171")
            c3.markdown(
                f'<span style="color:{tone};font-weight:700">{sign}{entry["amount"]:,.0f}</span>',
                unsafe_allow_html=True,
            )
            c4.button("刪除", key=f"lg_del_{entry['id']}", on_click=_delete_entry, args=(entry["id"],))

        if entries:
            total_in = sum(e["amount"] for e in entries if e["kind"] == "收入")
            total_out = sum(e["amount"] for e in entries if e["kind"] == "支出")
            m1, m2, m3 = st.columns(3)
            m1.metric("記帳收入", ui.fmt_money(total_in))
            m2.metric("記帳支出", ui.fmt_money(total_out))
            m3.metric("結餘", ui.fmt_money(total_in - total_out))

with right:
    with ui.card("ledger-pie", "blue"):
        ui.card_title("月收支圖表", "資料來源：人生終結者 + 調控 / 資金面板")
        flow = mm.calc_monthly_cashflow(state.profile(), state.principal(), state.get("return_rate"))
        fig = go.Figure(
            go.Pie(
                labels=list(flow),
                values=list(flow.values()),
                hole=0.5,
                marker=dict(colors=["#F5B942", "#2DD4BF", "#60A5FA", "#F87171"], line=dict(color="#0B1220", width=2)),
                textinfo="label+percent",
                hovertemplate="%{label}<br>NT$ %{value:,.0f}<extra></extra>",
            )
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10, b=10, l=10, r=10),
            height=340,
            legend=dict(orientation="h", y=-0.05),
        )
        st.plotly_chart(fig, width="stretch")

        income = flow["月利息"] + flow["薪資收入"] + flow["其他收入"]
        c1, c2 = st.columns(2)
        c1.metric("月總收入", ui.fmt_money(income))
        c2.metric("月結餘", ui.fmt_money(income - flow["支出"]))
