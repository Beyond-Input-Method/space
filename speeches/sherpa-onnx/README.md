# Sherpa 离线语音资源

引擎使用 sherpa-onnx 2.0.1，模型类型为 SenseVoice。配置详见 speech.yaml。

## 模型准备

将已准备的 SenseVoice int8 模型放到 `SenseVoice/model.int8.onnx`，与本目录的 `SenseVoice/tokens.txt` 配套。模型本体约 228 MB，沿用本机现有 `*.onnx` 忽略规则，不包含在本次 Git 提交中；部署和打包前必须单独准备。

本次真机包所用模型：

- 文件大小：239233841 字节
- SHA-256：`c71f0ce00bec95b07744e116345e33d8cbbe08cef896382cf907bf4b51a2cd51`

语音在松手后执行离线推理，无实时 partial。默认单次录音最长 60 秒，等待结果最长 30 秒，可在 speech.yaml 调整。

info.yaml 的版本为资源元数据。使用此资源需要共享 bimkit 已移除默认 1.0.0～2.0.0 版本范围限制的修复。

## iOS

iOS 使用同一份 speech.yaml 与 SenseVoice 模型，info.yaml 声明 hmos 和 ios 平台。模型在 Host App 内加载，键盘扩展通过 App Group 请求录音并接收最终结果。iOS 需启用完全访问、麦克风权限和现有 PiP 待机流程。打包时保留相对目录结构；模型仍不纳入 Git。
