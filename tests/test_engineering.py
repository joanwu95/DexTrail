"""Check the full Markdown-to-HTML boundary used by engineering readers."""
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

import markdown

ROOT = Path(__file__).resolve().parents[1]


def hook(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f'website/hooks/{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


engineering = hook('engineering')
knowledge = hook('knowledge')


class Structure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.items = []
        self.invalid = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and 'a' in self.stack:
            self.invalid.append('nested link')
        if tag in {'div', 'h2', 'h3', 'ol', 'table'} and 'p' in self.stack:
            self.invalid.append('block inside paragraph')
        if attrs.get('data-topic-item'):
            self.items.append(attrs)
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        if tag not in {'img','br','input','hr','meta','link','source','wbr'}:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.stack:
            self.stack = self.stack[:len(self.stack) - 1 - self.stack[::-1].index(tag)]


def render(file):
    uri = 'engineering/' + file.name
    page = SimpleNamespace(file=SimpleNamespace(src_uri=uri), url=uri.replace('.md','/'))
    text = engineering.on_page_markdown(file.read_text(encoding='utf-8'), page, {}, [])
    html = markdown.markdown(text, extensions=['admonition','attr_list','md_in_html','tables','toc','pymdownx.superfences'], extension_configs={'toc': {'permalink': True}})
    return knowledge.on_page_content(html, page, {}, [])


class EngineeringTest(unittest.TestCase):
    def test_hub_has_exactly_eight_complete_filterable_links(self):
        html = render(ROOT / 'website/docs/engineering/index.md')
        parsed = Structure()
        parsed.feed(html)
        self.assertEqual(parsed.invalid, [])
        self.assertEqual(len(parsed.items), 8)
        nav = json.loads((ROOT / 'data/knowledge-navigation.json').read_text(encoding='utf-8'))
        for item, expected in zip(parsed.items, nav['pages']['engineering/index.md']['items']):
            target = ROOT / 'website/docs/engineering' / item['href'].strip('/')
            self.assertTrue(target.with_suffix('.md').is_file(), item['href'])
            self.assertEqual(item['data-topic-tags'].split(), expected['tags'])

    def test_articles_render_diagrams_and_keep_their_reading_anchors(self):
        for file in (ROOT / 'website/docs/engineering').glob('*.md'):
            if file.name == 'index.md':
                continue
            with self.subTest(page=file.name):
                html = render(file)
                parsed = Structure()
                parsed.feed(html)
                self.assertEqual(parsed.invalid, [])
                self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
                for anchor in re.findall(r'class="dex-scroll-nav"[^>]*>(.*?)</nav>', html, re.S):
                    for target in re.findall(r'href="#([^"]+)"', anchor):
                        self.assertIn(target, parsed.ids)
                self.assertNotIn('engineering:diagram', html)
                self.assertIn('class="eng-figure"', html)
                self.assertIn('https://', html)

    def test_unknown_diagram_stops_build_instead_of_silently_disappearing(self):
        page = SimpleNamespace(file=SimpleNamespace(src_uri='engineering/test.md'))
        with self.assertRaises(ValueError):
            engineering.on_page_markdown('<!-- engineering:diagram unknown -->', page, {}, [])


if __name__ == '__main__':
    unittest.main()
