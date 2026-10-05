"""Guard evidence, version scope and deep links as the route atlas grows."""
import copy
import importlib.util
import json
from html.parser import HTMLParser
from pathlib import Path
import unittest
import markdown

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('technology_routes', ROOT / 'website/hooks/technology_routes.py')
routes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(routes)


class RouteTest(unittest.TestCase):
    def test_embedded_figures_keep_both_plates_and_article_in_reading_canvas(self):
        # A Markdown/HTML boundary regression previously closed the page midway
        # through the first SVG, leaving subsequent prose outside its styling.
        class CanvasReader(HTMLParser):
            def __init__(self):
                super().__init__()
                self.stack = []
                self.plates = []
                self.headings = []

            def handle_starttag(self, tag, pairs):
                attrs = dict(pairs)
                inside = any('dex-hand-page' in classes.split() for _, classes in self.stack)
                if 'route-plate' in attrs.get('class', '').split():
                    self.plates.append(inside)
                if tag == 'h2':
                    self.headings.append(inside)
                if tag not in {'img', 'br', 'hr', 'input', 'meta', 'link'}:
                    self.stack.append((tag, attrs.get('class', '')))

            def handle_endtag(self, tag):
                for index in range(len(self.stack)-1, -1, -1):
                    if self.stack[index][0] == tag:
                        del self.stack[index:]
                        break

        for filename in ['tendon-driven.md', 'underactuation-and-synergies.md']:
            with self.subTest(filename=filename):
                source = (ROOT / 'website/docs/technologies' / filename).read_text(encoding='utf-8').split('---', 2)[-1]
                rendered = routes.on_page_markdown(source, None, None, None)
                parsed = CanvasReader()
                parsed.feed(markdown.markdown(rendered, extensions=['md_in_html', 'tables', 'attr_list']))
                self.assertEqual(parsed.plates, [True, True])
                self.assertTrue(parsed.headings and all(parsed.headings))

    def setUp(self):
        self.document = routes.load()
        self.navigation = json.loads((ROOT / 'data/knowledge-navigation.json').read_text(encoding='utf-8'))
        timeline = json.loads((ROOT / 'data/field-development.json').read_text(encoding='utf-8'))
        self.events = {event['id'] for event in timeline['events']}
        self.hands = {hand for event in timeline['events'] for hand in event['hand_ids']}

    def check_document(self, document):
        return routes.validate(document, self.navigation, self.hands, self.events)

    def test_untraceable_claims_and_crosslinks_fail_the_build(self):
        self.check_document(self.document)
        for defect in ['source', 'version', 'tag', 'hand', 'event', 'figure', 'default-question']:
            with self.subTest(defect=defect):
                document = copy.deepcopy(self.document)
                chapter = document['chapters'][0]
                if defect == 'source': chapter['questions'][0]['source_ids'] = ['unknown']
                if defect == 'version': chapter['cases'][0]['version'] = ''
                if defect == 'tag': chapter['cases'][0]['tags'] = ['unknown']
                if defect == 'hand': chapter['cases'][0]['hand_id'] = 'unknown'
                if defect == 'event': chapter['evolution'][0]['event_id'] = 'unknown'
                if defect == 'figure': chapter['questions'][0]['diagram'] = '../outside'
                if defect == 'default-question': chapter['default_question'] = 999
                with self.assertRaises(ValueError): self.check_document(document)

    def test_static_content_has_unique_ids_and_all_local_fragment_targets(self):
        identifiers, fragments = [], []
        class Reader(HTMLParser):
            def handle_starttag(self, tag, pairs):
                attrs = dict(pairs)
                if attrs.get('id'): identifiers.append(attrs['id'])
                if tag == 'a' and attrs.get('href', '').startswith('#'): fragments.append(attrs['href'][1:])
        content = routes.render(self.document, self.navigation)
        Reader().feed(content)
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertTrue(set(fragments).issubset(identifiers))
        # All prose is server-rendered and searchable, including inactive layers.
        for chapter in self.document['chapters']:
            for question in chapter['questions']: self.assertIn(question['answer'], content)
        document = copy.deepcopy(self.document)
        document['chapters'][0]['cases'][0]['name'] = '<script>untrusted()</script>'
        self.assertNotIn('<script>', routes.render(document, self.navigation))
        self.assertIn('&lt;script&gt;', routes.render(document, self.navigation))


if __name__ == '__main__':
    unittest.main()
