"""記帳面板 — 條列式記帳、月收支圓餅圖與 Excel 匯出。"""

import io
import uuid

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import math_models as mm
from utils import state, ui
from utils.i18n import _

CATEGORIES = ["餐飲", "交通", "居住", "醫療", "保險", "娛樂", "教育", "薪資", "投資", "其他"]
KINDS = ["支出", "收入"]

st.markdown(f"### {_('記帳面板')}")
st.caption(_("左側為你的日常記帳；右側圓餅圖會自動帶入【人生終結者】的月收支，並加總記帳表。"))

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


def _to_excel(logs: list[dict]) -> bytes:
    # TODO: 需要在 requirements.txt 加入 openpyxl (pandas.to_excel 的 xlsx 引擎)
    frame = pd.DataFrame(
        {
            _("類型"): [_(e["kind"]) for e in logs],
            _("顏色標籤"): [e["color"] for e in logs],
            _("標籤類別"): [_(e["category"]) for e in logs],
            _("文字描述"): [e["desc"] for e in logs],
            _("金額"): [e["amount"] for e in logs],
        }
    )
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        frame.to_excel(writer, index=False, sheet_name=_("記帳面板"))
    return buffer.getvalue()


left, right = st.columns([1.15, 1], gap="large")

with left:
    with ui.card("ledger-add", "gold"):
        ui.card_title(_("新增一筆"), _("顏色標籤可用來自訂分群，例如紅色代表必要支出"))
        st.radio(_("類型"), KINDS, key="lg_kind", horizontal=True, format_func=_)
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox(_("顏色標籤"), list(ui.COLOR_TAGS), key="lg_color", format_func=_)
        with c2:
            st.selectbox(_("標籤類別"), CATEGORIES, key="lg_category", format_func=_)
        c4, c5 = st.columns([2, 1])
        with c4:
            st.text_input(_("文字描述"), key="lg_desc", placeholder=_("例如：午餐、水電費"))
        with c5:
            st.number_input(_("金額"), key="lg_amount", min_value=0, step=100, format="%d")
        st.button(_("＋ 新增記帳"), on_click=_add_entry, type="primary")

    with ui.card("ledger-list", "teal"):
        ui.card_title(_("記帳明細"), _("共 {n} 筆").format(n=len(entries)))
        if not entries:
            st.info(_("還沒有任何記帳紀錄，從上方新增第一筆吧。"))
        for entry in reversed(entries):
            c1, c2, c3, c4 = st.columns([1.1, 2.6, 1.5, 0.9], vertical_alignment="center")
            color = ui.COLOR_TAGS.get(entry["color"], "#9CA3AF")
            c1.markdown(
                f'<span class="pill" style="background:{color}">{_(entry["category"])}</span>',
                unsafe_allow_html=True,
            )
            c2.markdown(f'{_(entry["kind"])}　{entry["desc"] or "—"}')
            sign, tone = ("+", "#2DD4BF") if entry["kind"] == "收入" else ("-", "#F87171")
            c3.markdown(
                f'<span style="color:{tone};font-weight:700">{sign}{entry["amount"]:,.0f}</span>',
                unsafe_allow_html=True,
            )
            c4.button(_("刪除"), key=f"lg_del_{entry['id']}", on_click=state.delete_ledger_entry, args=(entry["id"],))

        if entries:
            total_in = sum(e["amount"] for e in entries if e["kind"] == "收入")
            total_out = sum(e["amount"] for e in entries if e["kind"] == "支出")
            m1, m2, m3 = st.columns(3)
            m1.metric(_("記帳收入"), ui.fmt_money(total_in))
            m2.metric(_("記帳支出"), ui.fmt_money(total_out))
            m3.metric(_("結餘"), ui.fmt_money(total_in - total_out))

        try:
            st.download_button(
                _("⬇ 匯出 Excel"),
                data=_to_excel(entries) if entries else b"",
                file_name="tony_accounting_logs.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                disabled=not entries,
                key="lg_download",
            )
        except ImportError:
            st.warning(_("匯出 Excel 需要 openpyxl，請在 requirements.txt 加入 openpyxl 後重新安裝。"))

with right:
    with ui.card("ledger-pie", "blue"):
        ui.card_title(_("月收支圖表"), _("資料來源：人生終結者 + 記帳表 + 調控 / 資金面板"))
        flow = mm.calc_monthly_cashflow(state.profile(), state.principal(), state.get("return_rate"), entries)
        slice_keys = ["月利息", "薪資收入", "副業收入", "記帳收入", "支出"]
        slice_colors = ["#F5B942", "#2DD4BF", "#60A5FA", "#A78BFA", "#F87171"]
        shown = [(k, c) for k, c in zip(slice_keys, slice_colors) if flow[k] > 0]
        fig = go.Figure(
            go.Pie(
                labels=[_(k) for k, _c in shown],
                values=[flow[k] for k, _c in shown],
                hole=0.5,
                marker=dict(colors=[c for _k, c in shown], line=dict(color="#0B1220", width=2)),
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

        c1, c2 = st.columns(2)
        c1.metric(_("月總收入"), ui.fmt_money(flow["總收入"]))
        c2.metric(_("月總支出"), ui.fmt_money(flow["總支出"]))
        c3, c4 = st.columns(2)
        c3.metric(_("月利息"), ui.fmt_money(flow["月利息"]))
        c4.metric(_("月結餘"), ui.fmt_money(flow["總收入"] + flow["月利息"] - flow["總支出"]))
