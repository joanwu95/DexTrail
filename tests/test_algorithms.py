"""Evidence boundaries and links in the two-dimensional algorithm atlas."""
import copy
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('algorithms', ROOT / 'website/hooks/algorithms.py')
algorithms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(algorithms)


class AlgorithmsTest(unittest.TestCase):
    def setUp(self):
        self.document = algorithms.load_document()
        self.docs = ROOT / 'website/docs'

    def test_all_readers_and_relation_evidence_exist(self):
        algorithms.validate(self.document, self.docs)
        for group in ('problems', 'methods', 'cases'):
            for item in self.document[group]:
                body = (self.docs / item['path']).read_text(encoding='utf-8')
                self.assertIn('<!-- algorithm-related -->', body)
                self.assertIn('依据', body)

    def test_missing_evidence_unknown_relations_and_unsafe_paths_fail(self):
        mutations = [
            lambda d: d['cases'][0]['methods'].update({'unknown': ['pp-tac']}),
            lambda d: d['cases'][0]['problems'].update({'perception-and-state': []}),
            lambda d: d['cases'][0]['sources'].append('missing'),
            lambda d: d['problems'][0].update(path='../../AGENTS.md'),
            lambda d: d['sources']['scope'].update(url='javascript:alert(1)'),
            lambda d: d['cases'][0].update(boundary=''),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                document = copy.deepcopy(self.document)
                mutate(document)
                with self.assertRaises(ValueError):
                    algorithms.validate(document, self.docs)

    def test_overview_works_without_javascript_and_preserves_adjacent_scope(self):
        html = algorithms.render_index(self.document, 'algorithms/')
        for group in ('problems', 'methods'):
            self.assertIn(f'id="{group}"', html)
            self.assertNotIn(f'data-algo-panel="{group}" hidden', html)
        self.assertEqual(html.count('data-algo-case '), len(self.document['cases']))
        self.assertIn('相邻操作研究', html)
        self.assertIn('不作为灵巧手实验证据', html)
        self.assertIn('href="../papers/learning-dexterous-in-hand-manipulation/"', html)

    def test_related_links_work_from_legacy_paper_and_deep_readers(self):
        html = algorithms.render_related(self.document, 'papers/learning-dexterous-in-hand-manipulation.md', 'papers/learning-dexterous-in-hand-manipulation/')
        self.assertIn('href="../../algorithms/methods/reinforcement-learning/"', html)
        html = algorithms.render_related(self.document, 'algorithms/methods/optimization.md', 'algorithms/methods/optimization/')
        self.assertIn('href="../../cases/dexgraspnet/"', html)
        self.assertNotIn('DexMV', html)

    def test_dynamic_text_is_escaped(self):
        self.document['cases'][0]['title'] = '<script>alert(1)</script>'
        html = algorithms.render_index(self.document, 'algorithms/')
        self.assertNotIn('<script>', html)
        self.assertIn('&lt;script&gt;', html)

    def test_markers_are_replaced_for_searchable_built_content(self):
        page = SimpleNamespace(file=SimpleNamespace(src_uri='algorithms/index.md'), url='algorithms/')
        config = SimpleNamespace(extra={'algorithm_atlas': self.document})
        rendered = algorithms.on_page_markdown('<!-- algorithm-atlas -->', page, config, None)
        self.assertNotIn('<!-- algorithm-atlas -->', rendered)
        self.assertIn('抓取生成与评价', rendered)


if __name__ == '__main__':
    unittest.main()
