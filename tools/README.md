# 正式表情资源维护

默认部署两个表情目录：

| 目录 | 名称 | 分类数 | 唯一内容 | 显示条目 |
| --- | --- | --- | --- | --- |
| default | Emoji | 21 个正式分类＋常用 | 3972 | 4036 |
| kaomoji | 颜文字 | 32 个主题 | 1296 | 1296 |

## Emoji 与分类

固定使用 Unicode Emoji 18.0 官方清单，包含 3963 条 fully-qualified 和 9 条 component；完整集合仍为 3972。肤色、性别、职业、家庭、ZWJ、旗帜按原始完整码点序列保留，不纳入重复的 minimally-qualified/unqualified 表示。实际字形取决于设备字体。

按照官方 group/subgroup 映射为单独主题：笑脸、情感、手势、身体、人物、肤色、发型、动物、植物、食物、饮品、餐具、地点、交通、时间、天气、活动、运动、物品、符号、旗帜。每条 Emoji 只属于一个正式分类；分类内保留 Unicode 顺序。

- 官方数据：https://www.unicode.org/Public/18.0.0/emoji/emoji-test.txt
- 固定快照：`tools/data/emoji-test-18.0.txt`
- 数据授权：`tools/data/UNICODE-LICENSE.txt`

## 常用

`tools/data/emoji-common.json` 维护 64 条默认快捷内容，固定放在正式分类之前。最近使用由应用生成并固定最左侧，两者相互独立。常用条目仍保留在原正式分类中，因此显示条目为 3972＋64＝4036，但唯一内容依然是 3972。

依据为 Unicode 公开的 **2019 年历史总体使用频率** 与中文聊天场景人工整理。前者不是实时排名，也不能代表中文或任何特定平台；后者明确标记为编辑整理，不称为大模型内部输入统计。每条都记录 `basis`，来源及年份也随清单维护。

公开资料：https://home.unicode.org/emoji/emoji-frequency/

生成器强制常用条目全部属于完整官方集合且无重复，不会因先生成常用而从正式分类移除内容。

## 颜文字合并

1074 条单行和 222 条多行合为 1296 条，名称为“颜文字”。问候、加油、抱抱、猫咪、小熊、兔子等同名主题合并，最终 32 类。同主题先排列单行，再排列多行；按完整字符串去重，不修剪空格、缩进或换行。运行时三个平台均按条目实际换行数布局，所有条目仍是 text，不修改 type 原有含义。

## 生成与验证

```bash
python3 tools/generate_emoticons.py
python3 tools/test_emoticons.py
```

生成不下载外部数据，只更新 default/kaomoji。快照、常用清单及结果哈希和数量见 `tools/emoticon-manifest.json`；`items` 表示唯一内容，`display_entries` 包含常用快捷重复项。

原生读取可用 `tools/test_emoticon_reader.cpp` 与共享 bimkit 的 `src/theme/emoticon_pack.cpp`、yaml-cpp 编译，然后传本资源仓根路径运行。验证两个包、常用引用、唯一 ID、完整字符和单行/多行混排均可正常解析。

## 旧包保护与部署边界

`tools/data/retired-emoticon-packs.json` 记录旧官方 multiline-kaomoji 的每个文件 SHA-256 和替代目录 kaomoji。**源资源生成器**只有在目录全部文件、哈希均匹配且无符号链接时才移除旧目录；包含改动、额外文件或链接则保留。

这不是客户端自动迁移：既有用户目录中若留有旧包，单纯更新 bundle 不会自动删除它。部署方应按相同官方指纹规则迁移，并先备份；不能删改用户自定义包，也不能用清空整个 space、词库或剪贴板的方式更新表情。用户修改的旧包保留为独立用户包是预期行为。最近历史按完整文本保存，合并后仍能在颜文字中匹配。

所有修改都维护此源仓，再经既有资源预处理脚本部署，不直接编辑应用工程的生成副本。正式包不包含媒体样例或压测数据。
