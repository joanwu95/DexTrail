"""Material evidence must retain its version, component and uncertainty in both views."""
import copy
import html
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def hook(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f'website/hooks/{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


materials = hook('tendon_materials')
products = hook('product_details')


class TendonMaterialsTest(unittest.TestCase):
    def test_evidence_does_not_inherit_between_generations_or_confuse_components(self):
        records = materials.load()
        self.assertIsNone(records['ruka-v2']['material'])
        self.assertIsNone(records['qb-softhand-research']['material'])
        self.assertIsNone(records['leap-hand-v2']['material'])
        self.assertNotIn('leap-hand', records)
        self.assertIn('不锈钢', records['sdm-hand']['material'])
        self.assertIn('导管', records['sdm-hand']['specification'])
        self.assertIn('1 mm', records['orca-hand']['specification'])
        self.assertIn('扁平', records['utah-mit-hand']['specification'])
        self.assertIn('耦合', records['dlr-hit-hand-ii']['material'])

    def test_product_and_chapter_keep_the_same_cited_material_and_missing_specs(self):
        records = materials.load()
        chapter = materials.comparison()
        for key, record in records.items():
            with self.subTest(hand=key):
                self.assertIn(f'../hands/generated/{key}.md#record-mechanics', chapter)
                sections = products.make_sections({'id': key}, {'dimensions': [], 'projects': []}, {}, str, lambda *_: '')
                sections = {s['id']: html.unescape(s['content_html']) for s in sections}
                self.assertIn('肌腱与绳索材料', sections['mechanics'])
                self.assertIn(record['scope'], sections['mechanics'])
                self.assertIn(record['missing'], sections['mechanics'])
                self.assertIn('../../../engineering/transmission/#tendon-material-choice', sections['mechanics'])
                for source in record['sources']:
                    self.assertIn(source['url'], sections['mechanics'])
                    self.assertIn(source['url'], sections['sources'])
                if record['material']:
                    self.assertIn(record['material'], sections['overview'])
                    self.assertIn(record['material'], chapter)
                else:
                    self.assertIn('尚未确认化学成分', sections['mechanics'])

    def test_invalid_evidence_and_uncertain_materials_stop_the_build(self):
        valid = materials.load()['orca-hand']
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'data').mkdir()
            (root / 'data/hand-kinematics.json').write_text('{"orca-hand": {}}', encoding='utf-8')
            for change in [dict(status='partial'), dict(sources=[]), dict(scope=''),
                           dict(material=None), dict(checked_on='invalid')]:
                record = copy.deepcopy(valid)
                record.update(change)
                (root / 'data/tendon-materials.json').write_text(json.dumps({'orca-hand': record}), encoding='utf-8')
                with self.subTest(change=change), patch.object(materials, 'ROOT', root):
                    with self.assertRaises(ValueError):
                        materials.load()
            record = copy.deepcopy(valid)
            record['sources'][0]['locator'] = ''
            (root / 'data/tendon-materials.json').write_text(json.dumps({'orca-hand': record}), encoding='utf-8')
            with patch.object(materials, 'ROOT', root), self.assertRaises(ValueError):
                materials.load()

    def test_mechanisms_keep_component_scope_and_do_not_follow_material_status(self):
        records = materials.load()
        self.assertEqual(records['pisa-iit-softhand']['status'], 'verified')
        self.assertEqual(records['pisa-iit-softhand']['fixation']['status'], 'unconfirmed')
        self.assertEqual(records['ruka-v2']['return_mechanism']['scope'], 'RUKA-v2 · 新增展收模块')
        self.assertIn('2015', records['dlr-david']['fixation']['scope'])
        self.assertIn('有意松弛', records['sdm-hand']['tensioning']['text'])
        self.assertIn('差值', records['shadow-hand']['tensioning']['text'])
        self.assertIn('螺纹', records['barrett-bh8-280']['fixation']['text'])
        self.assertIn('CMC1', records['mm-hand']['return_mechanism']['text'])

    def test_every_cord_configuration_keeps_its_mechanism_evidence_in_both_views(self):
        records = materials.load()
        comparison = materials.mechanism_comparison()
        for key, record in records.items():
            with self.subTest(hand=key):
                self.assertIn(f'../hands/generated/{key}.md#record-mechanics', comparison)
                product = materials.product(record)
                for field in materials.MECHANISMS:
                    item = record[field]
                    self.assertIn(item['text'], product)
                    self.assertIn(item['scope'], product)
                    if item['status'] != 'unconfirmed':
                        self.assertIn(item['text'], comparison)
                        for source in item['sources']:
                            self.assertIn(source['url'], comparison)
                            self.assertIn(source['locator'], product)

    def test_uncited_mechanism_cannot_be_presented_as_confirmed(self):
        valid = materials.load()['orca-hand']
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'data').mkdir()
            (root / 'data/hand-kinematics.json').write_text('{"orca-hand": {}}', encoding='utf-8')
            for field in materials.MECHANISMS:
                for invalid in [dict(sources=[]), dict(scope=''), dict(status='unsupported'), dict(text='')]:
                    record = copy.deepcopy(valid)
                    record[field].update(invalid)
                    record[field]['status'] = invalid.get('status', 'verified')
                    (root / 'data/tendon-materials.json').write_text(json.dumps({'orca-hand': record}), encoding='utf-8')
                    with self.subTest(field=field, invalid=invalid), patch.object(materials, 'ROOT', root):
                        with self.assertRaises(ValueError):
                            materials.load()


if __name__ == '__main__':
    unittest.main()
