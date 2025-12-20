#!/usr/bin/env python3
"""將 .yaml 檔文字化以利差異比對

- 設定 git diff 比對此腳本文字化的內容（比對增刪字碼）：
  git config diff.yamldict.textconv 'python /PATH/TO/textconv.py -m=char2codes'
"""

import sys
import os
import argparse
import logging
import re
import json
import yaml

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
log = logging.getLogger()

def textconv(file, mode='char2codes', format='text'):
    # load file to text
    if file == '-':
        text = text0 = sys.stdin.read()
    else:
        with open(file, 'r', encoding='UTF-8', newline=None) as f:
            text = text0 = f.read()
            f.close()

    m = re.match(r'^(.*?\n\.\.\.(?:\n|$))?(.*?)(\n\s*)?$', text, flags=re.S)
    header, lines, footer = m.group(1) or '', m.group(2), m.group(3)

    if header:
        config = yaml.load(header, Loader=yaml.FullLoader)
        code_idx = config['columns'].index('code')
        char_idx = config['columns'].index('text')
    else:
        code_idx = 0
        char_idx = 1

    lines = [x.split('\t') for x in lines.split('\n')]

    if mode == 'code2chars':
        # make dict
        dict = {}
        for line in lines:
            if len(line) <= 1: continue
            if line[code_idx] not in dict: dict[line[code_idx]] = []
            dict[line[code_idx]].append(line[char_idx])

        # generate output
        if format == 'json':
            output = json.dumps(dict, ensure_ascii=False)
        else: # default: text
            lines = '\n'.join(f"{code}\t{' '.join(dict[code])}" for code in sorted(dict.keys()))
            output = header + lines + footer

    else: # default: char2codes
        dict = {}
        for line in lines:
            if len(line) <= 1: continue
            if line[char_idx] not in dict: dict[line[char_idx]] = []
            dict[line[char_idx]].append(line[code_idx])

        # generate output
        if format == 'json':
            output = json.dumps(dict, ensure_ascii=False)
        else: # default: text
            lines = '\n'.join(f"{char}\t{' '.join(dict[char])}" for char in sorted(dict.keys()))
            output = header + lines + footer

    print(output)

def main():
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
<mode> 可用選項：
  - char2codes: 適於比對增刪字碼
  - code2chars: 適於比對重碼字排序

<format> 可用選項：
  - text: 純文字輸出
  - json: JSON 格式輸出""")
    parser.add_argument('file',
        help="""要轉換的檔案，或用 "-" 讀取標準輸入。""")
    parser.add_argument('-m', '--mode', default='char2codes',
        choices=['char2codes', 'code2chars'], metavar='<mode>',
        help="""轉換模式，預設 "%(default)s"。""")
    parser.add_argument('-f', '--format', default='text',
        choices=['text', 'json'], metavar='<format>',
        help="""輸出格式，預設 "%(default)s"。""")
    args = parser.parse_args()
    textconv(args.file, mode=args.mode, format=args.format)

if __name__ == "__main__":
    main()
