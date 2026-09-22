# US Stock Skills

在 Cursor Agent 里做美股研究的一组项目技能。用 Cursor 打开本仓库后，技能会自动出现，不必单独安装。

| 技能 | 适合问什么 | 产出 |
| --- | --- | --- |
| `daily-analysis` | 投资备忘录、目标价、催化剂、风险、技术面、组合视角 | 机构风格的综合研究 |
| `deep-analysis` | 公司深度分析、投资评级、商业模式、竞争优势、增长点 | 先给评级和 12 个月目标价，再展开基本面与估值 |
| `earnings-analysis` | 最新一季财报解读 | 收入、EPS、利润率、现金流、指引，以及超预期 / 利空评分 |

默认中文，标的默认是美股或 ADR。财务和行情数字来自当次拉取的公开数据（雅虎财经、公司财报 / IR），不靠模型记忆。

## 开始使用

1. 用 Cursor 打开本仓库根目录。技能放在 `.cursor/skills/`，只有打开这个项目才会加载。
2. 打开 **Agent** 对话（需要联网拉行情和财报）。Ask 模式只回答问题，不会按技能去取数、写完整报告。
3. 确认技能已加载：侧边栏 **Customize → Skills**，应能看到上面三个名字。看不到就重开一次本仓库。

取数脚本依赖 Python 和 `yfinance`。第一次使用前在仓库根目录执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Agent 会自己调用脚本，一般不用手动跑。

## 两种调用方式

**直接说任务。** Agent 会根据你的问题和技能描述自行选用。

```text
深度分析 NVDA
财报分析 AAPL
给 CRWV 写一份 6 个月投资备忘录，包含目标价和主要风险
```

**手动指定。** 在 Agent 输入框输入 `/`，搜索技能名后回车。斜杠只作用于这一条消息。

```text
/deep-analysis 分析 CRWV
/earnings-analysis TSLA
/daily-analysis MSFT 未来 12 个月的催化剂和估值
```

也可以输入 `@`，把技能作为上下文附上。

想让同一个技能贯穿整段对话：在技能上按 `Option+Enter`（Windows 为 `Alt+Enter`），它会变成当前会话的 Custom Mode，输入框旁会出现徽章。

## 示例

深度分析，要评级和目标价：

```text
/deep-analysis 分析 CRWV
```

财报，要最新一季和超预期评分：

```text
/earnings-analysis NVDA
```

综合备忘录，自己补上期限和侧重点即可：

```text
/daily-analysis 写一份 AMD 的投资备忘录，horizon 12 个月，重点看数据中心 GPU 份额和毛利率
```

没写期限时，综合分析默认按 1–12 个月、美元计价。只给代码、没说要做什么时，说明是研究还是财报，避免选错技能。

## 在别的项目里用

这些技能跟本仓库走。换一个项目打开时不会自动带上。要在所有项目里使用，把对应文件夹复制到个人技能目录：

```bash
mkdir -p ~/.cursor/skills
cp -R .cursor/skills/daily-analysis ~/.cursor/skills/
cp -R .cursor/skills/deep-analysis ~/.cursor/skills/
cp -R .cursor/skills/earnings-analysis ~/.cursor/skills/
```

个人技能只在本机生效。Cloud Agent 需要在 **Settings → Agents → Sync Skills for Cloud Agents** 里打开同步。和同事共享时，把本仓库发给对方，用 Cursor 打开即可。

## 说明

报告供研究使用，不构成投资建议。
