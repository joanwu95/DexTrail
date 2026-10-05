"""Curated historical labels, bounded by each event's own historical sources."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'data/field-development.json'
document = json.loads(path.read_text(encoding='utf-8'))
labels = {
    'okada-1974': ['tactile-sensing', 'joint-sensing', 'shape-recognition'],
    'stanford-jpl-1982': ['kinematics', 'force-control'],
    'utah-mit-1986': ['modular-design', 'system-integration', 'maintenance'],
    'barrett-1993': ['product-platform'],
    'dlr-hand-i-1998': ['integrated-actuation', 'system-integration'],
    'dlr-hand-ii-2001': ['joint-sensing', 'system-integration'],
    'hit-dlr-2003': ['integrated-actuation', 'manufacturing'],
    'dlr-hit-ii-2008': ['modular-design', 'integrated-actuation', 'system-integration'],
    'schunk-sdh-2008': ['modular-design', 'tactile-sensing', 'system-integration'],
    'robotiq-2010': ['adaptive-grasping', 'product-platform'],
    'allegro-v1-2012': ['product-platform'],
    'adaptive-synergies-2014': ['tendon-driven', 'underactuated', 'compliant-mechanics', 'adaptive-grasping'],
    'learning-in-hand-2018': ['learning-based', 'sim-to-real', 'in-hand-manipulation'],
    'qb-research-2018': ['tendon-driven', 'compliant-mechanics', 'adaptive-grasping', 'system-integration'],
    'rubiks-cube-2019': ['visual-sensing', 'learning-based', 'sim-to-real', 'in-hand-manipulation'],
    'trifinger-2020': ['open-platform', 'learning-platform'],
    'leap-2023': ['open-platform', 'learning-based', 'sim-to-real'],
    'dexee-2024': ['maintenance', 'tactile-sensing', 'learning-platform'],
    'anyrotate-2024': ['tactile-sensing', 'learning-based', 'sim-to-real', 'in-hand-manipulation'],
    'allegro-v5-2024': ['tactile-sensing', 'maintenance', 'product-platform'],
    'dexumi-2025': ['demonstration-data', 'learning-based'],
    'allegro-v6f-2026': ['tactile-sensing', 'contact-data', 'product-platform']
}
assert set(labels).issubset({event['id'] for event in document['events']})
for event in document['events']:
    if event['id'] not in labels:
        continue
    event['tags'] = [event['track']] + labels[event['id']]
    event['tag_sources'] = {tag: event['source_ids'] for tag in event['tags']}
document.setdefault('selection', {
    'type': 'curated',
    'description': '精选能说明研究问题、技术方案或产品使用需求变化的节点；不按每家企业或每款手逐项铺开。',
    'criteria': ['具有明确时间和原始来源', '说明具体技术变化或研究问题', '区分论文结果、产品记录与工程解读']
})
path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f"Tagged {len(document['events'])} curated events")
