"""Authored route illustrations with responsive, searchable HTML labels.

Geometry explains a mechanism; HTML explains the relationship. Keep scientific
scope and sources in technology-routes.json rather than deriving product claims
from the schematic. SVGs are decorative here; every panel has a text equivalent.
"""
from html import escape


def svg(body, viewbox='0 0 320 172'):
    return f'<svg class="route-sketch" viewBox="{viewbox}" aria-hidden="true" focusable="false">{body}</svg>'


def line(path, kind='structure'):
    return f'<path d="{path}" class="sketch-{kind}"/>'


def circle(x, y, radius=9, kind='joint'):
    return f'<circle cx="{x}" cy="{y}" r="{radius}" class="sketch-{kind}"/>'


def marker(x, y, number):
    return f'<g class="sketch-marker"><circle cx="{x}" cy="{y}" r="12"/><text x="{x}" y="{y}" dy=".35em" text-anchor="middle">{number}</text></g>'


def motor(x, y):
    return (f'<rect x="{x}" y="{y}" width="48" height="40" rx="6" class="sketch-motor"/>'
            + circle(x + 24, y + 20, 10, 'rotor'))


def heading(number, title, subtitle):
    return f'<div class="route-plate-heading"><span>{escape(number)}</span><div><h4>{escape(title)}</h4><p>{escape(subtitle)}</p></div></div>'


def plate(number, title, subtitle, content, note=''):
    return f'<article class="route-plate">{heading(number, title, subtitle)}{content}' + (f'<p class="route-plate-note">{escape(note)}</p>' if note else '') + '</article>'


def legend(items):
    return '<ol class="route-part-labels">' + ''.join(f'<li><span>{i}</span>{escape(label)}</li>' for i, label in enumerate(items, 1)) + '</ol>'


def node(title, detail, tone='neutral'):
    return f'<div class="route-node route-node-{tone}"><strong>{escape(title)}</strong><span>{escape(detail)}</span></div>'


def arrow(label=''):
    return f'<div class="route-flow-connector"><span>{escape(label)}</span><svg viewBox="0 0 40 16" aria-hidden="true"><path d="M1 8H37M31 2l6 6-6 6"/></svg></div>'


def flow(nodes, labels):
    parts = [node(*nodes[0])]
    for label, item in zip(labels, nodes[1:]):
        parts += [arrow(label), node(*item)]
    return f'<div class="route-flow route-flow-{len(nodes)}">' + ''.join(parts) + '</div>'


def loop(text):
    return f'<div class="route-feedback"><span>反馈返回</span><p>{escape(text)}</p></div>'


def compare(*plates):
    return '<div class="route-compare">' + ''.join(plates) + '</div>'


def shape():
    pinch = svg(circle(160, 88, 29, 'object') + line('M39 122H83L129 88M281 122H237L191 88') + circle(129, 88, 5, 'contact') + circle(191, 88, 5, 'contact'))
    wrap = svg(circle(160, 88, 40, 'object') + line('M43 143L91 123L111 75L142 47M277 143L229 123L209 75L178 47') + ''.join(circle(x, y, 5, 'contact') for x, y in [(112, 77), (143, 50), (208, 77), (177, 50)]))
    rotate = svg(circle(160, 88, 36, 'object') + line('M48 140L98 126L127 103M272 49L221 61L194 75') + circle(127, 103, 5, 'contact') + circle(194, 75, 5, 'contact') + line('M149 36A53 53 0 0 1 211 109M211 109l-2 -13M211 109l10 -7', 'signal'))
    return '<div class="route-trio">' + ''.join([
        plate('01', '捏取', '相对的指尖接触', pinch, '两侧指尖到达相对位置。'),
        plate('02', '包覆', '多个指节参与接触', wrap, '手指沿物体外形形成接触。'),
        plate('03', '手内重定向', '保持物体，同时改变接触', rotate, '接触与运动需要持续配合。')]) + '</div>'


def thumb():
    palm = '<rect x="103" y="100" width="150" height="60" rx="16" class="sketch-palm"/>' + line('M124 107V43M162 103V30M200 104V36M238 110V51')
    first = svg(palm + line('M113 141L61 112L47 65') + line('M47 62v-23m-5 7 5 -7 5 7', 'signal') + line('M124 40V18m-5 7 5 -7 5 7', 'signal'))
    second = svg(palm + circle(139, 65, 25, 'object') + line('M113 141L90 109L115 74') + circle(115, 74, 5, 'contact') + circle(125, 44, 5, 'contact') + line('M61 97Q64 53 100 45M100 45l-11 -2M100 45l-5 10', 'signal'))
    return compare(plate('A', '接触面朝向不同方向', '先看拇指的朝向', first, '有拇指，并不自动具备所需的对掌范围。'), plate('B', '拇指转向其他手指', '再看能否形成相对接触', second, '关节轴向、运动范围与掌部结构共同决定对掌。'))


def coupling():
    drawing = svg(line('M28 117H75H134L211 75L285 98') + ''.join(circle(x, y, kind='coupled' if x > 200 else 'joint') for x, y in [(75, 117), (134, 117), (211, 75), (260, 90)]) + line('M211 64V47Q242 30 260 57V79', 'constraint'), '0 20 320 132')
    metrics = '<div class="route-metrics"><div><strong>4</strong><span>关节</span></div><span>≠</span><div><strong>3</strong><span>自由度</span></div></div>'
    left = plate('A', '关节与自由度', 'Shadow 长指 · 2024 规格', drawing + '<p class="route-constraint-label">虚线连接：远端两关节的运动约束</p>' + metrics, '远端两关节存在运动约束，不能分别任意指定。')
    right = plate('B', '关节与驱动输入', 'SoftHand · 单执行器原型', '<div class="route-input-example">' + node('1 个执行器', '驱动输入', 'motion') + arrow('腱索传力') + node('19 个关节', '由机构、弹性与接触组织运动') + '</div>', '输入数量与关节数量，是两个不同的参数。')
    return compare(left, right)


def drive():
    remote = svg(motor(22, 108) + line('M72 132H142L216 86L290 108') + circle(142, 132) + circle(216, 86) + line('M49 116H139L213 69L289 91', 'force') + marker(45, 85, 1) + marker(121, 95, 2) + marker(236, 127, 3), '0 45 320 125')
    local = svg(line('M31 132H128L216 86L290 108') + motor(104, 112) + motor(192, 66) + line('M128 132L171 110M216 86L265 101', 'force') + marker(95, 91, 1) + marker(273, 134, 2), '0 45 320 125')
    return compare(plate('A', '执行器集中在基部', '以 Shadow Classic 为例', remote + legend(['执行器', '沿手指走向的腱索', '受驱动的关节']), '拉力从基部沿腱索传到关节。'), plate('B', '模块布置在关节附近', '以 LEAP v1 为例', local + legend(['电机模块', '连接到相邻指节']), '模块内部仍可包含减速与传动结构。'))


def transmission():
    return compare(plate('A', '腱索传递拉力', '先看力经过哪些部件', flow([('执行器', '产生驱动力', 'motion'), ('腱索', '沿走索路径受拉', 'motion'), ('关节', '形成运动')], ['拉力', '关节力矩']), 'Shadow 与 SoftHand 都用腱索，输入分配可以不同。'), plate('B', '模块内部的传动', '位置与传动形式分别判断', flow([('电机', '产生转动', 'motion'), ('减速 / 传动', '模块内部结构', 'motion'), ('指节', '通过关节运动')], ['转动', '输出运动']), '“电机在关节附近”并不能据此判断为无减速器直驱。'))


def allocation():
    left = '<div class="route-input-rows">' + flow([('输入 1', '单独命令', 'motion'), ('运动 1', '相应可控运动')], ['驱动']) + flow([('输入 2', '单独命令', 'motion'), ('运动 2', '相应可控运动')], ['驱动']) + '</div>'
    right = node('1 个输入', 'SoftHand 原型 · 一个执行器', 'motion') + arrow('共同组织闭合') + '<div class="route-factor-group"><strong>闭合后的手形</strong><ul><li>关节运动</li><li>弹性变形</li><li>物体接触</li></ul></div>'
    return compare(plate('A', '多路输入', '分别控制相应的运动', left, '示意两路命令，不代表特定产品的轴数。'), plate('B', '一个输入带动多个关节', '闭合过程中适应接触', right, '三项是决定手形的因素，不是三个独立驱动通道。'))


def sensing():
    sketches = [svg(motor(115, 62) + line('M163 82H248', 'force') + circle(211, 82, 6, 'sensor'), '35 35 250 115'), svg(line('M65 123H144L246 61') + circle(144, 123, 12) + circle(144, 123, 5, 'sensor'), '35 35 250 115'), svg(circle(209, 85, 38, 'object') + line('M55 125L117 117L168 87') + circle(168, 87, 6, 'sensor'), '35 35 250 115')]
    specs = [('传动侧', '腱索负载', '传动受力', '负载读数不直接等于物体接触力。'), ('关节处', '关节角度', '自身姿态', '描述相应关节当前的位置。'), ('接触表面', '触觉信号', '局部接触', '只能直接覆盖布置了传感器的区域。')]
    return '<div class="route-trio">' + ''.join(plate(f'0{i}', name, 'Shadow 配置中的测量位置', drawing + '<div class="route-measurement"><span>测量</span><strong>' + reading + '</strong><span>对应 ' + meaning + '</span></div>', note) for i, (drawing, (name, reading, meaning, note)) in enumerate(zip(sketches, specs), 1)) + '</div>'


def optical():
    cutaway = svg(circle(160, 38, 31, 'object') + line('M40 63H130Q160 94 190 63H280', 'membrane') + '<path d="M48 68V151H272V68" class="sketch-housing"/>' + '<path d="M145 137L124 75M175 137L196 75" class="sketch-light"/>' + '<rect x="138" y="131" width="44" height="26" rx="5" class="sketch-camera"/>' + marker(95, 62, 1) + marker(204, 142, 2))
    process = flow([('触觉图像', '摄像头输出', 'signal'), ('处理与模型', '标定与估计', 'signal'), ('接触信息', '位置、力或运动')], ['图像', '估计'])
    return '<div class="route-optical">' + plate('01', '接触使表面变形', 'DIGIT 视触觉原理', cutaway + legend(['弹性表面', '内部摄像头'])) + '<div class="route-optical-process">' + heading('02', '从图像获得接触信息', '传感输出与估计结果分开') + process + '<p class="route-plate-note">像素不是已标定的接触力；估计结果取决于所用算法。</p></div></div>'


def feedback():
    return flow([('建立接触', '触觉信号发生变化'), ('检测滑动', '处理信号，判断初始滑动', 'signal'), ('调整抓力', '控制器改变动作', 'motion'), ('再次观测', '接触是否稳定？')], ['信号', '判断结果', '新的接触状态']) + loop('继续检测接触与滑动，更新下一步动作。')


def control():
    return flow([('目标与当前观测', '要达到什么状态？现在怎样？'), ('控制器 / 策略', '由输入生成下一步命令', 'signal'), ('手与物体', '执行动作，改变状态', 'motion')], ['输入', '动作命令']) + loop('手与物体产生新的状态、接触观测，送回控制器 / 策略。')


def demonstration():
    training = flow([('人类示范', '记录观测与动作'), ('示范辅助强化学习', '结合示范与模拟交互', 'signal'), ('策略参数', '训练后保存', 'signal')], ['示范数据', '训练得到'])
    running = flow([('当前观测', '模拟环境的状态'), ('学到的策略', '使用训练所得参数', 'signal'), ('模拟手', '执行输出动作', 'motion')], ['输入', '动作'])
    return '<div class="route-phases"><section>' + heading('01', '训练阶段', 'DAPG · RSS 2018') + training + '</section><div class="route-phase-transfer"><span>保存的参数用于运行时策略 ↓</span></div><section>' + heading('02', '运行阶段', '原论文验证范围：模拟实验') + running + '</section></div>'


def transfer():
    training = flow([('变化的仿真环境', '随机化物理参数与物体外观'), ('强化学习', '不使用人类示范', 'signal'), ('学到的策略', '仿真训练的结果', 'signal')], ['模拟交互', '训练得到'])
    return '<div class="route-phases"><section>' + heading('01', '仿真训练', 'OpenAI · 2018 研究') + training + '</section><div class="route-phase-transfer"><span>将学到的策略接入真实硬件 ↓</span></div><section>' + heading('02', '实物验证', '真实 Shadow 平台 · 物体重定向') + flow([('真实观测', '实物状态与目标'), ('同一策略', '通过实物接口输出命令', 'signal'), ('真实手', '验证物体重定向任务', 'motion')], ['输入', '动作']) + '</section></div>'


# Legend terms describe semantics, not decoration. Not every figure needs one.
DIAGRAMS = {
    'shape': (shape, '接触与运动', [('motion', '接触位置'), ('signal', '运动方向')]),
    'thumb-opposition': (thumb, '接触朝向', [('motion', '接触位置'), ('signal', '朝向变化')]),
    'joint-coupling': (coupling, '两个不同的计数问题', []),
    'drive': (drive, '执行器布置对照', [('motion', '驱动与传力'), ('neutral', '指节与关节')]),
    'transmission-path': (transmission, '动力经过的路径', [('motion', '驱动与传动')]),
    'input-allocation': (allocation, '输入与运动的关系', [('motion', '驱动输入')]),
    'sense': (sensing, '测量位置对照', [('signal', '传感位置'), ('motion', '传力路径')]),
    'optical-tactile': (optical, '接触 → 图像 → 估计', [('signal', '感知与处理')]),
    'contact-feedback': (feedback, '接触反馈闭环', [('signal', '信号处理'), ('motion', '动作执行')]),
    'control': (control, '运行时闭环', [('signal', '信息与决策'), ('motion', '动作执行')]),
    'demonstration-learning': (demonstration, '训练与运行分开', [('signal', '学习与策略'), ('motion', '动作执行')]),
    'simulation-transfer': (transfer, '训练与验证分开', [('signal', '学习与策略'), ('motion', '实物执行')]),
}


def render(key):
    builder, label, _ = DIAGRAMS[key]
    return f'<div class="route-diagram route-diagram-{escape(key)}" role="group" aria-label="{escape(label)}">{builder()}</div>'


def render_legend(key):
    items = DIAGRAMS[key][2]
    return '<div class="route-legend">' + ''.join(f'<span><i class="route-swatch-{tone}" aria-hidden="true"></i>{escape(label)}</span>' for tone, label in items) + '</div>' if items else ''
