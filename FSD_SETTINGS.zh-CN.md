# FSD 可视化（实验性功能）

## 设置项

设置页面包含三个控制项：

1. **启用 FSD 注入（Enable FSD injections）**
2. **AP 期间暂停 FSD（Suspend FSD during AP）**
3. **启用 FSD 可视化（Enable "FSD Visualisation"）**

最后一个开关用于选择 `UI_enableFullSelfDriving` 的原始值：

- `1`：开启（ON）
- `0`：关闭（OFF）

该值写入 CHASSIS 总线报文 `0x3FD` 的 MUX0 bit46。

关闭主开关后，FSD 回显会停止。原始 bit46 读回值仍会显示。此功能不会发送 FSD MUX2 回显，也不会修改其他 FSD 字段。共享的 TLSSC 组合逻辑和现有传输门控仍然有效。

## 配置保存

三个设置均保存在 `features/fsd` 中。

加载配置时，旧版本中额外的信号位和路由位会被忽略。新保存的数据只保留以下内容：

- 标记位（marker）
- 主开关状态
- AP 期间暂停选项
- bit46 选择值

旧配置值会通过掩码处理，仅保留 bit1。

启用“AP 期间暂停”后，如果 AP 状态未知或数据已过期，系统会阻止 FSD；当系统收到新鲜的手动驾驶状态后，才会恢复。

## API

### 获取状态

`GET /api/fsd/stats`

返回值包括：

- `values`：`0` 或 `2`
- `stock1`：原始 bit46 读回值

### 更新设置

`POST /api/fsd/update`

请求必须包含：

- `enabled`
- `values`（`0` 或 `2`）

可选字段：

- `suspendDuringAp`

### S3XY 按键

S3XY 动作 **FSD Visualisation** 会切换已保存的主开关状态，同时保留另外两个设置。
