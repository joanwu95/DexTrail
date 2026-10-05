"""Check published reader links and the common navigation after a MkDocs build."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
from urllib.parse import urlsplit, unquote

SITE = Path(__file__).resolve().parents[1] / 'website/site'
READERS = ['index.html', 'compare/index.html', 'development/index.html',
           'technologies/index.html', 'technologies/tendon-driven/index.html',
           'technologies/underactuation-and-synergies/index.html', 'engineering/index.html',
           'engineering/transmission/index.html', 'engineering/degrees-of-freedom/index.html',
           'engineering/sensing-chain/index.html', 'papers/index.html',
           'papers/leap-hand-2023/index.html', 'papers/learning-dexterous-in-hand-manipulation/index.html',
           'papers/reviews/index.html', 'papers/adaptive-synergies-2014/index.html', 'papers/trifinger-2020/index.html']


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.nav_links = set(), [], []
        self.nav_count, self.in_nav = 0, False
        self.feed(text)

    def handle_starttag(self, tag, pairs):
        attr = dict(pairs)
        if 'id' in attr:
            self.ids.add(attr['id'])
        if tag == 'nav' and 'knowledge-nav' in attr.get('class', '').split():
            self.in_nav = True
            self.nav_count += 1
        if tag == 'a' and attr.get('href'):
            self.links.append(attr['href'])
            if self.in_nav:
                self.nav_links.append(attr)
        if tag == 'img' and attr.get('src'):
            self.links.append(attr['src'])

    def handle_endtag(self, tag):
        if tag == 'nav':
            self.in_nav = False


documents = {path.resolve(): Document(path.read_text(encoding='utf-8')) for path in SITE.rglob('*.html')}
count = 0
for path, document in documents.items():
    if document.nav_count:
        assert document.nav_count == 1, f'Duplicate nav: {path}'
        assert len(document.nav_links) == 6, f'Incomplete nav: {path}'
        for link in document.nav_links:
            href = link['href']
            target = (path.parent / unquote(urlsplit(href).path)).resolve()
            if target.is_dir():
                target /= 'index.html'
            assert target.is_file(), f'Invalid navigation: {path} -> {href}'
        count += 1

checked = 0
for reader in READERS:
    path = (SITE / reader).resolve()
    assert path in documents, f'Missing reader: {path}'
    for address in documents[path].links:
        url = urlsplit(address)
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if target.is_dir():
            target /= 'index.html'
        assert target.is_file(), f'Broken link: {reader} -> {address}'
        if url.fragment and target in documents:
            assert unquote(url.fragment) in documents[target].ids, f'Broken anchor: {reader} -> {address}'
        checked += 1
print(f'PASS: common six-entry navigation on {count} pages; {checked} local reader links and images; {len(READERS)} reader pages.')

home_html = (SITE / 'index.html').read_text(encoding='utf-8')
header_pattern = r'<header class="dex-brand"[^>]*>.*?</header>'
footer_pattern = r'<footer class="dex-disclaimer"[^>]*>.*?</footer>'
shared_header = re.search(header_pattern, home_html, re.S).group()
shared_footer = re.search(footer_pattern, home_html, re.S).group()
branded = 0
for path in documents:
    text = path.read_text(encoding='utf-8')
    if documents[path].nav_count:
        assert re.findall(footer_pattern, text, re.S) == [shared_footer], f'Missing or duplicate map declaration: {path}'
    headers = re.findall(header_pattern, text, re.S)
    if headers:
        assert headers == [shared_header], f'Inconsistent site header: {path}'
        assert re.findall(footer_pattern, text, re.S) == [shared_footer], f'Inconsistent declaration: {path}'
        assert '灵巧手技术图谱' not in text, f'Obsolete header label: {path}'
        branded += 1
print(f'PASS: identical map header and declaration on {branded} branded pages.')

for reader in READERS[1:]:
    text = (SITE / reader).read_text(encoding='utf-8')
    assert text.count('knowledge-tag-rail') == 1, f'Missing or duplicate tag sidebar: {reader}'
    assert len(re.findall(r'<aside\b[^>]*\bclass="dex-rail\b', text)) == 1, f'Duplicate reading sidebar: {reader}'
    if reader in ['compare/index.html', 'development/index.html', 'technologies/index.html', 'engineering/index.html', 'papers/index.html']:
        assert 'class="hand-heading"' not in text, f'Duplicate section title: {reader}'
        assert text.count('knowledge-section-purpose') == 1, f'Missing section description: {reader}'
history = (SITE / 'development/index.html').read_text(encoding='utf-8')
events = json.loads((SITE.parents[1] / 'data/field-development.json').read_text(encoding='utf-8'))['events']
assert len(re.findall(r'<article class="history-event [^"]+" data-topic-item="1" data-topic-tags="[^"]+"', history)) == len(events)
profiles = list(SITE.glob('hands/generated/*/index.html'))
assert profiles, 'Missing product profiles'
print(f'PASS: one tag sidebar per reader; section titles appear only in navigation; all {len(events)} history nodes are tagged; declaration present on all {count} content pages, including {len(profiles)} product profiles.')
