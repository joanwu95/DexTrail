# 概念索引：去重、自动播放与排版整理

2026-10-05，使用 frontend-design-pro，沿用暖纸、炭黑、砖红及共享右侧标签栏。

## 最终行为

- 导航下方的大标题已去掉；保留屏幕阅读器使用的隐藏 H1。
- 左侧双语术语目录，中间为当前条目的标题、定义、图解与来源，右侧为分类和图解形式筛选。删除顶部重复的分类横栏。
- 分类与形式可组合筛选，搜索支持中文、英文与关节缩写；状态保存在 URL，相关概念、上/下一项及浏览器返回继续有效。
- 18 张 GIF 在条目打开时自动播放，文件自身无限循环；无需点击播放，系统的减少动态偏好也不会覆盖用户明确要求。用户可手动暂停并恢复。切换条目时停止隐藏的 GIF，再次打开仍自动播放。
- 无 JavaScript 时仍能阅读全部 31 个条目，GIF 也直接加载并循环。
- 手机目录默认收起；右侧标签改为使用网站已有的筛选抽屉。

## 全部图版

网页引用 `website/docs/images/knowledge/concept-diagrams/`：31 个 PNG、24 个 SVG、18 个 GIF。原有独立图版保留，便于其他文章使用。

`scripts/render-concept-diagrams.py` 从已有几何绘图代码画出 30 个新网页图版，不读取或修改原有位图。去掉品牌页眉、整幅图的术语标题、中文解释页脚和来源页脚。保留关节、受力、接触、坐标、公式与运动阶段等必要标注。GIF 采用所有帧的共同绘图范围，避免画布跳动或截断。检查时发现欠驱动首阶段的一行标注与连杆重叠，已拆成两行。

关节说明图使用内置 imagegen 编辑，已逐项目视核对五指、指骨与 15 个关节缩写。最终保存为 `website/docs/images/knowledge/concept-diagrams/hand-anatomy.png`。提示词：

> Edit this anatomy diagram for embedding in an existing technical website. Preserve the complete hand diagram, every finger label, every phalanx label, every joint acronym, every leader, and the entire right joint nomenclature column exactly as provided. Preserve the flat charcoal / brick red linework on warm paper #f4f1ea. Remove only the redundant top editorial header (DEXTRAIL / ANATOMY 01, Finger segments & joints, Five-finger hand · anatomical nomenclature and the top horizontal rule). Remove only the tiny bottom-right two-line footer starting Schematic anatomy and Terminology. Make the background uniform #f4f1ea without any texture, shading, or light effects. Recompose the existing content vertically to reduce the vacated top white space, with about 24px outer margin, keeping all diagram and legend labels intact, spelled correctly and clearly legible. No new title or decorative text. Do not remove Proximal / Distal / Thumb explanations within the right column. Output a landscape diagram.

## 检查

- 检查 31 个图版的总览及全部 18 个动画的六阶段接触表；记录位于 `research/previews/concept-index-refresh-2026-10-05/`。
- 验证 31 个 PNG 可解码、18 个 GIF `loop=0`，每帧画布相同，循环时长 6.4 或 7.68 秒；`asset-audit.json` 记录详情。
- 浏览器逐项打开全部 31 个目录链接：只显示一个条目，图片全部加载，18 个动图全部默认播放。
- 分类与形式组合筛选、MCP 搜索、无结果与清除、暂停与恢复通过。
- 1440 × 1000 桌面和 390 × 844 手机截图检查；手机无横向溢出，标签抽屉筛选并关闭后 GIF 继续播放。
- 两项概念栏目测试覆盖资产清单、来源、默认 GIF 和 Markdown 转换后 31 个条目及右侧标签栏仍在页面容器内；原有 knowledge 测试 25 项通过，JS 语法检查与 MkDocs 构建通过。
