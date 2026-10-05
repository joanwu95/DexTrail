"""Responsive engineering illustrations; prose and evidence stay in Markdown.

All labels are HTML so they remain readable on narrow screens. Schematics are
conceptual, not CAD or measurements. Unknown markers fail the build.
"""
from html import escape
import importlib.util
from math import atan2, cos, degrees, hypot, pi, sin
from pathlib import Path
import re

_tendon_spec = importlib.util.spec_from_file_location('tendon_materials', Path(__file__).with_name('tendon_materials.py'))
tendon_materials = importlib.util.module_from_spec(_tendon_spec)
_tendon_spec.loader.exec_module(tendon_materials)


def drawing(body, viewbox='0 0 320 190'):
    return f'<svg viewBox="{viewbox}" aria-hidden="true" focusable="false">{body}</svg>'


def path(d, kind='structure'):
    return f'<path d="{d}" class="eng-{kind}"/>'


def joint(x, y, passive=False):
    return (f'<circle cx="{x}" cy="{y}" r="10" class="eng-joint{" eng-passive" if passive else ""}"/>'
            f'<circle cx="{x}" cy="{y}" r="3" class="eng-shaft"/>')


def link(x1, y1, x2, y2, width=18):
    length = hypot(x2-x1, y2-y1)
    angle = degrees(atan2(y2-y1, x2-x1))
    return f'<rect x="0" y="{-width/2}" width="{length}" height="{width}" rx="7" transform="translate({x1} {y1}) rotate({angle})" class="eng-link-body"/>'


def finger(points):
    return ''.join(link(*a, *b) for a, b in zip(points, points[1:])) + ''.join(joint(*point) for point in points[:-1])


def motor(x, y):
    return (f'<rect x="{x}" y="{y}" width="54" height="38" rx="6" class="eng-motor-body"/>'
            + f'<circle cx="{x+27}" cy="{y+19}" r="10" class="eng-joint"/>'
            + path(f'M{x+54} {y+19}h17'))


def number(x, y, value):
    return f'<g class="eng-part-number"><circle cx="{x}" cy="{y}" r="10"/><text x="{x}" y="{y}" dy=".35em" text-anchor="middle">{value}</text></g>'


def parts(labels):
    return '<ol class="eng-part-key">' + ''.join(f'<li><span>{i}</span>{escape(label)}</li>' for i, label in enumerate(labels, 1)) + '</ol>'


def arrow(x1, y1, x2, y2, kind='force'):
    angle = atan2(y2-y1, x2-x1)
    ax, ay = x2-8*cos(angle-.55), y2-8*sin(angle-.55)
    bx, by = x2-8*cos(angle+.55), y2-8*sin(angle+.55)
    return path(f'M{x1} {y1}L{x2} {y2}M{ax:.2f} {ay:.2f}L{x2} {y2}L{bx:.2f} {by:.2f}', kind)


def gear(x, y, radius, teeth=12):
    points=[]
    for i in range(teeth*4):
        r = radius + (3 if i%4 in (1,2) else 0)
        a = 2*pi*i/(teeth*4)
        points.append(f'{x+r*cos(a):.2f},{y+r*sin(a):.2f}')
    return '<polygon points="' + ' '.join(points) + '" class="eng-gear-body"/>' + joint(x,y)


def panel(label, title, description, geometry='', note=''):
    return ('<article class="eng-panel"><div class="eng-panel-head"><span>' + escape(label)
            + '</span><h3>' + escape(title) + '</h3></div><p>' + escape(description)
            + '</p>' + geometry + (f'<p class="eng-panel-note">{escape(note)}</p>' if note else '') + '</article>')


def panels(*items):
    return '<div class="eng-panels">' + ''.join(items) + '</div>'


def flow(items):
    return '<ol class="eng-flow">' + ''.join(f'<li><span>{i:02}</span><strong>{escape(title)}</strong><p>{escape(detail)}</p></li>' for i, (title, detail) in enumerate(items, 1)) + '</ol>'


def mechanism():
    points=[(105,139),(187,92),(276,64)]
    a = drawing(finger(points) + motor(51,130) + motor(161,113) + path('M85 115Q107 92 127 114M127 114l-9-3m9 3-4-8','motion') + path('M163 82Q184 54 208 77M208 77l-9-3m9 3-4-8','motion') + number(55,122,1) + number(190,139,2))
    b = drawing('<rect x="269" y="40" width="32" height="85" rx="9" class="eng-object"/>' + finger(points) + motor(25,112) + path('M53 119H98L182 73L274 48','force') + number(28,104,1) + number(164,62,2) + number(293,36,3))
    c = drawing(finger(points) + motor(51,130) + path('M109 119V80Q148 45 187 72V79','constraint') + number(50,122,1) + number(146,59,2))
    d = drawing('<rect x="28" y="127" width="82" height="29" rx="5" class="eng-link-body"/>' + link(98,141,140,141) + link(140,141,225,80) + joint(140,141,True) + path('M119 127l-9-13 13-3-4-13 12 3-1-14','spring') + arrow(286,58,229,80) + number(99,92,1) + number(277,47,2))
    return panels(panel('A','两个输入分别驱动','两个关节目标可分别设定，运动仍受限位约束。',a+parts(['近端驱动','远端驱动'])), panel('B','一个输入带动两关节','接触后姿态由绳路、弹性和接触共同决定。',b+parts(['卷线驱动','共用腱绳','物体表面'])), panel('C','一个输入、刚性角度耦合','机构约束两个角度的关系，只剩一个独立构型变量。',c+parts(['驱动输入','角度约束（虚线示意）'])), panel('D','未独立驱动的被动关节','外力使关节偏转，弹性元件提供复位作用。',d+parts(['复位弹性','外部接触力'])))


def contacts():
    obj = '<circle cx="160" cy="80" r="40" class="eng-object"/>'
    two = drawing(obj + finger([(34,141),(91,123),(118,83)]) + finger([(286,141),(229,123),(202,83)]) + arrow(92,80,122,80) + arrow(228,80,198,80) + arrow(160,91,160,150,'load') + number(88,57,1) + number(181,142,2))
    three = drawing(obj + finger([(32,132),(95,123),(124,98)]) + finger([(273,25),(225,36),(186,51)]) + link(271,147,235,134) + path('M235 134L193 101','constraint') + ''.join(f'<circle cx="{x}" cy="{y}" r="5" class="eng-contact"/>' for x,y in [(124,98),(186,51)]) + arrow(196,115,233,146,'motion') + number(145,42,1) + number(251,161,2))
    return panels(panel('A','相对捏取','两侧接触通过摩擦支持物体，抗旋转还取决于接触模型。',two+parts(['法向夹力','向下重力'])),panel('B','换指与备用接触','一个接触退出时，其他接触需接替支持。',three+parts(['保留的接触','正在离开的手指']), '虚线为离开过程；蓝色箭头表示运动。'))


def skin():
    cells=''.join(f'<rect x="{x}" y="{y}" width="21" height="13" rx="3" class="eng-taxel"/>' for y in [110,132] for x in range(51,260,34))
    surface = drawing('<rect x="118" y="26" width="86" height="45" rx="10" class="eng-object"/>' + '<path d="M34 75H112Q160 101 209 75H286V99H34Z" class="eng-skin"/>' + '<rect x="34" y="104" width="252" height="53" rx="6" class="eng-board"/>' + cells + arrow(160,3,160,53) + number(265,77,1) + number(281,122,2) + number(81,156,3))
    return panels(panel('A','接触表面与读出结构','物体使弹性表面变形，下方单元读取对应变化。',surface+parts(['可变形接触层','局部敏感单元','支撑与读出结构']), '图示阵列式结构，不代表所有传感原理。'), panel('B','从原始读数到控制信息','物理量估计和任务判断分别需要标定与验证。',flow([('采集原始信号','电容 / 电阻 / 磁场 / 图像'),('标定或重建','压力、形变、几何或力'),('提取时序特征','接触位置与滑动相关变化'),('供控制器使用','与动作、坐标和时间对齐')])) )


def placement():
    hand='<rect x="105" y="117" width="121" height="92" rx="30" class="eng-link-body"/><rect x="131" y="191" width="68" height="34" rx="5" class="eng-link-body"/>'
    for x, tip in [(113,37),(143,18),(173,26),(203,54)]:
        hand += '<rect x="'+str(x)+'" y="'+str(tip)+'" width="23" height="'+str(133-tip)+'" rx="11" class="eng-link-body"/>'
        hand += f'<rect x="{x+3}" y="{tip+4}" width="17" height="20" rx="7" class="eng-skin"/><rect x="{x+4}" y="{tip+35}" width="15" height="24" rx="5" class="eng-skin"/>'
    hand += link(115,168,74,126,25) + link(74,126,58,91,25) + '<ellipse cx="160" cy="161" rx="32" ry="27" class="eng-skin"/>' + number(122,28,1) + number(158,82,2) + number(162,160,3)
    picture=drawing(hand,'0 0 320 235')
    return panels(panel('A','触觉贴在实际接触表面','表面覆盖直接决定哪些接触能被局部观察。',picture+parts(['指尖：精细接触','指腹 / 指节：包覆接触','掌面：支撑与包覆']), '图中覆盖为示意，关节和边缘仍可能有盲区。'),panel('B','负载测量沿驱动链路布置','读取安装处的负载，与局部表面分布互补。',flow([('电机 / 腱绳','电流、张力：驱动与传动侧'),('关节 / 指根','力矩或单指合量'),('腕部','整手的合力与合力矩')]),'合量不能唯一还原多个接触点的压力分布。'))


def transmission():
    gears = drawing(motor(22,91) + gear(108,110,15) + gear(153,110,24) + link(153,110,263,54) + path('M149 65Q185 66 184 98M184 98l-6-8m6 8 5-8','motion') + number(28,81,1) + number(129,66,2) + number(268,47,3))
    tendon = drawing(motor(18,111) + finger([(107,143),(191,95),(277,64)]) + path('M44 117H102L188 76L277 46','force') + number(19,99,1) + number(129,95,2) + number(200,128,3))
    links = drawing(''.join(link(*a,*b,12) for a,b in [((55,147),(112,130)),((112,130),(193,84)),((112,130),(131,82)),((131,82),(217,41)),((193,84),(266,40)),((217,41),(266,40)),((131,82),(193,84))]) + ''.join(joint(*p) for p in [(55,147),(112,130),(193,84),(131,82),(217,41),(266,40)]) + number(46,133,1) + number(139,54,2) + number(277,35,3))
    elastic = drawing(motor(20,102) + path('M91 121H108l8-13 12 26 12-26 12 26 12-26 8 13H200','spring') + link(200,121,277,65) + joint(200,121) + number(22,92,1) + number(145,95,2) + number(265,54,3))
    return panels(panel('A','齿轮与减速传动','旋转经啮合传到输出关节，改变速度和力矩。',gears+parts(['电机','齿轮级','输出指节']), '齿形为示意，图形尺寸不表示实际减速比。'),panel('B','腱绳与滑轮','卷线收放改变腱长，张力通过关节力臂作用。',tendon+parts(['卷线驱动','腱绳路径','关节与滑轮'])),panel('C','连杆与闭链','杆件长度和铰链位置确定输出运动关系。',links+parts(['输入端','约束杆件','输出端']), '拓扑示意，不是经过尺寸综合的机构。'),panel('D','串联弹性元件','弹性形变参与传力，与刚性输出运动共同构成状态。',elastic+parts(['驱动输入','弹性元件','输出指节'])))


def planning():
    return flow([('定义任务', '物体去哪、接触在哪里'), ('求可达姿态', '指尖位置 + 必要朝向 → 关节角'), ('规划接触与路径', '避碰、滚动、换指与关节限制'), ('安排运动时间', '速度、加速度与同步'), ('反馈执行', '跟踪动作并更新接触状态')])


def control():
    return flow([('目标','位置 / 速度 / 接触力 / 柔顺性'),('误差与控制律','将目标与有效反馈比较'),('可用驱动接口','位置 / 速度 / 力矩，输出限幅'),('手指与物体','真实传动、接触和负载')]) + '<div class="eng-loop-return"><strong>← 测量反馈返回误差比较</strong><p>关节与触觉 / 力信号 → 时间与坐标对齐 → 测量或估计状态；接触变化也可能触发目标更新。</p></div>'


def force():
    fig=drawing('<rect x="125" y="42" width="70" height="86" rx="8" class="eng-object"/>' + '<rect x="94" y="69" width="31" height="44" rx="12" class="eng-skin"/><rect x="195" y="69" width="31" height="44" rx="12" class="eng-skin"/>' + link(30,96,109,96,25)+link(211,96,290,96,25) + arrow(76,80,125,80)+arrow(244,80,195,80)+arrow(136,116,136,53)+arrow(184,116,184,53)+arrow(160,105,160,169,'load') + number(65,69,1)+number(148,43,2)+number(179,168,3))
    return panels(panel('A','两指夹持的受力图','每侧法向夹力相同，两侧摩擦力共同支持物体。',fig+parts(['每侧法向夹力 N','向上摩擦力（每侧 ≤ μN）','向下重力 mg'])),panel('B','抓力的可行区间','抗滑下限与物体、传感和驱动上限一起检查。','<div class="eng-force-band"><span>低于下限：支持可能不足</span><strong>满足全部约束的可用区间</strong><span>高于上限：损伤、饱和或驱动超限</span></div>','若区间不存在，需要改变接触、支持或动作。'))


def antagonistic():
    geometry = drawing(motor(24,26)+motor(24,131)+link(220,100,290,78)+joint(220,100)+path('M50 45H119l6-9 8 18 8-18 8 18 8-18 6 9H192Q221 45 235 83','force')+path('M50 150H119l6-9 8 18 8-18 8 18 8-18 6 9H192Q220 151 235 113','force')+number(18,20,1)+number(18,170,2)+number(276,72,3))
    return panels(panel('A','两侧张力共同作用于同一关节','两根腱绳沿相反方向产生力矩，弹性元件参与受载形变。',geometry+parts(['第一侧张力 T₁','第二侧张力 T₂','输出关节与指节'])),panel('B','差动与共同加载','相同净力矩可以对应不同预紧状态。','<div class="eng-equation-pair"><div><strong>张力差 T₁ − T₂</strong><p>恒定相等力臂的模型中，决定净驱动力矩。</p></div><div><strong>共同预紧</strong><p>改变弹性工作点；能否调节刚度取决于实际结构。</p></div></div>','绳索只能承受张力；图不表示具体产品绳路。'))


def pressure_map():
    colors=['#d9e7ed','#b7cedb','#8badc0','#5e879f']
    cells=''
    for i,(x,y) in enumerate([(67,125),(168,125),(67,45),(168,45)]):
        cells += f'<rect x="{x}" y="{y}" width="80" height="56" rx="5" fill="{colors[i]}" stroke="#6d8c9d" stroke-width="1"/>' + number(x+14,y+14,i+1)
    cells += path('M161 97h14m-7-7v14','motion') + path('M177 94L265 20','constraint') + number(277,18,5)
    return panels(panel('A','四单元压力分布算例','各单元面积相同，压力不同；蓝色十字为压力中心。',drawing(cells,'0 0 320 210')+parts(['10 kPa','20 kPa','30 kPa','40 kPa','压力中心（1.2, 1.4）mm']),'深浅表示本算例的压力，不是实际传感器图像。'),panel('B','压力、合力与中心分别计算','先把每个单元的读数换成相同物理单位。',flow([('每单元力','压力 × 有效面积'),('合力','同法向时求和；曲面需变换方向'),('压力中心','用各单元力对位置加权')]),'接触面积中心与压力中心不一定重合。'))


def kinematics():
    geometry = drawing(finger([(52,150),(161,111),(224,65)]) + arrow(52,150,94,150,'motion')+arrow(52,150,52,106,'motion')+arrow(224,65,258,40,'motion')+arrow(224,65,206,39,'motion')+path('M161 111L203 96','constraint')+path('M88 150A36 36 0 0 0 86 138M193 99A34 34 0 0 0 188 89','motion')+number(36,167,1)+number(97,124,2)+number(187,78,3)+number(270,38,4))
    return panels(panel('A','关节角决定指尖位置与朝向','指节长度和关节角给出正运动学；蓝色轴表示局部方向。',geometry+parts(['掌部坐标原点','近端角 q₁','相对关节角 q₂','指尖局部坐标']), '图示一般姿态，不对应正文数值的比例。'),panel('B','反过来求可行关节角','先选必须满足的位置与朝向，再处理解和约束。',flow([('任务目标','接触位置、必要法向与坐标系'),('逆运动学','求满足目标的关节角解'),('可行性检查','限位、耦合、碰撞与奇异位形')]),'可达位置、可达朝向和可执行路径要分别检查。'))


def trajectory():
    axes=arrow(42,150,289,150,'structure')+arrow(42,150,42,26,'structure')
    left=drawing(axes+path('M65 132C94 120 85 69 148 76S212 38 267 41','motion')+number(64,132,1)+number(267,41,2)+'<text x="287" y="174" class="eng-axis-label">q₁</text><text x="17" y="30" class="eng-axis-label">q₂</text>')
    pts=' '.join(f'{62+206*i/30:.2f},{135-94*(3*(i/30)**2-2*(i/30)**3):.2f}' for i in range(31))
    right=drawing(axes+f'<polyline points="{pts}" class="eng-motion"/>'+'<text x="285" y="174" class="eng-axis-label">t</text><text x="19" y="30" class="eng-axis-label">s</text><text x="23" y="146" class="eng-axis-label">0</text><text x="23" y="46" class="eng-axis-label">1</text>')
    return panels(panel('A','路径 q(s)：经过哪些构型','路径在关节空间中连接起点与终点，本身没有速度。',left+parts(['起点构型','终点构型'])),panel('B','时间缩放 s(t)：何时经过','同一条路径可以采用不同时间函数，产生不同速度与加速度。',right,'曲线为归一化三次时间函数示意，实际周期须由约束计算。'))


def impedance():
    geometry=drawing('<rect x="245" y="38" width="41" height="100" rx="8" class="eng-object"/>'+path('M33 118H67l9-13 13 26 13-26 13 26 13-26 9 13H164','spring')+finger([(164,118),(203,94),(246,88)])+arrow(186,70,236,70,'motion')+number(83,81,1)+number(238,50,2)+number(280,156,3))
    return panels(panel('A','虚拟弹簧描述交互关系','位置偏差通过目标刚度转换成作用力，速度偏差可经阻尼项参与。',geometry+parts(['目标刚度 K（概念弹簧）','参考与实际的位置偏差','环境接触']),'虚拟弹簧由控制实现，不表示必须安装这个机械弹簧。'),panel('B','相同偏差，不同作用力','一维静态教学例子，偏差都取 10 mm。','<div class="eng-equation-pair"><div><strong>K = 100 N/m → 1 N</strong><p>较小的目标刚度。</p></div><div><strong>K = 1000 N/m → 10 N</strong><p>较大的目标刚度；仍需检查力上限。</p></div></div>','增益数值用于理解关系，不是硬件控制推荐。'))


def finger_gait():
    def frame(phase):
        body='<circle cx="160" cy="87" r="42" class="eng-object"/>'
        fingers=[[(38,153),(89,130),(122,109)],[(283,153),(231,130),(198,109)],[(266,26),(216,36),(183,51)]]
        for i,points in enumerate(fingers):
            leaving=(phase==1 and i==2) or (phase==3 and i==0)
            body += (path('M'+'L'.join(f'{x} {y}' for x,y in points),'constraint') if leaving else finger(points))
            if not leaving:body+=f'<circle cx="{points[-1][0]}" cy="{points[-1][1]}" r="5" class="eng-contact"/>'
        if phase==1:body+=arrow(217,46,191,55,'motion')
        if phase==3:body+=arrow(111,112,78,132,'motion')
        return drawing(body)
    return panels(panel('01','保留原有支持','新的手指朝计划接触位置移动。',frame(1)),panel('02','建立并确认新接触','逐步加载，检查新组合能承担负载。',frame(2)),panel('03','旧接触卸载并离开','剩余接触维持支持，再移动旧手指。',frame(3),'图示接触顺序，不证明各组合都稳定。'))


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
    'antagonistic': ('两个驱动：净力矩与共同预紧分别看', antagonistic),
    'pressure-map': ('从压力分布到合力与压力中心', pressure_map),
    'kinematics': ('从关节角到指尖位姿，再求逆解', kinematics),
    'trajectory': ('路径与时间是两个独立步骤', trajectory),
    'impedance': ('阻抗控制规定偏差与作用力的关系', impedance),
    'finger-gait': ('换指先移交支持，再解除旧接触', finger_gait),
}


def render(key):
    if key not in DIAGRAMS:
        raise ValueError(f'工程图解不存在：{key}')
    title, content = DIAGRAMS[key]
    return '<div markdown="0" class="eng-figure"><p class="eng-figure-title">' + escape(title) + '</p>' + content() + '<p class="eng-caption">概念示意 · 非产品结构图；尺寸、角度与箭头长度不表示数值。</p></div>'


def on_page_markdown(markdown, page, config, files):
    if not page.file.src_uri.startswith('engineering/'):
        return markdown
    if '<!-- engineering:tendon-materials -->' in markdown:
        markdown = markdown.replace('<!-- engineering:tendon-materials -->', tendon_materials.comparison())
    markdown = markdown.replace('<!-- engineering:tendon-material-summary -->', tendon_materials.material_summary()) if '<!-- engineering:tendon-material-summary -->' in markdown else markdown
    markdown = markdown.replace('<!-- engineering:tendon-mechanisms -->', tendon_materials.mechanism_comparison()) if '<!-- engineering:tendon-mechanisms -->' in markdown else markdown
    return re.sub(r'<!-- engineering:diagram ([a-z-]+) -->', lambda match: render(match[1]), markdown)
