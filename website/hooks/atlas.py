"""Validate atlas YAML and generate virtual pages without overwriting notes."""
from datetime import date
from pathlib import Path, PurePosixPath
import re
import json
import html
import importlib.util
import markdown as markdown_library
from urllib.parse import urlsplit

import yaml
from mkdocs.exceptions import ConfigurationError
from mkdocs.structure.files import File

ROOT = Path(__file__).resolve().parents[2]
_detail_spec = importlib.util.spec_from_file_location("product_details", ROOT / "website/hooks/product_details.py")
product_details = importlib.util.module_from_spec(_detail_spec)
_detail_spec.loader.exec_module(product_details)
_comparison_spec = importlib.util.spec_from_file_location("comparison", ROOT / "website/hooks/comparison.py")
comparison = importlib.util.module_from_spec(_comparison_spec)
_comparison_spec.loader.exec_module(comparison)
STATUS = {"planned": "计划收录", "scaffold": "结构示例 / 待核验", "researched": "已整理", "partial": "已有深入资料 · 补证中"}
EVIDENCE = {"official": "官方支持", "paper": "文献实现", "experiment": "本人验证"}
FIELDS = {
    "model": "型号 / 版本", "company": "公司 / 机构", "country": "国家",
    "year": "时间定位与依据", "application": "应用", "product_status": "产品状态",
    "fingers": "手指数", "dof": "自由度（注明主动 / 被动）",
    "actuators": "驱动数量", "weight": "重量（含单位）",
    "dimensions": "尺寸（含单位）", "materials": "材料",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe_page(value, docs):
    require(isinstance(value, str) and "\\" not in value, "页面路径必须使用正斜杠")
    path = PurePosixPath(value)
    require(not path.is_absolute() and ".." not in path.parts and ":" not in value
            and path.suffix == ".md", f"非法页面路径: {value}")
    require((docs / value).is_file(), f"页面不存在: {value}")
    require((docs / value).resolve().is_relative_to(docs.resolve()), "页面越过 docs 边界")


def load_data(data_dir, docs):
    data = {}
    for filename, key, version in [
        ("hands", "hands", 2), ("technologies", "dimensions", 1),
        ("sources", "sources", 1), ("projects", "projects", 1),
    ]:
        document = yaml.safe_load((data_dir / f"{filename}.yaml").read_text(encoding="utf-8"))
        require(isinstance(document, dict) and document.get("schema_version") == version,
                f"{filename}: schema_version 应为 {version}")
        require(isinstance(document.get(key), list), f"{filename}: {key} 必须是列表")
        data[key] = document[key]

    module_spec = importlib.util.spec_from_file_location("research_hands", ROOT / "website/hooks/research_hands.py")
    adapter = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(adapter)
    extra_hands, extra_sources = adapter.research_records()
    # Specific models replace the old family placeholders.
    replaced = {"allegro-hand", "dlr-hand", "barrett-hand", "xynova-flex-series"}
    data["hands"] = [h for h in data["hands"] if h["id"] not in replaced] + extra_hands
    data["sources"].extend(extra_sources)

    def index(rows, label):
        result = {}
        for row in rows:
            require(isinstance(row, dict), f"{label} 条目必须是对象")
            identifier = row.get("id", "")
            require(isinstance(identifier, str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier),
                    f"{label}: 非法 ID {identifier}")
            require(identifier not in result, f"{label}: 重复 ID {identifier}")
            result[identifier] = row
        return result

    hands = index(data["hands"], "hands")
    coordinates = json.loads((data_dir / "map-coordinates.json").read_text(encoding="utf-8"))
    timeline = json.loads((data_dir / "hand-timeline.json").read_text(encoding="utf-8"))
    labels = {"document": "公开资料", "paper": "论文", "release": "产品公告", "demonstration": "公开展示"}
    require(set(timeline) <= set(hands), "时间记录引用了不存在的产品")
    for identifier, hand in hands.items():
        if identifier in coordinates:
            hand["coordinates"] = coordinates[identifier]
        if identifier not in timeline:
            continue
        record = timeline[identifier]
        require(type(record.get("year")) is int and 1900 <= record["year"] <= date.today().year,
                f"{identifier}: 非法时间年份")
        require(record.get("basis") in labels and record.get("relation") in {"by", "event"},
                f"{identifier}: 非法时间口径")
        month = record.get("month")
        require(month is None or type(month) is int and 1 <= month <= 12,
                f"{identifier}: 非法时间月份")
        require(bool(record.get("detail")), f"{identifier}: 时间记录必须解释依据")
        source = record.get("source", {})
        require(bool(source.get("title")) and bool(source.get("url")), f"{identifier}: 时间记录必须提供证据")
        source_id = identifier + "-timeline"
        data["sources"].append({**source, "id": source_id, "version": record["detail"],
                                "verified_on": record.get("verified_on")})
        stamp = str(record['year']) + (f"-{month:02d}" if month is not None else "")
        label = f"{'≤ ' if record['relation'] == 'by' else ''}{stamp} · {labels[record['basis']]}"
        hand["timeline"] = {**record, "label": label, "source_id": source_id}
        hand.setdefault("coordinates", {})["year"] = record["year"]
        hand["coordinates"].get("gaps", {}).pop("year", None)
        hand.setdefault("facts", {})["year"] = {"value": label + "。" + record["detail"], "sources": [source_id]}
        hand.setdefault("resources", []).append(source_id)
    sources = index(data["sources"], "sources")
    index(data["dimensions"], "dimensions")
    index(data["projects"], "projects")
    terms = []
    for dimension in data["dimensions"]:
        require(isinstance(dimension.get("name"), str) and dimension["name"].strip(), "分类缺少名称")
        require(isinstance(dimension.get("terms"), list), "分类缺少 terms 列表")
        terms.extend(dimension["terms"])
    technology_index = index(terms, "technologies")
    for term in terms:
        require(isinstance(term.get("name"), str) and term["name"].strip(), "技术缺少名称")
        if term.get("page"):
            safe_page(term["page"], docs)

    def refs(values, target, label, required=False):
        require(isinstance(values, list), f"{label} 必须是列表")
        require(not required or bool(values), f"{label} 必须提供证据")
        require(all(isinstance(v, str) and v in target for v in values), f"{label} 引用了不存在的 ID")

    for source in sources.values():
        for field in ("title", "url", "kind", "version", "verified_on"):
            require(source.get(field) is not None, f"来源缺少 {field}")
        require(source["kind"] in {"official", "paper", "report", "repository", "video", "community"},
                "非法来源类型")
        address = urlsplit(str(source["url"]))
        require(address.scheme in {"https", "http"} and address.netloc, "来源 URL 必须为 HTTP(S)")
        date.fromisoformat(str(source["verified_on"]))

    for hand in hands.values():
        require(isinstance(hand.get("name"), str) and hand["name"].strip(), "产品缺少名称")
        require(hand.get("status") in STATUS, "非法产品状态")
        if hand.get("analysis_page"):
            safe_page(hand["analysis_page"], docs)
        facts = hand.get("facts", {})
        require(isinstance(facts, dict), "facts 必须是对象")
        require(set(facts) <= set(FIELDS), "存在未知参数字段")
        for field, fact in facts.items():
            require(isinstance(fact, dict) and "value" in fact, f"{field} 必须包含 value")
            require(fact["value"] is None or isinstance(fact["value"], (str, int, float, bool)),
                    f"{field} 必须是标量")
            refs(fact.get("sources", []), sources, field, fact["value"] is not None)
        for key in ("technologies", "assessments", "resources"):
            require(isinstance(hand.get(key, []), list), f"{key} 必须是列表")
        for relation in hand.get("technologies", []):
            require(isinstance(relation, dict), "技术关联必须是对象")
            require(relation.get("id") in technology_index, "未知技术 ID")
            require(relation.get("evidence_type") in EVIDENCE, "缺少有效的能力证据类型")
            require(bool(relation.get("scope")), "技术关联必须说明型号、版本与条件")
            refs(relation.get("sources", []), sources, "技术关联", True)
            require(isinstance(relation.get("explanation", []), list), "技术解释必须是列表")
            for item in relation.get("explanation", []):
                require(isinstance(item, dict) and item.get("kind") in {"fact", "interpretation"}
                        and bool(item.get("title")) and bool(item.get("text")), "技术解释缺少类型、标题或内容")
        for claim in hand.get("assessments", []):
            require(isinstance(claim, dict), "评价必须是对象")
            require(claim.get("kind") in {"fact", "reported_limitation", "interpretation"}, "非法陈述类型")
            require(bool(claim.get("text")) and bool(claim.get("scope")), "评价缺少内容或适用条件")
            refs(claim.get("sources", []), sources, "评价", True)
        refs(hand.get("resources", []), sources, "资源")
        if hand["status"] == "researched":
            require(facts.get("model", {}).get("value") is not None, "已整理产品必须明确型号")

    for project in data["projects"]:
        require(project.get("status") in {"planned", "in-progress", "completed"}, "非法案例状态")
        require(bool(project.get("name")) and bool(project.get("summary")), "案例缺少名称或摘要")
        safe_page(project.get("page"), docs)
        refs(project.get("hand_ids", []), hands, "案例产品")
        refs(project.get("technology_ids", []), technology_index, "案例技术")
        refs(project.get("source_ids", []), sources, "案例来源")
    data["source_index"] = sources
    data["technology_index"] = technology_index
    data['sensing_audits'] = product_details.sensing.load(
        data_dir / 'sensing-audits.json', hands, technology_index, require)
    data['editorials'] = product_details.editorials.load(data_dir / 'product-editorials.json', hands, require)
    return data


def text(value):
    """Escape YAML scalar values for Markdown, including table cells."""
    if value is None:
        return "待核验"
    value = str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for symbol in ("\\", "`", "*", "_", "[", "]", "|"):
        value = value.replace(symbol, "\\" + symbol)
    return value.replace("\n", " ").replace("\r", " ")


def source_links(ids, data):
    return " · ".join(
        f"[{text(data['source_index'][identifier]['title'])}](<{data['source_index'][identifier]['url']}>)"
        for identifier in ids
    ) or "待补充"


def cards(data, prefix):
    rows = ['<div class="hand-directory" markdown>', ""]
    for hand in data["hands"]:
        rows += [f"- **{text(hand['name'])}**", "",
                 f"    {STATUS[hand['status']]}", "",
                 f"    机构：{text(hand.get('facts', {}).get('company', {}).get('value'))}", ""]
        tags = [data["technology_index"][r["id"]]["name"] for r in hand.get("technologies", [])]
        rows += [f"    技术标签：{text(' / '.join(tags)) if tags else '待核验'}", ""]
        if hand["status"] != "planned":
            rows += [f"    [查看参数与证据]({prefix}hands/generated/{hand['id']}.md)", ""]
        else:
            rows += ["    型号与资料待核验。", ""]
    return "\n".join(rows + ["</div>"])


def hand_page(hand, data):
    return product_details.product_page(hand, data, FIELDS, text, source_links)


def technology_map(data):
    rows = []
    for dimension in data["dimensions"]:
        rows += [f"## {text(dimension['name'])} {{ #{dimension['id']} }}", ""]
        for term in dimension["terms"]:
            description = (f"[阅读原理、实现差异与工程取舍](../{term['page']})"
                           if term.get("page") else "定义、分类依据和工程权衡待核验。")
            rows += [f"### {text(term['name'])} {{ #{term['id']} }}", "", description, ""]
            associated = [
                h for h in data["hands"] if h["status"] != "planned"
                and any(r["id"] == term["id"] for r in h.get("technologies", []))
            ]
            rows += [f"- [{text(h['name'])}](../hands/generated/{h['id']}.md)" for h in associated] or ["暂无已核验的产品关联。"]
            for project in data["projects"]:
                if term["id"] in project.get("technology_ids", []):
                    rows += [f"- 研究案例（{project['status']}）：[{text(project['name'])}](../{project['page']})"]
            rows.append("")
    return "\n".join(rows)


def project_index(data):
    rows = []
    labels = {"planned": "计划中", "in-progress": "进行中", "completed": "已完成"}
    for project in data["projects"]:
        rows += [f"## [{text(project['name'])}](../{project['page']})", "",
                 f"**{labels[project['status']]}** · {text(project['summary'])}", ""]
    return "\n".join(rows) or "暂无案例。"


def source_index(data):
    rows = ["## 来源登记", ""]
    for source in data["sources"]:
        rows += [f"- {source_links([source['id']], data)} · {text(source['kind'])}"
                 f" · 版本：{text(source['version'])} · 核验：{text(source['verified_on'])}"]
    return "\n".join(rows + ([] if data["sources"] else ["尚无已登记来源。"]))


def graph(data, hand_id=None):
    """Only validated YAML relations become evidence edges; no inferred links."""
    payload = {
        "dimensions": data["dimensions"], "hands": data["hands"],
        "sources": data["sources"], "projects": data["projects"],
        "hand": hand_id,
    }
    encoded = html.escape(json.dumps(payload, ensure_ascii=False, default=str), quote=True)
    return (
        f'<div class="atlas-map" data-atlas-map="{encoded}">'
        '<p class="atlas-map-loading">交互地图加载中。完整参数与来源仍可在下方阅读。</p>'
        '<noscript>启用 JavaScript 可查看交互关系图；下方文字资料可正常阅读。</noscript>'
        '</div>'
    )


def map_payload(data):
    """Use the same validated records for the map and detail pages."""
    media = json.loads((ROOT / "data/media.json").read_text(encoding="utf-8"))
    hands = []
    for original in data["hands"]:
        if original["status"] == "planned":
            continue
        hand = {k: v for k, v in original.items() if k not in {"note_content", "note_sections"}}
        hand.update(short=hand["name"], media=media.get(hand["id"]))
        hand['classification'] = product_details.classification(hand, data)
        hands.append(hand)
    systems = json.loads((ROOT / "data/related-systems.json").read_text(encoding="utf-8"))
    return {"hands": hands, "systems": systems, "sources": data["sources"], "dimensions": data["dimensions"]}


def on_files(files, config):
    try:
        data = load_data(ROOT / "data", Path(config.docs_dir))
    except (ValueError, TypeError, KeyError, OSError, yaml.YAMLError) as error:
        raise ConfigurationError(f"Atlas 数据校验失败：{error}") from error
    # Store on this build's config so live reload never reuses stale data.
    config.extra["atlas_data"] = data
    files.append(File.generated(config, "comparison-data.json", content=json.dumps(
        comparison.payload(data, product_details.classification), ensure_ascii=False, default=str)))
    files.append(File.generated(config, 'sensing-data.json', content=json.dumps(
        product_details.sensing.payload(data), ensure_ascii=False)))
    # Replace the checked-in preview export in memory on every build/live reload.
    uri = "visual-lab/specimens.json"
    previous = files.get_file_from_path(uri)
    if previous is not None:
        files.remove(previous)
    files.append(File.generated(config, uri, content=json.dumps(map_payload(data), ensure_ascii=False, default=str)))
    entries = [{"数据库": "hands/index.md"}]
    for hand in data["hands"]:
        if hand["status"] != "planned":
            uri = f"hands/generated/{hand['id']}.md"
            require(files.get_file_from_path(uri) is None, f"生成路径与手写文件冲突：{uri}")
            files.append(File.generated(config, uri, content=hand_page(hand, data)))
            entries.append({hand["name"]: uri})
        if hand.get("analysis_page"):
            entries.append({f"{hand['name']} · 工程分析": hand["analysis_page"]})
    entries.append({"工程分析模板": "hands/template.md"})
    for group in config.nav:
        if "灵巧手数据库" in group:
            group["灵巧手数据库"] = entries
    return files


def on_page_markdown(markdown, page, config, files):
    data = config.extra["atlas_data"]
    prefix = "../" * len(PurePosixPath(page.file.src_uri).parent.parts)
    replacements = {
        "<!-- atlas:hand-count -->": lambda: str(sum(h["status"] != "planned" for h in data["hands"])),
        "<!-- atlas:map -->": lambda: graph(data),
        "<!-- atlas:hands -->": lambda: cards(data, prefix),
        "<!-- atlas:technologies -->": lambda: technology_map(data),
        "<!-- atlas:projects -->": lambda: project_index(data),
        "<!-- atlas:sources -->": lambda: source_index(data),
    }
    for marker, render in replacements.items():
        if marker in markdown:
            markdown = markdown.replace(marker, render())
    return markdown
