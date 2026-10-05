# 硬件、SDK 与模型支持整理（2026-10-02）

64 个地图档案均增加固定支持栏目。数据在 `data/platform-support.json`，由 `scripts/build-platform-support.py` 维护并生成；修改维护脚本后运行 `.venv/Scripts/python.exe scripts/build-platform-support.py`。页面由 `website/hooks/product_details.py` 渲染。

## 每款手记录的内容

- 硬件版本、驱动结构、接入条件及来源。
- SDK 的语言、环境、控制和状态接口、单位、固件匹配、许可及来源。
- CAD、URDF/Xacro、MuJoCo/MJCF、Isaac、Gazebo、其他仿真或学习模型的版本和入口。
- 区分官方、作者、第三方资源；有入口、需申请、未核实、入口失效分别记录。

支持栏目覆盖所有档案，不等于所有字段都已经找到公开资料。没有运行实物、编译 SDK 或加载模型；未核实不能解读为不支持。原有逐款研究来源继续保留，新增核查来源写在字段旁。

## 新增与重点纠正

- [Xynova Prima 1](https://www.xynova.com.cn/en/xynova-prima-1)：新增正式档案，与 Flex 2 同时可在地图搜索“曦诺”。官网总自由度与主动关节数量不混用；上市日期尚未找到，以当前官方存在证据标注时间上界。
- [苏度 R1](https://www.sudo.ai/)：官网介绍自研软硬件机器人系统，但本轮未找到独立灵巧手型号表、关节指标或下载包。新增 `/systems/sudo-r1/`，首页搜索“苏度 / sudo”提供入口，不虚构多款手或坐标参数。
- Allegro V3 仿真模型不当作 V4 精确对应；Wuji 不混用 A00/A01；Linker 按 L6/O6/L20/L30/O30 单独记录。
- RBO Hand 2 的公开 FEM 是单个 PneuFlex 执行器模型，不是整手 MuJoCo 模型。
- LEAP v1 CAD 是带 CC BY-NC-SA 条款的申请入口，不能根据 API 的 MIT 许可推断 CAD 也为 MIT。

## 页面布局

首页与产品详情取消固定最大内容宽度，两侧改用随屏幕调整的小边距。模型矩阵使用可用宽度，长段落仍限制行长。

## 验证

数据一致性测试覆盖 64 款手及每款 6 类模型字段；静态站点严格构建。浏览器核查详情支持栏目、曦诺搜索与苏度系统入口。实际硬件和仿真运行留待单独验证。
