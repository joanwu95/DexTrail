---
title: Sudo R1 · 已收录的机器人系统
hide: [navigation, toc, footer]
---

<div class="dex-hand-page" markdown="1">

<header class="hand-brand"><a class="hand-brand-name" href="../.."><svg class="dex-emblem" viewBox="0 0 52 52" aria-hidden="true"><path d="M10 39C4 18 14 8 25 8c15 0 22 13 16 27M17 42C8 18 21 10 31 17c7 5 7 13 3 23M24 44c-8-14-9-23 0-23 8 0 5 10 5 16"/><circle cx="41" cy="35" r="3"/></svg>DexTrail<span>.</span></a><a class="hand-back" href="../..">← 返回产品地图</a></header>

<div class="hand-heading"><h1>Sudo R1</h1><p class="hand-identity">苏度 · Sudo Robotics · 2026 官方系统介绍</p><span class="hand-status">已收录 · 系统档案</span></div>

<section class="sudo-media" data-sudo-videos data-player="../../javascripts/vendor/hls.min.js" aria-label="Sudo R1 官网视频">
<div class="sudo-player"><video controls playsinline preload="none" aria-label="Sudo R1 官方视频播放器"></video><button class="sudo-play" type="button">播放官网视频</button></div>
<div class="sudo-video-heading"><h2 class="sudo-video-title">系统演示</h2><a href="https://www.sudo.ai/" target="_blank" rel="noopener">官网出处 ↗</a></div>
<p class="sudo-video-description">官网开篇的 R1 系统视频。</p>
<p class="sudo-video-status" role="status">点击播放；视频直接来自苏度官网，不使用替代图片。</p>
<nav class="sudo-video-picker" aria-label="选择官网视频">
<button type="button" data-stream="https://assets.sudo.ai/public/videos/bf4a220b37f0/figure_1-1-2/master.m3u8" data-description="官网开篇的 R1 系统视频。" aria-pressed="true">系统演示</button>
<button type="button" data-stream="https://assets.sudo.ai/public/videos/bf4a220b37f0/figure_6-1/master.m3u8" data-description="官网连续评估视频；完整任务和成功率口径见原文。" aria-pressed="false">60 分钟连续评估</button>
<button type="button" data-stream="https://assets.sudo.ai/public/videos/bf4a220b37f0/figure_3-4-1/master.m3u8" data-description="官网不同视觉条件下的抓取演示之一。" aria-pressed="false">不同光照与背景</button>
<button type="button" data-stream="https://assets.sudo.ai/public/videos/bf4a220b37f0/figure_3-1-1/master.m3u8" data-description="官网任务中施加干扰的演示之一。" aria-pressed="false">外界干扰与闭环响应</button>
<button type="button" data-stream="https://assets.sudo.ai/public/videos/bf4a220b37f0/figure_5-1-1/master.m3u8" data-description="官网受限空间中接近目标的演示之一。" aria-pressed="false">障碍与受限空间</button>
<button type="button" data-stream="https://assets.sudo.ai/public/videos/bf4a220b37f0/figure_4-1-1/master.m3u8" data-description="官网杂乱物体条件下的抓取演示之一。" aria-pressed="false">杂乱物体抓取</button>
<button type="button" data-stream="https://assets.sudo.ai/public/videos/bf4a220b37f0/figure_7-3-1/master.m3u8" data-description="官网 Why Simulation 章节中的仿真视频，不标作真实硬件演示。" aria-pressed="false">仿真演示</button>
</nav>
<noscript><p>播放器需要 JavaScript。<a href="https://www.sudo.ai/">在官网观看视频</a>。</p></noscript>
</section>

## 它与灵巧手地图的关系

Sudo 官网介绍的是**自研软硬件与操作模型集成的 R1 系统**。截至本次核查，页面没有列出可分别核对的多款灵巧手型号、逐指自由度和手部规格书。本档案已经加入首页地图，按“机器人系统”标记，搜索 Sudo 或苏度即可找到。公开时间视图按 2026 年官方介绍定位；自由度和传动视图列在“已收录 · 坐标待核”中，不计入 64 款手本体，也不根据画面推定末端型号。[官方介绍](https://www.sudo.ai/)

## 硬件、SDK 与模型公开情况

| 维度 | 已知内容 | 当前边界 |
| --- | --- | --- |
| 硬件 | 官方声明为自研软硬件集成系统 | 未取得独立手部型号、驱动数、接线及供电资料 |
| SDK / API | 官网展示系统运行 | 未找到可核查的公开 SDK、控制 API、OS 支持表或版本说明 |
| 训练 | 官方称只使用仿真数据训练 | 不等于已经公开训练数据、仿真器或训练代码 |
| CAD / URDF / MJCF / USD | 本轮未确认公开下载 | 不标成支持或不支持某个模拟器 |
| 操作模型权重 | 本轮未确认公开权重 | 不把演示系统称为可本地部署的开源模型 |
| 本机验证 | 未连接硬件、未运行模型 | 此页为文档核查记录 |

以上状态依据本轮读取的[官网页面及资源入口](https://www.sudo.ai/)，不是对未公开产品的判断。核查日期：2026-10-02。

## 演示说明了什么

官网提供约一小时连续抓取演示，报告在其测试设置下首试成功率约 98%，两次内接近 100%；还描述每次观察后以 15–25 Hz 更新动作。它们属于**厂商报告的整套系统表现**，包含机械臂、末端、感知与策略的共同作用，不能当作某一款手本体的独立性能。[演示与指标定义](https://www.sudo.ai/)

## 后续需要补齐

独立手型号和修订号、机械与传感参数、开发接口、模型和权重的获取方式、许可，以及可复现的任务协议。如后续公开了独立手部型号，再单独建立手部档案并与本系统链接；不影响当前 R1 系统档案的已收录状态。

</div>
