# TONY終結者 (Retirement & Wealth Dashboard)

給銀行業中高齡從業人員使用的退休與資產規劃儀表板，以 Streamlit + Plotly 打造的深色主題 Web 應用。

## 五個面板

| 面板 | 說明 |
| --- | --- |
| 人生終結者 | Google 表單風格的基本資料、收入、支出、車、房與重大事件輸入 |
| 記帳面板 | 條列式記帳 (顏色標籤 / 類別 / 描述 / 金額) 與月收支圓餅圖 |
| 調控面板 | 報酬率與保本、外國債、非投資等級債、槓桿等偏好開關 |
| 數據面板 | Metric Cards、Duration / Convexity、債券組合圓餅圖、重大事件彙總 |
| 資金面板 | 投入金額與模式，以及信用卡專屬「提前領息 3 次」與利息消費折扣權益 |

## 執行

```bash
pip install -r requirements.txt
streamlit run app.py   # 預設 http://localhost:8765
```

## 專案結構

```
app.py                # 入口：主題、Header、頂部 5 個導覽按鈕、st.navigation
pages/                # 五個面板 (只負責 UI 與圖表)
utils/math_models.py  # 所有公式與台灣統計數據 (目前為假數據，找 TODO 替換)
utils/state.py        # st.session_state 跨頁同步層 (單一 _store)
utils/ui.py           # CSS 主題、卡片、輸入元件
.streamlit/config.toml
```

## 你要填寫的地方

搜尋 `TODO`：`utils/math_models.py` 內的中位數表 (`MEDIAN_DEFAULT` / `MEDIAN_BY_OCCUPATION`)、
通膨率、月利息轉換、日息、所需工作年數、Duration / Convexity、債券組合與報酬率上限規則。
UI 層不含任何公式，替換函式內容即可，介面會自動更新。
