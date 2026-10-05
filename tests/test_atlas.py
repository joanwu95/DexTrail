import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
import yaml
import html
import json
import markdown
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("atlas", ROOT / "website/hooks/atlas.py")
atlas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(atlas)


class AtlasTest(unittest.TestCase):
    def test_rendered_product_chapters_remain_in_the_shared_page_wrapper(self):
        # Markdown's HTML handling must not strand later chapters outside the
        # product canvas when nested media, disclosures and lineage are present.
        class CanvasParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.stack, self.orphans, self.chapters = [], [], []
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if 'hand-record-section' in attrs.get('class', '').split():
                    self.chapters.append(attrs.get('id'))
                    if not any('dex-hand-page' in a.get('class', '').split() for _, a in self.stack):
                        self.orphans.append(attrs.get('id'))
                if tag not in {'img', 'input', 'br', 'hr', 'meta', 'link', 'source', 'wbr'}:
                    self.stack.append((tag, attrs))
            def handle_endtag(self, tag):
                for i in range(len(self.stack) - 1, -1, -1):
                    if self.stack[i][0] == tag:
                        del self.stack[i:]
                        break
        data = self.load()
        for key in ['shadow-hand', 'leap-hand', 'wuji-hand-2', 'mm-hand']:
            with self.subTest(hand=key):
                hand = next(h for h in data['hands'] if h['id'] == key)
                body = atlas.hand_page(hand, data).split('---', 2)[2]
                rendered = markdown.markdown(body, extensions=['md_in_html', 'tables', 'attr_list', 'pymdownx.superfences', 'toc'])
                parser = CanvasParser()
                parser.feed(rendered)
                self.assertFalse(parser.orphans)
                for anchor in ['hand-intro', 'technical-summary', 'record-lineage', 'complete-metrics', 'record-mechanics']:
                    self.assertEqual(parser.chapters.count(anchor), 1)

    def test_product_briefs_cover_published_hands_without_inventing_editorials(self):
        data = self.load()
        editorials = data['editorials']['hands']
        for hand in data['hands']:
            if hand['status'] == 'planned':
                continue
            page = atlas.hand_page(hand, data)
            self.assertEqual(page.count('id="technical-summary"'), 1)
            self.assertIn('href="#technical-summary">技术摘要', page)
            self.assertLess(page.index('class="hand-explorer"'), page.index('id="technical-summary"'))
            self.assertLess(page.index('id="technical-summary"'), page.index('id="record-lineage"'))
            self.assertEqual('id="record-editorial"' in page, hand['id'] in editorials)
            if hand['id'] in editorials:
                self.assertIn('编辑草稿 · 待 Joan Wu 审阅', page)
                self.assertLess(page.index('id="record-assessment"'), page.index('id="record-editorial"'))
                self.assertLess(page.index('id="record-editorial"'), page.index('id="record-research"'))
                self.assertIn('尚未执行的验证流程', page)
                for part in ['evidence', 'reasoning', 'judgment', 'validation']:
                    self.assertIn(html.escape(editorials[hand['id']]['analysis'][part]), page)
            else:
                self.assertIn('尚无单独审阅的工程分析', page)
                self.assertNotIn('Joan Wu’s Analysis', page)

    def test_editorial_sources_and_author_review_cannot_be_implied(self):
        path = self.data / 'product-editorials.json'
        original = json.loads(path.read_text(encoding='utf-8'))
        for change in [lambda d: d['hands']['shadow-hand']['brief'][0].update(sources=[]),
                       lambda d: d['hands']['leap-hand']['analysis'].update(source_ids=['missing']),
                       lambda d: d['hands']['wuji-hand-2'].update(review_status='reviewed'),
                       lambda d: d['hands']['wuji-hand-2']['sources']['notice'].update(url='javascript:alert(1)')]:
            document = json.loads(json.dumps(original))
            change(document)
            path.write_text(json.dumps(document, ensure_ascii=False), encoding='utf-8')
            with self.assertRaises(ValueError):
                self.load()

    def test_sensing_audits_preserve_measurement_boundaries_across_views(self):
        data = self.load()
        products = {h['id']: h for h in data['hands']}
        mapped = {h['id']: h for h in atlas.map_payload(data)['hands']}
        compared = {h['id']: h for h in atlas.comparison.payload(data, atlas.product_details.classification)['hands']}
        for key in ['shadow-hand', 'leap-hand', 'wuji-hand-2']:
            audit = products[key]['sensing_audit']
            self.assertEqual(mapped[key]['sensing_audit'], audit)
            section = next(e for e in atlas.product_details.make_sections(products[key], data, atlas.FIELDS, atlas.text, atlas.source_links) if e['id'] == 'sensing')
            for channel in audit['channels']:
                self.assertIn(channel['quantity'], section['markdown'])
                self.assertIn(channel['quantity'], compared[key]['cells']['sensing']['value'])
                self.assertTrue(all(source['url'].startswith('https://') for source in atlas.product_details.sensing.references(audit, channel)))
            self.assertIn(audit['version'], compared[key]['cells']['sensing']['scope'])
        shadow = mapped['shadow-hand']['classification']['tags']
        self.assertEqual(next(t['label'] for t in shadow if t['id'] == 'sensing:force-sensing'), '腱负载感知')
        for key in ['leap-hand', 'wuji-hand-2']:
            tags = {t['id'] for t in mapped[key]['classification']['tags'] if t['group'] == 'sensing'}
            self.assertEqual(tags, {'sensing:position-sensing', 'sensing:current-sensing'})
        wuji = products['wuji-hand-2']['sensing_audit']['channels']
        self.assertEqual(next(c['status'] for c in wuji if c['id'] == 'tactile'), 'absent')
        self.assertEqual(next(c['status'] for c in wuji if c['id'] == 'torque-estimation'), 'unvalidated')
        self.assertIn('单位 A', next(c['quantity'] for c in wuji if c['id'] == 'current'))

    def test_sensing_audit_rejects_uncited_or_unvalidated_capability(self):
        path = self.data / 'sensing-audits.json'
        original = json.loads(path.read_text(encoding='utf-8'))
        for change in [lambda d: d['hands']['shadow-hand'].update(version=''),
                       lambda d: d['hands']['shadow-hand']['channels'][0].update(sources=['missing']),
                       lambda d: d['hands']['wuji-hand-2']['channels'][-1].update(tag='tactile-sensing')]:
            document = json.loads(json.dumps(original))
            change(document)
            path.write_text(json.dumps(document, ensure_ascii=False), encoding='utf-8')
            with self.assertRaises(ValueError):
                self.load()

    def test_engineering_articles_link_only_relevant_products(self):
        data = self.load()
        articles = atlas.comparison.payload(data, atlas.product_details.classification)['articles']
        ids = {h['id'] for h in data['hands']}
        for article in articles:
            self.assertTrue(set(article['hand_ids']) <= ids)
            self.assertTrue((ROOT / 'website/docs' / article['page']).is_file())
            href = '../../../' + article['page'][:-3] + '/'
            for hand in data['hands']:
                if hand['status'] == 'planned':
                    continue
                page = atlas.hand_page(hand, data)
                self.assertEqual(href in page, hand['id'] in article['hand_ids'])

    def test_comparison_retains_scope_sources_and_unknowns(self):
        data = self.load()
        result = atlas.comparison.payload(data, atlas.product_details.classification)
        products = {h['id']: h for h in result['hands']}
        self.assertEqual(set(products), {h['id'] for h in data['hands'] if h['status'] != 'planned'})
        shadow = products['shadow-hand']['cells']
        self.assertEqual(shadow['dof']['value'], '20')
        self.assertIn('腕', shadow['dof']['scope'])
        self.assertIn('2024', shadow['version']['value'])
        self.assertTrue(shadow['dof']['sources'])
        self.assertIn('第三方', shadow['models']['value'])
        self.assertIn('文献', shadow['control']['value'])
        rows = {r['id'] for r in result['rows']}
        for hand in result['hands']:
            self.assertEqual(set(hand['cells']), rows)
            for cell in hand['cells'].values():
                self.assertIsInstance(cell['value'], str)
                for source in cell['sources']:
                    self.assertTrue(source['url'].startswith(('http://', 'https://')))
        unknown = next(h for h in data['hands'] if h['status'] != 'planned' and not h.get('technologies') and not h.get('sensing_audit'))
        self.assertEqual(products[unknown['id']]['cells']['sensing']['value'], '尚未核实')
        self.assertIn('不代表不支持', next(r['help'] for r in result['rows'] if r['id'] == 'sensing'))

    def test_lineage_links_versions_and_sources_are_consistent(self):
        data = self.load()
        products = {h['id']: h for h in data['hands']}
        families = json.loads((ROOT / 'data/product-lineages.json').read_text(encoding='utf-8'))['families']
        memberships = []
        for family in families:
            memberships.extend(family['member_ids'])
            nodes = {n['id']: n for n in family['milestones']}
            self.assertEqual(len(nodes), len(family['milestones']))
            self.assertEqual({n['hand_id'] for n in nodes.values() if n.get('hand_id')}, set(family['member_ids']))
            self.assertTrue(set(family['member_ids']) <= products.keys())
            records = list(nodes.values()) + family['relationships'] + family['ecosystem']
            records += [row for comparison in family['comparisons'] for row in comparison['rows']]
            for record in records:
                self.assertTrue(record['sources'])
                for key in record['sources']:
                    self.assertTrue(family['sources'][key]['url'].startswith('https://'))
            for edge in family['relationships']:
                self.assertIn(edge['from'], nodes)
                self.assertIn(edge['to'], nodes)
                self.assertNotEqual(edge['from'], edge['to'])
                self.assertIn(edge['type'], {'generation', 'revision', 'branch', 'parallel'})
            for node in nodes.values():
                self.assertIn(node['date_relation'], {'on', 'by', 'unknown'})
                self.assertTrue(node['date_basis'])
                if not node.get('hand_id'):
                    self.assertTrue(node['url'].startswith('https://'))
            self.assertIn(family['status'], {'lineage', 'parallel', 'review'})
            if family['status'] != 'lineage':
                self.assertFalse(family['relationships'], 'Parallel/unconfirmed families must not imply succession')
            else:
                self.assertTrue(family['relationships'])
        self.assertEqual(len(memberships), len(set(memberships)))
        self.assertEqual(set(memberships), set(products), 'Every published hand needs a lineage audit')

    def test_lineage_only_appears_for_reviewed_families_and_keeps_media_first(self):
        data = self.load()
        products = {h['id']: h for h in data['hands']}
        for key, peer in [('wuji-hand', 'wuji-hand-2'), ('wuji-hand-2', 'wuji-hand')]:
            page = atlas.hand_page(products[key], data)
            self.assertEqual(page.count('id="record-lineage"'), 1)
            self.assertIn('href="#record-lineage">产品演进', page)
            self.assertIn(f'href="../{peer}/#record-lineage"', page)
            self.assertLess(page.index('class="hand-explorer"'), page.index('id="record-lineage"'))
            self.assertLess(page.index('id="record-lineage"'), page.index('<h2>完整技术记录</h2>'))
            self.assertIn('至迟 2025.11.07', page)
            self.assertIn('非触觉版', page)
        for key, hand in products.items():
            with self.subTest(hand=key):
                page = atlas.hand_page(hand, data)
                self.assertEqual(page.count('id="record-lineage"'), 1)
                self.assertIn('href="#record-lineage">产品演进', page)
                self.assertNotIn('../None/', page)
                self.assertLess(page.index('class="hand-explorer"'), page.index('id="record-lineage"'))
                self.assertLess(page.index('id="record-lineage"'), page.index('<h2>完整技术记录</h2>'))

    def test_lineage_distinguishes_external_parallel_and_unconfirmed_records(self):
        data = self.load()
        products = {h['id']: h for h in data['hands']}
        leap = atlas.hand_page(products['leap-hand'], data)
        self.assertIn('href="https://v2-adv.leaphand.com/"', leap)
        self.assertNotIn('../leap-advanced/', leap)
        linker = atlas.hand_page(products['linker-l20'], data)
        section = linker.split('id="record-lineage"', 1)[1].split('</section>', 1)[0]
        self.assertIn('产品族 / 并行路线', section)
        self.assertNotIn('class="lineage-relation"', section)
        review = atlas.hand_page(products['mm-hand'], data)
        section = review.split('id="record-lineage"', 1)[1].split('</section>', 1)[0]
        self.assertIn('前后代关系待确认', section)
        self.assertNotIn('class="lineage-track"', section)
        self.assertIn('MM-Hand 1.0', section)
        # Historical nodes must not become unreviewed products in the home map.
        self.assertEqual({h['id'] for h in atlas.map_payload(data)['hands']}, set(products))

    def test_named_vendors_publish_without_inflating_active_dof(self):
        data = self.load()
        products = {h['id']: h for h in atlas.map_payload(data)['hands']}
        expected = {'brainco-revo-1': 6, 'brainco-revo-2': 6,
                    'brainco-revo-3': 21, 'elephant-h100': 6,
                    'xpeng-iron-hand-2025': None, 'tencent-trx-hand': 8}
        for key, active in expected.items():
            with self.subTest(hand=key):
                self.assertEqual(products[key]['coordinates']['dof'], active)
                self.assertIsNotNone(products[key]['coordinates']['year'])
                self.assertTrue(products[key]['media']['url'].startswith('https://'))
                hand = next(h for h in data['hands'] if h['id'] == key)
                self.assertIn('SDK 与控制接口', atlas.hand_page(hand, data))
        self.assertEqual(products['xpeng-iron-hand-2025']['media']['kind'], 'video')
        self.assertNotIn('nvidia-hand', products)
        support = json.loads((ROOT / 'data/platform-support.json').read_text(encoding='utf-8'))
        gazebo = next(m for m in support['brainco-revo-2']['models'] if m['format'] == 'Gazebo')
        self.assertIn('官方', gazebo['status'])
        mujoco = next(m for m in support['tencent-trx-hand']['models'] if m['format'] == 'MuJoCo / MJCF')
        self.assertIn('下载包待核', mujoco['status'])

    def test_fourth_batch_keeps_coupled_inputs_and_variant_boundaries(self):
        products = {h['id']: h for h in atlas.map_payload(self.load())['hands']}
        batch = json.loads((ROOT / 'research/sources/expansion-04-dexterous-hands.json').read_text(encoding='utf-8'))
        for item in batch:
            hand = products[item['id']]
            self.assertEqual(hand['coordinates']['year'], item['year'])
            self.assertTrue(hand['media']['url'].startswith('https://'))
        self.assertIsNone(products['aero-hand-open']['coordinates']['dof'])
        self.assertEqual(products['aero-hand-open']['coordinates']['actuators'], 7)
        self.assertEqual(products['dexlink-hand']['coordinates']['dof'], 16)
        self.assertEqual(products['mm-hand']['coordinates']['dof'], 21)
        self.assertIsNone(products['mm-hand']['coordinates']['actuators'])
        self.assertEqual(products['dmanus']['coordinates']['dof'], 10)
        self.assertEqual(products['paxini-dexh13-gen2']['coordinates']['dof'], 13)
        self.assertIsNone(products['paxini-dexh13-gen2']['coordinates']['transmission'])
        self.assertEqual(products['tesollo-dg-5f-s']['coordinates']['dof'], 20)
        support = json.loads((ROOT / 'data/platform-support.json').read_text(encoding='utf-8'))
        gazebo = next(m for m in support['tesollo-dg-5f-s']['models'] if m['format'] == 'Gazebo')
        self.assertTrue(gazebo['sources'][0]['url'].endswith('/dg5f_s_ros2'))

    def test_dexterous_expansion_reaches_map_without_mixing_joint_counts(self):
        products = {h['id']: h for h in atlas.map_payload(self.load())['hands']}
        ids = ['isyhand-v6', 'bidexhand-v4', 'faive-hand', 'ruka-v2',
               'dexhand-021', 'robotera-xhand1']
        for key in ids:
            self.assertIn(key, products)
            hand = products[key]
            self.assertTrue(hand['media']['url'].startswith('https://'))
            self.assertIsNotNone(hand['coordinates']['year'])
            self.assertIsNotNone(hand['coordinates']['transmission'])
        self.assertEqual(products['isyhand-v6']['coordinates']['dof'], 18)
        self.assertEqual(products['faive-hand']['coordinates']['dof'], 11)
        self.assertEqual(products['faive-hand']['coordinates']['actuators'], 16)
        self.assertIsNone(products['ruka-v2']['coordinates']['dof'])
        self.assertEqual(products['dexhand-021']['coordinates']['dof'], 12)
        self.assertEqual(products['robotera-xhand1']['coordinates']['transmission'], 'geared-drive')
        self.assertEqual(products['bidexhand-v4']['timeline']['relation'], 'by')

    def test_system_map_entry_and_official_video_provenance(self):
        payload = atlas.map_payload(self.load())
        systems = payload['systems']
        self.assertFalse({h['id'] for h in payload['hands']} & {s['id'] for s in systems})
        sudo = next(s for s in systems if s['id'] == 'sudo-r1')
        self.assertEqual(sudo['kind'], 'system')
        self.assertEqual(sudo['coordinates']['year'], 2026)
        for field in ['dof', 'actuators', 'transmission']:
            self.assertIsNone(sudo['coordinates'][field])
        page = (ROOT / 'website/docs' / sudo['detail_url'] / 'index.md')
        if not page.exists():
            page = ROOT / 'website/docs' / (sudo['detail_url'].rstrip('/') + '.md')
        text = page.read_text(encoding='utf-8')
        self.assertNotIn('<img', text)
        self.assertNotIn('poster=', text)
        videos = json.loads((ROOT / 'research/sources/sudo-r1-videos.json').read_text(encoding='utf-8'))
        self.assertEqual(len(videos), 7)
        self.assertEqual(len({v['url'] for v in videos}), len(videos))
        for video in videos:
            self.assertTrue(video['url'].startswith('https://assets.sudo.ai/public/videos/'))
            self.assertIn(video['url'], text)
            self.assertEqual(video['source'], 'https://www.sudo.ai/')

    def test_platform_support_covers_every_hand_without_inventing_compatibility(self):
        support = json.loads((ROOT / 'data/platform-support.json').read_text(encoding='utf-8'))
        data = self.load()
        self.assertEqual(set(support), {h['id'] for h in data['hands']})
        for hand in data['hands']:
            record = support[hand['id']]
            self.assertEqual(len(record['models']), 6)
            self.assertEqual(len({m['format'] for m in record['models']}), 6)
            for model in record['models']:
                if model['status'] != '尚未核实':
                    self.assertTrue(model['sources'])
            sections = atlas.product_details.make_sections(hand, data, atlas.FIELDS, atlas.text, atlas.source_links)
            rendered = next(s['content_html'] for s in sections if s['id'] == 'simulation')
            self.assertIn('SDK 与控制接口', rendered)
            self.assertIn('模型与仿真支持矩阵', rendered)
        self.assertIn('V3', support['allegro-v4']['models'][2]['detail'])
        self.assertIn('单个 PneuFlex', support['rbo-hand-2']['models'][5]['detail'])
        self.assertEqual(support['xynova-prima-1']['sdk']['status'], '资源中心存在，具体文件待核')
        self.assertIn('xynova-prima-1', support)
        self.assertNotIn('sudo-r1', support)

    def test_second_batch_preserves_versions_and_nonangular_inputs(self):
        products = {h['id']: h for h in atlas.map_payload(self.load())['hands']}
        batch = json.loads((ROOT / 'research/sources/expansion-02-2026-10-02.json').read_text(encoding='utf-8'))
        for record in batch:
            hand = products[record['id']]
            self.assertEqual(hand['timeline']['year'], record['year'])
            self.assertTrue(hand['media']['url'].startswith('https://'))
        self.assertEqual(products['allegro-v5']['coordinates']['dof'], 9)
        self.assertEqual(products['allegro-v5-plus']['coordinates']['dof'], 16)
        self.assertEqual(products['allegro-v6f']['coordinates']['dof'], 20)
        metrics = json.loads((ROOT / 'data/research-metrics.json').read_text(encoding='utf-8'))
        self.assertTrue(metrics['allegro-v5']['source'].endswith('?idx=3'))
        self.assertTrue(metrics['allegro-v5-plus']['source'].endswith('?idx=4'))
        self.assertEqual(products['omnidirectional-sensing-hand']['coordinates']['actuators'], 9)
        self.assertIsNone(products['omnidirectional-sensing-hand']['coordinates']['dof'])
        self.assertIsNone(products['tactile-active-palm']['coordinates']['dof'])
        self.assertEqual(products['tactile-active-palm']['coordinates']['actuators'], 7)
        self.assertEqual(products['tactile-softhand-a']['coordinates']['actuators'], 2)

    def test_venue_expansion_is_published_with_media_and_correct_counting(self):
        data = self.load()
        products = {h['id']: h for h in atlas.map_payload(data)['hands']}
        batch = json.loads((ROOT / 'research/sources/expansion-2026-10-02.json').read_text(encoding='utf-8'))
        for record in batch:
            hand = products[record['id']]
            self.assertEqual(hand['venue'], record['venue'])
            self.assertTrue(hand['media']['url'].startswith('https://'))
            self.assertEqual(hand['timeline']['year'], record['year'])
        self.assertEqual(products['vms-hand']['coordinates']['dof'], 13)
        self.assertEqual(products['vms-hand']['coordinates']['actuators'], 13)
        self.assertIsNone(products['palm-finger-soft-hand']['coordinates']['dof'])
        self.assertEqual(products['palm-finger-soft-hand']['coordinates']['actuators'], 6)
        self.assertEqual(products['dexco-hand']['coordinates']['transmission'], 'hydraulic-soft')
        self.assertEqual(products['adapt-hand-1']['venue'], 'Communications Engineering')
        self.assertEqual(products['detachable-crawling-hand']['timeline']['year'], 2026)

    def test_joint_review_covers_every_published_product(self):
        reviews = json.loads((ROOT / 'data/hand-kinematics.json').read_text(encoding='utf-8'))
        galleries = json.loads((ROOT / 'data/media-galleries.json').read_text(encoding='utf-8'))
        products = {h['id'] for h in self.load()['hands'] if h['status'] != 'planned'}
        self.assertEqual(set(reviews), products)
        self.assertEqual(set(galleries), products)
        for key, record in reviews.items():
            with self.subTest(hand=key):
                self.assertTrue(record['parts'])
                self.assertTrue(record['ranges'])
                self.assertTrue(record['gaps'])
                self.assertTrue(all(s['url'].startswith('https://') for s in record['sources']))
                self.assertTrue(record['capability']['source'].startswith('https://'))
                self.assertTrue(all(a['source'] and a['label'] for a in galleries[key]))
                urls = [a['url'] for a in galleries[key]]
                self.assertEqual(len(urls), len(set(urls)))

    def test_detail_surfaces_known_dof_and_semantic_headings(self):
        data = self.load()
        hand = next(h for h in data['hands'] if h['id'] == 'wuji-hand-2')
        entries = atlas.product_details.make_sections(hand, data, atlas.FIELDS, atlas.text, atlas.source_links)
        self.assertIn('20', entries[0]['markdown'])
        self.assertIn('180 × 80 × 40', entries[0]['markdown'])
        self.assertIn('cmc_flex', entries[1]['markdown'])
        page = atlas.hand_page(hand, data)
        self.assertIn('class="dex-emblem"', page)
        self.assertIn('<h2>机械与驱动</h2>', page)
        self.assertIn('data-gallery-index="3"', page)

    def test_all_products_share_one_category_menu_and_keep_archive(self):
        data = self.load()
        expected = [key for key, _ in atlas.product_details.SECTIONS]
        for hand in data["hands"]:
            with self.subTest(hand=hand["id"]):
                page = atlas.hand_page(hand, data)
                self.assertRegex(page, r'class="dex-hand-page(?: [^\"]*)?"')
                self.assertEqual(page.count('aria-label="产品技术维度"'), 1)
                entries = atlas.product_details.make_sections(hand, data, atlas.FIELDS, atlas.text, atlas.source_links)
                self.assertEqual([e['id'] for e in entries], expected)
                self.assertTrue(all(e['content_html'] for e in entries))
                self.assertEqual(page.count('aria-label="本页章节目录"'), 1)
                self.assertIn('href="#complete-metrics"', page)
                for key in expected[1:]:
                    self.assertIn(f'href="#record-{key}"', page)
                    self.assertIn(f'id="record-{key}"', page)
                if hand.get('note_content'):
                    self.assertIn('class="hand-note-archive"', page)
        ruka = next(h for h in data['hands'] if h['id'] == 'ruka-v1')
        entries = atlas.product_details.make_sections(ruka, data, atlas.FIELDS, atlas.text, atlas.source_links)
        self.assertNotIn('首轮摘要记录', ''.join(e['markdown'] for e in entries))
        self.assertIn('首轮摘要记录', atlas.hand_page(ruka, data))

    def test_navigation_tags_preserve_unknowns_and_evidence_scope(self):
        data = self.load()
        rows = {h['id']: h for h in atlas.map_payload(data)['hands']}
        self.assertEqual(rows['shadow-hand']['classification']['fingers'], 5)
        leap = rows['leap-hand']['classification']
        self.assertEqual(leap['transmission'], 'unknown')
        self.assertEqual(leap['fingers'], 4)  # Reuse the same reviewed count as the detail table.
        unknown = atlas.product_details.classification({'id': 'unverified-five-finger-hand', 'facts': {}, 'coordinates': {}}, data)
        self.assertIsNone(unknown['fingers'])  # Never guess fingers from a name or image.
        pneumatic = next(h for h in rows.values() if h['coordinates']['transmission'] == 'pneumatic-soft')
        self.assertEqual(pneumatic['classification']['transmission'], 'unknown')
        self.assertTrue(any(t['group'] == 'actuation' for t in pneumatic['classification']['tags']))
        shadow_tags = rows['shadow-hand']['classification']['tags']
        learning = next(t for t in shadow_tags if t['id'] == 'control:reinforcement-learning')
        self.assertIn('文献', learning['label'])
        self.assertIn('非 2024', learning['scope'])
        self.assertTrue(learning['sources'])
        self.assertFalse(any(t['id'] == 'software:mjcf' for t in rows['tencent-trx-hand']['classification']['tags']))

    def test_timeline_covers_curated_map_without_fabricating_dof(self):
        data = self.load()
        payload = atlas.map_payload(data)
        published = json.loads((ROOT / 'data/report-pages.json').read_text(encoding='utf-8'))
        self.assertEqual(len(payload["hands"]), len(published))
        for hand in payload["hands"]:
            self.assertEqual(hand["coordinates"]["year"], hand["timeline"]["year"])
            self.assertIn(hand["timeline"]["source_id"], data["source_index"])
        xynova = next(h for h in data["hands"] if h["id"] == "xynova-flex-2")
        self.assertIsNone(xynova["coordinates"]["dof"])
        self.assertIn("≤ 2026", atlas.hand_page(xynova, data))
        self.assertIn(xynova["timeline"]["source"]["url"], atlas.hand_page(xynova, data))

    def test_invalid_timeline_or_missing_evidence_rejected(self):
        path = self.data / "hand-timeline.json"
        original = json.loads(path.read_text(encoding="utf-8"))
        for change in ({"year": None}, {"basis": "guess"}, {"source": {}},
                       {"month": 0}, {"month": 13}, {"month": True}, {"month": "04"}):
            with self.subTest(change=change):
                document = json.loads(json.dumps(original))
                document["shadow-hand"].update(change)
                path.write_text(json.dumps(document), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "时间"):
                    self.load()

    def test_timeline_months_preserve_source_bounds_and_year_only_records(self):
        payload = atlas.map_payload(self.load())
        hands = {hand['id']: hand for hand in payload['hands']}
        shadow = hands['shadow-hand']['timeline']
        self.assertEqual(shadow['month'], 1)
        self.assertIn('≤ 2013-01', shadow['label'])
        self.assertEqual(shadow['relation'], 'by')
        self.assertEqual(hands['sharpa-w01']['timeline']['month'], 12)
        self.assertNotIn('month', hands['elephant-h100']['timeline'])
        self.assertNotIn('month', hands['unitree-dex5-1']['timeline'])

    def test_curated_products_have_interactive_detail_and_null_coordinates(self):
        data = self.load()
        published = json.loads((ROOT / 'data/report-pages.json').read_text(encoding='utf-8'))
        self.assertEqual(len(data["hands"]), len(published))
        clash = next(h for h in data["hands"] if h["id"] == "dlr-clash")
        self.assertTrue(any("论文" in s["title"] for s in clash["note_sections"]))
        page = atlas.hand_page(clash, data)
        self.assertIn("content_html", page)
        self.assertIn("完整技术记录", page)
        self.assertIn("霍尔", page)
        self.assertEqual(clash["coordinates"]["actuators"], 8)
        xynova = next(h for h in data["hands"] if h["id"] == "xynova-flex-2")
        self.assertIsNone(xynova["coordinates"]["dof"])
        self.assertIsNone(xynova["coordinates"]["actuators"])
        self.assertIn("23", xynova["facts"]["dof"]["value"])
        self.assertIn("未拆分", xynova["coordinates"]["gaps"]["dof"])
        self.assertIn("地图参数与计数口径", atlas.hand_page(xynova, data))

    def test_graph_payload_preserves_only_registered_relations(self):
        data = self.load()
        class MapParser(HTMLParser):
            payload = None
            def handle_starttag(self, tag, attrs):
                for key, value in attrs:
                    if key == "data-atlas-map":
                        self.payload = json.loads(value)
        parser = MapParser()
        parser.feed(atlas.graph(data, "shadow-hand"))
        self.assertEqual(parser.payload["hand"], "shadow-hand")
        self.assertEqual(parser.payload["hands"][0]["technologies"], data["hands"][0]["technologies"])
        self.assertTrue(all(not h.get("technologies") for h in parser.payload["hands"] if h["status"] == "planned"))
        self.assertNotIn("<script", atlas.graph({"dimensions": [], "hands": [{"name": '</div><script>alert(1)</script>'}], "sources": [], "projects": []}))

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name) / "data"
        shutil.copytree(ROOT / "data", self.data)

    def edit(self, name, change):
        path = self.data / f"{name}.yaml"
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
        change(document)
        path.write_text(yaml.safe_dump(document, allow_unicode=True), encoding="utf-8")

    def load(self):
        return atlas.load_data(self.data, ROOT / "website/docs")

    def test_unknown_is_explicit(self):
        data = self.load()
        self.assertIn("待核验", atlas.hand_page(data["hands"][0], data))
        self.assertEqual(atlas.cards(data, "").count("查看参数与证据"),
                         sum(h["status"] != "planned" for h in data["hands"]))

    def test_parameter_requires_evidence(self):
        self.edit("hands", lambda d: d["hands"][0]["facts"]["dof"].update(value=20, sources=[]))
        with self.assertRaisesRegex(ValueError, "必须提供证据"):
            self.load()

    def test_unknown_source_rejected(self):
        self.edit("hands", lambda d: d["hands"][0]["facts"]["dof"].update(value=20, sources=["missing"]))
        with self.assertRaisesRegex(ValueError, "不存在"):
            self.load()

    def test_duplicate_id_rejected(self):
        self.edit("hands", lambda d: d["hands"].append(dict(d["hands"][0])))
        with self.assertRaisesRegex(ValueError, "重复"):
            self.load()

    def test_path_traversal_rejected(self):
        self.edit("hands", lambda d: d["hands"][0].update(analysis_page="../../README.md"))
        with self.assertRaisesRegex(ValueError, "非法页面"):
            self.load()

    def test_project_requires_real_hand(self):
        self.edit("projects", lambda d: d["projects"][0].update(hand_ids=["missing"]))
        with self.assertRaisesRegex(ValueError, "不存在"):
            self.load()

    def test_detail_uses_media_and_preserves_evidence(self):
        data = self.load()
        page = atlas.hand_page(data["hands"][0], data)
        self.assertIn("data-hand-explorer", page)
        self.assertIn("<img", page)
        self.assertNotIn("data-atlas-map", page)
        self.assertIn("完整技术指标", page)
        self.assertIn("mujoco_menagerie/tree/main/shadow_hand", page)
        self.assertIn("E3M5", page)

    def test_new_product_flows_to_views(self):
        # Synthetic facts remain confined to temporary test data.
        self.edit("sources", lambda d: d["sources"].append({
            "id": "test-source", "title": "Fixture source", "url": "https://example.com/test",
            "kind": "paper", "version": "fixture", "verified_on": "2026-10-01",
        }))
        self.edit("hands", lambda d: d["hands"].append({
            "id": "fixture-hand", "name": "Fixture Hand", "status": "scaffold",
            "facts": {"dof": {"value": 7, "sources": ["test-source"]}},
            "technologies": [{"id": "mujoco", "evidence_type": "paper",
                              "scope": "fixture model", "sources": ["test-source"]}],
        }))
        data = self.load()
        self.assertIn("hands/generated/fixture-hand.md", atlas.cards(data, ""))
        page = atlas.hand_page(next(h for h in data["hands"] if h["id"] == "fixture-hand"), data)
        # Assert the published value remains paired with its evidence, regardless
        # of whitespace or table serialization in the product template.
        class TableRows(HTMLParser):
            def __init__(self):
                super().__init__()
                self.rows, self.row, self.cell = [], None, None
            def handle_starttag(self, tag, attrs):
                if tag == 'tr':
                    self.row = []
                elif tag == 'td':
                    self.cell = ''
            def handle_data(self, value):
                if self.cell is not None:
                    self.cell += value
            def handle_endtag(self, tag):
                if tag == 'td' and self.cell is not None:
                    self.row.append(self.cell.strip())
                    self.cell = None
                elif tag == 'tr' and self.row:
                    self.rows.append(self.row)
        table = TableRows()
        table.feed(page)
        self.assertTrue(any(row[:2] == [atlas.FIELDS['dof'], '7'] and 'Fixture source' in row[2]
                            for row in table.rows))
        self.assertIn("文献实现", page)
        self.assertIn("Fixture source", page)
        self.assertIn("fixture-hand.md", atlas.technology_map(data))


if __name__ == "__main__":
    unittest.main()
