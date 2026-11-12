"""市場資料串接窗口 (Yahoo Finance 等)。目前回傳假數據，等待你串接真實資料。"""

from __future__ import annotations

import streamlit as st

from utils.math_models import BOND_RATING_BUCKETS


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_yfinance_bond_data() -> dict[str, float]:
    """取得債券組合的各評級基準配置比例 (加總為 100)。

    TODO: 預留串接 Yahoo Finance API
          例如用 yfinance 抓取 公債 / 投資等級 / 非投資等級 債券 ETF 的殖利率與權重，
          再換算成下列各評級配置；ttl 可依資料更新頻率調整。
    """
    dummy = [45.0, 25.0, 15.0, 10.0, 5.0]  # 假數據
    return dict(zip(BOND_RATING_BUCKETS, dummy))
