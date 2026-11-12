"""資金面板 — 投入金額、投入模式與信用卡專屬權益。"""

from datetime import date

import streamlit as st

from utils import math_models as mm
from utils import state, ui
from utils.i18n import _

title_col, bank_col = st.columns([4, 1.4], vertical_alignment="center")
with title_col:
    st.markdown(f"### {_('資金面板')}")
    st.caption(_("設定要投入的資金與時間，本金會同步到數據面板。"))
with bank_col:
    ui.bank_sync_button("bank_sync_funds")

left, right = st.columns(2, gap="large")

with left:
    with ui.card("amount", "gold"):
        ui.card_title(_("投入金額"), _("不設上限，可依需求隨時調整"))
        ui.num_input("invest_amount", _("投入金額 (元)"), hint=False, min_value=0, step=10_000, format="%d")
        st.caption(_("原本資金額 {cash} 元，投入後本金 {principal} 元").format(cash=f"{state.get('cash'):,.0f}", principal=f"{state.principal():,.0f}"))

with right:
    with ui.card("mode", "teal"):
        ui.card_title(_("日期與投入模式"))
        mode = ui.select(_("投入模式"), "invest_mode", ["今日投入", "預約單筆投入", "預約週期性投入"])
        if mode == "今日投入":
            st.caption(_("將於今日 ({d}) 投入。").format(d=f"{date.today():%Y-%m-%d}"))
        else:
            state.bind("invest_date")
            st.date_input(_("投入日期") if mode == "預約單筆投入" else _("首次投入日期"), key="invest_date", min_value=date.today())
            state.commit("invest_date")
            if mode == "預約週期性投入":
                c1, c2 = st.columns(2)
                with c1:
                    ui.select(_("投入週期"), "periodic_freq", ["每週", "每兩週", "每月", "每季", "每年"])
                with c2:
                    state.bind("periodic_end")
                    st.date_input(_("結束日期"), key="periodic_end", min_value=date.today())
                    state.commit("periodic_end")

st.markdown(f'<div class="section-title">{_("特殊權益")}</div>', unsafe_allow_html=True)
holder = ui.checkbox(_("我持有指定信用卡 (示範用開關，實際資格由後台判定)"), "card_holder")

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
          <span class="badge">{_("信用卡專屬")}</span>
          <div class="card-title">{_("提前領息 {n} 次權益").format(n=quota)}</div>
          <div class="big">{remaining} / {quota}</div>
          <div class="desc">{_("剩餘可提前領息次數，不必等到配息日即可領取已累積的利息。")}</div>
        </div>""",
        unsafe_allow_html=True,
    )
    st.button(_("使用一次提前領息"), on_click=_use_early_claim, disabled=(not holder) or remaining == 0, key="use_early")
with b2:
    st.markdown(
        f"""<div class="benefit{locked}">
          <span class="badge">{_("利息消費優惠")}</span>
          <div class="card-title">{_("利息消費折扣優惠活動")}</div>
          <div class="big">{mm.get_interest_spend_discount_rate():.1f}%</div>
          <div class="desc">{_("以利息進行消費時享有的折扣比率，實際活動內容以公告為準。")}</div>
        </div>""",
        unsafe_allow_html=True,
    )
if not holder:
    st.caption(_("勾選上方「持有指定信用卡」即可解鎖以上權益。"))
