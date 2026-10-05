# Dexterous Hand Atlas

## 算法图谱（2026-10-05）

新增与产品地图并列的 `/algorithms/`，通过“按问题”“按方法”“研究案例”三个入口阅读内容，首页统一单列，右侧标签栏筛选研究案例。首批包含八个问题专题、六个方法专题、五个灵巧手案例与一个单独标明平台边界的相邻操作案例。基础解释、方法与案例正文使用 Markdown，分类属于编辑组织方式；尚未运行算法或复现实物实验。

关系与阅读范围维护于 `data/algorithm-atlas.json`，`website/hooks/algorithms.py` 校验页面、来源和案例关联并生成目录、来源登记与交叉阅读。问题和方法的筛选跨维度同时满足，URL 保留筛选状态；禁用 JavaScript 仍可阅读全部专题与案例。已有 Shadow 论文页直接接入，不另复制一份解读。

检查：`python -m unittest discover -s tests -v`、`node --test tests/algorithm-atlas.test.cjs` 和 MkDocs 严格构建。新增 Python hook 后须重启开发服务。

## 知识地图与发展脉络（2026-10-04）

网站按“具体平台 → 技术路线 → 工程问题 → 领域发展”组织阅读。首页新增领域发展、技术路线、工程问题与论文入口；现有产品地图继续承载逐型号探索。以下历史进度数量不作为当前统计，实时数量由地图数据生成。

- `/development/`：首批七条学术与工业记录，涵盖 2001–2024；记录选样而非完整领域年表。每条说明问题、方案、进展、时间口径与证据边界。关注点归纳属于本站解读，不能把样本数量当作领域热度。
- `/technologies/tendon-driven/` 与 `/technologies/underactuation-and-synergies/`：有来源的技术路线与实现对照；相同路线不自动表示技术继承。
- `/engineering/transmission/`：在原研究框架上补充公开资料分析；验证流程尚未执行。
- `/papers/`：按研究问题组织论文入口，保留原有笔记与阅读范围。

发展记录维护于 `data/field-development.json`，由 `website/hooks/knowledge.py` 校验和渲染。日期保留年、月、日的实际精度；`basis` 区分论文发表、预印本提交、展示、公告、厂商回溯，`date_relation` 区分事件日期与至迟边界。来源记录 URL、类型、阅读定位和复核日期。关系分为 `same-route`、`comparison`、`documented-transfer`；最后一种必须由编辑核对原始转化证据，结构校验不能代替人工审阅。

路线入口使用 `data/technologies.yaml` 的可选 `page`。产品详情与对比的相关阅读共用 `data/engineering-articles.json`，`section_label` 区分工程解读和技术路线。新页面沿用现有纸色、砖红配色，布局规则位于 `website/docs/stylesheets/knowledge.css`。

检查：`.venv\Scripts\python.exe -m unittest discover -s tests -v` 与 `.venv\Scripts\python.exe -m mkdocs build --strict -f website\mkdocs.yml`。修改或新增 Python hook 后须重启开发服务。

2026-10-02 阶段记录：**64 个地图档案**。最新加入曦诺 Prima 1，并为全部详情页增加硬件 / SDK / 模型支持栏目，见 [本轮说明](research/sources/platform-support-2026-10-02.md)。苏度 R1 已作为机器人系统接入地图和搜索，统计为 64 款手 + 1 个系统；自由度/传动参数待核的档案直接列在地图下方。R1 使用 7 个官网视频，见 [修正记录](research/sources/map-coverage-and-sudo-2026-10-02.md)。前批新增清单见 [第二轮](research/sources/expansion-02-2026-10-02.md) 和 [第一轮](research/sources/expansion-2026-10-02.md)。档案仍为部分核验，不代表完整技术报告。以下早期记录中的数量保留为当时进度。

A technical map of robotic dexterous hands from research platforms to embodied AI systems.

本地 MkDocs Material 知识地图，以产品、技术分类、原始证据和研究案例建立关联。未上传 GitHub。

## 启动与安装

PowerShell：

```powershell
Set-Location Q:\daydream\JoanWu\hand
.\.venv\Scripts\python.exe -m mkdocs serve -f website\mkdocs.yml
```

打开 http://127.0.0.1:8000 。前台运行按 Ctrl+C 停止；端口占用时先确认是否已有本站服务。
修改 Markdown 或 data 下 YAML 会自动重建；修改 Python hook 后需要重启服务。

重新安装环境（无需 Node）：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --no-cache-dir -r website\requirements.txt
```

## 目录与职责

| 路径 | 职责 |
| --- | --- |
| data/hands.yaml | 产品参数、状态、技术关联、评价与资源 |
| data/technologies.yaml | 多维分类与稳定 ID |
| data/sources.yaml | 原始来源、版本与核验日期 |
| data/projects.yaml | 案例进度、页面与关联对象 |
| website/hooks/atlas.py | 校验并生成产品详情、卡片、导航与索引 |
| website/docs/hands/ | 手写工程分析与模板 |
| website/docs/technologies/ | 技术地图 |
| website/docs/engineering/ | 问题导向的研究框架 |
| website/docs/research/ | 研究入口、案例与模板 |
| website/docs/resources/ | 资源与证据规范 |
| website/docs/papers/ | 论文索引 |
| research/papers、notes、sources | 本地研究工作目录 |
| tests/test_atlas.py | 证据约束与生成行为检查 |

## 自动生成与新增产品

首页与技术地图提供“系统结构 / 产品关联”两个视图。点击图中节点查看分类入口或具体证据；产品视图支持切换灵巧手及筛选技术维度。产品详情页直接显示该产品关系图。

灰线表示编辑分类；实线表示官方支持，虚线表示文献实现，点线表示本人验证。没有证据的能力不连线。地图直接读取同一份 YAML，修改数据后自动同步；使用本地 SVG 与 JavaScript，不依赖外部 CDN。

宽屏采用中心向两侧展开的布局，窄屏改为顶部向下展开。键盘可通过 Tab 选择节点、Enter 或空格查看详情；禁用 JavaScript 时仍可阅读下方资料。

serve / build 自动读取 YAML。非 planned 产品生成虚拟页面 hands/generated/<id>.md 并加入导航。
不向 docs 写入生成文件，不覆盖手写分析。首页和数据库卡片、技术关联、研究索引和来源登记也从数据渲染。
最终 HTML 在 website/site，不要直接编辑。

在 hands.yaml 的 hands 列表添加：

```yaml
- id: new-hand
  name: 新灵巧手名称
  status: scaffold
  facts:
    model: {value: null, sources: []}
    company: {value: null, sources: []}
  technologies: []
  assessments: []
  resources: []
```

保存后卡片、页面、导航自动更新，无需手改首页和索引。ID 使用小写连字符。

- planned：候选卡片，不生成详情。
- scaffold：结构示例，参数允许未知。
- researched：资料已整理，必须有带来源的具体型号；不代表独立实验验证。

正式整理时按具体型号、版本拆分系列。facts 支持 model、company、country、year、application、product_status、fingers、dof、actuators、weight、dimensions、materials。
重量和尺寸写清单位；自由度注明主动/被动。null 是未知，所有非空值必须引用已有来源。

如需分析，复制 website/docs/hands/template.md，并添加 analysis_page: hands/new-hand.md。此页面必须存在且位于 docs 内。

## 证据与技术关联

在 sources.yaml 登记真实来源：id、title、url、kind、version、verified_on。
kind 可选 official / paper / report / repository / video / community；日期使用 YYYY-MM-DD；URL 必须是 HTTP(S)。
version 记录文档或型号版本，不明确时写“来源未标注”，不要猜测。

参数使用 {value: 实际值, sources: [真实来源ID]}。

technologies 每项字段：

- id：technologies.yaml 中的技术 ID。
- evidence_type：official（官方支持）、paper（文献实现）、experiment（本人验证）。
- scope：型号、版本、条件。
- sources：支持这条关联的来源 ID 列表。

本人验证应引用包含方法和结果的实验记录地址。来源类型与能力证据类型不可混用。
assessments 每项使用 kind（fact / reported_limitation / interpretation）、text、scope、sources。
resources 直接引用来源 ID；图片、论文、CAD、视频和代码统一记录 URL，不自动下载。

## 添加研究案例

复制 website/docs/research/template.md，记录问题、假设、环境、复现步骤、指标、结果、失败与局限。
在 projects.yaml 添加 id、name、status、page、summary、hand_ids、technology_ids、source_ids。
研究入口与技术关联自动更新；状态 planned / in-progress / completed 按实际进度维护。
若需要顶栏导航，另在 mkdocs.yml 的“研究与实验”中添加页面。

当前抓取仿真案例只是计划，没有代码、数据或已验证结果。个人经历待本人确认后补充。

## 检查

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m mkdocs build --strict -f website\mkdocs.yml
```

校验拒绝重复 ID、未知关联、无来源的非空参数和非法页面路径。
结构校验不代替人工核验真实性和来源是否支持陈述。

参考：[Material 卡片布局](https://squidfunk.github.io/mkdocs-material/reference/grids/) · [MkDocs hooks](https://www.mkdocs.org/user-guide/configuration/#hooks)

## 首页地图与时间依据

首页默认使用“公开年份 × 主动轴数量分组”，同时提供传动路线、手指构型、驱动规模和主动轴演进视图。五种视图的横轴均为公开年份，纵轴按当前技术维度定位，未知数值保留 null。缩小时邻近坐标聚合，悬停查看名称与依据；图片直接进入该产品详情，数字按钮选择同组产品，预览中的“在地图中展开全部”用于展开。

- `data/hand-timeline.json`：逐型号登记年份、事件类型、具体解释、出处与核验日期。`basis` 为 paper / release / demonstration / document；`relation: by` 表示至迟当年已有公开资料，页面显示“≤ 年份”，不冒充首发时间。论文采用说明中明确的版本年份。
- `data/map-coordinates.json` 和 `data/research-metrics.json`：数值坐标、传动分类及计数口径。
- `data/media.json`：远程图片、视频及出处，不下载媒体。

`website/hooks/atlas.py` 每次构建把同一份校验后的产品数据用于地图 JSON 和详情页，避免网页快照遗漏新增年份。`.\.venv\Scripts\python.exe scripts/build-visual-samples.py` 可额外刷新 docs 内供独立预览使用的快照；正常 MkDocs 构建不依赖手动刷新。

操作能力入口位于 `website/docs/capabilities.md`。坐标不是灵巧性排名；同色连线表示分类关联，不表示技术继承。

### 探索状态与筛选

搜索词和已选标签显示在地图上方，可逐项移除；“清除全部筛选”清空搜索和标签，保留当前视图。“清除标签筛选”只移除侧栏标签。同组标签取并集，不同组取交集；缺少某项标签不等于产品不支持该能力。

同一浏览器标签页中，从产品详情返回地图会恢复视图、搜索、标签、缩放、平移、已展开的产品及滚动位置。状态保存在 `sessionStorage`，关闭标签页后不保证保留，也不跨设备同步。返回时显示恢复提示；“重新开始探索”回到默认自由度视图并清空筛选、重置地图位置。图内复位按钮重置缩放和平移并收起已展开的聚合组，保留搜索和标签。

`javascripts/map-state.js` 检查保存记录，剔除已经移除的标签和产品 ID；保存记录损坏或浏览器禁止存储时，地图仍能使用。平移按绘图区比例保存，窗口大小变化时同步调整。状态验证运行 `node --test tests/map-state.test.cjs`。

## 技术资料网页

34份深入资料入口：<http://127.0.0.1:8000/hands/reports/>。

`data/report-pages.json`维护发布清单、摘要和待补项；`website/hooks/reports.py`在MkDocs构建时将其中的研究笔记生成网页，并加入导航与搜索。Shadow和LEAP继续使用原有报告。其余正文直接编辑`research/collection/hands/`对应文件，开发服务器会监测更新；不要在构建输出`website/site/`里修改。

新增报告时向清单添加名称、源路径、页面路径、摘要与缺口，再运行严格构建核对链接。发布资料不等于已经核验坐标参数；坐标依据单独登记，但首页与详情在同一次构建中同步。


## 34款产品接入地图（2026-10-02）

首页地图与产品详情统一使用`website/hooks/atlas.py`加载的数据。`research_hands.py`将发布清单中的32份研究笔记转换为产品记录，与Shadow/LEAP两条原记录合并。详情直接呈现大图、可选技术维度与完整证据正文。

`data/research-metrics.json`存放新增产品经核对的坐标、口径与来源，缺失值为null。`data/media.json`维护远程图片/视频及出处。正常构建会同步地图数据。34 款均登记了媒体入口，远程可用性取决于原站。时间地图中传动未知的产品位于灰色行；其他参数视图中缺少当前坐标的产品进入“未定位”面板。

修改Python hook代码后需重启MkDocs开发服务；仅修改研究笔记或参数文件会触发重建。


## 统一产品详情页

### 产品演进（2026-10-03）

`data/product-lineages.json`（schema 2）保存产品族、公开记录节点、代际/修订关系、变化对照与出处。2026-10-03 的核查覆盖全部 82 款已发布灵巧手，共 56 组共享产品族或单款核查。覆盖不表示所有历史已查全；每组记录独立的证据边界。

详情页在媒体与技术预览之后、完整技术记录之前显示路线，右侧目录提供“产品演进”锚点。同族页面共享一份数据，并突出本页型号；点击其他型号进入对应详情。`product-lineage.css` 维护该模块样式。

扩展时将已有产品 ID 加入 `member_ids`，每款只归属一个共享记录。`status` 分为 `lineage`（有依据的迭代或技术分支）、`parallel`（产品族/并行路线）、`review`（未确认前后代，展示简短具体核查说明）。`mode=review` 不绘制空时间线。

节点记录 `date_relation`（on / by / unknown）、日期依据与来源。已收录节点填写 `hand_id`；未单独收录的历史节点填写 `hand_id: null` 与原始 `url`，不会新增首页产品。只有明确证据才添加 `relationships`，不能依据公司相同、编号相近或年份相邻推定继承。来源同时支持关系与具体变化；比较说明区分原文事实与工程解释，平行配置使用具体型号列名，避免暗示“此前/此后”。首次公开、文档发布、软件更新和交付日期不得混写。

运行 `.venv\Scripts\python.exe -X utf8 scripts/export-lineage-audit.py` 导出逐款核查表至 `research/notes/product-lineage-audit-2026-10-03.md`。测试检查全量覆盖、重复归属、来源键、内外部跳转和地图产品集合；MkDocs 严格构建检查生成页面。`research/sources/assemble-lineage-review-2026-10-03.py` 仅是本次编辑快照，不应在后续人工维护 JSON 后重新运行。

82 款产品共用 `website/hooks/product_details.py`，布局与交互分别在 `product-details.css`、`hand-detail.js` 中维护。页面保留产品地图返回入口，使用统一的藏青底色、柔白正文和荧光紫强调。`--dex-accent` 为品牌强调色，旧的 `--dex-gold` 变量作为兼容别名保留；分类标签与地图路线继续使用独立的分类颜色。

产品概览采用 B 方案：左侧章节标题、紧凑的产品身份栏，下方图片与技术预览并排。可选 `display_name` 只改变显示标题，完整产品名仍在标题下保留。已整理的手指、驱动和重量字段显示为快捷指标，点击跳到完整指标与依据；机构口径复用已核查记录。700px 以下媒体与技术预览改为上下排列。图库保留原始出处与说明，图片显示缩略图，视频提供播放标记；远程媒体不可用时保留说明和来源入口。

技术导航固定为基本信息、机械与驱动、感知系统、控制与操作、仿真与软件、优势与局限、技术解读、资料来源。预览和下方完整记录共用内容；原始研究笔记单独折叠保存，明确标注早期记录与修订过程。笔记标题只用于编辑分类，不据此推断产品具备某项能力；跨维度说明保留其原文与出处。

详情正文沿用技术摘要与产品演进的开放式排版。桌面端从产品概览、技术摘要、产品演进，到完整技术指标、技术章节与工程分析，统一采用左侧章节标题、右侧正文的布局，正文与表格的缩进保持一致；左侧标题在所属章节内随滚动保持可见，右侧固定目录独立于正文布局。850px 及以下收为标题在上、正文在下的单列，避免手机正文过窄。摘要要点、演进时间线与分析步骤保留各自的内部结构。表格无外框和竖线，采用透明底色、轻细横线、弱化的列标题与统一单元格留白。四列以上的宽表在自身容器内横向滚动，两三列短表优先换行；不因宽表扩大整页。共用规则集中维护于 `product-details.css`，`explorer-rail.css` 只控制侧栏及顶部响应布局，不再切换正文章节的列数。

### 逐指机构与媒体画廊

`data/hand-kinematics.json` 为每款产品记录适用版本、逐部位主动输入与耦合、传动解释、运动范围、操作证据和未核清内容。`range_rows` 仅录入已找到出处的逐轴上下限；`basic` 用于同步已确认的顶部指标。研究笔记与原始记录仍保留，不把缺少关节信息的产品标成“资料完整”。

`data/media-galleries.json` 按产品登记图片、视频和图册，包含画面说明与出处。`image` / `video` 在画廊切换，`link` / `document` 显示外部入口。不同型号和选配必须在说明中标明；不自动将官网导航图片或其他型号照片加入画廊。`scripts/collect-media-candidates.py` 只搜集候选 URL，人工筛选后才入库；不下载媒体。

2026-10-02：34 款均有机构核查记录，21 款有多个图片/视频画面。已剔除本次检查发现的 3 条 LEAP v2 失效直链；qb SoftHand2 原站拒绝本次媒体请求，保留来源和手册入口。各款的限位与逐轴映射缺口见数据中的 `gaps`。
## 技术对比入口

访问 `/compare/`，选择最多三款灵巧手。所选 ID 保存在 URL 的 `hands` 参数中，刷新与分享链接均保留选择；清空选择不会影响产品数据。

提供完整对比、机械构型、感知与力控、仿真与开发四种视图。`view` 和 `differences` 参数保留视图与差异筛选；同一浏览器标签页的 `sessionStorage` 保存当前组合。显式 `hands` 参数优先于保存的组合，`hands=` 表示清空；详情和地图的 `add` 入口追加产品，满三款时提示移除，不替换已有项。关闭标签页后不保证保留。

差异标记仅描述文字记录差异、统计范围核查需要及缺少依据的情况，不判定产品优劣或参数可比性。SDK 摘要保留语言与环境；模型摘要列出各格式状态；原始记录和出处可以展开阅读。验证状态行为可运行 `node --test tests/comparison-state.test.cjs`。

对比数据由 `website/hooks/comparison.py` 在构建时生成 `comparison-data.json`，复用现有产品事实、地图坐标、机构核查、软件支持和标签依据，不手写另一份产品参数。来源 ID 解析为原始链接，版本、统计边界与未知项保留。感知/控制暂只投影已结构化记录，未标注不表示产品不支持。该对比工具不进行综合性能评分，也不代表已完成本地实验验证。

## 感知核查与测量位置图

`data/sensing-audits.json` 记录具体版本、通道测量位置、物理量、输出单位、频率口径、标定、配置、控制用途、证据边界和逐项出处。当前深入核查 Shadow Classic Electric（December 2024）、LEAP v1 Full、Wuji Hand 2（2.2 Beta 非触觉样机）；不表示其余产品都已达到相同整理深度。

`website/hooks/sensing.py` 校验并投影这份记录。已核查产品的详情感知章节与预览、首页标签、对比表和 `/engineering/sensing-chain/` 可点击位置图都复用它。只有 `documented` 通道允许能力标签；`absent`、`unknown` 和 `unvalidated` 分别表示此配置未配备、证据不足和估计链路未验证，不能生成正向能力标签。早期研究笔记作为历史记录保留。

API main 分支及厂商 latest 文档会更新，复核日期不等于固定修订号；本次未做实物测量或接口运行验证。增加产品时必须先确认版本和原始来源，不能把电流、腱负载或仿真传感器自动标记为实物接触力支持。

## 技术摘要与编辑分析

各产品在媒体区后、产品演进前显示“技术摘要”。已有单独编辑记录的产品使用 `data/product-editorials.json` 中带来源和事实/解读标注的三个要点；其他产品直接摘录 `hand-kinematics.json` 的机构定位、驱动链路与核查缺口，不自动生成作者观点。

当前 Shadow Classic、LEAP v1 Full、Wuji Hand 2 有完整的编辑分析草稿，按“公开依据 → 推理 → 有条件的判断 → 待验证问题”组织。页面的 `Joan Wu’s Analysis` 是作者栏目名，`draft` 状态明确显示“待 Joan Wu 审阅”；生成草稿不表示作者已经认可结论，也不表示已经执行实验。仅在作者实际审阅后将记录改为 `reviewed`，并填写 `reviewed_on`。编辑日期 `edited_on` 不等于来源重新核查日期。

`website/hooks/editorials.py` 校验来源、版本与审阅状态并渲染；摘要和分析都加入固定章节目录。追加产品需写出具体推理及适用条件，不能复制通用“优点/缺点”文案或给未核查的产品附上作者署名结论。


## 首页时间泳道（2026-10-04）

首页采用 B 方案：横向逐年排列，纵向按所选分类分行，每款产品是独立的图片与名称链接。同一年、同一类别的多款产品依次排列，行高按内容增长，避免标签重叠。年份栏和分类栏在产品区域滚动时固定。

五种视图保留：自由度分组、传动路线、手指构型、驱动规模、主动轴演进。后两种按确切数量分行，行距不表达数值距离；未知参数保留在待核实行，只有公开年份缺失的条目进入时间待核面板。`≤ 年份` 保留证据上界含义，未改写为发布日期。

搜索、证据标签、产品详情和技术对比入口保留；列宽可调整，分类、条件、列宽、横纵滚动位置保存于同一标签页，进入详情后返回可恢复。默认浏览最近年份，较早产品通过横向滚动查看。数据仍由 MkDocs 钩子生成，不在页面重复维护。

布局分组逻辑：`website/docs/javascripts/timeline-layout.js`；交互：`dextrail-map.js`；样式：`website/docs/stylesheets/timeline-map.css`。验证可运行 `node --test tests/timeline-layout.test.cjs tests/map-state.test.cjs`。

## 知识栏目阅读版（2026-10-04）

产品地图、领域发展、技术路线、工程问题、论文与方法、技术对比共用六项导航，由 `website/hooks/knowledge.py` 的 `on_page_content` 按当前页面深度生成；产品详情和资料内页也保留地图入口。

技术路线首页以机构示意与路线入口呈现，不再输出旧关系图和未完成的分类底稿。工程入口只展示已有图解，论文入口采用年份、研究问题、方法摘要和原文链接。发展页按年份组织学术与工业节点，并区分资料记录与跨案例解释。来源、时间口径和适用范围用原生 `details` 展开，保持键盘可用。

阅读样式集中在 `website/docs/stylesheets/knowledge-reader.css`，五张机构与方法概念图在 `website/docs/images/knowledge/`。示意图不替代产品几何或实验结果；具体结构与方法均保留原始来源。嵌套图文区块显式使用 `markdown="0"`，避免 `md_in_html` 误拆阅读容器。

此前的页面正文保存在 `research/backups/knowledge-presentation-2026-10-04/`。构建后可运行 `.venv/Scripts/python.exe research/check-knowledge-presentation.py`，检查统一导航、栏目内链接及图示路径。
