#!/usr/bin/env python3
"""从固定版本 Unicode 清单和本文件维护的文字画生成 Emoji、颜文字两个正式表情包。

用法：python3 tools/generate_emoticons.py
只更新 default、kaomoji；仅移除指纹完全匹配的已退役官方包。
"""
from pathlib import Path
import collections
import hashlib
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'tools/data/emoji-test-18.0.txt'
COMMON_SOURCE = ROOT / 'tools/data/emoji-common.json'
RETIRED_SOURCE = ROOT / 'tools/data/retired-emoticon-packs.json'
CATEGORY_IDS = {
    '笑脸':'smileys', '情感':'emotion', '手势':'gestures', '身体':'body', '人物':'people',
    '肤色':'skin-tone', '发型':'hair-style', '动物':'animals', '植物':'plants',
    '食物':'food', '饮品':'drinks', '餐具':'dishware', '地点':'places', '交通':'transport',
    '时间':'time', '天气':'weather', '活动':'activities', '运动':'sports', '物品':'objects', '符号':'symbols', '旗帜':'flags'
}

def category_for(group, subgroup):
    if group == 'Smileys & Emotion': return '情感' if subgroup in {'heart','emotion'} else '笑脸'
    if group == 'People & Body':
        if subgroup.startswith('hand-') or subgroup == 'hands': return '手势'
        return '身体' if subgroup == 'body-parts' else '人物'
    if group == 'Component': return {'skin-tone':'肤色','hair-style':'发型'}[subgroup]
    if group == 'Animals & Nature': return '植物' if subgroup.startswith('plant-') else '动物'
    if group == 'Food & Drink': return {'drink':'饮品','dishware':'餐具'}.get(subgroup,'食物')
    if group == 'Travel & Places':
        if subgroup.startswith('transport-'): return '交通'
        return {'time':'时间','sky & weather':'天气','hotel':'地点'}.get(subgroup,'地点')
    if group == 'Activities': return '运动' if subgroup == 'sport' else '活动'
    return {'Objects':'物品','Symbols':'符号','Flags':'旗帜'}[group]

def quote(value):
    return json.dumps(value, ensure_ascii=False)

def write_pack(pack_id, title, groups, emoji=False):
    directory = ROOT / 'emoticons' / pack_id
    directory.mkdir(parents=True, exist_ok=True)
    seen = set()
    result = []
    for group_id, label, values in groups:
        items = []
        local_seen = set()
        shortcut = emoji and group_id == 'common'
        for value in values:
            assert value and '\r' not in value and '\t' not in value
            assert not emoji or '\n' not in value
            if value not in local_seen and (shortcut or value not in seen):
                local_seen.add(value)
                if not shortcut: seen.add(value)
                items.append(value)
        if items:
            result.append((group_id, label, items))
    lines = ['# 由 tools/generate_emoticons.py 生成；编辑生成器后重新生成。']
    for gid, name, items in result:
        lines += [f'- id: {quote(gid)}', f'  type: {1 if emoji else 0}', f'  name: {quote(name)}', '  items:']
        lines += ['    - ' + quote(value) for value in items]
    (directory / 'emoticon.yaml').write_text('\n'.join(lines) + '\n')
    (directory / 'info.yaml').write_text(f'name: {title}\nversion: 3.0.0\nauthor: BIM\n')
    return {'groups': len(result), 'items':len(seen), 'display_entries':sum(len(items) for _,_,items in result), 'sha256':hashlib.sha256((directory/'emoticon.yaml').read_bytes()).hexdigest()}


def emojis():
    text = SOURCE.read_text()
    assert '# Version: 18.0' in text
    groups = collections.OrderedDict()
    statuses = collections.Counter()
    for line in text.splitlines():
        if line.startswith('# group: '): group = line.removeprefix('# group: ')
        elif line.startswith('# subgroup: '): subgroup = line.removeprefix('# subgroup: ')
        elif line and not line.startswith('#'):
            match = re.match(r'^([0-9A-F ]+)\s*;\s*([\w-]+)\s*#', line)
            if match and match[2] in {'fully-qualified', 'component'}:
                name = category_for(group, subgroup)
                groups.setdefault(name, []).append(''.join(chr(int(cp,16)) for cp in match[1].split()))
                statuses[match[2]] += 1
    assert set(groups) == set(CATEGORY_IDS)
    common = json.loads(COMMON_SOURCE.read_text())
    shortcuts = [item['text'] for item in common['items']]
    official = {value for values in groups.values() for value in values}
    assert len(shortcuts) == 64 and len(set(shortcuts)) == 64
    assert set(shortcuts) <= official, '常用条目必须是完整官方 Emoji 序列'
    values = [(common['id'],common['name'],shortcuts)]
    values += [(CATEGORY_IDS[name],name,items) for name,items in groups.items()]
    return values, statuses

# 每类维护不同表情核心及与情境相符的手势，避免编号、文字标签凑数。
SINGLE = [
('happy','开心', ['(^_^)','(＾▽＾)','(≧▽≦)','(⌒▽⌒)','(o^^o)','(*^▽^*)','(๑˃̵ᴗ˂̵)و','(｡♥‿♥｡)','(✿◠‿◠)','(❁´◡`❁)','(๑´ㅂ`๑)','(●ˇ∀ˇ●)'], ['', 'ﾉ','ノ','✧','♪','♡']),
('greeting','问候', ['(｡･ω･｡)','(＾ω＾)','(・∀・)','(●´ω｀●)','( ´ ▽ ` )','(￣▽￣)','(o´▽`o)','(｡•̀ᴗ-)✧','(˶ᵔ ᵕ ᵔ˶)','(๑•̀ㅂ•́)و'], ['ノ','ﾉﾞ','ﾉ♪','ノ♡','つ','ノ～']),
('cheer','加油', ['(ง •̀_•́)ง','(๑•̀ㅂ•́)و✧','ᕦ(ò_óˇ)ᕤ','٩(ˊᗜˋ*)و','٩(๑❛ᴗ❛๑)۶','( •̀ ω •́ )✧','(๑•̀ㅁ•́๑)✧','(ง •̀ω•́)ง','୧(๑•̀⌄•́๑)૭','ᕙ(⇀‸↼‶)ᕗ'], ['', '✧','☆','♪','!!']),
('love','喜欢', ['(♡˙︶˙♡)','(♡´艸`)','(灬º‿º灬)♡','(｡♥‿♥｡)っ','(づ｡◕‿‿◕｡)づ','(っ˘з(˘⌣˘ )','(๑♡⌓♡๑)','( ˘ ³˘)♥','(ღ˘⌣˘ღ)','(◍•ᴗ•◍)'], ['', '♡','♥','～♡','✿']),
('shy','害羞', ['(⁄ ⁄•⁄ω⁄•⁄ ⁄)','(〃▽〃)','(*/ω＼*)','(//∇//)','(〃ω〃)','(๑´•.̫ • `๑)','(*/▽＼*)','(⁄ ⁄>⁄ ▽ ⁄<⁄ ⁄)','(„• ֊ •„)','(⸝⸝⸝ᵒ̴̶̷ωᵒ̴̶̷⸝⸝⸝)'], ['', '♡','…','♪','～']),
('sad','难过', ['(╥﹏╥)','(T_T)','(ಥ_ಥ)','(｡•́︿•̀｡)','(つ﹏⊂)','(；ω；)','(ノД`)','(｡•́ - •̀｡)','(っ˘̩╭╮˘̩)っ','(இ﹏இ`｡)'], ['', '…','。','｡','っ']),
('angry','生气', ['(╬ Ò﹏Ó)','(＃`Д´)','(｀へ´)','(ง •̀皿•́)ง','(╯°□°）╯','(￣皿￣)','(눈_눈)','(¬_¬)','(｀Д´)','(๑•̀д•́๑)'], ['', '!!','╬','…','ノ']),
('surprise','惊讶', ['Σ(°△°|||)','(⊙_⊙)','(°ロ°)','(゜ロ゜)','(ﾟдﾟ)','(๑°ㅁ°๑)','(꒪⌓꒪)','(ﾉﾟ0ﾟ)ﾉ','(ʘдʘ╬)','(⊙o⊙)'], ['', '！','?!','…','ﾉ']),
('confused','疑惑', ['(・・?)','(・_・ヾ','(｡･д･)？','(・・;)','(⊙_⊙)?','(￣～￣;)','(•ิ_•ิ)?','(๑•̌.•̑๑)','(°ー°〃)','(￢_￢)'], ['', '？','…','ゞ','??']),
('speechless','无语', ['(￣_￣)','(ー_ー)','(눈‸눈)','(=_=)','(；一_一)','(¬_¬ )','(￣▽￣;)','(￢_￢;)','( ˘•ω•˘ )','(；￣Д￣)'], ['', '…','。','|||',';']),
('sleep','困倦', ['(－ω－) zzZ','(￣o￣) . z Z','(∪｡∪)｡｡｡zzZ','(－_－) zzZ','( ˘ω˘ )','(｡-ω-)','(ᴗ˳ᴗ)','(￣ρ￣)..zzZZ','(っ ̯- )','(¦3[▓▓]'], ['', '…','～','｡']),
('comfort','抱抱', ['(づ｡◕‿‿◕｡)づ','(つ≧▽≦)つ','⊂(・▽・⊂)','(つ´∀｀)つ','(つ✧ω✧)つ','(っ´▽`)っ','⊂( ´ ▽ ` )⊃','(っ˘ω˘ς )','(つ･ω･)つ','(づ￣ ³￣)づ'], ['', '♡','♥','～','✿']),
('thanks','感谢', ['(人´∀｀)','(人 •͈ᴗ•͈)','(人´ω｀*)','(人*´∀｀)｡*ﾟ+','(ㅅ´ ˘ `)','(人´▽`*)','(人 •͈ᴗ•͈)✧','(人´∀`)♪','(人˘︶˘*)','(人･ω･)'], ['', '♡','✧','♪','～']),
('sorry','道歉', ['m(_ _)m','(シ_ _)シ','(｡•́︿•̀｡)ゞ','(；′⌒`)','(o_ _)o','(◞‸◟)','(。_。)','(・_・;)','(；´д｀)ゞ','(｡-人-｡)'], ['', '…','。',';','っ']),
('proud','得意', ['(￣▽￣)b','( •̀ᴗ•́ )و','(⌐■_■)','(￣ー￣)','(๑•̀ㅂ•́)و','( ͡° ͜ʖ ͡°)','(¬‿¬)','( •̀∀•́ )','(๑˙ー˙๑)','(＾－＾)V'], ['', '✧','☆','♪','～']),
('dance','跳舞', ['♪┏(・o･)┛♪','└( ＾ω＾ )」','ヾ(⌐■_■)ノ♪','ヽ(⌒▽⌒)ﾉ','♪ヽ(･ˇ∀ˇ･ゞ)','┗(＾0＾)┓','ヘ(￣ω￣ヘ)','(ノ￣ω￣)ノ','♪(┌・。・)┌','ヽ(°◇° )ノ'], ['', '♫','♪','☆']),
('cat','猫咪', ['(=^･ω･^=)','(=^･ｪ･^=)','(=｀ω´=)','ฅ^•ﻌ•^ฅ','(=①ω①=)','(=ＴェＴ=)','(=^-ω-^=)','(=ↀωↀ=)','(=；ェ；=)','(=^‥^=)'], ['', 'ฅ','ﾉ','♡','♪']),
('bear','小熊', ['ʕ•ᴥ•ʔ','ʕᵔᴥᵔʔ','ʕ·ᴥ·ʔ','ʕ•̀ω•́ʔ✧','ʕ≧ᴥ≦ʔ','ʕ´•ᴥ•`ʔ','ʕง•ᴥ•ʔง','ʕっ•ᴥ•ʔっ','ʕ •́؈•̀ ₎','ʕ￫ᴥ￩ʔ'], ['', 'ﾉ','♡','♪','✿']),
('rabbit','兔子', ['／(･ × ･)＼','／(^ x ^)＼','／(=´x`=)＼','／(•ㅅ•)＼','／(≧ x ≦)＼','／(=･ x ･=)＼','／(・ x ・)＼','／(｡･x･｡)＼'], ['', '♡','♪','✧','～']),
('animals','动物', ['(•ө•)♡','(・Θ・)','(•̀ᴗ•́)و ̑̑','U・ᴥ・U','U^ｪ^U','U ´꓃ ` U','(❍ᴥ❍ʋ)','(￣(工)￣)','( ´(00)`)','(･θ･)','(◉Θ◉)','(•ㅂ•)/'], ['', '♪','♡','～']),
('food','吃喝', ['(๑´ڡ`๑)','(っ˘ڡ˘ς)','(๑ᵔ⤙ᵔ๑)','(￣﹃￣)','( ˘▽˘)っ♨','( ^-^)_旦','(o˘◡˘o)','(っ˘ω˘ς)'], ['', '♪','♡','～']),
('party','庆祝', ['ヽ(✿ﾟ▽ﾟ)ノ','ヾ(≧▽≦*)o','٩(｡•́‿•̀｡)۶','(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧','(∩^o^)⊃━☆','✧*｡٩(ˊᗜˋ*)و✧*｡','ヽ(ﾟ∀ﾟ)ﾒ(ﾟ∀ﾟ)ﾉ','(ﾉ´ヮ`)ﾉ*: ･ﾟ'], ['', '☆','♪','♡']),
('action','动作', ['(╯°□°）╯︵ ┻━┻','┬─┬ ノ( ゜-゜ノ)','┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻','(ヘ･_･)ヘ┳━┳','(つ▀¯▀)つ','ᕕ( ᐛ )ᕗ','ε=ε=ε=┌(;*´Д`)ﾉ','ε≡≡ﾍ( ´Д`)ﾉ','(☞ﾟヮﾟ)☞','☜(ﾟヮﾟ☜)','( •_•)>⌐■-■','(ง •̀_•́)ง','( •_•)O*¯`·.¸.·´¯`°Q(•_• )','＿|￣|○','orz','(:з」∠)','_(:з」∠)_'], [''])
]

def single():
    return [(gid,name,[face+suffix for face in faces for suffix in suffixes]) for gid,name,faces,suffixes in SINGLE]

def display_width(text):
    return sum(0 if unicodedata.combining(c) else 2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in text)

def center(text, width):
    padding = width - display_width(text)
    return ' ' * (padding // 2) + text + ' ' * (padding - padding // 2)

def multiline():
    groups = []
    # 小幅文字画控制行数和宽度；相同动物使用多种独立表情，保留缩进。
    eyes = [('o','o'),('^','^'),('-','-'),('>','<'),('T','T'),('*','*'),('•','•'),('=','='),('◕','◕'),('♥','♥'),('¬','¬'),('x','x')]
    groups.append(('cats','猫咪', [f' /\\_/\\\n( {l}.{r} )\n > ^ <' for l,r in eyes] + [f'  /\\_/\\\n (= {l}ω{r} =)\n  /   づ♡' for l,r in eyes]))
    groups.append(('rabbits','兔子', [f' /) /)\n( {l}.{r})\n/ >♡' for l,r in eyes] + [f' (\\_/)\n ( {l}x{r} )\n /づ✿' for l,r in eyes]))
    groups.append(('bears','小熊', [f'  ʕ {l}ᴥ{r} ʔ\n  /  つ♡\n  しーＪ' for l,r in eyes] + [f'  ʕ {l}ᴥ{r} ʔ\n  /  つ旦\n  しーＪ' for l,r in eyes]))
    groups.append(('dogs','小狗', [f' / \\__\n(    @\\___\n /         O\n/   (_____/\n/_____/   U' , ' / \\__\n(    @\\___\n /         O\n/   (_____/\n/_____/  ﾉ'] + [f' /\\___/\\\n U {l}ᴥ{r} U\n /     \\\n(＿) (＿)' for l,r in eyes]))
    groups.append(('penguins','企鹅', [f'  /‾‾\\\n ( {l}Θ{r})\n /|   |\\\n  しＪ' for l,r in eyes]))
    groups.append(('owls','猫头鹰', [f' /\\___/\\\n( {l} v {r} )\n /|___|\\\n   ║ ║' for l,r in eyes]))
    groups.append(('fish','游鱼', ['  ><(((°>\n     ><(((°>\n ><(((°>', ' ><(((°>\n~~~~~~~~~~~~\n   ><(((°>', '  ><(((°>\n      ♡\n  <°)))><', '    |\\\n   /  \\\n< (°   ) ><\n   \\__/']))
    groups.append(('flowers','花与植物', ['    _\n  _/ \\_\n / \\_/ \\\n \\_/ \\_/\n    |\n  \\ | /\n   \\|/', '    ✿\n    |\n  \\ | /\n   \\|/\n  __|__\n  \\___/', '   _/\\_\n  /    \\\n  \\    /\n   \\/\\/\n     |\n   \\ | /\n    \\|/', '   /\\\n  /**\\\n /****\\\n/******\\\n   ||']))
    faces = ['(｡･ω･｡)','(＾▽＾)','(≧▽≦)','(•̀ᴗ•́)و','(๑•̀ㅂ•́)و','(˶ᵔ ᵕ ᵔ˶)','(｡•́︿•̀｡)','(╥﹏╥)','(￣▽￣)','(❁´◡`❁)','(๑´ڡ`๑)','(◕‿◕)']
    groups.append(('cheer','加油', [f'   {face}\n  ୧     ୨\n   しーＪ' for face in faces] + [f'  {face}\n  /つ つ\n  しーＪ\n   加油！' for face in faces[:6]]))
    groups.append(('hugs','抱抱', [f'  {face}\n /  づ♡\n しーＪ' for face in faces] + [f'  {face}\n ⊂     ⊃\n   しＪ' for face in faces]))
    groups.append(('magic','魔法', [f'  ∧＿∧\n {face}つ━☆・*。\n  と   ノ    ・゜+.\n   しーＪ' for face in faces]))
    groups.append(('tea','请喝茶', [f'  {face}\n  /つ旦\n  しーＪ' for face in faces]))
    groups.append(('greetings','问候', [f'┌──────────┐\n│ {center(word, 8)} │\n└──────────┘\n   {face}' for word,face in [('你好','(｡･ω･｡)ﾉ'),('早安','(＾▽＾)ﾉ'),('晚安','( ˘ω˘ )'),('欢迎','(≧▽≦)ﾉ'),('再见','( ´ ▽ ` )ﾉ'),('辛苦了','(｡•̀ᴗ-)✧'),('谢谢','(人´∀｀)'),('请多关照','m(_ _)m'),('周末快乐','(⌒▽⌒)'),('生日快乐','(✿◠‿◠)'),('节日快乐','(ﾉ◕ヮ◕)ﾉ'),('好久不见','(o´▽`o)')]]))
    groups.append(('messages','心情留言', [f'  /) /)\n (｡･ω･｡)\n┌─∪─∪─────┐\n│ {word}\n└─────────┘' for word in ['加油呀！','抱抱你～','今天也要开心','慢慢来就好','我在这里','记得休息','你已经很棒啦','一起努力吧','一切都会好的','谢谢你的陪伴','给你一朵小花','请收下我的心','好好吃饭','晚安好梦','祝你顺利','明天见！']]))
    groups.append(('scenes','生活小景', ['   .     *\n      .\n  *    ☾\n     .     *', '   .-~~-.\n .(      ).\n(___.__(___)\n  / / / /', '     |\n  \\  |  /\n -- ( ) --\n  /  |  \\\n     |', '     /\\\n    /  \\\n   /____\\\n   | [] |\n   | __ |\n   ||__||', '   ______\n  |      |\n  |______|\n    |  |\n   _|__|_', '   ( (\n    ) )\n  .----.\n  |    |]\n  \\____/', '    ,,,,\n   |||||\n  [=====]\n  | ♡ ♡ |\n  |_____|', '    /\\\n   /  \\\n  /____\\\n    ||\n    ||', '    |\\\n    | \\\n    |__\\\n ___|_____\n \\_______/\n ~~~~~~~~~', '   __   __\n  /  \\ /  \\\n  \\   V   /\n   \\     /\n    \\   /\n     \\_/']))
    return groups


def kaomoji():
    groups = collections.OrderedDict()
    for gid, name, values in single() + multiline():
        if name not in groups: groups[name] = (gid, [])
        groups[name][1].extend(values)
    # 同主题单行在前，多行在后；完整文本不修剪、不重新居中。
    return [(gid,name,sorted(values,key=lambda value: '\n' in value)) for name,(gid,values) in groups.items()]

def retire_official_packs():
    outcome = {}
    for pack, spec in json.loads(RETIRED_SOURCE.read_text()).items():
        directory = ROOT / 'emoticons' / pack
        if directory.is_symlink() or (directory.exists() and not directory.is_dir()):
            outcome[pack] = 'preserved-custom'
            continue
        if not directory.exists(): continue
        expected = spec['files']
        children = list(directory.iterdir())
        if directory.is_symlink() or {p.name for p in children} != set(expected) or any(
            p.is_symlink() or not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != expected[p.name]
            for p in children):
            outcome[pack] = 'preserved-custom'
            continue
        for p in children: p.unlink()
        directory.rmdir()
        outcome[pack] = 'retired-official'
    return outcome

def main():
    emoji_groups, statuses = emojis()
    result = {'unicode_version':'18.0', 'qualification':dict(statuses), 'emoji_source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              'common_source_sha256':hashlib.sha256(COMMON_SOURCE.read_bytes()).hexdigest(), 'packs':{}}
    result['packs']['default'] = write_pack('default','Emoji',emoji_groups,True)
    result['packs']['kaomoji'] = write_pack('kaomoji','颜文字',kaomoji())
    assert result['packs']['default']['items'] == sum(statuses.values())
    retire_official_packs()
    (ROOT/'tools/emoticon-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
