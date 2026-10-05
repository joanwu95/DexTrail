# 期刊与会议节点收录复核（2026-10-04）

本轮新增 14 条，领域发展合计 59 条。筛选目标是补充技术问题和关注点的变化，不将期刊声望、引用次数或入选本页等同于公认突破。正文只保留方案摘要；原文标题、时间口径、收录解读和证据边界放入“背景与来源”。

| 节点日期 | 论文／出处 | 收录目的 |
| --- | --- | --- |
| 1988-06 | Montana, The Kinematics of Contact and Grasp · IJRR | 接触几何与滚动操作的基础 |
| 2000 | Okamura et al., An Overview of Dexterous Manipulation · ICRA | 接触、规划、控制的整体问题框架 |
| 2000-12 | Bicchi, Hands for Dexterous Manipulation and Robust Grasping · IEEE T-RA | 灵巧、稳健、易用与简化设计的取舍 |
| 2010-02-02 | Dollar & Howe, The Highly Adaptive SDM Hand · IJRR | 被动柔顺吸收抓握误差 |
| 2012-09-10 | Bullock et al., A Hand-Centric Classification · IEEE Transactions on Haptics | 描述与区分操作任务 |
| 2016-10 | Gupta et al., Learning Dexterous Manipulation for a Soft Robotic Hand · IROS | 物体中心示范与软手学习 |
| 2018-06 | Rajeswaran et al., Learning Complex Dexterous Manipulation with Deep Reinforcement Learning and Demonstrations · RSS | 多任务仿真及示范帮助策略学习 |
| 2020-05-01 | Handa et al., DexPilot · ICRA | 视觉遥操作与示范采集 |
| 2020-07-08 | Li et al., A Review of Tactile Information · T-RO | 触觉信号到物体理解与动作 |
| 2022-01-20 | Morgan et al., Compliance-Enabled Finger Gaiting · RA-L | 柔顺、换指与接触规划 |
| 2023-08-21 | Sieler & Brock, Dexterous Soft Hands Linearize Feedback-Control · IROS | 软机构、形变状态与反馈控制 |
| 2023-11 | Qi et al., General In-hand Object Rotation with Vision and Touch · CoRL | 多模态感知与多轴旋转 |
| 2025-12-29 | Li et al., The Developments and Challenges Toward Dexterous and Embodied Robotic Manipulation · IEEE RAM | 近期数据与学习研究的整体视角 |
| 2026-02-18 | Lepora, Tactile robotics: Past and future · IJRR | 触觉历史、关注点变化与作者展望 |

原始来源 URL、定位和核验范围均在 `data/field-development.json` 的 sources 中；每条事件记录标签对应的本节点来源。

## 时间与类型

- Bullock 分类论文原文页脚注明在线发表 2012-09-10，卷期为 2013 年 4–6 月。本页采用在线日期；不能仅凭 PDF 文件名写成 2013 年首发，也不能误标为 T-RO。
- IEEE RAM 综述的 IEEE 元数据注明首次发表 2025-12-29，编入 33(1)，2026-03。官网文章推介日期 2026-04-17 与预印本首版 2025-07-16 均不替代该节点的在线发表日期。
- T-RO 触觉综述在线发表 2020-07-08，卷期为 2020-12。作者机构 PDF 与 IEEE 元数据共同支撑内容和日期。
- Morgan 作者稿写明 RA-L 录用 2022-01-06；该日期不是出版日期。本节点采用可核对的 arXiv 首版 2022-01-20，并显示 RA-L 出处。
- Sieler 预印本作者注明 accepted at IROS 2023；节点采用首版日期，不把录用说明当作正式出版时间。
- DexPilot 的作者机构页明确 ICRA 2020；Gupta 软手示范学习的作者列表明确 IROS 2016，两者没有互换会议。
- Bicchi 2000 年论文当时期刊名称为 IEEE Transactions on Robotics and Automation（T-RA）。保留历史名称。
- ICRA 2000 概述和 T-RO 2020 综述的 Review 是内容类型，不声称它们属于期刊 Focus／Viewpoint 栏目。
- IJRR 的 Tactile robotics: Past and future 在出版社页面被标为 Research article。保留正式类型，以“领域观点”主题标签表达其历史回顾与展望内容。

## 去重与本轮未收录

- 已有 SoftHand、LEAP、DexCap、DexUMI 等成果，不另加同一成果的会议／期刊版本。SoftHand 的 Adaptive synergies 论文核对为 IJRR，补充出处展示；不是 T-RO。
- 与物体抓取整体相关、主要讨论其他末端执行器的综述可以作为背景资料；本轮优先补多指接触、手内操作、软手、触觉和示范学习，未为覆盖每个会议而增加条目。
- DOGlove 可核对预印本及技术方案，但本轮尚未核实拟标注的 RA-L 出处，因此不以 RA-L 论文身份新增。
- T-RO 的 Tactile Robotics 专题征稿页能证明专题方向，但它是征稿／专题页面，不能直接冒充已发表的观点论文或以征稿时间当作技术突破。
- 历史综述引用的分期和商业化展望归属于作者，不将其写成整个灵巧手产业已经确认的发展阶段。

## 复核范围

Montana、RotateIt、DAPG、DexPilot、IEEE RAM 的概括依据公开摘要与元数据。其余原文阅读范围见来源定位。未复现实验，未以综述替代单个系统的能力证据。

完成 16 项领域发展与页面呈现测试、MkDocs strict 构建及全站检查：199 页导航和声明、85 个产品详情、59 条带标签的时间轴节点。浏览器验证“领域观点”筛选得到 9/59 条，新增出处类型及展开区日期与来源均可读。截图保存于 `research/previews/venue-development-2026-10-04/recent-discussion-nodes.png`。
