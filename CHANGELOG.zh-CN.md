# P4-CAN Universal 中文更新记录

> 本文件先提供 v3.35.3 与 v3.35.2 的简体中文更新摘要。更早版本的完整记录请查看 [CHANGELOG.md](CHANGELOG.md)。

## v3.35.3 — 2026-11-19

- 新增 Lighting 灯光功能。
- 新增实验性灯光选项。
- 修复 AP 退出后再次接入时出现的 R79 注入错误。
- 在标准版和中文 Dashboard 中加入 AP 强制远光灯，以及动态刹车灯设置（关闭 / 轻踩刹车 / 重踩刹车）。
- 灯光功能独立放在 `lighting/` 模块中，复用提供的纯逻辑参考实现。
- 增加灯光设置持久化、`/api/lighting/stats`、`/api/lighting/update`，并监听三条物理总线的 RX 路径。
- 灯光功能由独立任务处理。AP 权限需要驾驶员主动踩下制动踏板（PUSH）条件；AP 退出或数据过期时停止。
- 动态刹车灯使用踏板输入，并要求新鲜的 D 挡状态及车速大于 8 km/h；仅处理 `0x3E9` 刹车请求位。
- 保留传输/恢复门控和常规转向灯优先级。

## v3.35.2 — 2026-11-19

- 新增 S3XY 动作：AP 右变道（UP_2=4）和 AP 左变道（DOWN_2=8），并保存按键动作分配。
- 在拨杆车型上使用现有单次/旧版转向灯传输及 TX 门控；保留常规 Blinker / Auto Blinker 命令。
- 移除 LAB 菜单、LAB 首页和底部导航入口。
- 将 CAN Research Capture 移入 System 页面，并保留设置页返回导航。
- 新增实验性设置卡片，将 FSD Visualisation、SmartShift、Country / Map、Lane Change 和 Continuous AP 放入其中。
- 新增 GPIO 设置。
- 新增 Battery Preheating Beta（电池预热 Beta）。
- 集成实验性 SmartShift 功能，来源：[P4Can-automatic-shifting](https://github.com/kl79613/P4Can-automatic-shifting)。
- 新增 S3XY 动作：FSD Visualisation。
- 新增服务模式入口。
- 恢复 Settings > Auto Lane Change Enable。
- 为标准 AP 配置增加 S3XY 变道按键支持：LEFT 发送 DOWN_2（0x8），RIGHT 发送 UP_2（0x4）。
- 新增简体中文（zh-CN）Dashboard 版本。
