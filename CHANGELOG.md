# 更新日志

本项目所有值得记录的变更都写在这里。格式参考 Keep a Changelog，日期为 `YYYY-MM-DD`。
**约定：每轮修改完成后，由代理在「未发布」下追加一条；人类确认归档后再整理到日期段（见 `AGENTS.md` 准则九）。**

---

## 未发布

### 2026-09-14 · todo.md 批次 3（第 4、7 项）：结局文本扩充 + 300 局全量测试与结局参数标定

**背景**：批次 3 = 第 4 项（结局文本扩充）与第 7 项（300 局全量测试、按结果调结局参数达标）；人类确认口径为「沿用 `test_6` 的真实主链驱动 + 随机合法玩家加点，待业如实记 0%」

**变更（数据，仅 `data/endings.json`）**
- 11 条结局文案由 1 句扩充到 **3~4 句（65 ~ 84 字）**，保留 `{school}` 占位符：先写去向落点，再补过程与回望。结局页排版实测最长一条仅占 4 行（末行 y ≈ 396，按钮区自 y = 850 起）→ **无需改界面**
- 竞争权重与硬门槛按 300 局实测**重新标定**：保研外校 3.5 / 保研本校 6.2 / 考研外校 0.7 / 考研本校 1.9 / 出国留学 2.2 / 进入大厂 0.26 / 创业 0.62 / 进入编制 0.5 / 援建乡村 2.4；**延毕门槛 智力 < 5.4 → 3.3**

**测试与标定过程（第 7 项）**
- 正式测试：**真实 `main.py` 链路 300 局**（合成点击驱动、种子 `20260919`、随机合法玩家加点、存档隔离），共 4 轮（1 轮基线 + 3 轮验证）
- 标定方法：在**快速仿真**（同函数、1000 局）上迭代参数，再用真实 300 局验收；两者口径经对照验证偏差 ≤2 个百分点（如进入编制 17.2% vs 17.7%）
- **关键修复**：调参前**延毕高达 26.3%**（`test_6` 100 局为 24%），根因是「智力 < 5.4」门槛正落在实测终局智力分布的高密度区（300 局 5% 分位 ≈ 3.6）→ 门槛改为 3.3 后延毕降到 **4.0%**
- **最终结果：除结构性不可达的「待业」外，每条结局与归一化目标的偏差都在 ±2 个百分点内（最大 1.7）**，对原目标最大偏差 3.0

**最终 300 局实测（种子 20260919）**

| 结局 | 实测 | 原目标 | 归一化目标 | 偏差 |
| --- | --- | --- | --- | --- |
| 保研本校 | 23.0% | 20% | 22.2% | +0.8 |
| 考研本校 | 20.7% | 20% | 22.2% | −1.5 |
| 进入大厂 | 10.0% | 10% | 11.1% | −1.1 |
| 创业 | 11.3% | 10% | 11.1% | +0.2 |
| 进入编制 | 10.7% | 10% | 11.1% | −0.4 |
| 待业 | **0.0%** | 10% | —（结构性不可达） | — |
| 考研外校 | 6.3% | 5% | 5.6% | +0.7 |
| 援建乡村 | 7.3% | 5% | 5.6% | +1.7 |
| 延毕 | 4.0% | 5% | 5.6% | −1.6 |
| 出国留学 | 3.7% | 3% | 3.3% | +0.4 |
| 保研外校 | 3.0% | 2% | 2.2% | +0.8 |

**其它实测（同一次 300 局）**
- 运行完整性：**300 / 300 局零异常**、14805 帧、14804 次合成点击、**0 个空回合**（候选池为空 0 次）
- **成就 19 / 19 全部解锁**（含 `test_6` 中不可达的「军工强校」第 17 局、「！？拉拉！？」第 21 局、「！？给给！？」第 32 局）
- 入党三步链：申请书 67.7% → 积极分子 30.0% → **正式党员 10.0%**（无天赋）
- 恋爱线：被表白 100 次（答应 51 / 婉拒 49）、主动表白 88 次（成功 45 / 失败 43）、同性在一起 4 局、回溯 5 局
- 事件覆盖 **184 / 191**（181 条被匹配器命中 + 3 条 `{shuyuan}` 事件因显示时占位符被替换而未被认出，实际已触发）；仍未触发的 7 条 = 6 条「平平淡淡」保底文案 + 1 条假期作息事件

**新增文档**
- `test_7.md`：**测试报告 7 · 300 局全量测试（结局参数标定后 · 真实界面代码路径）**，12 节 —— 测试方法、运行完整性、分布对照、**四轮标定过程**、终局属性与综测、各硬门槛实测通过率、第 3/5 项新增内容实测、成就、事件覆盖、与 `test_6` 的对照、测试局限、结论

**文档同步（2 份）**
- `docs/ending.md`：§3 硬门槛表的「实测通过率」按 300 局更新（保研外校 11.3%、保研本校 34.7%、考研类 89.3%、出国 11.0%（家境与语言成绩两道门槛同时通过）、大厂 97.7%、创业 61.3%、编制 100%、援建 41.3%、延毕 4.0%）；§4 竞争权重说明改按新权重（**保研本校 6.2 为最高**）；§6「目标分布与实际分布」整表替换为 300 局实测
- `docs/ending-list.md`：11 行按新文案 + 新权重 + 新门槛重新生成

**本轮无其它代码改动**：未改 `main.py`、`game/`、`docs/01~05`（`ending.md` 除外）；临时脚本与结果文件全部删除，仓库真实 `save/records.json` 未改

**待人类确认**
1. 延毕门槛现为「智力 < 3.3」（实测 4.0%，目标 5%）—— 若觉得太严可回调到 3.5 左右
2. 「待业」仍 0%：纯兜底 + 就业类门槛 100% 通过；本批**未**给它加真实门槛（沿用此前裁定）
3. 6 条「平平淡淡」保底事件与 `进编制` 标签 0 供给两项死内容仍未处理
4. 300 局下单条结局的 95% 置信区间约 ±1 ~ ±4 个百分点，故偏差进入 ±2 个百分点即停止拟合，避免过拟合到本组随机数
---

### 2026-09-14 · 批次 2 追加调整：入党链 5 步改 3 步、恋爱中「TA」改「对象」

**背景**：人类指示「**1 将 5 步改为 3 步入党；2 恋爱中 TA 可以改为对象；其余不变**」

**变更（数据，仅 `data/events.json`）**
- 入党链 **5 步 → 3 步**：删除「你被列为发展对象。」与「你成为了预备党员。」两条事件；第三步「你按期转为正式党员。」的 `flags_need` 由 `["预备党员"]` 改为 `["积极分子"]` —— 链路变为 **递交入党申请书 → 入党积极分子 → 正式党员**（时段 常规 / 寒假 / 暑假、权重 5、`入党` / `党员` 标签、「光荣入党」成就、`党员 × 3` 结局权重均**不变**）
- 恋爱中的 3 条事件文案把「TA」改为「**对象**」：「你和对象一起去看了场电影。」「你和对象因为一件小事吵了起来。」「你和对象分开了。」
- 事件 **193 → 191** 条（基础 101 / 特殊 90；常规 106、特殊时段 88）

**实测（300 局逻辑层仿真）**
- 入党三步到达率：普通玩家 97.3% → 85.0% → **正式党员 65.0%**；带「根正苗红」三步均 **100%**
- 被表白 37.3%（普通玩家）/ 47.3%（带「彩虹」）；同性在一起 23.0%（需「彩虹」）
- 三步化把「光荣入党」的解锁率从五步时的 20% 提升到 **65%**，与「根正苗红」的差距仍然明显（65% → 100%）
- `data/events.json` 全文已无「TA」（0 次）

**验证**
- 5 局真实 `main.py` 链路冒烟：零异常、零意外场景；**4 / 5 局走完三步**（与 65% 的实测吻合），实测出现「你和对象一起看了场电影。」与「你按期转为正式党员。」
- 四份 JSON 重新解析通过；仓库真实 `save/records.json` 未改

**文档同步（7 份）**
- 重新生成 `docs/event-list.md`（191 条 + 结果分支附表）
- `docs/event.md`：事件池 191 条（基础 101 / 特殊 90）；时段统计改为 常规 106、特殊时段 88（寒假 46、暑假 47）；状态标志用法改为**入党三步**
- `docs/02-游戏设计.md`：「入党线」改为三步；事件总数 191 条
- `docs/talent.md`、`docs/01-可行性分析.md`、`docs/03-项目架构设计.md`、`README.md`：事件条数 191
- **顺带修掉一处上一批的漏改**：`docs/03-项目架构设计.md` 里 `event-list.md` 的条数在批次 2 时仍停在 184（未随批次 2 更新为 193），本批一并更正为 191

**待人类确认**：三步化后「光荣入党」解锁率约 65%，若希望它更稀有，可降低入党事件权重（现为 5）或收紧时段（现为 常规 / 寒假 / 暑假）
---

### 2026-09-14 · todo.md 批次 2（第 3、5 项）：表白线重构、被表白事件、入党五步链

**背景**：批次 2 = 第 3 项（表白文案改性别、被表白事件、三条表白系成就）与第 5 项（入党五步链、天赋「根正苗红」、成就「光荣入党」、入党提升编制/援建概率）；人类已授权「成就新增判定类型」等代码扩展

**变更（代码，2 处）**
- `game/events.py` `pick_event`：新增 **`chance_attr`**（`{base, attrs, max}`）—— 触发概率随属性变化，`概率 = base + Σ(属性值 × 系数)`，上限 `max`；没有该字段时行为与原来完全一致
- `game/achievements.py`：成就新增**「状态」判定类型**（`value` 里的状态需全部具备，如 `["同性恋爱", "女"]`），供三条表白系成就与「光荣入党」使用

**变更（数据）**
- `data/events.json`：事件 **184 → 193** 条
  - 表白线：4 条主动表白的成功 / 失败文案把「TA」改成确定的**他 / 她**；同性（需「彩虹之下」）成功分支追加状态「同性恋爱」，4 条失败分支统一追加状态「表白被拒」
  - 新增 4 条**被表白事件**（特殊 / 常规）：异性 2 条（`chance_attr` = 5% + 颜值×4%，上限 60%）、同性 2 条（1% + 颜值×1%，上限 15%，且需「彩虹之下」）；答应 / 拒绝固定 50%（`check.base = 50`、无属性系数）；**不带「表白」标签**，因此不吃「花言巧语」加成
  - 新增 5 条**入党链**事件（特殊）：递交入党申请书 → 入党积极分子 → 发展对象 → 预备党员 → 正式党员，用 `flags_need` 依次卡顺序；时段 常规 / 寒假 / 暑假、权重 5；最后一步带 `入党` + `党员` 两个标签
- `data/talents.json`：天赋 **26 → 27** 条，新增紫级「**根正苗红**」（`boost {入党: 5}`）
- `data/achievements.json`：成就 **15 → 19** 条，新增「！？拉拉！？」（同性恋爱 + 女）、「！？给给！？」（同性恋爱 + 男）、「悲伤的故事」（表白被拒）、「光荣入党」（正式党员），全部使用新的「状态」类型
- `data/endings.json`：`进入编制` 与 `援建乡村` 的影响因子各加 `党员 × 3`（入党后更容易走向体制内 / 援建）

**调参过程（重要，只调内容数值，未改结局参数）**
- 首轮实现后实测：入党五步走完仅 **5.0%**（真实链路 60 局）、被表白 60 局 **0 次**
- 逻辑层定位（300 局仿真）：机制本身正确 —— 问题出在**权重**（`chance` 是逐回合筛选，还要再与整池权重竞争，权重太低会被淹没），以及**常规时段只有约 25 个回合**，五步顺序链在原设定下几乎不可能走完
- 调整：入党事件时段放宽为 常规 / 寒假 / 暑假、权重 6 → 5；被表白事件权重 1 → 6
- 调整后复测（各 300 局）：入党五步走完 **20.0%**（普通玩家）/ **99.7%**（带「根正苗红」）；被表白 **39.7%**（普通玩家；同性线需「彩虹」故为 0%）

**验证**
- 语法检查通过；四份 JSON 重新解析通过（事件 193 / 天赋 27 / 成就 19 / 结局 11）
- 定向行为验证：`chance_attr` 生效（异性被表白 颜值 0 → 5.5%、5 → 26.4%、10 → 46.2%、20 → 60.0% 封顶）；同性被表白 颜值 20 → 15.8% 封顶，且**无「彩虹」时 500 次全部被挡住**；三条表白系成就与「光荣入党」按状态正确解锁，普通恋爱不会误触发；`党员` 使 进入编制 得分 4.24 → 7.24、援建乡村 0.88 → 3.88
- 真实链路：60 局（调参前）+ 5 局（调参后）均零异常、零意外场景；5 局冒烟中实测出现「你答应了他，你们在一起了。」（被表白成功）与走完五步的「你按期转为正式党员。」（7 次入党链事件）
- 仓库真实 `save/records.json` 全程未改（哈希一致）

**文档同步（本批已完成，10 份）**
- 重新生成 `docs/event-list.md`（193 条 + 结果分支附表，新增 `chance_attr` 的概率列渲染）、`docs/talent-list.md`（27 条）、`docs/achievement-list.md`（19 条 / 八类）
- `docs/event.md`：新增 `chance_attr` 字段说明；状态标志用法补同性恋爱 / 表白被拒 / 入党五步；内容规模 193 条、标签 10 种（新增 `入党`、`党员`）
- `docs/04-程序设计.md`：玩家 `flags` 补新状态；事件字段补 `chance_attr`；成就类型补「状态」并补 `value` 形式；`pick_event` 说明补概率判定
- `docs/02-游戏设计.md`：天赋 27 条、事件 193 条；新增「恋爱线」「入党线」两条说明；成就七类 + 19 条
- `docs/ending.md` / `docs/ending-list.md`：编制 / 援建的 `党员 × 3` 影响因子
- `docs/01-可行性分析.md`、`docs/03-项目架构设计.md`、`docs/05-页面设计.md`、`README.md`：条数同步（事件 193 / 天赋 27 / 成就 19）
- 三份清单均做**严格逐行比对**：除预期内容变化外**零格式漂移**

**待人类确认**
1. 入党链的时段（常规 / 寒假 / 暑假）与权重 5 是代理为了「让五步链走得完」而调的，若要更稀有 / 更常见可直接改 `data/events.json`
2. 带「根正苗红」时五步走完率 **99.7%**（boost 5 的效果），若嫌过强可降到 3
3. 被表白事件的数值（异性 5% + 颜值×4% / 同性 1% + 颜值×1%、答应 50%、权重 6）为代理按方案取值，可按实测调整
4. 「悲伤的故事」目前只由**主动表白被拒**触发（拒绝他人的表白不计入）
5. 恋爱中的 3 条后续事件（约会 / 争吵 / 分手）文案仍是「TA」，本轮按需求只改了表白事件 —— 是否一并改性别由人类定夺
---

### 2026-09-14 · 批次 1 文档同步 + pycache 取消跟踪

**背景**：人类确认「**文档同步做一批改一批**」（即本批改的数据与代码，本批就把 `docs/` 同步掉），并指示 `game/__pycache__/*.pyc` **取消跟踪**；同时澄清 `test_1`~`test_5` 的删除与 `todo.md` 的改动均为**人类本人**所为，`问卷-游戏反馈调查.md` **无需提交**

**变更（文档同步，10 份）**
- `docs/event-list.md`：按 `data/events.json` **整份重新生成**（181 → **184** 条；常规 96 → 99；特殊 81 → 83、基础 100 → 101）—— 3 条书院级组织事件改为 `{shuyuan}` 占位符、原「学生组织/社团」拆为「校团委 / 街舞社」、北湖文案同步、追加雅思 / 托福两条；附表「判定事件的结果分支」一并重生成（新增雅思 / 托福各 2 个分支行）
  - **生成口径与原文完全一致**：效果列按固定属性序（智力 / 体质 / 颜值 / 家境）、时段用「 / 」连接、条件写作「需「」/ 未「」」、附表空事件名单元格写作 `| | `；重新生成后与原文**严格逐行比对**，除 13 处预期内容变化（8 增 5 改）外**零格式漂移**
- `docs/event.md`：事件池 181 → 184；`text` / `set_org` 字段补 `{score}`、`{shuyuan}` 占位符说明；`{score}` 判定注明**分数取整**；§3 状态标志补语言考试用法（`flags_forbid ["语言考试"]` 两考互斥且各一次、达标分支给「语言成绩达标」）；§8 内容规模同步
- `docs/04-程序设计.md`：事件 `text` / `set_org` 补占位符；**结局字段表新增 `flags_need`**；§2 结局判定第 2 步补 `flags_need`；函数表补 `roll_check`（`score` 取整）与 `apply_event`（占位符替换）
- `docs/ending.md`：§3 硬门槛表「出国留学」补「且状态『语言成绩达标』」；§8 字段表新增 `flags_need`；§6 分布表下加注（该表是结局系统刚落地时的 3000 局实测值，出国留学门槛已变，将在 300 局测试后统一更新）
- `docs/ending-list.md`：出国留学门槛列补「状态『语言成绩达标』」
- `docs/02-游戏设计.md`：事件总数 181 → 184；硬门槛示例补「且考出语言成绩」
- `docs/01-可行性分析.md`、`docs/03-项目架构设计.md`、`docs/talent.md`、`README.md`：事件条数 181 → 184
- **未改**：`AGENTS.md`（其 §0 未写事件条数，无需修订）、`test_1`~`test_6.md`（历史测试报告按当时的数据版本如实记录，不做追溯修改）

**变更（仓库整理）**
- `game/__pycache__/` 下 **8 个 .pyc 取消 git 跟踪**（`git rm -r --cached`，磁盘文件保留；`.gitignore` 已含 `__pycache__/`，此后不再进入提交）
- `prototype/__pycache__/game.cpython-312.pyc` **仍在跟踪中**（人类只点了 `game/`，未擅自处理，待确认）

**事实澄清（非本轮代理改动）**
- `test_1.md`~`test_5.md` 的删除与 `todo.md` 的改动均由人类本人完成
- `问卷-游戏反馈调查.md` 按人类指示**不提交**，保持未跟踪状态

**本轮无代码与数据改动**（只动了文档与 git 索引）
---

### 2026-09-14 · todo.md 批次 1（第 1、2、6 项）：书院组织名、北湖文案、四六级取整、雅思托福与出国前提

**背景**：人类在 `todo.md` 写入 7 项改动；确认「**分三批推进，每批做完汇报**」，批次 1 = 第 1、2、6 项；并授权 4 处必要代码扩展（占位符、chance_attr、结局 flags_need、score 取整）与成就新增判定类型

**变更（代码，均为几行小改，未引入新依赖、未改技术栈）**
- `game/events.py`
  - `apply_event`：新增 `{shuyuan}` 占位符替换（与既有 `{score}` 同类），文案与 `set_org` 一并替换为玩家所属书院 → 「你加入了睿信科协。」且 `player["org"] = "睿信科协"`（组织部长 / 主席文案随之正确）
  - `roll_check` 的 `score` 分支：返回值改为 `int(val)` → 四六级分数为整数（截断）
- `game/endings.py`：`fits()` 新增 `flags_need` 硬门槛（与事件 schema 同名字段、同语义）→ 结局可以要求玩家状态

**变更（数据）**
- `data/events.json`：事件 **181 → 184** 条
  - 三条书院级组织事件的文案与组织名改用 `{shuyuan}`：`书院科协` → `{shuyuan}科协`、`书院自管委` → `{shuyuan}自管委`、`书院学生会` → `{shuyuan}学生会`
  - 含糊的通用事件「你加入了学生组织/社团。」（`set_org` 直接显示「学生组织/社团」）拆为两条具体组织：**「你加入了校团委。」**（学生组织）与 **「你加入了街舞社。」**（社团），各 `weight 15`（原 30，总量不变，保持「必定加入组织」的强度与分布）
  - 第 2 项：`寒假你去北湖看鹅，结果被羊驼追了两步。` → `寒假你去北湖看羊驼，结果被鹅追了两步。`
  - 新增两条语言考试事件（特殊 / 常规 / `weight 3` / `flags_forbid ["语言考试"]`，两考互斥且各只有一次机会）：
    - 「你考了雅思。」达标线 6.5，得分 = 2.5 + 智力×0.35 + randint(0,3)
    - 「你考了托福。」达标线 90，得分 = 63 + 智力×2 + randint(0,20)
    - 达标分支给 flag「语言成绩达标」；未达标分支只给「语言考试」（把唯一一次机会用掉）
- `data/endings.json`：**出国留学**新增 `flags_need: ["语言成绩达标"]`（原 `need 家境 ≥7.1` 保留）

**验证**
- 语法检查通过；两份 JSON 重新解析通过（events 184 / endings 11）
- 行为验证（真实函数调用）：
  - `{shuyuan}`：睿信 / 特立 → 「你加入了睿信科协。」「你加入了特立自管委。」「你加入了睿信学生会。」，`set_org` 同步正确
  - 四六级：连续 8 次抽样全部为 `int`（553 / 548 / 537 / 580 / 505 / 581 / 554 / 538）
  - 语言考试达标率（各 300 次抽样）：雅思 智力 5 → 26.3%、8 → 53.3%、10 → 80.0%；托福 智力 5 → 15.7%、8 → 44.0%、10 → 70.0%（托福初始 40 + 智力×4 时智力 8 仅 15%，已对齐为 63 + 智力×2）
  - 出国留学：无「语言成绩达标」→ `fits = False`；有 → `fits = True`；有 flag 但家境 6.5 → `fits = False`（两道门槛同时生效）；其余 10 条结局未受 `flags_need` 影响
- **8 局真实 `main.py` 链路**：零异常、零意外场景；实测出现「你加入了睿信 / 求是 / 特立自管委」「你加入了校团委」「你加入了街舞社」「寒假你去北湖看羊驼，结果被鹅追了两步。」「雅思 / 托福出分…」以及「你在「校科协」留任了部长」等正确替换，其中 1 局拿到「语言成绩达标」
- 仓库真实 `save/records.json` 全程未改（测试使用独立临时存档，测试后哈希一致）

**本轮未做**：第 3、4、5、7 项（按人类确认的分批顺序留待批次 2、3）

**待人类确认**
1. 拆分出的两条组织名由代理拟定（**校团委** / **街舞社**），若需换成其它组织 / 社团名，改 `data/events.json` 即可
2. `docs/event.md`（事件字段表）、`docs/04-程序设计.md`（`apply_event` / `roll_check` / `fits` 的描述）、`docs/ending-list.md`（出国留学门槛）、`AGENTS.md §0`（事件 181 → 184）已与新实现不一致 —— 本轮未改（准则六），是否同步由人类定夺
3. 雅思 / 托福的达标数值是代理拟定的**临时值**，按第 7 项将在 300 局测试后统一调参
4. 上一轮问卷设计稿 `问卷-游戏反馈调查.md` 仍未提交（`?? 未跟踪`）
---

### 2026-09-14 · 游戏反馈调查问卷（新增 问卷-游戏反馈调查.md）

**背景**：人类「请设计一份游戏反馈调查问卷，内容包括基本信息（年级、是否校内）、游戏画面（UI、美术）、游戏内容（事件、天赋、成就、属性）、游戏可玩性、与北理工主题符合度等，生成md文件」；确认四项 —— **只做在线问卷**、**精简版 12~15 题**、**汇报证据与改版定位并重**、**放仓库根目录**

**新增**
- `问卷-游戏反馈调查.md`（189 行）：**15 题在线问卷设计稿**，含六节
  - 一、设计依据（准则二检索结果：5 条来源的「采用 / 不采用」及理由）+ 全卷量表规格
  - 二、问卷正文：卷首语 + 基本信息 3 题（年级 / 是否校内 / 玩到哪一步）+ 游戏画面 2 题（UI、美术）+ 游戏内容 4 题（事件、天赋、成就、属性与结局判定的可理解性）+ 可玩性 3 题（节奏、重开意愿、推荐意愿）+ 北理工主题 2 题（贴合度、最有共鸣的校园元素）+ 开放题 1 题
  - 三、在线投放设置清单（题型映射、Q3 分流跳转逻辑、匿名与防重复提交设置）
  - 四、统计口径（4 轴板块均分与雷达图、NPS 算法、3 组交叉分析、Q14/Q15 定性整理）
  - 五、投放与回收建议（样本量门槛、校内/校外分层、渠道）
  - 六、说明

**设计要点（备查）**
- 题型构成：单选 3 + 五点李克特 9（Q4~Q11、Q13，平台侧由一道 9 行矩阵题承载）+ 0~10 评分 1（推荐意愿）+ 限选 3 的多选 1 + 开放题 1（选填）
- 五点量表全卷**正向陈述统一**（1 非常不同意 ~ 5 非常同意、不设反向题，便于直接算均分）；未体验栏目可答「没注意到 / 没体验过」，按**缺失值**处理并单列有效样本数 n
- 坚持**一题一构念**，避免双管题（依据 SurveyMethods、Culture Amp 的问卷设计要点）
- **精简题量的依据**：UES-SF 把长量表压到 12 题仍可支撑分维度计分；GUESS 只借鉴其维度划分、不取其题量；SUS 因只测可用性、覆盖不到内容与主题维度而**不采用**
- Q3 设为**分流题**：只看了首页的答卷跳过 Q6~Q12，确保内容与可玩性评分有真实体验作依据

**本轮无代码与数据改动**：未改动 `main.py`、`game/`、`data/`、`docs/`、`AGENTS.md`；唯一新增文件是 `问卷-游戏反馈调查.md`

**待人类确认**：问卷**未实际投放**，§四 的样本量门槛与统计结论均为口径建议；若要给「事件 / 天赋 / 成就」拆出单条内容的评分题，按 §六 建议另加一页追问，而不是撑大本卷

**事实更新（非本轮改动）**：人类已提交 `5d59803 docs:第六轮测试`（含 `CHANGELOG.md` 与 `test_6.md`），该提交同时把工作区里已删除的 `build_exe.ps1` 一并提交为删除（−71 行）；上一轮记录的「是否恢复由人类定夺」至此由人类的提交给出结论，代理不再处理
---

### 2026-09-14 · 100 局全量测试（新增 test_6.md）

**背景**：人类「对游戏做100局全量分析测试，补充文档」；确认四项 —— 驱动真实 `main.py` 代码路径、报告新建 `test_6.md`、测试脚本跑完即删不入库、固定随机种子可复现

**新增**
- `test_6.md`：**测试报告 6 · 100 局全量测试（结局系统重构后 · 真实界面代码路径）**，15 节 352 行
  - §1~2：测试方法与运行完整性（含可复现性验证）
  - §3~6：开局分配、8 个学期期末属性曲线、6 次综测排名、结局与升学院校
  - §7：**归因交叉表**（开局智力分档 → 结局，附相关系数）
  - §8~11：天赋、事件覆盖、成就、标签与其它数据
  - §12：各结局**硬门槛通过率**（解释每条结局的局数是怎么来的）
  - §13~15：测试局限与未覆盖面、8 项问题分析、结论

**测试方法（临时脚本未入库，已删除）**
- **驱动方式**：给 `pygame.event.get` 打桩，按当前场景合成左键点击，让 `main.py` 自己的主循环跑完 100 局；每次点击都走真实点击处理分支（「随机分配」「开始」「下个月」「再来一局」），因此综测排名计算、成就写入、回溯重置这些**只写在 `main.py` 里**的逻辑都被真实覆盖
- 无显示器 / 无声卡：SDL `dummy` 视频与音频驱动；窗口 540×960 时 `scale = 1`、偏移 0（实测），合成点击坐标 1:1 命中
- **存档隔离**：`game.records.RECORDS_PATH` 指向 `_sim100_save.json`，仓库真实 `save/records.json` 全程未改（测试前后 SHA256 一致 `CE511E59…AE26`）
- `game.events.pick_event` 外套一层只做计数的外壳，统计「候选事件池为空」的回合数
- 临时的 `_sim100.py`、`_sim100_gate.py` 与全部 `_sim100*` 结果文件、`__pycache__` 已在测试后删除，仓库不留脚手架（准则三）

**核心发现**
- **运行完整性**：100/100 局零异常、4910 帧、0 个空回合（4808 个事件月全部命中事件池）、`pick_event` 返回 `None` 0 次；同种子**独立重跑两次，逐局结局 100/100 完全一致**（可复现性验证通过）
- **结局命中 10 / 11 种**（`test_5` 时期仅 2 种）；延毕 **24%**（目标 5%）、待业 0%（沿用 `test_5` 的结构性结论）
- **延毕是最大偏差**：24 局延毕**全部满足至少一条升学或就业门槛**（`图书馆`≥2 的 24/24、`进大厂`≥1 的 23/24、`学生组织`≥1 的 24/24），被判定第一步「延毕优先」截胡
- **归因（本篇最重要的结论）**：开局智力与最终智力 **r = 0.946**、与平均综测百分位 **r = −0.956**；开局智力 ≤4 的 26 局中 24 局延毕（92%），≥6 的 36 局中 0 局延毕 —— 结局在开局点完属性点时基本已定，48 回合的属性总增幅仅 +5.47
- **综测排名大二起失去区分度**：每学期 **14 ~ 25 局并列年级第一**（`rank = int(total × pct / 100)` 与 `pct` 下限 1 的组合，得分 ≥81.5 即为第 1 名）
- **内容不可达**：事件覆盖 **170/181**，11 条不可达（6 条「平平淡淡」保底文案 `weight 0.2` 被完全支配、3 条表白事件、1 条军训事件）；成就 14/15（「军工强校」不可达，因其绑定事件 100 局 0 触发）；`进编制` 标签仍 0 条供给（承接 `test_5` §6.1）
- **与 CHANGELOG 记录的 3000 局口径不一致**：延毕 24% vs 4.8%、保研本校 13% vs 22.3%、考研本校 11% vs 20.0%；两次测试**同种子 `20260919`**，且 `data/endings.json`（自 `f7ca1a5` 引入 `延毕: 智力 < 5.4` 门槛后）与 `game/endings.py` 均未改动，故差异只能来自两次测试的**加点口径不同**（3000 局那次的具体加点策略未记录）。已在 §14.4 如实记录，未做任何数值改动

**本轮无代码与数据改动**：未改动 `main.py`、`game/`、`data/`、`docs/`、`AGENTS.md`；唯一新增文件是 `test_6.md`

**待人类确认（准则六，本轮只记录未处理）**
1. §14.4 的口径差异：是把本篇（真实代码路径 + 可复现）作为新基准，还是用同一驱动重跑 3000 局做对齐
2. 延毕 24%、综测排名大面积并列第一是否调整（涉及 `data/endings.json` 门槛与 `main.py` 名次公式）
3. 死内容是否激活（6 条保底事件、3 条表白事件、「军工强校」成就、`进编制` 标签 0 供给）
4. **顺带核实（非本轮改动）**：工作区里 `build_exe.ps1` 已处于**删除（D）**状态（`git status` 可见，非代理所为 —— 上一轮代理只删了 `BIT重开模拟器.spec`）；该文件在 `HEAD` 中存在（3137 字节），`git checkout -- build_exe.ps1` 可恢复，是否恢复未擅自处理

---

### 2026-09-14 · 打包产物清理 + 交付压缩包核对 + GitHub Releases 发布准备

**背景**：人类「我已打包并压缩，请清理打包文件，并帮我将压缩包发布」；确认项三项 —— 压缩包由**人类自行压缩**、成品 zip 存放于 `dist/`、发布渠道选定 **GitHub Releases**

**变更（清理，准则六仅清理打包产物）**
- 删除 `BIT重开模拟器.spec`（PyInstaller 按命令行参数自动生成的构建描述文件，`.gitignore` 已忽略，下次打包会重新生成）
- `build/` 由**人类自行删除**；`web/`（含此前被进程占用的空目录 `web\audio`）已随网页路线终止一并清除
- **保留** `dist/BIT重开模拟器/`（人类还需用它压缩交付包），以及 `game/`、`prototype/` 下的 `__pycache__`（Python 缓存，`.gitignore` 已忽略，未擅自删除）

**核对结果（发布前验证）**
- ❌ **首次压缩包内容错误（已废弃）**：`F:\Re-BIT\build\BIT重开模拟器.zip`（7,421,546 字节）压的是 PyInstaller **中间产物目录 `build/`** —— 包内仅 `Analysis-00.toc`、`PKG-00.toc`、`PYZ-00.pyz`、`xref-BIT重开模拟器.html`、`localpycs/` 与一个裸 exe，**缺 `_internal/`、`data/`、`fonts/`、`audio/`、`save/`**，解压后双击必然报错，不可用于发布
- ✅ **交付包核对通过**：`dist/BIT重开模拟器v0.2.zip` —— 134 条目、17,493,811 字节、解压后 41,463,805 字节（压缩率 58%），逐项齐全：`BIT重开模拟器.exe`、`_internal/python312.dll`、`_internal/pygame/*.pyd`、`data/`（events/talents/endings/achievements 四个 json）、`fonts/zpix.ttf`、`audio/click.ogg`、`save/records.json`、**空目录 `exports/`**（`game/records.py` 直接写入 `exports/xxx.txt`，该目录必须存在，丢失会导致导出成绩失败）；包内无 `__pycache__` 或构建残留
- ✅ **成品自检**：以 dummy SDL 驱动启动 `dist\BIT重开模拟器\BIT重开模拟器.exe`，4 秒内未退出 → 打包成品可正常运行
- 校验值：大小 `17493811` 字节，SHA256 `260DBF170EE6B272D75EA120EC28F4587AAE8449E8DED2E26070F2A9C06DDA61`
- 推送状态：`main` 与 `origin/main` 同步于 `c56f7a9 feat:exe打包`，无未推送提交

**待人类执行（发布）**
1. 打开 https://github.com/FlySkyXing/Re-BIT/releases/new
2. tag 填 `v0.2`（Create new tag on publish），目标分支 `main`
3. 标题与发布说明见本轮对话给出的 Markdown（可直接粘贴）
4. 把 `F:\Re-BIT\dist\BIT重开模拟器v0.2.zip` 拖入「Attach binaries」区，Publish release

> **沙箱无网络能力**（`pip install`、`git push`、URL 上传均不可用；TLS 握手失败），因此**上传动作只能由人类在浏览器完成**，代理负责核对产物、给出逐步命令与发布说明文案

**本轮无代码改动**：未改动 `main.py`、`game/`、`data/`、`docs/`、`AGENTS.md`

**遗留（交人类决定）**
- 远程 `gh-pages` 分支仍保留已终止的网页版部署（`14ed83b deploy: 北理工重开模拟器网页版 2026-09-13 21:47`），是否删除该分支未擅自处理
- 压缩包内**无顶层文件夹**（解压后 `BIT重开模拟器.exe` 与各资源目录直接铺在当前目录），建议在发布说明中提示「解压到新建的空文件夹」

---

### 2026-09-14 · 新增 exe 打包（PyInstaller --onedir + 资源外置）

**背景**：人类要求「将文件打包成 exe 可执行文件」，并选定 **PyInstaller** + **单目录 + 资源外置**

**新增**
- `build_exe.ps1`：**一键打包脚本** —— 检查 PyInstaller 是否安装 → `python -m PyInstaller --noconfirm --clean --onedir --noconsole --name "BIT重开模拟器" main.py` → 把 `data/` `fonts/` `audio/` 复制到 exe 旁边 → 生成空白 `save/records.json`（**不带 BOM**，否则 Python 的 `json.load` 会报 `Expecting value`）与 `exports/` → **启动自检**（dummy 视频驱动跑 3 秒，进程未在 3 秒内退出即通过）→ 打印交付说明
- `.gitignore`：新增 `build/`、`dist/`、`*.spec`（PyInstaller 产物）
- `requirements.txt`：以**注释形式**注明打包工具（不参与运行期安装）
- `README.md`：新增「打包成 exe（Windows）」小节（安装、一键打包、脚本做了什么、产物与交付方式、为什么不选 `--onefile`）

**设计取舍（准则二检索依据）**
- `--onefile` 需把资源打进包、代码改用 `sys._MEIPASS` 取路径（[PyInstaller #8997](https://github.com/pyinstaller/pyinstaller/issues/8997)），且每次启动解压到临时目录 → **启动慢几秒、常被杀软误报**（[onefile 机制](https://devbytes.co.in/news/understanding-pyinstallers-onefile-mode)、[误报案例](https://github.com/TomSchimansky/TkinterMapView/issues/136)、[方案对比](https://codegym.cc/groups/posts/python-script-to-exe)）
- 故选 **`--onedir` + 资源外置**：**零代码改动**、启动快、误报少；交付时压缩整个目录即可

**验证（本地可验证的部分）**
- 脚本语法检查通过（UTF-8 带 BOM，Windows PowerShell 5.1 下中文不乱码）
- 存档写入逻辑单独验证：生成的 `records.json` 无 BOM，`json.load` 解析成功
- **未执行实际打包**：本机未安装 PyInstaller 且沙箱无网络（`pip install` 不可用）

**待人类执行**
1. `python -m pip install pyinstaller`
2. `powershell -ExecutionPolicy Bypass -File build_exe.ps1`
3. 双击 `dist\BIT重开模拟器\BIT重开模拟器.exe` 验证；交付时压缩整个 `dist\BIT重开模拟器` 目录

**待人类确认（准则四）**：`AGENTS.md` 准则四的技术栈表可考虑加一行「打包工具：PyInstaller（仅构建 exe 时使用）」—— 该文件由人类维护，代理未擅自改动

---

### 2026-09-14 · PyScript / Pyodide 路线终止（失败归档）与清理

**结论：网页版第二条路线（PyScript / Pyodide）终止** —— 人类裁定「打开主页，但在运行中报错，请同样放弃该路线」

**这条路线走到哪一步（备查）**

1. ✅ PyScript 与 Pyodide 加载成功（`/lib/python314.zip/`，该版本内置 **Python 3.14.2**）
2. ✅ `pygame-ce 2.5.7 (SDL 2.32.10)` 安装成功（`config='{"packages": ["pygame-ce"]}'` 声明式预加载生效）
3. ✅ 按官方《Using SDL》启用实验性 SDL 的 opt-in 标志 `pyodide._api._skip_unwind_fatal_error = true`，并用 `pyodide.canvas.setCanvas2D()` 注册 `id="canvas"` 画布
4. ✅ **游戏首页成功渲染在页面画布上**（比 pygbag 路线走得远得多）
5. ❌ 随后在**运行中**报错（人类未提供具体堆栈）→ 终止，不再投入

**变更（清理）**
- 删除 `web/`（20 个文件）：网页版源码副本（async 改造版 `main.py`）、PyScript 引导页、`web/README.md`、游戏资源副本
- **归档唯一不可再生的产物**：`archive/2026-09-14-pyscript/index.html` + `归档说明.md` —— 该引导页积累了四轮浏览器实测的结论，无法靠推导重建；说明文件里记下了 6 条必备结论（Python 侧无 `loadPackage` 要用 `pyodide_js`、`micropip` 默认不加载、SDL 需 opt-in 标志、需 `setCanvas2D` 注册画布、主循环必须 async、官方文档链接）
- **遗留**：空目录 `web\audio` 被其它进程占用未能删除（应是仍有终端停留在 `web\` 目录下）；关闭该终端后执行 `rmdir /s /q web` 即可

**两条网页路线至此均已终止**
- pygbag（社区 WASM 打包器）：见「网页部署路线终止（失败归档）与相关文件清理」
- PyScript / Pyodide：本条

**未受影响**：桌面版 `main.py`、`game/`、`data/`、`docs/`、`AGENTS.md` 一律未改动；`archive/` 仅新增一个快照目录

---

### 2026-09-14 · 按官方《Using SDL》文档启用 SDL opt-in 标志（人类提供文档原文）

**背景**：人类第四次实测的日志里 Python 侧注册画布失败，并提供了 Pyodide 官方文档《Using SDL》原文。文档给出三条硬要求，此前我们**漏了第 1 条**（这正是「Pyodide has suffered a fatal error」的直接原因）：

1. SDL 支持在 Pyodide 中**实验性**，必须启用 opt-in 标志：`pyodide._api._skip_unwind_fatal_error = true;`
2. 必须注册画布，且对象要是 `id="canvas"` 的 `HTMLCanvasElement`：`pyodide.canvas.setCanvas2D(canvas)`
3. 主循环必须 async + 每帧 `await asyncio.sleep(1 / fps)`（此前已按官方 PyScript 示例做到）

**修复**
- `web/index.html`
  - 页面脚本：轮询等 `window.pyodide` 就绪 → **设 `_skip_unwind_fatal_error = true`** + `pyodide.canvas.setCanvas2D(canvas)` → 置 `window.sdlReady = true`
  - Python 启动段：**先等 `window.sdlReady`（最多 15 秒）**，再导入 pygame-ce 并运行 `main.py` —— 确保 opt-in 标志早于 `set_mode` 生效；若页面脚本拿不到 `window.pyodide`，则用 `pyodide_js` 兜底完成同样两步（并打印实际生效路径）
  - 顶部补 `import asyncio`
- `web/README.md`：新增「附二：Pyodide 官方对 SDL 的三条硬要求」，逐条给出官方写法与本目录实现方式

**说明**：官方文档明确 SDL 支持「依赖 Emscripten 与 SDL 的未公开行为，未来可能损坏或改变」，属实验特性 —— 这也是本路线需要多次实测迭代的原因

---

### 2026-09-14 · 注册 2D 画布给 Pyodide 的 SDL（浏览器第四次实测反馈）

**背景**：人类第四次实测 —— 包加载✓（`pygame-ce 2.5.7 (SDL 2.32.10, Python 3.14.2)` 横幅已打印），页面里也已有 `<canvas id="canvas">`，但 `main.py` 第 49 行 `pygame.display.set_mode(...)` 仍触发 Pyodide 致命错误：

```
TypeError: Cannot read properties of undefined (reading 'createImageData')
```

**判断**：SDL 不是「自动找页面上叫 canvas 的元素」，而是需要把画布**显式注册**给 Pyodide 的画布 API；未注册时其内部画布为 `undefined`，`set_mode` 便崩在这一行

**修复**
- `web/index.html`：
  - `<body>` 里在 canvas 之后插入一段 `type="module"` 脚本：轮询等待 `window.pyodide` 就绪后调用 **`pyodide.canvas.setCanvas2D(canvas)`** 注册画布（带 `typeof` 存在性判断，API 不存在时不抛错）
  - Python 启动段**也注册一次**（`from js import pyodide` → `pyodide.canvas.setCanvas2D(...)`），以消除「Python 先于页面脚本跑到 `set_mode`」的时序竞争；失败时打印提示并依赖页面脚本兜底
- `web/main.py`：`set_mode((BASE_W, BASE_H), pygame.RESIZABLE)` → **去掉 `RESIZABLE`**（浏览器里画布尺寸由页面决定）

**待人类再测**（改的是页面与 main.py，刷新即可，无需重新构建）：整页强刷 `Ctrl+Shift+R`（上次是致命错误，运行时已失效）

**仍不确定的点**：`pyodide.canvas.setCanvas2D` 这一 API 名称来自记忆，尚未对照官方文档。若本次仍失败，需要人类把 [Pyodide · Using SDL](https://pyodide.org/en/stable/usage/sdl.html) 页面里关于 canvas 的段落贴过来对齐

---

### 2026-09-14 · 补回 canvas（浏览器第三次实测反馈）

**背景**：人类第三次实测 —— **包加载这关过了**（控制台打印 `[启动] pygame-ce 就绪，方式：PyScript config 预加载`，即第一层 `config='{"packages": ["pygame-ce"]}'` 生效），但随后 Pyodide 致命错误：

```
Pyodide has suffered a fatal error …
TypeError: Cannot read properties of undefined (reading 'createImageData')
  File "main.py", line 49 in <module>        ← pygame.display.set_mode((540, 960), pygame.RESIZABLE)
```

**根因**：页面里**没有 `<canvas id="canvas">`**，SDL 拿不到 2D 上下文。（上一轮我按官方示例「没有 canvas 配置」推断可以省略 canvas，是**误判**；官方示例省略它是因为 PyScript 的 PyGame 支持可能自行创建，而在本用法下 SDL 需要显式画布。）

**修复**
- `web/index.html`：`<body>` 里补回 `<canvas id="canvas" width="540" height="960"></canvas>` 及其样式，并加注释说明缺失会导致该致命错误
- `web/README.md`：排错表把「看不到画面」一行改写为实测结论（含完整报错特征与「致命错误需整页刷新」的提示）；§6 更正「不再手写 canvas」的说法

**注意**：该错误是 Pyodide 级致命错误，整个运行时失效，**改完必须整页刷新（Ctrl+Shift+R）**才有意义

**进展**：网页版已连续推进 —— 加载 Pyodide ✓ → 装 pygame-ce ✓（config 预加载）→ 现在卡在显示初始化，属最后一个环节

---

### 2026-09-14 · 修复 pygame-ce 加载方式（浏览器第二次实测反馈）

**背景**：人类第二次实测反馈 `AttributeError("module 'pyodide' has no attribute 'loadPackage'")` —— **`loadPackage` 是 Pyodide 的 JS 侧 API，Python 侧没有**；Python 侧对应的是 `pyodide_js` 模块

**修复**
- `web/index.html`：把「装 pygame-ce」改成**三层加载策略**，并把实际生效的方式打印到控制台，便于后续排错：
  1. **`<script type="py" config='{"packages": ["pygame-ce"]}'>`** —— PyScript 声明式预加载（若生效则后面两层都不会执行）
  2. **`import pyodide_js; await pyodide_js.loadPackage("pygame-ce")`** —— Python 侧的 JS API 镜像
  3. **`import micropip; await micropip.install("pygame-ce")`** —— 从 PyPI / Pyodide 包索引安装
- `web/README.md`：排错表新增该报错一行；文末「浏览器侧依赖与版本」补上三层策略说明与控制台标志（`[启动] pygame-ce 就绪，方式：…`）

**说明**：之所以写三层而不是单一写法，是因为 PyScript/Pyodide 各版本的包加载 API 名称不一致（本轮已连续遇到 `micropip` 未预加载、`pyodide.loadPackage` 不存在两种），而每轮实测都要占用人类一次浏览器验证；该策略会让控制台直接告诉我们哪一层可用

**进展**：网页版已能跑进浏览器并执行到包加载阶段（此前 pygbag 从未越过加载画面）

---

### 2026-09-14 · 修复 PyScript 页面的 micropip 加载（浏览器首次实测反馈）

**背景**：人类在浏览器里首次实测，PyScript 与 Pyodide **已成功加载**（控制台显示 `/lib/python314.zip/`，即该版本内置 Python 3.14），脚本执行到第 4 行时报错：

```
ModuleNotFoundError: No module named 'micropip'
The module 'micropip' is included in the Pyodide distribution, but it is not installed.
```

**修复**
- `web/index.html`：
  - 顶部不再直接 `import micropip`；改为 `import pyodide`
  - 安装 pygame-ce 前先 **`await pyodide.loadPackage("micropip")`**（按报错提示的做法），再 `import micropip` 并 `micropip.install("pygame-ce")`
  - 读入游戏文件后补 `os.makedirs("exports", exist_ok=True)` —— 否则在浏览器里点「回顾页 → 导出 txt」会因目录不存在而报错
- `web/README.md`：排错对照表新增 micropip 一行；文末新增「浏览器侧依赖与版本」（PyScript 版本、Python 3.14、pygame-ce 安装来源、页面启动顺序）

**意义**：这是网页版**第一次真正跑进浏览器**（此前 pygbag 路线从未越过加载阶段），说明 PyScript/Pyodide 路线在环境上是通的

**待人类再测**：同一地址刷新即可（`python -m http.server -d web 8000` → <http://localhost:8000>），观察状态行是否推进到「正在安装 pygame-ce …」→「正在读取游戏文件 …」→「正在启动游戏 …」

---

### 2026-09-14 · 按 PyScript 官方示例对齐网页版（人类提供示例代码）

**变更**
- **采纳人类提供的 PyScript 官方 PyGame 示例写法**（[PyScript · PyGame Support](https://docs.pyscript.net/2026.7.2/user-guide/pygame-ce/)）：官方示例表明 —— ① 浏览器里**不需要任何插件 API 或 canvas 配置**，SDL 显示由 PyScript 自动接管；② 主循环每帧用 `await asyncio.sleep(1 / 60)`；③ 入口用兼容惯用法：

  ```python
  try:
      asyncio.get_running_loop()          # 浏览器（PyScript）已有事件循环
      asyncio.create_task(main())
  except RuntimeError:
      asyncio.run(main())                 # 本地 Python
  ```

- `web/main.py`：每帧 `await asyncio.sleep(0)` → **`await asyncio.sleep(1 / 60)`**；末尾 `asyncio.ensure_future(main())` → **官方 `try / except RuntimeError` 惯用法**（副作用：网页版副本在本地也能 `python web/main.py` 直接跑，便于调试）
- `web/index.html`：**移除手写的 `<canvas id="canvas">`**（官方示例没有 canvas，由 PyScript 自行创建），页面只保留状态行与自举脚本
- `web/README.md`：差异表与本地测试章节同步；§3 新增「先本地跑一遍网页版副本」；排错表 canvas 行改为「画面看不到时手动加 canvas」；§6 由「待确认」改为「**已按官方示例对齐**」并附官方示例代码

**验证**
- `web/main.py` 语法通过；**本地实跑 `python web/main.py`（走 `except RuntimeError: asyncio.run` 分支）连续绘制 5 帧后正常退出**（`LOCAL_OK | 已绘制帧数 = 5`）
- 桌面版 `main.py` 仍未改动

**待人类实测**：浏览器侧仍需你在本地执行 `python -m http.server -d web 8000` → 打开 <http://localhost:8000>

---

### 2026-09-14 · 改用 PyScript / Pyodide 重做网页版（替代 pygbag）

**背景**：pygbag 路线失败后，人类要求改用 Pyodide 系重试，并选定「先试 PyScript」+「不改桌面版 `main.py`」

**调研依据（准则二）**
- [Pyodide · Using SDL](https://pyodide.org/en/0.29.4/_sources/usage/sdl.md)（官方讲浏览器里跑 SDL 类库）
- [Pyodide 包索引 · pygame-ce](https://index.pyodide.org/0.26.2/pygame-ce/)（**官方提供 pygame 的 WASM 包**，API 与 pygame 兼容）
- [PyScript · PyGame Support](https://docs.pyscript.net/2026.7.2/user-guide/pygame-ce/)、[PyGame 插件解析](https://deepwiki.com/pyscript/pyscript/3.2-pygame-plugin)、[Bouncing Ball 官方示例](https://docs.pyscript.net/2026.7.2/example-apps/bouncing-ball/info/)
- 与 pygbag 的关键差别：Pyodide/PyScript 是官方生态、CDN 走 `pyscript.net` + `cdn.jsdelivr.net`（国内通常可访问）、有官方 pygame 支持，而 pygbag 是社区项目且模板自带 bug

**新增（`web/`，与桌面版分离的副本）**
- `web/index.html`：PyScript 页面 —— 加载 `core.js` → `micropip.install("pygame-ce")` → 用 `pyFetch` 把 15 个游戏文件写进浏览器虚拟文件系统 → `runpy` 运行 `main.py`；页面顶部有状态行（依次显示「加载 Pyodide / 安装 pygame-ce / 读取游戏文件 / 启动游戏」），出错时把异常摘要显示在页面上、完整堆栈打印到浏览器控制台
- `web/main.py`：桌面版 `main.py` 的副本，仅三处适配 —— ① 字体统一为随包的 `fonts/zpix.ttf`（浏览器里没有 `C:/Windows/Fonts`）；② 暂不初始化混音器（浏览器音频需用户手势，先保证能启动）；③ 主循环改为 `async def main()` + 每帧 `await asyncio.sleep(0)`，末尾用 `asyncio.ensure_future(main())` 调度（PyScript 已有事件循环，不能用 `asyncio.run`），并补全 `global` 声明
- `web/README.md`：方案对比、与桌面版差异、本地测试方法、排错对照表、静态发布方式、待对齐官方插件的说明

**未改动**：桌面版 `main.py`、`game/`、`data/`、`docs/` 一行未改（人类要求），`git status` 可核验

**验证（本地；浏览器侧因沙箱无 TLS 无法代验）**
- 用 asyncio 模拟 PyScript 的执行方式加载 `web/main.py`：启动成功（初始界面「首页」、字体 `fonts/zpix.ttf`、`click_sound = None`），**连续绘制 5 帧**后按 QUIT 正常退出
- 过程中修掉一个真 bug：循环体被包进函数后，`popup_text` / `chosen` / `points_left` 等**在循环内被赋值的名字必须声明 `global`**，否则抛 `UnboundLocalError`（首次仿真即暴露）
- 页面声明的 15 个游戏文件在 `web/` 中全部存在

**待人类实测**
- 浏览器首次实测需人类执行：`python -m http.server -d web 8000` → 打开 <http://localhost:8000>（**不能双击 index.html**，需 http 服务）
- 若自实现引导不通，需要按官方 PyScript PyGame 插件示例改写 `index.html`

---

### 2026-09-14 · 网页部署路线终止（失败归档）与相关文件清理

**结论：网页版（pygbag / WebAssembly）部署失败，路线终止（人类裁定「不行，仍报错」）**

失败现象与四轮排查记录（备查）：

1. 页面卡在「Loading, please wait ...」
2. **排查①**：网页版沿用 Windows 系统字体路径（`C:/Windows/Fonts/msyh.ttc`、`seguiemj.ttf`），浏览器虚拟文件系统里不存在 → 改为随包分发的 `fonts/zpix.ttf`
3. **排查②**：pygbag 默认 `ume_block: 1`，会先停在「Ready to start ! Please click/touch page」等用户点击，期间页面底色为模板自带的 `#7f7f7f`（表现为灰屏）→ 构建加 `--ume_block 0`
4. **排查③**：控制台报 `PyMain: BrowserFS not found` 并伴随 404 —— pygbag 0.9.3 默认模板把地址拼成 `https://pygame-web.github.io/cdn/0.9.3//browserfs.min.js`（多一个斜杠）→ 构建后自动修补为单斜杠，本地静态自检全部通过
5. **结果：修复后仍然报错** → 判定该路线在课程工期与当前网络条件下不划算，**终止**

**变更（清理）** —— 删除所有为网页部署准备的文件

- `web/`（34 个文件 / 7.6 MB）：网页版源码副本、触屏与手势适配、pygbag 产物（`web.apk` / `web.tar.gz`）、`web/README.md`
- `build_web.ps1`、`deploy_web.ps1`、`check_web.ps1`：打包 / 部署 / 自检脚本
- `.devcontainer/devcontainer.json`：Codespaces 配置
- `requirements.txt`：移除 `pygbag`，只保留 `pygame==2.6.1`
- `.gitignore`：移除 `build/`、`web/build/` 两条，仅保留 Python 缓存规则
- **可恢复性**：`web/` 与 devcontainer 曾提交进仓库（commit `2c88bee`、`5159fb6`），需要时可用 git 历史取回；触屏与手势代码只存在于网页版，随之一并移除
- **遗留**：空目录 `web\audio` 被其它进程占用（疑为仍在 `web\` 目录下的终端）未能删除，关闭占用进程后手动删除即可

**未受影响**：桌面版 `main.py`、`game/`、`data/`、`docs/`、`AGENTS.md`、`archive/`、`test_*.md` 全部未改动；桌面版 `python main.py` 仍照常运行

**下一步**：改为调研「能直接部署 Python 项目的平台」（见后续条目）

---

### 2026-09-14 · 修复灰屏真因：pygbag 模板 browserfs 地址多一个斜杠

**修复**
- **根因**：pygbag 0.9.3 默认模板把 browserfs 的地址拼错 —— `{{cookiecutter.cdn}}` 本身已带结尾斜杠，模板却又加了一个：

  ```html
  <script src="{{cookiecutter.cdn}}pythons.js">        正常
  <script src="{{cookiecutter.cdn}}/browserfs.min.js"> 多一个斜杠
  ```

  生成结果 `https://pygame-web.github.io/cdn/0.9.3//browserfs.min.js` **请求 404** → 浏览器挂载不了 apk → 控制台报
  `PyMain: BrowserFS not found` → 页面一直灰屏
- `build_web.ps1`：新增**构建后修补**步骤 `$html -replace '/cdn/([0-9.]+)//', '/cdn/$1/'`，自动去掉多余斜杠（每次构建都会执行，重新下载模板也有效）
- 同步修补构建缓存里的模板 `web/build/web-cache/*.tmpl`（`{{cookiecutter.cdn}}/browserfs.min.js` → `{{cookiecutter.cdn}}browserfs.min.js`）
- `check_web.ps1`：新增检查项「运行时 URL 无双斜杠」，输出 `[OK] 运行时 URL 无双斜杠（pygbag 模板 bug 已修）` / `[FAIL]` 并打印出错 URL

**变更（文档）**
- `web/README.md`：§8 新增第 8 条「控制台报 `PyMain: BrowserFS not found`」——含原理、手工修补命令；§10 失败对照表新增一行

**验证**
- 重新构建后 `index.html` 的 5 个外部 URL 全部为单斜杠；`browserfs.min.js` 一行现为 `https://pygame-web.github.io/cdn/0.9.3/browserfs.min.js`
- `check_web.ps1` 机械性检查全部通过（含新增的双斜杠检查）

---

### 2026-09-14 · 新增网页版本地检查脚本与检查清单

**新增**
- `check_web.ps1`：**一键跑完网页版的机械性检查**，五组共 20 余项：
  - **A 环境**：Python 版本、`pygbag` 是否安装、`PYTHONUTF8` 是否为 1
  - **B 源码**：`web/` 下 16 项资源齐全性；三个字体路径是否为包内文件（不能是 `C:/Windows/Fonts/...`）；主循环是否 `async def main()`；是否有 `await asyncio.sleep(0)`；有无阻塞调用；语法编译
  - **C 产物**：`index.html` / `web.apk` / `favicon.png`；`ume_block: 0`；页面标题；绝对路径检查；**解包 apk 校验内部资源齐全、apk 内字体路径、以及 apk 内代码与 `web/main.py` 的 MD5 是否一致**（能自动发现「改完代码没重新构建」）
  - **D 启动自测**：用 dummy 视频/音频驱动实际启动 `web/main.py` 并跑通一帧（验证字体、数据、音效可加载）
  - **E 部署前**：`git check-ignore` 确认产物被忽略（提醒必须用 `deploy_web.ps1`）
- `web/README.md` **§10 本地检查的完整步骤**：脚本用法 + 分组说明 + 浏览器手工实测 7 步（Console / Network / 玩一局 / 响应式 / 设备模式触屏 / 真机局域网）+ **常见失败对照表**（灰屏两种、404、CDN pending、产物过期、方框字、GBK 报错）

**实现说明**
- 脚本以**带 UTF-8 BOM** 保存：Windows PowerShell 5.1 读取无 BOM 的 UTF-8 脚本时会按 GBK 解码中文，直接语法报错（本轮踩过一次，已修正）
- 启动自测的临时脚本放在 `%TEMP%`，需 `sys.path.insert(0, os.getcwd())` 才能 `import game.*`（`sys.path[0]` 是脚本所在目录而非工作目录）

**验证**
- 实测输出：机械性检查全部通过，唯一 `[WARN]` 是预期内的「运行时需访问 pygbag CDN」

---

### 2026-09-14 · 修复部署 404（产物被 .gitignore 忽略）+ 新增部署脚本

**问题**
- 浏览器报 `Failed to load resource: ... 404 (File not found)`，线上站点打不开
- **根因**：`web/build/` 在 `.gitignore` 中（第 7 行），因此「把产物复制进 gh-pages 工作区再 `git add -A`」这一做法会让 git **静默忽略整个产物目录** —— 推送出去的 `gh-pages` 分支里没有 `index.html` / `web.apk`，线上自然 404
- 自查命令：`git check-ignore -v web/build/web/web.apk`（有输出即被忽略）

**新增**
- `deploy_web.ps1`：**一键部署到 GitHub Pages** —— 构建（可 `-SkipBuild`）→ 把产物复制到**全新临时仓库**（无 `.gitignore`，从根上避开忽略规则）→ `git add -A` → 打印本次提交文件清单 → 强制推送 `gh-pages`；支持 `-DryRun` 演练

**变更（文档）**
- `web/README.md` 新增 **§9 部署到 GitHub Pages / 静态托管（含 404 坑）**：脚本用法、`git check-ignore` 自查、部署后如何确认线上文件齐全（GitHub 分支页面 / `git ls-tree -r --name-only origin/gh-pages` / F12 Network 看 `web.apk` 是否 200）、Cloudflare Pages 必须拖 `web\build\web` 而不是 `web\`

**验证**
- `deploy_web.ps1 -SkipBuild -DryRun` 演练通过：临时仓库的提交内容恰为 `index.html`、`web.apk`、`web.tar.gz`、`favicon.png` 四个站点文件（分支根目录）

---

### 2026-09-14 · 定位「Loading 之后灰屏」并改为免点击启动

**修复**
- `build_web.ps1` 与 `web/README.md`：构建命令加入 **`--ume_block 0`** 并重新打包
- **根因（pygbag 模板机制，非本项目 bug）**：pygbag 默认 `ume_block: 1`，运行时先等**媒体用户激活**（页面上的「Ready to start ! Please click/touch page」），在点击之前不启动应用；此时页面显示的是模板自带的灰底（`platform.document.body.style.background = "#7f7f7f"`），所以看起来是「Loading 之后灰屏」
- 关掉这一步后应用会直接启动；音频仍遵循浏览器规则（首次点击后才可发声，本游戏本来就只在点击时播音效）

**文档**
- `web/README.md` §8 开头新增「两种灰屏」对照表：① 等你点击（用 `--ume_block 0` 消除）② 点过仍旧灰 = Python 启动异常，需按 7 条排查；并说明灰底是模板自带颜色

**验证**
- 重新构建后 `index.html` 中已是 `ume_block : 0`；apk 内 `assets/main.py` 仍为修复版（`fonts/zpix.ttf`、`async def main()`）
- 产物：`web/build/web/`（`index.html` 12.5 KB、`web.apk` 1.33 MB、`web.tar.gz`、`favicon.png`）

**构建耗时说明**
- 构建日志显示 pygbag 会尝试从 CDN 拉取 `default.tmpl` / `favicon.png`，网络不通时会 `retrying in 5 seconds` 造成构建变慢；有缓存后仍能完成构建

---

### 2026-09-14 · 网页版打包完成 + 清理错误产物

**新增**
- `build_web.ps1`：**一键构建网页版** —— 设好 `PYTHONUTF8=1`、调用 `pygbag --build --app_name re-bit --title "北理工重开模拟器" web`、打印产物清单；加 `-Serve` 参数可顺手起本地服务（含 UTF-8 BOM，兼容 Windows PowerShell 5.1）

**修复（构建阻塞）**
- **pygbag 在中文 Windows 下用 GBK 读取 `main.py`**，遇到中文直接抛 `UnicodeDecodeError: 'gbk' codec can't decode byte 0x80 ...`；构建前必须设 `$env:PYTHONUTF8='1'`（脚本已内置）

**打包产物（已在本地构建并逐项验证）**
- 产物目录：**`web/build/web/`**（即 `<应用目录>/build/web`）
  - `index.html`（12.5 KB，页面标题「北理工重开模拟器」）
  - **`web.apk`**（1.33 MB）—— 内含 `assets/main.py`、`assets/game/`（8 个模块）、`assets/data/`（4 份 JSON）、`assets/save/records.json`、`assets/fonts/zpix.ttf`、`assets/audio/click.ogg`，共 **17 个文件**
  - `web.tar.gz`、`favicon.png`
- **校验**：apk 内 `assets/main.py` 的 `FONT_PATH`/`PIXEL_FONT`/`EMOJI_FONT` 均为 `fonts/zpix.ttf`、主循环为 `async def main()` 且含 `await asyncio.sleep(0)`、代码中无 Windows 字体路径残留；`index.html` 不含绝对路径（子路径部署安全）；本地 HTTP 服务抓取 `index.html` / `web.apk` / `favicon.png` 全部返回 **200**

**清理（错误的打包文件）**
- 删除仓库根目录的 `build/`：那是把**仓库根目录当应用**打的包（入口是桌面版 `main.py`，非 async 主循环 + Windows 字体路径，必然卡在 Loading），而且把 `docs/`、`archive/`、`test_*.md` 全打进了 2.86 MB 的包
- 确认 `.gitignore` 同时忽略 `build/` 与 `web/build/`

**文档修正**
- `web/README.md`：产物路径改回 **`web/build/web/`**、apk 名改为 `web.apk`、新增「Windows 必须开 UTF-8 模式」提示、新增 §8 第 7 条「CDN 卡住」的判定方法与本地化步骤、§4 增加 `build_web.ps1` 用法

**待人类定夺**
- 生成的 `index.html` 运行时会从 `https://pygame-web.github.io/cdn/0.9.3/` 拉取运行时；国内网络下这同样会表现为**卡在「Loading, please wait ...」**。彻底解决需把 CDN 文件本地化并改写 `index.html`（`web/README.md` §8 第 7 条），该步骤必须在**有网环境**执行（本会话的沙箱拿不到 TLS 凭证）

---

### 2026-09-14 · 修复网页版卡在「Loading, please wait ...」

**修复**
- `web/main.py`：字体路径从 **Windows 系统字体**（`C:/Windows/Fonts/msyh.ttc`、`C:/Windows/Fonts/seguiemj.ttf`）改为**随包分发**的 `fonts/zpix.ttf`
- **根因**：浏览器（pygbag / WebAssembly）运行在虚拟文件系统里，**没有 `C:/Windows/Fonts`**；原代码在**第一帧渲染**时调用 `pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 19)` 抛 `FileNotFoundError`，pygbag 的启动画面便永远停在「Loading, please wait ...」

**新增**
- `web/README.md` §8「卡在 Loading, please wait ... 怎么办」：按顺序的 6 条排查 —— ① F12 Console / `pygbag web` 终端看 traceback ② 构建产物是否齐全（`main.py` / `game/` / `data/` / `save/` / `fonts/` / `audio/`）③ 只能用随包字体 ④ 音效嫌疑 ⑤ GitHub Pages 无法设置 COOP/COEP 头的平台限制 ⑥ 缺字形符号（✌）

**变更（修正此前文档与忽略规则的错误）**
- **构建产物路径纠正**：实测 `pygbag --build web` 的输出在**仓库根目录的 `build/web/`**（不是 `web/build/web/`），主要文件为 `index.html` + **`re-bit.apk` / `re-bit.tar.gz`（游戏本体被打包进 apk）** + `favicon.png`；`web/README.md` 中 4 处路径已改正，并补充「改了代码必须重新构建」的提醒
- `.gitignore`：改为忽略真正的构建目录 `build/`（原先写的是 `web/build/`，导致 `build/` 出现在待提交列表）

**验证**
- `web/main.py` 语法检查通过；用合成 QUIT 事件跑通一帧，字体从 `fonts/zpix.ttf` 正常加载
- 桌面版 `main.py` **未改动**，仍使用微软雅黑

**影响与待确认**
- 网页版正文/标题**统一为像素字体 Zpix**（Zpix 为 OFL 可再分发字体，含中文）—— 视觉风格随之变为像素风；若要更接近微软雅黑，需引入可再分发的 CJK 字体（如思源黑体 / Noto Sans SC），属新增资源，待人类定夺
- 「特立✌」的 `✌` 在 Zpix 中无字形，浏览器里会显示为方框（不影响运行）

---

### 2026-09-14 · Codespaces 启动优化

**变更**
- `.devcontainer/devcontainer.json`
  - `postCreateCommand` → **`onCreateCommand`**：依赖安装改到会被**预构建**打进快照的生命周期钩子（`postCreateCommand` 在快照之后、分配实例时才跑，等于每次新建都要重装 pygame + pygbag）
  - **移除** `customizations.vscode.extensions`：不再自动安装 `ms-python.python`（约 100 MB 下载）
  - `portsAttributes.8000.onAutoForward`：`openPreview` → **`notify`**（启动时不再自动加载预览页）
- `web/README.md`：新增 **§7「Codespaces 启动太慢怎么办」** —— 按收益排序的 7 条措施（配置 Prebuild、延长闲置超时、依赖钩子、扩展、端口预览、机器类型、网络）+ **静态托管替代方案**（`pygbag --build web` / `--archive web` 发布到 GitHub Pages 等）

**原因**
- 实测本仓库 **90 个文件 / 9.7 MB**（其中 `fonts/zpix.ttf` 4.7 MB × 2 份，`.git` 2.16 MB）——启动慢**不来自仓库体积**，而来自：容器镜像首次拉取（约 1 GB）、每次新建都重装依赖、VS Code 扩展下载、以及**没有配置预构建**
- 参考：[GitHub Codespaces prebuilds](https://docs.github.com/en/codespaces/prebuilding-your-codespaces/about-github-codespaces-prebuilds)、[devcontainer 生命周期规范](https://containers.dev/implementors/json_reference/)、[如何缩短 Codespaces 启动时间（社区讨论）](https://github.com/orgs/community/discussions/207723)

**未做（需人类操作或确认后实施）**
- **Prebuild 预构建、闲置超时、机器类型**属于仓库 Settings 项，本地无 `gh` 也无网络，代理改不了，步骤已写入 `web/README.md` §7
- **「Actions 构建 WASM + 发布 GitHub Pages」**需要新增 `.github/workflows/*`（GitHub Actions 属新增工具链，按准则四待人类批准）

---

### 2026-09-14 · 音效格式改为 OGG（Vorbis）

**变更**
- `audio/click.wav` → **`audio/click.ogg`**：Vorbis / 22050 Hz / 单声道 / 60 ms / 3912 字节（用 ffmpeg `-c:a libvorbis -q:a 6` 转出）
- `web/audio/click.ogg`：网页版同步替换，并与根目录那份**字节一致**（SHA256 相同，原先两份是各自转码、内容不同）
- `main.py` 第 51 行、`web/main.py` 第 57 行：`pygame.mixer.Sound("audio/click.ogg")`
- 文档引用同步：`docs/02-游戏设计.md`（§12 已做项）、`docs/03-项目架构设计.md`（目录树）、`docs/05-页面设计.md`（交互汇总·音效）、`README.md`（文件结构）

**原因**
- WAV 在浏览器（pygbag / WebAssembly）与部分移动环境下的解码播放兼容性不如 Ogg Vorbis；OGG 体积更小、跨平台播放更稳 —— 这也是本轮做移动端 / 网页版适配后需要换格式的直接原因

**修复（原改动曾误伤历史记录与只读快照）**
- **恢复只读快照** `archive/2026-09-14/`：一次全局替换波及了快照里的 `CHANGELOG.md`、`docs/03`、`docs/05` 三个文件，已用 `git checkout -- archive` 复原为冻结状态（快照按 `归档说明.md` 约定不再更新）
- **还原 `CHANGELOG.md` 的历史条目**：2026-09-13 那条记录的当轮事实是 `click.wav`，不应被回溯改写；本轮改动改为**新增本条目**（准则九），而不是改写历史

**验证**
- OGG 流信息：`vorbis, 22050 Hz, mono`，时长 0.060 秒；`volumedetect` mean −11.5 dB / max −2.2 dB（确有声音，不是静音）
- `pygame.mixer.Sound("audio/click.ogg")` 加载与播放调用成功
- 桌面版 `python main.py`、网页版 `web/main.py` 启动均正常
- 两份副本 SHA256 一致

---

### 2026-09-14 · 移动端适配与 Codespaces 分享

**新增（网页版）** —— `web/`
- `web/main.py`：根目录 `main.py` 的**独立副本**（877 行），额外做三件事：① 主循环改为 `async def main()` + 每帧 `await asyncio.sleep(0)`（pygbag 要求让出控制权）；② 触屏适配；③ 点击逻辑抽成 `handle_click()`，鼠标左键与手指轻触共用
- **触屏与手势**：`FINGERDOWN/FINGERUP` 轻触（位移 < 40 基准像素）等价左键点击，且 `hit()` 在手指输入时把命中区**向外放大 12 基准像素**；上/下滑滚动（游戏页滚月度日志、其余页滚列表）；左滑在游戏页推进一个月、右滑打开暂停页；在暂停/结局/成就/回顾/回顾详情右滑返回
- `web/game/`、`web/data/`、`web/fonts/`、`web/audio/`：资源副本（网页版随包分发，从空存档开始）
- `web/save/records.json`：空存档（个人记录不随分享包外泄）
- `web/README.md`：网页版说明、手势表、本地运行、pygbag 打包、**Codespaces 分享步骤**、浏览器限制（无持久存档、音效需先点击）与副本同步提醒

**新增（Codespaces 与依赖声明）**
- `.devcontainer/devcontainer.json`：Python 3.12 镜像 + `pip install -r requirements.txt` + 转发 **8000** 端口并设为 **Public**（打开即预览）
- `requirements.txt`：`pygame==2.6.1`（桌面版唯一依赖）+ `pygbag`（仅打包网页版时需要）
- `.gitignore`：忽略 `__pycache__/`、`*.pyc`、`web/build/`

**原因**
- 手机端无法运行 pygame 桌面窗口，浏览器是唯一可行的移动端入口；pygbag 是 pygame 官方的 WebAssembly 打包方案（[pygame-web/pygbag](https://github.com/pygame-web/pygbag)）
- Codespaces 转发端口设为 Public 后即可得到一个手机也能打开的试玩链接（[端口转发文档](https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace)）

**验证**
- `web/main.py` 语法检查通过；用合成事件（`FINGERDOWN/FINGERUP`、`MOUSEBUTTONDOWN`）跑通全流程：首页轻触 → 开局页上滑 → 「开  始」→ 游戏页左滑推进一个月 → 右滑暂停 → 鼠标点「继续游戏」→ 退出
- 命中区放大专项验证：鼠标点按钮上方 8px **不**触发；手指点同一位置**触发**；手指点上方 20px 不触发
- 根目录桌面版 `main.py` **未改动**，冒烟测试正常启动

**未改动**
- `docs/` 下所有设计文档与 `AGENTS.md` 本轮均未修改（按人类要求）
- 上一轮记录的待确认问题（`docs/talent.txt` / `color.txt` 缺失、`main.py` 死代码与残留注释、`exports/` 占位文件、`todo.md` 三处不符）**一律保留未处理**

**待人类确认**
- pygbag 属新增依赖：按准则四需更新 `AGENTS.md` 准则四的技术栈表（本文件由人类维护，代理未擅自修改），建议在「第三方依赖」行注明「pygame（运行）+ pygbag（仅网页版打包）」

---

### 2026-09-14 · 全量文档核对与同步（对齐当前实现）

**变更（文档同步，共 9 份）**
- `docs/05-页面设计.md`：按与 `main.py` 的逐条审计修正 20+ 处 —— 界面清单 7 → **8**（补「回顾详情页」）；字号体系（大标题 48→**64**、标题 22–30、正文 15–22、辅助 13–17）；次文字 `#6B7280`→`#545C6A`；背景渐变止统一 `#C6DED0`；卡片色条圆角 2 并补天赋等级配色；**删除代码未实现的 3 项**（游戏页下划线、暂停标题下划线、方向键滚动）；§2.4 通用规格改为与 §5/§6 一致（按钮 64/36/44、卡片间距 54、行高 32/29/26/34、内缩 20/14/0）；成就列表 y=90→**105**、示例 `3 / 20`→`3 / 15`；修正 4 处按钮文案（含全角空格）；**补写代码里有但文档没写的元素**（游戏页右上角性别、回顾页空状态与列表性别、回顾详情页标题与「返  回」按钮、天赋卡条件显示、开局「开  始」的动作与自动计时重置、未命中按钮也播音效、回顾页可滚动）；修复表格里字面量 `` `n `` 造成的错行；§12 已裁定事项同步（#9 成就已完成、#13 日志最新在顶端、#16 游戏页下划线取消、#18 大标题 64，新增 #30~#32）
- `docs/04-程序设计.md`：玩家字段补 `gender` / `org` / `flags` / `term_bonus` / `cet4` / `cet6` / `check_bonus`；事件字段补 `need_max` / `visit` / `score_field`，`check` 补「只出分」形式；结局字段补 `kind` / `weight` / `school` / `need` / `need_max` / `rank_max`；成就类型三类 → **七类**；存档补 `provinces`；月度日志改为「**最新在顶端**」；流程图「选 3 个天赋」→「最多选 2 个」；函数表补 `draw_talents` / `collect_forces` / `collect_rewind` / `apply_forces` / `roll_check` / `save_records`；§2.12 装饰元素改为实际实现（去掉顶部装饰条与标题短线、渐变止改 `#C6DED0`）
- `docs/03-项目架构设计.md`：准则一~八 → **一~九**；目录树补 `ending.md`、`archive/`、测试报告；清单条数改为 event-list **181** / achievement-list **15**；`records.json` 说明补 `provinces`；成就类型改六类；「根目录正式代码 待编写」→ **已完成（1288 行）**
- `docs/02-游戏设计.md`：天赋 18 → **26 条**；事件 113 条 → **181 条**；补判定的三种形式；保底事件说明；成就三类 → **六类 + 开局**并补 15 条；§12 边界「不做音效」→ 改为「按钮点击音效已做」；§11 补暂停覆盖层与回顾详情；§13 待确认同步
- `docs/01-可行性分析.md`：文案文件三份 → **四份**；甘特图状态更新（P2 / P3 已完成、P4 进行中）；代码行数改实测（原型 430 / 正式版 1288）；运行方式改为根目录 `python main.py`
- `docs/talent.md`：已实现 21 → **26 条**；`进编制` 标签标注「当前无事件（已知缺口）」；删除「事件池仍是占位文案」的过期说明
- `docs/event.md`：状态改为「已实现，181 条」；`tags` 说明同步；「两种判定」→ **三种**；抽取流程把 `chance` 移到候选筛选阶段并说明保底事件保证不空；§8「待补」→「内容规模」
- `docs/achievement-list.md`：类型补「开局」（共七类）；「保研上岸」条件改为「保研本校 或 保研外校」
- `README.md`：运行方式改为根目录 `python main.py`；天赋 5 选 3 → **最多选 2**；结局按钮改为「回顾本局 / 返回首页 / 再来一局」；文件结构改为正式代码 + 数据 + 存档 + 文档 + 原型；改文案路径改为 `data/*.json` 并重写事件字段表；「当前状态」由「设计阶段、代码为原型」改为「**正式版已完成**」并列出内容规模

**核对方法与结果**
- 用脚本从 `data/*.json` 与 `game/*.py` 提取事实基线（事件 181、天赋 26、成就 15、结局 11、专业 20、书院 4、时段 7、名次公式常量、院校 16 所）逐条比对 14 份文档
- `docs/05-页面设计.md` 由子代理与 `main.py`（785 行）逐行审计：**按钮坐标 100% 一致**，偏差集中在字号体系、§2.4 通用规格自相矛盾、未实现的视觉细节、未写进文档的可见元素
- 生成类清单（talent-list / event-list / ending-list / achievement-list）与数据逐项核对，无缺失
- 最终复查：旧判定字样、旧条数、字面量 `` `n `` 均已清零

**发现但未处理（按准则六只记录，等人类定夺）**
- `docs/talent.md` 引用的 **`docs/talent.txt`** 与 `docs/05-页面设计.md` 引用的 **`color.txt`** 在仓库中都已不存在（疑被删除）—— 需决定补回文件还是改掉引用
- `main.py:39` 的 `TIER_NAMES`（稀有 / 史诗 / 传说）已无人使用（开局页只用颜色），属死代码；`main.py:165` docstring 仍写「+ 顶部装饰条」；`draw_button` 的 `disabled` 参数全文无调用
- `exports/` 里还留着早期带「【占位】」的导出文件（2026-09-09 / 09-10 / 09-13）
- `todo.md` 第 10 项要求的「RM机甲大师赛（追梦机器人队专享）」在事件池中不存在；第 6 项「院校层级至少 985」与后来加入的国科大（非 985）冲突；第 12.4 项「特立奖学金每学年限一次」实际实现为特殊事件（每局限一次）

---

### 2026-09-14 · 文档归档与同步修订

**新增（归档）**
- `archive/2026-09-14/`：结局系统重构**之前**的全部文档快照，共 22 个文件 —— `docs/` 14 份 + `AGENTS.md` / `README.md` / `CHANGELOG.md` / `todo.md` / `test_1.md`~`test_5.md` + `归档说明.md`
- 快照只读，后续修改一律改仓库中对应文件

**变更（文档同步，使文档与新的结局判定一致）**
- `docs/02-游戏设计.md`：§7 结局系统改为新判定（五步流程、保研的平均综测排名门槛、保外校仅限高位院校、边际效用与随机权重）；§2 玩法流程第 5 步与 §13 待确认事项（各结局权重）同步
- `docs/04-程序设计.md`：§2.4 结局判定改写为五步流程 + 竞争权重公式 + 平均综测排名换算；流程图（`结局判定 → 定院校 → 成就判定`）、模块职责表、玩家数据结构（新增 `rank` / `rank_pcts`，`tags` 说明）同步
- `docs/03-项目架构设计.md`：`endings.py` 模块说明与数据流改为「结局判定、升学院校、综测百分位」
- `docs/01-可行性分析.md`、`docs/event.md`：措辞「结局算分」→「结局判定」
- `README.md`：结局规则改写为新判定；`docs/` 文件结构行补充内容文档与清单
- `AGENTS.md` §0：文档清单补充 `docs/ending.md` / `ending-list.md` / `achievement-list.md`、`test_1.md`~`test_5.md`、`archive/`（**人类已批准本次 §0 修订**；§0 以外未改动，变更记录表待人类自行追加）
- `test_3.md` / `test_4.md` / `test_5.md`：各加一行「归档说明」指向新文档与快照，**历史数据一律不改**

**发现但未处理（按准则六只记录，等人类定夺）**
- `docs/02-游戏设计.md` §6 写「事件主题清单：20 类 / 113 条」，实际为 **181 条**
- `docs/02-游戏设计.md` §5 写「天赋当前共 18 条」，`docs/talent.md` 写 **26 条**，两处不一致
- `README.md` 写「天赋：随机抽 5 个选 3 个」，实际规则是**最多选 2 个**
- `README.md` 文件结构写「AGENTS.md　AI 协作准则（准则一~八）」，现为**准则一~九**

---

### 2026-09-14 · 结局系统重构（硬门槛 + 加权竞争）

**变更（数据）** —— `data/endings.json`
- 每条结局新增判定字段：`kind`（升学 / 就业 / 学业 / 兜底）、`weight`（竞争权重）、`school`（院校名单范围）、`need`（属性下限或标签次数下限）、`need_max`（属性上限）、`rank_max`（平均综测百分位上限）
- 按人类要求设定硬门槛：保研本校 = `保研`≥1 且 平均排名 ≤40%；**保研外校 = `保研`≥1 且 平均排名 ≤5%，且院校仅限「高于北理层级」**；出国留学 = 家境 >7；考研类 = `图书馆`≥2；进入大厂 = `进大厂`≥1；创业 = 家境 ≥6；进入编制 = `学生组织`≥1；援建乡村 = `学生组织`≥1 且 家境 ≤6；延毕 = 智力 <5.4
- 竞争权重按目标分布校准：保研外校 4.5、保研本校 4.0、考研外校 0.6、考研本校 1.7、出国留学 0.4、进入大厂 0.27、创业 0.5、进入编制 0.4、援建乡村 4.0
- 院校表新增 **中国科学院大学（能力分 ≥115，人类确认）**，并为 16 所院校标记「是否高于北理层级」（高位 8 所：清华 / 北大 / 国科大 / 上交 / 复旦 / 浙大 / 北航 / 哈工大）

**变更（逻辑）** —— `game/endings.py` 重写
- 判定改为五步：① 延毕优先 → ② 硬门槛过滤 → ③ 升学类内部按竞争权重抽一个 → ④ 升学胜者与就业类按竞争权重抽一个 → ⑤ 都不满足则「待业」兜底
- **边际效用**：影响因子贡献改为 `√(属性值或标签次数) × 权重`（收益递减），替代原来的线性加权取最高分
- **随机权重**：竞争权重 = `weight × 影响因子得分 × random(0.7, 1.3)`，并设 0.01 下限（援建乡村的家境权重为负，防止抽签参数非法）
- 新增 `rank_percentile(score)`：`百分位 = 100 − 100 × (得分 − 28) / 54`（夹 1~100）、`average_rank(player)`：6 次综测百分位均值
- `judge_school(player, high_only)`：保研外校只在高位名单取档，考研外校用全部 16 所

**变更（流程）** —— `main.py`、`game/player.py`
- 综测名次改用新公式并记录 `player["rank_pcts"]`（6 次百分位），供保研门槛使用；时间倒流（败者食尘）时清空
- 结局院校调用改为 `judge_school(player, ending.get("school") == "高位")`
- **名次公式重校准的原因**：旧公式 `(得分 − 20) / 120` 把平均百分位压在 34% ~ 89%（均值 66%），「≤5%」在 1000 局中出现 **0 次**、「≤40%」仅 2.3% —— 保研门槛完全不可达；重校准后 ≤5% 约 5%、≤40% 约 43%

**新增文档**
- `docs/ending.md`：**结局系统设计文档**（结局构成、平均综测排名、硬门槛表、竞争与随机权重、升学院校、目标分布与实际分布、与旧判定的差异、数据字段说明）
- `docs/ending-list.md`：按新数据结构重新生成

**验证（3000 局，种子 20260919）**
| 结局 | 目标 | 实际 |
| --- | --- | --- |
| 保研外校 | 2% | 2.0% |
| 出国留学 | 3% | 3.3% |
| 保研本校 | 20% | 22.3% |
| 考研外校 | 5% | 5.6% |
| 考研本校 | 20% | 20.0% |
| 进入大厂 | 10% | 11.1% |
| 创业 | 10% | 12.4% |
| 进入编制 | 10% | 12.0% |
| 援建乡村 | 5% | 6.4% |
| 延毕 | 5% | 4.8% |
| 待业 | 10% | **0.0%** |

- **可命中结局从 2 种提升到 10 种**，且每条结局的实际占比与目标偏差 ≤2.4 个百分点
- 保研外校的院校 100% 落在高位名单内（国科大 21、清华 20、复旦 6、北航 5、北大 4、浙大 4）
- `python main.py` 冒烟测试正常启动

**已知偏差（待人类定夺，未实施）**
- **待业 0%**：它是纯兜底，但就业类门槛很宽（`进大厂` 97%、`进入编制` 100%），没有任何一局能让全部门槛同时落空。差额按人类裁定并入了就业类。若要待业达到 10%，需二选一：给待业一个真实门槛，或收紧就业类门槛
- **待确认（按准则六未擅自修改）**：`docs/02-游戏设计.md`（第 26 行、第 102~104 行）与 `docs/04-程序设计.md` 仍写着旧判定「按属性与经历算分，取最高分」，与新判定不一致，是否同步修订由人类定夺

---

### 2026-09-14 · 结局命中分析（test_5.md）

**新增**
- `test_5.md`：**测试报告 5 · 结局命中分析**（1000 局，种子 `20260916`）—— 含 11 条结局的得分分布与命中率、支配关系（代数证明 + 实测）、得分构成、逐条归因、两处数据缺口、门槛模拟

**本轮无代码与数据改动**（纯只读分析；§7 的门槛为分析用假设模拟，未写入 `data/endings.json`）

**核心发现**
- **11 条结局实际只有 2 条在竞争**（出国留学 56.6% / 保研外校 43.4%），同分并列仅 0.2%；第二名与第三名差 **10.8 分**，是断层而非接近
- **5 条被代数恒等式锁死**：
  - 保研外校 − 保研本校 = `智力 + 保研` ≥ 0；考研外校 − 考研本校 = `0.5×智力` ≥ 0 → 同门槛时本校两条永远不可能夺冠
  - 出国留学 − 待业 = `3×家境 + 3×智力 + 0.5×体质` ≥ 0；待业 − 延毕 = `1.5×智力 + 0.5×体质` ≥ 0 → 待业/延毕结构性不可达
  - 出国留学 − 援建乡村 = `4×家境 + 智力 − 2×学生组织` > 0（学生组织单局上限仅 3）
- **两处数据缺口**：① `进编制` 标签在 181 条事件中**一条都没有**，导致进入编制（×2）与创业（×−1）的该权重项恒为 0；② `学生组织` 单局最多只能拿 3 次（16 条加入组织事件带 `flags_forbid`），把援建乡村/创业/进入编制的标签项封顶在 +4.5 ~ +6
- **门槛模拟**：按 `test_3.md` §5.3 的 `require` 过滤后，命中种类 2 种 → **6 种**（v1）；若把校/外校改成互斥的属性区间，可到 **8 种**（v2）；两种方案下援建乡村、延毕仍为 0%

**建议的下一轮顺序（待人类定夺，未实施）**
1. 补两处标签供给（`进编制` 事件、`学生组织` 来源）—— 数据层，风险低
2. 加 `require` 门槛 v2（校/外校门槛互斥）—— 解决「结局由属性决定」
3. 给延毕独立的机制（它被无门槛的待业恒久压制）

---

### 2026-09-14 · 全量测试（test_4.md）

**新增**
- `test_4.md`：**测试报告 4 · 全量测试（事件供给再平衡后复测）** —— 种子 `20260913`、100 局（与 `test_2` 同种子，逐项对照），含 8 个学期末属性、6 次综测排名、结局与院校、竞赛、组织、成就、事件与旅游、改前改后对照总表，以及 7 条问题分析

**本轮无代码与数据改动**（纯测试与分析）

**测试结论（改前 → 改后）**
- ✅ **属性失衡已解决**：智力 +4.04 → **+1.75**，体质 **−1.00 → +0.90**，四属性净变化收敛到 +0.90 ~ +1.75，同向增长
- ✅ **升学院校不再顶格**：升学能力分均值 115.4 → **89.8**，清华占比 26% → **2%**（反向问题：顶尖档几乎不可达）
- ❌ **结局仍为 2 种**：分布 77/23 → 53/47，冠军与亚军分差 9.1 → 5.7，但第三名与第二名差 10.7 分，属性项仍是标签项的 3 ~ 4 倍
- ❌ **下游门槛整体偏严**（本轮新暴露的核心问题）：名次公式、竞赛档位线与门槛、属性类成就阈值、院校档位线都按改前的高智力水平标定，智力下移后连带变严 —— 综测前 5 名 21 → **3 次**、竞赛 1.86 → **1.33 次/局**、竞赛一等奖 15.6% → **5.3%**、学霸成就 62% → **12%**、平均成就解锁 3.5 → **2.3 / 15**
- ✅ **无事件回合 0 / 4811**、跨局旅游 **33 / 33** 保持有效

**建议的下一轮顺序（待人类定夺，未实施）**
1. 校准下游门槛（名次公式分母 120 → 80 等、竞赛门槛与档位线、学霸阈值、院校档位线）—— 参数级改动，风险低
2. 再做结局硬门槛 + `attr_weights` / `tag_weights` 拆分（`test_3.md` §5.3）

---

### 2026-09-14 · 事件供给再平衡（属性失衡修复）

**变更（数据）** —— `data/events.json`，按 `test_3.md` §6.1「方案 A」实施，人类选定「只做事件供给再平衡」
- **下调 23 条高频事件的智力数值**：期末池 通宵自习室 0.5→0.15、认真复习 0.4→0.2、图书馆难抢 0.3→0.1、综教交卷 0.3→0.1、呼噜声 0.2→0.1；寒假/暑假 实验室、图书馆、竞赛集训营 0.5/0.4→0.15；常规 理教靠窗、数模校赛、讲座、实验室打杂、点名 0.3~0.4→0.1、早八 0.2→0.1；实习/答辩 0.4→0.15；负向同步减半（翘课 −0.3→−0.15、点名没答 −0.2→−0.1）
- **竞赛判定档次智力收益减半**：8 条竞赛 × 4 档（0.6→0.3、0.4→0.2、0.3→0.15、0.2→0.1）
- **组织加入事件颜值 +0.2 → +0.1**（16 条，§6.1 原定动作）
- **软化 3 处体质流失**：通宵自习室 −0.4→−0.2、呼噜声 −0.2→−0.1、实习加班 −0.5→−0.3
- **新增 17 条事件**（164 → **181** 条）
  - 体质正向 10 条：体育馆办卡、体测八百米、十一点睡、晨跑三圈、游泳馆、戒夜宵、期末早睡、考完聚餐、实习散步、军训拉伸
  - 家境正向 7 条：快递驿站兼职、课题劳务费、外包小单、学习进步奖学金、勤工助学岗位（特殊，每局限一次）、实习工资、暑假兼职

**变更（文档）**
- `docs/event-list.md`：按新数据重新生成（181 条；常规 96、特殊时段 85；特殊 81、基础 100）
- `test_3.md`：新增 §8「实施结果（方案 A 已落地并复测）」，含改动清单与前后对比数据

**原因**
- 改前实测（300 局）：智力 **+5.18** / 体质 **−1.06** / 颜值 +2.18 / 家境 +0.65 —— 智力虚高、体质倒扣，导致开局属性分配几乎失去意义
- 根因是事件池供给失衡，且智力集中于「小事件池被反复抽中」的期末时段（仅 8 条候选，每局抽 ~8 次）

**验证**
- 改后（各 300 局，种子 20260914 / 20260915）：智力 **+2.01/+2.01**、体质 **+1.12/+1.15**、颜值 +1.88/+1.89、家境 +1.55/+1.49 —— 四属性收敛到 +1.1 ~ +2.0，**体质转正**，换种子结果稳定
- 静态供给：智力 14.2→**8.1**、体质 −0.7→**+3.3**、颜值 9.8→**8.2**、家境 2.8→**5.9**，全部落入 §6.1 的 +3 ~ +8 目标区间
- 17 条新事件全部可被抽中（合计 6.95 次/局）
- 副作用：升学院校不再顶格（清华 20.7%→0.3%，分布拉开到 13 所）；结局分布由 89.3/10.7 改善为 59.7/40.3，但**结局种类仍为 2 种**（硬门槛属本轮范围之外，未实施）

---

### 2026-09-13 · 属性与结局归因分析（test_3.md）

**新增**
- `test_3.md`：**测试报告 3 · 属性变化与结局的归因分析及修改方案**，含
  - 属性归因表（开局分配 / 天赋 / 常规事件 / 竞赛判定 / 各时段 → 期末终值）
  - 事件池净供给分析、贡献最大的 12 条事件
  - 每个结局的得分构成（属性部分 vs 标签部分）与夺冠优势幅度
  - **6 组权重缩放的敏感性实验** + 结局硬门槛方案
  - 属性供给平衡方案与目标配比

**关键发现**
- **属性失衡的量化根因**：事件池净供给 智力 **+23.2** / 颜值 +10.2 / 家境 +1.3 / 体质 **−0.7**；运行 100 局后流入流出比 智力 10.5:1、颜值 18.8:1、家境 22:1、体质仅 2.7:1
- **结局集中的三个根因**：①属性与标签权重同表同量级（属性 30~60 vs 标签 0~10）；②智力膨胀传导；③4 条升学结局权重结构高度相似；**④缺少硬门槛**（最直接原因）
- **敏感性实验结论**：把属性权重缩放到 ×0.05、标签放大到 ×3，结局种类也只从 **2 种** 涨到 **3 种** —— **单纯调权重解决不了结局集中**

**提出的修改方案（待人类定夺，未实施）**
- 结局：加 `require` **硬门槛**（如保研需 `保研` 标签且智力 ≥ 8、延毕需智力 ≤ 5、待业无门槛兜底），并拆分 `attr_weights` / `tag_weights`
- 属性：按**净供给**对齐（降智力向事件权重、补家境 6~8 条与体质 8~10 条正向事件），目标四属性净供给落在 +3 ~ +8 且体质不再为负

---
### 2026-09-13 · 100 局全量测试（test_2.md）

**新增**
- `test_2.md`：**测试报告 2 · 100 局全量测试**（随机种子 `20260913`），含测试方法、8 个学期末属性、6 次综测排名、结局与院校、竞赛、组织、成就、事件与旅游统计，以及 7 条问题分析

**修复**
- `game/achievements.py`：**结局类成就支持「结局名列表」** —— 原先「保研上岸」只认「保研本校」一个结局，导致达成「保研外校」时不解锁；现 `value` 可为结局名或列表

**测试暴露的主要问题**
1. **属性严重失衡**：智力 5.35 → 9.39（+4.04），体质 5.25 → 4.25（−1.00）。事件池中**智力正向 92 条 / 负向 6 条**，而体质只有 18/20 —— 智力正向事件数量碾压其他属性
2. **升学院校普遍顶格**：升学 77 局中清华占 20 局（26%）；升学能力分均值 **115.4**（最高档门槛 130）
3. **结局高度集中**：100 局只触发 **2 种**结局（保研外校 77 / 出国留学 23），**11 条里 9 条不可达**。根因是属性量级（30~40）把标签权重（1~3）完全盖过
4. **成就可达性差**：单局 100 局从未解锁「特立奖学金！」「军工强校」（后者实际概率仅约 2%）；解锁率 ≤5% 的有 ta大帝！/ ye天帝！/ 不怕兄弟苦
5. **竞赛与旅游被摊薄**：平均每局参赛 1.86 次，**33 局完全没参赛**；单局旅游 9.3 个省份
6. **排名缺乏波动**：大三下百分位均值 47.6%，范围 1.9%~100%，但基本由智力线性锁定
7. **无事件回合 0 / 4800** —— 第 11 项的保底机制有效 ✅

**验证**
- 100 局累计旅游省份 **33 / 33**，证明「走遍全国」跨局可达

---
### 2026-09-13 · 补齐事件对应成就（清单遗漏修正）

**修复**
- **补齐第 12 项中遗漏的 8 个事件类成就**：ta大帝！、ye天帝！、新宿舍、特立奖学金！、军工强校、不怕兄弟苦、吃一堑、热带风味；成就总数 **7 → 15**
- **成就判定改用「最终显示文案」**：原先用事件父文案判定，导致带判定的成就（如「吃一堑」只在被诈骗的失败分支才该解锁）无法正确触发；现在 `apply_event` 返回判定结果文案，`main.py` 用它做成就匹配
- **修正诈骗事件文案结构**：父文案由「你被电信诈骗了…」改为诱因描述「你接到一个陌生电话…」，成功 / 失败分支各自给出结果文案

**新增**
- **同性表白事件 2 条**（男生 / 女生版），要求 `flags_need: ["男"/"女", "彩虹"]` —— 补上「彩虹之下」天赋缺失的实现（原先该天赋只设状态、没有可用事件）

**验证**
- 诈骗事件 300 次：**88 次触发「吃一堑」**（智力 3 时成功率 67%，未识破约占 1/3）✅
- 同性表白：无「彩虹」不可触发，有「彩虹」可触发 ✅
- 事件类成就 **9 条全部能在事件池中找到对应文案**（父文案或判定结果文案）✅

**数据量**
- 事件 **162 → 164 条**、成就 **7 → 15 条**；`docs/event-list.md`、`docs/achievement-list.md` 已重新生成

---
### 2026-09-13 · todo 第 12–15 项（完成）

**新增**
- **第 12 项 · 10 条特殊事件**：ztagg / yjcgg 粉丝团（需科协，成就「ta大帝！/ ye天帝！」）、搬到勤园、特立奖学金（需排名前 5）、助学贷款（家境 < 3）、军训坦克（8%，成就「军工强校」）、舍友 Rank1、电信诈骗（智力判定，成就「吃一堑」）、热带风味冰红茶（期末 12%，加排名，成就「热带风味」）、四级 / 六级出分
- **第 13 项 · 扩充事件**：新增 19 条军训 / 寒暑假 / 校园 / 实习事件，覆盖**特立图书馆、综教、理教、文萃楼、文博中心、北湖（鹅 / 羊驼 / 孔雀）、东 / 北 / 南食堂三楼**等校园地标
- **第 14 项 · 5 个新天赋**：生而为男 / 生而为女（指定性别）、彩虹之下（同性表白）、花言巧语（表白判定 +25）、警惕心（免疫诈骗）；天赋总数 **21 → 26**
- **第 15 项 · 4 个新成就**：北理新生（开局）、Rank1（综测第一）、歪果仁（六级 > 600）、走遍全国（跨局累计 33 个省级行政区）
- **33 条旅游事件**（寒假 / 暑假，覆盖全部省级行政区）

**变更**
- 事件 schema 扩展：`need_max`（属性上限条件）、`visit`（记录旅游省份）、`score_field`（记录分数）；`check` 新增 **只出分** 形式 `{score: {base, attrs, roll, max}}`
- 天赋 schema 扩展：`gender`（指定性别）、`check_bonus`（按事件标签加判定分）、`flags_set`（天赋直接给状态）
- `game/player.py`：新增 `rank` / `cet4` / `cet6` / `check_bonus` 字段；`apply_talents` 处理性别、状态、判定加成
- `game/events.py`：`can_use` 支持 `need_max`；`roll_check` 支持三种判定形式并计入 `check_bonus`；`apply_event` 支持 `{score}` 替换与 `score_field`
- `game/achievements.py`：成就类型扩展到 **结局 / 事件 / 属性 / 排名 / 数值 / 全局** 六类（全局类读存档，如省份数）
- `game/records.py`：存档补 `provinces` 字段（跨局累计旅游省份）
- `main.py`：开局解锁「北理新生」；每次综测排名后维护 `Rank1` / `排名前5` 状态；记录旅游省份
- 数据量：事件 **99 → 162 条**、天赋 **21 → 26 条**、成就 **3 → 7 条**

**修复**
- 清理存档中因成就改名而失效的 `【占位】…` 成就名（3 条），成就计数恢复正确
- 提高四级 / 六级事件权重（1 → 4），保证能触发

**验证**
- 生而为男 → 性别男；花言巧语使表白成功率由 **70.4% → 94.8%**（+24.4 ≈ +25）
- 六级出分：智力 4 均分 **476**（88% 过 425）；智力 10 均分 **587**（100% 过 425）
- 全流程实跑：性别 / 组织 / 排名 / 竞赛 / 结局院校（清华大学）/ 旅游省份 **11 个**均正常写入

---
### 2026-09-13 · todo 第 1–11 项

**新增**
- `audio/click.wav`：像素按钮音（标准库 `wave` 生成方波，60ms）
- `docs/achievement-list.md`（成就表）、`docs/ending-list.md`（结局表 + 升学院校分层）

**变更**
- **第 1 项**：14 条占位事件全部改写为正式事件，事件池 83 → **99 条**（含 16 条学生组织加入事件），全文无「占位」字样
- **第 2 项**：`main.py` 初始化 `pygame.mixer`，左键点击播放 `click.wav`
- **第 3 项**：天赋卡片去掉「【稀有/史诗/传说】」前缀，只显示效果
- **第 4 项**：成就达成时在**左下角弹窗**显示 3 秒（浅绿卡片），并列出成就表
- **第 5/6 项**：结局改写为 **11 条正式结局**（含文案与权重）；升学类结局按 `{school}` 占位由 `game/endings.py` 的 `SCHOOLS` 决定，**15 所院校全部为 985**
- **第 7 项**：表白事件按性别拆为两条（男生追女生 / 女生追男生）；性别写入 `flags` 供事件判定
- **第 8 项**：加入 **16 个学生组织/社团**（含大比重的「学生组织/社团」通用项）；大一 10 月加入（`flags_forbid: ["组织"]` 保证每局只一次）、**大二 9 月留任部长**、**大三 9 月当选主席**
- **第 9 项**：大一/大二/大三的 6 个期末增加**综测排名**文案（大一约 300 人、大二大三约 50 人）；排名 = 智力 × 10 + 本学期加分换算；期末有「认真复习 +5 / 摆烂 −8」
- **第 10 项**：新增 **8 个竞赛**（校级：屠龙大赛、芯火计划、数模校赛、微积分竞赛；全国级：挑战杯、ACM-ICPC、数模国赛、蓝桥杯），按判定分**一等奖 / 二等奖 / 三等奖 / 未获奖**，获奖加综测分
- **第 11 项**：取消「这个月没什么特别的事」，改为每个时段都有保底事件，**每回合必有事件**

**验证**
- 200 局 × 48 回合 = **9600 回合，`pick_event` 返回 None 次数为 0**（取消的分支不会被触发）
- 单局实跑：组织加入 1 次、综测排名 6 条、竞赛获奖正常、结局「保研外校 → 清华大学」、成就弹窗与音效均已加载

**未做（下一轮）**
- todo 第 12–15 项：10 条特殊事件、更多军训/寒暑假/校园/实习事件、5 个新天赋、4 个新成就

---
### 2026-09-10 · 天赋与事件清单独立成两个文件

**变更**
- 从 `docs/talent.md`、`docs/event.md` 的附录中拆出两份独立清单：
  - **`docs/talent-list.md`**：天赋清单（属性天赋 12 条 / 特殊天赋 9 条 / 等级概率表）
  - **`docs/event-list.md`**：事件清单（58 条，含文本 / 类型 / 时段 / 效果 / 条件 / 判定 / 状态 / 标签 / 权重 / 概率）+ 判定事件结果分支表
- 原 `docs/talent.md` §8、`docs/event.md` §9 改为**一行指引**，指向对应清单文件；正文层级不再嵌套附录
- `docs/03` 目录树、`AGENTS.md` §0 文档行同步补充这两个文件

---
### 2026-09-10 · 开局性别 + 事件/天赋清单表

**新增**
- **玩家性别**：开局随机为男 / 女，并作为开局第一条日志文本：「你是一名男生/女生，是北理工的大一新生。」
- 性别显示位置：**游戏主界面右上角**（主强调色 22 号字）、**回顾列表每行**「第 N 局（男/女）」、**单局回顾标题**「本局回顾 · 男/女」
- 存档记录新增 `gender` 字段
- `docs/event.md` **附录：事件清单**（58 条，含文本 / 类型 / 时段 / 效果 / 条件 / 判定 / 状态 / 标签 / 权重 / 概率）+ 判定事件结果分支表
- `docs/talent.md` **附录：天赋清单**（属性天赋 12 条、特殊天赋 9 条、等级概率表）

**变更**
- `game/player.py`：`new_player` 新增 `gender`（随机男 / 女）
- `main.py`：开局写入开场日志文本；游戏页右上角、回顾列表、回顾详情显示性别；`write_record` 记录性别
- 两张清单表由 `data/*.json` 生成，内容变更后需重新生成

**未做**
- 人类已确认 **`ppt.md` 不恢复**（该文件此前被删除，git 中显示为 `D ppt.md`）

---
### 2026-09-10 · 100 局随机测试 + 设计文档归入 docs/

**新增**
- `test_1.md`：**测试报告 1 · 随机天赋与属性 100 局**（测试方法、8 个学期期末的四属性汇总与极值、结局分布、每局明细、结论与观察）

**变更**
- **设计类文档移入 `docs/`**：`talent.md` → `docs/talent.md`，`event.md` → `docs/event.md`；根目录只保留 `AGENTS.md`、`README.md`、`CHANGELOG.md`、`test_1.md`
- 同步更新引用：`AGENTS.md` §0、`docs/02` 天赋与事件、`docs/04` 事件字段表；`docs/03` 目录树补充 `docs/` 下的文件清单

**测试结论摘要**
- 智力一路上涨（大一上 5.69 → 大四下 10.41，**+4.72**）；体质持续下滑（5.38 → 3.59，**−1.79**）；颜值 +1.26、家境 +0.75
- 四属性合计平均 **+4.94**，整体上行
- 结局 **100 局全部命中「【占位】保研本校」** —— 因为 `data/endings.json` 目前只有 3 条占位结局且权重偏向它；需补齐 11 条真实结局后复测
- 属性极值出现 **体质 −1.7**、**智力 15.8** —— 与「不封顶」裁定一致，但负值体验不合理，建议后续裁定**下限 0**

---
### 2026-09-10 · 事件系统详细设计 + 36 条日常事件

**新增**
- `event.md`：**事件系统详细设计**（分类、字段表、状态标志、判定公式、保底机制、特殊时段库、抽取流程）
- `data/events.json`：新增 **44 条日常事件**（含 6 条保底、8 条无属性影响纯叙事、22 条有好有坏、5 条带标签、3 条有前提条件、2 条判定事件），事件总数 58 条

**变更**
- 事件 schema 扩展：新增 `flags_need` / `flags_forbid` / `flags_set` / `flags_clear`（状态标志）、`chance`（触发概率）、`weight`（抽取权重）、`check`（判定）；选填字段可省略
- `game/player.py`：玩家新增 `flags` 状态集合（与结局标签 `tags` 分开）
- `game/events.py`：
  - `can_use` 增加状态判断（`flags_need` / `flags_forbid`）
  - `pick_event` 改用事件自带 `weight` 作基础权重（保底事件 0.2），并在候选筛选阶段掷 `chance`
  - `apply_event` 支持 `check` 判定（成功率 = base + Σ(属性值 × 系数)，夹在 5%~95%），支持 `flags_set` / `flags_clear`，日志文案取判定结果文案
- `main.py`：败者食尘！回溯时一并清空 `flags`
- `docs/02` §6 事件系统、`docs/04` §1.2 事件字段表同步更新

**验证**
- 表白判定：颜值 8 / 家境 5 → 实测成功率 69.8%（公式期望 70%）；颜值 2 / 家境 1 → 33.1%（期望 32%）
- 状态标志：未恋爱时"约会/分手"不可触发；表白成功获得「恋爱中」；恋爱后"表白"不可触发、"约会"可触发；分手后状态清空、"表白"恢复可触发
- 30 局 × 48 回合模拟：普通事件 1108 / 保底事件 26 / 无事件 306（保底占比约 1.8%，符合 6 条 × 0.2 权重）；出现状态「恋爱中」「学生组织」

---
### 2026-09-10 · AGENTS.md 项目信息与技术栈准则

**规范**
- **AGENTS.md 新增 §0 项目信息（简要）**：项目名、课程、范围、代码位置、数据与存档、文档清单、交付物、详细设计出处
- **准则四改为内嵌技术栈表作为硬约束**：Python 3.12 / pygame 2.6.1（唯一第三方依赖）/ JSON / 本地文件存档与导出 / 系统字体 + Zpix 像素字体 / Windows / `python main.py`；并新增「禁止引入课程未要求的工具链」（测试框架、CI、容器、打包脚本）
- AGENTS.md 引言由「不包含任何游戏设计内容」改为「规定行为准则与简要项目信息」

### 2026-09-10 · 结局页三张信息卡片移到大标题下方

**界面调整**
- 位置由 `(30, 620 / 674 / 728)` 改为 `(30, 80 / 134 / 188)`；结局文案起点由 y=100 下移到 y=260

### 2026-09-10 · 属性卡片 / 结局页信息卡 / 文本清晰度

**新增**
- 新增**准则九「每轮修改记入更新日志」**，写入 `AGENTS.md`

**界面调整**
- **游戏主界面属性改为卡牌**：白底卡片 `(30, 170, 480, 46)` + 墨绿左条；分专业提示条下移到 y=224、分隔线 y=270、日志区改为 y=284 高 556
- **结局页复用三张信息卡片**：书院·专业 / 天赋 / 属性
- **文本清晰度修复**：次要文字色 `TEXT_DIM` 由 `(107,114,128)` 加深为 `(84,92,106)`；日志正文 17 号 → 18 号、行高 26 → 29；日志区加半透明白底面板

### 2026-09-10 · 天赋分级与特殊天赋

**新增**
- **天赋分级系统**：蓝（稀有 75%）/ 紫（史诗 20%）/ 金（传说 5%），抽天赋按等级概率
- **4 属性 × 3 等级 = 12 个属性天赋**：数值分别为 +1 / +2 / +4
- **9 个特殊天赋**（名称严格照 `docs/talent.txt`）：睿信土著 / 明德土著 / 求是土著 / 特立✌ / 败者食尘！ / 竞赛大神 / 全面发展 / 你就卷吧 / 手眼通天
- **两个新天赋接口**：`force`（强制某类事件）、`rewind`（回溯时间）
- `talent.md`：天赋系统详细设计文档；`CHANGELOG.md`：本文件

**变更**
- `data/talents.json` 结构改为 `{ tier_rates, talents }`，每条含 `effects` / `shuyuan` / `boost` / `force` / `rewind`
- `data/events.json`：为占位事件补打事件标签（竞赛 / 文体 / 实验 / 图书馆 / 学生组织），并新增 4 条占位事件
- `game/player.py`：新增 `collect_forces`、`collect_rewind`；`draw_talents` 按等级概率抽取
- `game/events.py`：新增 `apply_forces`（按天赋规则收窄候选，同时限定时段）
- 开局页天赋卡片按等级着色（左侧色条 + 等级标签）

**已实现的特殊天赋规则**
- 指定书院：睿信土著 / 明德土著 / 求是土著 / 特立✌
- 标签加权：竞赛大神（竞赛 ×3）、全面发展（文体 ×3）
- 强制事件：你就卷吧（寒假 / 暑假必定从竞赛 / 实验 / 图书馆里抽）、手眼通天（大一 10 月必定加入学生组织）
- 时间回溯：败者食尘！（每回合开始 3% 概率回到大一 9 月，保留属性 / 天赋 / 书院，清空专业与已触发记录，每局限一次）

### 2026-09-10 · 卡片化改造 / 符号字体 / 回溯保留文本

**界面调整**
- 游戏主界面：书院 / 专业、天赋改为**独立卡片 + 放大字号 + 明显配色**（浅绿卡片 / 浅褐卡片），分专业提示条改为深绿底白字

**修复**
- **符号字体回退**：主字体缺字时自动换用 Segoe UI Emoji，修复「特立✌」的 ✌ 显示为方框
- **败者食尘！回溯保留原本事件文本**，只追加回溯提示

---

## 2026-09-09 · 规范与设计阶段

### 新增
- `AGENTS.md`：把人类给定的 5 条准则扩充为可执行规范
- `docs/01-可行性分析.md`、`docs/02-游戏设计.md`、`docs/03-项目架构设计.md`、`docs/04-程序设计.md`、`docs/05-页面设计.md`：五份设计文档
- 新增准则六「只做人类要求的事」、准则七「设计阶段不涉及实际开发」、准则八「设计流程只保留五项基础规范」
- 甘特图：2026-09-07 ~ 09-17，以 2 天为周期

### 变更
- `AGENTS.md` 重构：只保留 AI 准则 + 变更记录，游戏设计内容全部迁入 `docs/`
- 可行性分析补充工期与甘特图
- 时段体系：由「军训 / 期末 / 寒暑假 / 实习」改为**七个时段**（新增毕业论文答辩，寒暑假拆为寒假与暑假）
- 属性规则：**不封顶**、20 点**可以分不完**、允许 **0.1 粒度小数**
- 结局判定：**同分随机取**

### 确定的关键规格
- 技术栈：Python 3.12 + pygame 2.6.1（唯一第三方依赖）
- 题材：BIT 重开模拟器，本科四年 48 回合
- 书院 4 个（睿信 / 求是 / 明德 / 特立），大二开学随机分配专业（20 个）
- 事件 ≥100 条，分通用 / 特殊；天赋先 5 选 3，后改 5 选 2
- 界面 6 个：首页 / 开局 / 游戏 / 结局 / 成就 / 回顾

---

## 2026-09-09 · 原型与框架

### 新增
- `prototype/`：游戏原型（`main.py` + `game.py` + `data/`），验证玩法与界面可行性
- `main.py` + `game/`（8 个模块：`data` / `player` / `timeline` / `events` / `endings` / `achievements` / `records`）+ `data/`（4 份 JSON）+ `save/` + `exports/`
- `fonts/zpix.ttf`：开源像素字体 Zpix（OFL），用于大标题
- `README.md`：运行与数据字段说明
- `ppt.md`：开题报告 PPT 文案（5 页）

### 变更
- 正式代码落仓库根目录；原型保留在 `prototype/` 作对照
- 逻辑层由单文件 `game.py` 拆为 `game/` 八个模块
- 记录与成就进度**跨次运行保留**（写入 `save/records.json`）

---

## 2026-09-09 · 界面与交互迭代

### 新增
- **成就系统**：达成结局 / 触发特殊事件 / 属性达到特定值，跨局累计
- **回顾与导出**：保留最近 5 局，可查看每月文本并导出 txt 到 `exports/`
- **暂停页**：暂停按钮 + ESC，两项（继续游戏 / 结束并返回首页）
- **月度日志**：保留本局全部月份文本，可滚动
- 开局页「返回首页」按钮；属性分配「随机分配」「清零」按钮
- 响应式：竖屏 540 × 960，等比缩放 + 居中留白

### 变更
- 视觉风格重做：北理绿配色（`#1B9849`）、渐变背景、卡片色条、圆角渐变主按钮
- 大标题改为像素风「BIT重开模拟器」，字号 48
- 去除顶部装饰条与标题下划线；游戏页「书院·专业」「属性」加下划线
- 日志顺序改为**最新月份在顶端**
- 属性分配每项加卡片边框；「随机分配」「清零」缩小到与标题同排
- 天赋显示在游戏页右上角、回顾列表每行与单局详情右上角
- 天赋由 5 选 3 改为 **5 选 2**，且**未选完也能开始**

### 修复
- **按钮误触发**：`MOUSEBUTTONDOWN` 未区分按键，右键 / 中键 / 滚轮都会触发按钮。改为只响应左键（`event.button == 1`）
- 寒假与暑假事件描述混淆：时段拆分 + 事件 `stage` 改为列表，寒假专属 / 暑假专属 / 假期通用三类
- 游戏中途结束后记录缺失：暂停页「结束并返回首页」写入记录，结局记为「中途结束」