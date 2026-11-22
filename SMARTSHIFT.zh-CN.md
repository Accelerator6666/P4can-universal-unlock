# SmartShift 自动换挡

## 功能与信号

本功能替代此前对 `UI_enableSmartShift` / BODY `0x334` 字段的直接覆盖。

Pedal Response（踏板响应）和 AP Accel / Regen（AP 加速 / 能量回收）仍保留原有的 `0x334` 处理逻辑。

- 上游项目：[P4Can-automatic-shifting](https://github.com/kl79613/P4Can-automatic-shifting)
- 上游 Commit：`c61c90dd40153b62271e524bcd354a75900e9749`（MIT，已保留 LICENSE）
- 四个可移植核心头文件保持未修改状态。
- 适配后的运行时和 Web 文件位于 `automatic_shift/`。
- 上游测试仅调整了 include 路径。

## 运行机制

服务会监听三条物理总线，并由独立的 10 ms 任务运行。

- **V12**：评估雷达距离。
- **V13/V14**：使用 `0x255` 与 `0x12B` 候选报文对。

可选的独立确认条件包括：

- D/R 挡手动转向
- P 挡转向
- D/R 挡障碍物转向

P 挡转向的方向符号校准仅适用于 Model Y Legacy。选择 V12 不会隐式地为其他车型执行校准。

## 换挡请求与保护条件

系统会复制新鲜且经过验证的 BODY 模板：

- V12：`0x229`
- V13/V14：`0x678`

系统保留并检查以下条件：

- 原始制动状态
- 车速
- 加速踏板
- 车门状态
- 安全带状态
- 模板采样数量
- 冷却时间
- 最终确认门控

一次真实的物理制动踏板按压最多只允许产生一次请求。

禁用后重新启用，以及 CAN 恢复流程，都会保留已经消耗的制动事件周期（brake epoch）。

最终应用层 TX 互斥锁负责串行化换挡执行与恢复/配置操作。CAN 恢复时会使观察器、模板和候选跟踪器失效。

以下情况会阻止执行：

- 被动模式
- 管理性发送保持（administrative hold）
- 控制器不可用
- 不支持 BODY-A / CHASSIS-B 路由

**当前移植版本不支持 Model YL 的 SmartShift 执行。**

## 设置页面

`Settings > SmartShift` 提供以下设置：

- 执行开关
- 协议选择
- 车速总线
- 安全带要求
- 三项独立转向确认开关
- 车速阈值
- 冷却时间
- 转向角度
- 障碍物距离

页面状态包括候选来源、数据源、拒绝原因、模板就绪状态，以及请求/确认/失败计数。

该功能独立于 LAB。

## API

获取状态：

`GET /api/smartshift/stats`

更新配置：

`POST /api/smartshift/update`

支持一个或多个字段：

| 字段 | 允许值 / 范围 |
| --- | --- |
| `enabled` | 启用状态 |
| `protocol` | `AUTO` / `V12` / `V13V14` |
| `speedBus` | `0` BODY / `1` CHASSIS / `2` PARTY |
| `requireSeatbelt` | 安全带确认开关 |
| `requireSteering` | 转向确认开关 |
| `steeringFallback` | 手动挡位转向备用确认 |
| `parkSteeringFallback` | P 挡转向备用确认 |
| `maxKph` | `0..8` |
| `hardCutKph` | `1..30`，且必须大于或等于 `maxKph` |
| `cooldownMs` | `0..10000` |
| `pDeg` / `drDeg` / `obstacleDeg` | `1..720` |
| `obstacleCm` | `1..499` |

## 配置存储

配置以带版本号的 22 字节数据块形式原子写入：

`features/autoShiftCfg`

写入后会进行读回校验。

旧的 `features/smartshift` 字段会被忽略，不能启用实际换挡执行。新安装默认关闭执行功能。

## 验证范围与限制

`tests/test_automatic_shift_host.py` 会在 ASan/UBSan 下编译三组上游核心测试，以及实际适配后的运行时和 Web 代码。测试覆盖一次可观察到的 V12 制动触发请求，以及维护/恢复/配置互锁。

独立 Dashboard Demo 仅模拟配置和状态，不会实际换挡。

上游报告的主要测试环境是配备雷达的 2021 款 Model Y（V12）。**本移植版本尚未完成整套固件编译、刷写或实车测试。** Model 3 和 Juniper 的执行情况仍未验证。主机测试结果不能证明 ECU 会接受报文，也不能证明车辆会按预期运动。
