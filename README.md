# Space 资源目录说明

## 目录

- [1. 这个目录是做什么的？](#1-这个目录是做什么的)
- [2. 顶层重要文件](#2-顶层重要文件)
- [3. 子目录一览](#3-子目录一览)
- [4. 如果我想修改这些资源-该注意什么](#4-如果我想修改这些资源该注意什么)
- [5. 给以后自己或同伴的小记](#5-给以后自己或同伴的小记)
- [6. 主题themes进阶public-公共目录怎么用](#6-主题themes进阶public-公共目录怎么用)
- [7. 方案schemas进阶目录结构和导入规则](#7-方案schemas进阶目录结构和导入规则)
- [8. 方案-infoyaml-示例以-bim-pinyin-为例](#8-方案-infoyaml-示例以-bim-pinyin-为例)

## 1. 这个目录是做什么的？

- 用来存放输入法「Space」 仓库里的各种资源文件。
- 这里的文件决定了：
  - 用哪一种输入方案（schema），比如拼音方案。
  - 键盘长什么样（主题 theme）。
  - 用哪些符号面板、表情包、声音、振动方案等。
- 你可以简单地把这里理解成：**「键盘外观 + 行为 的素材和配置仓库」**。

> 如果你只是正常使用输入法，不需要改这里的内容。
> 只有在「想做深度定制」或者「开发新方案 / 主题」时才需要动它。

---

## 2. 顶层重要文件

- **space.yaml**
  - 这是整个 Space 的「入口配置文件」。
  - 它告诉系统：默认用哪个方案、哪个主题、哪些资源目录。
  - 当前内容示例（简化解释）：
    - `schema`: 默认输入方案名称，例如 `bim-pinyin`。
    - `schema_dir`: 输入方案所在的目录，一般是 `schemas/`。
    - `theme`: 默认主题名称，例如 `t9`。
    - `theme_dir`: 主题所在的目录，一般是 `themes/`。
    - `symbol`: 默认符号方案名称，例如 `default`。
    - `symbol_dir`: 符号配置目录，一般是 `symbols/`。
    - `emoticon`: 默认表情方案名称，例如 `default`。
    - `emoticon_dir`: 表情配置目录，一般是 `emoticons/`。
    - `config_version`: 配置版本号，目前是 `1.0`，用来区分不同配置格式。
    - `sound_on`: 是否开启按键音效（`true/false`）。
    - `sound_volume`: 按键音量大小（数字）。
    - `sound_effect`: 使用哪一套音效资源，例如 `default`。
    - `haptics_on`: 是否开启按键振动（`true/false`）。
    - `haptics_volume`: 振动强度（数字）。

- **LICENSE**
  - Space 仓库的开源协议文件。
  - 一般不需要修改，只是说明这些资源的版权和使用规则。

- **.git / .gitmodules**
  - 用来把 Space 当成一个独立仓库或子模块管理。
  - 对于日常使用来说可以忽略，不建议随便删除或修改。

---

## 3. 子目录一览

下面是 `resources/space/` 下各个子目录的大致作用，用「看得懂」的方式简单解释：

- **schemas/**
  - 存放输入方案（schema）的配置，例如拼音方案、双拼方案等。
  - 一般是一些 `.yaml` 或其他文本配置文件，里面写着「怎么把按键变成文字」。

- **themes/**
  - 键盘主题相关资源：颜色、布局风格、背景等。
  - 想做「皮肤」类效果时，通常会改这里的文件。

- **symbols/**
  - 符号面板配置，比如各种标点、特殊符号、数学符号等如何排布。
  - 不同的 symbol 方案可以决定你看到的是「哪一套符号键盘」。

- **emoticons/**
  - 表情相关配置和资源，例如颜文字、特殊表情组合等。
  - 不一定是图片，也可能是文本形式的表情。

- **sounds/**
  - 键盘声音资源，例如按键音效、确认音等。
  - `space.yaml` 里的 `sound_effect` 字段会引用这里的某个音效方案。

- **haptics/**
  - 震动（触觉反馈）配置，比如按键时「轻震一下」还是「重点震动」。
  - `space.yaml` 里的 `haptics_on` 和 `haptics_volume` 会影响这些效果是否启用、强度多大。

- **patches/**
  - 补丁配置，用来对现有方案做「局部修改 / 增强」。
  - 比如：调整候选条高度、修改某个按键功能等。
  - 补丁通常配合项目里的补丁系统一起工作，不建议随意删除。

- **plugins/**
  - 插件相关配置或脚本，用来扩展输入法行为。
  - 例如：日期自动生成、特殊格式转换等高级功能。

- **resources/**
  - 通用资源目录，里面可能包含图片、模板、配置片段等，供其他目录引用。
  - 可以理解成「共享素材库」。

---

## 4. 如果我想修改这些资源，该注意什么？

> 下面这段是写给「想自己折腾一下」的你看的，如果只是普通使用，可以直接跳过。

- **1）改动前先备份**
  - 最稳妥的方式是：
    - 把整个 `resources/space/` 目录复制一份到安全位置；
    - 或者用 git 提交一遍当前状态，这样出问题可以随时回退。

- **2）只改自己看得懂的内容**
  - 建议你优先改：
    - 文本类配置（`*.yaml`、`*.json` 等）；
    - 颜色值、开关布尔值（true/false）、音量数字等。
  - 不太建议：
    - 随便移动 / 删除整个子目录；
    - 修改你完全看不懂的键名或结构。

- **3）整体结构不要乱动**
  - 尽量不要：
    - 删除 `schemas/`、`themes/` 这类顶层目录；
    - 把 `space.yaml` 改成其它名字；
    - 删除 `LICENSE`、`.gitmodules` 等文件。
  - 否则可能导致构建失败，或者运行时加载不到资源。

- **4）改完之后要重新编译 / 重新安装应用**
  - 对于这个输入法项目来说，资源修改好后，建议按项目根目录 README 里的方式重新构建一次。
  - 这样可以保证新的配置真的被打包并生效。

---

## 5. 给以后自己或同伴的小记

- 如果你在别的地方（例如 `products/phone/src/main/resources/resfile/space/`）也看到了类似的目录结构，
  说明那边很可能是「面向具体产品」的拷贝或发布版本，这里则更接近「源仓库」。
- 当你对 Space 里的 schema、theme、patch 做了比较大的调整，建议：
  - 把本文件（`resources/space/README.md`）按需要补充一下；
  - 简单写清楚「改了哪些子目录、主要目的是什么」，方便未来排查问题。

这样，哪怕是完全没有编程基础的同学，只要耐心读一遍这个 README，也能大致明白：
「Space 目录在整个输入法里负责什么」「哪些东西可以改」「改的时候要注意什么」。

---

## 6. 主题（themes）进阶：public 公共目录怎么用？

这里稍微讲细一点 `themes/` 目录，方便你以后看懂主题配置：

- **每个子目录就是一套主题**
  - 例如：`t9/`、`t14/`、`t18/`、`t26_classic/`、`microsoft/` 等。
  - 这些名字会和 `space.yaml` 里的 `theme: t9` 对应，决定默认使用哪一套主题。
  - 一个典型主题目录（以 `t9/` 为例）里通常有：
    - `theme.yaml`：主题的主配置文件（颜色、布局、键盘样式等）。
    - `info.yaml`：主题的简介、作者信息等。
    - `res/`：图片等资源文件。
    - `build/`：编译后的中间产物，一般不需要手动修改。

- **themes/public/ 是所有主题共享的「素材库」**
  - `themes/public/` 下面有很多以 `preset_` 开头的目录，例如：
    - `preset_keyboards/`：常用键盘布局预设，比如 QWERTY 布局、默认高度等。
    - `preset_keys/`：单个按键的预设配置。
    - `preset_color_schemes/`：颜色方案预设。
    - `preset_fonts/`：字体预设。
    - `preset_styles/`：通用样式（圆角、阴影、边框等）。
    - `preset_menu/`：长按菜单、候选菜单等预设。
    - 以及 `style/`、`info/` 等其他公共配置。
  - 这些公共文件的好处是：
    - 多个主题可以**复用**同一份基础配置；
    - 你只需要在主题自己的 `theme.yaml` 里定制少量差异化内容。

- **`__include` 语法：从 public 引用公共配置**
  - 在 `t9/theme.yaml` 开头，你会看到类似这样的写法：
    - `style: __include: ./../public/style/default:/style`
    - `preset_styles: __include: ./../public/preset_styles/default:/preset_styles`
    - `preset_candidates: __include: ./../public/preset_candidates/default:/preset_candidates`
    - `preset_fonts: __include: ./../public/preset_fonts/default:/preset_fonts`
    - `preset_color_schemes: __include: ./../public/preset_color_schemes/default:/preset_color_schemes`
    - `preset_keys: __include: ./../public/preset_keys/default:/preset_keys`
  - 可以简单理解为：
    - `__include: A:/B` 表示「从文件/目录 A 里，把路径 B 对应的那一段配置**拷贝过来用**」。
    - 这样 `t9` 主题就可以直接复用 `public` 里的默认样式、颜色和键盘预设。

- **主题里的 preset_keyboards 如何用到 public？**
  - 在 `t9/theme.yaml` 里，`preset_keyboards` 下会有这样的配置：
    - `__include: ./../public/preset_menu/default:/preset_menu/default_menu`
  - 而 `themes/public/preset_keyboards/default.yaml` 中，则定义了默认的字母键盘布局（QWERTY 行、按键大小、间距等）。
  - 多个主题（比如 `t9` 和别的主题）可以共享这一份默认键盘布局，再各自加一点点差异配置。

> 如果你只是想「改一个主题的颜色或布局」，建议：
> - **优先修改某个具体主题目录里的 `theme.yaml`**；
> - 尽量不要随便改动 `themes/public/` 里的内容，因为它会影响到**所有**引用它的主题。

---

## 7. 方案（schemas）进阶：目录结构和导入规则

`schemas/` 目录里放的是**输入方案**，比如全拼、双拼、五笔等。我们用一个稍微技术一点、但尽量好懂的方式来解释：

- **子目录 = 一大类方案家族**
  - 例如：
    - `bim-pinyin/`：拼音相关的所有方案（全拼、各种双拼、T9 拼音等）。
    - `bim-wubi/`：五笔方案。
    - `zhuyin/`：注音方案。
    - `wanxiang/` 等：其他方案家族。
  - 打开 `bim-pinyin/` 可以看到很多文件：
    - `xxx.schema.yaml`：方案主配置（最关键）。
    - `xxx.custom.yaml`：用户 / 默认的个性化覆盖配置。
    - `xxx.dict.yaml`：词典源文件。
    - `*.db`：编译后的词典数据库。
    - `info.yaml`、`README.md` 等说明文件。

- **什么文件会被当成「方案」？**
  - 在 ` 系统` 里，`Schema` 会这样判断：
    - 只要某个目录里有文件名**以 `.schema.yaml` 结尾**，就认为这是一个「schema 目录」。
    - 如果是单独的一个 `xxx.schema.yaml` 文件，也会被当成一个 schema 文件处理。
  - 这就是「方案的导入规则」的核心：
    - **命名规则**：`*.schema.yaml` 是方案主配置。
    - **目录规则**：包含 `*.schema.yaml` 的目录，会整个被复制到全局 schema 目录中。

- **zip 导入是怎么工作的？**
  - 你可以把它想象成：
    - 把一整套方案文件放进一个「总文件夹」里；
    - 再把这个「总文件夹」压缩成一个 zip；
    - 系统会把解压出来的这个「总文件夹」，整个搬到 `schemas/` 目录下面。
  - **特别重要的规则：最外层一定要是一个文件夹**
    - ✅ 正确：
      - `my_schema/` 目录 → 里面有 `my_schema.schema.yaml`、词典、lua 等文件；
      - 压缩后得到 `my_schema.zip`，zip 里**最外层就是这个 `my_schema/` 文件夹**。
    - ❌ 不推荐：
      - 直接把一堆 `.schema.yaml`、`.dict.yaml` 散文件丢在 zip 根目录；
      - 这样解压后的结构不清晰，也不方便系统判断「这一整套文件属于哪个方案目录」。
  - **方案 zip 打包示例**：
    - 目录结构：
      ```text
      my_schema/                 # 最外层目录（非常重要）
        my_schema.schema.yaml    # 方案主配置
        my_schema.custom.yaml    # 可选：个性化配置
        my_schema.dict.yaml      # 可选：词典
        other_files...           # 其它配套文件
      ```
    - 操作：
      - 选中 `my_schema/` 这个文件夹 → 压缩成 `my_schema.zip`；
      - 在 App 里导入 `my_schema.zip`；
      - 系统会在 `resources/space/schemas/` 下面生成 `my_schema/` 目录，里面就是刚才那些文件。
  - **主题 zip 打包示例（原理类似）**：
    - 目录结构：
      ```text
      my_theme/
        theme.yaml     # 必须：主题主配置
        info.yaml      # 可选：主题说明
        res/           # 可选：图片等资源
        build/         # 可选：编译产物
      ```
    - 压缩方式同上：选中 `my_theme/` → 压缩成 `my_theme.zip` → 在 App 里导入；
    - 系统会把 `my_theme/` 放到 `resources/space/themes/` 下，之后就可以在 `space.yaml` 或方案里引用这个主题。

- **结合实际目录来理解**
  - 现在的项目里，`schemas/bim-pinyin/` 已经包含了一整套拼音方案家族：
    - 比如 `bim_t9.schema.yaml`、`double_pinyin.schema.yaml`、`rime_ice.schema.yaml` 等等。
  - 如果你将来需要导入一套全新的方案，可以大致按这样准备 zip 包：
    - zip 里面有一个目录，比如 `my_schema/`；
    - 这个目录里至少有一个 `my_schema.schema.yaml`；
    - 导入 zip 后，系统会把整个 `my_schema/` 目录复制到 `resources/space/schemas/my_schema/`。

> 小结一下：
> - **名字以 `.schema.yaml` 结尾** → 被当成「方案主配置」识别。
> - **包含这些文件的目录** → 会整体被当成一个方案目录复制到 `schemas/` 下。
> - 其它配套文件（dict、db、lua 等）只要和 `.schema.yaml` 放在一起，就会一起被拷过去。
> - 打 zip 时，请始终保证：**zip 里的最外层是一个清晰命名的目录**（比如 `my_schema/`、`my_theme/`）。

---

## 8. 方案 info.yaml 示例：以 bim-pinyin 为例

每个方案目录里通常都会有一个 `info.yaml`，用来描述这套方案的「名片信息」。
以 `schemas/bim-pinyin/info.yaml` 为例，主要包含几类内容：

- **基础信息**
  - `name`: 在界面上展示给用户看的方案名称，例如：`中文拼音`。
  - `author`: 作者或维护者，例如：`iDvel`。
  - `version`: 版本号，例如：`1.0.1`。
  - `description`: 简短描述，比如「方案主体来源雾松拼音」。
  - `url`: 项目的主页地址或源码地址。
  - `createTime` / `updateTime`: 创建时间 / 最近更新时间。

- **重点：use_theme（为方案绑定主题）**
  - 这一段配置的作用是：
    - 告诉系统「这套方案默认应该用哪一套键盘主题」。
    - 不同的子方案（比如 T9 拼音、双拼）可以对应不同的主题目录。
  - 结构大致如下：
    ```yaml
    use_theme:
      default: "themes/default"
      custom:
        "bim_t9": "themes/t9"
        "bim_t14": "themes/t14"
        "rime_ice_18": "themes/t18"
        "double_pinyin_14": "themes/t14"
        ...
    ```
  - 可以这样理解：
    - `default: "themes/default"`
      - 如果某个子方案**没有在 custom 里单独指定主题**，就用 `themes/default` 这一套主题。
    - `custom` 下面是一张「方案 → 主题」对照表：
      - 左边的键，比如 `"bim_t9"`、`"double_pinyin_18"`：
        - 是方案内部的名字，一般和对应的 `*.schema.yaml` 文件同名（去掉后缀）。
        - 比如 `bim_t9` 通常对应 `bim_t9.schema.yaml`。
      - 右边的值，比如 `"themes/t14"`、`"themes/t18_microsoft"`：
        - 是主题在 Space 里的目录路径。
        - 开头的 `themes/` 表示这是 `resources/space/themes/` 下面的某个子目录。
  - 举几个实际例子：
    - `"bim_t9": "themes/t9"`
      - 当你在应用里选择 `bim_t9` 这套方案时，键盘会自动使用 `themes/t9/` 这套主题。
    - `"double_pinyin_mspy": "themes/microsoft"`
      - 微软双拼方案会自动套用 `themes/microsoft/` 这套主题。
    - `"double_pinyin_sogou_18": "themes/t18_microsoft"`
      - 搜狗双拼 18 键方案则用 `themes/t18_microsoft/`。

> 换句话说：
> - `info.yaml` 里的 `use_theme` 就是在帮你做「**哪套方案默认用哪套皮肤**」的整体规划。
> - 如果你以后新增了一套方案，希望它默认用一套新主题，只需要：
>   1. 在 `schemas/某方案目录/` 里给它加上相应的 `*.schema.yaml`；
>   2. 在 `themes/` 下准备好对应的主题目录；
>   3. 在这张 `custom` 对照表里多加一行，把「方案名」指向「主题目录」。