---
title: K个一组翻转链表
time: 14:37
description: K个一组翻转链表
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
# 题目  
  
给你链表的头节点 `head` ，每 `k` 个节点一组进行翻转，请你返回修改后的链表。

`k` 是一个正整数，它的值小于或等于链表的长度。如果节点总数不是 `k` 的整数倍，那么请将最后剩余的节点保持原有顺序。

你不能只是单纯的改变节点内部的值，而是需要实际进行节点交换。
  
Example:  
  
```c  
Given this linked list: 1->2->3->4->5  
  
For k = 2, you should return: 2->1->4->3->5  
  
For k = 3, you should return: 3->2->1->4->5  
```  
  
  
# 解题思路  
  
这一题是 problem 24 的加强版，problem 24 是两两相邻的元素，翻转链表。而 problem 25 要求的是 k 个相邻的元素，翻转链表，problem 相当于是 k = 2 的特殊情况。

```go
func reverseKGroup(head *ListNode, k int) *ListNode {  
    node := head  
    // 检查是否有足够的节点来进行反转  
    for i := 0; i < k; i++ {  
       if node == nil {  
          return head // 不足 k 个节点，不反转，直接返回原链表  
       }  
       node = node.Next  
    }  
  
    // 反转 head 到 node 之间的 k 个节点  
    newHead := reverse1(head, node)  
  
    // 递归反转后续部分，并将 head 的 Next 指向下一部分反转后的头节点  
    head.Next = reverseKGroup1(node, k)  
    return newHead 
}  
  
func reverse(head, tail *ListNode) *ListNode {  
    var pre, cur, next *ListNode  
    cur = head  
    // 反转直到 cur 到达 tail    for cur != tail {  
       next = cur.Next  
       cur.Next = pre  
       pre = cur  
       cur = next  
    }  
    // pre 是反转后的新头节点  
    return pre  
}
```