"""Apply field-level source reviews to every published hand representation."""
import json
from datetime import date
from urllib.parse import urlsplit


def apply_reviews(path, hands, sources, fields, require):
    document = json.loads(path.read_text(encoding='utf-8'))
    require(document.get('schema_version') == 1, '参数复核 schema_version 应为 1')
    records = document.get('hands', {})
    require(set(records) <= set(hands), '参数复核引用不存在的手')
    for key, record in records.items():
        date.fromisoformat(record['checked_on'])
        require(bool(record.get('scope')), f'{key}: 参数复核缺少版本范围')
        reviewed = record.get('fields', {})
        require(set(reviewed) <= set(fields), f'{key}: 参数复核含未知字段')
        for field, entry in reviewed.items():
            require(isinstance(entry.get('value'), (str, int, float)) and bool(str(entry['value']).strip()), f'{key}/{field}: 参数复核缺少值')
            refs = entry.get('sources', [])
            require(bool(refs), f'{key}/{field}: 参数复核缺少来源')
            ids = []
            for i, source in enumerate(refs):
                url = urlsplit(source.get('url', ''))
                require(url.scheme in {'http', 'https'} and bool(url.netloc) and bool(source.get('title')) and bool(source.get('locator')), f'{key}/{field}: 来源缺少地址、标题或阅读位置')
                sid = f'{key}-reviewed-{field}-{i}'
                sources.append(dict(id=sid, title=source['title'], url=source['url'], kind=source.get('kind', 'official'), version=record['scope']+' · '+source['locator'], verified_on=record['checked_on']))
                ids.append(sid)
            hands[key].setdefault('facts', {})[field] = dict(value=entry['value'], sources=ids)
            hands[key].setdefault('resources', []).extend(ids)
        hands[key]['fact_review'] = record
    return document
