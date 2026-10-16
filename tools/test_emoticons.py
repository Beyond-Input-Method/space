#!/usr/bin/env python3
"""验证生成配置；共享 YAML 读取另由 bimkit 原生测试覆盖。"""
import hashlib
import io
import json
from pathlib import Path
import re
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
import generate_emoticons as generator

ROOT = Path(__file__).resolve().parents[1]


def groups(pack, root=ROOT):
    result = []
    for line in (root/'emoticons'/pack/'emoticon.yaml').read_text().splitlines():
        if line.startswith('- id: '): result.append({'id':json.loads(line[6:]), 'items':[]})
        elif line.startswith('  name: '): result[-1]['name'] = json.loads(line[8:])
        elif line.startswith('    - '): result[-1]['items'].append(json.loads(line[6:]))
    return result


def entries(pack):
    return [value for group in groups(pack) for value in group['items']]


class FormalPacksTest(unittest.TestCase):
    def test_only_two_official_packs(self):
        self.assertEqual({p.name for p in (ROOT/'emoticons').iterdir() if p.is_dir()}, {'default','kaomoji'})
        self.assertIn('name: 颜文字', (ROOT/'emoticons/kaomoji/info.yaml').read_text())

    def test_emoji_official_categories_are_exact_rgi_partition(self):
        expected = set()
        for line in generator.SOURCE.read_text().splitlines():
            match = re.match(r'^([0-9A-F ]+)\s*;\s*(fully-qualified|component)\s*#',line)
            if match: expected.add(''.join(chr(int(cp,16)) for cp in match[1].split()))
        official = groups('default')[1:]
        actual = [value for group in official for value in group['items']]
        self.assertEqual(len(expected),3972)
        self.assertEqual(set(actual),expected)
        self.assertEqual(len(actual),len(expected))
        self.assertEqual({g['name'] for g in official},set(generator.CATEGORY_IDS))
        self.assertEqual(len(official),21)
        self.assertTrue(all('与' not in g['name'] and '&' not in g['name'] for g in official))
        by_name = {g['name']:g['items'] for g in official}
        self.assertIn('😀',by_name['笑脸']); self.assertIn('❤️',by_name['情感'])
        self.assertIn('👍',by_name['手势']); self.assertIn('🧠',by_name['身体'])
        self.assertIn('☕',by_name['饮品']); self.assertIn('🚗',by_name['交通'])
        self.assertIn('⚽',by_name['运动']); self.assertNotIn('⚽',by_name['活动'])

    def test_common_is_sourced_shortcut_not_removed_from_canonical_groups(self):
        actual = groups('default')
        common = actual[0]
        self.assertEqual((common['id'],common['name']),('common','常用'))
        self.assertEqual(len(common['items']),64)
        self.assertEqual(len(set(common['items'])),64)
        official = [value for group in actual[1:] for value in group['items']]
        self.assertTrue(set(common['items']) <= set(official))
        self.assertEqual(len(entries('default')),4036)
        source = json.loads(generator.COMMON_SOURCE.read_text())
        self.assertEqual(common['items'],[item['text'] for item in source['items']])
        self.assertEqual(source['sources'][0]['data_year'],2019)
        self.assertEqual({x['basis'] for x in source['items']},{'unicode-frequency-2019','chinese-chat-curation'})

    def test_kaomoji_merge_preserves_every_original_string(self):
        expected_single = {v for _,_,items in generator.single() for v in items}
        expected_multi = {v for _,_,items in generator.multiline() for v in items}
        actual = entries('kaomoji')
        self.assertEqual(len(actual),1296)
        self.assertEqual(len(set(actual)),1296)
        self.assertEqual(set(actual),expected_single | expected_multi)
        self.assertEqual(sum('\n' not in v for v in actual),1074)
        self.assertEqual(sum('\n' in v for v in actual),222)
        self.assertIn(' /\\_/\\\n( o.o )\n > ^ <',actual)
        self.assertTrue(all(v.strip() and '\t' not in v and '\r' not in v for v in actual))
        themes = groups('kaomoji')
        self.assertEqual(len(themes),32)
        self.assertEqual(len({g['name'] for g in themes}),32)
        for g in themes:
            shapes = ['\n' in v for v in g['items']]
            self.assertEqual(shapes,sorted(shapes))

    def test_generation_is_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory); (temporary/'tools').mkdir()
            with patch.object(generator,'ROOT',temporary), redirect_stdout(io.StringIO()): generator.main()
            for pack in ['default','kaomoji']:
                for name in ['emoticon.yaml','info.yaml']:
                    relative = Path('emoticons')/pack/name
                    self.assertEqual((temporary/relative).read_bytes(),(ROOT/relative).read_bytes())
            self.assertEqual((temporary/'tools/emoticon-manifest.json').read_bytes(),(ROOT/'tools/emoticon-manifest.json').read_bytes())

    def test_manifest_distinguishes_unique_items_and_shortcuts(self):
        manifest = json.loads((ROOT/'tools/emoticon-manifest.json').read_text())
        self.assertEqual(hashlib.sha256(generator.SOURCE.read_bytes()).hexdigest(),manifest['emoji_source_sha256'])
        self.assertEqual(hashlib.sha256(generator.COMMON_SOURCE.read_bytes()).hexdigest(),manifest['common_source_sha256'])
        for pack,expected in manifest['packs'].items():
            config = ROOT/'emoticons'/pack/'emoticon.yaml'; values = entries(pack); parsed = groups(pack)
            self.assertLess(config.stat().st_size,2*1024*1024)
            self.assertEqual(len(set(values)),expected['items'])
            self.assertEqual(len(values),expected['display_entries'])
            self.assertEqual(hashlib.sha256(config.read_bytes()).hexdigest(),expected['sha256'])
            self.assertEqual(len(parsed),expected['groups'])
            self.assertEqual(len(parsed),len({g['id'] for g in parsed}))

    def test_retirement_only_removes_exact_official_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); old = root/'emoticons/multiline-kaomoji'; old.mkdir(parents=True)
            originals = {'info.yaml':b'official info', 'emoticon.yaml':b'official content'}
            for name,data in originals.items(): (old/name).write_bytes(data)
            manifest = root/'retired.json'
            manifest.write_text(json.dumps({'multiline-kaomoji':{'replacement':'kaomoji','files':{n:hashlib.sha256(b).hexdigest() for n,b in originals.items()}}}))
            with patch.object(generator,'ROOT',root),patch.object(generator,'RETIRED_SOURCE',manifest):
                (old/'emoticon.yaml').write_bytes(b'custom')
                self.assertEqual(generator.retire_official_packs()['multiline-kaomoji'],'preserved-custom')
                (old/'emoticon.yaml').write_bytes(originals['emoticon.yaml']); (old/'extra.txt').write_text('custom')
                self.assertEqual(generator.retire_official_packs()['multiline-kaomoji'],'preserved-custom')
                (old/'extra.txt').unlink()
                self.assertEqual(generator.retire_official_packs()['multiline-kaomoji'],'retired-official')
                self.assertFalse(old.exists())

    def test_retirement_never_follows_directory_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); target=root/'custom';target.mkdir();(target/'info.yaml').write_text('private')
            packs=root/'emoticons';packs.mkdir();(packs/'multiline-kaomoji').symlink_to(target,target_is_directory=True)
            with patch.object(generator,'ROOT',root):
                self.assertEqual(generator.retire_official_packs()['multiline-kaomoji'],'preserved-custom')
                self.assertEqual((target/'info.yaml').read_text(),'private')

if __name__ == '__main__': unittest.main()
