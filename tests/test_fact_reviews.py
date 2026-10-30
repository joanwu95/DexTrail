import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('fact_reviews', ROOT / 'website/hooks/fact_reviews.py')
reviews = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reviews)


def require(ok, message):
    if not ok:
        raise ValueError(message)


class FactReviewsTest(unittest.TestCase):
    def test_every_published_hand_has_cited_identity(self):
        document = json.loads((ROOT / 'data/hand-fact-reviews.json').read_text(encoding='utf-8'))
        reports = json.loads((ROOT / 'data/report-pages.json').read_text(encoding='utf-8'))
        ids = {dict(**{'shadow-classic': 'shadow-hand', 'leap-v1': 'leap-hand'}).get(Path(r['source']).stem, Path(r['source']).stem) for r in reports}
        self.assertEqual(set(document['hands']), ids)
        for key, record in document['hands'].items():
            with self.subTest(hand=key):
                for field in ['company', 'country']:
                    self.assertTrue(record['fields'][field]['value'])
                    self.assertTrue(record['fields'][field]['sources'])
                for entry in record['fields'].values():
                    for source in entry['sources']:
                        self.assertTrue(source['locator'])
                        self.assertTrue(source['url'].startswith('https://'))

    def test_scoped_review_replaces_stale_value_with_its_own_source(self):
        document = dict(schema_version=1, hands={'example-hand': dict(checked_on='2026-10-30', scope='Revision B; excludes base', fields={'weight': dict(value='800 g; excludes base', sources=[dict(title='Official revision B manual', url='https://example.org/manual', locator='Table 2', kind='official')])})})
        hands = {'example-hand': dict(facts={'weight': dict(value='unknown', sources=[])})}
        sources = []
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'reviews.json'
            path.write_text(json.dumps(document), encoding='utf-8')
            reviews.apply_reviews(path, hands, sources, {'weight': 'Mass'}, require)
        self.assertEqual(hands['example-hand']['facts']['weight']['value'], '800 g; excludes base')
        self.assertEqual(hands['example-hand']['facts']['weight']['sources'], [sources[0]['id']])
        self.assertIn('excludes base', sources[0]['version'])
        self.assertIn('Table 2', sources[0]['version'])

    def test_missing_field_source_is_rejected(self):
        document = dict(schema_version=1, hands={'example-hand': dict(checked_on='2026-10-30', scope='Revision B', fields={'weight': dict(value='800 g', sources=[])})})
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'reviews.json'
            path.write_text(json.dumps(document), encoding='utf-8')
            with self.assertRaises(ValueError):
                reviews.apply_reviews(path, {'example-hand': {}}, [], {'weight': 'Mass'}, require)
