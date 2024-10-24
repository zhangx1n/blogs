---
title: 函数的堆栈调用过程
time: 14:37
description: 函数的堆栈调用过程
navbar: true
sidebar: true
footer: true
date: 2024-01-29
category: Article
author: Zhang Xin
next: true
tags:
  - cpp
---
# 引言

在现代程序开发中，理解函数调用栈的工作原理是非常重要的，尤其在调试和优化代码时。函数的调用不仅是一个逻辑的执行过程，它背后还涉及到内存管理、寄存器操作、汇编指令的生成以及栈帧的动态维护。通过分析函数调用栈，开发者能够深入了解程序的底层运行机制，识别并解决性能瓶颈或潜在的错误。下面，我们通过一个简单的 C++ 代码示例，从汇编指令的角度详细解读函数的调用过程

---
```cpp
#include<iostream>
 
int sum(int a, int b)
{
	int tmp = 0;
	tmp = a + b;
	return tmp;
}
 
int main()
{
	int a = 10;
	int b = 20;
	int ret = sum(a, b);
	std::cout << ret << std::endl;
	return 0;
}
```

* main函数调用sum函数，sum函数执行完以后，怎么知道回到哪个函数？

* sum函数执行完，回到main以后，怎么知道从哪一行指令继续运行呢？

下面我们就来看一下函数调用栈的具体过程：

![img](https://img-blog.csdnimg.cn/20200310202640774.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoaW5QaWthY2h1,size_16,color_FFFFFF,t_70)

首先，内存会为main函数开辟一块空间来当做main函数的栈帧，其中esp寄存器存放当前函数栈顶的地址，即main函数栈顶的地址，而ebp寄存器存放当前函数栈底的地址，即main函数栈底的地址。

当执行

```
int a = 10;
```

会生成 `mov dword ptr [a],0Ch`  这样一条汇编指令，其中 dword代表双字，就是4个字节，ptr 代表指针，[]里的数据是一个地址，这个地址指向一个双字型数据，所以这条汇编指令的意思是就是将a入栈。同样的，执行完

```
int b = 20;
```

会生成汇编指令 mov dword ptr [b],0  也就是将b入栈

![img](https://img-blog.csdnimg.cn/2020031020393817.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoaW5QaWthY2h1,size_16,color_FFFFFF,t_70)

接着执行

```
int ret = sum(a,b);
```

但是我们知道**语句的执行是从右向左指向的**，因此这里会先执行sum(a,b)，而这里sum又是一个函数，因此我们会向sum函数的栈帧内压入参数b，a。而sum(a,b)生成的汇编指令是

 

```
 mov         eax,dword ptr [b]  
 push        eax  
 mov         ecx,dword ptr [a]  
 push        ecx 
```

第一条指令的意思是将b的值放入eax寄存器中，第二条指令的意思是将eax寄存器内的值压入栈中，即将形参b入栈。

第三条指令的意思是将a的值放入ecx寄存器中，第四条指令的意思是将ecx寄存器内的值压入栈中，即将形参a入栈。

这里还要注意，因为我们将两个参数压入了栈内，因此栈顶指针也要进行相应的移动。

![img](https://img-blog.csdnimg.cn/2020031021011664.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoaW5QaWthY2h1,size_16,color_FFFFFF,t_70)

**接下来会生成call指令，call指令的意思是将这行指令的下一行指令的地址压入栈。这样当执行完sum(s,b)并且推出sum函数以后，系统就可以知道从哪里继续运行了**。现在我们先将call指令的后两行指令给大家写出来

  

```
add         esp,8  
mov         dword ptr [ret],eax 
```

![img](https://img-blog.csdnimg.cn/20200310210922877.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoaW5QaWthY2h1,size_16,color_FFFFFF,t_70)

接下来我们就进入sum函数了

```
int sum(int a, int b)
{
	int tmp = 0;
	tmp = a + b;
	return tmp;
}
```

**这里需要注意，花括号｛ 到 int tmp = 0;这行代码之间虽然没有其他任何语句，但是还是会有指令生成。**

![img](https://img-blog.csdnimg.cn/20200310212538361.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoaW5QaWthY2h1,size_16,color_FFFFFF,t_70)

第一条指令 push ebp的意思是，将ebp的值压入栈，即

![img](https://img-blog.csdnimg.cn/2020031021321235.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoaW5QaWthY2h1,size_16,color_FFFFFF,t_70)

此时我们已经sum函数的栈帧，为了区别，我们使用红色来表示sum函数的栈帧。

第二条指令 mov ebp,esp的意思是，将esp的值赋给ebp，也就是说让ebp指向当前esp所指向的位置，也就是当前函数sum的栈底位置。

而第三条指令sub esp,0CCh的意思是给sum函数开辟大小为0CCh大小的栈帧，并且此时esp+=0CCh，即让esp指向当前函数sum的栈顶位置。

![img](https://img-blog.csdnimg.cn/2020031021371445.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoaW5QaWthY2h1,size_16,color_FFFFFF,t_70)

**注意，如果你使用的是VS编译器，那么系统就会将这块为sum函数新开辟的内存赋值为0xCCCCCCCC，而如果你是用的是gcc或g++则不会进行0xCCCCCCCC的初始化。**

 接下来就会执行

```
int tmp = 0;
```

生成指令 mov  dword ptr [tmp],0，即将tmp入栈。

![img](https://img-blog.csdnimg.cn/20200311111432294.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoaW5QaWthY2h1,size_16,color_FFFFFF,t_70)

```
tmp = a + b;
```

会生成指令

 

```
mov         eax,dword ptr [a]  
 add         eax,dword ptr [b]  
 mov         dword ptr [tmp],eax 
```

第一条指令  mov         eax,dword ptr [a]  的意思是，将形参a的值放入到寄存器eax中去，第二条指令 add         eax,dword ptr [b]  的意思是，将b的值与eax寄存器中存放的值相加，并将相加后的值重新存放到eax寄存器中去，即eax+=b，第三条指令 mov         dword ptr [tmp],eax 的意思是将eax寄存器中的值赋给tmp

![img](https://img-blog.csdnimg.cn/20200310215133755.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoaW5QaWthY2h1,size_16,color_FFFFFF,t_70)

最后

```
return tmp;
```

会生成指令mov         eax,dword ptr [tmp]，意思是将tmp的值存放到eax寄存器中，由eax将值带出去返回给主函数。接着return 到花括号 }之间也会有指令生成

![img](https://img-blog.csdnimg.cn/20200310220537899.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoaW5QaWthY2h1,size_16,color_FFFFFF,t_70)

第一条指令 mov esp,ebp的意思是，将ebp的值赋给esp，即让esp指向当前ebp所指向的位置。

![img](https://img-blog.csdnimg.cn/20200310220800845.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoaW5QaWthY2h1,size_16,color_FFFFFF,t_70)

第二条指令 pop ebp的意思是进行出栈（pop）操作，并将出栈的值赋给ebp，于是我们会发现此时ebp又指向了main函数的栈底，因为进行了出栈操作，因此esp也要移动。

![img](https://img-blog.csdnimg.cn/20200310221512205.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoaW5QaWthY2h1,size_16,color_FFFFFF,t_70)

第三条指令ret会先执行出栈操作，并把出栈的内容放入CPU的PC寄存器中，而当前出栈的内容就是我们当初存放的下一行指令的地址，这样系统就可以知道返回到main函数后该从哪儿继续执行了。

![img](https://img-blog.csdnimg.cn/20200310221602708.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoaW5QaWthY2h1,size_16,color_FFFFFF,t_70)

注意，此时系统不会把sum函数的栈帧上的数据清空。

回到main函数后就又到了

```
int ret = sum(a, b);
```

此时，sum(a,b)以执行完毕，接着就会执行int ret，并且将sum函数的返回值通过eax寄存器赋值给ret。相应的指令为

```
add         esp,8  
mov         dword ptr [ret],eax
```

第一条add esp,8的意思是将之前的形参变量a,b交还给系统，且此时esp又指向了main函数的栈顶位置。

![img](https://img-blog.csdnimg.cn/20200310222311369.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoaW5QaWthY2h1,size_16,color_FFFFFF,t_70)

而mov dword ptr [ret],eax的意思是，首先将ret入栈，接着将eax寄存器中的值放到ret中。

![img](https://img-blog.csdnimg.cn/20200310222525658.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1RoaW5QaWthY2h1,size_16,color_FFFFFF,t_70)

接着就是打印操做和出栈操作了，致此我们的函数调用栈的过程就大致讲解完毕了。

**还有一点需要注意，就是当函数的返回值<=4个字节时，返回值是由eax寄存器带出的，当返回值>4  &&   <=8个字节时，返回值是由eax和edx寄存器带出的，当返回值>8个字节时，会产生临时变量带出返回值。**

<=4  eax

>4  &&  <= 8   eax  edx

>8    产生临时量带出返回值





参考：[从汇编指令角度理解函数调用过程_Redamanc的博客-CSDN博客](https://blog.csdn.net/m0_46308273/article/details/115826807)