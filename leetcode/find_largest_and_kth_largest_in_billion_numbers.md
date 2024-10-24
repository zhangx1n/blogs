---
title: 10亿个数中如何高效地找到最大的一个数以及最大的第 K 个数
time: 14:37
description: 10亿个数中如何高效地找到最大的一个数以及最大的第 K 个数
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
### 1. 寻找最大值

找到最大值是最简单的部分，只需要遍历数组一次，记录最大的值。

---

```go
package main

import "fmt"

func findMax(arr []int) int {
    max := arr[0]
    for _, v := range arr {
        if v > max {
            max = v
        }
    }
    return max
}

func main() {
    arr := []int{3, 2, 1, 5, 6, 4}
    max := findMax(arr)
    fmt.Println("Maximum:", max)
}
```

### 2. 寻找第 K 大的值

找到第 K 大的值需要更复杂的算法。可以使用**快速选择算法（Quickselect）**，这是一种基于快速排序思想的算法，可以在平均 O(n) 时间内找到第 K 大的元素。

```go
package main

import "fmt"

func partition(arr []int, left, right int) int {
    pivot := arr[right]
    i := left
    for j := left; j < right; j++ {
        if arr[j] > pivot {
            arr[i], arr[j] = arr[j], arr[i]
            i++
        }
    }
    arr[i], arr[right] = arr[right], arr[i]
    return i
}

func quickSelect(arr []int, left, right, k int) int {
    if left == right {
        return arr[left]
    }

    pivotIndex := partition(arr, left, right)
    if k == pivotIndex {
        return arr[k]
    } else if k < pivotIndex {
        return quickSelect(arr, left, pivotIndex-1, k)
    } else {
        return quickSelect(arr, pivotIndex+1, right, k)
    }
}

func findKthLargest(arr []int, k int) int {
    return quickSelect(arr, 0, len(arr)-1, k-1)
}

func main() {
    arr := []int{3, 2, 1, 5, 6, 4}
    k := 2
    kthLargest := findKthLargest(arr, k)
    fmt.Println("The", k, "th largest element is:", kthLargest)
}
```

### 3. 适应10亿个数的情况

对于10亿个数的问题，由于数组太大，可能无法直接全部加载到内存中。我们需要考虑以下两种策略：

- **分块处理**：将数据分成多个小块，分别处理每一块，然后在所有块的结果中找到最终的最大值或第 K 大的值。
- **流式处理**：使用堆（Heap）结构，只维护第 K 大的值集合。当处理流中的每一个元素时，更新堆中的值。

#### 使用小顶堆（Min-Heap）寻找第 K 大值

对于寻找第 K 大值，可以使用一个大小为 K 的最小堆。遍历整个数组，如果当前值大于堆顶元素，就替换堆顶元素并调整堆。

```go
package main

import (
    "container/heap"
    "fmt"
)

// 定义一个最小堆
type MinHeap []int

func (h MinHeap) Len() int           { return len(h) }
func (h MinHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h MinHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *MinHeap) Push(x interface{}) {
    *h = append(*h, x.(int))
}

func (h *MinHeap) Pop() interface{} {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[0 : n-1]
    return x
}

func findKthLargestUsingHeap(arr []int, k int) int {
    h := &MinHeap{}
    heap.Init(h)

    for _, num := range arr {
        if h.Len() < k {
            heap.Push(h, num)
        } else if num > (*h)[0] {
            heap.Pop(h)
            heap.Push(h, num)
        }
    }
    return (*h)[0]
}

func main() {
    arr := []int{3, 2, 1, 5, 6, 4}
    k := 2
    kthLargest := findKthLargestUsingHeap(arr, k)
    fmt.Println("The", k, "th largest element is:", kthLargest)
}
```

### 4. 总结

- **寻找最大值**可以通过简单的线性扫描实现，时间复杂度为 O(n)。
- **寻找第 K 大值**可以使用快速选择算法或者最小堆的方法：
  - 快速选择算法的平均时间复杂度为 O(n)。
  - 最小堆方法的时间复杂度为 O(n log K)，适合在内存有限的情况下使用。

这些算法都可以在 Go 语言中高效地处理大规模数据集。