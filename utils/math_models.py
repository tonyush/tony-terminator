"""TONY終結者 — 運算邏輯與固定數據模組。

本檔案是「唯一」放置數學公式與台灣總經 / 統計數據的地方。
UI 層 (app.py / pages/ / utils/ui.py) 只會呼叫這裡的函式，不含任何公式。
目前所有函式皆回傳「假數據 (Dummy data)」，讓介面可以正常運作；
請依照各處 `# TODO` 註解替換為你自己的公式與數據，函式簽名請盡量保持不變。
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# 一、固定數據區 (台灣政府 / 統計數據)
# ---------------------------------------------------------------------------

OCCUPATIONS: list[str] = [
    "金融業",
    "科技業",
    "教育業",
    "學生",
    "高風險產業",
    "醫療業",
    "法律業",
    "服務業",
]

# 欄位 key -> (中文欄位名稱, 單位)。UI 會用它組成「XXX 中位數：…」說明文字。
MEDIAN_FIELDS: dict[str, tuple[str, str]] = {
    "health": ("健康狀態程度", "%"),
    "cash": ("現金資產", "元"),
    "death_age": ("預估死亡年紀", "歲"),
    "retire_age": ("預估退休年紀", "歲"),
    "invest_ratio": ("願意投入資金比例", "%"),
    "age": ("年紀", "歲"),
    "salary": ("年薪", "元"),
    "salary_growth": ("年薪增長率", "%"),
    "salary_vol": ("年薪波動率", "%"),
    "side_income": ("副業收入", "元"),
    "fixed_exp": ("月固定支出", "元"),
    "insurance_exp": ("保險支出", "元"),
    "family_exp": ("家庭支出", "元"),
    "medical_exp": ("醫療支出", "元"),
    "rent_exp": ("租金支出", "元"),
    "car_loan": ("車貸", "元"),
    "car_value": ("車的價值", "元"),
    "car_cost": ("車持有成本", "元"),
    "house_loan": ("房貸", "元"),
    "house_value": ("房的價值", "元"),
    "house_final_value": ("終值", "元"),
}

# 全體(不分職業)中位數。None 代表尚未填寫，UI 會顯示「待填入」。
# TODO: 請填入台灣政府數據 (例如主計總處薪資中位數、內政部簡易生命表等)
MEDIAN_DEFAULT: dict[str, float | None] = {key: None for key in MEDIAN_FIELDS}

# 依職業覆寫的中位數；未填寫的欄位會自動回退到 MEDIAN_DEFAULT。
# 格式範例： "金融業": {"retire_age": 62, "salary": 1_050_000, ...}
# TODO: 請填入台灣政府數據 (各職業的 預估死亡年紀 / 退休年紀 / 收入 / 健康狀態 中位數)
MEDIAN_BY_OCCUPATION: dict[str, dict[str, float | None]] = {
    occupation: {} for occupation in OCCUPATIONS
}

# 債券評級分類 (圓餅圖標籤順序)
BOND_RATING_BUCKETS: list[str] = [
    "AAA 公債/國債",
    "AA 投資等級",
    "A 投資等級",
    "BBB 投資等級",
    "BB 以下 非投資等級",
]

# ---------------------------------------------------------------------------
# 二、查詢函式
# ---------------------------------------------------------------------------


def get_median(field_key: str, occupation: str | None = None) -> float | None:
    """回傳欄位對應職業的中位數；尚未填寫則回傳 None。"""
    by_occupation = MEDIAN_BY_OCCUPATION.get(occupation or "", {})
    if by_occupation.get(field_key) is not None:
        return by_occupation[field_key]
    return MEDIAN_DEFAULT.get(field_key)


def get_current_inflation_rate() -> float:
    """目前通膨率 (單位：%)。

    TODO: 請填入台灣政府數據 (例如主計總處 CPI 年增率，或自行推估的長期通膨率)
    """
    return 2.0  # 假數據


def get_interest_spend_discount_rate() -> float:
    """信用卡專屬「利息消費折扣優惠活動」比率 (單位：%)。

    TODO: 請填入實際優惠活動比率
    """
    return 5.0  # 假數據


EARLY_CLAIM_QUOTA: int = 3  # 指定信用卡用戶可提前領息次數


# ---------------------------------------------------------------------------
# 三、運算函式 (全部為佔位符)
# ---------------------------------------------------------------------------


def convert_to_monthly_interest(principal: float, annual_rate_pct: float) -> float:
    """月利息 = 本金與年報酬率換算成月值。

    TODO: 請在此處填寫你的數學公式 (月轉換公式，例如複利月化 (1+r)^(1/12)-1)
    """
    return principal * (annual_rate_pct / 100.0) / 12.0  # 假公式：單利 / 12


def calc_daily_interest(principal: float, annual_rate_pct: float) -> float:
    """日領息額。

    TODO: 請在此處填寫你的數學公式 (日息換算，365 或 360 日基礎等)
    """
    return principal * (annual_rate_pct / 100.0) / 365.0  # 假公式


def calc_daily_interest_balance(principal: float, annual_rate_pct: float, days: int = 30) -> float:
    """日利息結餘 (累積尚未領取 / 使用的利息餘額)。

    TODO: 請在此處填寫你的數學公式 (累積利息結餘，可考慮複利與已領 / 已花費利息)
    """
    return calc_daily_interest(principal, annual_rate_pct) * days  # 假公式：累積 30 天


def calc_principal(cash: float, invest_amount: float) -> float:
    """本金金額 = 原本資金額 + 資金面板投入金額。

    TODO: 請在此處填寫你的數學公式 (例如依「願意投入資金比例」、槓桿倍數調整)
    """
    return cash + invest_amount  # 假公式


def calc_monthly_cashflow(profile: dict, principal: float, annual_rate_pct: float) -> dict[str, float]:
    """月收支：月利息 / 薪資收入 / 其他收入 / 支出 (供記帳面板圓餅圖使用)。

    `profile` 為【人生終結者】面板的欄位 (key 同 utils/state.py 的 DEFAULTS)。
    TODO: 請在此處填寫你的數學公式 (月薪換算、副業收入月化、支出彙總與車房成本攤提等)
    """
    salary = 0.0 if profile["retired"] else profile["salary"] / 12.0
    other_income = profile["side_income"] / 12.0
    expense = (
        profile["fixed_exp"]
        + profile["insurance_exp"]
        + profile["family_exp"]
        + profile["medical_exp"]
        + profile["rent_exp"]
    )
    if not profile["no_car"]:
        expense += profile["car_cost"] / 12.0
    return {  # 假公式
        "月利息": convert_to_monthly_interest(principal, annual_rate_pct),
        "薪資收入": salary,
        "其他收入": other_income,
        "支出": expense,
    }


def calc_beat_inflation_rate(return_rate_pct: float, inflation_rate_pct: float) -> float:
    """通膨超越率 = 報酬率 - 通膨率 (單位：%)。

    TODO: 如需改用實質報酬率公式 ((1+r)/(1+i)-1)，請在此處修改
    """
    return return_rate_pct - inflation_rate_pct


def calc_years_to_work(
    age: int,
    retire_age: int,
    retired: bool,
    principal: float,
    monthly_expense: float,
    annual_rate_pct: float,
) -> float:
    """所需工作年數 (還需要工作多少年才能讓利息覆蓋固定支出)。

    TODO: 請在此處填寫你的數學公式 (需考慮通膨、薪資成長、蒙地卡羅模擬等)
    """
    if retired:
        return 0.0
    required_principal = monthly_expense * 12 / max(annual_rate_pct / 100.0, 0.001)
    gap = max(required_principal - principal, 0.0)
    return round(min(gap / max(monthly_expense * 12 * 0.3, 1.0), max(retire_age - age, 0)), 1)  # 假公式


def calc_rate_sensitivity(annual_rate_pct: float, allow_leverage: bool) -> dict[str, float]:
    """理財商品利率敏感度 (Duration / Convexity)。

    TODO: 請在此處填寫你的數學公式 (債券組合的 修正存續期間 與 凸性)
    """
    return {
        "duration": 6.4 if not allow_leverage else 8.1,  # 假數據
        "convexity": 52.3 if not allow_leverage else 74.8,  # 假數據
    }


def calc_bond_portfolio(
    return_rate_pct: float,
    capital_protected: bool,
    unprotected_ratio_pct: float,
    allow_foreign_gov: bool,
    allow_foreign_corp: bool,
    allow_junk: bool,
    allow_leverage: bool,
) -> dict[str, float]:
    """債券組合型式：回傳各評級債券配置比例 (加總為 100)。

    TODO: 請在此處填寫你的債券組合評價 / 最佳化公式
    """
    weights = {
        "AAA 公債/國債": 45.0,
        "AA 投資等級": 25.0,
        "A 投資等級": 15.0,
        "BBB 投資等級": 10.0,
        "BB 以下 非投資等級": 5.0 if allow_junk else 0.0,
    }  # 假數據：僅示範開關會影響圖表
    if not allow_foreign_gov:
        weights["AAA 公債/國債"] -= 5.0
        weights["AA 投資等級"] += 5.0
    if not allow_foreign_corp:
        weights["BBB 投資等級"] -= 5.0
        weights["A 投資等級"] += 5.0
    total = sum(weights.values())
    return {name: round(value / total * 100.0, 2) for name, value in weights.items()}


def calc_max_return_cap(allow_junk: bool, allow_leverage: bool) -> float:
    """調控面板報酬率上限 (單位：%)。

    規格：「不願意持有非投資等級債」且「不使用槓桿」時，上限為 7%。
    TODO: 如需調整上限規則或數值，請在此處修改
    """
    if (not allow_junk) and (not allow_leverage):
        return 7.0
    return 100.0
