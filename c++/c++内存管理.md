---
title: c++内存管理
time: 14:37
description: c++内存管理
navbar: true
sidebar: true
footer: true
date: 2023-01-29
category: Document
author: Zhang Xin
next: true
tags:
  - cpp
---
# Primitives 基础组件

* 使用内存的途径

  <img src="https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/20230315204101.png" style="zoom:50%;" />

从应用到操作系统分为四个层次，可以用来操作内存。

![](https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/20230315204150.png)

代码使用示例：

```c++
#include <iostream>
#include <complex>
#include <memory>                //std::allocator  
//#include <ext\pool_allocator.h>    //GCC使用，欲使用 std::allocator 以外的 allocator, 就得自行 #include <ext/...> 
using namespace std;
namespace jj01
{
    void test_primitives()
    {
        cout << "\ntest_primitives().......... \n";

        void* p1 = malloc(512); //512 bytes
        free(p1);

        complex<int>* p2 = new complex<int>; //one object
        delete p2;

        void* p3 = ::operator new(512); //512 bytes
        ::operator delete(p3);

        //以下使用 C++ 标准库提供的 allocators。
        //其接口虽有标准规格，但实现厂商尚未完全遵守；下面三者形式略异。
#ifdef _MSC_VER
        //以下两都是 non-static，定要通過 object 調用。以下分配 3 個 ints.
        int* p4 = allocator<int>().allocate(3, (int*)0);
        p4[0] = 666;
        p4[1] = 999;
        p4[2] = 888;
        cout << "p4[0] = " << p4[0] << endl;
        cout << "p4[1] = " << p4[1] << endl;
        cout << "p4[2] = " << p4[2] << endl;
        allocator<int>().deallocate(p4, 3);
#endif
#ifdef __BORLANDC__
        //以下两函数都是 non-static，定要通过 object 调用。以下分配 5 个 ints.
        int* p4 = allocator<int>().allocate(5);
        allocator<int>().deallocate(p4, 5);
#endif
#ifdef __GNUC__
        //以下两函数都是 static，可通过全名调用之。以下分配 512 bytes.
        //void* p4 = alloc::allocate(512); 
        //alloc::deallocate(p4,512);   

        //以下两函数都是 non-static，定要通过 object 调用。以下分配 7 个 ints.    
        void* p4 = allocator<int>().allocate(7);
        allocator<int>().deallocate((int*)p4, 7);

        //以下两函数都是 non-static，定要通过 object 调用。以下分配 9 个 ints.  
        void* p5 = __gnu_cxx::__pool_alloc<int>().allocate(9);
        __gnu_cxx::__pool_alloc<int>().deallocate((int*)p5, 9);
#endif
    }
} //namespace

int main(void)
{
    jj01::test_primitives();
    return 0;
}
```

## 基本构件 new/delete expression

1. **内存申请**

   ![](https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/20230315204806.png)

   上面这张图揭示了new操作背后编译器做的事：

   - 第一步通过operator new()操作分配一个目标类型的内存大小，这里是Complex的大小；
   - 第二步通过[**static_cast**]([static_cast、const_cast用法_const_cast static_cast_lesliefish的博客-CSDN博客](https://blog.csdn.net/y396397735/article/details/50742750))将得到的内存块强制转换为目标类型指针，这里是Complex*
   - 第三步调用目标类型的构造方法，但是需要注意的是，直接通过pc->Complex::Complex(1, 2)这样的方法调用构造函数只有编译器可以做，用户这样做将产生错误。

   值得注意的是，operator new()操作的内部是调用了malloc()函数。

2. **内存释放**

   ![](https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/20230315205209.png)同样地，delete操作第一步也是调用了对象的析构函数，然后再通过operator delete()函数释放内存，本质上也是调用了free函数。

## Array new / Array delete

![](https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/20230315205555.png)上图主要展示的是关于new array内存分配的大致情况。当new一个数组对象时（例如 new Complex[3])，编译器将分配一块内存，这块内存首部是关于对象内存分配的一些标记，然后下面会分配三个连续的对象内存，在使用delete释放内存时需要使用delete[]。如果不使用delete[]，只是使用delete只会将分配的三块内存空间释放，但不会调用对象的析构函数，如果对象内部还使用了new指向其他空间，如果指向的该空间里的对象的析构函数没有意义，那么不会造成问题，如果有意义，那么由于该部分对象析构函数不会调用，那么将会导致内存泄漏。图中new string[3]便是一个例子，虽然str[0]、str[1]、str[2]被析构了，但只是调用了str[0]的析构函数，其他对象的析构函数不被调用，这里就会出问题。

## placement new

![](https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/20230315231528.png)

## 重载

![](https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/20230315231749.png)如果是正常情况下，调用new之后走的是第二条路线，如果在类中重载了operator new()，那么走的是第一条路线，但最后还是要调用到系统的::operator new()函数，这在后续的例子中会体现。

![](https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/20230315232050.png)如果是在类中重载operator new()方法，那么该方法有N多种形式，但必须保证函数参数列表第一个参数是size_t类型变量；对于operator delete()，第一个参数必须是void* 类型，第二个size_t是可选项，可以去掉。

![](https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/20230315232445.png)



# std::allocator

# malloc/free

# Loki::allocator

# Other Issues


# reference

- [侯捷C++ 内存管理 第一讲 笔记 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/476637169)


