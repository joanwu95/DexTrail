"""Guard all concept assets and the Markdown boundary of the three-zone reader."""
import importlib.util
from html.parser import HTMLParser
from pathlib import Path
import unittest
import markdown

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('concepts', ROOT / 'website/hooks/concepts.py')
concepts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(concepts)


class Reader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.entries = []
        self.images = []
        self.rails = []

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        inside = any('concept-page' in classes.split() for _, classes in self.stack)
        if 'concept-entry' in attrs.get('class', '').split():
            self.entries.append((attrs['id'], inside))
        if 'concept-tag-rail' in attrs.get('class', '').split():
            self.rails.append(inside)
        if tag == 'img' and 'data-poster' in attrs:
            self.images.append(attrs)
        if tag not in {'img', 'input', 'br', 'hr', 'meta', 'link'}:
            self.stack.append((tag, attrs.get('class', '')))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                self.stack = self.stack[:i]
                break


class ConceptTest(unittest.TestCase):
    def test_every_entry_uses_a_present_web_asset_and_a_source(self):
        groups, entries = concepts.catalog()
        self.assertEqual(len(entries), 31)
        self.assertEqual(sum(bool(entry.get('animated')) for entry in entries), 18)
        for entry in entries:
            self.assertIn(entry['group'], groups)
            self.assertTrue(entry['sources'])
            self.assertTrue(entry['image'].startswith(concepts.WEB + '/'))

    def test_reader_rail_and_all_images_survive_markdown_rendering(self):
        source = (ROOT / 'website/docs/concepts/index.md').read_text(encoding='utf-8')
        source = source.split('---', 2)[2].replace('<!-- concept-index -->', concepts.render_index())
        rendered = markdown.markdown(source, extensions=['extra', 'md_in_html', 'toc'])
        parser = Reader()
        parser.feed(rendered)
        self.assertEqual(len(parser.entries), 31)
        self.assertTrue(all(inside for _, inside in parser.entries))
        self.assertEqual(parser.rails, [True])
        self.assertEqual(len(parser.images), 31)
        animations = [image for image in parser.images if 'data-animation' in image]
        self.assertEqual(len(animations), 18)
        self.assertTrue(all(image['src'] == image['data-animation'] for image in animations))
        self.assertNotIn('播放动图</button>', rendered)


if __name__ == '__main__':
    unittest.main()
