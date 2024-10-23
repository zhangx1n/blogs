---
title: 岛屿数量
time: 14:37
description: 岛屿数量
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
  
给你一个由 `'1'`（陆地）和 `'0'`（水）组成的的二维网格，请你计算网格中岛屿的数量。

岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。

此外，你可以假设该网格的四条边均被水包围。
  
**Example 1:**  
  
    Input:    11110    11010    11000    00000        Output: 1  
  
**Example 2:**  
  
    Input:    11000    11000    00100    00011        Output: 3  
  
  
# 解题思路  
  
- 要求找出地图中的孤岛。孤岛的含义是四周被海水包围的岛。  
- 这一题可以按照第 79 题的思路进行搜索，只要找到为 "1" 的岛以后，从这里开始搜索这周连通的陆地，也都标识上访问过。每次遇到新的 "1" 且没有访问过，就相当于遇到了新的岛屿了。
```go
var dir = [][]int{  
    {-1, 0},  
    {0, 1},  
    {1, 0},  
    {0, -1},  
}  
  
func numIslands(grid [][]byte) int {  
    m := len(grid)  
    if m == 0 {  
       return 0  
    }  
    n := len(grid[0])  
    if n == 0 {  
       return 0  
    }  
    res, visited := 0, make([][]bool, m)  
    for i := 0; i < m; i++ {  
       visited[i] = make([]bool, n)  
    }  
    for i := 0; i < m; i++ {  
       for j := 0; j < n; j++ {  
          if grid[i][j] == '1' && !visited[i][j] {  
             searchIslands(grid, &visited, i, j)  
             res++  
          }  
       }  
    }  
    return res  
}  
  
func searchIslands(grid [][]byte, visited *[][]bool, x, y int) {  
    (*visited)[x][y] = true  
    for i := 0; i < 4; i++ {  
       nx := x + dir[i][0]  
       ny := y + dir[i][1]  
       if isInBoard(grid, nx, ny) && !(*visited)[nx][ny] && grid[nx][ny] == '1' {  
          searchIslands(grid, visited, nx, ny)  
       }  
    }  
}  
  
func isInBoard(board [][]byte, x, y int) bool {  
    return x >= 0 && x < len(board) && y >= 0 && y < len(board[0])  
}
```
