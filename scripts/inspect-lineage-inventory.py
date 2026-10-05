"""Print a compact, source-linked inventory for a full lineage review (read-only)."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('atlas', ROOT / 'website/hooks/atlas.py')
atlas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(atlas)
data = atlas.load_data(ROOT / 'data', ROOT / 'website/docs')
reviews = json.loads((ROOT / 'data/hand-kinematics.json').read_text(encoding='utf-8'))
for hand in data['hands']:
    review = reviews.get(hand['id'], {})
    timeline = hand.get('timeline', {})
    print(json.dumps(dict(id=hand['id'], name=hand['name'],
                         organization=review.get('basic', {}).get('company'),
                         timeline=timeline, summary=review.get('summary'),
                         sources=review.get('sources', [])), ensure_ascii=False))
