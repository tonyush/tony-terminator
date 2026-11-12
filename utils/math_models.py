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
    "軍人",
    "農林漁牧業生產人員",
    "技藝生產人員",
]

STUDENT_OCCUPATION = "學生"

# 欄位 key -> (中文欄位名稱, 單位)。UI 會用它組成「XXX 中位數：…」說明文字。
MEDIAN_FIELDS: dict[str, tuple[str, str]] = {
    "health": ("健康狀態程度", "%"),
    "tuition": ("學期學費", "元"),
    "cash": ("現金資產", "元"),
    "death_age": ("預估死亡年紀", "歲"),
    "retire_age": ("預估退休年紀", "歲"),
    "invest_ratio": ("願意投入資金比例", "%"),
    "age": ("年紀", "歲"),
    # 收入
    "salary": ("年薪", "元"),
    "salary_growth": ("年薪增長率", "%"),
    "salary_vol": ("年薪波動率", "%"),
    "side_income": ("副業收入", "元"),
    # 支出
    "fixed_exp_total": ("月固定支出", "元"),
    "fe_food": ("食物費用", "元"),
    "fe_transit": ("大眾交通費用", "元"),
    "fe_entertain": ("娛樂費用", "元"),
    "fe_subscription": ("非娛樂金融或其他訂閱費用與月費", "元"),
    "fe_other": ("其他費用", "元"),
    "insurance_exp": ("保險支出", "元"),
    "medical_exp": ("醫療支出", "元"),
    "rent_exp": ("租金支出", "元"),
    # 家庭 (數量 / 年花費)
    "family_exp": ("其他家庭支出", "元"),
    "family_child_n": ("小孩數量", "人"),
    "family_child_cost": ("小孩年花費金額", "元"),
    "family_elder_n": ("長輩數量", "人"),
    "family_elder_cost": ("長輩年花費金額", "元"),
    "family_pet_n": ("寵物數量", "隻"),
    "family_pet_cost": ("寵物年花費金額", "元"),
    "family_spouse_n": ("老婆/配偶數量", "人"),
    "family_spouse_cost": ("老婆/配偶年花費金額", "元"),
    # 車子 / 摩托車 / 特殊交通工具
    "car_loan": ("貸款月繳額", "元"),
    "car_value": ("車子價值", "元"),
    "car_use_cost": ("使用成本(油費等)", "元"),
    "car_cost": ("持有成本(稅收等)", "元"),
    "moto_loan": ("貸款月繳額", "元"),
    "moto_value": ("摩托車價值", "元"),
    "moto_use_cost": ("使用成本(油費等)", "元"),
    "moto_cost": ("持有成本(稅收等)", "元"),
    "special_loan": ("貸款月繳額", "元"),
    "special_value": ("特殊交通工具價值", "元"),
    "special_use_cost": ("使用成本(油費等)", "元"),
    "special_cost": ("持有成本(稅收等)", "元"),
    # 房子
    "house_loan": ("貸款月繳額", "元"),
    "house_value": ("房子價值", "元"),
    "house_cost": ("持有成本(稅收等)", "元"),
}

# 全體(不分職業)中位數。None 代表尚未填寫，UI 會顯示「待填入」。
# TODO: 請填入台灣政府數據 (例如主計總處薪資中位數、內政部簡易生命表等)
MEDIAN_DEFAULT: dict[str, float | None] = {key: None for key in MEDIAN_FIELDS}

# 依職業覆寫的中位數；未填寫的欄位會自動回退到 MEDIAN_DEFAULT。
# 格式範例： "金融業": {"retire_age": 62, "salary": 1_050_000, ...}
# TODO: 請填入台灣政府數據 (各職業的 預估死亡年紀 / 退休年紀 / 收入 / 健康狀態 / 學期學費 中位數)
# TODO: 中位數附註 — 家庭 / 車 / 房 / 支出等欄位的中位數也請填在這裡 (欄位 key 見 MEDIAN_FIELDS)
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


VEHICLE_PREFIXES: tuple[tuple[str, str], ...] = (
    ("car", "no_car"),
    ("moto", "no_moto"),
    ("special", "no_special"),
)
FAMILY_ITEMS: tuple[str, ...] = ("child", "elder", "pet", "spouse")


def calc_fixed_expense(profile: dict) -> float:
    """月固定支出：依「總額輸入 / 細項加總」模式回傳最終月總額。

    TODO: 請在此處填寫你的數學公式 (例如細項加權、季節性調整)
    """
    if profile["fixed_exp_mode"] == "itemized":
        return float(
            sum(profile[k] for k in ("fe_food", "fe_transit", "fe_entertain", "fe_subscription", "fe_other"))
        )
    return float(profile["fixed_exp_total"])


def calc_family_expense(profile: dict) -> float:
    """家庭月支出 = 其他家庭支出(月) + Σ(數量 × 年花費) / 12。

    TODO: 請在此處填寫你的數學公式 (各成員年花費的成長率、年齡階段調整等)
    """
    annual = sum(profile[f"family_{item}_n"] * profile[f"family_{item}_cost"] for item in FAMILY_ITEMS)
    return float(profile["family_exp"] + annual / 12.0)


def calc_vehicle_monthly_cost(loan_monthly: float, use_cost_monthly: float, hold_cost_yearly: float) -> float:
    """單一交通工具的月成本 = 貸款月繳額 + 使用成本(月) + 持有成本(年)/12。

    TODO: 請在此處填寫你的數學公式 (折舊、保養攤提等)
    """
    return loan_monthly + use_cost_monthly + hold_cost_yearly / 12.0


def calc_monthly_expense(profile: dict) -> float:
    """【人生終結者】的所有月支出 + 各類貸款月繳額 (不含記帳表)。

    TODO: 請在此處填寫你的數學公式 (支出彙總與房 / 車成本攤提)
    """
    expense = (
        calc_fixed_expense(profile)
        + profile["insurance_exp"]
        + profile["medical_exp"]
        + profile["rent_exp"]
        + calc_family_expense(profile)
    )
    for prefix, no_key in VEHICLE_PREFIXES:
        if not profile[no_key]:
            expense += calc_vehicle_monthly_cost(
                profile[f"{prefix}_loan"], profile[f"{prefix}_use_cost"], profile[f"{prefix}_cost"]
            )
    if not profile["no_house"]:
        expense += profile["house_loan"] + profile["house_cost"] / 12.0
    if profile["occupation"] == STUDENT_OCCUPATION:
        expense += profile["tuition"] / 6.0  # 假公式：學期學費以 6 個月攤提
    return float(expense)


def calc_monthly_cashflow(
    profile: dict,
    principal: float,
    annual_rate_pct: float,
    ledger_entries: list[dict] | None = None,
) -> dict[str, float]:
    """月收支：月利息 / 薪資 / 副業 / 記帳收入 / 支出，以及總收入與總支出。

    總收入 = 人生終結者(薪資 + 副業) + 記帳表標記為「收入」的加總 (不含月利息，利息另列)。
    總支出 = 人生終結者(所有月支出 + 各類貸款月繳額) + 記帳表標記為「支出」的加總。
    TODO: 請在此處填寫你的數學公式 (月薪換算、副業收入月化、記帳資料的月份歸屬等)
    """
    ledger_entries = ledger_entries or []
    salary = 0.0 if profile["retired"] else profile["salary"] / 12.0
    side = profile["side_income"] / 12.0
    ledger_income = float(sum(e["amount"] for e in ledger_entries if e["kind"] == "收入"))
    ledger_expense = float(sum(e["amount"] for e in ledger_entries if e["kind"] == "支出"))
    expense = calc_monthly_expense(profile) + ledger_expense
    return {  # 假公式
        "月利息": convert_to_monthly_interest(principal, annual_rate_pct),
        "薪資收入": salary,
        "副業收入": side,
        "記帳收入": ledger_income,
        "支出": expense,
        "總收入": salary + side + ledger_income,
        "總支出": expense,
    }


def calculate_projected_income(
    salary: float,
    growth_pct: float,
    volatility_pct: float,
    side_income: float,
    age: int,
    retire_age: int,
    retired: bool,
    horizon_age: int = 100,
) -> dict[str, list[float]]:
    """未來收入推估 (年度)。回傳 {"ages": [...], "income": [...]}。

    TODO: 請在此處填寫你的數學公式 (薪資邊際收斂公式：成長率隨年齡遞減、波動率帶入情境區間)
    """
    ages = list(range(age, max(horizon_age, age + 1) + 1))
    income: list[float] = []
    for t, current_age in enumerate(ages):
        working = (not retired) and current_age < retire_age
        base = salary * (1 + growth_pct / 100.0) ** t if working else 0.0  # 假公式：固定成長
        income.append(base + side_income)
    return {"ages": ages, "income": income}


def calc_lifetime_series(
    profile: dict,
    principal: float,
    annual_rate_pct: float,
    inflation_pct: float,
) -> dict[str, list[float]]:
    """折線圖序列：年齡 vs 年度 總收入 / 總支出 / 利息。

    TODO: 請在此處填寫你的數學公式 (逐年現金流模擬、利息再投入、蒙地卡羅路徑平均等)
    """
    projection = calculate_projected_income(
        profile["salary"],
        profile["salary_growth"],
        profile["salary_vol"],
        profile["side_income"],
        profile["age"],
        profile["retire_age"],
        profile["retired"],
        profile["death_age"],
    )
    ages = projection["ages"]
    annual_expense = calc_monthly_expense(profile) * 12.0
    return {  # 假數據
        "ages": ages,
        "總收入": projection["income"],
        "總支出": [annual_expense * (1 + inflation_pct / 100.0) ** t for t in range(len(ages))],
        "利息": [principal * annual_rate_pct / 100.0 for _ in ages],
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
    market_weights: dict[str, float] | None = None,
) -> dict[str, float]:
    """債券組合型式：回傳各評級債券配置比例 (加總為 100)。

    `market_weights` 來自 utils/market_data.fetch_yfinance_bond_data() 的基準配置。
    TODO: 請在此處填寫你的債券組合評價 / 最佳化公式
    """
    weights = dict(market_weights or {name: 0.0 for name in BOND_RATING_BUCKETS})  # 假數據：僅示範開關會影響圖表
    if not allow_junk:
        weights["BB 以下 非投資等級"] = 0.0
    if not allow_foreign_gov:
        weights["AAA 公債/國債"] -= 5.0
        weights["AA 投資等級"] += 5.0
    if not allow_foreign_corp:
        weights["BBB 投資等級"] -= 5.0
        weights["A 投資等級"] += 5.0
    weights = {name: max(value, 0.0) for name, value in weights.items()}
    total = sum(weights.values()) or 1.0
    return {name: round(value / total * 100.0, 2) for name, value in weights.items()}


def calc_max_return_cap(allow_junk: bool, allow_leverage: bool) -> float:
    """調控面板報酬率上限 (單位：%)。

    規格：「不願意持有非投資等級債」且「不使用槓桿」時，上限為 7%。
    TODO: 如需調整上限規則或數值，請在此處修改
    """
    if (not allow_junk) and (not allow_leverage):
        return 7.0
    return 100.0
