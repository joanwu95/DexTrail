"""Refresh map from the same validated records as product pages."""
from pathlib import Path
import importlib.util
import json
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("atlas", ROOT / "website/hooks/atlas.py")
atlas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(atlas)
data = atlas.load_data(ROOT / "data", ROOT / "website/docs")
payload = atlas.map_payload(data)
hands = payload["hands"]
target = ROOT / "website/docs/visual-lab/specimens.json"
target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
print(f"Map: {len(hands)} products; {sum(bool(h['media']) for h in hands)} media entries")
