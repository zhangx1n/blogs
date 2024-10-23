---
title: io_uring 使用
time: 14:37
description: io_uring 基础
navbar: true
sidebar: true
footer: true
date: 2024-01-29
category: Article
author: Zhang Xin
next: true
tags:
  - Linux
  - io_uring
---
# io_uring: 高性能异步框架

https://zhuanlan.zhihu.com/p/608787533

## 原理及核心数据结构：SQ/CQ/SQE/CQE

Io_uring 利用 mmap 开辟出一块空间，让用户态和内核态的程序都可以共享的一块区域

- **提交队列**：submission queue (SQ)
- **完成队列**：completion queue (CQ)

<img src="https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/image-20230601150201557.png" alt="image-20230601150201557" style="zoom: 50%;" />

这两个队列：

- 都是**单生产者、单消费者**，size 是 2 的幂次；
- 提供**无锁接口**（lock-less access interface），内部使用 **内存屏障**做同步（coordinated with memory barriers）。

**使用方式**：

- 请求
  - 应用创建 SQ entries (SQE)，更新 SQ tail；
  - 内核消费 SQE，更新 SQ head。
- 完成
  - 内核为完成的一个或多个请求创建 CQ entries (CQE)，更新 CQ tail；
  - 应用消费 CQE，更新 CQ head。
  - 完成事件（completion events）可能以任意顺序到达，到总是与特定的 SQE 相关联的。
  - 消费 CQE 过程无需切换到内核态。