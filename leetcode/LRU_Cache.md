---
title: LRU Cache
time: 14:37
description: LRU Cache
navbar: true
sidebar: true
footer: true
date: 2024-01-29
category: Article
author: Zhang Xin
next: true
tags:
  - leetcode
---
> Leetcode: https://leetcode.cn/problems/lru-cache/description/


# [146. LRU 缓存](https://leetcode.cn/problems/lru-cache/)


## 问题描述

请你设计并实现一个满足  [LRU (最近最少使用) 缓存](https://baike.baidu.com/item/LRU) 约束的数据结构。

实现 `LRUCache` 类：

- `LRUCache(int capacity)` 以 **正整数** 作为容量 `capacity` 初始化 LRU 缓存
- `int get(int key)` 如果关键字 `key` 存在于缓存中，则返回关键字的值，否则返回 `-1` 。
- `void put(int key, int value)` 如果关键字 `key` 已经存在，则变更其数据值 `value` ；如果不存在，则向缓存中插入该组 `key-value` 。如果插入操作导致关键字数量超过 `capacity` ，则应该 **逐出** 最久未使用的关键字。

函数 `get` 和 `put` 必须以 `O(1)` 的平均时间复杂度运行。

---
## 解法

```go
type node struct {  
    k, v int  
}  
  
type LRUCache struct {  
    capacity int  
    // 链表，新使用的插入队头。  
    mlist *list.List  
    // 记录每一项使用的频率，map[]int  
    mmap map[int]*list.Element  
}  
  
func Constructor(capacity int) LRUCache {  
    return LRUCache{  
       capacity: capacity,  
       mlist:    list.New(),  
       mmap:     make(map[int]*list.Element),  
    }  
  
}  
  
func (this *LRUCache) Get(key int) int {  
    if v, ok := this.mmap[key]; ok {  
       this.mlist.MoveToFront(v)  
       return v.Value.(*node).v  
    }  
    return -1  
}  
  
func (this *LRUCache) Put(key int, value int) {  
    if v, ok := this.mmap[key]; ok {  
       this.mlist.MoveToFront(v)  
       v.Value.(*node).v = value  
    } else {  
       if this.mlist.Len() == this.capacity {  
          old := this.mlist.Back()  
          delete(this.mmap, old.Value.(*node).k)  
          this.mlist.Remove(old)  
       }  
       newNode := new(node)  
       *newNode = node{k: key, v: value}  
       newElem := this.mlist.PushFront(newNode)  
       this.mmap[key] = newElem  
  
    }  
  
}
```

