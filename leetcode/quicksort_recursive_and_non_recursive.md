---
title: 快速排序的 golang 实现
time: 14:37
description: 使用递归及非递归两种方式实现快速排序
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
快速排序（Quicksort）是一种高效的排序算法，采用分治法策略。以下是使用 Go 语言分别实现递归和非递归版本的快速排序。

---

## 递归实现

递归版本是快速排序的经典实现方式。它通过递归地对数组进行分区和排序。

```go
package main

import "fmt"

func quickSortRecursive(arr []int, low, high int) {
    if low < high {
        pi := partition(arr, low, high)

        // 递归地对左右子数组进行排序
        quickSortRecursive(arr, low, pi-1)
        quickSortRecursive(arr, pi+1, high)
    }
}

func partition(arr []int, low, high int) int {
    pivot := arr[high] // 选择最后一个元素作为基准点
    i := low - 1       // i 是较小元素的索引，当前已知的比基准点小的元素的最后一个位置

    for j := low; j < high; j++ {
        if arr[j] < pivot {
	        // i 左边的元素都是小于 pivot 的
            i++
            arr[i], arr[j] = arr[j], arr[i]
        }
    }

    // 将基准点移至正确的位置
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i + 1
}

func main() {
    arr := []int{10, 7, 8, 9, 1, 5}
    n := len(arr)
    quickSortRecursive(arr, 0, n-1)
    fmt.Println("Sorted array is:", arr)
}
```

**输出**：
```
Sorted array is: [1 5 7 8 9 10]
```

## 非递归实现

非递归（迭代）版本通过使用显式的栈来模拟递归调用，以避免函数调用栈的开销。

```go
package main

import "fmt"

func quickSortIterative(arr []int, low, high int) {
    stack := make([]int, high-low+1) // 创建一个栈

    top := -1
    top++
    stack[top] = low
    top++
    stack[top] = high

    for top >= 0 {
        high = stack[top]
        top--
        low = stack[top]
        top--

        p := partition(arr, low, high)

        if p-1 > low {
            top++
            stack[top] = low
            top++
            stack[top] = p - 1
        }

        if p+1 < high {
            top++
            stack[top] = p + 1
            top++
            stack[top] = high
        }
    }
}

func partition(arr []int, low, high int) int {
    pivot := arr[high] // 选择最后一个元素作为基准点
    i := low - 1       // i 是较小元素的索引

    for j := low; j < high; j++ {
        if arr[j] < pivot {
            i++
            arr[i], arr[j] = arr[j], arr[i]
        }
    }

    // 将基准点移至正确的位置
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i + 1
}

func main() {
    arr := []int{10, 7, 8, 9, 1, 5}
    n := len(arr)
    quickSortIterative(arr, 0, n-1)
    fmt.Println("Sorted array is:", arr)
}
```

**输出**：
```
Sorted array is: [1 5 7 8 9 10]
```

# 总结

- **递归实现**：代码简洁，容易理解，但对于大规模数据可能会导致栈溢出问题。
- **非递归实现**：通过显式的栈来模拟递归，避免了栈溢出的问题，但代码稍微复杂一些。

这两种方法在实际应用中都很常见，选择哪种方式可以根据具体的需求和场景来决定。
## 快速排序的最好和最坏时间复杂度是多少？如何计算的？

|算法|平均时间|最好时间|最坏时间|空间|
|---|---|---|---|---|
|快速排序|O(n * log(n))|O(n * log(n))|O(n^2)|O(log(n))|

除了快速排序，像插入排序，堆排序，桶排序的时间复杂度也是高频的面试题。那么怎么计算的呢？算法的时间复杂度等于所有子步骤的时间复杂度之和，快速排序的效率取决于数组划分是否平衡，即依赖于主元（pivot）的选择。最好的情况，假设主元每次都恰好是待排序数组的中位数，能够把待排序数组平衡地划分为两个相近长度的子数组。我们可以使用递归树的方法来计算。可以看到在每一次递归中，一方面数组长度变小，另一方面数组数量变多，但是每层的总时间复杂度和不变。（ n 为数组的长度）

|递归树|每层总时间|
|---|---|
|1. T(n)|O(n) （主元划分数组的时间）|
|2. T(n/2) T(n/2)|O(1/2 n) * 2 = O(n)|
|3. T(n/4) T(n/4) T(n/4) T(n/4)|O(1/4 n) * 4 = O(n)|

我们可以看到每一层划分数组的时间都为 O(n)，**这棵树共有 log(n) 层**，所以总的时间复杂度是 O(nlog(n))


##  如何优化快速排序？编程语言是如何实现快速排序的？

快速排序有着非常悠久的历史（1962年到今天），经过时代的变迁大家也研究出非常多的变形和优化方式，你需要有足够的好奇心才能把这个问题回答好，常见的方法包括

1. **随机化**

在快速排序最开始的时候先对数组进行随机化，**攻击者无法通过构造一种特殊的输入来触发快速排序的最坏情况。**

2. **混合排序**

插入排序的最佳时间复杂度是 O(n)，当数组长度少于一定长度的时候，我们可以使用插入排序。

3. **更聪明地选择主元**

有非常多选择的方法，例如中位数法，为了不要选到待排序数组的极值，可以选择该数组的首，中间，尾数字，然后取其中位数作为主元，

4. **双主元排序**

与单主元的本质思想是一样的，不过使用了双主元把待排序数组划分为三部分而不是两部分。

5. **实际应用**

Java 7 使用了双主元排序，Golang 的快速排序综合了 2，3，4 三种方法，在小数据的时候会使用插入排序以及希尔排序，为了避免大数据的栈溢出所以也使用了堆排序，一般的情况下，Golang 会使用双主元的快速排序。

# reference

https://zhuanlan.zhihu.com/p/267133203