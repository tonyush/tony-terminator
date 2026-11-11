"""資金面板 — 投入金額、投入模式與信用卡專屬權益。"""

from datetime import date

import streamlit as st

from utils import math_models as mm
from utils import state, ui

st.markdown("### 資金面板")
st.caption("設定要投入的資金與時間，本金會同步到數據面板。")

left, right = st.columns(2, gap="large")

with left:
    with ui.card("amount", "gold"):
        ui.card_title("投入金額", "不設上限，可依需求隨時調整")
        ui.num_input("投入金額 (元)", "invest_amount", hint=False, min_value=0, step=10_000, format="%d")
        st.caption(f"原本資金額 {state.get('cash'):,.0f} 元，投入後本金 {state.principal():,.0f} 元")

with right:
    with ui.card("mode", "teal"):
        ui.card_title("日期與投入模式")
        mode = ui.select("投入模式", "invest_mode", ["今日投入", "預約單筆投入", "預約週期性投入"])
        if mode == "今日投入":
            st.caption(f"將於今日 ({date.today():%Y-%m-%d}) 投入。")
        else:
            state.bind("invest_date")
            st.date_input("投入日期" if mode == "預約單筆投入" else "首次投入日期", key="invest_date", min_value=date.today())
            state.commit("invest_date")
            if mode == "預約週期性投入":
                c1, c2 = st.columns(2)
                with c1:
                    ui.select("投入週期", "periodic_freq", ["每週", "每兩週", "每月", "每季", "每年"])
                with c2:
                    state.bind("periodic_end")
                    st.date_input("結束日期", key="periodic_end", min_value=date.today())
                    state.commit("periodic_end")

st.markdown('<div class="section-title">特殊權益</div>', unsafe_allow_html=True)
holder = ui.checkbox("我持有指定信用卡 (示範用開關，實際資格由後台判定)", "card_holder")

quota = mm.EARLY_CLAIM_QUOTA
used = min(int(state.get("early_claims_used")), quota)
remaining = quota - used
locked = "" if holder else " locked"


def _use_early_claim() -> None:
    state.set_value("early_claims_used", min(int(state.get("early_claims_used")) + 1, quota))


b1, b2 = st.columns(2, gap="large")
with b1:
    st.markdown(
        f"""<div class="benefit{locked}">
          <span class="badge">信用卡專屬</span>
          <div class="card-title">提前領息 {quota} 次權益</div>
          <div class="big">{remaining} / {quota}</div>
          <div class="desc">剩餘可提前領息次數，不必等到配息日即可領取已累積的利息。</div>
        </div>""",
        unsafe_allow_html=True,
    )
    st.button("使用一次提前領息", on_click=_use_early_claim, disabled=(not holder) or remaining == 0, key="use_early")
with b2:
    st.markdown(
        f"""<div class="benefit{locked}">
          <span class="badge">利息消費優惠</span>
          <div class="card-title">利息消費折扣優惠活動</div>
          <div class="big">{mm.get_interest_spend_discount_rate():.1f}%</div>
          <div class="desc">以利息進行消費時享有的折扣比率，實際活動內容以公告為準。</div>
        </div>""",
        unsafe_allow_html=True,
    )
if not holder:
    st.caption("勾選上方「持有指定信用卡」即可解鎖以上權益。")
