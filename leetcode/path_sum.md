---
title: 路径总和
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
  - leetcode
---
> [113. Path Sum II](https://leetcode.cn/problems/path-sum-ii/)

```go
 func pathSum(root *TreeNode, targetSum int) [][]int {  
    result := make([][]int, 0)  
    traverse(root, &result, new([]int), targetSum)  
    return result  
}  
  
func traverse(node *TreeNode, result *[][]int, currPath *[]int, targetSum int) {  
    if node == nil { // 这个判空也可以挪到递归遍历左右子树时去判断  
        return  
    }  
  
    targetSum -= node.Val // 将targetSum在遍历每层的时候都减去本层节点的值  
    *currPath = append(*currPath, node.Val) // 把当前节点放到路径记录里  
  
    if node.Left == nil && node.Right == nil && targetSum == 0 { // 如果剩余的targetSum为0, 则正好就是符合的结果  
        // 不能直接将currPath放到result里面, 因为currPath是共享的, 每次遍历子树时都会被修改  
        pathCopy := make([]int, len(*currPath))  
        for i, element := range *currPath {  
            pathCopy[i] = element  
        }  
        *result = append(*result, pathCopy) // 将副本放到结果集里  
    }  
  
    traverse(node.Left, result, currPath, targetSum)  
    traverse(node.Right, result, currPath, targetSum)  
    *currPath = (*currPath)[:len(*currPath)-1] // 当前节点遍历完成, 从路径记录里删除掉  
}
```