#!/usr/bin/env python3
"""修正編碼表排序
"""

import sys
import os
import argparse
import logging
import re
import yaml

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
log = logging.getLogger()

def sort(file):
    def key_func(x):
        if len(x) <= columns: # 欄數不足者（空行或註解）排最前
            return ('', -1)
        elif 0x4E00 <= ord(x[char_idx]) <= 0x9FFF: # 統一區，不改變順序
            order = 0
        elif 0x3400 <= ord(x[char_idx]) <= 0x4DBF or 0x20000 <= ord(x[char_idx]) <= 0x3FFFF: # Ext-A~G+ 按 Unicode 排序
            order = ord(x[char_idx])
        else: # 其他非漢字符號，排最後面，按 Unicode 排序
            order = 0x10FFFF + 1 + ord(x[char_idx])

        return (x[code_idx], order)

    with open(file, 'r', encoding='UTF-8', newline=None) as f:
        text0 = text = f.read()
        f.close()

    m = re.match(r'^(.*?\n\.\.\.(?:\n|$))?(.*?)(\n\s*)?$', text, flags=re.S)
    header, lines, footer = m.group(1) or '', m.group(2) or '', m.group(3) or ''

    if header:
        config = yaml.load(header, Loader=yaml.FullLoader)
        code_idx = config['columns'].index('code')
        char_idx = config['columns'].index('text')
    else:
        code_idx = 0
        char_idx = 1

    columns = max(code_idx, char_idx)

    lines = [x.split('\t') for x in lines.split('\n')]
    lines = sorted(lines, key=key_func)
    lines = '\n'.join('\t'.join(x) for x in lines)

    text = header + lines + footer

    if text == text0:
        return

    with open(file, 'w', encoding='UTF-8') as f:
        f.write(text)
        f.close()

def main():
    # 解析指令參數
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('path', help="""要處理的檔案""")
    args = parser.parse_args()

    # 開始修改
    log.info("sorting {}".format(args.path))
    sort(args.path)

if __name__ == "__main__":
    main()
