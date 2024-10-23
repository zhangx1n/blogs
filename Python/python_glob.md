---
title: python glob 模块
time: 14:37
description: python glob 模块
navbar: true
sidebar: true
footer: true
date: 2024-03-29
category: Document
author: Zhang Xin
next: true
tags:
  - python
---
## glob 模块 （查找文件路径）

### 通配符：

- 通配符-星号`*`：星号`*`匹配一个文件名段中的0个或多个字符
- 单配符-问号`?`：问号`?`会匹配文件名中该位置的单个字符。
- 字符区间-`[a-z]`：使用字符区间`[a-z]`，可以匹配多个字符中的一个字符。

### 基本用法：

1. `glob.glob(pathname)`
     返回所有匹配的文件路径列表。它只有一个参数`pathname`，定义了文件路径匹配规则，这里可以是绝对路径，也可以是相对路径。
2. `glob.iglob(pathname)`,
     获取一个可编历对象，使用它可以逐个获取匹配的文件路径名。与`glob.glob()`的区别是：`glob.glob`同时获取所有的匹配路径，而`glob.iglob`一次只获取一个匹配路径。
     Eg:



```python
import glob 
  
print glob.glob(r'E:\*\*.doc') 
print glob.glob(r'.\*.py') 
  
f = glob.iglob(r'.\*.py') 
  
for py in f: 
    print py 
```



```bash
>>>
['E:\\test_file\\adplus.doc'] 
['.\\perfrom_test.py', '.\\pyTest.py', '.\\simulation_login.py', '.\\widget.py', '.\\__init__.py'] 
.\perfrom_test.py 
.\pyTest.py 
.\simulation_login.py 
.\widget.py 
.\__init__.py 
```

### 详解：

1. 通配符-星号`*`匹配一个文件名段中的0个或多个字符



```python
import glob
for name in glob.glob('tmp/*'):
    print name
```

这个模式会匹配所有的路径名，但是不会递归搜索到子目录。



```bash
>>> 
tmp\checklog_status.sh
tmp\check_Adwords_v1.2.sh
tmp\check_traffic.sh
tmp\cut_nginxlog_V1.2.sh
tmp\ip_conn.sh
tmp\ip_keepalive.sh
tmp\nagios使用手册.doc
tmp\nmap_ping
tmp\nrpe_install-1.3.sh
tmp\one
tmp\syn.sh
tmp\zabbix_agentd_2.0.10_win_V1.2.bat
tmp\zabbix_agentd_2.0.8_V1.3.sh
tmp\工作内容.doc
```

要列出子目录中的文件，必须把子目录包含在模式中。



```python
import glob
print 'Name explicitly:'
for name in glob.glob('tmp/one/*'):
    print '\t', name
print 'Name with wildcard:'
for name in glob.glob('tmp/*/*'):
    print '\t', name 
```

第一种情况显示列出子目录名，第二种情况则依赖一个通配符查找目录。



```bash
>>>
Name explicitly:
    tmp/one\another.txt
    tmp/one\file.txt
Name with wildcard:
    tmp\one\another.txt
    tmp\one\file.txt
```

1. 单配符-问号`?`：问号`?`会匹配文件名中该位置的单个字符。



```python
import glob
for name in glob.glob('tmp/chec?_traffic.sh'):
    print name
```



```bash
>>> 
tmp\check_traffic.sh
```

1. 字符区间-`[a-z]`：使用字符区间`[a-z]`，可以匹配多个字符中的一个字符。



```python
import glob
for name in glob.glob('tmp/one/[a-z]*'):
    print name
```

区间可以匹配所有小写字母。



```bash
>>> 
tmp/one\another.txt
tmp/one\file.txt
```



作者：DexterLei
链接：https://www.jianshu.com/p/542e55b29324
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。