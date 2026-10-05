# DexTrail 抓取概念图版

日期：2026-10-04。

这组素材供已有网页按需嵌入，没有新增网站页面或导航。共 24 张独立图版，其中 12 张以静态图说明关系，12 张另外提供 GIF 展示过程。所有图版均提供 PNG 和 SVG，GIF 同时有静态对应图。英文概念名为主标题，中文简要解释放在图下。

## 文件与格式

- 目录：`website/docs/images/knowledge/grasp-concepts-dextrail/`
- [全部素材 ZIP](../../website/docs/images/knowledge/grasp-concepts-dextrail/grasp-concepts-dextrail.zip)
- [24 张图版总览](../../website/docs/images/knowledge/grasp-concepts-dextrail/grasp-concepts-overview.png)
- [资产清单、中文替代文本与来源](../../website/docs/images/knowledge/grasp-concepts-dextrail/manifest.json)
- [生成脚本](../../scripts/render-grasp-concepts.py)
- 尺寸：960 × 720。动画：80 个原始帧，80 ms/帧，循环 6.4 秒；GIF 编码可合并相同的连续帧，但保留总时长。
- PNG 可直接用于 Markdown；SVG 适合缩放或后续编辑；GIF 用于过程说明。网站支持减少动画偏好时，应使用同名 PNG 替代 GIF。

每个 SVG 内含 `title` 与中文 `desc`，清单提供适用于网页 `img` 的中文 `alt`。SVG 使用 Segoe UI、Microsoft YaHei 字体栈，不嵌入字体。

## 静态关系图

| 术语 | 素材 | 选用静态图的原因 |
| --- | --- | --- |
| Form closure / 形封闭 | [PNG](../../website/docs/images/knowledge/grasp-concepts-dextrail/form-closure.png) · [SVG](../../website/docs/images/knowledge/grasp-concepts-dextrail/form-closure.svg) | 观察固定接触位置、法向与平移/转动约束。 |
| Force closure / 力封闭 | [PNG](../../website/docs/images/knowledge/grasp-concepts-dextrail/force-closure.png) · [SVG](../../website/docs/images/knowledge/grasp-concepts-dextrail/force-closure.svg) | 同时观察摩擦锥与可抵抗的受力方向。 |
| Friction cone / 摩擦锥 | [PNG](../../website/docs/images/knowledge/grasp-concepts-dextrail/friction-cone.png) · [SVG](../../website/docs/images/knowledge/grasp-concepts-dextrail/friction-cone.svg) | 对比锥内与锥外的静态力需求。 |
| Antipodal grasp / 对向抓取 | [PNG](../../website/docs/images/knowledge/grasp-concepts-dextrail/antipodal-grasp.png) · [SVG](../../website/docs/images/knowledge/grasp-concepts-dextrail/antipodal-grasp.svg) | 对比接触连线与两摩擦锥的位置关系。 |
| Contact models / 接触模型 | [PNG](../../website/docs/images/knowledge/grasp-concepts-dextrail/contact-models.png) · [SVG](../../website/docs/images/knowledge/grasp-concepts-dextrail/contact-models.svg) | 并列比较三类接触允许的力/力矩分量。 |
| Wrench / 力旋量 | [PNG](../../website/docs/images/knowledge/grasp-concepts-dextrail/wrench.png) · [SVG](../../website/docs/images/knowledge/grasp-concepts-dextrail/wrench.svg) | 说明作用点、参考点、力与力矩之间的关系。 |
| Grasp matrix / 抓取矩阵 | [PNG](../../website/docs/images/knowledge/grasp-concepts-dextrail/grasp-matrix.png) · [SVG](../../website/docs/images/knowledge/grasp-concepts-dextrail/grasp-matrix.svg) | 展示接触布局与具体矩阵的对应。 |
| Internal force / 抓取内力 | [PNG](../../website/docs/images/knowledge/grasp-concepts-dextrail/internal-force.png) · [SVG](../../website/docs/images/knowledge/grasp-concepts-dextrail/internal-force.svg) | 对比夹持内力大小，保持其合力旋量为零。 |
| Grasp wrench space / 抓取力旋量空间 | [PNG](../../website/docs/images/knowledge/grasp-concepts-dextrail/grasp-wrench-space.png) · [SVG](../../website/docs/images/knowledge/grasp-concepts-dextrail/grasp-wrench-space.svg) | 将接触和力预算与可行受力集合联系起来。 |
| Grasp quality / 抓取质量 | [PNG](../../website/docs/images/knowledge/grasp-concepts-dextrail/grasp-quality.png) · [SVG](../../website/docs/images/knowledge/grasp-concepts-dextrail/grasp-quality.svg) | 比较同一归一化下的最不利抗扰余量。 |
| Power / precision / intermediate grasp | [PNG](../../website/docs/images/knowledge/grasp-concepts-dextrail/grasp-types.png) · [SVG](../../website/docs/images/knowledge/grasp-concepts-dextrail/grasp-types.svg) | 并列展示包握、指尖捏取与侧向捏持。 |
| Virtual finger / 虚拟手指 | [PNG](../../website/docs/images/knowledge/grasp-concepts-dextrail/virtual-finger.png) · [SVG](../../website/docs/images/knowledge/grasp-concepts-dextrail/virtual-finger.svg) | 用同一握持姿态说明功能分组。 |

## 动态过程图

| 术语 | 动画 | 运动中需要观察的内容 |
| --- | --- | --- |
| Caging / 笼式约束 | [GIF](../../website/docs/images/knowledge/grasp-concepts-dextrail/caging.gif) | 物体可在围笼内活动，开口却不能容许它逃脱。 |
| Equilibrium & stability / 平衡与稳定性 | [GIF](../../website/docs/images/knowledge/grasp-concepts-dextrail/equilibrium-stability.gif) | 相同初始平衡下，受扰并释放后是否恢复。 |
| In-hand manipulation / 手内操作 | [GIF](../../website/docs/images/knowledge/grasp-concepts-dextrail/in-hand-manipulation.gif) | 物体相对固定手掌转动，多指协同跟随。 |
| Finger gaiting / 指间换步 | [GIF](../../website/docs/images/knowledge/grasp-concepts-dextrail/finger-gaiting.gif) | 一指离开、换位、重新接触；其余接触支撑物体。 |
| Rolling / 滚动 | [GIF](../../website/docs/images/knowledge/grasp-concepts-dextrail/rolling.gif) | 物体平移与转动同时发生，接触处无相对滑动。 |
| Sliding / 滑动 | [GIF](../../website/docs/images/knowledge/grasp-concepts-dextrail/sliding.gif) | 物体相对指腹移动，方向标记保持不变。 |
| Pivoting / 绕支点转动 | [GIF](../../website/docs/images/knowledge/grasp-concepts-dextrail/pivoting.gif) | 支点位置不动，物体围绕支点转动。 |
| Compliance / 顺应性 | [GIF](../../website/docs/images/knowledge/grasp-concepts-dextrail/compliance.gif) | 加载后让位，卸载后恢复。 |
| Impedance control / 阻抗控制 | [GIF](../../website/docs/images/knowledge/grasp-concepts-dextrail/impedance-control.gif) | 在虚拟质量—弹簧—阻尼关系下响应扰动。 |
| Underactuation / 欠驱动 | [GIF](../../website/docs/images/knowledge/grasp-concepts-dextrail/underactuation.gif) | 一个输入驱动多个关节，接触改变运动分配。 |
| Postural synergy / 姿态协同 | [GIF](../../website/docs/images/knowledge/grasp-concepts-dextrail/synergy.gif) | 一个示例协同变量同时组织多个关节姿态。 |
| Adaptive synergy / 自适应协同 | [GIF](../../website/docs/images/knowledge/grasp-concepts-dextrail/adaptive-synergy.gif) | 一侧先接触后停留，其他顺应分支继续适应物体。 |

以上动画均有同名 `.png` 和 `.svg`。`*-review.png` 为六帧检查图，不需要嵌入网页。[第 1 组预览](../../website/docs/images/knowledge/grasp-concepts-dextrail/grasp-concepts-sheet-01.png)、[第 2 组预览](../../website/docs/images/knowledge/grasp-concepts-dextrail/grasp-concepts-sheet-02.png)、[第 3 组预览](../../website/docs/images/knowledge/grasp-concepts-dextrail/grasp-concepts-sheet-03.png)、[第 4 组预览](../../website/docs/images/knowledge/grasp-concepts-dextrail/grasp-concepts-sheet-04.png)。

## 证据与教学模型边界

- 形封闭与力封闭依据 [Modern Robotics：形封闭](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-1-7-form-closure/)和[力封闭](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-2-3-force-closure/)。图中为平面刚体模型。力封闭的方向条件并不意味着实际驱动器能够承受无限载荷，也不把平面双点接触的结论直接推广到空间双点接触。
- 摩擦锥依据 [Modern Robotics：摩擦](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-2-1-friction/)。对向抓取与内力依据 [UC Berkeley 抓取讲义](https://pages.github.berkeley.edu/EECS-106/sp22-site/assets/scribe_notes/scribe_lec_9A.pdf)。内力图只显示内力分量，省略外部载荷。
- Caging 采用完全笼式约束的平面例子，依据 [Mahler et al.](https://goldberg.berkeley.edu/pubs/Cage-Grasp-Synthesis-WAFR-accepted-Dec-2016.pdf)。圆盘直径大于固定开口宽度；没有用“完全不动”解释笼式约束。
- 接触模型、抓取矩阵、力旋量和质量指标依据 [Multi-Fingered Robotic Grasping: A Primer](https://arxiv.org/pdf/1607.06620)。软指接触的附加力矩绕接触法向，不表示接触可任意传递所有方向的力矩。
- GWS 图采用对向接触位于 `(-a,0)` 与 `(a,0)`、每指法向力在 `[0,1]`、摩擦系数 `0.5` 的平面模型。展示的是 `Mz=0` 切片：零力矩要求两接触的切向力相等，由此得到 `|Fx|≤1`、`|Fy|≤2μ(1−|Fx|)=1−|Fx|` 的菱形。它不是完整空间六维 GWS。质量图是两个示意的归一化二维截面；显示原点中心内切圆的余量，不声称它就是某个真实抓取的完整六维 Ferrari–Canny 分数。
- 抓取姿态和虚拟手指依据 [Feix et al. 的 GRASP taxonomy](https://www.eng.yale.edu/grablab/pubs/Feix_THMS2016.pdf)。侧向捏持在本分类中属于 intermediate grasp；不同分类存在差异。
- 手内操作和换步依据 [Shi et al. 的手内操作论文](https://robotics.northwestern.edu/documents/publications/dynamic-in-hand-sliding-manipulation-tro.pdf)。换步例子为平面教学模型，两个保留接触对向支撑；假设其摩擦和施力足以维持物体。
- 滚动与滑动的接触条件另见 [Modern Robotics：Contact Types](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-1-2-contact-types-rolling-sliding-and-breaking/)。滚动动画严格使用 `dx=R dθ`；滑动动画保持物体方向固定。绕支点转动保持支点固定。它们都是运动学教学例子，不是完整动力学仿真。
- 顺应性和阻抗关系依据 [DLR Hand II](https://www.robotic.dlr.de/fileadmin/robotic/borst/BorstEtAl-ICRA03-HandApplications.pdf)。稳定性与阻抗动画使用释放时速度为零的阻尼振子解析响应，图中控制器只是期望关系的说明，不是实现后的闭环控制性能报告。中性平衡与渐近稳定有不同的恢复行为；不能将中性平衡简单称为不稳定。
- 欠驱动、协同和自适应协同依据 [Pisa/IIT SoftHand 论文记录](https://arpi.unipi.it/handle/11568/507072)。图中机构、协同参数与接触顺序是解释概念的绘图选择，不是复现该产品传动，也不是从人手数据提取的第一主协同。

## 绘图与再生成

继续应用 `frontend-design-pro`，以现有网页主题为依据。纸色 `#f4f1ea`、炭灰 `#292b29`、砖红 `#aa4d3e`；其余为同色系浅色。无阴影、打光、纹理、渐变或写实渲染。线宽、虚线、标记和英文标签分别承担结构、参考、接触与术语说明。

图版由新几何绘图生成，不对已有手部栅格图做像素编辑。图像、矢量与动画使用同一组绘图函数。

使用包含 Pillow 的 Python，运行 `scripts/render-grasp-concepts.py`。`--preview` 生成静态预览；`--only slug [slug ...]` 更新选定图版。脚本在当前项目内读取 `website/docs/stylesheets/theme.css`，字体来自 Windows 字体目录。

## 已执行核查

- 24 个 PNG 均可解码，尺寸为 960 × 720；24 个 SVG 均可解析，含标题和中文说明。浏览器检查了 SVG 窄窗口缩放和 GIF 直接显示。
- 解码 12 个 GIF 的全部帧，确认无限循环和 6400 ms 总时长。编码后合并相同帧的图版仍保留完整循环时长。
- 确认形封闭示例的法向力旋量矩阵秩为 3，存在全正零空间向量；对向摩擦接触的锥边力旋量满足相应平面力封闭条件。
- 独立构造 GWS 切片边界上的可行接触力，确认法向力预算、摩擦界和零力矩条件同时成立。
- 采样实际绘图几何，确认手内操作及换步的各段长度固定，换步时另两支撑接触保持不动；阻抗图的手指连杆长度固定；欠驱动图接触后的近端停止、远端继续运动。
- 确认滚动满足无滑动位移/转角关系，笼内圆盘轨迹与边界不穿透，阻尼解析响应满足零初始释放速度和相应振子方程。
- 检查 24 张静态代表帧的文字包围盒，无文字越界或相互重叠；动画生成逐帧检查文字边界。用六帧接触表检查过程中的形态和标注。
- ZIP 完整性检查通过，含 60 个独立媒体文件、总览、清单和说明，共 63 个文件。

来源、替代文本和每个图版的模型范围同步保存在清单中。以上检查不等于真实机器人动力学或接触控制性能验证。
