"""Authored route illustrations with responsive, searchable HTML labels.

Geometry explains a mechanism; HTML explains the relationship. Keep scientific
scope and sources in technology-routes.json rather than deriving product claims
from the schematic. SVGs are decorative here; every panel has a text equivalent.
"""
from html import escape
from math import hypot, cos, sin, pi


def svg(body, viewbox='0 0 320 220'):
    return f'<svg class="route-sketch" viewBox="{viewbox}" aria-hidden="true" focusable="false">{body}</svg>'


def line(path, kind='structure'):
    return f'<path d="{path}" class="sketch-{kind}"/>'


def circle(x, y, radius=6, kind='joint'):
    return f'<circle cx="{x}" cy="{y}" r="{radius}" class="sketch-{kind}"/>'


def marker(x, y, number, to=None):
    leader = line(f'M{x} {y+9}L{to[0]} {to[1]}', 'leader') if to else ''
    return leader + f'<g class="sketch-marker"><circle cx="{x}" cy="{y}" r="9"/><text x="{x}" y="{y}" dy=".35em" text-anchor="middle">{number}</text></g>'


def segment(a, b, width=14):
    """Tapered link contours with clearance around hinge centers."""
    dx, dy = b[0]-a[0], b[1]-a[1]
    length = hypot(dx, dy)
    ux, uy = dx/length, dy/length
    nx, ny = -uy, ux
    start, end = (a[0]+ux*8, a[1]+uy*8), (b[0]-ux*8, b[1]-uy*8)
    def p(point, offset):
        return f'{point[0]+nx*offset:.2f} {point[1]+ny*offset:.2f}'
    return line(f'M{p(start,width/2)}L{p(end,width*.39)}Q{b[0]} {b[1]} {p(end,-width*.39)}L{p(start,-width/2)}Q{a[0]} {a[1]} {p(start,width/2)}Z', 'link')


def finger(points, width=14):
    return ''.join(segment(a,b,width) for a,b in zip(points,points[1:])) + ''.join(circle(x,y,3.6)+circle(x,y,1,'hub') for x,y in points[:-1])


def gear(x, y, radius, teeth=12):
    points=[]
    for i in range(teeth*4):
        angle=2*pi*i/(teeth*4)
        r=radius if i%4 in (1,2) else radius-3
        points.append(f'{x+r*cos(angle):.2f},{y+r*sin(angle):.2f}')
    return '<polygon points="'+' '.join(points)+'" class="sketch-gear"/>'+circle(x,y,3,'rotor')


def motor(x, y):
    return (f'<rect x="{x}" y="{y}" width="46" height="34" rx="5" class="sketch-motor"/>'
            + line(f'M{x+7} {y+9}v16M{x+12} {y+9}v16M{x+17} {y+9}v16','motor-detail')
            + circle(x+31,y+17,8,'rotor')+circle(x+31,y+17,2,'hub')
            + line(f'M{x+46} {y+17}h10'))


def heading(number, title, subtitle):
    return f'<div class="route-plate-heading"><span>{escape(number)}</span><div><h4>{escape(title)}</h4><p>{escape(subtitle)}</p></div></div>'


def plate(number, title, subtitle, content, note=''):
    return f'<article class="route-plate">{heading(number, title, subtitle)}{content}' + (f'<p class="route-plate-note">{escape(note)}</p>' if note else '') + '</article>'


def legend(items):
    return '<ol class="route-part-labels">' + ''.join(f'<li><span>{i}</span>{escape(label)}</li>' for i, label in enumerate(items, 1)) + '</ol>'


def icon(kind):
    """Small line drawings identify the physical or information process."""
    if kind=='motor': body=motor(8,15)
    elif kind=='hand': body=line('M18 55V30Q18 26 22 30L27 37V15Q31 10 33 15V31V10Q37 5 39 10V31V14Q43 9 45 14V34V21Q49 16 51 21V45Q51 57 41 57H29Q24 57 18 55','link')
    elif kind=='image': body='<rect x="12" y="14" width="44" height="38" rx="2" class="sketch-housing"/>'+line('M17 45L29 29L39 39L50 25','signal')+circle(45,23,3,'contact')
    elif kind=='model': body=line('M13 20H55M13 32H55M13 44H55','guide')+line('M22 14V26M44 26V38M30 38V50','signal')+circle(22,20,3,'sensor')+circle(44,32,3,'sensor')+circle(30,44,3,'sensor')
    elif kind=='learning': body=line('M17 17L36 32L17 49M36 32L54 17M36 32L54 49','leader')+''.join(circle(x,y,4,'sensor') for x,y in [(17,17),(17,49),(36,32),(54,17),(54,49)])
    elif kind=='object': body=line('M17 23L36 13L55 23V44L36 54L17 44ZM17 23L36 34L55 23M36 34V54','link')
    else: body=line('M12 49H56M15 16V49','guide')+line('M15 36H24L29 22L36 44L42 30H55','signal')
    return '<svg class="route-stage-icon" viewBox="0 0 68 68" aria-hidden="true">'+body+'</svg>'


def node(title, detail, tone='neutral', symbol='data', number=''):
    return f'<div class="route-node route-node-{tone}"><div class="route-node-symbol">{icon(symbol)}<span class="route-step-number">{number}</span></div><strong>{escape(title)}</strong><span>{escape(detail)}</span></div>'


def arrow(label=''):
    return f'<div class="route-flow-connector"><span>{escape(label)}</span><svg viewBox="0 0 40 16" aria-hidden="true"><path d="M1 8H37M31 2l6 6-6 6"/></svg></div>'


def flow(nodes, labels):
    parts = [node(*nodes[0], number='01')]
    for index, (label, item) in enumerate(zip(labels, nodes[1:]), 2):
        parts += [arrow(label), node(*item, number=f'{index:02}')]
    return f'<div class="route-flow route-flow-{len(nodes)}">' + ''.join(parts) + '</div>'


def loop(text, count=3):
    # The last stage returns its observation to the second, decision stage.
    start, end = (1000*(count-.5)/count, 1500/count)
    return (f'<div class="route-feedback"><svg viewBox="0 0 1000 36" preserveAspectRatio="none" aria-hidden="true"><path d="M{start} 0V25H{end}V1m-5 7 5-7 5 7"/></svg>'
            f'<div class="route-feedback-caption"><span>反馈返回</span><p>{escape(text)}</p></div></div>')


def compare(*plates):
    return '<div class="route-compare">' + ''.join(plates) + '</div>'


def shape():
    pinch = svg(circle(160,104,36,'object')+finger([(24,167),(68,165),(105,132),(124,104)])+finger([(296,167),(252,165),(215,132),(196,104)])+circle(124,104,3.5,'contact')+circle(196,104,3.5,'contact')+line('M160 43V66M160 142V168','guide'))
    wrap = svg(circle(160,102,37,'object')+finger([(24,178),(88,146),(111,107),(123,80),(151,60)],16)+finger([(296,178),(232,146),(209,107),(197,80),(169,60)],16)+''.join(circle(x,y,3.5,'contact') for x,y in [(128.2,83.1),(152.2,65.8),(191.8,83.1),(167.8,65.8)]))
    rotate = svg(line('M160 72l26 31-26 31-26-31Z','ghost')+'<g transform="rotate(-20 160 103)">'+line('M160 69l30 34-30 34-30-34Z','object')+'</g>'+finger([(26,172),(88,149),(131,113)])+finger([(294,36),(233,57),(189,93)])+circle(131,113,3.5,'contact')+circle(189,93,3.5,'contact')+line('M121 51A65 65 0 0 1 222 118M222 118l-1-11m1 11 8-7','signal'))
    return '<div class="route-trio">' + ''.join([
        plate('01', '捏取', '相对的指尖接触', pinch, '两侧指尖到达相对位置。'),
        plate('02', '包覆', '多个指节参与接触', wrap, '手指沿物体外形形成接触。'),
        plate('03', '手内重定向', '保持物体，同时改变接触', rotate, '接触与运动需要持续配合。')]) + '</div>'


def palm(opposed=False):
    body=line('M108 140Q111 124 122 122H251Q267 125 267 145V185Q264 204 246 204H127Q111 199 108 181Z','palm')
    index = [(129,132),(153,105),(147,85)] if opposed else [(129,132),(129,89),(129,55)]
    for points in [index,[(171,129),(171,79),(171,37)],[(213,131),(213,84),(213,49)],[(250,138),(250,99),(250,72)]]:
        body+=finger(points,17)
    body+=finger([(111,175),(82,146),(112,104)] if opposed else [(111,175),(74,151),(48,110)],19)
    return body


def thumb():
    first=svg(palm()+line('M36 118L28 95M28 95l-1 10m1-10 8 6M129 44V24M129 24l-5 7m5-7 5 7','signal')+line('M82 146L112 104','ghost'))
    second=svg(palm(True)+circle(128,91,20,'object')+circle(112,104,3.5,'contact')+circle(147,85,3.5,'contact')+line('M50 96Q69 72 93 85M93 85l-10-1m10 1-4-9','signal'))
    return compare(plate('A', '接触面朝向不同方向', '先看拇指的朝向', first, '有拇指，并不自动具备所需的对掌范围。'), plate('B', '拇指转向其他手指', '再看能否形成相对接触', second, '关节轴向、运动范围与掌部结构共同决定对掌。'))


def coupling():
    drawing=svg(finger([(35,143),(111,143),(177,116),(232,86),(290,96)],17)+circle(177,116,4.3,'coupled')+circle(232,86,4.3,'coupled')+line('M177 100Q192 57 225 60Q246 59 244 74','constraint')+marker(93,74,2,(111,139))+marker(156,43,3,(176,110))+marker(239,31,4,(232,81))+marker(40,106,1,(35,137)))
    metrics = '<div class="route-metrics"><div><strong>4</strong><span>关节</span></div><span>≠</span><div><strong>3</strong><span>自由度</span></div></div>'
    left = plate('A', '关节与自由度', 'Shadow 长指 · 2024 规格', drawing + '<p class="route-constraint-label">虚线连接：远端两关节的运动约束</p>' + metrics, '关节位置与轴向为计数示意，不复刻产品运动链。')
    right = plate('B', '关节与驱动输入', 'SoftHand · 单执行器原型', '<div class="route-input-example">' + node('1 个执行器', '驱动输入', 'motion','motor') + arrow('腱索传力') + node('19 个关节', '由机构、弹性与接触组织运动','neutral','hand') + '</div>', '输入数量与关节数量，是两个不同的参数。')
    return compare(left, right)


def remote_body():
    return motor(16,144)+finger([(93,162),(163,162),(231,116),(297,95)],19)+circle(163,162,10,'pulley')+circle(231,116,9,'pulley')+line('M47 151H157Q162 147 172 152L224 105Q232 100 239 110L296 85','force')+circle(47,161,11,'rotor')+line('M16 187H71M27 187v6m13-6v6m13-6v6m13-6v6','ground')


def local_body():
    return finger([(39,164),(135,164),(222,118),(294,95)],19)+motor(105,144)+motor(192,98)+line('M151 161L182 144M238 114L268 104','force')


def drive():
    remote=svg(remote_body()+marker(38,105,1,(38,139))+marker(167,91,2,(188,140))+marker(268,159,3,(233,124)))
    local=svg(local_body()+marker(122,110,1,(127,142))+marker(265,171,2,(267,115)))
    return compare(plate('A', '执行器集中在基部', '以 Shadow Classic 为例', remote + legend(['执行器', '沿手指走向的腱索', '受驱动的关节']), '拉力从基部沿腱索传到关节。'), plate('B', '模块布置在关节附近', '以 LEAP v1 为例', local + legend(['电机模块', '连接到相邻指节']), '模块内部仍可包含减速与传动结构。'))


def transmission():
    tendon=svg(remote_body()+marker(37,112,1,(38,141))+marker(115,112,2,(113,151))+marker(232,61,3,(232,104))+line('M90 132H133M133 132l-7-4m7 4-7 4','signal'))
    module=svg('<rect x="30" y="89" width="173" height="94" rx="9" class="sketch-housing"/>'+motor(41,119)+gear(111,136,19)+gear(151,136,24)+finger([(203,136),(266,100),(300,96)],20)+line('M96 136H110M176 136H203','force')+marker(58,60,1,(62,114))+marker(151,59,2,(151,105))+marker(270,159,3,(261,107))+line('M30 190H203','guide'))
    return compare(plate('A','腱索传递拉力','沿走索路径到达关节',tendon+legend(['执行器与卷盘','受拉的腱索','关节滑轮']),'Shadow 与 SoftHand 都用腱索，输入分配可以不同。'),plate('B','模块内部的传动','位置与传动形式分别判断',module+legend(['电机','内部减速 / 传动','输出指节']),'内部传动为概念示意；关节附近的电机不自动等于无减速器直驱。'))


def allocation():
    left=svg(motor(18,51)+motor(18,144)+finger([(97,68),(161,68),(218,42),(283,45)],17)+finger([(97,161),(161,161),(220,135),(283,139)],17)+line('M74 68H97M74 161H97','force')+line('M219 75Q249 91 283 71M283 71l-11 1m11-1-5 10M219 174Q249 190 283 170M283 170l-11 1m11-1-5 10','signal'))
    right=svg(circle(239,94,35,'object')+motor(17,116)+line('M74 133H100V73H137M100 133V172H137','force')+line('M103 73l7-5 7 10 7-10 7 5M103 172l7-5 7 10 7-10 7 5','constraint')+finger([(137,73),(179,70),(212,71)],17)+finger([(137,172),(178,146),(213,117)],17)+circle(212,71,3.5,'contact')+circle(213,117,3.5,'contact')+line('M138 172L173 180L220 180','ghost'))+'<div class="route-factor-group"><strong>共同决定手形</strong><ul><li>关节运动</li><li>弹性变形</li><li>物体接触</li></ul></div>'
    return compare(plate('A', '多路输入', '分别控制相应的运动', left, '示意两路命令，不代表特定产品的轴数。'), plate('B', '一个输入带动多个关节', '闭合过程中适应接触', right, '三项是决定手形的因素，不是三个独立驱动通道。'))


def sensing():
    sketches=[svg(motor(22,129)+finger([(96,146),(173,146),(259,93)],18)+line('M52 136H164L258 80','force')+'<rect x="105" y="129" width="30" height="14" rx="3" class="sketch-sensor-outline"/>'+line('M116 129V102H155','signal')+circle(159,102,3,'sensor')),svg(finger([(36,152),(145,152),(236,98),(290,96)],19)+circle(145,152,15,'sensor-outline')+line('M145 137V90H178','signal')+circle(182,90,3,'sensor')),svg(circle(239,102,39,'object')+finger([(31,171),(108,153),(173,112),(200,102)],18)+line('M188 94Q203 92 202 104Q201 114 191 116','sensor-outline')+line('M185 101V73H139','signal')+circle(135,73,3,'sensor'))]
    specs = [('传动侧', '腱索负载', '传动受力', '负载读数不直接等于物体接触力。'), ('关节处', '关节角度', '自身姿态', '描述相应关节当前的位置。'), ('接触表面', '触觉信号', '局部接触', '只能直接覆盖布置了传感器的区域。')]
    return '<div class="route-trio">' + ''.join(plate(f'0{i}', name, 'Shadow 配置中的测量位置', drawing + '<div class="route-measurement"><span>测量</span><strong>' + reading + '</strong><span>对应 ' + meaning + '</span></div>', note) for i, (drawing, (name, reading, meaning, note)) in enumerate(zip(sketches, specs), 1)) + '</div>'


def optical():
    cutaway=svg(circle(160,66,33,'object')+line('M38 84H125Q160 114 195 84H282','membrane')+line('M44 91V193H276V91','housing')+line('M150 169L127 95M170 169L193 95','light')+'<rect x="140" y="165" width="40" height="26" rx="4" class="sketch-camera"/>'+circle(160,173,5,'rotor')+line('M75 180V151M65 164l10-13 10 13M245 180V151M235 164l10-13 10 13','light')+marker(88,47,1,(98,84))+marker(219,156,2,(182,179)))
    process = flow([('触觉图像', '摄像头输出', 'signal','image'), ('处理与模型', '标定与估计', 'signal','model'), ('接触信息', '位置、力或运动','neutral','data')], ['图像', '估计'])
    return '<div class="route-optical">' + plate('01', '接触使表面变形', 'DIGIT 视触觉原理', cutaway + legend(['弹性表面', '内部摄像头'])) + '<div class="route-optical-process">' + heading('02', '从图像获得接触信息', '传感输出与估计结果分开') + process + '<p class="route-plate-note">像素不是已标定的接触力；估计结果取决于所用算法。</p></div></div>'


def feedback():
    return flow([('建立接触', '触觉信号发生变化','neutral','hand'), ('检测滑动', '处理信号，判断初始滑动', 'signal','data'), ('调整抓力', '控制器改变动作', 'motion','motor'), ('再次观测', '接触是否稳定？','neutral','image')], ['信号', '判断结果', '新的接触状态']) + loop('继续检测接触与滑动，更新下一步动作。',4)


def control():
    return flow([('目标与当前观测', '要达到什么状态？现在怎样？','neutral','data'), ('控制器 / 策略', '由输入生成下一步命令', 'signal','model'), ('手与物体', '执行动作，改变状态', 'motion','hand')], ['输入', '动作命令']) + loop('手与物体产生新的状态、接触观测，送回控制器 / 策略。')


def demonstration():
    training = flow([('人类示范', '记录观测与动作','neutral','hand'), ('示范辅助强化学习', '结合示范与模拟交互', 'signal','learning'), ('策略参数', '训练后保存', 'signal','model')], ['示范数据', '训练得到'])
    running = flow([('当前观测', '模拟环境的状态','neutral','data'), ('学到的策略', '使用训练所得参数', 'signal','model'), ('模拟手', '执行输出动作', 'motion','hand')], ['输入', '动作'])
    return '<div class="route-phases"><section>' + heading('01', '训练阶段', 'DAPG · RSS 2018') + training + '</section><div class="route-phase-transfer"><span>保存的参数用于运行时策略 ↓</span></div><section>' + heading('02', '运行阶段', '原论文验证范围：模拟实验') + running + '</section></div>'


def transfer():
    training = flow([('变化的仿真环境', '随机化物理参数与物体外观','neutral','object'), ('强化学习', '不使用人类示范', 'signal','learning'), ('学到的策略', '仿真训练的结果', 'signal','model')], ['模拟交互', '训练得到'])
    return '<div class="route-phases"><section>' + heading('01', '仿真训练', 'OpenAI · 2018 研究') + training + '</section><div class="route-phase-transfer"><span>将学到的策略接入真实硬件 ↓</span></div><section>' + heading('02', '实物验证', '真实 Shadow 平台 · 物体重定向') + flow([('真实观测', '实物状态与目标','neutral','data'), ('同一策略', '通过实物接口输出命令', 'signal','model'), ('真实手', '验证物体重定向任务', 'motion','hand')], ['输入', '动作']) + '</section></div>'


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
