# HarmonyOS 振动开发指导

[官方文档](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/vibrator-guidelines#%E6%8C%AF%E5%8A%A8%E6%95%88%E6%9E%9C%E8%AF%B4%E6%98%8E)

## 振动类型说明

| 名称 | 说明 |
|------|------|
| 固定时长振动 | 传入一个固定时长,马达按照默认强度和频率触发振动,振动效果描述请参考VibrateTime。 |
| 预置振动 | 系统中的预置振动效果,这些效果适用于某些固定场景,比如效果"haptic.clock.timer"通常用于用户调整计时器时的振感反馈,振动效果描述请参考VibratePreset。 |
| 自定义振动 | 自定义振动提供给用户设计自己所需振动效果的能力,用户可通过自定义振动配置文件,并遵循相应规则编排所需振动形式,使能更加开放的振感交互体验,效果描述请参考VibrateFromFile。 |

## 自定义振动配置文件

自定义振动配置文件为Json格式,示例如下:

```json
{
    "MetaData": {
        "Create": "2023-01-09",
        "Description": "a haptic case",
        "Version": 1.0,
        "ChannelNumber": 1
    },
    "Channels": [
        {
            "Parameters": {
                "Index": 0
            },
            "Pattern": [
                {
                    "Event": {
                        "Type": "transient",
                        "StartTime": 0,
                        "Parameters": {
                            "Frequency": 31,
                            "Intensity": 100
                        }
                    }
                },
                {
                    "Event": {
                        "Type": "continuous",
                        "StartTime": 40,
                        "Duration": 54,
                        "Parameters": {
                            "Frequency": 30,
                            "Intensity": 38,
                            "Curve": [
                                {
                                    "Time": 0,
                                    "Frequency": 0,
                                    "Intensity": 0
                                },
                                {
                                    "Time": 1,
                                    "Frequency": 15,
                                    "Intensity": 0.5
                                },
                                {
                                    "Time": 40,
                                    "Frequency": -8,
                                    "Intensity": 1.0
                                },
                                {
                                    "Time": 54,
                                    "Frequency": 0,
                                    "Intensity": 0
                                }
                            ]
                        }
                    }
                }
            ]
        }
    ]
}
```

## 配置文件结构说明

Json文件共包含3个属性。

### 1. MetaData 属性

文件头信息,可添加以下描述:

| 名称 | 必填项 | 说明 |
|------|--------|------|
| Version | 是 | 文件格式的版本号,向前兼容,目前支持版本1.0。 |
| ChannelNumber | 是 | 表示马达振动的通道数,最大支持双马达通道。 |
| Create | 否 | 可记录文件创作时间。 |
| Description | 否 | 可指明振动效果、创建信息等附加说明。 |

### 2. Channels 属性

马达振动通道的相关信息。

"Channels"是Json数组,表示各个通道的信息,包含2个属性:

| 名称 | 必填项 | 说明 |
|------|--------|------|
| Parameters | 是 | 为通道参数。其中"Index"表示通道编号,0表示全通道发送,1、2分别对应左右马达。0不能与其他通道编号同时作为配置参数。 |
| Pattern | 否 | 马达振动序列。 |

### 3. Pattern 属性

"Pattern"是Json数组,包含振动事件序列,每个"Event"属性代表1个振动事件,支持添加2种振动类型:

| 振动类型 | 说明 |
|----------|------|
| transient | 瞬态短振动,干脆有力。 |
| continuous | 稳态长振动,具备长时间输出强劲有力振动的能力。 |

## Event 事件属性

"Event"表示一个振动事件,包含如下属性:

| 名称 | 必填项 | 说明 |
|------|--------|------|
| Type | 是 | 振动事件类型,为"transient" 或"continuous"。 |
| StartTime | 是 | 振动的起始时间,单位ms,有效范围为[0, 1800,000]。 |
| Duration | 是 | 振动持续时间,仅当类型为"continuous"时有效,单位ms,有效范围为[0, 5000]。 |

## Parameters 参数设置

"Parameters"表示振动事件参数设置,必填项,可设置以下属性参数:

| 名称 | 必填项 | 说明 |
|------|--------|------|
| Intensity | 是 | 振动事件强度,有效范围为[0, 100],数字大小代表最大振动量的xx%。 |
| Frequency | 是 | 振动事件频率,有效范围为[0, 100],一般支持频率调节的马达设置为55时为器件的谐振频率,此时振动量最大,越靠近谐振频率的振动,同强度设置的振动量越大。 |
| Curve | 否 | 振动曲线,当振动事件类型为"continuous"时有效,为Json数组,支持设置一组调节点,调节点数量最大支持16个,最小为4个。 |

### Curve 调节点属性

每个调节点需包含如下属性:

- **Time**: 相对事件起始时间的偏移,最小为0,最大不能超过事件振动时长
- **Intensity**: 相对事件振动强度的增益,范围为[0, 1],此值乘上振动事件强度为对应时间点调节后的强度
- **Frequency**: 相对事件振动频率的变化,范围为[-100, 100],此值加上振动事件频率为对应时间点调节后的频率

## 其他要求

| 参数 | 要求 |
|------|------|
| 振动事件(event)的数量 | 不得超过128个。 |
| 振动配置文件长度 | 不得超过64KB。 |
