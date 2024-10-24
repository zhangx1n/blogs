---
title: 无重复字符的最长子串
time: 14:37
description: 无重复字符的最长子串
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
## 题目  

给定一个字符串 `s` ，请你找出其中不含有重复字符的 **最长子串** 的长度。

---
Example 1:  
  
```c  
Input: "abcabcbb"  
Output: 3 Explanation: The answer is "abc", with the length of 3. 
```  
  
Example 2:  
  
```c
Input: "bbbbb"  
Output: 1  
Explanation: The answer is "b", with the length of 1.  
```  
  
Example 3:  
  
```c  
Input: "pwwkew"  
Output: 3  
Explanation: The answer is "wke", with the length of 3.   
             Note that the answer must be a substring, "pwke" is a subsequence and not a substring.  
```  
  
  
## 解题思路  
  
这一题和第 438 题，第 3 题，第 76 题，第 567 题类似，用的思想都是"滑动窗口"。  
  
滑动窗口的右边界不断的右移，只要没有重复的字符，就持续向右扩大窗口边界。一旦出现了重复字符，就需要缩小左边界，直到重复的字符移出了左边界，然后继续移动滑动窗口的右边界。以此类推，每次移动需要计算当前长度，并判断是否需要更新最大长度，最终最大的值就是题目中的所求。
1. 使用滑动窗口法，左指针 left 和右指针 right。
2. 用 map 记录每个字符最后出现的位置。
3. 遍历字符串，不断更新右指针。
4. 如果遇到重复字符，更新左指针为该字符上次出现位置的下一个位置。
5. 每次迭代更新最长子串长度。
6. 返回最终的最长子串长度。

```go
func lengthOfLongestSubstring(s string) int {  
    dict := make(map[byte]int)  
    ans := 0  
    left := -1  
    for right, _ := range s {  
       if val, ok := dict[s[right]]; ok {  
          // 更新左指针  
          left = max(left, val)  
       }  
       // Hash 表中更新为最新的下标  
       dict[s[right]] = right  
       ans = max(ans, right-left)  
    }  
    return ans  
}
```

时间复杂度为 O(n)，空间复杂度为 O(min(m,n))，其中 n 是字符串长度，m 是字符集大小。