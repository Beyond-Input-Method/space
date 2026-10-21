# 速成26键主题

在主题列表选择「速成26键」并部署即可使用，不需要在补丁管理中启用。

`theme.yaml` 继承同级 `default/theme.yaml`（标准中文26键），通过 `key_labels.yaml` 中的补丁覆盖中文 `default`、`default_sm_md` 布局的52处主键符。点击编码、长按、滑动、副键符、英文和数字键盘均沿用标准主题。切换回「标准中文26键」即可恢复字母显示。

字根沿用现有 `rime-quick/quick5.schema.yaml`，包括 X→難、Z→符：

```text
Q 手  W 田  E 水  R 口  T 廿  Y 卜  U 山  I 戈  O 人  P 心
A 日  S 尸  D 木  F 火  G 土  H 竹  J 十  K 大  L 中
Z 符  X 難  C 金  V 女  B 月  N 弓  M 一
```

推荐与速成（quick5）方案搭配。主题不会切换输入方案，不会自动启用。

资源源目录为单仓 `resources/space/themes/quick`，鸿蒙工程的 `products/phone/src/main/resources/resfile/space/themes/quick` 是打包副本。后续修改源目录，通过现有 `scripts/build_themes.sh --no-schemas quick` 编译，再部署资源。不要只修改打包副本。

本主题依赖同级 default/public 资源，无需复制整套标准主题。若标准主题修改按键顺序或新增中文布局，需同步核对 `key_labels.yaml` 的索引。

旧版 `patches/quick_key_labels` 已移除。已启用过旧版补丁的设备，应先取消旧补丁并重新部署原主题，再选择本主题；覆盖安装不会主动清理用户数据中的旧补丁。
