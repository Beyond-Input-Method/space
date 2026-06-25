# 自定义字体导入指南

本文档说明如何在本项目中导入并启用自定义字体资源。

## 1. 目录位置

字体资源根目录：

`/space/fonts/`

每个字体建议放在独立子目录中，例如：

```text
/space/fonts/
  ├── default/                       # 系统默认字体（仅 info.yaml，无字体文件，走系统字体）
  │   └── info.yaml
  ├── jf-openhuninn-2.1/             # 仓库当前内置的字体示例
  │   ├── info.yaml
  │   └── jf-openhuninn-2.1.ttf
  └── your-font/                     # 你新增的字体
      ├── info.yaml
      └── your-font.ttf
```

> 当前仓库内置两套字体：`default/`（系统字体，无字体文件）与 `jf-openhuninn-2.1/`（justfont 粉圆，`.ttf`）。

## 2. 快速导入步骤

1. 在 `space/fonts/` 下新建字体目录（目录名建议英文、唯一）。
2. 将字体文件拷贝到该目录（当前支持：`.ttf`、`.otf`、`.ttc`）。
3. 在同目录新增或编辑 `info.yaml`（见下方模板）。
4. 重新构建并安装应用。
5. 在 Host App 或 IME 设置中进入“字体”列表，选择新字体。

## 3. info.yaml 配置模板

可参考 `/space/fonts/jf-openhuninn-2.1/info.yaml`。

```yaml
id: your-font-id
name: 你的字体名称
author: 作者名
version: 1.0.0
createTime: 2026-04-15
updateTime: 2026-04-15
description: 字体描述
url: https://example.com/font-home
```

### 字段说明（建议）

- `id`: 字体唯一标识，建议与目录名一致。
- `name`: UI 展示名称（用户在字体列表看到的名称）。

## 4. 默认字体配置（可选）

在 `/space/space.yaml` 中，通过以下字段配置默认字体：

```yaml
font: default
font_dir: fonts/
```

说明：

- `font`: 默认字体目录名（例如 `default` 或 `jf-openhuninn-2.1`）。
- `font_dir`: 字体根目录（通常为 `fonts/`）。

如果不修改，系统会使用当前默认值；你也可以通过应用内“字体”列表动态切换。

## 5. 生效方式说明（重要）

字体选择成功后，界面会提示：

- 新字体需要“重启输入法”后生效；
- 操作方式：先切换到其他输入法，再切回本输入法。

提示框支持“仅提示这一次”。

## 6. 常见问题

### Q1：字体在列表中不显示

- 检查字体目录是否位于 `/space/fonts/` 下。
- 检查 `info.yaml` 是否存在且格式正确（YAML 缩进不能错）。
- 检查字体文件扩展名是否为 `.ttf/.otf/.ttc`。

### Q2：选择字体后没变化

- 请按提示重启输入法（切到其他输入法再切回）。
- 确认该字体文件可正常读取且未损坏。

### Q3：同目录有多个字体文件

- 当前建议每个字体目录仅放一个主字体文件，避免实际加载与预期不一致。

---

如需新增多字重/多样式字体，可在 `files` 中继续追加条目，并保持文件名与实际资源一致。
