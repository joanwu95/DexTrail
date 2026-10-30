# RobotEra XHAND 1

<!-- hand-fact-review-2026-10-30 -->

## 研发机构与技术参数复核

复核日期：2026-10-30。适用范围：官方 XHAND 1 产品页。国家按研发机构所在地记录；联合研发分别列出，不作为制造地声明。

| 项目 | 已核实内容与适用条件 | 来源 / 阅读位置 |
| --- | --- | --- |
| 研发机构 | 北京星动纪元 · RobotEra | [官方规格 / 原始论文](https://www.robotera.com/#/product/XHAND) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 国家 / 地区（机构所在地） | 中国 | [官方规格 / 原始论文](https://www.robotera.com/#/product/XHAND) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 手指数 | 5 | [官方规格 / 原始论文](https://www.robotera.com/#/product/XHAND) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 自由度与计数范围 | 五指 12 主动自由度、0 被动自由度；拇指与食指各 3，其余三指各 2。不含 Lite 或 Pro。 | [官方规格 / 原始论文](https://www.robotera.com/#/product/XHAND) · 型号介绍、技术规格表或论文机构与硬件设计章节 |
| 执行器 | 12（该版本执行器计数） | [官方规格 / 原始论文](https://www.robotera.com/#/product/XHAND) · 型号介绍、技术规格表或论文机构与硬件设计章节 |

## 本次仍未取得的版本资料

- 结构材料 / 具体部位：已检查所列来源，尚未取得可对应本版本的明确值。

本次为文档与文件资料复核，未进行实物测量、SDK 编译或仿真运行。

<!-- /hand-fact-review -->

<!-- dexterous-expansion-03 -->

核对日期：2026-10-02；收录范围：官方 XHAND 1 产品页。记录为部分核验，未知项见各节。

## 平台与版本

北京星动纪元 · RobotEra。五指 12 主动自由度、0 被动自由度；拇指与食指各 3，其余三指各 2。不含 Lite 或 Pro。 [原始依据](https://www.robotera.com/#/product/XHAND)

## 感知系统

官网列五指各 120 点的环绕触觉阵列，输出法向力、切向力和温度等；关节反馈另含位置、速度、温度、电流。电流用于力矩相关控制，不等同直接测得指尖接触力。 [原始依据](https://www.robotera.com/#/product/XHAND)

## 工程优势与适用边界

工程解释：齿轮和电机集成于手部减少外部腱传动维护；传动摩擦、回差以及触觉标定仍应实测。厂商“全直驱”的叫法不用于替代机构分类。 [原始依据](https://www.robotera.com/#/product/XHAND)

## 待核验内容

精确首次公开日期、逐轴运动范围、固件与 SDK 二进制对应关系、触觉标定及任务重复测试待核。

## 来源索引

- [官方 XHAND 1 产品页 · 结构、感知与实验依据](https://www.robotera.com/#/product/XHAND)
- [官方规格 PDF](https://www.robotera.com/upload/goods/20241208/2ab64afaae0098db948e9d4063951c28.pdf)
- [厂商 STAR1 整机 URDF](https://github.com/roboterax/models)
- [IIT / robotology 的 XHand1 YARP 接入](https://github.com/robotology/yarp-device-xhand)
