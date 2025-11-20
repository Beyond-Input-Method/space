# 虚拟键盘触感方案说明文档

## 概述

本文档包含 10 种不同风格的虚拟键盘按键触感方案，每种方案都严格遵循 HarmonyOS 振动开发规范。每种风格包含 4 个触感配置文件，分别对应不同的按键类型。

## 目录结构

```
keyboard_haptics/
├── gentle/          # 轻柔触感
├── crisp/           # 清脆触感
├── mechanical/      # 机械键盘触感
├── typewriter/      # 打字机触感
├── modern/          # 现代简约触感
├── strong/          # 强劲有力触感
├── bouncy/          # 弹性触感
├── precise/         # 精准触感
├── comfortable/     # 舒适触感
└── gaming/          # 游戏触感
```

每个目录包含 4 个 JSON 文件：
- `default.json` - 默认按键触感
- `return.json` - 回车键触感
- `backspace.json` - 删除键触感
- `space.json` - 空格键触感

## 方案详细说明

### 1. 轻柔触感 (gentle)

**特点**：柔和、低强度、适合长时间打字
- **默认按键**：瞬态振动，强度 25%，频率 50Hz
- **回车键**：双击效果，强度 40% + 20%
- **删除键**：渐弱连续振动，35ms 持续时间
- **空格键**：轻微瞬态振动，强度 28%

**适用场景**：夜间使用、安静环境、长文本输入

### 2. 清脆触感 (crisp)

**特点**：干脆利落、中等强度、清晰反馈
- **默认按键**：瞬态振动，强度 55%，频率 60Hz
- **回车键**：双击效果，强度 75% + 45%
- **删除键**：快速衰减，30ms 持续时间
- **空格键**：中等强度瞬态振动，强度 50%

**适用场景**：日常打字、办公环境、一般文本输入

### 3. 机械键盘触感 (mechanical)

**特点**：模拟机械键盘的双段触感
- **默认按键**：双段瞬态振动，强度 65% + 35%
- **回车键**：三段触感，强度递减（85% → 50% → 30%）
- **删除键**：连续振动带渐弱曲线，40ms 持续时间
- **空格键**：双段触感，强度 70% + 40%

**适用场景**：机械键盘爱好者、追求打字手感

### 4. 打字机触感 (typewriter)

**特点**：模拟经典打字机的机械冲击感
- **默认按键**：冲击式连续振动，25ms，频率 45Hz
- **回车键**：长冲击 + 回弹，45ms + 瞬态
- **删除键**：中等冲击感，35ms 持续时间
- **空格键**：强劲冲击，30ms，强度 70%

**适用场景**：怀旧体验、创意写作、特殊场景

### 5. 现代简约触感 (modern)

**特点**：简洁、现代、平衡的触感设计
- **默认按键**：简单瞬态振动，强度 45%
- **回车键**：平滑连续振动，35ms 渐弱曲线
- **删除键**：简洁瞬态振动，强度 50%
- **空格键**：轻微瞬态振动，强度 42%

**适用场景**：现代 UI 设计、极简主义用户

### 6. 强劲有力触感 (strong)

**特点**：高强度、明显反馈、适合嘈杂环境
- **默认按键**：强力瞬态振动，强度 80%
- **回车键**：最强瞬态（100%）+ 连续振动（70%）
- **删除键**：强力连续振动，45ms，强度 85%
- **空格键**：强力瞬态振动，强度 85%

**适用场景**：嘈杂环境、户外使用、需要明确反馈

### 7. 弹性触感 (bouncy)

**特点**：模拟弹簧回弹效果，富有弹性
- **默认按键**：弹性曲线，40ms，多次振幅变化
- **回车键**：多次回弹效果，60ms，6 个调节点
- **删除键**：中等回弹，45ms，5 个调节点
- **空格键**：平衡回弹，42ms，5 个调节点

**适用场景**：追求趣味性、游戏化体验

### 8. 精准触感 (precise)

**特点**：精确、快速响应、专业感
- **默认按键**：高频瞬态振动，频率 62Hz，强度 60%
- **回车键**：双击高频振动，强度 80% + 50%
- **删除键**：快速衰减，28ms 持续时间
- **空格键**：精准瞬态振动，强度 58%

**适用场景**：专业打字、编程、需要精确反馈

### 9. 舒适触感 (comfortable)

**特点**：舒适柔和、适合长时间使用
- **默认按键**：柔和连续振动，32ms，强度 38%
- **回车键**：平滑连续振动，48ms，强度 52%
- **删除键**：温和连续振动，38ms，强度 42%
- **空格键**：舒适连续振动，35ms，强度 40%

**适用场景**：长时间打字、减少疲劳、舒适优先

### 10. 游戏触感 (gaming)

**特点**：快速响应、高强度、电竞级反馈
- **默认按键**：高频瞬态振动，频率 68Hz，强度 72%
- **回车键**：三连击效果，强度递减（95% → 60% → 35%）
- **删除键**：快速强力振动，32ms，强度 78%
- **空格键**：高频强力瞬态，频率 69Hz，强度 75%

**适用场景**：游戏输入、竞技场景、快速响应需求

## 技术规范

### 低延时设计

所有触感方案的 `StartTime` 均设置为 **0ms**，确保按键触发后立即产生振动反馈，满足低延时要求。

### 符合 HarmonyOS 规范

所有 JSON 文件均遵循以下规范：
- ✅ 使用标准 JSON 格式
- ✅ 包含必需的 MetaData 属性（Version, ChannelNumber）
- ✅ 振动强度范围：0-100
- ✅ 振动频率范围：0-100
- ✅ 振动事件数量 ≤ 128
- ✅ 文件大小 < 64KB
- ✅ Curve 调节点数量：4-16 个

### 振动类型说明

#### Transient（瞬态振动）
- 干脆有力的短振动
- 适合按键点击反馈
- 无需设置 Duration

#### Continuous（连续振动）
- 可调节的长振动
- 支持 Curve 曲线调节
- 适合需要渐变效果的场景

## 使用建议

### 选择指南

| 使用场景 | 推荐方案 | 备选方案 |
|---------|---------|---------|
| 日常打字 | 清脆触感 | 现代简约 |
| 长时间输入 | 舒适触感 | 轻柔触感 |
| 专业编程 | 精准触感 | 机械键盘 |
| 游戏场景 | 游戏触感 | 强劲有力 |
| 安静环境 | 轻柔触感 | 舒适触感 |
| 嘈杂环境 | 强劲有力 | 游戏触感 |
| 趣味体验 | 弹性触感 | 打字机 |
| 怀旧风格 | 打字机 | 机械键盘 |

### 集成方法

```typescript
// 示例：加载触感配置
import vibrator from '@ohos.vibrator';

// 加载触感文件
const hapticFile = 'keyboard_haptics/crisp/default.json';

// 触发振动
vibrator.startVibration({
    type: 'file',
    hapticFd: { fd: hapticFile }
}, {
    usage: 'touch'
});
```

### 自定义建议

如需调整触感强度，可修改以下参数：
- **Intensity**：调整振动强度（0-100）
- **Frequency**：调整振动频率（0-100，55 为谐振频率）
- **Duration**：调整持续时间（仅 continuous 类型）
- **Curve**：调整振动曲线（精细控制）

## 文件清单

共计 **40 个 JSON 文件**，分布在 10 个目录中：

```
✅ gentle/default.json
✅ gentle/enter.json
✅ gentle/backspace.json
✅ gentle/space.json
✅ crisp/default.json
✅ crisp/enter.json
✅ crisp/backspace.json
✅ crisp/space.json
✅ mechanical/default.json
✅ mechanical/enter.json
✅ mechanical/backspace.json
✅ mechanical/space.json
✅ typewriter/default.json
✅ typewriter/enter.json
✅ typewriter/backspace.json
✅ typewriter/space.json
✅ modern/default.json
✅ modern/enter.json
✅ modern/backspace.json
✅ modern/space.json
✅ strong/default.json
✅ strong/enter.json
✅ strong/backspace.json
✅ strong/space.json
✅ bouncy/default.json
✅ bouncy/enter.json
✅ bouncy/backspace.json
✅ bouncy/space.json
✅ precise/default.json
✅ precise/enter.json
✅ precise/backspace.json
✅ precise/space.json
✅ comfortable/default.json
✅ comfortable/enter.json
✅ comfortable/backspace.json
✅ comfortable/space.json
✅ gaming/default.json
✅ gaming/enter.json
✅ gaming/backspace.json
✅ gaming/space.json
```

## 版本信息

- **创建日期**：2025-11-19
- **版本**：1.0
- **兼容性**：HarmonyOS 振动框架 1.0+

## 注意事项

> [!IMPORTANT]
> 1. 所有触感文件均已测试符合 HarmonyOS 振动开发规范
> 2. StartTime 均为 0，确保低延时响应
> 3. 建议根据实际设备测试后微调参数

> [!TIP]
> - 可以根据用户偏好提供触感方案选择
> - 建议在设置中允许用户调整触感强度
> - 不同按键类型使用不同触感可提升用户体验

> [!WARNING]
> - 过高的振动强度可能影响电池续航
> - 建议提供"关闭触感"选项
> - 某些设备可能不支持频率调节

## 参考文档

- [HarmonyOS 振动开发指导](./HarmonyOS振动开发指导.md)
