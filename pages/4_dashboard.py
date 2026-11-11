"""數據面板 — Metric Cards、利率敏感度、債券組合、重大事件彙總。"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import math_models as mm
from utils import state, ui

st.markdown("### 數據面板")
st.caption("所有數字皆由【人生終結者】、【調控面板】與【資金面板】的設定自動計算。")

p = state.profile()
principal = state.principal()
rate = p["return_rate"]
inflation = mm.get_current_inflation_rate()
flow = mm.calc_monthly_cashflow(p, principal, rate)
sens = mm.calc_rate_sensitivity(rate, p["allow_leverage"])
beat = mm.calc_beat_inflation_rate(rate, inflation)
years = mm.calc_years_to_work(p["age"], p["retire_age"], p["retired"], principal, flow["支出"], rate)

cards = [
    ("日利息結餘", ui.fmt_money(mm.calc_daily_interest_balance(principal, rate)), "累積未領利息", "gold"),
    ("本金金額", ui.fmt_money(principal), f"原本資金 {p['cash']:,.0f} + 投入 {p['invest_amount']:,.0f}", "gold"),
    ("現在報酬率", f"{rate:.1f}%", f"通膨率 {inflation:.1f}%", "teal"),
    ("通膨超越率", f"{beat:+.1f}%", "報酬率 − 通膨率", "teal" if beat >= 0 else "red"),
    ("日領息額", ui.fmt_money(mm.calc_daily_interest(principal, rate)), "每日可領利息", "gold"),
    ("所需工作年數", "已退休" if p["retired"] else f"{years:.1f} 年", f"預計 {p['retire_age']} 歲退休", "blue"),
    ("修正存續期間 Duration", f"{sens['duration']:.2f}", "利率敏感度", "blue"),
    ("凸性 Convexity", f"{sens['convexity']:.2f}", "利率敏感度", "blue"),
]
for row in range(0, len(cards), 4):
    cols = st.columns(4, gap="medium")
    for col, (label, value, sub, accent) in zip(cols, cards[row : row + 4]):
        with col:
            ui.metric_card(label, value, sub, accent)

left, right = st.columns([1, 1], gap="large")

with left:
    with ui.card("bond", "gold"):
        ui.card_title("債券組合型式", "各評級債券配置比例")
        portfolio = mm.calc_bond_portfolio(
            rate,
            p["capital_protected"],
            p["unprotected_ratio"],
            p["allow_foreign_gov"],
            p["allow_foreign_corp"],
            p["allow_junk"],
            p["allow_leverage"],
        )
        portfolio = {k: v for k, v in portfolio.items() if v > 0}
        fig = go.Figure(
            go.Pie(
                labels=list(portfolio),
                values=list(portfolio.values()),
                hole=0.5,
                marker=dict(
                    colors=["#F5B942", "#2DD4BF", "#60A5FA", "#A78BFA", "#F87171"],
                    line=dict(color="#0B1220", width=2),
                ),
                textinfo="percent",
                hovertemplate="%{label}<br>%{value:.1f}%<extra></extra>",
            )
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10, b=10, l=10, r=10),
            height=340,
            legend=dict(orientation="h", y=-0.08),
        )
        st.plotly_chart(fig, width="stretch")

with right:
    with ui.card("events", "red"):
        ui.card_title("重大事件彙總", "來源：人生終結者")
        events = [e for e in state.events() if e["name"].strip() or e["amount"]]
        if events:
            df = pd.DataFrame(
                {
                    "事件名稱": [e["name"] or "(未命名)" for e in events],
                    "發生年紀": [e["age"] for e in events],
                    "金額": [e["amount"] for e in events],
                }
            ).sort_values("發生年紀")
            st.dataframe(
                df,
                hide_index=True,
                width="stretch",
                column_config={
                    "發生年紀": st.column_config.NumberColumn(format="%d 歲"),
                    "金額": st.column_config.NumberColumn(format="NT$ %d"),
                },
            )
        else:
            st.info("尚未設定重大事件，請至【人生終結者】新增。")
        total = sum(e["amount"] for e in events)
        ui.metric_card("總額", ui.fmt_money(total), f"共 {len(events)} 件重大事件", "red")
