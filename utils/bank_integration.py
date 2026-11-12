"""銀行對接窗口 (Open Banking API Placeholder)。

目前所有函式只回傳假數據；UI 以反灰的「同步銀行真實數據 (Coming Soon)」按鈕作為視覺佔位。
"""

from __future__ import annotations

from typing import Any


def is_bank_connected() -> bool:
    """是否已完成銀行授權。

    TODO: 預留銀行 API 串接 (OAuth 授權狀態檢查)
    """
    return False


def fetch_bank_balance() -> dict[str, Any]:
    """取得使用者真實存款 / 資產餘額。

    TODO: 預留銀行 API 串接 (Open Banking: accounts / balances endpoint)
    """
    return {"currency": "TWD", "cash": 0.0, "investments": 0.0}  # 假數據


def fetch_bank_transactions(days: int = 30) -> list[dict[str, Any]]:
    """取得近 N 天的真實收支明細，格式對齊記帳面板 (category / desc / amount / kind)。

    TODO: 預留銀行 API 串接 (Open Banking: transactions endpoint)
    """
    return []  # 假數據


def sync_bank_data() -> bool:
    """把銀行資料同步進 st.session_state.user_profile 與 accounting_logs。

    TODO: 預留銀行 API 串接 (呼叫上面的 fetch_* 並寫入 utils.state)
    """
    return False
