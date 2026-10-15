# 正式表情资源维护

默认仅部署三个表情目录：

| 目录 | 名称 | 分类 | 去重后条目 |
| --- | --- | --- | --- |
| default | Emoji | 10 | 3972 |
| kaomoji | 单行颜文字 | 23 | 1074 |
| multiline-kaomoji | 多行颜文字 | 15 | 222 |

Emoji 来源为 Unicode Emoji 18.0 官方清单的固定快照，包含 3963 条 fully-qualified 和 9 条 component；这是文件说明定义的完整 RGI 集合。不重复纳入缺失变体选择符的 minimally-qualified/unqualified 表示。肤色、性别、职业、家庭、ZWJ 及旗帜序列按原始码点保留。使用官方 CLDR 分组顺序，仅翻译分类名称。最新字符的实际字形取决于系统字体支持。

- 官方数据：[emoji-test.txt](https://www.unicode.org/Public/18.0.0/emoji/emoji-test.txt)
- 来源目录说明：[ReadMe](https://www.unicode.org/Public/emoji/latest/ReadMe.txt)
- 固定快照：`tools/data/emoji-test-18.0.txt`
- 数据授权：`tools/data/UNICODE-LICENSE.txt`（Unicode License v3）
- 快照和生成配置的 SHA-256、版本及数量见 `tools/emoticon-manifest.json`。

颜文字核心和文字画在生成器中按情境维护，组合与其情境匹配的手势；同包按完整字符串去重。单行不包含换行，多行保留空格、缩进及换行，不添加测试编号或说明占位条目。修改时优先维护生成器，避免下次生成丢失编辑。

```bash
python3 tools/generate_emoticons.py
python3 tools/test_emoticons.py
```

脚本只更新这三个包，不自动下载外部数据，不删除其他目录。更新 Unicode 版本时显式替换快照、核对授权及状态、修改版本与路径后重新生成。文件内容用 JSON 字符串形式写入 YAML，避免特殊字符、冒号、引号及反斜杠被 YAML 误解析；无需第三方 Python 依赖。

媒体能力仍由输入法支持，正式预置包本期不包含图片、GIF 样例或压测资源；可自行创建独立媒体目录。
