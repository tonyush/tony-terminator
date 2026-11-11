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
    "fixed_exp": 35_000,
    "insurance_exp": 8_000,
    "family_exp": 12_000,
    "medical_exp": 3_000,
    "rent_exp": 0,
    # 車子
    "no_car": False,
    "car_loan": 0,
    "car_value": 600_000,
    "car_cost": 60_000,
    # 房子
    "no_house": False,
    "house_loan": 8_000_000,
    "house_value": 18_000_000,
    "house_final_value": 22_000_000,
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


def _store() -> dict[str, Any]:
    if "_store" not in st.session_state:
        st.session_state["_store"] = {
            "events": [
                {"id": uuid.uuid4().hex[:8], "name": "子女大學學費", "age": 55, "amount": 1_200_000},
                {"id": uuid.uuid4().hex[:8], "name": "房貸結清", "age": 62, "amount": 3_000_000},
            ],
            "ledger": [],
        }
    return st.session_state["_store"]


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


def ledger() -> list[dict[str, Any]]:
    return _store()["ledger"]


def profile() -> dict[str, Any]:
    """回傳全站目前所有欄位 (人生終結者 / 調控 / 資金) 的快照。"""
    return {key: get(key) for key in DEFAULTS}


def principal() -> float:
    from utils import math_models as mm

    return mm.calc_principal(get("cash"), get("invest_amount"))
