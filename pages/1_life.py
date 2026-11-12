"""人生終結者 — 基本資料與參數表單 (Google 表單卡片風格)。"""

import plotly.graph_objects as go
import streamlit as st

from utils import math_models as mm
from utils import state, ui
from utils.i18n import _

title_col, bank_col = st.columns([4, 1.4], vertical_alignment="center")
with title_col:
    st.markdown(f"### {_('人生終結者')}")
    st.caption(_("填寫你的人生參數，其他面板會自動同步使用這些資料。金額單位為新台幣元。"))
with bank_col:
    ui.bank_sync_button("bank_sync_life")

# ---------------------------------------------------------------- 基礎參數
with ui.card("basic", "gold"):
    ui.card_title(_("基礎參數"), _("職業會連動下方各欄位的中位數參考數據"))

    left, right = st.columns(2, gap="large")
    with left:
        ui.radio(_("性別"), "gender", ["男", "女"], horizontal=True)
    with right:
        occupation = ui.select(_("職業"), "occupation", mm.OCCUPATIONS)

    retired = ui.checkbox(_("已退休"), "retired")

    left, right = st.columns(2, gap="large")
    with left:
        ui.slider("age", 0, 100)
        ui.slider("retire_age", 0, 100)
        ui.money_input("cash", note=_("現金或存款"))
    with right:
        if occupation == mm.STUDENT_OCCUPATION:
            ui.money_input("tuition")
        ui.slider("health", 0, 100)
        ui.slider("death_age", 0, 100)
        ui.slider("invest_ratio", 0, 100)

# ---------------------------------------------------------------- 收入
with ui.card("income", "teal"):
    ui.card_title(_("收入列表"), _("已退休時，年薪相關欄位會自動隱藏"))
    if not retired:
        left, right = st.columns(2, gap="large")
        with left:
            ui.money_input("salary")
            ui.pct_input("salary_vol")
        with right:
            ui.pct_input("salary_growth")
            ui.money_input("side_income")
    else:
        ui.money_input("side_income")

    with st.expander(_("查看未來收入推估預覽")):
        projection = mm.calculate_projected_income(
            state.get("salary"),
            state.get("salary_growth"),
            state.get("salary_vol"),
            state.get("side_income"),
            state.get("age"),
            state.get("retire_age"),
            state.get("retired"),
        )
        # TODO: 請在 math_models.calculate_projected_income 導入薪資邊際收斂公式，此預覽會自動更新
        st.caption(_("目前為示意數據 (固定成長率)，薪資邊際收斂公式待填入。"))
        fig = go.Figure(
            go.Scatter(
                x=projection["ages"],
                y=projection["income"],
                mode="lines",
                line=dict(color="#2DD4BF", width=3),
                fill="tozeroy",
                fillcolor="rgba(45,212,191,0.12)",
                hovertemplate="%{x}<br>NT$ %{y:,.0f}<extra></extra>",
            )
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10, b=10, l=10, r=10),
            height=260,
            xaxis_title=_("年紀"),
            yaxis_title=_("年收入"),
        )
        st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------- 支出
with ui.card("expense", "red"):
    ui.card_title(_("支出列表"), _("以「月」為單位"))

    mode = ui.radio(
        _("月固定支出"),
        "fixed_exp_mode",
        ["total", "itemized"],
        horizontal=True,
        format_func=lambda m: _("總額輸入") if m == "total" else _("細項加總"),
    )
    if mode == "total":
        ui.money_input("fixed_exp_total")
        fixed_total = state.get("fixed_exp_total")
    else:
        left, right = st.columns(2, gap="large")
        with left:
            ui.money_input("fe_food")
            ui.money_input("fe_entertain")
            ui.money_input("fe_other")
        with right:
            ui.money_input("fe_transit")
            ui.money_input("fe_subscription")
        fixed_total = sum(state.get(k) for k in ("fe_food", "fe_transit", "fe_entertain", "fe_subscription", "fe_other"))
        st.write(f"{_('細項加總金額')}：NT$ {fixed_total:,.0f}")
    state.set_value("fixed_exp", fixed_total)

    left, right = st.columns(2, gap="large")
    with left:
        ui.money_input("insurance_exp")
        ui.money_input("rent_exp")
    with right:
        ui.money_input("medical_exp")

# ---------------------------------------------------------------- 家庭
with ui.card("family", "red"):
    ui.card_title(_("家庭支出"), _("每個成員填入數量與年花費金額 (每人每年)"))
    for item in mm.FAMILY_ITEMS:
        left, right = st.columns([1, 2], gap="large")
        with left:
            ui.int_input(f"family_{item}_n")
        with right:
            ui.money_input(f"family_{item}_cost")
    ui.money_input("family_exp", note=_("每月其他家庭開銷"))
    family_total = mm.calc_family_expense(state.profile())
    state.set_value("family_total", family_total)
    st.write(f"{_('家庭月支出總額')}：NT$ {family_total:,.0f}")


# ---------------------------------------------------------------- 交通工具 / 房子
def vehicle_card(prefix: str, no_key: str, title: str, no_label: str) -> None:
    with ui.card(prefix, "blue"):
        ui.card_title(_(title), _("貸款月繳額、使用成本以月計；持有成本以年計"))
        if not ui.checkbox(_(no_label), no_key):
            left, right = st.columns(2, gap="large")
            with left:
                ui.money_input(f"{prefix}_loan")
                ui.money_input(f"{prefix}_use_cost")
            with right:
                ui.money_input(f"{prefix}_value")
                ui.money_input(f"{prefix}_cost")


vehicle_card("car", "no_car", "車子", "無車子")
vehicle_card("moto", "no_moto", "摩托車", "無摩托車")
vehicle_card("special", "no_special", "特殊交通工具", "無特殊交通工具")

with ui.card("house", "blue"):
    ui.card_title(_("房子"), _("貸款月繳額以月計；持有成本以年計"))
    if not ui.checkbox(_("無房子"), "no_house"):
        left, right = st.columns(2, gap="large")
        with left:
            ui.money_input("house_loan")
            ui.money_input("house_cost")
        with right:
            ui.money_input("house_value")

# ---------------------------------------------------------------- 重大事件
with ui.card("events", "gold"):
    ui.card_title(_("重大事件"), _("例如子女教育、換屋、長照準備等，可自由新增多筆"))

    events = state.events()

    if events:
        h1, h2, h3, h4 = st.columns([3, 2, 2, 1])
        h1.caption(_("事件名稱"))
        h2.caption(_("發生時間 / 年紀"))
        h3.caption(_("金額"))

    for event in events:
        eid = event["id"]
        c1, c2, c3, c4 = st.columns([3, 2, 2, 1], vertical_alignment="center")
        for field, default in (("name", event["name"]), ("age", event["age"]), ("amt", event["amount"])):
            st.session_state.setdefault(f"ev_{field}_{eid}", default)
        with c1:
            st.text_input(_("事件名稱"), key=f"ev_name_{eid}", label_visibility="collapsed", placeholder=_("事件名稱"))
        with c2:
            st.number_input(_("發生時間 / 年紀"), key=f"ev_age_{eid}", min_value=0, max_value=100, step=1, label_visibility="collapsed")
        with c3:
            st.number_input(_("金額"), key=f"ev_amt_{eid}", step=1000, format="%d", label_visibility="collapsed")
        with c4:
            st.button(_("刪除"), key=f"ev_del_{eid}", on_click=state.delete_event, args=(eid,), width="stretch")
        event["name"] = st.session_state[f"ev_name_{eid}"]
        event["age"] = st.session_state[f"ev_age_{eid}"]
        event["amount"] = st.session_state[f"ev_amt_{eid}"]

    if not events:
        st.info(_("目前沒有重大事件，點擊下方按鈕新增第一筆。"))
    st.button(
        _("＋ 新增事件"),
        on_click=state.add_event,
        kwargs={"age": int(state.get("age"))},
        type="primary",
    )
