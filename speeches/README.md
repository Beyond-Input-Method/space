# speeches 目录配置教程

这份教程是写给**不懂代码的同学**看的。

你可以把 `resources/space/speeches` 理解成一个“语音方案资料夹”。
每一个子文件夹，代表一种语音服务。
比如：

- `default`：系统默认语音
- `volcengine`：豆包语音

如果你要新增一种语音服务，或者修改某个语音服务在页面上的显示方式，通常就是改这里面的配置文件。

---

## 一、这个目录是做什么的

`resources/space/speeches` 目录下，每个语音服务都会有一个自己的文件夹。

例如：

```text
resources/space/speeches/
├── default/
│   └── info.yaml
└── volcengine/
    └── info.yaml
```

你可以把它理解成：

- 文件夹名 = 这个语音服务的内部名字
- `info.yaml` = 这个语音服务的说明卡片

程序会读取 `info.yaml`，然后决定：

- 页面上显示什么名字
- 显示什么介绍
- 需不需要用户先配置 key
- 缺少 key 时弹窗显示什么按钮
- “去申请”按钮跳到哪个网址
- “配置 key”按钮跳到哪个补丁设置页

---

## 二、最常改的是哪个文件

通常你只需要改这个文件：

```text
某个语音目录/info.yaml
```

例如：

```text
resources/space/speeches/volcengine/info.yaml
```

如果你是要新增一个语音服务，一般做法是：

1. 先复制一个已有的语音目录
2. 改文件夹名字
3. 再修改里面的 `info.yaml`

---

## 三、info.yaml 是什么

`info.yaml` 可以理解成一张“配置表”。

它长这样：

```yaml
name: 豆包语音
description: 豆包同款在线语音识别
version: 1.0
create_date: 2025-11-19
patch_dir_name: _speech_volcengine
apply_url: https://www.volcengine.com/
cancel_button_text: 稍后再说
apply_button_text: 去官网申请
config_button_text: 立即配置
required_keys: [accessKey, appKey]
```

你不需要会编程，只要把它理解成：

- 左边是“项目名”
- 右边是“填写的内容”

例如：

- `name: 豆包语音`
  - 意思是：页面上显示的名字叫“豆包语音”

---

## 四、每个字段是什么意思

下面我用最容易懂的方式解释。

### 1. `name`

作用：语音服务显示给用户看的名字。

示例：

```yaml
name: 豆包语音
```

通俗理解：

- 用户在页面上看到的标题

---

### 2. `description`

作用：语音服务的说明文字。

示例：

```yaml
description: 豆包同款在线语音识别
```

通俗理解：

- 给用户看的简介
- 可以写一句短说明

---

### 3. `version`

作用：版本号。

示例：

```yaml
version: 1.0
```

通俗理解：

- 这是这个配置的版本
- 一般保持 `1.0` 就可以
- 如果以后做了很大调整，可以改成 `1.1`、`2.0`

---

### 4. `create_date`

作用：创建日期。

示例：

```yaml
create_date: 2025-11-19
```

通俗理解：

- 记录这个配置是什么时候建的
- 格式建议固定写成：`年-月-日`
- 例如：`2026-03-17`

---

### 5. `patch_dir_name`

作用：告诉程序，“去配置 key”按钮应该跳到哪个配置页面。

示例：

```yaml
patch_dir_name: _speech_volcengine
```

通俗理解：

- 用户缺少 key 时，点“配置 key”
- 程序会根据这个名字，跳到对应的补丁设置页

你可以把它理解成“跳转目标的代号”。

注意：

- 这个值不是随便写的
- 必须和项目里已经存在的补丁目录对应上
- 如果写错了，用户点“配置 key”时可能会打不开正确页面

如果你不确定这个值，**不要自己猜**，最好找开发同学确认。

---

### 6. `required_keys`

作用：告诉程序，这个语音服务必须先配置哪些 key，才能正常使用。

示例：

```yaml
required_keys: [accessKey, appKey]
```

通俗理解：

- 这像是一张“必填项清单”
- 如果这些项目没填，程序就会拦住用户，并弹出提示框

例如上面这行的意思是：

- 这个语音服务必须配置：
  - `accessKey`
  - `appKey`

如果用户没填，就不能直接切换使用。

注意：

- 方括号 `[]` 不能丢
- 多个 key 之间用英文逗号分开

正确写法：

```yaml
required_keys: [accessKey, appKey]
```

错误写法：

```yaml
required_keys: accessKey, appKey
```

---

### 7. `apply_url`

作用：告诉程序，“去申请”按钮要打开哪个网站。

示例：

```yaml
apply_url: https://www.volcengine.com/
```

通俗理解：

- 如果用户缺少 key
- 弹窗里会显示一个“去申请”按钮
- 点了以后，会打开这里填写的网址

如果你**不想显示“去申请”按钮**，可以不写这个字段。

也就是说：

- 写了 `apply_url`：会显示“去申请”
- 不写 `apply_url`：不会显示“去申请”

---

### 8. `cancel_button_text`

作用：配置弹窗里“取消按钮”的文字。

示例：

```yaml
cancel_button_text: 稍后再说
```

通俗理解：

- 你可以把默认的“取消”改成更口语化的话

如果不写，系统默认会显示：

```text
取消
```

---

### 9. `apply_button_text`

作用：配置弹窗里“去申请按钮”的文字。

示例：

```yaml
apply_button_text: 去官网申请
```

如果不写，系统默认会显示：

```text
去申请
```

注意：

- 只有在写了 `apply_url` 的情况下，这个按钮才会显示
- 只写这个字段，不写 `apply_url`，按钮还是不会出现

---

### 10. `config_button_text`

作用：配置弹窗里“配置 key 按钮”的文字。

示例：

```yaml
config_button_text: 立即配置
```

如果不写，系统默认会显示：

```text
配置 key
```

---

## 五、给你一份最简单模板

### 场景 1：这是一个完全不用 key 的语音

比如系统内置语音，可以这样写：

```yaml
name: 系统语音
description: 手机自带语音
version: 1.0
create_date: 2026-03-17
```

这种情况下：

- 不会检查 key
- 不会弹“去申请”
- 也不会弹“配置 key”

---

### 场景 2：这是一个需要 key 的第三方语音

```yaml
name: 某某云语音
description: 需要先申请 key 后才能使用
version: 1.0
create_date: 2026-03-17
patch_dir_name: _speech_demo
apply_url: https://www.example.com/
cancel_button_text: 先不配置
apply_button_text: 去官网申请
config_button_text: 现在去配置
required_keys: [accessKey, secretKey]
```

这种情况下：

- 用户没填 `accessKey` 和 `secretKey` 时
- 程序会弹框提醒
- 可以点“去官网申请”打开申请网站
- 也可以点“现在去配置”跳到配置页

---

### 场景 3：需要 key，但是不想给“去申请”按钮

```yaml
name: 内部语音服务
description: 由管理员统一分配 key
version: 1.0
create_date: 2026-03-17
patch_dir_name: _speech_internal
config_button_text: 去填写信息
required_keys: [token]
```

这种情况下：

- 会检查 `token` 是否已配置
- 会弹配置提示框
- 但**不会显示“去申请”按钮**
- 因为没有写 `apply_url`

---

## 六、一步一步操作教程

下面是最适合非开发人员的操作顺序。

### 第一步：找到要修改的语音目录

例如你要改豆包语音，就打开：

```text
resources/space/speeches/volcengine/
```

### 第二步：打开 `info.yaml`

你只需要改这里面的文字内容。

### 第三步：先改最重要的 4 项

建议先确认这几个字段：

- `name`
- `description`
- `patch_dir_name`
- `required_keys`

因为这几个会直接影响：

- 页面显示什么
- 缺少哪些配置时要拦截
- 点“配置 key”要跳去哪里

### 第四步：决定要不要“去申请”按钮

如果需要，就写：

```yaml
apply_url: 申请网址
```

如果不需要，就删掉这一行，或者不要写。

### 第五步：按需要修改按钮文案

如果你想让提示更像产品文案，而不是技术词，可以改：

```yaml
cancel_button_text: 稍后再说
apply_button_text: 去官网申请
config_button_text: 立即配置
```

### 第六步：保存文件

保存后，这份配置就更新了。

### 第七步：让开发同学帮你构建验证

因为这是工程项目，改完配置后，最好让开发同学重新编译一下，确认没有格式问题。

---

## 七、最常见的错误

### 错误 1：字段名拼错

例如把：

```yaml
required_keys
```

写成：

```yaml
require_keys
```

这样程序就认不出来。

结论：

- 字段名一定要照着教程写
- 不要自己改英文名字

---

### 错误 2：缩进乱了

YAML 对格式比较敏感。

虽然我们这里大多数字段都很简单，但还是建议：

- 一行只写一个字段
- 不要随便多加空格
- 不要用中文冒号 `：`
- 一定要用英文冒号 `:`

正确：

```yaml
name: 豆包语音
```

错误：

```yaml
name：豆包语音
```

---

### 错误 3：网址没写完整

例如：

```yaml
apply_url: www.example.com
```

这样不规范。

建议一定写完整：

```yaml
apply_url: https://www.example.com/
```

---

### 错误 4：`required_keys` 格式不对

正确：

```yaml
required_keys: [accessKey, appKey]
```

不要漏掉：

- 方括号
- 英文逗号

---

### 错误 5：`patch_dir_name` 乱写

这个值通常要和已有补丁目录对应。

如果这里写错：

- 用户点击“配置 key”
- 可能打不开正确页面

如果你不知道该填什么，最稳妥的方法是：

- 先参考一个已有语音的写法
- 或者请开发同学确认

---

## 八、推荐的编辑方法

如果你是产品、运营、测试同学，不熟悉代码，推荐这样做：

### 方法 1：照着已有的 `volcengine` 改

它已经是一个完整示例，包含：

- 必填 key
- 申请网址
- 按钮文案
- 配置页跳转

### 方法 2：先复制，再改内容

新增语音时，不建议从空白开始写。

建议：

1. 复制一个最接近的现成目录
2. 改目录名
3. 改 `info.yaml` 内容

这样出错率最低。

---

## 九、给非开发人员的最简单判断法

如果你不知道一个字段要不要填，可以用下面这个判断表。

### 这个语音需不需要用户自己填写 key？

- 需要：写 `required_keys`
- 不需要：不要写 `required_keys`

### 这个语音需不需要引导用户去官网申请？

- 需要：写 `apply_url`
- 不需要：不要写 `apply_url`

### 这个语音点“配置 key”后要不要跳到设置页？

- 需要：写 `patch_dir_name`
- 不需要：通常也就不会提供配置入口

### 这个弹窗文案要不要更像产品语言？

- 需要：写按钮文案字段
- 不需要：不写也行，系统会用默认值

---

## 十、推荐你直接抄的完整示例

```yaml
name: 豆包语音
description: 豆包同款在线语音识别
version: 1.0
create_date: 2025-11-19
patch_dir_name: _speech_volcengine
apply_url: https://www.volcengine.com/
cancel_button_text: 稍后再说
apply_button_text: 去官网申请
config_button_text: 立即配置
required_keys: [accessKey, appKey]
```

---

## 十一、改完后你应该检查什么

改完一个 `info.yaml` 后，请自己检查这 6 件事：

- `name` 有没有写
- `description` 是否通顺
- `required_keys` 格式对不对
- `apply_url` 是否是完整网址
- `patch_dir_name` 是否对应正确配置页
- 按钮文案是否符合产品表达

---

## 十二、如果你完全不会写，最安全的做法

你可以直接照下面这个句式，把需求发给开发同学：

```text
请帮我新增一个 speech 配置：
1. 名称叫：XXX
2. 简介是：XXX
3. 需要填写的 key 有：XXX、XXX
4. 官网申请地址是：XXX
5. 配置页代号是：XXX
6. 取消按钮文案：XXX
7. 申请按钮文案：XXX
8. 配置按钮文案：XXX
```

这样对方就能很快帮你落成配置。

---

## 十三、最后总结

你只需要记住一句话：

**`info.yaml` 就是一张“语音服务说明表”。**

你在这里填的内容，会决定：

- 用户看到什么名字
- 用户看到什么介绍
- 是否必须先填 key
- 是否显示“去申请”按钮
- 弹窗按钮写什么字
- 点“配置 key”跳去哪里

如果你只是做产品配置，不用理解底层代码，照着这份教程填写就可以。
