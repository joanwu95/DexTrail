"""Apply the reader-facing knowledge edition; preserve the previous source pages."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'website/docs'
BACKUP = ROOT / 'research/backups/knowledge-presentation-2026-10-04'
SHADOW = 'https://www.shadowrobot.com/wp-content/uploads/2024/12/shadow_dexterous_hand_e_technical_specification_20241204.pdf'
SOFT = 'https://www.centropiaggio.unipi.it/sites/default/files/PisaIIT_SoftHand_0.pdf'
LEAP = 'https://roboticsproceedings.org/rss19/p089.pdf'
API = 'https://github.com/leap-hand/LEAP_Hand_API'


def save(path, text):
    destination = DOCS / path
    if destination.exists():
        old = BACKUP / path
        if not old.exists():
            old.parent.mkdir(parents=True, exist_ok=True)
            old.write_bytes(destination.read_bytes())
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text.strip() + '\n', encoding='utf-8')


def page(path, title, subtitle, body, *, eyebrow='', rail=()):
    depth = len(Path(path).parent.parts) + (0 if Path(path).name == 'index.md' else 1)
    home = '../' * depth
    aside = ''
    if rail:
        aside = '<aside class="dex-rail dex-detail-rail" aria-label="本页目录"><div class="dex-rail-heading"><strong>本页内容</strong></div><nav class="dex-scroll-nav">' + ''.join(f'<a href="#{key}">{label}</a>' for key, label in rail) + '</nav></aside>'
    # Nested editorial HTML must stay a single block inside markdown="1".
    # Otherwise md_in_html can close the reading canvas at an inner div.
    body = re.sub(r'<div (?![^>]*markdown=)', '<div markdown="0" ', body)
    body = body.replace('><', '>\n<')
    save(path, f'''---
title: {title.replace('<br>', '')} · DexTrail
hide: [navigation, toc, footer]
---

<div class="dex-hand-page dex-essay dex-knowledge{' has-dex-rail' if rail else ''}" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="{home}"><img class="dex-emblem" src="{home}images/brand/dextrail-fingerprint-original.svg" alt="">DexTrail<span>.</span></a><span class="knowledge-edition">灵巧手技术图谱</span></header>
{aside}
<div class="hand-heading"><p class="knowledge-kicker">{eyebrow}</p><h1>{title}</h1><p class="hand-identity">{subtitle}</p></div>

{body}

<footer class="knowledge-footer"><a href="{home}">返回产品地图 ↗</a><span>DexTrail · Joan Wu</span></footer>
</div>''')


def figure(name, alt, caption, prefix='../'):
    return f'<figure class="knowledge-figure"><img src="{prefix}images/knowledge/{name}.svg" alt="{alt}"><figcaption>{caption}</figcaption></figure>'


def drawer(text):
    return '<details class="evidence-drawer" markdown="1">\n<summary>依据与适用范围</summary>\n\n' + text + '\n\n</details>'


def svg(name, title, body):
    save(f'images/knowledge/{name}.svg', f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 280" role="img" aria-labelledby="title"><title id="title">{title}</title><defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10" fill="#aa4d3e"/></marker></defs><style>text{{font-family:'Segoe UI','Microsoft YaHei',sans-serif;fill:#292b29;font-size:22px}}.small{{font-size:13px;fill:#696d67}}.accent{{fill:#aa4d3e}}.line{{fill:none;stroke:#292b29;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}}.cable{{fill:none;stroke:#aa4d3e;stroke-width:3;stroke-linecap:round}}.soft{{fill:none;stroke:#6b8070;stroke-width:3;stroke-linecap:round}}.surface{{fill:#e9e5dc;stroke:#d2cec3;stroke-width:1.5}}</style>{body}</svg>''')


svg('tendon', '腱传动概念图：电机通过腱索与滑轮将拉力传到关节', '''
<text x="34" y="35" class="small">01 / 动力沿腱索传递</text><rect x="38" y="102" width="90" height=" seventy" class="surface"/><path class="line" d="M46 104H126V176H46Z"/><text x="65" y="145">M</text><path class="line" d="M127 140H164"/><circle class="line" cx="186" cy="140" r="24"/><circle class="line" cx="352" cy="140" r="25"/><circle class="line" cx="514" cy="103" r="22"/><circle class="line" cx="647" cy="63" r="17"/>
<path d="M210 140H326M377 135L492 108M535 96L630 68M665 65L735 91" fill="none" stroke="#c1bbaf" stroke-width="18" stroke-linecap="round"/>
<path class="cable" d="M186 116H346Q359 113 375 119L506 79Q522 73 535 83L645 46Q659 46 666 61L728 82"/><path class="soft" d="M186 164H357Q376 164 377 146L523 126Q540 125 540 109L654 80L728 101"/>
<path class="cable" d="M247 115H283" marker-end="url(#arrow)"/><text x="51" y="226">执行器</text><text x="175" y="226">卷盘</text><text x="332" y="226">关节滑轮</text><text x="508" y="199" class="accent">腱索路径</text><text x="596" y="226">指端运动</text><text x="35" y="261" class="small">概念示意 · 走索数量、回复机构与关节约束依具体设计而异</text>'''.replace('height=" seventy"', 'height="72"'))

svg('synergy', '一个输入通过腱索和柔顺结构组织多关节运动，接触使手形改变', '''
<text x="34" y="35" class="small">02 / 同一闭合输入，两种接触条件</text><circle class="surface" cx="76" cy="144" r="29"/><text x="68" y="150">u</text><path class="cable" d="M107 144H176M176 144V89H214M176 144V199H214"/>
<g class="line"><path d="M265 66L330 104L366 154M265 136L330 149L365 197M265 211L329 211L365 244"/><circle cx="330" cy="104" r="7"/><circle cx="330" cy="149" r="7"/><circle cx="329" cy="211" r="7"/></g><path class="cable" d="M230 92L261 92M230 202L261 202" marker-end="url(#arrow)"/>
<text x="273" y="35">自由闭合</text><path d="M420 145H470" class="cable" marker-end="url(#arrow)"/><text x="418" y="179" class="small">加入接触</text>
<circle class="surface" cx="629" cy="145" r="48"/><g class="line"><path d="M518 61L582 87L639 97M518 137L574 138L581 146M518 218L580 205L636 193"/><circle cx="582" cy="87" r="7"/><circle cx="574" cy="138" r="7"/><circle cx="580" cy="205" r="7"/></g><g fill="#aa4d3e"><circle cx="639" cy="97" r="5"/><circle cx="581" cy="146" r="5"/><circle cx="636" cy="193" r="5"/></g><text x="604" y="150">物体</text><text x="565" y="35">受约束闭合</text><text x="35" y="266" class="small">概念示意 · 接触与弹性共同影响实际手形；不是 SoftHand 的走索或关节几何复刻</text>''')

svg('measurement', '测量链：电机电流、传动负载、关节角度和物体接触力位于不同位置', '''
<text x="34" y="35" class="small">03 / 测量位置决定读数的物理意义</text><path d="M113 134H707" stroke="#d2cec3" stroke-width="2" stroke-dasharray="4 8"/>
<rect class="surface" x="63" y="103" width="91" height="62" rx="5"/><path class="line" d="M76 119H88V151H102V119H116V151H132"/><circle class="line" cx="301" cy="134" r="33"/><circle class="line" cx="301" cy="134" r="8"/><path class="line" d="M436 145L502 126L556 91"/><circle class="line" cx="502" cy="126" r="12"/><path class="line" d="M652 94L690 129H723M723 103V158"/><circle cx="721" cy="130" r="5" fill="#aa4d3e"/>
<text x="79" y="205">电机电流</text><text x="265" y="205">传动负载</text><text x="470" y="205">关节角度</text><text x="670" y="205">接触力</text><text class="small" x="87" y="232">驱动侧</text><text class="small" x="280" y="232">传动侧</text><text class="small" x="482" y="232">关节侧</text><text class="small" x="675" y="232">接触侧</text><path class="cable" d="M164 74H683"/><text x="300" y="64" class="accent">跨位置换算，需要模型与标定</text>''')

svg('axes', 'Shadow独立受控轴总计20，含手部18和腕部2；LEAP v1手部16', '''
<text x="34" y="35" class="small">04 / 先统一计数范围</text><text x="35" y="109">Shadow Classic</text><text x="35" y="187">LEAP v1</text><rect x="207" y="80" width="486" height="45" fill="#6b8070"/><rect x="693" y="80" width="54" height="45" fill="#aa4d3e"/><rect x="207" y="158" width="432" height="45" fill="#6b8070"/><text x="407" y="109" style="fill:#fffdf8">手部 18</text><text x="700" y="109" style="fill:#fffdf8;font-size:13px">腕 2</text><text x="385" y="187" style="fill:#fffdf8">手部 16</text><text x="208" y="250" class="small">等长单位代表 1 个轴 · 长度不代表性能 · 耦合末节不另计为独立输入</text>''')

svg('learning', '策略从仿真训练迁移到真实硬件，需要跨越动力学和观测差异', '''
<text x="34" y="35" class="small">05 / 策略如何从仿真进入实物？</text><rect class="surface" x="44" y="77" width="205" height="126" rx="5"/><path class="line" d="M93 157L145 107L198 157Z"/><text x="108" y="232">仿真训练</text><path class="cable" d="M268 138H347" marker-end="url(#arrow)"/><rect x="366" y="100" width="96" height="76" rx="38" fill="#aa4d3e"/><text x="396" y="145" style="fill:#fffdf8">策略</text><path class="cable" d="M480 138H558" marker-end="url(#arrow)"/><g class="line"><path d="M584 178L617 138L617 94M617 138L648 119L648 82M648 119L682 128L692 102M682 128L712 158L737 147"/></g><circle class="surface" cx="682" cy="173" r="25"/><text x="623" y="232">真实硬件</text><text x="288" y="78" class="small">物理与观测差异</text><text x="289" y="218" class="small">随机化与迁移验证</text>''')

page('technologies/index.md', '技术路线', '先看力怎样传递，再看运动怎样组织。', '''
<div class="knowledge-section-head"><span>机构与驱动</span><span>两条路线，两个不同问题</span></div>
<div class="route-spread">
<article class="route-feature"><p class="knowledge-kicker">01 / 传力路径</p><a class="route-visual" href="tendon-driven/">''' + figure('tendon', '电机、卷盘和关节滑轮之间的腱传动路径', '读懂动力怎样从执行器到达关节。') + '''</a><h2><a href="tendon-driven/">腱绳传动 <span>↗</span></a></h2><p>同样采用腱索，Shadow 与 SoftHand 的驱动分配和控制结构却不同。</p><p class="route-examples">Shadow Classic / Pisa-IIT SoftHand</p></article>
<article class="route-feature"><p class="knowledge-kicker">02 / 运动分配</p><a class="route-visual" href="underactuation-and-synergies/">''' + figure('synergy', '相同驱动输入在自由闭合与接触闭合时产生不同手形', '读懂少量输入如何组织多关节运动。') + '''</a><h2><a href="underactuation-and-synergies/">欠驱动与协同 <span>↗</span></a></h2><p>把一部分适应性放进机构，简化输入，也改变了可独立控制的运动。</p><p class="route-examples">Pisa-IIT SoftHand / qb SoftHand</p></article>
</div>
<div class="knowledge-insight"><strong>传动方式与驱动分配，是两个维度。</strong><p>腱绳描述力的路径；欠驱动描述输入与运动的关系。两者可以同时出现在一款手上。</p></div>
<div class="knowledge-next"><a href="../development/">沿时间轴看研究与产品如何发展 ↗</a><a href="../engineering/transmission/">进一步理解传动与标定 ↗</a></div>
''', eyebrow='技术图谱 / 路线')

page('development/index.md', '领域发展', '学术界如何提出问题，工业界如何回应需求。', '''
<div class="focus-strip"><a href="#dlr-hand-ii-2001"><span>系统集成</span><small>机构 × 感知</small></a><a href="#adaptive-synergies-2014"><span>机械适应</span><small>输入 × 接触</small></a><a href="#learning-in-hand-2018"><span>策略学习</span><small>仿真 × 实物</small></a><a href="#leap-2023"><span>实验平台</span><small>开放 × 维护</small></a></div>
<p class="knowledge-caption">从七个代表案例观察问题的展开。这些关注点长期并存，时间先后不表示路线替代。</p>

## 学术与工业的代表节点 {#timeline}

<!-- knowledge:development -->

<div class="knowledge-next"><a href="../technologies/">从时间轴进入技术路线 ↗</a><a href="../papers/">查看对应论文与方法 ↗</a></div>
''', eyebrow='技术图谱 / 发展', rail=(('timeline', '发展时间轴'), ('focus', '关注点的展开'), ('relationships', '路线与共同问题'), ('sources', '原始资料')))

page('engineering/index.md', '工程问题', '把参数差异，转成对机构、感知与控制的理解。', '''
<div class="engineering-library">
<a class="engineering-story" href="degrees-of-freedom/"><div>''' + figure('axes', '手部与腕部独立受控轴分开计数', '构型 / 独立输入') + '''</div><div><p class="knowledge-kicker">01 / 构型</p><h2>20 与 16，<br>差异究竟在哪里？ ↗</h2><p>先拆开手部与腕部，再看运动分配和关节约束。</p><span class="story-products">Shadow Classic × LEAP v1</span></div></a>
<a class="engineering-story" href="sensing-chain/"><div>''' + figure('measurement', '电机、传动、关节和接触位置的测量量不同', '感知 / 测量位置') + '''</div><div><p class="knowledge-kicker">02 / 感知</p><h2>力感知，<br>究竟测在哪里？ ↗</h2><p>沿测量链点击查看：电流、腱负载与接触力各自意味着什么。</p><span class="story-products">Shadow × LEAP × Wuji · 交互图解</span></div></a>
<a class="engineering-story" href="transmission/"><div>''' + figure('tendon', '执行器通过传动驱动关节', '控制 / 传动映射') + '''</div><div><p class="knowledge-kicker">03 / 控制</p><h2>传动方案，<br>怎样改变标定？ ↗</h2><p>命令、关节运动与接触状态，为什么需要分层理解。</p><span class="story-products">Shadow × LEAP × SoftHand</span></div></a>
</div>
''', eyebrow='技术图谱 / 工程')

page('technologies/tendon-driven.md', '腱绳传动', '力沿着腱索到达关节，控制结构取决于驱动怎样分配。', figure('tendon', '执行器、卷盘、腱索和关节滑轮的概念结构', '传力路径示意；实际走索与关节约束依产品而异。', '../../') + '''
## 同一传动方式，两种实现 {#implementations}

<div class="implementation-pair"><article><p class="knowledge-kicker">Shadow Classic · 2024 电驱配置</p><h3>多路输入，局部耦合</h3><p>电机模组经腱索传力，长指末节存在耦合。多路控制仍需保留这些运动约束。</p><a href="../../hands/generated/shadow-hand/">查看结构与感知档案 ↗</a></article><article><p class="knowledge-kicker">Pisa-IIT SoftHand · 论文原型</p><h3>一个输入，接触适应</h3><p>一根腱索经过关节滑轮，配合弹性韧带组织闭合。手形由输入、弹性和接触共同决定。</p><a href="../../hands/generated/pisa-iit-softhand/">查看原型与版本档案 ↗</a></article></div>

<div class="knowledge-insight"><strong>“采用腱索”并不能确定有多少独立输入。</strong><p>传力路径相同，运动分配可以不同；两种设计属于同类路线对照。</p></div>

## 对控制意味着什么？ {#control}

<div class="result-trio"><article><span>01</span><h3>保留耦合约束</h3><p>关节目标需要符合实际的驱动映射。</p></article><article><span>02</span><h3>区分测量位置</h3><p>传动侧腱负载到物体接触力，还涉及姿态与接触模型。</p></article><article><span>03</span><h3>区分自由与接触</h3><p>柔顺机构的实际手形随接触条件变化。</p></article></div>
''' + drawer(f'''结构依据：[Shadow §2.3、§4.3、§5]({SHADOW})；[SoftHand 摘要、§II、§IV]({SOFT})。控制影响是基于上述结构的工程解读，不是跨平台任务评测。

对照范围为 Shadow December 2024 电驱 Classic 与 SoftHand 论文原型。两者的同类路线关系不表示技术继承；没有实物传动误差或任务对照数据。''') + '''
<div class="knowledge-next"><a href="../underactuation-and-synergies/">欠驱动与协同 ↗</a><a href="../../engineering/transmission/">传动与标定 ↗</a><a href="../../compare/?hands=shadow-hand,pisa-iit-softhand">对照两款手 ↗</a></div>
''', eyebrow='技术路线 / 01', rail=(('implementations', '两种实现'), ('control', '控制影响')))

page('technologies/underactuation-and-synergies.md', '欠驱动与协同', '少量输入组织多关节运动；柔顺与接触让手形继续适应。', figure('synergy', '单个驱动输入通过柔顺结构在接触中产生不同手形', '自适应协同概念图；不是产品几何或走索复刻。', '../../') + '''
## 三个概念，三个不同维度 {#concepts}

<div class="result-trio"><article><span>输入维度</span><h3>欠驱动</h3><p>驱动输入少于所讨论的机构运动维度。</p></article><article><span>运动组织</span><h3>协同</h3><p>少量变量组织多关节运动，可以由软件或机构实现。</p></article><article><span>力学响应</span><h3>柔顺</h3><p>外力下允许偏离参考构型，具体来源取决于结构与控制。</p></article></div>

## SoftHand 把适应性放进了机构 {#mechanism}

<div class="mechanism-summary"><div class="mechanism-number"><strong>19</strong><span>关节</span><b>←</b><strong>1</strong><span>执行器</span></div><p>论文原型通过腱索与弹性韧带组织闭合。物体阻挡部分运动时，实际手形需要结合接触条件理解。</p></div>

<div class="knowledge-insight"><strong>简化输入，也改变了可独立指定的运动。</strong><p>执行器位置不能直接代表每个关节的实际角度。抓握适应性与精细手内操作，需要各自的任务证据。</p></div>

## 从机构研究，到应用接入 {#development}

<div class="route-continuity"><div><span>2014 / 期刊发表</span><h3>Pisa-IIT SoftHand</h3><p>自适应协同与原型抓握实验。</p></div><b>同类路线</b><div><span>2018 / 厂商回溯</span><h3>qb SoftHand Research</h3><p>单电机、柔顺抓握与协作机器人接入。</p></div></div>
''' + drawer(f'''概念与结构：[SoftHand §II、§IV]({SOFT})。19 个关节和一个执行器来自该论文原型；不推广到后续商业配置。

时间与产品记录：[IJRR 元数据](https://portal.fis.tum.de/en/publications/adaptive-synergies-for-the-design-and-control-of-the-pisaiit-soft/)、[qb 厂商回溯](https://qbrobotics.com/between-soft-technology-and-collaborative-robots/)。这里是同类路线对照，资料不足以建立逐版工程继承或独立可靠性结论。

关于观测与任务边界的说明属于基于机构约束的工程解读；没有本站实物实验数据。''') + '''
<div class="knowledge-next"><a href="../tendon-driven/">腱绳传动 ↗</a><a href="../../hands/generated/pisa-iit-softhand/">SoftHand 技术档案 ↗</a><a href="../../development/">领域发展 ↗</a></div>
''', eyebrow='技术路线 / 02', rail=(('concepts', '三个概念'), ('mechanism', '接触适应'), ('development', '研究与产品')))

page('engineering/transmission.md', '传动与标定', '读数、运动映射与物体接触，是三个不同层次。', figure('measurement', '驱动、传动、关节和接触位置的测量链', '测量位置概念图；不是三款产品共用的机构图。', '../../') + '''
## 三种实现，三种控制约束 {#comparison}

<div class="result-trio"><article><span>Shadow Classic / 2024</span><h3>多路腱传动</h3><p>关节角、腱负载与指尖触觉分别测量；末节耦合仍需保留。</p></article><article><span>LEAP v1 Full / RSS 2023</span><h3>集成舵机</h3><p>每指四轴，API 提供位置、速度、电流接口；坐标与单位需与模型对应。</p></article><article><span>SoftHand / 论文原型</span><h3>单输入协同</h3><p>接触与弹性共同影响手形，执行器位置不能给出所有关节的独立状态。</p></article></div>

## 为什么标定要分层？ {#calibration}

<div class="calibration-levels"><article><span>01</span><div><h3>读数与坐标</h3><p>单位、方向和零位决定接口与模型是否一致。</p></div><small>读数能否正确解释</small></article><article><span>02</span><div><h3>驱动与关节映射</h3><p>耦合和柔顺决定命令与实际运动之间的关系。</p></div><small>运动能否正确描述</small></article><article><span>03</span><div><h3>接触与任务</h3><p>从驱动侧反馈推到物体受力，还需要接触模型与独立验证。</p></div><small>接触能否可靠判断</small></article></div>

<div class="knowledge-insight"><strong>完成零位标定，还不能证明接触力准确。</strong><p>接口读数、机构运动和任务表现，需要对应各自的测量与证据。</p></div>
''' + drawer(f'''结构与接口依据：[Shadow §2.3、§4–5]({SHADOW})；[LEAP §III–IV]({LEAP})与[官方 API]({API})；[SoftHand §II、§IV]({SOFT})。

三层标定是基于来源组织的工程解释，尚未通过本站实物实验验证。集成舵机不因为安装在指内，就等同于无减速直驱。API main 分支会变化，接口实验应另行记录使用的提交。

本文不比较三款手的统一任务成功率或寿命。''') + '''
<div class="knowledge-next"><a href="../sensing-chain/">交互测量位置图 ↗</a><a href="../../compare/?hands=shadow-hand,leap-hand,pisa-iit-softhand">三款技术对比 ↗</a><a href="../../technologies/">技术路线 ↗</a></div>
''', eyebrow='工程图解 / 03', rail=(('comparison', '实现差异'), ('calibration', '三层标定')))

page('papers/index.md', '论文与方法', '沿着研究问题，找到原始方法与对应的技术解读。', '''
<div class="paper-library">
<article class="paper-entry"><span class="paper-year">2014<small>IJRR</small></span><div><p class="knowledge-kicker">机构与控制</p><h2>Adaptive Synergies</h2><p>通过机械自适应协同，把丰富抓形与低维驱动联系起来。</p><div class="paper-actions"><a href="../technologies/underactuation-and-synergies/">阅读图解 ↗</a><a href="''' + SOFT + '''">作者稿 ↗</a></div></div><img src="../images/knowledge/synergy.svg" alt="自适应协同的接触示意"></article>
<article class="paper-entry"><span class="paper-year">2018<small>arXiv v1</small></span><div><p class="knowledge-kicker">机器人学习</p><h2>Learning Dexterous<br>In-Hand Manipulation</h2><p>在仿真中训练物体重定向策略，结合随机化迁移到实物手。</p><div class="paper-actions"><a href="learning-dexterous-in-hand-manipulation/">阅读方法摘要 ↗</a><a href="https://arxiv.org/abs/1808.00177v5">论文 v5 ↗</a></div></div><img src="../images/knowledge/learning.svg" alt="仿真策略迁移到实物"></article>
<article class="paper-entry"><span class="paper-year">2020<small>arXiv v1</small></span><div><p class="knowledge-kicker">实验平台</p><h2>TriFinger</h2><p>以开放硬件、软件与安全检查，降低真实机器人实验门槛。</p><div class="paper-actions"><a href="../development/#trifinger-2020">查看发展节点 ↗</a><a href="https://arxiv.org/abs/2008.03596">原文 ↗</a></div></div><span class="paper-word-art" aria-hidden="true">实验<br>平台</span></article>
<article class="paper-entry"><span class="paper-year">2023<small>RSS</small></span><div><p class="knowledge-kicker">构型与学习</p><h2>LEAP Hand</h2><p>围绕机器学习实验组织四指构型、制造资料、模型与接口。</p><div class="paper-actions"><a href="leap-hand-2023/">阅读方法摘要 ↗</a><a href="''' + LEAP + '''">原文 ↗</a></div></div><img src="../images/knowledge/axes.svg" alt="LEAP v1的独立受控轴计数"></article>
</div>
''' + drawer('''条目简介转述原文或作者摘要，不代表本站复现实验。2018 与 2020 采用 arXiv 首次提交年份；SoftHand 与 LEAP 采用期刊、会议年份。

SoftHand 结构解读参考 §II、§IV；LEAP 方法摘要参考 §VI.D；OpenAI 与 TriFinger 条目限于已核查的摘要和版本信息。各阅读入口保留具体配置与范围。''') + '''
''', eyebrow='技术图谱 / 文献')

page('papers/leap-hand-2023.md', 'LEAP Hand', '四指构型、开放资源与机器人学习实验。', figure('axes', 'LEAP v1手部16个独立受控轴与Shadow含腕计数示意', '本图只解释计数范围，条长不代表任务能力。', '../../') + f'''
<div class="paper-byline">Kenneth Shaw · Ananye Agarwal · Deepak Pathak / RSS 2023 / <a href="{LEAP}">原始论文 ↗</a></div>

## 论文如何组织手内旋转？

<div class="result-trio"><article><span>训练</span><h3>PPO + Isaac Gym</h3><p>在仿真中训练方块手内旋转策略。</p></article><article><span>动作</span><h3>16 个关节角</h3><p>§VI.D 的策略输入和输出均包含关节角信息。</p></article><article><span>执行</span><h3>20 Hz 位置命令</h3><p>策略输出以该频率发送到位置控制接口。</p></article></div>

上述方法来自 [论文 §VI.D]({LEAP}#page=8)。论文中的学习系统与硬件接口，需要分别理解。
''' + drawer('''阅读范围：论文首页、运动学讨论及 §VI.D；未复现训练或核验所有性能表格。方法对应 LEAP v1 Full，不外推至 v2，也不表示产品出厂自带该策略。成本与性能依赖论文年代和条件。''') + '''
<div class="knowledge-next"><a href="../../hands/generated/leap-hand/">LEAP v1 技术档案 ↗</a><a href="../../engineering/degrees-of-freedom/">自由度与构型图解 ↗</a></div>
''', eyebrow='论文解读 / 构型与学习')

page('papers/learning-dexterous-in-hand-manipulation.md', '学习手内操作', '在仿真中训练策略，再迁移到真实 Shadow Hand。', figure('learning', '仿真训练到真实硬件的策略迁移概念图', '方法概念图；历史研究配置与当前产品配置分别阅读。', '../../') + '''
<div class="paper-byline">OpenAI 等 / arXiv v1 · 2018-08-01 / 阅读版本 v5 · 2019-01-18 / <a href="https://arxiv.org/abs/1808.00177v5">原文 ↗</a></div>

## 摘要记录的方法

<div class="result-trio"><article><span>01 / 学习</span><h3>强化学习</h3><p>在仿真中训练物体重定向策略。</p></article><article><span>02 / 迁移</span><h3>域随机化</h3><p>随机化物理参数与视觉外观。</p></article><article><span>03 / 实物</span><h3>视觉物体重定向</h3><p>作者报告将策略用于历史 Shadow Hand 系统。</p></article></div>

以上转述 [v5 摘要](https://arxiv.org/abs/1808.00177v5)，摘要同时说明方法不依赖人类示范。
''' + drawer('''阅读范围限于摘要与版本记录，未运行代码、复现实验或核验全部试验协议。历史实验使用的硬件与感知配置，不能直接套用到当前 Classic 档案的 December 2024 配置；文献实现也不等同于厂商提供完整训练系统。''') + '''
<div class="knowledge-next"><a href="../../hands/generated/shadow-hand/">Shadow Classic 技术档案 ↗</a><a href="../../development/#learning-in-hand-2018">查看发展节点 ↗</a></div>
''', eyebrow='论文解读 / 策略迁移')

page('engineering/degrees-of-freedom.md', '自由度与构型', '20 与 16 的差异，先从计数范围和运动分配读起。', figure('axes', 'Shadow手部18加腕部2，LEAP v1手部16个独立受控轴', '相同长度单位代表一个独立受控轴；耦合末节不另计，条长不代表性能。', '../../') + f'''
## 先把手部和腕部分开 {{#boundary}}

Shadow Classic 的 20 个独立受控轴包含 2 个腕部轴；只看手部时为 **18**。LEAP v1 为四指、每指四轴，共 **16**，不计外接腕。[Shadow §2.3]({SHADOW}) · [LEAP §III–IV]({LEAP})

<div class="knowledge-insight"><strong>统一计数范围，才有可解释的差异。</strong><p>18 与 16 是手部范围的计数对照，仍不能直接回答哪款手更适合某个操作任务。</p></div>

## 数量之外，还要理解运动分配 {{#structure}}

<div class="result-trio"><article><span>运动位置</span><h3>轴分配在哪里</h3><p>Shadow 的拇指与掌部运动、LEAP 的关节轴排列，决定了不同的构型特征。</p></article><article><span>运动约束</span><h3>关节是否独立</h3><p>多个可动关节可以共用输入，控制目标需要满足耦合关系。</p></article><article><span>任务条件</span><h3>接触能否形成</h3><p>指定物体与目标姿态后，才能讨论可行构型、限位与碰撞。</p></article></div>

第一项依据 [Shadow §2.3]({SHADOW}) 与 [LEAP §III、图 4–5]({LEAP})；后两项是基于机构约束的工程解读。

## 不同任务，关注不同的运动 {{#decision}}

<div class="implementation-pair"><article><p class="knowledge-kicker">人手动作映射</p><h3>关节与动作的对应关系</h3><p>五指外形之外，还需要理解拇指运动、指间协调和指尖可达位置。</p></article><article><p class="knowledge-kicker">固定物体手内重定向</p><h3>可行接触与姿态变化</h3><p>目标接触、关节余量与运动约束共同决定动作是否可实现。</p></article></div>
''' + drawer(f'''比较版本：Shadow December 2024 电驱 Classic 与 LEAP v1（RSS 2023）。手部 18 = 总计 20 − 腕部 2 是基于规格的计数推导。

依据：[Shadow 官方规格书 §2.3]({SHADOW})、[LEAP §III–IV]({LEAP})。任务说明属于工程解释，没有实物跨产品对照或已验证的性能排名。

若开展验证，运动学可行解与实物抓取成功应分别统计；求解失败还涉及初值、算法与预算。''') + '''
<div class="knowledge-next"><a href="../../compare/?hands=shadow-hand,leap-hand">两款技术对比 ↗</a><a href="../transmission/">传动与标定 ↗</a></div>
''', eyebrow='工程图解 / 01', rail=(('boundary', '计数范围'), ('structure', '运动分配'), ('decision', '任务差异')))

# Preserve the working interactive sensing component while editing its narrative.
sensing_path = 'engineering/sensing-chain.md'
old_sensing = BACKUP / sensing_path
if not old_sensing.exists():
    old_sensing.parent.mkdir(parents=True, exist_ok=True)
    old_sensing.write_bytes((DOCS / sensing_path).read_bytes())
sensing_source = old_sensing.read_text(encoding='utf-8')
sensing_component = sensing_source.split('<div markdown="0" id="dex-sensing-map"', 1)[1].split('\n## 把', 1)[0]
page(sensing_path, '力感知的测量位置', '电机电流、传动负载与指尖接触，测的是不同的量。', '''
## 沿链路选择测量位置 {#measurement-map}

<div markdown="0" id="dex-sensing-map"''' + sensing_component + f'''

## 读数怎样进入控制？ {{#judgment}}

<div class="result-trio"><article><span>电流限幅</span><h3>约束驱动侧</h3><p>电流反馈与限幅，需要按电机单位和接口解释。</p></article><article><span>接触力控制</span><h3>还需要模型与标定</h3><p>测量位置、接触方向和独立参考，决定能否解释物体受力。</p></article><article><span>触觉与滑动</span><h3>还需要识别方法</h3><p>触觉原始读数与接触或滑动识别，是不同层次的信息。</p></article></div>

<div class="knowledge-insight"><strong>“有反馈”还需说明测量量与控制目标。</strong><p>Wuji 用户须知提醒：当前电流读数不应作为外部接触力或力矩判据。驱动反馈到接触判断的链路需要独立验证。</p></div>

依据：[Wuji 用户须知](https://docs.wuji.tech/docs/zh/wuji-hand/latest/user-notice/)。其余记录可在位置图中展开原始来源；上方控制说明是工程解读。
''' + drawer(f'''版本范围：Shadow December 2024 Classic；LEAP v1 Full；Wuji 2.2 Beta 非触觉样机。数据与产品详情、对比表共用同一份感知记录。

来源：[Shadow §3.2、§4、§5]({SHADOW})；[LEAP API]({API})、[电机手册](https://emanual.robotis.com/docs/en/dxl/x/xc330-m288/)与[RSS 2023]({LEAP})；[Wuji 版本兼容性](https://docs.wuji.tech/docs/zh/wuji-hand/latest/version-compatibility/)。API 和 latest 文档会更新。

本站未开展实物实验。力估计的验证需要固定配置与单位，使用独立参考测量，并将标定条件与验证条件分开。''') + '''
<div class="knowledge-next"><a href="../../compare/?hands=shadow-hand,leap-hand,wuji-hand-2&amp;view=sensing">三款感知对比 ↗</a><a href="../transmission/">传动与标定 ↗</a></div>
''', eyebrow='工程图解 / 02', rail=(('measurement-map', '交互测量图'), ('judgment', '控制意义')))

print('Rebuilt 11 reader pages and 5 explanatory SVG figures; original pages preserved in', BACKUP)
