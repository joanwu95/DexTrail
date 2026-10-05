"""Reviewed sensing records shared by product profiles, tags and comparisons."""
import html
import json
from datetime import date
from urllib.parse import urlsplit

STATUS = {'documented': '资料明确支持', 'absent': '此配置未配备',
          'unknown': '尚未核实', 'unvalidated': '估计链路未验证'}
FIELDS = [('quantity', '测什么'), ('location', '测在哪里'), ('output', '输出与单位'),
          ('rate', '更新 / 查询频率'), ('calibration', '标定情况'),
          ('configuration', '配置范围'), ('control', '用于什么控制'), ('boundary', '不能据此断言什么')]


def load(path, hands, terms, require):
    document = json.loads(path.read_text(encoding='utf-8'))
    require(document.get('schema_version') == 1, '感知记录 schema_version 应为 1')
    stages = document.get('stages', [])
    stage_ids = [s['id'] for s in stages]
    require(len(stage_ids) == len(set(stage_ids)), '感知位置 ID 重复')
    require(set(stage_ids) == {'motor', 'transmission', 'joint', 'contact'}, '感知位置不完整')
    audits = document.get('hands', {})
    require(set(audits) <= set(hands), '感知记录引用了不存在的产品')
    for key, audit in audits.items():
        require(bool(audit.get('version')), f'{key}: 感知记录必须注明版本')
        date.fromisoformat(audit['checked_on'])
        sources = audit.get('sources', {})
        for source in sources.values():
            address = urlsplit(source.get('url', ''))
            require(address.scheme in {'http', 'https'} and bool(address.netloc)
                    and bool(source.get('title')) and bool(source.get('locator')),
                    f'{key}: 感知来源缺少标题、定位或 HTTP(S) URL')
        channels = audit.get('channels', [])
        require(bool(channels), f'{key}: 感知通道为空')
        require(len({c['id'] for c in channels}) == len(channels), f'{key}: 感知通道重复')
        for channel in channels:
            require(channel.get('stage') in stage_ids and channel.get('status') in STATUS,
                    f'{key}: 非法感知位置或状态')
            require(bool(channel.get('label')) and all(bool(channel.get(k)) for k, _ in FIELDS),
                    f'{key}: 感知通道缺少测量说明')
            require(bool(channel.get('sources')) and set(channel['sources']) <= set(sources),
                    f'{key}: 感知通道缺少有效来源')
            tag = channel.get('tag')
            require(not tag or (tag in terms and channel['status'] == 'documented'),
                    f'{key}: 未验证或未配备通道不能添加能力标签')
        hands[key]['sensing_audit'] = audit
    return document


def references(audit, channel):
    return [audit['sources'][key] for key in channel['sources']]


def tags(audit, terms):
    result = []
    for channel in audit['channels']:
        if not channel.get('tag'):
            continue
        result.append(dict(group='sensing', id='sensing:' + channel['tag'],
                           label=channel.get('tag_label', terms[channel['tag']]['name']),
                           scope=audit['version'] + '。' + channel['quantity'] + ' ' + channel['boundary'],
                           target='record-sensing', sources=references(audit, channel)))
    return result


def markdown(audit):
    def escape(value):
        return html.escape(value).replace('|', ' / ').replace('\n', ' ')
    lines = ['### 感知通道逐项核查', '', f"**版本：{escape(audit['version'])}** · 资料复核：{audit['checked_on']}",
             '', '以下是原始资料的具体内容转述；工程解读单独标注。频率来自资料或接口说明，未在本机测量。', '']
    for channel in audit['channels']:
        lines += [f"#### {escape(channel['label'])} · {STATUS[channel['status']]}", '',
                  '| 核查项 | 资料说明 |', '| --- | --- |']
        lines += [f'| {label} | {escape(channel[key])} |' for key, label in FIELDS]
        if channel.get('interpretation'):
            lines += ['', '**工程解读：** ' + escape(channel['interpretation'])]
        lines += ['', ' · '.join(f"[{escape(s['title'])} · {escape(s['locator'])}](<{s['url']}>)"
                                 for s in references(audit, channel)), '']
    lines += ['[打开测量位置图：这些量分别测在哪里？](../../../engineering/sensing-chain/)', '']
    return '\n'.join(lines)


def comparison_cell(audit):
    sources, seen = [], set()
    for source in audit['sources'].values():
        if source['url'] not in seen:
            sources.append(source)
            seen.add(source['url'])
    return dict(value='\n\n'.join(c['label'] + ' · ' + STATUS[c['status']] + '：' + c['quantity']
                                  for c in audit['channels']),
                scope=audit['version'] + ' · 复核 ' + audit['checked_on'] + '；未开展实物验证。',
                sources=sources,
                explanations=[dict(title=c['label'], kind='fact',
                                   text='\n'.join(label + '：' + c[k] for k, label in FIELDS))
                              for c in audit['channels']] +
                             [dict(title=c['label'], kind='interpretation', text=c['interpretation'])
                              for c in audit['channels'] if c.get('interpretation')])


def payload(data):
    return dict(stages=data['sensing_audits']['stages'], statuses=STATUS, fields=FIELDS,
                hands=[dict(id=h['id'], name=h['name'], **h['sensing_audit'])
                       for h in data['hands'] if h.get('sensing_audit')])
