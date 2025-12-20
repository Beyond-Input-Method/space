#!/usr/bin/env python3
"""比對兩個編碼表的差異
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

def load(file):
    """將 yaml 資料檔載入為物件化編碼資料
    """
    with open(file, 'r', encoding='UTF-8', newline=None) as f:
        text = f.read()
        f.close()

    m = re.match(r'^(.*?\n\.\.\.(?:\n|$))?(.*?)(\n\s*)?$', text, flags=re.S)
    header, body, footer = m.group(1) or '', m.group(2) or '', m.group(3) or ''

    if header:
        config = yaml.load(header, Loader=yaml.FullLoader)
        code_idx = config['columns'].index('code')
        char_idx = config['columns'].index('text')
    else:
        code_idx = 0
        char_idx = 1

    data = {}
    for line in body.splitlines():
        if line.startswith('#'): continue

        line = line.split('\t')
        if len(line) <= 1: continue

        data.setdefault(line[char_idx], []).append(line[code_idx])

    return data

def diff(file1, file2=None, file3=None, mode='json'):
    """計算差異資料並輸出
    """
    def chars_to_codes(chars):
        """將字串轉為 Unicode 碼序列
        """
        return ' '.join(f"U+{ord(char):04X}" for char in chars)

    # load file# to dict#
    if file2 is not None:
        dict1 = load(file1)
        dict2 = load(file2)
    else:
        dict1 = {}
        dict2 = load(file1)

    if file3 is not None:
        dict3 = load(file3)
    else:
        dict3 = None

    # diff dict1 and dict2 to delta
    delta = {}
    for char, codes in dict2.items():
        for code in codes:
            if char not in dict1 or code not in dict1[char]:
                delta.setdefault(char, {'ins': [], 'del': []})['ins'].append(code)

    for char, codes in dict1.items():
        for code in codes:
            if char not in dict2 or code not in dict2[char]:
                delta.setdefault(char, {'ins': [], 'del': []})['del'].append(code)

    # filter using file3
    if dict3 is not None:
        for char, item in list(delta.items()):
            item['ins'] = [code for code in item['ins'] if not dict3.get(char, []).get(code)]
            item['del'] = [code for code in item['del'] if dict3.get(char, []).get(code)]
            if not len(item['ins']) and not len(item['del']):
                del delta[char]

    # 將差異資料轉為文字輸出
    if mode == 'ins_del':
        for char, item in delta.items():
            print(f"{char}\t{','.join(item['ins'])}\t{','.join(item['del'])}")

    elif mode == 'ins_del_m':
        for char, item in delta.items():
            equivs = [code for code in dict1.get(char, []) if code not in item['del']]
            print(f"{char} ({chars_to_codes(char)})\t+{','.join(item['ins'])}\t-{','.join(item['del'])}\t={','.join(equivs)}")

    elif mode == 'old_new':
        for char in delta:
            print(f"{char}\t{','.join(dict1.get(char, []))}\t{','.join(dict2.get(char, []))}")

    elif mode == 'old_new_m':
        for char in delta:
            print(f"{char} ({chars_to_codes(char)})\to:{','.join(dict1.get(char, []))}\tn:{','.join(dict2.get(char, []))}")

    else: # default: json
        print(json.dumps(delta, ensure_ascii=False))

def main():
    # 解析指令參數
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('file1',
        help="""檔案1，差異比對修訂前；若省略檔案2則輸出此檔案全部內容""")
    parser.add_argument('file2', nargs='?',
        help="""檔案2，差異比對修訂後""")
    parser.add_argument('file3', nargs='?',
        help="""檔案3，自輸出內容濾除此檔案已有的內容""")
    parser.add_argument('-m', "--mode", default='ins_del_m',
        choices=['json', 'ins_del', 'ins_del_m', 'old_new', 'old_new_m'],
        help="""輸出模式，預設：%(default)s""")
    args = parser.parse_args()

    # 開始比對
    diff(args.file1, args.file2, args.file3, mode=args.mode)

if __name__ == "__main__":
    main()
