---
title: 缺失的第一个正数
time: 14:37
description: 缺失的第一个正数
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
  
给你一个未排序的整数数组 `nums` ，请你找出其中没有出现的最小的正整数。

请你实现时间复杂度为 `O(n)` 并且只使用常数级别额外空间的解决方案。

---
Example 1:    
  
```  
Input: [1,2,0]  Output: 3  
```  
  
Example 2:    
  
```  
Input: [3,4,-1,1]  Output: 2  
```  
  
Example 3:    
  
```  
Input: [7,8,9,11,12]  Output: 1  
```  

  
# 解题思路  
  
如果可以使用 O(n)的空间复杂度，可以把 input 数组都装到 map 中，然后 i 循环从 1 开始，依次比对 map 中是否存在 i，只要不存在 i 就立即返回结果，即所求。
```go
func firstMissingPositive(nums []int) int {  
    numMap := make(map[int]int, len(nums))  
    for _, v := range nums {  
       numMap[v] = v  
    }  
    for index := 1; index < len(nums)+1; index++ {  
       if _, ok := numMap[index]; !ok {  
          return index  
       }  
    }  
    return len(nums) + 1  
}
```

## 常数空间复杂度解决方案

1. nums 数组的长度是n, 那么如果有缺失的最小的正整数一定是在`[1, n]`这个区间，如果不在，那么缺失的最小的正整数就是`n+1`。
2. 那么只需要给 nums中的数字放到正确的位置上，1 放到位置 0...n放到位置 n-1.
![|800](https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/202410161539579.png)
```go
func firstMissingPositive1(nums []int) int {  
    n := len(nums)  
    for i, num := range nums {  
       if num <= 0 {  
          nums[i] = n + 1  
       }  
    }  
    for _, num := range nums {  
       num := abs(num)  
       if num <= n {  
          nums[num-1] = -abs(nums[num-1])  
       }  
    }  
    for i, num := range nums {  
       if num > 0 {  
          return i + 1  
       }  
    }  
    return n + 1  
}  
  
func abs(x int) int {  
    if x < 0 {  
       return -x  
    }  
    return x  
}
```

>需要注意的是要使用 abs， 因为在修改为`-nums[num-1]` 后就出现了负数。 

