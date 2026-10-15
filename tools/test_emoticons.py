#!/usr/bin/env python3
"""校验生成配置的数据契约；运行时 YAML 解析另外由 bimkit 验证。"""
import hashlib
import json
from pathlib import Path
import re
import unittest
import tempfile
from unittest.mock import patch
from contextlib import redirect_stdout
import io
import generate_emoticons as generator

ROOT = Path(__file__).resolve().parents[1]


def entries(pack):
    # 生成器的每个条目都是 JSON 字符串（YAML 的合法子集），直接还原实际字符串。
    return [json.loads(line.removeprefix('    - ')) for line in (ROOT/'emoticons'/pack/'emoticon.yaml').read_text().splitlines() if line.startswith('    - ')]


class FormalPacksTest(unittest.TestCase):
    def test_only_three_formal_packs(self):
        self.assertEqual({p.name for p in (ROOT/'emoticons').iterdir() if p.is_dir()}, {'default','kaomoji','multiline-kaomoji'})

    def test_emoji_is_exact_official_rgi_set(self):
        expected = set()
        for line in generator.SOURCE.read_text().splitlines():
            match = re.match(r'^([0-9A-F ]+)\s*;\s*(fully-qualified|component)\s*#',line)
            if match:
                expected.add(''.join(chr(int(cp,16)) for cp in match[1].split()))
        actual = entries('default')
        self.assertGreater(len(expected),3900)
        self.assertEqual(set(actual),expected)
        self.assertEqual(len(actual),len(expected))

    def test_text_shape_and_uniqueness(self):
        for pack,minimum,multiline in [('kaomoji',1000,False),('multiline-kaomoji',200,True)]:
            values = entries(pack)
            self.assertGreaterEqual(len(values),minimum)
            self.assertEqual(len(values),len(set(values)))
            self.assertTrue(all(('\n' in value)==multiline and value.strip() for value in values))
            self.assertTrue(all('\t' not in value and '\r' not in value for value in values))
        self.assertIn(' /\\_/\\\n( o.o )\n > ^ <',entries('multiline-kaomoji'))

    def test_generation_is_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            (temporary/'tools').mkdir()
            with patch.object(generator, 'ROOT', temporary), redirect_stdout(io.StringIO()):
                generator.main()
            for pack in ['default','kaomoji','multiline-kaomoji']:
                for name in ['emoticon.yaml','info.yaml']:
                    relative = Path('emoticons')/pack/name
                    self.assertEqual((temporary/relative).read_bytes(),(ROOT/relative).read_bytes())
            self.assertEqual((temporary/'tools/emoticon-manifest.json').read_bytes(),(ROOT/'tools/emoticon-manifest.json').read_bytes())

    def test_manifest_matches_files(self):
        manifest = json.loads((ROOT/'tools/emoticon-manifest.json').read_text())
        self.assertEqual(hashlib.sha256(generator.SOURCE.read_bytes()).hexdigest(),manifest['emoji_source_sha256'])
        for pack,expected in manifest['packs'].items():
            config = ROOT/'emoticons'/pack/'emoticon.yaml'
            self.assertLess(config.stat().st_size,2*1024*1024)
            self.assertEqual(len(entries(pack)),expected['items'])
            self.assertEqual(hashlib.sha256(config.read_bytes()).hexdigest(),expected['sha256'])
            ids = [json.loads(line[6:]) for line in config.read_text().splitlines() if line.startswith('- id: ')]
            self.assertEqual(len(ids),expected['groups'])
            self.assertEqual(len(ids),len(set(ids)))

if __name__ == '__main__':
    unittest.main()
