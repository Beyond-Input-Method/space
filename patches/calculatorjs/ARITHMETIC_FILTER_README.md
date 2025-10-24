# 算术表达式计算过滤器 (Arithmetic Filter)

## 📖 简介

`ArithmeticFilter` 是一个 RIME 输入法的 JavaScript Filter 插件,用于识别**前置文本**(external context)中的算术表达式并自动计算结果。

## 🎯 功能特点

### 与 Translator 版本的区别

| 特性 | Translator 版本 | Filter 版本 |
|------|----------------|-------------|
| **处理范围** | 只能处理当前输入 | 可以处理前置文本(external context) |
| **使用场景** | 直接在RIME中输入表达式 | 外部输入表达式,RIME中触发计算 |
| **候选项位置** | 替换当前输入 | 添加到候选列表开头 |
| **segment限制** | 受segment范围限制 | 不受segment限制 |

### 核心功能

1. ✅ **识别前置文本中的表达式**
   - 自动从 external context 中提取算术表达式
   - 支持跨越前置文本和当前输入的表达式

2. ✅ **智能计算**
   - 安全的表达式计算(使用 Function 而非 eval)
   - 支持基本运算: `+`, `-`, `*`, `/`, `()`
   - 支持幂运算: `**`

3. ✅ **多种输出格式**
   - 计算结果: `8093`
   - 完整等式: `8084+9 = 8093`
   - 原始表达式: `8084+9`

4. ✅ **详细日志**
   - 完整的执行流程日志
   - 便于调试和追踪问题

## 🚀 使用方法

### 1. 配置 RIME Schema

在你的 schema 配置文件中添加 Filter:

```yaml
engine:
  filters:
    - qjs_filter@arithmetic_filter  # 添加算术过滤器
    - uniquifier                     # 其他filter...
```

### 2. 使用示例

#### 场景1: 外部输入表达式

```
步骤1: 在外部输入框输入 "8084+9"
步骤2: 切换到RIME,输入任意拼音(如 "j")
步骤3: 候选列表中会显示:
  1. 8093          (= 8084+9)
  2. 8084+9 = 8093 (算术计算)
  3. 8084+9        (表达式)
  4. [其他拼音候选项...]
```

#### 场景2: 表达式在当前输入中

如果表达式完全在当前输入中,Filter 会跳过处理,交由 Translator 处理:

```
输入: "100+200"
结果: 由 ArithmeticCalculator (Translator) 处理
```

## 📋 工作原理

### 处理流程

```
1. Filter 接收候选项列表
   ↓
2. 获取 external context (前置文本)
   ↓
3. 检查前置文本是否包含算术表达式
   ↓
4. 如果表达式在前置文本中:
   - 计算表达式结果
   - 创建算术候选项
   - 插入到候选列表开头
   ↓
5. 返回处理后的候选项列表
```

### 关键判断逻辑

```javascript
// 检查表达式位置
if (exprInfo.startPos < precedingTextLen) {
  // 表达式在前置文本中 → Filter 处理
  // 生成算术候选项并添加到列表
} else {
  // 表达式在当前输入中 → Translator 处理
  // Filter 跳过,返回原候选项列表
}
```

## 🔧 技术细节

### Filter vs Translator

**Filter 的优势:**
- 不受 segment 范围限制
- 可以访问 external context
- 可以在任何候选项列表中添加新候选项
- 适合"触发式"计算场景

**Translator 的优势:**
- 直接响应用户输入
- segment 范围精确
- 适合"即时计算"场景

### 候选项创建

```javascript
const cand = new Candidate(
  "arithmetic",        // type: 候选项类型
  0,                   // start: 起始位置
  input.length,        // end: 结束位置
  formattedResult,     // text: 显示文本
  `= ${expression}`    // comment: 注释
);
```

## 📊 日志示例

```
========== [ArithmeticFilter] filter 开始 ==========
[ArithmeticFilter] 收到 5 个候选项
[ArithmeticFilter] 前置文本: "8084+9"
[ArithmeticFilter] 当前输入: "j"
[ArithmeticFilter] 完整文本: "8084+9j"
[ArithmeticFilter] --- extractExpression 开始 ---
[ArithmeticFilter] 有效字符结束位置: 6
[ArithmeticFilter] 提取的原始表达式: "8084+9" (位置: 0-6)
[ArithmeticFilter] ✓ 识别到表达式: "8084+9"
[ArithmeticFilter] ✓ 表达式在前置文本中,由Filter处理
[ArithmeticFilter] ✓ 计算成功: 8093
[ArithmeticFilter] 格式化结果: "8093"
[ArithmeticFilter] --- 生成候选项 ---
[ArithmeticFilter] 添加候选项: "8093" (= 8084+9)
[ArithmeticFilter] 添加候选项: "8084+9 = 8093"
[ArithmeticFilter] 添加候选项: "8084+9"
[ArithmeticFilter] 总共生成 3 个算术候选项
[ArithmeticFilter] 最终候选项数量: 8
========== [ArithmeticFilter] filter 结束 (成功) ==========
```

## ⚠️ 注意事项

1. **前置文本要求**
   - 必须有 external context (前置文本)
   - 表达式必须在前置文本中才会触发

2. **表达式格式**
   - 必须包含运算符 (`+`, `-`, `*`, `/`)
   - 括号必须匹配
   - 不能以运算符结尾

3. **性能考虑**
   - Filter 会在每次候选项生成时执行
   - 如果没有前置文本,会快速跳过

## 🔗 相关文件

- **Filter 实现**: `arithmetic_filter.js`
- **Translator 实现**: `arithmetic_calculator.js`
- **使用说明**: 本文档

## 📝 版本历史

- **v1.0.0** (2025-01-23)
  - 初始版本
  - 支持前置文本中的表达式识别
  - 支持基本算术运算
  - 详细的调试日志

## 🤝 贡献

欢迎提交问题和改进建议!

---

**作者**: librime-qjs  
**许可**: 与 librime 项目相同
