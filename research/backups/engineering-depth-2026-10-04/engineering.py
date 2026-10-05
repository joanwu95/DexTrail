"""Responsive engineering illustrations; prose and evidence stay in Markdown.

All labels are HTML so they remain readable on narrow screens. Schematics are
conceptual, not CAD or measurements. Unknown markers fail the build.
"""
from html import escape
import re


def drawing(body):
    return f'<svg viewBox="0 0 320 160" aria-hidden="true" focusable="false">{body}</svg>'


def path(d, kind='structure'):
    return f'<path d="{d}" class="eng-{kind}"/>'


def joint(x, y, passive=False):
    return f'<circle cx="{x}" cy="{y}" r="8" class="eng-joint{" eng-passive" if passive else ""}"/>'


def panel(label, title, description, geometry='', note=''):
    return ('<article class="eng-panel"><div class="eng-panel-head"><span>' + escape(label)
            + '</span><h3>' + escape(title) + '</h3></div><p>' + escape(description)
            + '</p>' + geometry + (f'<p class="eng-panel-note">{escape(note)}</p>' if note else '') + '</article>')


def panels(*items):
    return '<div class="eng-panels">' + ''.join(items) + '</div>'


def flow(items):
    return '<ol class="eng-flow">' + ''.join(f'<li><span>{i:02}</span><strong>{escape(title)}</strong><p>{escape(detail)}</p></li>' for i, (title, detail) in enumerate(items, 1)) + '</ol>'


def mechanism():
    base = path('M24 122H86L157 90L239 44') + joint(86, 122) + joint(157, 90)
    a = drawing(base + path('M61 143Q56 110 95 105M95 105l-12-2m12 2-7 10', 'motion') + path('M137 113Q124 80 159 70M159 70l-12-2m12 2-7 10', 'motion'))
    b = drawing(path('M24 122H86L157 90L239 44') + joint(86, 122) + joint(157, 90) + path('M37 138H86L158 103L250 55', 'force') + path('M242 33V100', 'constraint'))
    c = drawing(base + path('M86 108V70Q113 38 157 65V77', 'constraint'))
    return panels(panel('A', '分别驱动', '两处关节运动可分别指定；仍受关节范围限制。', a, '蓝色箭头：独立运动方向。'), panel('B', '一个输入，接触后适应', '腱绳拉动多关节；遇到物体后，姿态由接触与弹性共同决定。', b, '陶土色：腱绳；右侧虚线：物体表面。'), panel('C', '运动耦合', '机构关系约束两个角度；第二个角度不能任意指定。', c, '虚线连接两关节：存在角度约束，不表示具体传动零件。'))


def contacts():
    obj = '<circle cx="160" cy="80" r="40" class="eng-object"/>'
    two = drawing(obj + path('M20 80H120M200 80H300') + path('M96 80H128m-9-6 9 6-9 6M224 80H192m9-6-9 6 9 6', 'force') + path('M160 80V141m-6-9 6 9 6-9', 'motion'))
    three = drawing(obj + path('M20 108L123 98M263 25L187 52M264 135L192 102') + ''.join(f'<circle cx="{x}" cy="{y}" r="5" class="eng-contact"/>' for x, y in [(124,98),(186,51),(193,101)]) + path('M207 102L228 134', 'constraint'))
    return panels(panel('A', '相对捏取', '两侧接触通过摩擦支持物体。能否抗旋转还取决于接触模型。', two, '横向陶土色箭头：法向夹力；蓝色向下：重力。'), panel('B', '换指与备用接触', '一个接触退出时，其他接触需要继续承担物体的力与力矩。', three, '点表示接触位置；虚线表示正在离开的手指。'))


def skin():
    surface = drawing('<rect x="34" y="43" width="252" height="20" rx="8" class="eng-skin"/><rect x="34" y="64" width="252" height="51" rx="5" class="eng-object"/>' + path('M160 10V52m-6-9 6 9 6-9', 'force') + ''.join(f'<circle cx="{x}" cy="{y}" r="4" class="eng-contact"/>' for y in [82,99] for x in range(65,270,35)))
    return panels(panel('A', '接触引起皮肤变形', '弹性表面把压力或剪切转换为形变。下面的敏感单元读取变化。', surface, '示意一种阵列结构；不同传感原理的层结构不同。'), panel('B', '信号不等于最终结论', '每一步都需要相应的标定或模型。', flow([('原始信号', '电容 / 电阻 / 磁场 / 图像'), ('接触量', '压力、形状或力的估计'), ('任务判断', '接触位置、滑动、抓取状态')])) )


def placement():
    finger = drawing(path('M50 125H127L191 78L265 44') + joint(127,125) + joint(191,78) + '<ellipse cx="262" cy="47" rx="18" ry="10" transform="rotate(-24 262 47)" class="eng-skin"/>' + path('M144 121L188 89M211 79L243 64', 'skin-line') + '<rect x="56" y="116" width="59" height="14" rx="6" class="eng-skin"/>')
    return panels(panel('A', '触觉覆盖接触表面', '指尖用于局部精细接触；指腹、指节与掌面用于包覆接触。', finger, '蓝色区域：触觉覆盖示意，不代表某款产品的配置。'), panel('B', '负载测量沿驱动链路布置', '电机、腱绳、关节和腕部可测不同位置的负载。', flow([('驱动 / 腱绳', '电流、张力'), ('关节 / 指根', '力矩或合力'), ('腕部', '整手合力与合力矩')]), '这些读数不能直接给出每个接触点的压力分布。'))


def transmission():
    gear = drawing('<rect x="30" y="66" width="55" height="45" rx="6" class="eng-object"/>' + '<circle cx="120" cy="88" r="18" class="eng-joint"/><circle cx="158" cy="88" r="28" class="eng-joint"/>' + path('M84 88H102M158 88L251 41') + path('M132 51Q171 35 184 72', 'motion'))
    tendon = drawing('<rect x="23" y="90" width="49" height="40" rx="6" class="eng-object"/>' + path('M72 111H132L207 63L283 90') + joint(132,111) + joint(207,63) + path('M49 96H128L204 47L286 75', 'force'))
    links = drawing(path('M26 126H95L172 87L250 46M95 126L125 83L205 44L250 46M125 83L172 87') + ''.join(joint(x,y) for x,y in [(95,126),(125,83),(172,87),(205,44),(250,46)]))
    elastic = drawing(path('M24 95H81l8-12 13 24 13-24 13 24 13-24 9 12H188L263 46') + joint(188,95) + path('M74 128H155', 'force'))
    return panels(panel('A', '齿轮 / 减速器', '轴转动通过齿轮传到关节；减速比改变速度与力矩。', gear), panel('B', '腱绳 / 滑轮', '卷线轮收放绳索，张力通过力臂产生关节力矩。', tendon), panel('C', '连杆 / 闭链', '杆件与铰链建立关节之间的几何关系。', links), panel('D', '弹性元件参与传力', '弹簧可与腱绳或齿轮组合；形变是传动状态的一部分。', elastic))


def planning():
    return flow([('定义任务', '物体去哪、接触在哪里'), ('求可达姿态', '指尖位置 + 必要朝向 → 关节角'), ('规划接触与路径', '避碰、滚动、换指与关节限制'), ('安排运动时间', '速度、加速度与同步'), ('反馈执行', '跟踪动作并更新接触状态')])


def control():
    return flow([('设定目标', '指尖运动、接触力或柔顺性'), ('比较误差', '目标 − 已测量 / 已估计状态'), ('计算命令', '控制器 + 模型 + 输出限幅'), ('驱动手指', '硬件实际支持的位置 / 速度 / 力矩接口'), ('观测接触', '关节、触觉、力传感返回下一周期')]) + '<p class="eng-feedback"><span>闭环返回</span>最后一步的观测回到“比较误差”；滑动和物体姿态也可更新目标。</p>'


def force():
    fig = drawing('<rect x="122" y="35" width="76" height="79" rx="6" class="eng-object"/>' + path('M26 67H119m-10-6 10 6-10 6M294 67H201m10-6-10 6 10 6', 'force') + path('M128 106V47m-6 9 6-9 6 9M192 106V47m-6 9 6-9 6 9M160 80V145m-6-9 6 9 6-9', 'motion'))
    return panels(panel('A', '两指竖直夹持的简化模型', '两侧法向夹力相等；向上的摩擦力共同抵消重力。', fig, '陶土色：每侧夹力 N；蓝色：向上摩擦力与向下重力 mg。'), panel('B', '抓力要落在可行区间', '先求抗滑下限，再检查物体与硬件允许的上限。', '<div class="eng-force-band"><span>过小：可能滑落</span><strong>稳定且不过载</strong><span>过大：损伤 / 超限</span></div>', '下限高于上限时，需要改变接触、垫材、支撑或动作。'))


def validation():
    return flow([('固定版本与单位', '模型、驱动模式、周期与传感配置'), ('测单个环节', '角度、迟滞、力与延迟'), ('验证接触动作', '轻触 → 保持 → 小范围滑动 / 转动'), ('验证完整任务', '重复次数、失败原因、峰值力与姿态误差')])


DIAGRAMS = {
    'actuation': ('能动多少，与能独立命令多少，是两个问题', mechanism),
    'contacts': ('看接触布局与换指过程，而不是只数手指', contacts),
    'skin': ('触觉从接触变化到任务信息', skin),
    'placement': ('表面覆盖与负载测量补充不同信息', placement),
    'transmission': ('四种传力关系的概念示意', transmission),
    'planning': ('从物体任务到手指轨迹', planning),
    'control': ('控制目标通过反馈闭环实现', control),
    'force': ('需要多大夹力：先说明接触与负载', force),
    'validation': ('把可计算的模型变成可检验的结果', validation),
}


def render(key):
    if key not in DIAGRAMS:
        raise ValueError(f'工程图解不存在：{key}')
    title, content = DIAGRAMS[key]
    return '<div markdown="0" class="eng-figure"><p class="eng-figure-title">' + escape(title) + '</p>' + content() + '<p class="eng-caption">概念示意 · 非产品结构图；尺寸、角度与箭头长度不表示数值。</p></div>'


def on_page_markdown(markdown, page, config, files):
    if not page.file.src_uri.startswith('engineering/'):
        return markdown
    return re.sub(r'<!-- engineering:diagram ([a-z-]+) -->', lambda match: render(match[1]), markdown)
