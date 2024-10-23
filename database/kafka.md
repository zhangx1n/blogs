---
title: Kafka
time: 14:37
description: Kafka 基础
navbar: true
sidebar: true
footer: true
date: 2024-01-29
category: Article
author: Zhang Xin
next: true
tags:
  - Kafka
---
> 万字长文解析kafka：https://mp.weixin.qq.com/s/dOiNT0a_dRytwatzdrJNCg
>
> kafka日志存储：https://zhuanlan.zhihu.com/p/65415304

# 消息队列

用途：**不同服务server、进程process、线程thread**之间进行通信。

**使用消息队列的场景： **

 1. 异步处理： 短信通知、终端状态推送、app推送、用户注册等

    更快返回结果，减少等待，实现并发处理，提升系统总体性能。

 2. 流量控制：削峰

    秒杀场景下的下单状态。使用消息队列隔离网关和后端服务，以达到流量控制和保护后端服务的目的。

 3. 服务解耦

 4. 发布订阅

 5. 高并发缓冲

<img src="https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/image-20230615161253154.png" alt="image-20230615161253154" style="zoom:50%;" />

## kafka

使用消息队列的好处：

* 解耦:允许我们独立的扩展或修改队列两边的处理过程。
*  可恢复性:即使一个处理消息的进程挂掉，加入队列中的消息仍然可以在系统恢复后被处理。 
* 缓冲:有助于解决生产消息和消费消息的处理速度不一致的情况。 
* 灵活性&峰值处理能力:不会因为突发的超负荷的请求而完全崩溃，消息队列能够使关键组件顶住 突发的访问压力。
* 异步通信:消息队列允许用户把消息放入队列但不立即处理它。

## 架构

<img src="https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/image-20230615162048127.png" alt="image-20230615162048127" style="zoom:50%;" />

Kafka 存储的消息来自任意多被称为 Producer 生产者的进程。数据从而可以被发布到不同的 Topic 主题下的不同 Partition 分区。
在一个分区内，这些消息被索引并连同时间戳存储在一起。其它被称为 Consumer 消费者的进程可以从分区订阅消息。
 Kafka 运行在一个由一台或多台服务器组成的集群上，并且分区可以跨集群结点分布。

下面给出 Kafka 一些重要概念，让大家对 Kafka 有个整体的认识和感知，后面还会详细的解析每一个概 念的作用以及更深入的原理:

**Producer**:消息生产者，向 Kafka Broker 发消息的客户端。
 **Consumer**:消息消费者，从 Kafka Broker 取消息的客户端。
 **Consumer Group**:**消费者组(CG)**，消费者组内每个消费者负责消费不同分区的数据，提高消 费能力。一个分区只能由组内一个消费者消费，消费者组之间互不影响。所有的消费者都属于某个 消费者组，即消费者组是逻辑上的一个订阅者。
 **Broker**:**一台** **Kafka** **机器就是一个** **Broker**。一个集群(**kafka cluster**)由多个 Broker 组成。一个 Broker 可以容纳多个 Topic。
 **Topic**:可以理解为一个队列，Topic 将消息分类，生产者和消费者面向的是同一个 Topic。 **Partition**:为了实现扩展性，提高并发能力，一个非常大的 Topic 可以分布到多个 Broker (即服 务器)上，一个 Topic 可以分为多个 Partition，同一个topic在不同的分区的数据是不重复的，每 个 Partition 是一个有序的队列，其表现形式就是一个一个的文件夹。 **Replication**:每一个分区都有多个副本，副本的作用是做备胎。当主分区(Leader)故障的时候 会选择一个备胎(Follower)上位，成为Leader。在kafka中默认副本的最大数量是10个，且副本 的数量不能大于Broker的数量，follower和leader绝对是在不同的机器，同一机器对同一个分区也 只可能存放一个副本(包括自己)。
 **Message**:消息，每一条发送的消息主体。 **Leader**:每个分区多个副本的“主”副本，生产者发送数据的对象，以及消费者消费数据的对象，都 是 Leader。
 **Follower**:每个分区多个副本的“从”副本，实时从 Leader 中同步数据，保持和 Leader 数据的同 步。Leader 发生故障时，某个 Follower 还会成为新的 Leader。

**Offset:消费者消费的位置信息**，监控数据消费到什么位置，当消费者挂掉再重新恢复的时候，可 以从消费位置继续消费。
 **ZooKeeper**:Kafka 集群能够正常工作，需要依赖于 ZooKeeper，ZooKeeper 帮助 Kafka 存储和 管理集群信息。

### 工作流程

<img src="https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/image-20230615163015013.png" alt="image-20230615163015013" style="zoom:50%;" />

不同partition的offerset是独立的。

Kafka 中消息是以 Topic 进行分类的，生产者生产消息，消费者消费消息，面向的都是同一个 Topic。

Topic 是逻辑上的概念，而 Partition 是物理上的概念，**每个** **Partition** **对应于一个** **log** **文件**，该 log 文 件中存储的就是 Producer 生产的数据。

Producer 生产的数据会不断追加到该 log 文件末端，且每条数据都有自己的 Offset。

消费者组中的每个消费者，都会实时记录自己消费到了哪个 Offset，以便出错恢复时，从上次的位置继 续消费。
**日志默认在: /tmp/kafka-logs**

### 副本原理

**副本机制(****Replication****)**，也可以称之为备份机制，通常是指分布式系统在多台网络互联的机器上保

存有相同的数据拷贝。副本机制的好处在于:

1. **提供数据冗余**。在一部分节点宕机的时候，系统仍能继续工作(即提高可用性)。
2. 提供高伸缩性。支持扩大机器数量，从而可以支撑更高的**读请求量**，比如fastdfs、mongodb。

​	**kafka**是否支持通过副本机制提高读的请求量?**-》不支持这样的机制

3. 改善数据局部性。允许将数据放入与用户地理位置相近的地方，**从而降低系统延时。** **kafka****也不支**

**持。**

目前Kafka只实现了副本机制带来的第 1 个好处，即是提供数据冗余实现高可用性和高持久性。

在kafka生产环境中，每台 Broker 都可能保存有各个主题下不同分区的不同副本，因此，单个 Broker 上存有成百上千个副本的现象是非常正常的。

下图展示了一个有 3 台 Broker 的 Kafka 集群上的副本分布情况。从图中可以看到，主题 1 分区 0 的 3 个副本分散在 3 台 Broker 上，其他主题分区的副本也都散落在不同的 Broker 上，从而实现数据冗余。

<img src="https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/image-20230615164350539.png" alt="image-20230615164350539" style="zoom:50%;" />

<img src="https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/image-20230615164411337.png" alt="image-20230615164411337" style="zoom:50%;" />

1. 在 Kafka 中，副本分成两类:领导者副本(Leader Replica)和追随者副本(Follower Replica)。每个分区在创建时都要选举一个副本，称为领导者副本，其余的副本自动称为追随者 副本。

2. Kafka 副本机制中的追随者副本是不对外提供服务的，不同于Fastdfs、MongdoDB等。
3. 当领导者副本挂掉了，或领导者副本所在的 Broker 宕机时，Kafka 依托于 ZooKeeper 提供的监控 功能能够实时感知到，并立即开启新一轮的领导者选举，从追随者副本中选一个作为新的领导者。

​		老 Leader 副本重启回来后，只能作为追随者副本加入到集群中。

### 生产者

producer就是生产者，是数据的入口。Producer在写入数据的时候**永远的找leader**，不会直接将数据 写入follower。

<img src="https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/image-20230615164606380.png" alt="image-20230615164606380" style="zoom:50%;" />

#### **为什么分区-可以水平拓展**

kafka 的消息组织方式实际上是三级结构：主题-分区-消息。主题下的每条消息只会保存在某一个分区中而不会在多个分区中保存多份。

<img src="https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/image-20230615165057513.png" alt="image-20230615165057513" style="zoom:50%;" />

分区的作用主要**提供负载均衡的能力，能够实现系统的高伸缩性(Scalability)**。不同的分区能够被放置 到不同节点的机器上，而数据的读写操作也都是针对分区这个粒度而进行的，这样每个节点的机器都能 独立地执行各自分区的读写请求处理。这样，当性能不足的时候可以通过添**加新的节点机器来增加整体 系统的吞吐量**。

分区原则:我们需要将 Producer 发送的数据封装成一个 ProducerRecord 对象。 该对象需要指定一些参数:

topic:string 类型，NotNull。 partition:int 类型，可选。 timestamp:long 类型，可选。 key:string 类型，可选。 value:string 类型，可选。 headers:array 类型，Nullable。

#### 分区策略

所谓分区策略是决定生产者将消息发送到哪个分区的算法。Kafka 为我们提供了默认的分区策略，同时

它也支持你自定义分区策略。

1. **轮询策略**

   Round-robin 策略，即顺序分配。比如一个主题下有 3 个分区，那么第一条消息被发送到分区 0，第二 条被发送到分区 1，第三条被发送到分区 2，以此类推。当生产第 4 条消息时又会重新开始，即将其分 配到分区 0

2. **随机策略**

3. **按消息键保序策略-Key-ordering策略**

   Kafka 允许为每条消息定义消息键，简称为 Key。这个 Key 的作用非常大，它可以是一个有着明确业务 含义的字符串，比如客户代码、部门编号或是业务 ID 等;也可以用来表征消息元数据。特别是在 Kafka 不支持时间戳的年代，在一些场景中，工程师们都是直接将消息创建时间封装进 Key 里面的。一旦消息 被定义了 Key，那么你就可以保证**同一个** **Key** **的所有消息都进入到相同的分区里面**，由于每个分区下的 消息处理都是有顺序的，故这个策略被称为按消息键保序策略。

4. **默认分区规则**

   1. 指明 Partition 的情况下，直接将给定的 Value 作为 Partition 的值。
   2. 没有指明 Partition 但有 Key 的情况下，将 Key 的 Hash 值与分区数取余得到 Partition 值。
   3. 既没有 Partition 有没有 Key 的情况下，第一次调用时随机生成一个整数(后面每次调用都在这个

   整数上自增)，将这个值与可用的分区数取余，得到 Partition 值，也就是常说的Round-robin 策略

### 消费者

传统的消息队列模型的缺陷在于消息一旦被消费，就会从队列中被删除，而且只能被下游的一个 Consumer 消费。严格来说，这一点不算是缺陷，只能算是它的一个特性。但很显然，这种模型的伸缩 性(scalability)很差，因为下游的多个 Consumer 都要“抢”这个共享消息队列的消息。发布 / 订阅模型 倒是允许消息被多个 Consumer 消费，但它的问题也是伸缩性不高，因为每个订阅者都必须要订阅主题 的所有分区。这种全量订阅的方式既不灵活，也会影响消息的真实投递效果。

当 Consumer Group 订阅了多个主题后，组内的每个实例不要求一定要订阅主题的所有分区，它只会消 费部分分区中的消息。Consumer Group 之间彼此独立，互不影响，它们能够订阅相同的一组主题而互 不干涉。再加上 Broker 端的消息留存机制，Kafka 的 Consumer Group 完美地规避了上面提到的伸缩 性差的问题。可以这么说，Kafka 仅仅使用 Consumer Group 这一种机制，却同时实现了传统消息引擎 系统的两大模型:如果所有实例都属于同一个 Group，那么它实现的就是消息队列模型;如果所有实例 分别属于不同的 **Group，那么它实现的就是发布 / 订阅模型**。

#### 消费方式

Consumer 采用 Pull(拉取)模式从 Broker 中读取数据。

Pull 模式则可以根据 Consumer 的消费能力以适当的速率消费消息。Pull 模式不足之处是，如果 Kafka 没有数据，消费者可能会陷入循环中，一直返回空数据。

因为消费者从 Broker 主动拉取数据，需要维护一个长轮询，针对这一点， **Kafka** **的消费者在消费数据 时会传入一个时长参数** **timeout**。

如果当前没有数据可以消费，consumer会等待一段时间之后再返回，这但时间就是timeout。

#### 分区分配策略

一个 Consumer Group 中有多个 Consumer，一个 Topic 有多个 Partition，所以必然会涉及到 Partition 的分配问题，即确定哪个 Partition 由哪个 Consumer 来消费。

Kafka 有三种分配策略:

1. **RoundRobin**
2. **Range，默认为Range** 
3. Sticky

当消费者组内消费者发生变化时，会触发分区分配策略(方法重新分配)。 这里主要讲Range、RoundRobin。

* **Range（默认策略）**

  <img src="https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/image-20230615170606207.png" alt="image-20230615170606207" style="zoom:50%;" />

  Range 方式是按照主题来分的，不会产生轮询方式的消费混乱问题。

  假设我们有10个分区，3个消费者，排完序的分区将会是**0,1,2,3**,4,5,6,**7,8,9**;消费者线程排完序将会是 C1-0,C2-0,C3-0。然后将partitions的个数除于消费者线程的总数来决定每个消费者线程消费几个分区。 如果除不尽，那么前面几个消费者线程将会多消费一个分区。
   在我们的例子里面，

  **我们有10个分 区，3个消费者线程，** 10/3 = 3，而且除不尽，那么消费者线程 C1-0将会多消费一个分区 的结果看起来是这样的:
   C1-0 将消费 0, 1, 2, 3 分区
   C2-0将消费 4,5,6分区

  C3-0将消费 7,8,9分区

  **假如我们有2个主题(T1和T2)，分别有10**个分区，那么最后分区分配的结果看起来是这样的: C1-0 将消费 T1主题的 0, 1, 2, 3 分区以及 T2主题的 0, 1, 2, 3分区
   C2-0将消费 T1主题的 4,5,6分区以及 T2主题的 4,5,6分区
   C3-0将消费 T1主题的 7,8,9分区以及 T2主题的 7,8,9分区

  **可以看出，C1-0 **消费者线程比其他消费者线程多消费了2个分区，这就是**Range strategy**的一个很明 显的弊端

  即是Consumer0、Consumer1 同时订阅了主题 A 和 B，可能造成消息分配不对等问 题，当消费者组内订阅的主题越多，分区分配可能越不均衡。

* **RoundRobin**

  **RoundRobin** **轮询方式将分区所有作为一个整体进行** **Hash** **排序，**消费者组内分配分区个数最大差别为 1，是按照组来分的，可以解决多个消费者消费数据不均衡的问题。

  轮询分区策略是把所有partition和所有consumer线程都列出来，然后按照hashcode进行排序。最后通 过轮询算法分配partition给消费线程。如果所有consumer实例的订阅是相同的，那么partition会均匀 分布。

  在我们的例子里面，假如按照 hashCode排序完的topic-partitions组依次为**T1-5, T1-3, T1-0, T1-8**, T1- 2, T1-1, T1-4, T1-7, **T1-6, T1-9**，我们的消费者线程排序为C1-0,C1-1,C2-0,C2-1，最后分区分配的结果 为:
   C1-0将消费 T1-5,T1-2,T1-6分区;

  C1-1将消费 T1-3,T1-1,T1-9分区; C2-0将消费 T1-0,T1-4分区; C2-1将消费 T1-8,T1-7分区;

  但是，当消费者组内订阅不同主题时，可能造成消费混乱，如下图所示，**Consumer0** **订阅主题** **A****，** **Consumer1** **订阅主题** **B**。

<img src="https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/image-20230615171218698.png" alt="image-20230615171218698" style="zoom:50%;" />

将 A、B 主题的分区排序后分配给消费者组，TopicB 分区中的数据可能分配到 Consumer0 中。 使用轮询分区策略必须满足两个条件

1. **每个主题的消费者实例具有相同数量的流** 
2. **每个消费者订阅的主题必须是相同的**

#### 数据可靠性保证

为保证 Producer 发送的数据，能可靠地发送到指定的 Topic，Topic 的每个 Partition 收到 Producer

发送的数据后，都需要向 Producer 发送 ACK(ACKnowledge 确认收到)。 如果 Producer 收到 ACK，就会进行下一轮的发送，否则重新发送数据。