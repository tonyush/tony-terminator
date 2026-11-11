"""人生終結者 — 基本資料與參數表單 (Google 表單卡片風格)。"""

import uuid

import streamlit as st

from utils import math_models as mm
from utils import state, ui

st.markdown("### 人生終結者")
st.caption("填寫你的人生參數，其他面板會自動同步使用這些資料。金額單位為新台幣元。")

# ---------------------------------------------------------------- 基礎參數
with ui.card("basic", "gold"):
    ui.card_title("基礎參數", "職業會連動下方各欄位的中位數參考數據")

    left, right = st.columns(2, gap="large")
    with left:
        state.bind("gender")
        st.radio("性別", ["男", "女"], key="gender", horizontal=True)
        state.commit("gender")
    with right:
        ui.select("職業", "occupation", mm.OCCUPATIONS)

    retired = ui.checkbox("已退休", "retired")

    left, right = st.columns(2, gap="large")
    with left:
        ui.slider("年紀", "age", 0, 100)
        ui.slider("預估退休年紀", "retire_age", 0, 100)
        ui.money_input("現金資產", "cash", note="現金或存款")
    with right:
        ui.slider("健康狀態程度 (%)", "health", 0, 100)
        ui.slider("預估死亡年紀", "death_age", 0, 100)
        ui.slider("願意投入資金比例 (%)", "invest_ratio", 0, 100)

# ---------------------------------------------------------------- 收入
with ui.card("income", "teal"):
    ui.card_title("收入列表", "已退休時，年薪相關欄位會自動隱藏")
    if not retired:
        left, right = st.columns(2, gap="large")
        with left:
            ui.money_input("年薪", "salary")
            ui.pct_input("年薪波動率 (%)", "salary_vol")
        with right:
            ui.pct_input("年薪增長率 (%)", "salary_growth")
            ui.money_input("副業收入", "side_income")
    else:
        ui.money_input("副業收入", "side_income")

# ---------------------------------------------------------------- 支出
with ui.card("expense", "red"):
    ui.card_title("支出列表", "以「月」為單位")
    left, right = st.columns(2, gap="large")
    with left:
        ui.money_input("月固定支出", "fixed_exp")
        ui.money_input("家庭支出", "family_exp")
        ui.money_input("租金支出", "rent_exp")
    with right:
        ui.money_input("保險支出", "insurance_exp")
        ui.money_input("醫療支出", "medical_exp")

# ---------------------------------------------------------------- 車子
with ui.card("car", "blue"):
    ui.card_title("車子")
    if not ui.checkbox("無車子", "no_car"):
        left, right = st.columns(2, gap="large")
        with left:
            ui.money_input("車貸", "car_loan")
            ui.money_input("車持有成本 (年)", "car_cost")
        with right:
            ui.money_input("車的價值", "car_value")

# ---------------------------------------------------------------- 房子
with ui.card("house", "blue"):
    ui.card_title("房子")
    if not ui.checkbox("無房子", "no_house"):
        left, right = st.columns(2, gap="large")
        with left:
            ui.money_input("房貸", "house_loan")
            ui.money_input("終值", "house_final_value")
        with right:
            ui.money_input("房的價值", "house_value")

# ---------------------------------------------------------------- 重大事件
with ui.card("events", "gold"):
    ui.card_title("重大事件", "例如子女教育、換屋、長照準備等，可自由新增多筆")

    events = state.events()

    def _delete_event(event_id: str) -> None:
        state._store()["events"] = [e for e in state.events() if e["id"] != event_id]

    def _add_event() -> None:
        state.events().append({"id": uuid.uuid4().hex[:8], "name": "", "age": int(state.get("age")), "amount": 0})

    if events:
        h1, h2, h3, h4 = st.columns([3, 2, 2, 1])
        h1.caption("事件名稱")
        h2.caption("發生時間 / 年紀")
        h3.caption("金額")

    for event in events:
        eid = event["id"]
        c1, c2, c3, c4 = st.columns([3, 2, 2, 1], vertical_alignment="center")
        for field, default in (("name", event["name"]), ("age", event["age"]), ("amt", event["amount"])):
            st.session_state.setdefault(f"ev_{field}_{eid}", default)
        with c1:
            st.text_input("事件名稱", key=f"ev_name_{eid}", label_visibility="collapsed", placeholder="事件名稱")
        with c2:
            st.number_input("發生年紀", key=f"ev_age_{eid}", min_value=0, max_value=100, step=1, label_visibility="collapsed")
        with c3:
            st.number_input("金額", key=f"ev_amt_{eid}", step=1000, format="%d", label_visibility="collapsed")
        with c4:
            st.button("刪除", key=f"ev_del_{eid}", on_click=_delete_event, args=(eid,), width="stretch")
        event["name"] = st.session_state[f"ev_name_{eid}"]
        event["age"] = st.session_state[f"ev_age_{eid}"]
        event["amount"] = st.session_state[f"ev_amt_{eid}"]

    if not events:
        st.info("目前沒有重大事件，點擊下方按鈕新增第一筆。")
    st.button("＋ 新增事件", on_click=_add_event, type="primary")
