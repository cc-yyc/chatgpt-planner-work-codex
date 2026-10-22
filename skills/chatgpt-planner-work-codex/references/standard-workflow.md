# STANDARD 与 COMPREHENSIVE

STANDARD 适用于有边界的功能、页面、接口或流程。Chat 或 Work 分析关键方案、状态、依赖及边界，输出一份六字段交接；Codex 核实环境、实现并收集证据，规划端据此验收。

COMPREHENSIVE 用于更复杂或高影响的决策，按需要补充数据、安全、兼容性、回退与发布分析。分析更充分，交接仍只有六字段；不自动制造额外产物或审批。

用户已确认的任务可直接交 Codex；只讨论或规划时不实施。UI 约束写入 `implementation_constraints`，反馈明确已完成、需修复和未验证项。复审依据 [复审协议](reviewer-protocol.md)，不能把待复审结果冒充已验收。
