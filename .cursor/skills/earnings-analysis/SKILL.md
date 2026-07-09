---
name: earnings-analysis
description: 基于雅虎财经数据的美股财报（earnings）分析。自动解读 Revenue、EPS、毛利率、Operating Margin、FCF、Cash、Guidance、AI 业务增长、Management Commentary，并给出「超预期」「利空」星级评分。Use when the user asks 财报分析 / 分析财报 / earnings 解读 for a US ticker (e.g. 财报分析 NVDA, 分析 AAPL 财报, TSLA earnings 怎么样), or wants a quarterly earnings breakdown.
---

# 美股财报分析

对用户给出的美股代码（如 `NVDA`、`AAPL`）解读**最新一季财报**，数据以**雅虎财经（Yahoo Finance）** 为准。**默认中文**，禁止凭记忆编造财务数字。

## 触发方式

以下任一形式即启动本技能，无需额外确认：

- `财报分析 NVDA`
- `分析 AAPL 财报`
- `TSLA earnings 怎么样`
- `解读 MSFT 最新财报`

若上下文已在讨论某公司财报，直接对该 ticker 适用。

## 工作流程

1. **解析 ticker 与财报期**：确认美股代码、目标财季（默认最近一季 / most recent quarter）。
2. **拉取雅虎财经数据**（必须联网，数据源以 Yahoo Finance 为准）：
   - 页面：`https://finance.yahoo.com/quote/TICKER/financials`、`/analysis`、`/press-releases`
   - 关键项：Revenue、EPS（GAAP 与 Non-GAAP/Adjusted）、毛利率、Operating Margin、Free Cash Flow、Cash & Equivalents、下季/全年 Guidance、分析师共识（consensus）。
3. **可选加速取数**：若本地脚本可用，优先跑一次快速拉取：
   ```bash
   python3 ~/.codex/skills/wall-street-us-stock-analysis/scripts/market_data.py TICKER --period 1y --json
   ```
4. **逐项分析**：严格按下方 9 个分析项，每项对比「实际 vs 预期 vs 去年同期（YoY）/上季（QoQ）」。
5. **给出评分**：结尾用固定的「超预期 / 利空」星级卡片总结。
6. **标注数据时点**：报告开头注明财季、数据截止日期与来源为 Yahoo Finance。

## 固定分析项（9 项，缺一不可）

每一项都要给出**具体数字 + 与预期/同比的对比 + 一句判断**。数据缺失时明确标注「Yahoo 未披露」并给定性判断，不虚构。

| # | 分析项 | 必看内容 |
|---|--------|----------|
| 1 | **Revenue** | 营收金额、YoY/QoQ、是否 beat/miss 共识，beat/miss 幅度 |
| 2 | **EPS** | GAAP 与 Non-GAAP EPS、YoY、vs 共识 beat/miss |
| 3 | **毛利率 (Gross Margin)** | 本季毛利率、环比/同比变化、驱动因素 |
| 4 | **Operating Margin** | 营业利润率、趋势、费用端（研发/销售）变化 |
| 5 | **FCF (Free Cash Flow)** | 自由现金流金额、YoY、经营现金流 - Capex 说明 |
| 6 | **Cash** | 现金及等价物 / 短期投资、净现金或净负债、回购分红 |
| 7 | **Guidance** | 下季/全年指引 vs 分析师预期，上调/维持/下调 |
| 8 | **AI 业务增长** | AI 相关收入/需求/产能/订单增速，占比与趋势（无则说明） |
| 9 | **Management Commentary** | 财报电话会/新闻稿关键表态：需求、竞争、利润率、资本开支基调 |

## 固定输出结构

```markdown
# [公司]（[TICKER]）FY__ Q_ 财报分析

> 财季：____ | 数据截至：YYYY-MM-DD | 来源：Yahoo Finance

## 一、Revenue
[金额 · YoY/QoQ · vs 共识 beat/miss X% · 一句判断]

## 二、EPS
[GAAP / Non-GAAP · YoY · vs 共识]

## 三、毛利率
[本季 % · 变化 · 驱动]

## 四、Operating Margin
[本季 % · 变化 · 费用端]

## 五、FCF
[金额 · YoY · 质量]

## 六、Cash
[现金/投资 · 净现金或净负债 · 回购分红]

## 七、Guidance
[下季/全年指引 vs 预期 · 上调/维持/下调]

## 八、AI 业务增长
[AI 收入/需求/产能 · 增速 · 占比]

## 九、Management Commentary
[管理层关键表态 3–5 条]

---

## 本次财报

超预期  ⭐⭐⭐⭐☆
利空    ⭐⭐☆☆☆

**一句话总结：** [beat/miss 概览 + 股价潜在反应方向]
```

## 评分口径

结尾必须给出两行星级（1–5 星，实心 ⭐ + 空心 ☆ 共 5 格）：

- **超预期**：综合 Revenue/EPS/Guidance/AI 相对市场共识的 beat 程度。
  - 5 星 = 全面大幅超预期且指引上调；1 星 = 全面不及预期。
- **利空**：本次财报中的负面信号强度（miss、指引下调、利润率恶化、需求走弱、竞争加剧等）。
  - 5 星 = 重大利空；1 星 = 几乎无利空。

两个维度**独立评分**（可同时高，如「beat 但指引保守」）。评分后附一句话总结与预期股价反应方向。

## 分析标准

- 区分**事实**（财报数字/管理层原话）与**判断**（评分、股价预测）。
- 所有财务数字优先取自 Yahoo Finance 对应页面；共识/预期取 Yahoo `Analysis` 页。
- beat/miss 一律标注幅度（金额或 %）。
- 报告末尾一行免责声明：`以上内容仅供参考，不构成投资建议。`

## Examples

**输入：**
```
财报分析 NVDA
```
**输出：** 按 9 项结构解读 NVIDIA 最新季度财报，重点覆盖数据中心/AI 收入增速与 Guidance，结尾给出「超预期 ⭐⭐⭐⭐⭐ / 利空 ⭐☆☆☆☆」类星级卡片。

**输入：**
```
分析 AAPL 财报，重点看服务和毛利率
```
**输出：** 同样 9 项结构；在毛利率、Management Commentary 中加重 Services 与利润率分析，其余项仍须完整，结尾照常给出星级评分。
