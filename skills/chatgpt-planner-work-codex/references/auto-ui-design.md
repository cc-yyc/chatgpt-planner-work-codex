# 有边界的自动 UI 设计

普通 Chat 或 Work 的规划分析可以制定 UI 方向；Codex 接到已确认设计后实施，并可自主决定不改变产品方向的局部实现细节。

| 模式 | 用途 |
|---|---|
| `REUSE_PATTERN` | 现有页面的文案、样式或局部交互修正，复用已核实组件与 token |
| `REFERENCE_ADAPTATION` | 结合用户提供并实际读取的截图、Figma、样稿或设计系统 |
| `AUTO_DESIGN` | 新页面、流程或改版缺少完整视觉参考，至少采用 STANDARD 分析 |

`AUTO_DESIGN` 把需要的设计约束写入 `implementation_constraints`，可用 `AUTO_UI_DESIGN:` 前缀：视觉密度与层级、内容顺序、布局、主操作与反馈、必要的 loading/empty/error/disabled/success 状态、响应式与可访问性。只覆盖本次范围，方向应可逆并贴合已有产品，不强制某种布局风格。

有重大品牌、信息架构或范围选择未定时澄清；普通可逆实现细节由 Codex 处理。不得把“设计整个 UI”当作没有边界的交接，也不因本技能禁用 Codex 原有的 UI 实现与检查能力。证据由 Codex 收集，规划端审查已确认或生成的方向；未检查的状态仍为未验证。
