# 键盘音效配置指南

## 音效文件结构
键盘音效文件需要按照以下结构放置： 
space/sounds/
├── default/ # 默认音效目录
│ ├── default.wav # 默认按键音效
│ ├── a.wav # 字母A的音效
│ ├── b.wav # 字母B的音效
│ └── ... # 其他按键音效
└── other_theme/ # 其他音效主题目录
├── default.wav
└── ...

## 音效文件命名规则

1. 所有音效文件必须使用小写字母命名，扩展名为`.wav`
2. 文件名对应键码的名称，可参考以下对照表:

### 常用按键音效文件名
- 字母键: `a.wav` 到 `z.wav`
- 数字键: `0.wav` 到 `9.wav` 
- 特殊符号:
  - 空格键: `space.wav`
  - 回车键: `return.wav`
  - 退格键: `backspace.wav`
  - 标点符号: 
    - 逗号: `comma.wav`
    - 句号: `period.wav`
    - 问号: `question.wav`
    - 感叹号: `exclam.wav`
    
### 功能键音效
- `tab.wav`: Tab键
- `caps_lock.wav`: 大写锁定键
- `shift_l.wav`: 左Shift键
- `shift_r.wav`: 右Shift键
- `control_l.wav`: 左Ctrl键
- `control_r.wav`: 右Ctrl键
- `alt_l.wav`: 左Alt键
- `alt_r.wav`: 右Alt键

## 默认音效
如果某个按键没有对应的音效文件，系统会播放`default.wav`作为默认音效。建议始终在音效目录中包含`default.wav`文件。

## 音效主题
1. 在`sounds`目录下创建新的主题文件夹
2. 将音效文件放入主题文件夹中
3. 主题文件夹中的音效文件命名规则与默认主题相同

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