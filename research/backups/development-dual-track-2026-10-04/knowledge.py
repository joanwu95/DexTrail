"""Render sourced field history independently of product release coordinates."""
from datetime import date
import html
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from mkdocs.utils import get_relative_url

ROOT = Path(__file__).resolve().parents[2]
TRACKS = {"academic": "学术研究", "industry": "工业产品与研究合作"}
BASIS = {"publication": "论文发表", "preprint": "预印本提交", "public-demonstration": "公开展示", "announcement": "厂商公告", "retrospective": "厂商回溯记录"}
RELATIONS = {"same-route": "同类路线 · 非继承证明", "comparison": "问题对照 · 非继承证明", "documented-transfer": "来源明确说明的转化"}


def validate(document, hands):
    def require(condition, message):
        if not condition:
            raise ValueError(message)
    require(document.get("schema_version") == 1, "领域发展：未知 schema_version")
    sources = document.get("sources", {})
    require(isinstance(sources, dict) and bool(sources), "领域发展：缺少来源")
    for source in sources.values():
        address = urlsplit(source.get("url", ""))
        require(address.scheme in {"http", "https"} and bool(address.netloc), "领域发展：非法来源 URL")
        require(all(source.get(key) for key in ("title", "kind", "locator", "verified_on")), "领域发展：来源缺少核验范围")
        require(source["kind"] in {"official", "paper", "repository"}, "领域发展：非法来源类型")
        date.fromisoformat(source["verified_on"])
    identifiers = set()
    for event in document.get("events", []):
        identifier = event.get("id", "")
        require(bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier)) and identifier not in identifiers, "领域发展：重复或非法事件 ID")
        identifiers.add(identifier)
        require(event.get("track") in TRACKS and event.get("basis") in BASIS, "领域发展：非法轨道或时间口径")
        stamp = event.get("date", "")
        require(bool(re.fullmatch(r"\d{4}(?:-\d{2}(?:-\d{2})?)?", stamp)), "领域发展：非法日期")
        # Missing month/day stays missing; validate partial precision without inventing it.
        padded = stamp + ("-01-01" if len(stamp) == 4 else "-01" if len(stamp) == 7 else "")
        require(date.fromisoformat(padded) <= date.today(), "领域发展：日期不能在未来")
        require(event.get("date_relation") in {"on", "by"}, "领域发展：缺少日期边界")
        require(all(event.get(key) for key in ("title", "date_note", "problem", "approach", "evidence", "boundary", "focus")), "领域发展：事件缺少问题或证据边界")
        require(bool(event.get("source_ids")) and all(key in sources for key in event["source_ids"]), "领域发展：事件引用未知来源")
        require(all(key in hands for key in event.get("hand_ids", [])), "领域发展：事件引用未知产品")
    require(bool(identifiers), "领域发展：缺少事件")
    for relation in document.get("relations", []):
        require(relation.get("kind") in RELATIONS, "领域发展：非法关系类型")
        require(relation.get("from") in identifiers and relation.get("to") in identifiers and relation["from"] != relation["to"], "领域发展：关系引用未知或相同事件")
        require(bool(relation.get("text")) and bool(relation.get("source_ids")) and all(key in sources for key in relation["source_ids"]), "领域发展：关系缺少依据")
    return document


def render(document):
    esc = html.escape
    def source_links(keys):
        return " · ".join(f'<a href="{esc(document["sources"][key]["url"], quote=True)}">{esc(document["sources"][key]["title"])}</a>' for key in keys)
    events = sorted(document["events"], key=lambda event: (event["date"], event["id"]))
    rows = ['<div markdown="0" class="history-legend"><span>● 学术研究</span><span>◆ 工业产品与研究合作</span></div><div markdown="0" class="history-timeline" aria-label="学术与工业发展时间轴">']
    for year in sorted({event["date"][:4] for event in events}):
        rows.append(f'<section class="history-year"><div class="history-date">{year}</div><div class="history-entries">')
        for event in [item for item in events if item["date"].startswith(year)]:
            stamp = ("≤ " if event["date_relation"] == "by" else "") + event["date"]
            symbol = "●" if event["track"] == "academic" else "◆"
            rows += [f'<article class="history-event {event["track"]}" id="{esc(event["id"])}"><p class="field-meta">{symbol} {TRACKS[event["track"]]}<span>{esc(event["focus"])}</span></p><h3>{esc(event["title"])}</h3><p class="history-approach">{esc(event["approach"])}</p><details class="evidence-drawer"><summary>问题与证据 ↗</summary><p class="field-meta">{esc(stamp)} · {TRACKS[event["track"]]} · {BASIS[event["basis"]]}</p><p>{esc(event["date_note"])}</p><dl>']
            for key, label in [("problem", "研究或应用问题"), ("evidence", "来源记录"), ("boundary", "适用范围")]:
                rows.append(f'<dt>{label}</dt><dd>{esc(event[key])}</dd>')
            rows += [f'</dl><p class="field-sources">{source_links(event["source_ids"])}</p></details>']
            if event.get("hand_ids"):
                links = " · ".join(f'<a href="../hands/generated/{esc(key)}/">{esc(event.get("hand_names", {}).get(key, key))} ↗</a>' for key in event["hand_ids"])
                rows.append(f'<p class="history-product">{links}</p>')
            rows.append('</article>')
        rows.append('</div></section>')
    rows += ['</div>', '<h2 id="focus">关注点如何展开</h2>',
             '<p class="knowledge-caption">以下是对上述代表案例的工程解读；多种研究目标可以长期并存。</p>',
             '<div markdown="0" class="result-trio"><article><span>机构与控制</span><h3>适应性由谁承担？</h3><p><a href="#adaptive-synergies-2014">SoftHand</a> 将一部分适应性放进机构，连接了机械设计与低维控制。</p></article><article><span>控制与学习</span><h3>策略如何进入实物？</h3><p><a href="#learning-in-hand-2018">手内重定向研究</a> 把仿真与真实系统的差异纳入训练与迁移问题。</p></article><article><span>研究与工程</span><h3>实验怎样持续开展？</h3><p><a href="#trifinger-2020">TriFinger</a>、<a href="#leap-2023">LEAP</a> 与 <a href="#dexee-2024">DEX-EE</a> 分别强调开放资源、可获得性和长期实验维护。</p></article></div>',
             '<h2 id="relationships">路线的延续与共同问题</h2>']
    by_id = {event["id"]: event for event in events}
    for relation in document.get("relations", []):
        rows.append(f'<details class="evidence-drawer field-relation"><summary>{esc(by_id[relation["from"]]["title"].split("：")[0])} × {esc(by_id[relation["to"]]["title"].split("：")[0])}</summary><p class="field-meta">{RELATIONS[relation["kind"]]}</p><p>{esc(relation["text"])}</p><p class="field-sources">{source_links(relation["source_ids"])}</p></details>')
    rows.append(f'<details class="evidence-drawer" id="sources"><summary>来源与时间口径 · {len(document["sources"])} 项原始资料</summary><p>时间采用论文、公开展示或厂商记录，各节点分别注明。选入的代表案例不构成完整年表或研究热度统计。</p><ul class="field-source-register">')
    for source in document["sources"].values():
        rows.append(f'<li><a href="{esc(source["url"], quote=True)}">{esc(source["title"])}</a><span>{esc(source["locator"])} · 复核 {esc(source["verified_on"])}</span></li>')
    rows.append('</ul></details>')
    return "\n".join(rows).replace('><', '>\n<')


def on_files(files, config):
    from mkdocs.exceptions import ConfigurationError
    try:
        document = json.loads((ROOT / "data/field-development.json").read_text(encoding="utf-8"))
        hands = {hand["id"] for hand in config.extra["atlas_data"]["hands"]}
        config.extra["field_development"] = validate(document, hands)
    except (ValueError, TypeError, KeyError, OSError) as error:
        raise ConfigurationError(f"领域发展数据校验失败：{error}") from error
    return files


def on_page_markdown(markdown, page, config, files):
    marker = "<!-- knowledge:development -->"
    if marker in markdown:
        return markdown.replace(marker, render(config.extra["field_development"]))
    return markdown


def on_page_content(content, page, config, files):
    """One navigation contract for map, articles, generated records and legacy docs."""
    destinations = [("index.html", "产品地图", "map"), ("development/", "领域发展", "development"),
                    ("technologies/", "技术路线", "technologies"), ("engineering/", "工程问题", "engineering"),
                    ("papers/", "论文与方法", "papers"), ("compare/", "技术对比", "compare")]
    uri = page.file.src_uri
    section = "map" if uri == "index.md" or uri.startswith(("hands/", "systems/")) else uri.split("/")[0].replace(".md", "")
    links = []
    for target, label, key in destinations:
        address = get_relative_url(target, page.url)
        if key == "map":
            address = get_relative_url("./", page.url)
        current = ' aria-current="page"' if section == key else ""
        links.append(f'<a href="{html.escape(address, quote=True)}"{current}>{label}</a>')
    nav = '<nav class="knowledge-nav" aria-label="知识地图入口">' + "".join(links) + '</nav>'
    content = re.sub(r'<nav class="knowledge-nav[^\"]*"[^>]*>.*?</nav>', '', content, flags=re.S)
    header = re.search(r'<header class="(?:hand-brand|dex-brand)"[^>]*>.*?</header>', content, re.S)
    if header:
        return content[:header.end()] + nav + content[header.end():]
    return nav + content
