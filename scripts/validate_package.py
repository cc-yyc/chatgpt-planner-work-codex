"""Validate distributable structure and executable handoff schema; no network or writes."""
from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
NAME = 'chatgpt-planner-work-codex'
SKILL = ROOT / 'skills' / NAME


def validate() -> dict:
    checks = []

    def check(label, condition):
        if not condition:
            raise ValueError(label)
        checks.append(label)

    manifest = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))
    legacy = json.loads((ROOT / '.codex-plugin' / 'plugin.json').read_text(encoding='utf-8'))
    marketplace = json.loads((ROOT / '.agents' / 'plugins' / 'marketplace.json').read_text(encoding='utf-8'))
    text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    match = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    check('SKILL frontmatter exists', match is not None)
    frontmatter = yaml.safe_load(match.group(1))
    check('skill name and folder match', frontmatter['name'] == SKILL.name == NAME)
    check('name syntax', bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', NAME)) and len(NAME) < 64)
    check('discovery description is bounded', isinstance(frontmatter['description'], str) and 0 < len(frontmatter['description']) <= 1024)
    check('supported frontmatter only', set(frontmatter) <= {'name', 'description', 'license', 'allowed-tools', 'metadata'})
    check('plugin and skill versions match', manifest['version'] == legacy['version'] == frontmatter['metadata']['version'])
    check('plugin identities match', manifest['name'] == legacy['name'] == NAME)
    check('compatibility manifest resolves skills', (ROOT / legacy['skills']).resolve() == SKILL.parent.resolve())
    check('no MCP servers or hooks bundled', not any((ROOT / p).exists() for p in ['mcp.json', '.mcp.json', 'hooks', 'hooks.json']))
    entry, = marketplace['plugins']
    check('marketplace identity', marketplace['name'] == 'planner-work-codex-local' and entry['name'] == NAME)
    check('marketplace source resolves inside package', entry['source']['source'] == 'local' and (ROOT / entry['source']['path']).resolve() == ROOT)
    check('marketplace is opt-in available', entry['policy']['installation'] == 'AVAILABLE')
    agent = yaml.safe_load((SKILL / 'agents' / 'openai.yaml').read_text(encoding='utf-8'))
    check('automatic discovery enabled', agent['policy']['allow_implicit_invocation'] is True)
    check('default prompt names skill', '$' + NAME in agent['interface']['default_prompt'])
    check('UI description length', 25 <= len(agent['interface']['short_description']) <= 64)
    license_data = (ROOT / 'LICENSE').read_bytes()
    provenance = json.loads((ROOT / 'UPSTREAM.json').read_text(encoding='utf-8'))
    license_record, = [r for r in provenance['files'] if r['path'] == 'LICENSE']
    check('complete upstream license preserved', hashlib.sha256(license_data).hexdigest() == license_record['sha256'])
    check('standalone skill includes same license', (SKILL / 'LICENSE').read_bytes() == license_data)
    check('standalone skill attribution preserved', (SKILL / 'NOTICE.md').read_bytes() == (ROOT / 'NOTICE.md').read_bytes())
    check('all upstream files accounted for', len(provenance['files']) == 22 and all(r['status'] == 'verified' for r in provenance['files']))
    check('original visual resources excluded', all(not r['redistributed'] for r in provenance['files'] if r['path'].startswith('assets/')) and not (SKILL / 'assets').exists())
    json_files = list(ROOT.rglob('*.json'))
    for path in json_files:
        if '.git' not in path.parts:
            json.loads(path.read_text(encoding='utf-8'))
    check('all distributable JSON parses', True)
    links = []
    markdown_paths = [p for p in ROOT.rglob('*.md') if '.git' not in p.parts]
    for path in markdown_paths:
        content = path.read_text(encoding='utf-8')
        check_path = str(path.relative_to(ROOT))
        if re.search(r'(?im)^\s*\[TODO:[^\n]*\]\s*$', content):
            raise ValueError('unfinished scaffold in ' + check_path)
        for target in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^)]+)\)', content):
            url = target.strip('<>')
            if urlparse(url).scheme or url.startswith('#'):
                continue
            resolved = (path.parent / unquote(url.split('#')[0])).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.exists():
                raise ValueError('broken or escaping link: ' + check_path + ' -> ' + target)
            links.append((check_path, target))
    check('all relative Markdown links resolve within package', len(links) > 0)
    check('exactly one discoverable skill', len(list((ROOT / 'skills').rglob('SKILL.md'))) == 1)
    check('no machine-specific private path bundled', all('C:\\Users\\think book' not in p.read_text(encoding='utf-8') for p in markdown_paths))
    for path in ROOT.rglob('*'):
        if '.git' in path.parts or '__pycache__' in path.parts:
            continue
        if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
            raise ValueError('symlink or escaping package path: ' + str(path))
    check('package paths stay inside root', True)
    schema = json.loads((SKILL / 'references' / 'execution-context.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    valid_context = {
        'goal': 'Export local records to CSV',
        'scope': ['Export date, amount and category'],
        'non_goals': [],
        'implementation_constraints': ['UTF-8; no network upload'],
        'acceptance_criteria': ['CSV values match the source records'],
        'verification': [{'check': 'Compare a generated CSV against a known fixture', 'required': True}],
    }
    check('valid complete handoff accepted', validator.is_valid(valid_context))
    invalid = []
    item = copy.deepcopy(valid_context); del item['goal']; invalid.append(item)
    item = copy.deepcopy(valid_context); item['workflow_mode'] = 'LITE'; invalid.append(item)
    item = copy.deepcopy(valid_context); item['scope'] = []; invalid.append(item)
    item = copy.deepcopy(valid_context); item['goal'] = '  '; invalid.append(item)
    item = copy.deepcopy(valid_context); item['acceptance_criteria'] = ['']; invalid.append(item)
    item = copy.deepcopy(valid_context); item['verification'] = []; invalid.append(item)
    item = copy.deepcopy(valid_context); item['verification'][0]['required'] = 'true'; invalid.append(item)
    item = copy.deepcopy(valid_context); item['verification'][0]['status'] = 'passed'; invalid.append(item)
    item = copy.deepcopy(valid_context); item['non_goals'] = None; invalid.append(item)
    check('malformed handoffs rejected', all(not validator.is_valid(item) for item in invalid))
    return {'status': 'passed', 'checks': len(checks), 'relative_links': len(links), 'schema_cases': 1 + len(invalid), 'details': checks}


if __name__ == '__main__':
    print(json.dumps(validate(), ensure_ascii=False, indent=2))
