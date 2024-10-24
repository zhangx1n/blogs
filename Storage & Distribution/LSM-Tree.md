---
title: LSM-Tree 如何加速随机写
time: 14:37
description: lsm-tree 是一种非就地更新的数据结构
navbar: true
sidebar: true
footer: true
date: 2024-10-24
category: Article
author: Zhang Xin
next: true
tags:
  - storage
  - lsm-tree
---
# 引言

LSM-Tree(Log Structured Merge Tree),它是一种分层、有序、面向磁盘的数据结构。主要利用了磁盘批量的顺序写性能远胜于随机写的特性，对数据的操作均采用追加方式，不进行删除和更新。但是该设计在大大提升了写性能的同时降低了读性能。

---
# 写入

举个例子，我们要插入一条数据到LSM-Tree，那么执行 “put key1 bar”,该操作首先被写入磁盘的WAL日志中，该操作用于故障恢复，如果出现宕机就可以将内存中来不及写入磁盘的数据进行恢复从而确保了数据写入的可靠性。然后，将这个数据写入到内存中的MemTable，这个时候并不会去判断该key值是否已经存在，之后便可以回复用户写入成功。内存是有限的不可能不断写入，所以MemTable固定大小一般是32M，当MemTable写满之后，被转换为Immutable MemTable(只读MemTable)，然后创建一个空的MemTable继续写入数据，为什么使用Immutable MemTable呢？因为这样可以避免MemTable中的内存序列化到磁盘阻塞写操作。这个时候，有一个后台线程会不停地将Immutable MemTable复制到磁盘中并释放内存，每个Immutable MemTable对应于磁盘中的SSTable,SSTable,全称是sorted string table。它拥有一种持久化、有序且不可变的键值存储结构。它的key和value都是任意的字节数组。它内部包含一系列可配置大小的Block（默认大小一般是64k)。Block的索引存储在尾部,当SSTable打开时，索引被加载到内存。然后根据key在导入内存里面再进行二分查找，找到key对应的offset之后，然后去磁盘把相应的数据块读出来。这些SSTable文件，虽然每个文件中的key是有序的，但是文件之间完全完全无序遭成还是无法查找。这里SSTable巧妙地采用了**分层合并机制**来解决乱序的问题。啥意思？  
SSTable被分为很多了层，越往上层文件越少，越往底层文件越多。每一层的容量都有一个固定的上限值，一般来说，下一层的容量是上一层的10倍。当某一层写满了，就会触发后台线程往下一层合并，数据被合并到下一层之后，本层的SSTable文件就可以删除掉了。合并过程其实也是个排序过程，除了Level 0以外，每一层内的文件都是有序的，文件内的KV也是有序的，这样就便于查找了。  
这个合并步骤叫做Major Compaction,这个阶段会真正地清除掉被标记删除掉的数据以及多版本数据的合并，从而避免浪费空间。由于SSTable都是有序的，可以直接采用Merge Sort进行高效合并。  
所以，利用WAL确保数据写入的可靠性，只进行数据的追加不更新数据的特性，只要写入WAL和MemTable便认为数据已经写入成功，这样充分利用顺序写入提升了数据写入性能，同时又利用了分层合并机制提示了数据的查询性能。

# 读取
采用分层查找的方法。首先在内存中的MemTable和Immutable MemTable中查找，之后到磁盘的SSTable的每层进行查找，找到后直接返回。数据是根据这个路径追加的，因此按照这个路径就能查找到。这样的查找方式有可能由于需要多次进行内存和文件的查找才可以找到符合条件的key,但是这个分层结构越是被经常读写的热数据越靠上，对这样的key查找就很快。

## 读取优化
实际使用中，通常可以对读取操作进行下一步的优化，在内存中缓存SSTable文件的key,这样可以采用布隆过滤器进行加速查找。比如LevelDB中有个manifest文件，它记录了SSTable文件的一些关键信息，比如Level层数，文件名，最小key值，最大key值等，这个文件通常不大，完全可以放入内存。从而帮助快速定位要查询的SSTable文件。

# 删除
删除数据时并不是立即删除，而是记录下对这个key的操作操作做标记，只有当合并SSTable文件时才会真正地删除。