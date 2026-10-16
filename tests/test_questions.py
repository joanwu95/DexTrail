"""Verify evidence boundaries, two-way product links and complete question readers."""
import copy
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import unittest

import markdown

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('questions', ROOT / 'website/hooks/questions.py')
questions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(questions)


class ReadingStructure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
        self.entries = 0
        self.headings = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get('class', '').split()
        ancestor_classes = {c for _, names in self.stack for c in names}
        if 'question-entry' in classes:
            self.entries += 1
            if not {'question-reader', 'question-layout', 'question-article'} <= ancestor_classes:
                self.errors.append('Question escaped its reading layout')
        if 'question-article' in classes and 'question-layout' not in ancestor_classes:
            self.errors.append('Article escaped its layout')
        if tag == 'h1':
            self.headings += 1
        if tag not in {'img', 'br', 'hr', 'input', 'meta', 'link', 'source', 'wbr'}:
            self.stack.append((tag, classes))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                self.stack = self.stack[:i]
                break


class QuestionTest(unittest.TestCase):
    def setUp(self):
        self.document = questions.load_document()
        self.hands = {p['id']: {'name': p['id']} for q in self.document['questions'] for p in q['products']}
        self.config = SimpleNamespace(extra={'key_questions': self.document, 'question_hands': self.hands})

    def page(self, key):
        return SimpleNamespace(file=SimpleNamespace(src_uri='questions/' + key + '.md'), url='questions/' + ('' if key == 'index' else key + '/'))

    def test_registry_has_eight_sourced_paths_and_existing_readers(self):
        questions.validate(self.document, self.hands)
        self.assertEqual(len(self.document['questions']), 8)
        for q in self.document['questions']:
            self.assertTrue((ROOT / 'website/docs/questions' / (q['id'] + '.md')).is_file())
            self.assertGreaterEqual(len(q['claims']), 2)
            self.assertTrue(q['gaps'])

    def test_unknown_product_or_source_and_unsafe_reading_path_are_rejected(self):
        for mutate in [
            lambda d: d['questions'][0].update(tags=['missing-topic']),
            lambda d: d['questions'][0]['products'][0].update(id='missing-hand'),
            lambda d: d['questions'][0]['claims'][0].update(source='missing-source'),
            lambda d: d['questions'][0]['related'][0].update(path='../AGENTS.md'),
        ]:
            d = copy.deepcopy(self.document)
            mutate(d)
            with self.assertRaises(ValueError):
                questions.validate(d, self.hands)

    def test_index_and_all_pages_render_without_unresolved_placeholders(self):
        for key in ['index'] + [q['id'] for q in self.document['questions']]:
            path = ROOT / 'website/docs/questions' / (key + '.md')
            body = questions.on_page_markdown(path.read_text(encoding='utf-8'), self.page(key), self.config, [])
            html = markdown.markdown(body.split('---', 2)[-1], extensions=['attr_list', 'md_in_html', 'tables', 'toc'])
            html = questions.on_page_content(html, self.page(key), self.config, [])
            self.assertNotIn('<!-- questions:', html)
            self.assertIn('question-reader', html)
            if key != 'index':
                self.assertIn('class="question-claim"', html)
                self.assertIn('方案设计 · 尚未执行', html)
                self.assertIn('question-products', html)
                for anchor in ['judgement', 'evidence', 'verification', 'products', 'gaps', 'reading', 'sources']:
                    self.assertIn('id="' + anchor + '"', html)

    def test_final_chrome_keeps_readers_inside_the_layout_and_shared_brand(self):
        spec = importlib.util.spec_from_file_location('question_chrome', ROOT / 'website/hooks/knowledge.py')
        chrome = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(chrome)
        for key in ['index'] + [q['id'] for q in self.document['questions']]:
            page = self.page(key)
            path = ROOT / 'website/docs/questions' / (key + '.md')
            body = questions.on_page_markdown(path.read_text(encoding='utf-8'), page, self.config, [])
            html = markdown.markdown(body.split('---', 2)[-1], extensions=['attr_list', 'md_in_html', 'tables', 'toc'])
            html = questions.on_page_content(html, page, self.config, [])
            html = chrome.on_page_content(html, page, self.config, [])
            structure = ReadingStructure()
            structure.feed(html)
            with self.subTest(page=key):
                self.assertEqual(structure.errors, [])
                self.assertEqual(structure.headings, 1 if key == 'index' else 2)
                self.assertIn('<h1>DexTrail<span>.</span></h1>', html)
                self.assertNotIn('question-brand-wordmark', html)
                self.assertEqual(structure.entries, 8 if key == 'index' else 0)
                self.assertIn('knowledge-tag-rail', html)
                self.assertIn('dex-scroll-nav', html)
                self.assertNotIn('question-sidebar\"', html)
                if key == 'index':
                    self.assertEqual(html.count('data-topic-item=\"1\"'), 8)
                else:
                    self.assertIn('data-topic-mode=\"links\"', html)
                self.assertIn('全部网站栏目', html)

    def test_product_relations_are_explicit_and_bidirectional(self):
        page = SimpleNamespace(file=SimpleNamespace(src_uri='hands/generated/tars-dexhand.md'), url='hands/generated/tars-dexhand/')
        body = questions.on_page_content('<h2>完整技术记录</h2>', page, self.config, [])
        self.assertEqual(body.count('id="record-questions"'), 1)
        for q in self.document['questions']:
            expected = any(p['id'] == 'tars-dexhand' for p in q['products'])
            self.assertEqual(('questions/' + q['id'] + '/') in body, expected)
        self.assertNotIn('H-Gloves', body)
        self.assertNotIn('TARS-Dex 视触觉夹爪', body)

    def test_unmapped_product_gets_overview_without_invented_relation(self):
        page = SimpleNamespace(file=SimpleNamespace(src_uri='hands/generated/unmapped.md'), url='hands/generated/unmapped/')
        html = questions.on_page_content('<h2>完整技术记录</h2>', page, self.config, [])
        self.assertIn('查看全部关键问题', html)
        self.assertNotIn('<li>', html)

    def test_non_product_content_is_unchanged_and_templates_are_empty(self):
        page = self.page('index')
        self.assertEqual(questions.on_page_content('body', page, self.config, []), 'body')
        for name in ['performance-record', 'reliability-record']:
            lines = (ROOT / 'website/docs/resources/templates' / (name + '.csv')).read_text().splitlines()
            self.assertEqual(len(lines), 1, 'Download is a blank template, not fabricated results')


if __name__ == '__main__':
    unittest.main()
