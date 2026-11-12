"""調控面板 — 報酬率與投資偏好開關。"""

import streamlit as st

from utils import math_models as mm
from utils import state, ui
from utils.i18n import _

st.markdown(f"### {_('調控面板')}")
st.caption(_("調整目標報酬率與持有偏好，數據面板的債券組合會即時跟著變動。"))

rate_area = st.container()
switch_area = st.container()

# 第二類先渲染，讓第一類的上限限制讀到最新的開關狀態
with switch_area:
    with ui.card("switches", "teal"):
        ui.card_title(_("投資偏好"), _("勾選代表「願意」"))

        protected = ui.checkbox(_("保本 (取消勾選為不保本)"), "capital_protected")
        if not protected:
            ui.slider("unprotected_ratio", 0, 100, _("不保本比例 (%)"), hint=False)

        left, right = st.columns(2, gap="large")
        with left:
            allow_foreign_gov = ui.checkbox(_("是否願意持有外國國債"), "allow_foreign_gov")
            allow_foreign_corp = ui.checkbox(_("是否願意持有外國公司債"), "allow_foreign_corp")
        with right:
            allow_junk = ui.checkbox(_("是否願意持有非投資等級債"), "allow_junk")
            allow_leverage = ui.checkbox(_("是否願意使用槓桿"), "allow_leverage")

with rate_area:
    with ui.card("rate", "gold"):
        ui.card_title(_("報酬率"), _("預期年化報酬率"))
        cap = mm.calc_max_return_cap(allow_junk, allow_leverage)
        if float(state.get("return_rate")) > cap:
            state.set_value("return_rate", cap)
        state.bind("return_rate")
        if st.session_state["return_rate"] > cap:
            st.session_state["return_rate"] = cap
        st.slider(_("報酬率 (%)"), 0.0, float(cap), key="return_rate", step=0.1, format="%.1f%%")
        state.commit("return_rate")
        st.markdown(
            f'<div class="hint">{_("目前通膨率")}：{mm.get_current_inflation_rate():.1f}%</div>',
            unsafe_allow_html=True,
        )
        if cap < 100.0:
            st.warning(_("已同時選擇「不持有非投資等級債」與「不使用槓桿」，報酬率上限自動限制為 {cap}%。").format(cap=f"{cap:g}"))
