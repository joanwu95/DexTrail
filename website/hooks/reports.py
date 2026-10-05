"""Publish curated research notes without duplicating their Markdown sources."""
import html
import json
from pathlib import Path, PurePosixPath

from mkdocs.exceptions import ConfigurationError
from mkdocs.structure.files import File

ROOT = Path(__file__).resolve().parents[2]


def on_files(files, config):
    rows = json.loads((ROOT / "data/report-pages.json").read_text(encoding="utf-8"))
    seen = set()
    cards = ["# 灵巧手技术资料", "",
             f"已接入 **{len(rows)} 份**深入整理资料。每份保留来源、技术解释与待补证据；目前均处于核查补充阶段。",
             "",
             '<div class="hand-directory" markdown>', ""]
    entries = [{"全部资料": "hands/reports/index.md"}]
    for row in rows:
        source = (ROOT / row["source"]).resolve()
        uri = row["page"]
        if not source.is_relative_to(ROOT) or not source.is_file() or uri in seen:
            raise ConfigurationError(f"资料清单路径不存在或重复：{row}")
        seen.add(uri)
        if not row["source"].startswith("website/docs/"):
            if files.get_file_from_path(uri):
                raise ConfigurationError(f"资料页面与现有文件冲突：{uri}")
            content = source.read_text(encoding="utf-8")
            content = content.replace("(../papers/dextreme.md)", "(references/dextreme.md)")
            files.append(File.generated(config, uri, content=content))
        elif files.get_file_from_path(uri) is None:
            raise ConfigurationError(f"既有报告页面缺失：{uri}")
        cards += [f"- **[{row['name']}]({Path(uri).name})**", "",
                  f"    {row['summary']}", "",
                  f"    待补：{row['gaps']}。", ""]
        entries.append({row["name"]: uri})
    cards += ["</div>"]
    files.append(File.generated(config, "hands/reports/index.md", content="\n".join(cards)))
    files.append(File.generated(
        config, "hands/reports/references/dextreme.md",
        content=(ROOT / "research/collection/papers/dextreme.md").read_text(encoding="utf-8")))
    for group in config.nav:
        if "技术资料" in group:
            group["技术资料"] = entries
    config.extra["report_pages"] = seen
    hands = config.extra["atlas_data"]["hands"]
    config.extra["report_hand_ids"] = {}
    for row in rows:
        match = next((hand for hand in hands
                      if hand.get("analysis_page") == row["page"]
                      or hand["id"] == Path(row["source"]).stem), None)
        if match:
            config.extra["report_hand_ids"][row["page"]] = match["id"]
    return files


def on_page_markdown(markdown, page, config, files):
    uri = page.file.src_uri
    reports = config.extra.get("report_pages", set())
    legacy = {"hands/shadow-hand.md": "shadow-hand", "hands/leap-hand.md": "leap-hand"}
    if uri not in reports and uri not in legacy and uri not in {
        "hands/index.md", "hands/reports/index.md"
    }:
        return markdown

    # All published reports keep their source body and links, but use the same
    # open canvas as product profiles. Hide the Material chrome for this layout.
    page.meta["hide"] = ["navigation", "toc", "footer"]
    title, _, body = markdown.partition("\n")
    title = html.escape(title.removeprefix("# ").strip())
    depth = len(PurePosixPath(uri).parent.parts)
    if config.use_directory_urls and PurePosixPath(uri).name != "index.md":
        depth += 1
    home = "../" * depth
    hand_id = config.extra.get("report_hand_ids", {}).get(uri, legacy.get(uri))
    if hand_id:
        back = f'{home}hands/generated/{hand_id}/'
        back_label = "← 产品详情"
    else:
        back, back_label = home, "← 返回产品地图"
    report_link = f'<a href="{home}hands/reports/">全部技术资料 ↗</a>' if uri in reports else ''
    directory_search = ''
    if uri in {"hands/index.md", "hands/reports/index.md"}:
        directory_search = ('<div class="hand-directory-search">'
                            '<label for="directory-search">查找产品</label>'
                            '<input id="directory-search" type="search" data-directory-search placeholder="产品名称或技术关键词…">'
                            '<span class="hand-directory-count" role="status"></span></div>')
    return '\n\n'.join([
        '<div class="dex-hand-page dex-report-page" markdown="1">',
        f'<header class="hand-brand"><a class="hand-brand-name" href="{home}">'
        f'<img class="dex-emblem" src="{home}images/brand/dextrail-fingerprint-original.svg" alt="">'
        f'DexTrail<span>.</span></a><a class="hand-back" href="{back}">{back_label}</a></header>',
        f'<div class="hand-heading"><h1>{title}</h1>{report_link}</div>',
        '<div class="hand-report-body" markdown="1">',
        directory_search,
        body,
        '</div>',
        '</div>',
    ])
