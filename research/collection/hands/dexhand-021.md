# DexHand 021 · 五指版

<!-- dexterous-expansion-03 -->

核对日期：2026-10-02；收录范围：2025 结构与控制论文。记录为部分核验，未知项见各节。

## 平台与版本

DexRobot / 上海交通大学。五指，12 主动 + 7 被动自由度，12 电机；本页按 2025 论文配置，不混用 021S 三指版。 [原始依据](https://arxiv.org/html/2511.03481v1)

## 感知系统

Hall 传感器读关节角，指端电容触觉测接触。论文另用电流、位置、速度和温度训练关节力矩估计；这是模型估计，与指尖触觉实测是两套信息。 [原始依据](https://arxiv.org/html/2511.03481v1)

## 工程优势与适用边界

工程解释：较少驱动控制更多关节可减轻集成负担，但耦合关节无法任意独立设角。腱摩擦与温度变化会影响力矩估计的迁移，需在目标工况验证。 [原始依据](https://arxiv.org/html/2511.03481v1)

## 待核验内容

七个被动轴的逐指归属、硬件修订与模型版本、独立实验及耐久测试协议待补。

## 来源索引

- [2025 结构与控制论文 · 结构、感知与实验依据](https://arxiv.org/html/2511.03481v1)
- [官方 C++ SDK 与五指版本说明](https://github.com/DexRobot/dexhand_sdk_cpp)
- [官方 MuJoCo 型号与碰撞模型](https://dexrobot.github.io/dexrobot_mujoco/hand_models/index.html)
- [官方 URDF](https://dexrobot.github.io/dexrobot_urdf/)
