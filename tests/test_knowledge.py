"""Evidence boundaries and precision for the field-development renderer."""
import copy
import importlib.util
import json
import re
from pathlib import Path
import unittest
from types import SimpleNamespace
from html.parser import HTMLParser
from html import escape as html_escape
import markdown

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("knowledge", ROOT / "website/hooks/knowledge.py")
knowledge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(knowledge)
routes_spec = importlib.util.spec_from_file_location('technology_routes', ROOT / 'website/hooks/technology_routes.py')
technology_routes = importlib.util.module_from_spec(routes_spec)
routes_spec.loader.exec_module(technology_routes)


class KnowledgeTest(unittest.TestCase):
    def setUp(self):
        self.document = json.loads((ROOT / "data/field-development.json").read_text(encoding="utf-8"))
        self.hands = {hand for event in self.document["events"] for hand in event["hand_ids"]}

    def test_review_catalog_preserves_evidence_and_separates_publication_status(self):
        document = json.loads((ROOT / 'data/review-papers.json').read_text(encoding='utf-8'))
        knowledge.validate_reviews(document)
        body = knowledge.render_reviews(document)
        page = SimpleNamespace(file=SimpleNamespace(src_uri='papers/reviews/index.md'), url='papers/reviews/')
        rendered = knowledge.add_topic_navigation('<div class="dex-hand-page"><header class="dex-brand"></header>' + body + '</div>', page)
        self.assertEqual(rendered.count('data-topic-item="1"'), len(document['papers']))
        for paper in document['papers']:
            article = re.search(r'<article[^>]+id="' + paper['id'] + r'".*?</article>', rendered, re.S).group()
            self.assertIn(html_escape(paper['title']), article)
            self.assertIn(paper['source'], article)
            self.assertIn(html_escape(paper['locator']), article)
            self.assertIn('期刊综述' if paper['kind'] == 'journal-review' else '综述预印本', article)
            self.assertIn('本站阅读建议', article)
        self.assertIn('2019-05 ·', rendered)
        self.assertNotIn('2019-05-01', rendered)

    def test_review_catalog_rejects_missing_provenance_and_escapes_content(self):
        source = json.loads((ROOT / 'data/review-papers.json').read_text(encoding='utf-8'))
        for key, value in [('source', ''), ('locator', ''), ('kind', 'research-paper'), ('tags', ['unknown-tag']), ('date', '2099-01')]:
            with self.subTest(field=key):
                document = copy.deepcopy(source)
                document['papers'][0][key] = value
                with self.assertRaises(ValueError):
                    knowledge.validate_reviews(document)
        document = copy.deepcopy(source)
        document['papers'].append(copy.deepcopy(document['papers'][0]))
        with self.assertRaises(ValueError):
            knowledge.validate_reviews(document)
        document = copy.deepcopy(source)
        document['papers'][0]['title'] = '<script>bad()</script>'
        self.assertNotIn('<script>', knowledge.render_reviews(document))

    def test_research_readers_have_consistent_questions_methods_results_and_resources(self):
        index = (ROOT / 'website/docs/papers/index.md').read_text(encoding='utf-8')
        for slug in ['adaptive-synergies-2014', 'learning-dexterous-in-hand-manipulation', 'trifinger-2020', 'leap-hand-2023']:
            self.assertIn(f'href="{slug}/">阅读论文解读', index)
            body = (ROOT / 'website/docs/papers' / (slug + '.md')).read_text(encoding='utf-8')
            for title in ['研究问题', '采用的手', '具体做法', '实验结果', '局限与适用范围', '代码、模型与相关资源']:
                self.assertIn('## ' + title, body)
        self.assertIn('href="reviews/"', index)

    def test_year_directory_links_every_year_before_the_filters(self):
        body = knowledge.render(self.document)
        page = SimpleNamespace(file=SimpleNamespace(src_uri='development/index.md'), url='development/')
        content = '<div class="dex-hand-page"><header class="dex-brand"></header>' + body + '</div>'
        rendered = knowledge.add_topic_navigation(content, page)
        years = sorted({event['date'][:4] for event in self.document['events']})
        self.assertEqual(re.findall(r'data-history-link="(\d{4})"', rendered), years)
        for year in years:
            self.assertEqual(rendered.count(f'id="year-{year}"'), 1)
            self.assertIn(f'href="#year-{year}"', rendered)
        self.assertLess(rendered.index('history-year-directory'), rendered.index('<strong>标签筛选'))
        self.assertIn('id="decade-1970"', rendered)
        self.assertIn('id="decade-2020"', rendered)

    def test_agibot_records_reach_the_map_and_keep_publication_boundaries(self):
        atlas_spec = importlib.util.spec_from_file_location('agibot_atlas', ROOT / 'website/hooks/atlas.py')
        atlas = importlib.util.module_from_spec(atlas_spec)
        atlas_spec.loader.exec_module(atlas)
        products = {h['id']:h for h in atlas.map_payload(atlas.load_data(ROOT / 'data', ROOT / 'website/docs'))['hands']}
        expected = {'agibot-omnihand-2025':10, 'agibot-omnihand-pro-2025':12,
                    'agibot-omnihand-3-lite':4, 'agibot-omnihand-3-ultra-t':22, 'agibot-omnihand-3-ultra-m':20}
        for key, active in expected.items():
            self.assertEqual(products[key]['coordinates']['dof'], active)
            self.assertIsNone(products[key]['coordinates']['actuators'])
        events = {e['id']:e for e in self.document['events']}
        self.assertEqual(events['agibot-visuotactile-hand-2024']['hand_ids'], [])
        self.assertEqual(events['agibot-omnihand-docs-2025']['date_relation'], 'by')
        self.assertEqual(events['agibot-ultra-m-2026']['date'], '2026-07-18')
        self.assertIn('21', events['agibot-ultra-m-2026']['boundary'])

    def test_partial_dates_and_non_inheritance_labels_survive_rendering(self):
        knowledge.validate(self.document, self.hands)
        rendered = knowledge.render(self.document)
        self.assertIn("2001 · 学术研究", rendered)
        self.assertNotIn("2001-01", rendered)
        self.assertIn("2014-04 · 学术研究", rendered)
        # Other records can legitimately have that full date (e.g. SVH orders).
        soft_hand = re.search(r'<article\b[^>]*id="adaptive-synergies-2014".*?</article>', rendered, re.S).group()
        self.assertNotIn("2014-04-01", soft_hand)
        self.assertIn("同类路线 · 非继承证明", rendered)
        self.assertIn("问题对照 · 非继承证明", rendered)
        self.assertIn("厂商回溯记录", rendered)

    def test_unknown_evidence_product_and_relation_are_rejected(self):
        for field, value in [("source_ids", ["missing-source"]), ("hand_ids", ["missing-hand"]), ("date", "2023-13"), ("date_relation", "guess")]:
            with self.subTest(field=field):
                document = copy.deepcopy(self.document)
                document["events"][0][field] = value
                with self.assertRaises(ValueError):
                    knowledge.validate(document, self.hands)
        document = copy.deepcopy(self.document)
        document["relations"][0]["to"] = "missing-event"
        with self.assertRaises(ValueError):
            knowledge.validate(document, self.hands)

    def test_missing_boundaries_and_duplicate_events_are_rejected(self):
        document = copy.deepcopy(self.document)
        document["events"][0]["boundary"] = ""
        with self.assertRaises(ValueError):
            knowledge.validate(document, self.hands)
        document = copy.deepcopy(self.document)
        document["events"].append(copy.deepcopy(document["events"][0]))
        with self.assertRaises(ValueError):
            knowledge.validate(document, self.hands)

    def test_source_content_is_escaped_in_html(self):
        document = copy.deepcopy(self.document)
        document["events"][0]["title"] = '<script>alert("x")</script>'
        rendered = knowledge.render(document)
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)

    def test_every_academic_event_has_a_sourced_publication_header(self):
        rendered = knowledge.render(self.document)
        for event in self.document['events']:
            if event['track'] != 'academic':
                continue
            with self.subTest(event=event['id']):
                article = re.search(r'<article\b[^>]*id="' + event['id'] + r'".*?</article>', rendered, re.S).group()
                self.assertLess(article.index('history-publication'), article.index('<h3>'))
                self.assertIn(html_escape(event['publication']), article)
                self.assertTrue(set(event['publication_source_ids']).issubset(event['source_ids']))
        self.assertIn('arXiv · 预印本', rendered)
        for field in ('publication', 'publication_source_ids'):
            document = copy.deepcopy(self.document)
            document['events'][0].pop(field)
            with self.assertRaises(ValueError):
                knowledge.validate(document, self.hands)

    def test_timeline_hardware_batch_is_published_and_linked_without_version_merges(self):
        atlas_spec = importlib.util.spec_from_file_location('timeline_atlas', ROOT / 'website/hooks/atlas.py')
        atlas = importlib.util.module_from_spec(atlas_spec)
        atlas_spec.loader.exec_module(atlas)
        data = atlas.load_data(ROOT / 'data', ROOT / 'website/docs')
        products = {hand['id']: hand for hand in data['hands']}
        knowledge.validate(self.document, set(products))
        manifest = json.loads((ROOT / 'research/sources/development-catalog-2026-10-04.json').read_text(encoding='utf-8'))
        events = {event['id']: event for event in self.document['events']}
        map_ids = {hand['id'] for hand in atlas.map_payload(data)['hands']}
        for record in manifest['hands']:
            with self.subTest(hand=record['id']):
                self.assertIn(record['id'], map_ids)
                self.assertIn(record['id'], events[record['event_id']]['hand_ids'])
                self.assertEqual(products[record['id']]['timeline']['year'], record.get('year', int(events[record['event_id']]['date'][:4])))
                self.assertTrue(products[record['id']]['note_sections'])
        self.assertEqual(products['allegro-v5-2024']['facts']['fingers']['value'], 4)
        self.assertEqual(products['allegro-v5']['facts']['fingers']['value'], 3)
        self.assertEqual(events['unitree-dex5-2025']['hand_ids'], ['unitree-dex5-2025'])
        self.assertEqual(events['helix02-2026']['hand_ids'], ['figure-03-hand'])
        self.assertEqual(events['compliant-finger-gaiting-2022']['hand_ids'], ['yale-model-q'])

    def test_history_keeps_empty_lanes_and_matches_events_to_their_track(self):
        rendered = knowledge.render(self.document)
        class Lanes(HTMLParser):
            def __init__(self):
                super().__init__()
                self.years, self.divs, self.track = [], [], None

            def handle_starttag(self, tag, attributes):
                attributes = dict(attributes)
                classes = attributes.get('class', '').split()
                if tag == 'section' and 'history-year' in classes:
                    self.row = {'academic': [], 'industry': []}
                    self.years.append((attributes['aria-label'][:4], self.row))
                if tag == 'div':
                    self.divs.append(self.track)
                    if 'history-lane' in classes:
                        self.track = 'academic' if 'academic-lane' in classes else 'industry'
                if tag == 'article' and self.track:
                    self.row[self.track].append(attributes['id'])

            def handle_endtag(self, tag):
                if tag == 'div':
                    self.track = self.divs.pop()

            def handle_data(self, data):
                if self.track and not self.row[self.track] and data.strip():
                    raise AssertionError('An empty lane contains placeholder text')

        parser = Lanes()
        parser.feed(rendered)
        years = parser.years
        self.assertGreaterEqual(len(years), 15)
        for year, row in years:
            with self.subTest(year=year):
                for track, lane in row.items():
                    expected = {event['id'] for event in self.document['events'] if event['track'] == track and event['date'].startswith(year)}
                    actual = set(lane)
                    self.assertEqual(expected, actual)
                    if not expected:
                        self.assertEqual(lane, [])
        self.assertEqual(min(year for year, _ in years), '1974')
        self.assertEqual(max(year for year, _ in years), '2026')
        self.assertIn('≤ 2008-04-10', rendered)

    def test_history_tags_require_the_events_own_evidence(self):
        for change in ['unknown-tag', 'missing-evidence', 'wrong-track']:
            with self.subTest(change=change):
                document = copy.deepcopy(self.document)
                event = document['events'][0]
                if change == 'unknown-tag':
                    event['tags'].append('unknown-tag')
                elif change == 'missing-evidence':
                    event['tag_sources'][event['tags'][-1]] = ['unrelated-source']
                else:
                    event['tags'].remove(event['track'])
                with self.assertRaises(ValueError):
                    knowledge.validate(document, self.hands)

    def test_field_discussion_keeps_its_type_and_selection_reason(self):
        rendered = knowledge.render(self.document)
        discussions = [event for event in self.document['events'] if event.get('record_kind') == 'field-viewpoint']
        self.assertEqual({event['article_type'] for event in discussions}, {'Focus', 'Perspective', 'Review', 'News & Views', 'Research article'})
        for event in discussions:
            self.assertEqual(event['track'], 'academic')
            self.assertEqual(event['hand_ids'], [])
            self.assertIn(event['selection_reason'], rendered)
            self.assertIn(html_escape(event['publication']) + ' · ' + html_escape(event['article_type']), rendered)
        document = copy.deepcopy(self.document)
        event = next(event for event in document['events'] if event.get('record_kind') == 'field-viewpoint')
        event['article_type'] = 'unverified-type'
        with self.assertRaises(ValueError):
            knowledge.validate(document, self.hands)

    def test_research_papers_keep_venue_and_preprint_date_without_becoming_focus(self):
        knowledge.validate(self.document, self.hands)
        rendered = knowledge.render(self.document)
        paper = next(event for event in self.document['events'] if event['id'] == 'soft-hand-feedback-2023')
        self.assertEqual(paper['basis'], 'preprint')
        self.assertIn('2023-08-21 · 学术研究 · 预印本提交', rendered)
        self.assertIn('IROS 2023 · Conference paper', rendered)
        self.assertIn('IEEE T-RO · Review', rendered)
        document = copy.deepcopy(self.document)
        paper = next(event for event in document['events'] if event['id'] == 'soft-hand-feedback-2023')
        paper['article_type'] = 'Focus'
        with self.assertRaises(ValueError):
            knowledge.validate(document, self.hands)
        paper['article_type'] = 'Conference paper'
        paper.pop('publication')
        with self.assertRaises(ValueError):
            knowledge.validate(document, self.hands)

    def test_plain_markdown_pages_get_exactly_one_map_declaration(self):
        body = '<h1>技术资料</h1><p>Content</p>'
        first = knowledge.unify_site_chrome(body)
        self.assertIn('本站为个人学习与研究项目', first)
        self.assertEqual(first.count('class="dex-disclaimer"'), 1)
        self.assertEqual(knowledge.unify_site_chrome(first), first)

    def test_industry_views_require_attribution_and_their_own_original_source(self):
        for change in ['missing-role', 'missing-tag', 'wrong-track', 'unrelated-source', 'not-original']:
            with self.subTest(change=change):
                document = copy.deepcopy(self.document)
                event = next(item for item in document['events'] if item['id'] == 'wang-hand-choices-2024')
                if change == 'missing-role':
                    event['viewpoints'][0]['role'] = ''
                elif change == 'missing-tag':
                    event['tags'].remove('industry-viewpoint')
                elif change == 'wrong-track':
                    event['track'] = 'academic'
                elif change == 'unrelated-source':
                    event['viewpoints'][0]['source_ids'] = ['shadow-delivery-2005']
                else:
                    document['sources']['wang-hand-choices-2024']['kind'] = 'paper'
                with self.assertRaises(ValueError):
                    knowledge.validate(document, self.hands)

    def test_industry_views_are_attributed_without_duplicating_platform_launches(self):
        knowledge.validate(self.document, self.hands)
        rendered = knowledge.render(self.document)
        self.assertIn('产业观点 · 王兴兴', rendered)
        self.assertIn('产业观点 · 埃隆·马斯克', rendered)
        self.assertIn('平台发布 · 附产业观点 · 黄仁勋', rendered)
        self.assertEqual(rendered.count('id="nvidia-reference-platform-2026"'), 1)
        for event in self.document['events']:
            for viewpoint in event.get('viewpoints', []):
                self.assertIn(html_escape(viewpoint['context']), rendered)
                self.assertIn(html_escape(viewpoint['statement']), rendered)
        self.assertIn('2026-01-28 · 工业与产品 · 公开访谈或发言', rendered)
        self.assertIn('Industrial Robot · Technical Paper', rendered)
        document = copy.deepcopy(self.document)
        event = next(item for item in document['events'] if item['id'] == 'musk-hand-challenges-2026')
        event['viewpoints'][0]['statement'] = '<script>alert("x")</script>'
        escaped = knowledge.render(document)
        self.assertNotIn('<script>', escaped)
        self.assertIn('&lt;script&gt;', escaped)

    def test_root_sections_have_tags_without_repeating_the_active_title(self):
        for uri in knowledge.navigation_data()['pages']:
            if knowledge.navigation_data()['pages'][uri]['mode'] == 'links':
                continue
            with self.subTest(uri=uri):
                body = (ROOT / 'website/docs' / uri).read_text(encoding='utf-8').split('---', 2)[2]
                body = body.replace('<!-- knowledge:development -->', knowledge.render(self.document))
                body = body.replace('<!-- knowledge:routes -->', technology_routes.render(technology_routes.load(), knowledge.navigation_data()))
                if '<!-- knowledge:routes -->' in body:
                    route_spec = importlib.util.spec_from_file_location('knowledge_routes', ROOT / 'website/hooks/technology_routes.py')
                    routes = importlib.util.module_from_spec(route_spec)
                    route_spec.loader.exec_module(routes)
                    body = body.replace(routes.MARKER, routes.render(routes.load(), knowledge.navigation_data()))
                body = markdown.markdown(body, extensions=['md_in_html', 'tables', 'attr_list', 'toc'], extension_configs={'toc': {'permalink': True}})
                page = SimpleNamespace(file=SimpleNamespace(src_uri=uri), url=uri.replace('index.md', '').replace('.md', '/'))
                output = knowledge.on_page_content(body, page, None, None)
                self.assertEqual(output.count('knowledge-tag-rail'), 1)
                self.assertEqual(output.count('knowledge-section-purpose'), 1)
                self.assertNotIn('class="hand-heading"', output)
                self.assertIn('has-dex-rail', output)
                if uri == 'engineering/index.md':
                    class LinkNesting(HTMLParser):
                        depth = 0
                        def handle_starttag(parser, tag, attributes):
                            if tag == 'a':
                                self.assertEqual(parser.depth, 0, 'Nested links split the filterable card in browsers')
                                parser.depth += 1
                        def handle_endtag(parser, tag):
                            if tag == 'a':
                                parser.depth -= 1
                    LinkNesting().feed(output)

    def test_article_tags_share_the_existing_directory_sidebar(self):
        uri = 'technologies/underactuation-and-synergies.md'
        body = (ROOT / 'website/docs' / uri).read_text(encoding='utf-8').split('---', 2)[2]
        body = markdown.markdown(body, extensions=['md_in_html', 'tables', 'attr_list'])
        page = SimpleNamespace(file=SimpleNamespace(src_uri=uri), url='technologies/underactuation-and-synergies/')
        output = knowledge.on_page_content(body, page, None, None)
        self.assertEqual(len(re.findall(r'<aside\b', output)), 1)
        self.assertIn('class="dex-scroll-nav"', output)
        self.assertIn('href="#concepts"', output)
        self.assertIn('?tag=underactuated', output)
        self.assertIn('欠驱动与协同</h1>', output)

    def test_navigation_keeps_map_and_active_section_at_every_depth(self):
        for uri, url, home, active in [
            ("index.md", "", "./", "产品地图"),
            ("development/index.md", "development/", "../", "领域发展"),
            ("technologies/tendon-driven.md", "technologies/tendon-driven/", "../../", "技术路线"),
            ("hands/generated/leap-hand.md", "hands/generated/leap-hand/", "../../../", "产品地图"),
        ]:
            with self.subTest(uri=uri):
                page = SimpleNamespace(file=SimpleNamespace(src_uri=uri), url=url)
                body = '<header class="hand-brand">DexTrail</header><nav class="knowledge-nav">obsolete</nav><main>content</main>'
                output = knowledge.on_page_content(body, page, None, None)
                self.assertEqual(output.count('aria-label="知识地图入口"'), 1)
                self.assertIn(f'href="{home}"', output)
                self.assertIn(f'aria-current="page">{active}</a>', output)
                for label in ['产品地图', '领域发展', '技术路线', '工程问题', '研究论文解读', '技术对比']:
                    self.assertIn(label, output)
                self.assertNotIn('obsolete', output)

    def test_legacy_document_gets_the_same_navigation(self):
        page = SimpleNamespace(file=SimpleNamespace(src_uri='resources/index.md'), url='resources/')
        result = knowledge.on_page_content('<h1>Resources</h1>', page, None, None)
        self.assertTrue(result.startswith('<nav'))
        self.assertIn('href="../">产品地图', result)

    def test_branded_pages_share_map_header_and_declaration(self):
        source = (ROOT / 'website/docs/index.md').read_text(encoding='utf-8')
        expected_header = re.search(r'<header class="dex-brand".*?</header>', source, re.S).group()
        expected_footer = re.search(r'<footer class="dex-disclaimer".*?</footer>', source, re.S).group()
        for footer in ['', '<footer class="knowledge-footer">old signature</footer>', expected_footer]:
            with self.subTest(footer=footer):
                body = '<div class="dex-hand-page"><header class="hand-brand">灵巧手技术图谱<img src="old.svg"></header><div class="hand-heading"><p class="knowledge-kicker">技术图谱 / 路线</p><h1>技术路线</h1></div>' + footer + '</div>'
                output = knowledge.unify_site_chrome(body)
                self.assertIn(expected_header, output)
                self.assertIn(expected_footer, output)
                self.assertEqual(output.count('class="dex-disclaimer"'), 1)
                self.assertNotIn('灵巧手技术图谱', output)
                self.assertNotIn('old.svg', output)
                self.assertNotIn('技术图谱 / 路线', output)
                self.assertIn('<h1>技术路线</h1>', output)

    def test_report_navigation_survives_shared_header(self):
        content = '<div><header class="hand-brand"><a class="hand-back" href="../../generated/leap-hand/">← 产品详情</a></header><p>report body</p></div>'
        output = knowledge.unify_site_chrome(content)
        self.assertIn('href="../../generated/leap-hand/">← 产品详情', output)
        self.assertIn('report body', output)

    def test_nested_editorial_blocks_stay_inside_the_reading_canvas(self):
        class CanvasCheck(HTMLParser):
            def __init__(self):
                super().__init__()
                self.divs, self.detached, self.footer_count = [], [], 0

            def handle_starttag(self, tag, attributes):
                classes = set(dict(attributes).get('class', '').split())
                if tag == 'div':
                    self.divs.append(classes)
                inside = any('dex-knowledge' in parent for parent in self.divs)
                if classes.intersection({'paper-entry', 'route-feature', 'engineering-story', 'history-event', 'knowledge-footer'}):
                    if not inside:
                        self.detached.append(classes)
                    if 'knowledge-footer' in classes:
                        self.footer_count += 1

            def handle_endtag(self, tag):
                if tag == 'div' and self.divs:
                    self.divs.pop()

        pages = ['development/index.md', 'technologies/index.md', 'technologies/tendon-driven.md',
                 'technologies/underactuation-and-synergies.md', 'engineering/index.md',
                 'engineering/transmission.md', 'engineering/degrees-of-freedom.md',
                 'engineering/sensing-chain.md', 'papers/index.md', 'papers/leap-hand-2023.md',
                 'papers/learning-dexterous-in-hand-manipulation.md']
        for path in pages:
            with self.subTest(path=path):
                body = (ROOT / 'website/docs' / path).read_text(encoding='utf-8').split('---', 2)[2]
                body = body.replace('<!-- knowledge:development -->', knowledge.render(self.document))
                parser = CanvasCheck()
                parser.feed(markdown.markdown(body, extensions=['md_in_html', 'tables', 'attr_list']))
                self.assertEqual(parser.detached, [])
                self.assertEqual(parser.footer_count, 1)


if __name__ == "__main__":
    unittest.main()
