"""全站中英雙語 (i18n) 翻譯中樞。

用法：
    from utils.i18n import _
    st.markdown(_("人生終結者"))

規則：
  * 以「中文原文」作為 key；`st.session_state.language` 為 "zh" (預設) 時直接回傳原文。
  * 語言為 "en" 時查 EN 字典；查不到就回傳中文原文 (不會 KeyError)。
  * 含 `{變數}` 的 key 請搭配 `.format(...)` 使用，例如 `_("共 {n} 筆").format(n=3)`。
  * 新增文字時，請把中文 key 加進下方對應區段的字典即可。
"""

from __future__ import annotations

import streamlit as st

DEFAULT_LANGUAGE = "zh"
SUPPORTED_LANGUAGES = ("zh", "en")

# ---------------------------------------------------------------------------
# 共用詞彙
# ---------------------------------------------------------------------------
_COMMON: dict[str, str] = {
    "TONY終結者 | Retirement & Wealth Dashboard": "TONY Terminator | Retirement & Wealth Dashboard",
    "人生終結者": "Life Profile",
    "記帳面板": "Ledger",
    "調控面板": "Controls",
    "數據面板": "Analytics",
    "資金面板": "Funding",
    "刪除": "Delete",
    "金額": "Amount",
    "年紀": "Age",
    "總額": "Total",
    "待填入": "TBD",
    "{name}中位數：{value}": "{name} median: {value}",
    "元": "NTD",
    "歲": "yrs",
    "人": "persons",
    "隻": "pcs",
    "🏦 同步銀行真實數據 (Coming Soon)": "🏦 Sync Real Bank Data (Coming Soon)",
    "男": "Male",
    "女": "Female",
    "支出": "Expense",
    "收入": "Income",
    "利息": "Interest",
    "總收入": "Total Income",
    "總支出": "Total Expenses",
    "月利息": "Monthly Interest",
    "薪資收入": "Salary Income",
    "副業收入": "Side Income",
    "記帳收入": "Logged Income",
}

# ---------------------------------------------------------------------------
# 人生終結者 (基本資料 / 收入 / 支出 / 家庭 / 交通 / 房產 / 重大事件)
# ---------------------------------------------------------------------------
_LIFE: dict[str, str] = {
    "填寫你的人生參數，其他面板會自動同步使用這些資料。金額單位為新台幣元。": (
        "Enter your life parameters; every other panel reuses them automatically. Amounts are in NTD."
    ),
    "基礎參數": "Basic Profile",
    "職業會連動下方各欄位的中位數參考數據": "Occupation drives the median reference figures under each field below",
    "性別": "Gender",
    "職業": "Occupation",
    "已退休": "Retired",
    "現金或存款": "Cash or deposits",
    "學期學費": "Tuition per Semester",
    "健康狀態程度": "Health Status",
    "現金資產": "Cash Assets",
    "預估死亡年紀": "Expected Age at Death",
    "預估退休年紀": "Expected Retirement Age",
    "願意投入資金比例": "Investable Capital Ratio",
    # 職業
    "金融業": "Finance & Banking",
    "科技業": "Technology",
    "教育業": "Education",
    "學生": "Student",
    "高風險產業": "High-Risk Industry",
    "醫療業": "Healthcare",
    "法律業": "Legal",
    "服務業": "Services",
    "軍人": "Military",
    "農林漁牧業生產人員": "Agriculture, Forestry, Fishing & Livestock",
    "技藝生產人員": "Craft & Skilled Trades",
    # 收入
    "收入列表": "Income",
    "已退休時，年薪相關欄位會自動隱藏": "Salary fields are hidden automatically once you are retired",
    "年薪": "Annual Salary",
    "年薪增長率": "Salary Growth Rate",
    "年薪波動率": "Salary Volatility",
    "查看未來收入推估預覽": "View Projected Income Preview",
    "目前為示意數據 (固定成長率)，薪資邊際收斂公式待填入。": (
        "Illustrative data only (flat growth rate); the marginal salary-convergence formula is pending."
    ),
    "年收入": "Annual Income",
    # 支出
    "支出列表": "Expenses",
    "以「月」為單位": "Monthly figures",
    "月固定支出": "Monthly Fixed Expenses",
    "總額輸入": "Lump Sum",
    "細項加總": "Itemized",
    "細項加總金額": "Itemized total",
    "食物費用": "Food",
    "大眾交通費用": "Public Transport",
    "娛樂費用": "Entertainment",
    "非娛樂金融或其他訂閱費用與月費": "Non-entertainment Financial & Other Subscriptions / Monthly Fees",
    "其他費用": "Other Expenses",
    "保險支出": "Insurance Premiums",
    "醫療支出": "Medical Expenses",
    "租金支出": "Rent",
    # 家庭
    "家庭支出": "Family Expenses",
    "每個成員填入數量與年花費金額 (每人每年)": "Enter headcount and annual cost per member (per person per year)",
    "其他家庭支出": "Other Family Expenses",
    "每月其他家庭開銷": "Other monthly household spending",
    "家庭月支出總額": "Total monthly family expenses",
    "小孩數量": "Children (count)",
    "小孩年花費金額": "Children (annual cost)",
    "長輩數量": "Elders (count)",
    "長輩年花費金額": "Elders (annual cost)",
    "寵物數量": "Pets (count)",
    "寵物年花費金額": "Pets (annual cost)",
    "老婆/配偶數量": "Spouse (count)",
    "老婆/配偶年花費金額": "Spouse (annual cost)",
    # 交通工具 / 房子
    "車子": "Car",
    "摩托車": "Motorcycle",
    "特殊交通工具": "Special Vehicle",
    "無車子": "No car",
    "無摩托車": "No motorcycle",
    "無特殊交通工具": "No special vehicle",
    "貸款月繳額、使用成本以月計；持有成本以年計": "Loan payment and running cost are monthly; holding cost is annual",
    "貸款月繳額": "Monthly Loan Payment",
    "車子價值": "Car Value",
    "摩托車價值": "Motorcycle Value",
    "特殊交通工具價值": "Special Vehicle Value",
    "使用成本(油費等)": "Running Cost (fuel, etc.)",
    "持有成本(稅收等)": "Holding Cost (taxes, etc.)",
    "房子": "Home",
    "貸款月繳額以月計；持有成本以年計": "Mortgage payment is monthly; holding cost is annual",
    "無房子": "No home",
    "房子價值": "Home Value",
    # 重大事件
    "重大事件": "Major Life Events",
    "例如子女教育、換屋、長照準備等，可自由新增多筆": (
        "e.g. children's education, home upgrade, long-term care; add as many as you need"
    ),
    "事件名稱": "Event Name",
    "發生時間 / 年紀": "Timing / Age",
    "目前沒有重大事件，點擊下方按鈕新增第一筆。": "No major events yet. Click the button below to add the first one.",
    "＋ 新增事件": "+ Add Event",
}

# ---------------------------------------------------------------------------
# 記帳面板
# ---------------------------------------------------------------------------
_LEDGER: dict[str, str] = {
    "左側為你的日常記帳；右側圓餅圖會自動帶入【人生終結者】的月收支，並加總記帳表。": (
        "Log your daily entries on the left; the pie chart on the right combines your Life Profile "
        "monthly cash flow with the ledger."
    ),
    "類型": "Type",
    "顏色標籤": "Color Tag",
    "標籤類別": "Category",
    "文字描述": "Description",
    "新增一筆": "New Entry",
    "顏色標籤可用來自訂分群，例如紅色代表必要支出": "Color tags let you group entries, e.g. red for essential spending",
    "例如：午餐、水電費": "e.g. lunch, utilities",
    "＋ 新增記帳": "+ Add Entry",
    "記帳明細": "Ledger Entries",
    "共 {n} 筆": "{n} entries",
    "還沒有任何記帳紀錄，從上方新增第一筆吧。": "No entries yet. Add your first one above.",
    "記帳支出": "Logged Expenses",
    "結餘": "Net Balance",
    "⬇ 匯出 Excel": "⬇ Export to Excel",
    "匯出 Excel 需要 openpyxl，請在 requirements.txt 加入 openpyxl 後重新安裝。": (
        "Excel export requires openpyxl. Add it to requirements.txt and reinstall."
    ),
    "月收支圖表": "Monthly Cash Flow",
    "資料來源：人生終結者 + 記帳表 + 調控 / 資金面板": "Source: Life Profile + ledger + Controls / Funding panels",
    "月總收入": "Total Monthly Income",
    "月總支出": "Total Monthly Expenses",
    "月結餘": "Monthly Net Cash Flow",
    # 類別
    "餐飲": "Dining",
    "交通": "Transport",
    "居住": "Housing",
    "醫療": "Medical",
    "保險": "Insurance",
    "娛樂": "Entertainment",
    "教育": "Education",
    "薪資": "Salary",
    "投資": "Investment",
    "其他": "Other",
    # 顏色標籤
    "🔴 紅": "🔴 Red",
    "🟠 橙": "🟠 Orange",
    "🟡 黃": "🟡 Yellow",
    "🟢 綠": "🟢 Green",
    "🔵 藍": "🔵 Blue",
    "🟣 紫": "🟣 Purple",
    "⚪ 灰": "⚪ Gray",
}

# ---------------------------------------------------------------------------
# 調控面板
# ---------------------------------------------------------------------------
_CONTROL: dict[str, str] = {
    "調整目標報酬率與持有偏好，數據面板的債券組合會即時跟著變動。": (
        "Tune your target return and holding preferences; the bond mix in Analytics updates instantly."
    ),
    "投資偏好": "Investment Preferences",
    "勾選代表「願意」": "Tick = willing",
    "保本 (取消勾選為不保本)": "Principal Guaranteed (untick for non-guaranteed)",
    "不保本比例 (%)": "Non-guaranteed Portion (%)",
    "是否願意持有外國國債": "Willing to hold foreign government bonds",
    "是否願意持有外國公司債": "Willing to hold foreign corporate bonds",
    "是否願意持有非投資等級債": "Willing to hold non-investment-grade (high-yield) bonds",
    "是否願意使用槓桿": "Willing to use leverage",
    "報酬率": "Rate of Return",
    "預期年化報酬率": "Expected annualized return",
    "報酬率 (%)": "Rate of Return (%)",
    "目前通膨率": "Current inflation rate",
    "已同時選擇「不持有非投資等級債」與「不使用槓桿」，報酬率上限自動限制為 {cap}%。": (
        "Both \"no non-investment-grade bonds\" and \"no leverage\" are selected, so the return cap is "
        "automatically limited to {cap}%."
    ),
}

# ---------------------------------------------------------------------------
# 數據面板
# ---------------------------------------------------------------------------
_DASHBOARD: dict[str, str] = {
    "所有數字皆由【人生終結者】、【調控面板】與【資金面板】的設定自動計算。": (
        "All figures are calculated automatically from your Life Profile, Controls and Funding settings."
    ),
    "日利息結餘": "Accrued Daily Interest Balance",
    "累積未領利息": "Accumulated unclaimed interest",
    "本金金額": "Principal",
    "原本資金 {cash} + 投入 {invest}": "Existing capital {cash} + new deposit {invest}",
    "現在報酬率": "Current Rate of Return",
    "通膨率": "Inflation",
    "通膨超越率": "Real Return over Inflation",
    "報酬率 − 通膨率": "Return − inflation",
    "日領息額": "Daily Interest Payout",
    "每日可領利息": "Interest available per day",
    "所需工作年數": "Working Years Required",
    "{n} 年": "{n} yrs",
    "預計 {age} 歲退休": "Retiring at {age}",
    "修正存續期間 Duration": "Modified Duration",
    "凸性 Convexity": "Convexity",
    "利率敏感度": "Interest-rate sensitivity",
    "收支與利息趨勢": "Income, Expense & Interest Trend",
    "X 軸為年紀，Y 軸為年度金額": "X axis: age; Y axis: annual amount",
    "金額 (NT$)": "Amount (NT$)",
    "債券組合型式": "Bond Portfolio Allocation",
    "各評級債券配置比例": "Allocation by credit rating",
    "AAA 公債/國債": "AAA Government Bonds",
    "AA 投資等級": "AA Investment Grade",
    "A 投資等級": "A Investment Grade",
    "BBB 投資等級": "BBB Investment Grade",
    "BB 以下 非投資等級": "BB & Below (High Yield)",
    "重大事件彙總": "Major Events Summary",
    "來源：人生終結者": "Source: Life Profile",
    "發生年紀": "Age at Event",
    "(未命名)": "(Unnamed)",
    "%d 歲": "age %d",
    "尚未設定重大事件，請至【人生終結者】新增。": "No major events yet. Add some in Life Profile.",
    "共 {n} 件重大事件": "{n} major events",
}

# ---------------------------------------------------------------------------
# 資金面板
# ---------------------------------------------------------------------------
_FUNDS: dict[str, str] = {
    "設定要投入的資金與時間，本金會同步到數據面板。": "Set how much to invest and when; principal syncs to Analytics.",
    "投入金額": "Deposit Amount",
    "不設上限，可依需求隨時調整": "No cap; adjust any time",
    "投入金額 (元)": "Deposit Amount (NTD)",
    "原本資金額 {cash} 元，投入後本金 {principal} 元": (
        "Existing capital NTD {cash}; principal after deposit NTD {principal}"
    ),
    "日期與投入模式": "Date & Deposit Mode",
    "投入模式": "Deposit Mode",
    "今日投入": "Deposit Today",
    "預約單筆投入": "Scheduled One-off Deposit",
    "預約週期性投入": "Scheduled Recurring Deposit",
    "將於今日 ({d}) 投入。": "Will be deposited today ({d}).",
    "投入日期": "Deposit Date",
    "首次投入日期": "First Deposit Date",
    "投入週期": "Deposit Frequency",
    "結束日期": "End Date",
    "每週": "Weekly",
    "每兩週": "Bi-weekly",
    "每月": "Monthly",
    "每季": "Quarterly",
    "每年": "Yearly",
    "特殊權益": "Special Benefits",
    "我持有指定信用卡 (示範用開關，實際資格由後台判定)": (
        "I hold the designated credit card (demo switch; actual eligibility is decided by the back end)"
    ),
    "信用卡專屬": "Card Exclusive",
    "提前領息 {n} 次權益": "{n} Early Interest Withdrawals",
    "剩餘可提前領息次數，不必等到配息日即可領取已累積的利息。": (
        "Remaining early withdrawals: claim accrued interest without waiting for the payout date."
    ),
    "使用一次提前領息": "Use One Early Withdrawal",
    "利息消費優惠": "Interest Spending Perk",
    "利息消費折扣優惠活動": "Interest Spending Discount Offer",
    "以利息進行消費時享有的折扣比率，實際活動內容以公告為準。": (
        "Discount rate when spending your interest; actual terms follow the official announcement."
    ),
    "勾選上方「持有指定信用卡」即可解鎖以上權益。": "Tick \"I hold the designated credit card\" above to unlock these benefits.",
}

EN: dict[str, str] = {**_COMMON, **_LIFE, **_LEDGER, **_CONTROL, **_DASHBOARD, **_FUNDS}

TRANSLATIONS: dict[str, dict[str, str]] = {"zh": {}, "en": EN}


def current_language() -> str:
    language = st.session_state.get("language", DEFAULT_LANGUAGE)
    return language if language in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE


def _(text_key: str) -> str:
    """翻譯包裝函數：zh 直接回傳原文；其他語言查字典，找不到就回傳中文原文。"""
    if not isinstance(text_key, str):
        return text_key
    return TRANSLATIONS.get(current_language(), {}).get(text_key, text_key)
