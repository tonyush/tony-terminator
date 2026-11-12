"""跨頁面資料同步層 (st.session_state)。

Streamlit 在切換頁面時會清掉「該頁沒有渲染」的 widget key，
所以這裡用一份 `_store` 作為單一資料來源：
  * 每個 widget 渲染前，若 key 不存在就從 `_store` 還原 (bind)。
  * 每個 widget 渲染後，把最新值寫回 `_store`。
  * 其他頁面 (記帳 / 數據面板) 透過 `get()` 直接讀取 `_store`。
"""

from __future__ import annotations

import uuid
from datetime import date
from typing import Any

import streamlit as st

DEFAULTS: dict[str, Any] = {
    # 人生終結者 - 基礎參數
    "gender": "男",
    "retired": False,
    "age": 50,
    "occupation": "金融業",
    "tuition": 60_000,
    "health": 80,
    "cash": 3_000_000,
    "death_age": 85,
    "retire_age": 65,
    "invest_ratio": 60,
    # 收入
    "salary": 1_200_000,
    "salary_growth": 2.5,
    "salary_vol": 5.0,
    "side_income": 120_000,
    # 支出 (月)
    "fixed_exp_mode": "total",
    "fixed_exp_total": 35_000,
    "fe_food": 12_000,
    "fe_transit": 3_000,
    "fe_entertain": 5_000,
    "fe_subscription": 2_000,
    "fe_other": 13_000,
    "fixed_exp": 35_000,  # 目前模式下的最終月總額 (由人生終結者面板寫入)
    "insurance_exp": 8_000,
    "medical_exp": 3_000,
    "rent_exp": 0,
    # 家庭 (數量 / 年花費)
    "family_exp": 0,
    "family_child_n": 1,
    "family_child_cost": 120_000,
    "family_elder_n": 0,
    "family_elder_cost": 150_000,
    "family_pet_n": 0,
    "family_pet_cost": 30_000,
    "family_spouse_n": 1,
    "family_spouse_cost": 120_000,
    "family_total": 0,  # 家庭月支出總額 (由人生終結者面板寫入)
    # 車子
    "no_car": False,
    "car_loan": 0,
    "car_value": 600_000,
    "car_use_cost": 5_000,
    "car_cost": 25_000,
    # 摩托車
    "no_moto": True,
    "moto_loan": 0,
    "moto_value": 60_000,
    "moto_use_cost": 1_000,
    "moto_cost": 3_000,
    # 特殊交通工具
    "no_special": True,
    "special_loan": 0,
    "special_value": 500_000,
    "special_use_cost": 3_000,
    "special_cost": 10_000,
    # 房子
    "no_house": False,
    "house_loan": 25_000,
    "house_value": 18_000_000,
    "house_cost": 30_000,
    # 調控面板
    "return_rate": 4.5,
    "capital_protected": True,
    "unprotected_ratio": 20,
    "allow_foreign_gov": True,
    "allow_foreign_corp": False,
    "allow_junk": False,
    "allow_leverage": False,
    # 資金面板
    "invest_amount": 1_000_000,
    "invest_mode": "今日投入",
    "invest_date": date.today(),
    "periodic_freq": "每月",
    "periodic_end": date.today().replace(year=date.today().year + 5),
    "card_holder": True,
    "early_claims_used": 0,
}


def _default_events() -> list[dict[str, Any]]:
    return [
        {"id": uuid.uuid4().hex[:8], "name": "子女大學學費", "age": 55, "amount": 1_200_000},
        {"id": uuid.uuid4().hex[:8], "name": "房貸結清", "age": 62, "amount": 3_000_000},
    ]


def init_session_state() -> None:
    """啟動時補齊全站 session 變數的預設值 (可重複呼叫，不覆蓋既有值)，避免 KeyError。"""
    ss = st.session_state
    if "language" not in ss:
        ss["language"] = "zh"
    if "user_profile" not in ss:
        ss["user_profile"] = {}
    profile_store = ss["user_profile"]
    for key, value in DEFAULTS.items():
        profile_store.setdefault(key, value)
    if "events" not in profile_store:
        profile_store["events"] = _default_events()
    if "accounting_logs" not in ss:
        ss["accounting_logs"] = []


def _store() -> dict[str, Any]:
    init_session_state()
    return st.session_state["user_profile"]


def get(key: str) -> Any:
    store = _store()
    return store.get(key, DEFAULTS.get(key))


def bind(key: str) -> None:
    """widget 渲染前呼叫：key 不在 session_state 時從 store 還原。"""
    if key not in st.session_state:
        st.session_state[key] = get(key)


def commit(key: str) -> Any:
    """widget 渲染後呼叫：把 widget 目前值寫回 store。"""
    _store()[key] = st.session_state[key]
    return st.session_state[key]


def set_value(key: str, value: Any) -> None:
    """程式端強制修改 (例如報酬率被上限夾住)。"""
    st.session_state[key] = value
    _store()[key] = value


def events() -> list[dict[str, Any]]:
    return _store()["events"]


def add_event(name: str = "", age: int = 0, amount: int = 0) -> None:
    events().append({"id": uuid.uuid4().hex[:8], "name": name, "age": age, "amount": amount})


def delete_event(event_id: str) -> None:
    events()[:] = [e for e in events() if e["id"] != event_id]


def ledger() -> list[dict[str, Any]]:
    """記帳明細 (= st.session_state.accounting_logs)。"""
    init_session_state()
    return st.session_state["accounting_logs"]


def delete_ledger_entry(entry_id: str) -> None:
    ledger()[:] = [e for e in ledger() if e["id"] != entry_id]


def profile() -> dict[str, Any]:
    """回傳全站目前所有欄位 (人生終結者 / 調控 / 資金) 的快照；永遠包含 DEFAULTS 的全部 key。"""
    return {key: get(key) for key in DEFAULTS}


def principal() -> float:
    from utils import math_models as mm

    return mm.calc_principal(get("cash"), get("invest_amount"))
