# Patch 编写教程

## 什么是 Patch？

Patch（补丁）是一种用于修改和扩展输入法配置的方式。通过编写 patch 文件，你可以：
- 为输入法方案添加新功能
- 修改现有配置
- 添加自定义词库
- 调整输入法行为

## 目录结构

每个 patch 都位于 `patches` 目录下的独立文件夹中，基本结构如下：

```
patches/
├── your_patch_name/          # 你的补丁文件夹
│   ├── info.yaml            # 补丁信息文件（必需）
│   ├── patch.yaml           # 补丁配置文件（必需）
│   └── res/                 # 资源文件夹（可选）
│       └── your_files...    # 你的资源文件
```

## 1. 创建补丁信息文件 (info.yaml)

首先创建 `info.yaml` 文件，包含补丁的基本信息：

```yaml
author: "你的名字"                    # 作者
create_time: "2024-01-01"           # 创建时间
name: "补丁名称"                     # 补丁显示名称
update_time: "2024-01-01"           # 更新时间
url: ""                             # 相关链接（可选）
version: 1.0.0                      # 版本号
# 支持的输入法方案（可选）
support_schemas:
  - "bim-t9"
  - "bim-t14"
  - "rime-ice-18"
```

## 2. 编写补丁配置文件 (patch.yaml)

### 基本结构

```yaml
# 补丁标题和说明
# 注意：变量返回绝对路径，可以直接使用

# 指定要打补丁的目标文件
patch_to_file: "{$current_schema}"

# 补丁配置
patch:
  - title: "补丁标题"
    key: "unique_key"              # 唯一标识符
    description: "补丁描述"
    patch_to: "{$current_schema}"  # 补丁目标文件（可选，默认使用patch_to_file）
    resources:                     # 资源文件（可选）
      - source: "res/your_file.db"
        target: "{$current_schema_dir}/your_file.db"
    patch:                         # 实际的补丁配置
      # 你的配置内容
```

### 新增字段说明

#### `patch_to` 字段
- **作用**：为单个补丁指定目标文件，优先级高于全局的 `patch_to_file`
- **用法**：如果设置了 `patch_to`，该补丁将应用到指定的文件而不是全局目标文件
- **示例**：
  ```yaml
  patch:
    - title: "方案补丁"
      key: "schema_patch"
      patch_to: "{$current_schema}"  # 应用到方案文件
      patch: { ... }
    - title: "主题补丁"
      key: "theme_patch"
      patch_to: "{$current_theme}"   # 应用到主题文件
      patch: { ... }
  ```

### 目录变量

系统提供了以下变量，**所有变量都返回绝对路径**，可以直接使用：

#### 方案相关变量
- `{$current_schema_dir}` - 当前选择的方案目录（绝对路径）
  - 例如：`/xx/space/schemas/bim-t9`
- `{$current_schema}` - 当前选择的方案文件（绝对路径）
  - 例如：`/xx/space/schemas/bim-t9/bim-t9.schema.yaml`

#### 主题相关变量
- `{$current_theme_dir}` - 当前选择的主题目录（绝对路径）
  - 例如：`/xx/space/themes/default`
- `{$current_theme}` - 当前选择的主题文件（绝对路径）
  - 例如：`/xx/space/themes/default/theme.yaml`

#### 音效相关变量
- `{$current_sound_dir}` - 当前选择的音效目录（绝对路径）
  - 例如：`/xx/space/sounds/default`
- `{$current_sound}` - 当前选择的音效文件（绝对路径）
  - 例如：`/xx/space/sounds/default/sound.yaml`

#### 触感相关变量
- `{$current_haptic_dir}` - 当前选择的触感目录（绝对路径）
  - 例如：`/xx/space/haptics/default`
- `{$current_haptic}` - 当前选择的触感文件（绝对路径）
  - 例如：`/xx/space/haptics/default/haptic.yaml`

#### 字体相关变量
- `{$current_font_dir}` - 当前选择的字体目录（绝对路径）
  - 例如：`/xx/space/fonts/default`
- `{$current_font}` - 当前选择的字体文件（绝对路径）
  - 例如：`/xx/space/fonts/default/font.yaml`

### 补丁目标文件

你可以给不同的文件打补丁：

```yaml
# 给方案文件打补丁
patch_to_file: "{$current_schema}"

# 给主题文件打补丁
patch_to_file: "{$current_theme}"

# 给音效文件打补丁
patch_to_file: "{$current_sound}"
```

## 3. 常见补丁类型和示例

### 示例1：添加模糊拼音支持

```yaml
patch:
  - title: "ch = c"
    key: "ch_equals_c"
    description: "ch 和 c 音互通"
    patch:
      "speller/algebra/+":
        - "derive/ch/c/"
        - "derive/c/ch/"
```

### 示例2：添加联想功能

```yaml
patch_to_file: "{$current_schema}"
patch:
  - title: "联想"
    key: "predict"
    description: "给方案添加联想功能"
    resources:
      - source: "res/predict.db"
        target: "{$current_schema_dir}/predict.db"
    patch:
      "engine/processors/@before 0": "predictor"
      "engine/translators/@before 0": "predict_translator"
      "switches/+":
        - name: prediction
          states: [關閉預測, 開啓預測]
          reset: 1
      "predictor":
        db: predict.db
        max_candidates: 5
        max_iterations: 1
```

### 示例3：添加自定义开关

```yaml
patch:
  - title: "自定义开关"
    key: "custom_switch"
    description: "添加一个自定义开关"
    patch:
      "switches/+":
        - name: my_custom_switch
          states: [关闭, 开启]
          reset: 0
```

### 示例4：修改引擎配置

```yaml
patch:
  - title: "引擎优化"
    key: "engine_optimization"
    description: "优化引擎性能"
    patch:
      "engine/translators/@before 0": "my_translator"
      "my_translator":
        dictionary: my_dict
        enable_completion: true
```

## 4. 补丁语法说明

### 路径操作符

- `+` - 添加新项目到列表
- `-` - 从列表中移除项目
- `@before N` - 在指定位置前插入
- `@after N` - 在指定位置后插入

### 示例

```yaml
# 添加新的处理器
"engine/processors/@before 0": "new_processor"

# 添加新的开关
"switches/+":
  - name: new_switch
    states: [关闭, 开启]

# 修改现有配置
"translator/dictionary": "new_dict"
```

## 5. 资源文件管理

如果你的补丁需要额外的文件（如词库、数据库等），可以放在 `res/` 目录下：

```
your_patch/
├── info.yaml
├── patch.yaml
└── res/
    ├── custom_dict.txt
    ├── predict.db
    └── other_files...
```

然后在 `patch.yaml` 中通过 `resources` 复制到目标位置：

```yaml
resources:
  - source: "res/custom_dict.txt"
    target: "{$current_schema_dir}/custom_dict.txt"
  - source: "res/predict.db"
    target: "{$current_schema_dir}/predict.db"
```

## 6. 测试和调试

### 测试步骤

1. **PC端测试**：先在PC上测试你的补丁配置
2. **语法检查**：确保YAML语法正确
3. **功能验证**：测试补丁功能是否正常工作

### 常见错误

- YAML语法错误（缩进、引号等）
- 路径错误（相对路径不正确）
- 键值重复或冲突
- 资源文件路径错误

## 7. 最佳实践

1. **命名规范**：使用有意义的文件夹和键名
2. **版本管理**：及时更新版本号
3. **文档完善**：提供清晰的描述和说明
4. **兼容性**：在 `info.yaml` 中声明支持的方案
5. **测试充分**：确保补丁在各种情况下都能正常工作

## 8. 完整示例

创建一个名为 `my_custom_patch` 的补丁：

### info.yaml
```yaml
author: "张三"
create_time: "2024-01-01"
name: "我的自定义补丁"
update_time: "2024-01-01"
url: ""
version: 1.0.0
support_schemas:
  - "bim-t9"
  - "bim-t14"
```

### patch.yaml
```yaml
# 我的自定义补丁

patch_to_file: "{$current_schema}"
patch:
  - title: "模糊拼音支持"
    key: "fuzzy_pinyin"
    description: "添加常用模糊拼音规则"
    patch:
      "speller/algebra/+":
        - "derive/ch/c/"
        - "derive/c/ch/"
        - "derive/sh/s/"
        - "derive/s/sh/"
        - "derive/zh/z/"
        - "derive/z/zh/"
  
  - title: "自定义开关"
    key: "custom_switch"
    description: "添加一个自定义功能开关"
    patch:
      "switches/+":
        - name: my_feature
          states: [关闭, 开启]
          reset: 0
```

## 9. 绝对路径的优势

使用绝对路径变量有以下优势：

### 🎯 **简化配置**
- 不需要手动拼接路径
- 减少路径错误
- 配置更清晰易读

### 🔧 **自动适配**
- 自动适应不同的安装路径
- 支持多用户环境
- 跨平台兼容

### 📝 **示例对比**

**旧方式（相对路径）：**
```yaml
patch_to_file: "schemas/{$current_schema_dir}/{$current_schema}"
resources:
  - source: "res/predict.db"
    target: "schemas/{$current_schema_dir}/predict.db"
```

**新方式（绝对路径）：**
```yaml
patch_to_file: "{$current_schema}"
resources:
  - source: "res/predict.db"
    target: "{$current_schema_dir}/predict.db"
```

## 10. Patch 管理系统

### 激活和取消激活

Patch 系统提供了完整的激活和取消激活功能：

#### 激活补丁
```cpp
// 激活指定key的补丁
patchManager.activate("your_patch_key", variable);
```

激活过程包括：
1. **智能合并**：将补丁内容合并到对应的 `.custom.yaml` 文件中
2. **资源复制**：复制 `resources` 中指定的文件到目标位置
3. **状态更新**：自动更新补丁的 `toggle_` 状态

#### 取消激活补丁
```cpp
// 取消激活指定key的补丁
patchManager.deactivate("your_patch_key", variable);
```

取消激活过程包括：
1. **智能移除**：从 `.custom.yaml` 文件中移除对应的补丁内容
2. **资源清理**：删除之前复制的资源文件
3. **状态更新**：自动更新补丁的 `toggle_` 状态

### 智能合并和移除

系统提供了智能的合并和移除算法：

#### 字典类型合并
- 如果键已存在，递归合并值
- 如果键不存在，直接添加
- 支持嵌套字典的深度合并

#### 数组类型合并
- 如果元素已存在，用新值覆盖
- 如果元素不存在，添加到数组末尾
- 保持数组的完整性

#### 智能移除
- 精确移除匹配的元素
- 如果移除后容器为空，删除整个键
- 支持嵌套结构的递归移除

### Toggle 状态检查

系统会自动检查每个补丁的激活状态：

#### 检查逻辑
1. **字典类型**：检查补丁的所有键值对是否都在 `.custom.yaml` 中
2. **数组类型**：检查数组元素是否完全匹配
3. **其他类型**：直接比较值是否相等

#### 状态更新
- `toggle_ = true`：补丁已激活
- `toggle_ = false`：补丁未激活

### Custom.yaml 文件处理

系统会自动处理 `.custom.yaml` 文件：

#### 路径转换
- `xxx.schema.yaml` → `xxx.custom.yaml`
- `theme.yaml` → `theme.custom.yaml`
- `sound.yaml` → `sound.custom.yaml`

#### 文件操作
- 自动创建目录结构
- 智能合并现有内容
- 保持YAML格式的完整性

## 11. 系统架构和实现细节

### 核心组件

#### PatchFileManager
- **职责**：管理补丁文件的加载、激活、取消激活
- **主要方法**：
  - `load(path)`：加载补丁文件
  - `activate(key, variable)`：激活指定补丁
  - `deactivate(key, variable)`：取消激活指定补丁
  - `getPatches()`：获取所有补丁列表

#### 智能算法
- **`isValueContained`**：检查容器是否包含目标值
- **`smartMergeValues`**：智能合并两个Value对象
- **`smartRemoveValues`**：智能移除Value对象

#### 路径处理
- **`resolveVariables`**：解析路径中的变量
- **`convertToCustomYamlPath`**：转换为custom.yaml路径

### 数据流程

#### 激活流程
1. 解析 `patch_to` 路径变量
2. 转换为对应的 `.custom.yaml` 路径
3. 读取现有的custom patch
4. 智能合并新patch和现有patch
5. 写入合并后的结果到 `.custom.yaml`
6. 复制资源文件到目标位置
7. 更新toggle状态

#### 取消激活流程
1. 解析 `patch_to` 路径变量
2. 转换为对应的 `.custom.yaml` 路径
3. 读取现有的custom patch
4. 智能移除当前patch
5. 写入移除后的结果到 `.custom.yaml`
6. 删除之前复制的资源文件
7. 更新toggle状态

### 错误处理

系统提供了完善的错误处理机制：
- 文件不存在时的优雅降级
- YAML解析错误的详细日志
- 路径解析失败的回退处理
- 资源文件操作的异常捕获

## 12. 添加控件UI配置

### 为什么需要控件UI？

控件UI让用户可以通过友好的图形界面调整补丁参数，而不需要手动编辑YAML文件。这大大提升了用户体验。

### 控件配置结构

在 `patch.yaml` 中添加 `controls` 部分：

```yaml
controls:
  stringsTable: "Root"              # 字符串表名称
  preferences:                      # 控件列表
    - type: group                   # 分组标题
      title: 设置分组
      footer_text: 分组说明文字
    
    - type: toggle_switch           # 开关控件
      title: 功能开关
      key: feature_enabled          # 控件键名(用于变量绑定)
      default_value: false
      toggle_style: switch          # switch 或 checkmark
    
    - type: slider                  # 滑块控件
      title: 数值设置
      key: value_setting
      default_value: 10
      minimum_value: 1
      maximum_value: 20
      step: 1
```

### 支持的控件类型

#### 1. 分组标题 (group)
用于将相关设置归类显示：
```yaml
- type: group
  title: 分组标题
  footer_text: 分组说明文字(可选)
```

#### 2. 开关控件 (toggle_switch)
用于开启或关闭功能：
```yaml
- type: toggle_switch
  title: 功能名称
  key: feature_key              # 必需：唯一标识
  default_value: false          # 必需：默认值
  toggle_style: switch          # 可选：switch(滑动开关) 或 checkmark(勾选框)
```

#### 3. 滑块控件 (slider)
用于选择数值范围：
```yaml
- type: slider
  title: 参数名称
  key: param_key                # 必需：唯一标识
  default_value: 10             # 必需：默认值
  minimum_value: 1              # 必需：最小值
  maximum_value: 20             # 必需：最大值
  step: 1                       # 必需：步长
```

#### 4. 文本输入 (text_field)
用于输入文本内容：
```yaml
- type: text_field
  title: 文本设置
  key: text_key
  default_value: "默认文本"
  placeholder: "请输入内容"    # 可选：占位符
```

#### 5. 多值选择 (multi_value)
用于从多个选项中选择：
```yaml
- type: multi_value
  title: 选项设置
  key: option_key
  default_value: "option1"
  values:                       # 可选值列表
    - "option1"
    - "option2"
    - "option3"
  titles:                       # 对应的显示标题
    - "选项一"
    - "选项二"
    - "选项三"
```

### 变量绑定

在 `patch` 配置中使用 `{$key}` 来引用控件的值：

```yaml
patch:
  - title: "功能补丁"
    key: "feature_patch"
    bind_control: "feature_enabled"    # 绑定主开关
    patch:
      some_config: "{$value_setting}"  # 使用滑块的值
      another_config: "{$text_key}"    # 使用文本输入的值
```

### 完整示例：语言模型补丁

```yaml
patch_to: "{$current_schema}"
patch:
  - title: "语言模型"
    key: "turn_on_grammar"
    bind_control: "turn_on_grammar"
    patch:
      grammar:
        collocation_max_length: "{$collocation_max_length}"
        collocation_penalty: "{$collocation_penalty}"

controls:
  stringsTable: "Root"
  preferences:
    # 基本开关
    - type: group
      title: 基本设置
    
    - type: toggle_switch
      title: 启用语言模型
      key: turn_on_grammar
      default_value: false
      toggle_style: switch
    
    # 参数调整
    - type: group
      title: 词组长度配置
    
    - type: slider
      title: 最长词组长度
      key: collocation_max_length
      default_value: 8
      minimum_value: 2
      maximum_value: 15
      step: 1
    
    - type: slider
      title: 常见搭配惩罚
      key: collocation_penalty
      default_value: -6
      minimum_value: -30
      maximum_value: 0
      step: 1
```

### 最佳实践

1. **合理分组**：使用 group 将相关设置归类，提升界面清晰度
2. **清晰命名**：title 使用易懂的中文描述，key 使用英文标识
3. **合理默认值**：设置合适的默认值，让大多数用户无需调整
4. **添加说明**：使用 footer_text 解释设置的作用和影响
5. **控制范围**：为滑块设置合理的最小值、最大值和步长
6. **主开关绑定**：使用 bind_control 将补丁与主开关关联

### 控件UI的优势

- ✅ **用户友好**：图形界面比编辑YAML文件更直观
- ✅ **防止错误**：控件限制输入范围，避免配置错误
- ✅ **实时预览**：修改后立即生效，方便调试
- ✅ **降低门槛**：普通用户也能轻松使用高级功能

## 总结

编写 patch 的关键点：
1. 理解YAML语法和缩进规则
2. 熟悉输入法配置结构
3. 正确使用绝对路径变量
4. 充分测试补丁功能
5. 遵循命名和文档规范
6. 了解智能合并和移除机制
7. 掌握toggle状态检查原理
8. **善用控件UI提升用户体验**

通过这个教程，你应该能够创建自己的输入法补丁了。如果遇到问题，可以参考现有的补丁示例或寻求帮助。
