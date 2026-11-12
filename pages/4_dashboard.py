"""數據面板 — Metric Cards、利率敏感度、現金流折線圖、債券組合、重大事件彙總。"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import market_data
from utils import math_models as mm
from utils import state, ui
from utils.i18n import _

PLOT_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)

st.markdown(f"### {_('數據面板')}")
st.caption(_("所有數字皆由【人生終結者】、【調控面板】與【資金面板】的設定自動計算。"))

p = state.profile()
principal = state.principal()
rate = p["return_rate"]
inflation = mm.get_current_inflation_rate()
flow = mm.calc_monthly_cashflow(p, principal, rate)
sens = mm.calc_rate_sensitivity(rate, p["allow_leverage"])
beat = mm.calc_beat_inflation_rate(rate, inflation)
years = mm.calc_years_to_work(p["age"], p["retire_age"], p["retired"], principal, flow["支出"], rate)

cards = [
    (_("日利息結餘"), ui.fmt_money(mm.calc_daily_interest_balance(principal, rate)), _("累積未領利息"), "gold"),
    (
        _("本金金額"),
        ui.fmt_money(principal),
        _("原本資金 {cash} + 投入 {invest}").format(cash=f"{p['cash']:,.0f}", invest=f"{p['invest_amount']:,.0f}"),
        "gold",
    ),
    (_("現在報酬率"), f"{rate:.1f}%", f"{_('通膨率')} {inflation:.1f}%", "teal"),
    (_("通膨超越率"), f"{beat:+.1f}%", _("報酬率 − 通膨率"), "teal" if beat >= 0 else "red"),
    (_("日領息額"), ui.fmt_money(mm.calc_daily_interest(principal, rate)), _("每日可領利息"), "gold"),
    (
        _("所需工作年數"),
        _("已退休") if p["retired"] else _("{n} 年").format(n=f"{years:.1f}"),
        _("預計 {age} 歲退休").format(age=p["retire_age"]),
        "blue",
    ),
    (_("修正存續期間 Duration"), f"{sens['duration']:.2f}", _("利率敏感度"), "blue"),
    (_("凸性 Convexity"), f"{sens['convexity']:.2f}", _("利率敏感度"), "blue"),
]
for row in range(0, len(cards), 4):
    cols = st.columns(4, gap="medium")
    for col, (label, value, sub, accent) in zip(cols, cards[row : row + 4]):
        with col:
            ui.metric_card(label, value, sub, accent)

# ---------------------------------------------------------------- 折線圖
with ui.card("trend", "teal"):
    ui.card_title(_("收支與利息趨勢"), _("X 軸為年紀，Y 軸為年度金額"))
    series = mm.calc_lifetime_series(p, principal, rate, inflation)
    fig = go.Figure()
    for name, color in (("總收入", "#2DD4BF"), ("總支出", "#F87171"), ("利息", "#F5B942")):
        fig.add_trace(
            go.Scatter(
                x=series["ages"],
                y=series[name],
                name=_(name),
                mode="lines",
                line=dict(color=color, width=3),
                hovertemplate=f"{_(name)}<br>%{{x}}<br>NT$ %{{y:,.0f}}<extra></extra>",
            )
        )
    fig.update_layout(
        **PLOT_LAYOUT,
        margin=dict(t=10, b=10, l=10, r=10),
        height=360,
        xaxis_title=_("年紀"),
        yaxis_title=_("金額 (NT$)"),
        legend=dict(orientation="h", y=1.1),
        hovermode="x unified",
    )
    st.plotly_chart(fig, width="stretch")

left, right = st.columns([1, 1], gap="large")

with left:
    with ui.card("bond", "gold"):
        ui.card_title(_("債券組合型式"), _("各評級債券配置比例"))
        market_weights = market_data.fetch_yfinance_bond_data()
        portfolio = mm.calc_bond_portfolio(
            rate,
            p["capital_protected"],
            p["unprotected_ratio"],
            p["allow_foreign_gov"],
            p["allow_foreign_corp"],
            p["allow_junk"],
            p["allow_leverage"],
            market_weights,
        )
        portfolio = {k: v for k, v in portfolio.items() if v > 0}
        fig = go.Figure(
            go.Pie(
                labels=[_(k) for k in portfolio],
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
            **PLOT_LAYOUT,
            margin=dict(t=10, b=10, l=10, r=10),
            height=340,
            legend=dict(orientation="h", y=-0.08),
        )
        st.plotly_chart(fig, width="stretch")

with right:
    with ui.card("events", "red"):
        ui.card_title(_("重大事件彙總"), _("來源：人生終結者"))
        events = [e for e in state.events() if e["name"].strip() or e["amount"]]
        if events:
            col_name, col_age, col_amount = _("事件名稱"), _("發生年紀"), _("金額")
            df = pd.DataFrame(
                {
                    col_name: [e["name"] or _("(未命名)") for e in events],
                    col_age: [e["age"] for e in events],
                    col_amount: [e["amount"] for e in events],
                }
            ).sort_values(col_age)
            st.dataframe(
                df,
                hide_index=True,
                width="stretch",
                column_config={
                    col_age: st.column_config.NumberColumn(format=_("%d 歲")),
                    col_amount: st.column_config.NumberColumn(format="NT$ %d"),
                },
            )
        else:
            st.info(_("尚未設定重大事件，請至【人生終結者】新增。"))
        total = sum(e["amount"] for e in events)
        ui.metric_card(_("總額"), ui.fmt_money(total), _("共 {n} 件重大事件").format(n=len(events)), "red")
