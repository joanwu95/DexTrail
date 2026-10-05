"""Adapt the curated notes to the same product explorer as structured records."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def coordinate_review(record, facts):
    """Explain known values and non-comparable/missing values without inventing coordinates."""
    audit = record.get("audit", {})
    gaps = dict(audit.get("gaps", {}))
    defaults = {
        "dof": "尚未核实与独立受控关节角一致的自由度定义",
        "actuators": "已读资料尚未核清该版本执行器数量",
        "year": "尚未核实首次公开年份；不以手册修订日期代替",
        "transmission": "已读资料尚不足以确定整手传动分类",
    }
    for field, reason in defaults.items():
        if record.get(field) is None:
            gaps.setdefault(field, reason)
    if not audit:
        return "", gaps
    lines = ["## 地图参数与计数口径", "",
             f"核对日期：{audit['checked_on']}。本节更新此前记录中的地图参数缺项；其他指标仍按各自证据状态阅读。", "",
             audit["explanation"], "", "| 项目 | 已知内容 / 当前状态 |", "| --- | --- |"]
    for field, label in (("dof", "自由度原始记录"), ("actuators", "执行器记录")):
        value = facts.get(field, {}).get("value")
        if value is None:
            value = record.get(field)
        value = str(value) if value is not None else gaps[field]
        lines.append(f"| {label} | {value.replace('|', ' / ')} |")
    for field, label in (("dof", "地图主动轴坐标"), ("actuators", "地图执行器坐标")):
        value = record.get(field)
        lines.append(f"| {label} | {value if value is not None else gaps[field]} |")
    lines += ["", "**依据与阅读位置：**", ""]
    lines += [f"- [{s['title']}]({s['url']})" for s in audit["sources"]]
    return "\n".join(lines), gaps


def research_records():
    rows = json.loads((ROOT / "data/report-pages.json").read_text(encoding="utf-8"))
    metrics = json.loads((ROOT / "data/research-metrics.json").read_text(encoding="utf-8"))
    hands, sources = [], []
    for row in rows:
        if not row["source"].startswith("research/"):
            continue
        slug = Path(row["source"]).stem
        content = (ROOT / row["source"]).read_text(encoding="utf-8")
        links = list(dict.fromkeys(re.findall(r"\]\((https?://[^\s)]+)\)", content)))
        ids = []
        for i, url in enumerate(links):
            sid = f"{slug}-note-source-{i}"
            ids.append(sid)
            label = next((m.group(1) for m in re.finditer(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", content)
                          if m.group(2) == url), "原始来源")
            sources.append(dict(id=sid, title=label, url=url, kind="report",
                                version="研究笔记所引用版本，见正文", verified_on="2026-10-02"))
        facts = {"model": {"value": row["name"], "sources": ids[:1]}}
        m = metrics.get(slug, {})
        coordinate_sources = []
        if m:
            url = m["source"]
            sid = f"{slug}-map-spec"
            sources.append(dict(id=sid, title=row["name"] + " · 参数依据", url=url,
                                kind=m.get("source_kind", "official"), version=m["scope"], verified_on="2026-10-02"))
            coordinate_sources = [sid]
            for k, v in m.get("facts", {}).items():
                facts[k] = dict(value=v, sources=[sid])
        audit = m.get("audit", {})
        audit_ids = []
        for i, source in enumerate(audit.get("sources", [])):
            sid = f"{slug}-coordinate-review-{i}"
            sources.append(dict(id=sid, title=row["name"] + " · " + source["title"],
                                url=source["url"], kind=source["kind"],
                                version=audit["explanation"], verified_on=audit["checked_on"]))
            audit_ids.append(sid)
        coordinate_sources.extend(audit_ids)
        ids.extend(audit_ids)
        for k, v in audit.get("facts", {}).items():
            facts[k] = dict(value=v, sources=audit_ids)
        review, gaps = coordinate_review(m, facts)
        # A selected metric should explain the missing value just as the map does.
        for field in ("dof", "actuators"):
            if audit and field not in facts and m.get(field) is None:
                facts[field] = dict(value=gaps[field], sources=audit_ids)
        if review:
            title, body = content.split("\n", 1)
            content = title + "\n\n" + review + "\n\n" + body
        # Keep the complete, cited explanations in both the inspector and the page body.
        sections = []
        for match in re.finditer(r"^#{2,3} ([^\n]+)\n(.*?)(?=^#{1,3} |\Z)", content, re.M | re.S):
            title, body = match.groups()
            if body.strip() and title not in {"首轮记录", "来源与阅读范围"}:
                sections.append(dict(title=title, markdown=body.strip()))
        hands.append(dict(id=slug, name=row["name"], venue=row.get("venue", ""), status="partial", facts=facts,
                          resources=ids, technologies=[], assessments=[],
                          note_content=content, note_sections=sections, note_summary=row["summary"],
                          coordinates=dict(dof=m.get("dof"), actuators=m.get("actuators"),
                                           year=m.get("year"), transmission=m.get("transmission"),
                                           gaps=gaps,
                                           scope=m.get("scope", "数值坐标尚待逐项核对；技术内容与来源见详情。"),
                                           sources=coordinate_sources)))
    return hands, sources
