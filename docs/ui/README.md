# 项目规划助手 × Codex · 1.0.1 外观

| 元素 | 显示内容 |
|---|---|
| 名称 | 项目规划助手 · Codex |
| 简介 | 在 ChatGPT 和 Work 中规划与复审，交给 Codex 实施并验证 |
| 主色 | `#2563EB` |
| 深色主题强调色 | `#60A5FA` |
| 图标 | 蓝色规划文档与深色 `>_` 终端符号组合；SVG 与 400×400 PNG |
| 调用名 | `$chatgpt-planner-work-codex` |

![明暗背景与不同尺寸的图标预览](icon-preview.png)

保留规划助手的蓝色识别，将终端执行符号融入图标，并用中性黑白灰与克制的边框处理呼应 Codex 的简洁风格。这是本地生成的视觉组合检查图，不是 Codex 原生界面截图。实际卡片布局、显示尺寸与界面缓存刷新由客户端决定；插件提供名称、说明、图标与配色元数据。

技能卡片配置在 [agents/openai.yaml](../../skills/chatgpt-planner-work-codex/agents/openai.yaml)。插件列表同时配置 [portable manifest](../../plugin.json) 与 [兼容 manifest](../../.codex-plugin/plugin.json)。图标资源见 [SVG](../../skills/chatgpt-planner-work-codex/assets/planner-icon.svg) 和 [PNG](../../skills/chatgpt-planner-work-codex/assets/planner-icon.png)。

配置字段依据 [OpenAI 官方技能文档](https://learn.chatgpt.com/docs/build-skills) 与 [插件打包文档](https://developers.openai.com/plugins/build/plugins)。此次修改不调整技能的行为规则、默认提示词或自动调用策略。上游两个视觉资源继续排除，新增图标的来源与许可见 [NOTICE](../../NOTICE.md)。

范围与视觉检查见 [外观检查记录](polish-review.md)。

独立 Codex app-server 已在两个工作目录读到唯一启用的独立技能，新名称、两种图标路径和配色均与配置一致；[发现结果](discovery.json)已将本机路径归一化。该结果不等于当前原生窗口的卡片缓存已经刷新。
