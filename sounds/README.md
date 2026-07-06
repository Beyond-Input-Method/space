# 键盘音效配置指南

## 音效文件结构

`sounds/` 下每个子目录是**一套音效主题**，目录名就是 `space.yaml` 里 `sound_effect` 字段引用的名字。
当前仓库内置 5 套主题：

```text
space/sounds/
├── default/          # 默认音效（仅 default.wav + 备用 default2.wav）
│   ├── default.wav
│   ├── default2.wav
│   └── info.yaml
├── default2/         # 另一套默认风格
│   ├── default.wav
│   ├── backspace.wav
│   ├── return.wav
│   ├── space.wav
│   └── info.yaml
├── 叮叮/
├── 地下工作者/
└── 木鱼/
    ├── default.wav
    ├── backspace.wav
    ├── return.wav
    ├── space.wav
    └── info.yaml
```

每套主题目录里通常包含：

- 若干 `.wav` 音效文件（见下方命名规则）；
- 一个 `info.yaml`，描述这套音效的名片信息（`name`、`author`、`version`、`url`、`description` 等）。

## 音效文件命名规则

1. 所有音效文件使用小写字母命名，扩展名为 `.wav`。
2. 文件名对应**按键类型**。当前内置主题实际使用的是以下四个：

   - 默认按键：`default.wav`
   - 空格键：`space.wav`
   - 回车键：`return.wav`
   - 退格键：`backspace.wav`

   （`default/` 主题额外提供一个 `default2.wav` 作为备用默认音。）

## 默认音效

按键播放时，系统会先查找与该按键类型对应的 `.wav`；如果某个按键没有对应文件，就回退播放 `default.wav`。因此**每套主题都应至少包含 `default.wav`**。

## 新增音效主题

1. 在 `sounds/` 下创建新的主题文件夹（目录名将作为 `sound_effect` 的取值）。
2. 放入至少 `default.wav`，按需再加 `space.wav` / `return.wav` / `backspace.wav`。
3. 添加一个 `info.yaml` 描述这套主题。
4. 在 `space.yaml` 里把 `sound_effect` 改成你的目录名即可启用。

## 注意事项
1. 所有音效文件必须是WAV格式
2. 建议使用短促的音效以获得最佳体验
3. 音效文件大小建议控制在100KB以内
4. 确保音效文件的采样率和位深度适中，以平衡音质和性能

## 音效文件获取
您可以：
1. 使用音频编辑软件制作自己的音效
2. 从开源音效库下载合适的音效
3. 购买商业音效包

请确保您使用的音效拥有合适的使用许可。