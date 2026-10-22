# ChatGPT Planner — Work + Codex 定制版

ChatGPT 普通聊天和 Work 负责讨论、研究、规划、验收与复审；Codex 负责检查实际环境、修改项目、执行操作和验证，并反馈证据。只想探讨时，两端都停留在讨论阶段。

这是基于 [long-woo/chatgpt-planner](https://github.com/long-woo/chatgpt-planner) 3.1.0 的非官方修改版，定制版版本为 1.0.0。原版作者版权声明和完整 MIT 许可保留在 [LICENSE](LICENSE)。修改清单与资源处理见 [NOTICE.md](NOTICE.md)，原始文件哈希见 [UPSTREAM.json](UPSTREAM.json)。本项目不代表原作者或 OpenAI，也不暗示获得其认可。

## 使用

1. 在已安装本插件的 ChatGPT 普通聊天或 Work 中，用技能选择器选择显示名 `ChatGPT Planner · Work + Codex`：先比较方案、拆解任务、明确边界和验收方法。普通讨论不强制返回 JSON。
2. 准备实施时，规划端给出六字段任务说明。若没有可用且已获授权的派发接口，复制说明给 Codex；“说明已生成”不表示“任务已派发”。
3. 在 Codex 选择 `$chatgpt-planner-work-codex:chatgpt-planner-work-codex`，粘贴任务说明并要求实施。Codex 按真实环境实现、运行相关验证、返回证据。这个完整名字来自插件命名空间；如果只安装独立技能包，则为 `$chatgpt-planner-work-codex`。
4. 把证据带回规划端复审。未运行的检查保持“未验证”，没有经过规划端复审的结果保持“待复审”。

可以直接在 Codex 说：“按已确认清单实施”。用户目标和边界已清楚时，Codex 从上下文整理六字段后执行，无需先另开 ChatGPT 网页。只说“讨论”“先看看方案”时，不修改项目、不创建或发送任务。

## 安装

插件只包含一个技能，不包含 MCP 服务、钩子或自动派发脚本。不要同时安装插件和同名独立技能副本。

本机通过内置 CLI 注册本目录中的 marketplace 并安装：

```powershell
codex plugin marketplace add 'C:\path\to\chatgpt-planner-work-codex' --json
codex plugin add chatgpt-planner-work-codex@planner-work-codex-local --json
codex plugin list --marketplace planner-work-codex-local --json
```

把示例路径替换成解压后本目录的绝对路径。新会话可加载安装结果；若界面未更新，重新打开应用。卸载用 `codex plugin remove chatgpt-planner-work-codex@planner-work-codex-local`，不删除上游快照。

本地插件、工作区插件和网页端安装分别管理。CLI 的安装成功不证明某个 ChatGPT 普通 Chat 或 Work 会话已经加载。桌面端需分别在普通聊天和 Work 的技能选择器确认；网页/云端需要账户或工作区提供插件导入入口，并按该入口安装本插件包。若入口不提供，直接把技能规则和任务说明作为当前聊天的明确上下文使用，这属于手动加载，不等同于安装。

[官方技能说明](https://learn.chatgpt.com/docs/build-skills)说明了本地发现与调用语法；[官方插件打包说明](https://developers.openai.com/plugins/build/plugins)说明了本地 marketplace 和安装范围。最终安装与实测状态记录在本次交付的实施报告中，不在通用技能中预写成功状态。

## 分工与格式

交接保持原版的 `goal`、`scope`、`non_goals`、`implementation_constraints`、`acceptance_criteria`、`verification` 六字段，任务拆分放进 `scope`，不额外制造流程文件。需要保存计划或交接文件时，按用户指定位置保存。

规划端可以阅读资料、搜索、比较方案、编写计划和复审；项目文件修改、安装配置、部署、发布和外部状态变更交给 Codex。技能是行为约定，不能改变真实工具权限或替用户授权。角色由可信宿主信息识别，不能因为 Work 也有终端或文件工具就把它当成 Codex。

本地验证：

```powershell
python -m pip install -r requirements-dev.txt
python scripts/validate_package.py
```

此检查核实格式、引用、许可、交接模式和打包边界。典型情景需另做行为评估；静态检查不证明真实 Chat/Work 会话已调用技能。
