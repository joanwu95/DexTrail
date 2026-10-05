# 技术路线图解优化

2026-10-05。应用 frontend-design-pro，沿用 DexTrail 的暖纸、炭灰、砖红配色和现有栏目结构。

## 交付

- `website/hooks/route_diagrams.py`：重画技术路线首页全部 12 组图解。指节改为渐收圆角轮廓，关节、滑轮、接触与传力线分别表示；拇指对掌采用完整手掌；腱索与模块传动改为机构图；信息流程采用线图图标、步骤编号和轻量连接。
- `website/docs/stylesheets/technology-routes.css`：移除蓝色元素、白色圆角框与大面积填色，统一线宽、字号、分栏与窄屏布局。
- `website/hooks/technology_routes.py`：让两篇深入文章复用同一套图解；HTML 标签按行输出，保持 MkDocs 的阅读容器完整。
- `website/docs/technologies/tendon-driven.md`、`underactuation-and-synergies.md`：替换旧图解引用。
- `scripts/preview-route-figures.py`：一次导出全部图解的内部审阅稿，不加入网站导航。

图解仍是教学模型，来源和版本边界保留在 `data/technology-routes.json` 与文章的证据区。没有新增产品性能结论，也没有把概念传动示意当作产品内部结构。

## 验证与修正

- 修正视触觉剖面中物体与弹性表面脱离的问题。
- 修正对掌图中食指穿过物体的问题。
- 反馈流程显示从最后观测阶段返回第二个处理/决策阶段的路径。
- MkDocs 完整生产构建通过。此前其他同步修改的资料与页面暂缺，待其写入后构建完成；未保留对相关加载器的临时修改。
- 技术路线测试 3 项通过，知识栏目测试 25 项通过。
- 新增回归检查：两篇文章的两张子图及后续正文必须保持在阅读容器内部，防止 Markdown 与内嵌 SVG 边界导致样式丢失。
- 实际浏览器逐项切换 12 组图解，390px 手机视口全部无横向溢出，路径无 NaN/Infinity。
- 检查桌面、手机以及两篇深入文章的真实页面。
- 原图解源码与 CSS 已保存到 `research/backups/route-figures-2026-10-05/`。
- 实际页面截图：`research/previews/route-figures-2026-10-05/desktop.jpg`。
