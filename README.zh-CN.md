# P4-CAN Universal Unlock v3.35.3

[简体中文](README.zh-CN.md) | [English](README.md)

基于 ESP32-P4/C6 开发板与 3 个 SN65HVD230 CAN 收发器的 P4-CAN 项目。

> **软件版本要求：** 车辆软件低于 2026.20 时，项目可能无法正常工作。

## Dashboard 演示

- [English Dashboard Demo](dashboard_demo.html)
- [简体中文 Dashboard 演示](zh-CN/dashboard_demo.zh-CN.html)

## 版本更新

**v3.35.3**
- 新增 Lighting 灯光选项（实验性功能）。
- 修复 AP 退出后再次接入时的 R79 注入错误。

**v3.35.2**
- 新增 GPIO 设置。
- 新增电池预热 Beta 功能。
- 集成来自 kl79613/P4Can-automatic-shifting 的实验性 SmartShift 功能。
- 新增 FSD 可视化设置。**注意：该功能可能阻止 AP 工作，并导致部分自动泊车错误。**
- 新增 S3XY 动作：FSD 可视化。
- 新增服务模式入口。
- 重新整理设置页面。
- 新增 S3XY 动作：AP 左/右变道。
- 新增简体中文（zh-CN）版本。
- 更多更新内容请查看 [中文更新记录](CHANGELOG.zh-CN.md)；更早版本请查看 [英文完整更新记录](CHANGELOG.md)。

## 功能概览

- Nag 提醒抑制
- Advanced EAP（NOA 自动变道时自动触发转向灯）
- EU 区域解锁（绕过 R79 欧盟限制）
- 召唤距离解锁（±85 m）— ESP32-P4 稳定性修复
- 在所在地区不可用时启用 TLSSC
- 连续 AP（实验性功能）
- ISA 提醒音抑制
- 国家 / 地图区域信号模拟
- 视觉限速控制设置
- 踏板映射设置
- S3XY Button 蓝牙支持（仍有部分问题待修复）
- 恢复“确认空闲车道变道”设置的开关（欧盟地区不可用；可使用 Auto Blinker）
- 关闭驾驶员监控的选项
- Lighting 灯光功能（实验性功能）

部分功能需要有效的 EAP/FSD 订阅。

项目支持 Model 3、Model Y 和 Model YL 的五种车辆配置模式。请务必根据车辆实际硬件选择正确的配置。

## Android 仪表板

[下载 Android APK](https://github.com/06066060606060/t2can-universal-unlock/releases/tag/android_1.2.1)

## CAN 接线

| 物理总线 | 控制器 | TX | RX |
| --- | --- | --- | --- |
| CAN 1 BODY | CAN 1 | GPIO20 | GPIO21 |
| CAN 2 CHASSIS | CAN 2 | GPIO22 | GPIO23 |
| CAN 3 PARTY | CAN 3 | GPIO26 | GPIO27 |

**2026 年 4 月之后生产的 Model Y / Model YL：** 使用 YL Profile，并按下表连接：

| 物理总线 | 控制器 | TX | RX |
| --- | --- | --- | --- |
| CAN 1 VH | CAN 1 | GPIO20 | GPIO21 |
| CAN 2 BODY | CAN 2 | GPIO22 | GPIO23 |
| CAN 3 PARTY | CAN 3 | GPIO26 | GPIO27 |

## 推荐硬件配置

为获得较好的性能和稳定性，项目推荐：

- ESP32-P4 + 3 × SN65HVD230
- 移除 120 Ω 电阻
- 启用高速模式

硬件参考：

- [Amazon — 硬件链接 1](https://link.amazon/B05fkkBto)
- [Amazon — 硬件链接 2](https://link.amazon/B0eL8me5V)

## 编译固件

项目使用 Arduino-ESP32 **3.3.12**。手动配置时，README 当前列出的参数如下：

| 配置项 | 参数 |
| --- | --- |
| Board | `ESP32P4 Dev Module` |
| Chip variant | 根据芯片 Revision 选择 |
| Flash size | 32 MB |
| Partition scheme | `app3M_fat16M_16MB` |
| PSRAM | Enabled |
| USB mode | Hardware CDC/JTAG |
| CDC on boot | Enabled |

### 芯片 Revision 与编译目标

请先确认 ESP32-P4 芯片实际 Revision，再选择对应编译目标：

| 芯片 Revision | 编译参数 | 编译脚本中的标识 |
| --- | --- | --- |
| V1.X / REV1.X | `prev3` | `prev3` |
| V3.X / REV3.X | `postv3` | `postv3` |

不要仅根据商品标题或卖家描述判断芯片 Revision；应以实际芯片信息为准。

### 一键编译四种固件

Windows 环境安装并配置好 Arduino CLI、Arduino-ESP32 3.3.12 和 Python 后，在项目根目录运行：

```powershell
.\Compile-P4-Variants.cmd
```

编译脚本会依次生成以下四种组合：

1. Rev 3.x 英文版
2. Rev 1.x 英文版
3. Rev 3.x 简体中文版
4. Rev 1.x 简体中文版

中文版本会在独立的临时工作目录中，将中文 Dashboard 嵌入待编译副本；不会直接覆盖仓库中的英文 `dashboard_source.html`。

正式编译前可以先运行 Dry Run：

```powershell
.\Compile-P4-Variants.ps1 -DryRun
```

构建结果输出到 `Final-Build/`。中文固件文件名带有 `.zh-CN` 后缀；文件名同时包含 `REV1.X` 或 `REV3.X`，便于区分芯片版本。

> **分区参数需要注意：** 上表保留了项目 README 原有的 `app3M_fat16M_16MB` 参数；但当前 `Compile-P4-Variants.ps1` 自动编译脚本实际使用的是 `app3M_fat9M_16MB`。两者不一致。使用一键编译脚本时，以脚本中的参数为准；如果要手动编译，请先核对项目当前版本要求，不要直接混用。

## 安全提示

P4-CAN 涉及车辆 CAN 总线通信。部分功能可能发送或注入 CAN 报文，并影响车辆功能或控制行为。错误的车型配置、总线接线、GPIO 映射或固件版本都可能造成异常。

- 刷写前确认开发板型号、ESP32-P4 Revision 和固件变体相匹配。
- 首次使用前核对车辆配置、CAN 拓扑、收发器和 GPIO 接线。
- 先在受控台架环境中验证，不要在公共道路上测试实验性功能。
- 不要将实验性功能或本项目的测试结果视为 Tesla 官方支持或安全认证。

使用者应自行评估风险，并遵守当地法律法规。项目不保证适用于所有车辆、硬件修订或软件版本。

## 中文技术文档

- [FSD 可视化设置说明](FSD_SETTINGS.zh-CN.md)
- [SmartShift 自动换挡说明](SMARTSHIFT.zh-CN.md)
- [英文验证记录](VALIDATION.md)

## 支持项目

开发和维护该项目需要投入大量时间。如果项目对你有帮助，可以通过以下方式支持开发者：

- [Crypto 捐赠](https://tesla-mods.fkey.id/)
- [PayPal](https://www.paypal.com/donate/?hosted_button_id=Q2YMMMJYTAPJE)
- [Buy Me a Coffee](https://www.buymeacoffee.com/xbmod)

## Discord

[加入项目 Discord 社区](https://discord.gg/euPbYG8Npc)

## License

项目 README 声明采用 GNU GPL v3 或更高版本。不过当前 Fork 的仓库根目录未找到 `LICENSE` 文件，建议在发布或分发前补齐并核对正式许可证文本。
