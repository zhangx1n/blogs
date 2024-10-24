---
title: c++11 新特性
time: 14:37
description: c++11 新特性
navbar: true
sidebar: true
footer: true
date: 2023-01-29
category: Tutorial
author: Zhang Xin
next: true
tags:
  - cpp
---
查看编译器版本
```c++
cout<< __cplusplus << endl;
```
---

# Variadic Templates（可变参数模板）

## 一、Variadic Templates（可变参数模板）概述

### 1、谈的是模板Templates：

- 函数模板
- 类模板

### 2、变化的是模板参数：

- **参数个数**：**利用参数个数逐一递减的特性，实现递归函数的调用**，**使用函数模板完成。**
- **参数类型**：**利用参数个数逐一递减以致参数类型也逐一递减的特性，实现递归继承或递归复合**，**以类模板完成**。

![img](https://img-blog.csdnimg.cn/32a1afb0e6d2472991c052d9d31a461f.png)



### 3、print应用举例

```cpp
void print()
{
}

template <typename T, typename... Types>                //这里的...是关键字的一部分：模板参数包

void print(const T& firstArg, const Types&... args)     //这里的...要写在自定义类型Types后面：函数参数类型包
{
    cout << firstArg << endl;
    print(args...);                                     //这里的...要写在变量args后面：函数参数包
}
```

- 1. **注意三种不同的...的应用环境**，这些都是**语法规则**，所以记住即可；**...就是一个所谓的pack（包）**。
- 2. 还要注意的是，**在可变模板参数内部可以使用sizeof...(args)得到实参的个数**。
- 3. 如果同时定义了void print(const Types&... args)：

```cpp
template <typename... Types>

void print(const Types&... args)
{/*......*/}
```

**那么这两个函数是否可以并存，如果可以那么这两个定义会优先调用哪个？换句话说，哪个定义更加泛化，哪个更加特化？这个侯捷老师说以后会做解释。**

**(更新：这个void print(const Types&... args)定义更加泛化，所以会调用之前定义的更特化的版本void print(const T& firstArg, const Types&... args))**

![img](https://img-blog.csdnimg.cn/20210212220141252.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



## 二、Variadic Templates的两个应用

### **1. 实现函数的递归调用**

**举了一个unordered容器中hash函数的计算例子：\**万用的哈希函数，函数入口\**\**return hash_val(c.fname, c.lname, c.no);\****

```c++
class CustomerHash{
public:
    std::size_t operator() (const Customer& c) const {
        // 万用的哈希函数，函数入口return hash_val(c.fname, c.lname, c.no);
        return hash_val(c.fname, c.lname, c.no);
    }
};

template <typename T, typename... Types>
inline void hash_val(size_t& seed, const T& val, const Types&... args){
    hash_combine(seed, val);
    hash_val(seed, args);
}


template <typename... Types>
inline size_t hash_val(const Types&... args){
    size_t seed = 0;
    hash_val(seed, args...);
    return seed;
}

template <typename T>
inline void hash_val(size_t& seed, const T& val){
    hash_conbine(seed, val);
}


inline void hash_combine(size_t& seed, const T& val)
{
    seed ^= std::hash<T>()(val) + 0x9e3779b9 + (seed<<6) + (seed >> 2);
}
```

**本质上和概述里的例子一样，都是利用可变模板参数的函数****递归操作**，这里就不多做解释了。

![img](https://img-blog.csdnimg.cn/20210212220953297.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



### **2. 实现函数的递归继承**

**这里举了一个*tuple的实现*的例子：**

```cpp
template <typename... Values> class tuple;
template <> class tuple<> {};


template <typename Head, typename... Tail>
class tuple<Head, Tail...>
    : private tuple<Tail...>                  //注意这里的私有继承
{
    typedef tuple<Tail...> inherited;
public:
    tuple() {}
    tuple(Head v, Tail... vtail)
        :m_head(v), inherited(vtail...) {}
    Head head() { return m_head; }
    inherited& tail() { return *this; }       //这里涉及派生类到基类的类型转换
protected:
    Head m_head;
};
```

PPT里解释得很清楚：

**用于递归继承实现tuple：**

**typename Head::type head() {return m_head;}报错**

![img](https://img-blog.csdnimg.cn/20210213103526433.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



**第一种实现方法：优化使用decltype实现**

![img](https://img-blog.csdnimg.cn/20210213104402961.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

***\*第二种实现方法\**：直接使用Head作为返回值类型**

![img](https://img-blog.csdnimg.cn/20210213104526245.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



## 三、Variadic Templates应用举例

### 1. 一个简单的print()函数

同print应用举例。

![img](https://img-blog.csdnimg.cn/20210212223623236.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



### 2. 使用variadic templates 重写printf()

***\*逻辑和例子1其实一样，唯一不同的是前面有字符串指示格式，如果不匹配会抛出异常\**，代码如下：**

```cpp
template <typename T, typename... Args>
void printf(const char* s, T value, Args... args)
{
    while(*s){
        if(*s == '%' && *(++s) != '%'){
            std::cout << value;
            printf(++s, args...);
            return;
        }
        std::cout << *s++;
    }
    throw std::logic_error("extra arguments provided to printf");
}
```

![img](https://img-blog.csdnimg.cn/20210212224118878.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



### 3. 使用initializer_list定义max()

- **如果max()要接受可变数量的参数**，可以使用**initializer_list**或者**variadic templates**。
- ***如果参数类型相同，使用initializer_list即可，无需使用*** **variadic templates实现**。

**下面看一下标准库中的max()的例子：**

```cpp
//函数max()的定义
template <typename _Tp>
inline _Tp
max(initializer_list<_Tp> __l)
{
    return *max_element(__l.begin(), __l.end());
}

//函数max_element()的定义
template <typename _ForwardIterator,
          typename _Compare>
_ForwardIterator
__max_element(_ForwardIterator __first,
              _ForwardIterator __last,
              _Compare __comp)
{
    if(__first == __last) return __first;
    _ForwardIterator __result = __first;
    while(++__first != __last)
        if(__comp(__result, __first))
            __result = __first;
    return __result;
}


template<typename _ForwardIterator>
inline _ForwardIterator
max_element(_ForwardIterator __first,
            _ForwardIterator __last)
{
    return __max_element(__first, __last,
                         __iter_less_iter());

}

//函数__iter_less_iter()的定义
inline _Iter_less_iter
__iter_less_iter()
{ return _Iter_less_iter(); }

//类型_Iter_less_iter的定义
struct _Iter_less_iter
{
    template<typename _Iterator1,
             typename _Iterator2>
    bool 
    operator()(_Iterator1 __it1,
               _Iterator1 __it2) const

    { return *__it1 < *__it2; }

};
```



![img](https://img-blog.csdnimg.cn/2021021309400079.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



### 4. 参数类型相同，[递归调用](https://so.csdn.net/so/search?q=递归调用&spm=1001.2101.3001.7020)标准库的std::max()实现maximum()

```cpp
int maximum(int n)
{
    return n;
}
template<typename... Args>
int maximum(int n, Args... args)
{
    return std::max(n, maximum(args...));
}
```

### 

![img](https://img-blog.csdnimg.cn/20210213101654309.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



### 5. 为tuple重载<<运算符（使用类模板）

```cpp
//output operator for tuples
template <typename... Args>
ostream& operator<<(ostream& os, const tuple<Args...>& t){
    os << "[";
    PRINT_TUPLE<0, sizeof...(Args), Args...>::print(os, t);
    return os << "]";
}
  
//print element with index IDX of tuple with MAX elements
template <int IDX, int MAX, typename... Args>
struct PRINT_TUPLE{
    static void print(ostream& os, const tuple<Args...>& t){
        os << get<IDX>(t) << (IDX+1 == MAX ? "" : ",");
        PRINT_TUPLE<IDX+1, MAX, Args...>::print(os, t);
    }
};
//partial specialization to end the recursion
template <int MAX, typename... Args>
struct PRINT_TUPLE<MAX, MAX, Args...>{
    static void print(std::ostream& os, const tuple<Args...>& t){
    }
};
```

**这里关于模板的使用有点我不理解的地方：**

(1)类模板可以传入对象而不是类型，看起来有点像函数传参。

(2)下面的偏特化版本，class后面也可以写尖括号，没见过这种写法。模板这块可能还得下点功夫。

![img](https://img-blog.csdnimg.cn/20210213102549884.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



### 6. 用于递归继承

**tuple中的递归继承：见第二部分的2**



### 7. 受6的启发，用于递归复合

```cpp
template <typename... Values> class tup;
template<> class tup<> {};
template<typename Head, typename... Tail>
class tup<Head, Tail...>
{
    typedef tup<Tail...> composited;
protected:
    composited m_tail;
    Head m_head;
public:
    tup() {}
    tup(Head v, Tail... vtail)
        : m_tail(vtail...), m_head(v) {}
    Head head() { return m_head; }
    composited& tail() { return m_tail; }
};
```

![img](https://img-blog.csdnimg.cn/20210213105133244.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



# 语言特性之＜模板表达式中的空格、nullptr 、auto＞

## 一、语言特性之模板表达式中的空格

**C++11可以去掉模块表达式前面的空格**

![img](https://img-blog.csdnimg.cn/20201206221211949.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)


## 二、语言特性之nullptr

**标准库**允许使用**nullptr取代0或者NULL来对指针赋值。**

- **nullptr 是个新关键字**
- **nullptr 可以被自动转换为各种 pointer 类型，但不会被转换为任何整数类型，**
- **nullptr的类型为std::nullptr_t，定义于 `<cstddef>`头文件中

![img](https://img-blog.csdnimg.cn/20210203231819722.png)

**举例：**

```cpp
void f(int);
void f(void *);

f(0);    **// 调用 f(int).**
f(NULL); **// 如果定义NULL为0，则调用 f(int)，否则调用 f(void \*).**
f(nullptr); **// 调用 f(void \*).
```

 

## 三、语言特性之auto（自动类型推导）

（1）C++11 **auto**可以进行**自动类型推导。**

- C语言默认的局部变量是auto类型的
- C++11 auto可以进行自动类型推导

**（2）使用auto的场景**：**类型太长或者类型太复杂**

**举例：**

![img](https://img-blog.csdnimg.cn/20210203232346105.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

![img](https://img-blog.csdnimg.cn/20210203232605480.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

![img](https://img-blog.csdnimg.cn/20210203232720198.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



# 语言特性之＜一致性初始化、Initializer_list 、基于范围的for循环、explicit＞

## 一、一致性初始化（uniform initialization）

**C++11之前初始化时存在多个版本``{}，（），=``**。**让使用者使用时比较混乱**，**C++11提供一种万用的初始化方法，就是使用大括号{}。**

**原理解析**：

**当编译器看到大括号包起来的东西{t1,t2...tn}时**，会生成一个`initializer_list<T>（initializer_list它其实是关联一个array<T,n>)。`

- **调用函数（例如构造函数ctor）时该array内的元素可\**被编译器分解逐一传给函数；\****元素逐一分解传递给函数进行初始化
- **但是如果调用函数自身提供了`initializer_list<T>`参数类型的构造函数时，则\**不会分解而是直接传过去\**。**直接整包传入进行初始化。所有的容器都可以接受这样的参数

　![img](https://img-blog.csdnimg.cn/img_convert/d7f6c329e08199576ffcca7b56294f81.png)

***举例：\***

```cpp
// 初值列：强迫初始化为 0 （或nullptr）.
int i; // i 初始化为未定义值.
int j{}; // j 初始化为 0 （大括号可以用来设初值）
int * p; // p 初始化为未定义值.
int * q{}; // q 初始化为 0 （大括号可以用来设初值）
 
// 窄化（精度降低或造成数值变动）对大括号而言是不成立的.
int x0(3.4); // ok.
int x1 = 3.4; // ok.
int x2 { 3.4 }; // wrong.（不允许窄化数据处理，其实我的编译器只给警告）
int x3 = { 3.4 }; // wrong.（不允许窄化数据处理，其实我的编译器只给警告）
std::vector<int> v1 { 1, 2, 3 }; // ok.
std::vector<int> v2 { 1.1, 2.2, 3.3 }; // wrong.（不允许窄化数据处理，其实我的编译器只给警告）
```

**注：{}不允许窄化转化（类似不允许隐式类型转化）。**



## **二、Initializer_list**

### **1、`initializer_list<T>`使用举例**：

- **`initializer_list<T>`是一个class（类模板）**，这个必须类型要一致，跟模板不定的参数类型相比，模板不定的参数类型可以都不一样。
- `***initializer_list<T>`类似于*容器*的使用方法***

 **（1）例1**

![img](https://img-blog.csdnimg.cn/20210210224126737.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

**（2）例2**

![img](https://img-blog.csdnimg.cn/2021021022440166.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

**注意：**

- **如果没有版本2，只有版本1。q和s不变，但是会分为两个参数传入。r将会不成立。**
- ***只要编译器遇到大括号里面有一些数，再传值的时候都会去\**生成一个`initializer_list<T>`去处理；\*****
- ***\*`initializer_list<T>`\****这个和前面一章节提到的***\*不定参数模板相比，这个必须类型要一致，而后者则可以类型随意组合\**。**



### **2、initializer_list源码剖析：**

- **1.`initializer_list<T>`背后有array数组支撑，\**initializer_list它其实是关联一个array<T,n>\****
- **2.array是个指针，只是一个浅拷贝动作，比较危险，两个指针指向同一个内存**

![img](https://img-blog.csdnimg.cn/20210210224934246.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



### **3、initializer_list在STL中的使用：**

- **所有容器都接受指定任意数量的值\**用于构造或赋值或者insert（）或assign（）\****
- **算法max（）和min（）也接受任意参数**

![img](https://img-blog.csdnimg.cn/2021021022574624.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

**使用举例：**

![img](https://img-blog.csdnimg.cn/20210210225940477.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



### **4、容器array：**

**TR1版本：**

![img](https://img-blog.csdnimg.cn/20210210225220161.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

**GCC4.9版本：**

![img](https://img-blog.csdnimg.cn/2021021022525129.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

![img](https://img-blog.csdnimg.cn/img_convert/be0b5b54ddf5a680f70e0f4e3c06cc92.png)



## **三、基于范围的for循环**

### 1、C++2.0新增新语法本质是将后边的集合取出来依次赋值给前面申明的变量(基于范围的for循环背后的原理)

**![img](https://img-blog.csdnimg.cn/img_convert/9c246404ef0d6cd4445770d1352e585f.png)**

**![img](https://img-blog.csdnimg.cn/img_convert/c69d37de345079d6d2e12ad10eed0da0.png)**

 注意：

1. **上图中申明引用类型的速度快很多**，因为引用相当于指针的操作只操作4个字节，而非引用的速度开销随着数据类型所占空间增长而增大，且声明引用后的修改将直接影响到集合中数据的值；**但是带来的后果是可以改变容器的值，如果不希望被改变，则可以加const。**
2. 用for操作容器时，标准库规定，关联容器都不允许通过迭代器修改修改容器的值，也就是说上面申明为引用的for循环无法修改关联容器里的数值（因为关联容器的迭代器是const）；
3. 当解引用一个关联容器迭代器时，会获得一个类型为value_type的值的引用。对于map而言，value_type是一个pair，pair由first和second组成，first成员保存const关键字，second保存值，而对于set而言，set的迭代器也是const，虽然set定义了iterator和const_iterator类型，但是两种类型都只允许只读set的元素；
4. 因为set使用红黑树做底部结构，但是set只有一个元素（key和data是一样得，也就是说key就是value），所以set是不允许改变元素值得，所以在实现上，set的迭代器拿到的是const的iterator，是不能修改的；
5. 我们通常不去对关联容器使用泛型算法，因为set的关键字是const的，而map的元素pair的第一个成员也是const的，因此不能将关联容器传递给修改或重排元素的算法（实际中我们使用泛型算法一般只把关联容器当成我们要操作数据的源头位置或者目的位置，例如copy算法将元素从一个关联容器拷贝到另一个序列）。

### 2、基于范围的for循环对于explicit类型申明的转换是不可以的

![img](https://img-blog.csdnimg.cn/img_convert/e64a23441fc9bd4f9df831426b9ce838.png)



## **四、explicit**

　　**explicit关键字**一直存在，**只能作用在构造函数中**， **目的是阻止编译器进行\**不应该允许的构造函数进行隐式转换\**（也就是说不让编译器自作聪明）**。**声明为explicit的构造函数不能进行隐式转换，只能允许使用者明确调用构造函数；**

​    **在C++2.0中，explicit可以支持不止一个参数的构造函数使用（C++11之前只能支持传入一个实参）**

### 1、C++2.0以前，explicit只能作用在一个实参的构造函数上

![img](https://img-blog.csdnimg.cn/20210204000747804.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

```cpp
 1 #include <iostream>
 2 class Single{
 3 
 4 public:
 5     //普通构造函数(单一实参)
 6     Single(int a，int b = 0):num(a)
 7     {}
 8 private:
 9     int num;
10 };
11 
12 class SingleMore {
13 public:
14     //explicit 显示申明构造函数(单一实参)
15     explicit SingleMore(int a) :num(a)
16     {}
17 private:
18     int num;
19 };
20 
21 
22 #if 1
23 int main(int argc, char* argv[])
24 {
25     Single single(3);
26     Single single2 = 4;
27 
28     SingleMore singleMore(3);
29     SingleMore singleMore2 = 4;//编译报错，E0415 不存在从 "int" 转换到 "SingleMore" 的适当构造函数
30 
31     return 0;
32 }
33 #endif
```



### 2、C++2.0以后，explicit可以适用多个实参的构造函数

![img](https://img-blog.csdnimg.cn/20210204001126668.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

```cpp
 1 struct A
 2 {
 3     A(int) { }      // 转换构造函数
 4     A(int, int) { } // 转换构造函数 (C++11)
 5     operator bool() const { return true; }
 6 };
 7  
 8 struct B
 9 {
10     explicit B(int) { }
11     explicit B(int, int) { }
12     explicit operator bool() const { return true; }
13 };
14  
15 int main()
16 {
17     A a1 = 1;      // OK ：复制初始化选择 A::A(int)
18     A a2(2);       // OK ：直接初始化选择 A::A(int)
19     A a3 {4, 5};   // OK ：直接列表初始化选择 A::A(int, int)
20     A a4 = {4, 5}; // OK ：复制列表初始化选择 A::A(int, int)
21     A a5 = (A)1;   // OK ：显式转型进行 static_cast
22     if (a1) ;      // OK ：A::operator bool()
23     bool na1 = a1; // OK ：复制初始化选择 A::operator bool()
24     bool na2 = static_cast<bool>(a1); // OK ：static_cast 进行直接初始化
25  
26 //  B b1 = 1;      // 错误：复制初始化不考虑 B::B(int)
27     B b2(2);       // OK ：直接初始化选择 B::B(int)
28     B b3 {4, 5};   // OK ：直接列表初始化选择 B::B(int, int)
29 //  B b4 = {4, 5}; // 错误：复制列表初始化不考虑 B::B(int,int)
30     B b5 = (B)1;   // OK ：显式转型进行 static_cast
31     if (b2) ;      // OK ：B::operator bool()
32 //  bool nb1 = b2; // 错误：复制初始化不考虑 B::operator bool()
33     bool nb2 = static_cast<bool>(b2); // OK ：static_cast 进行直接初始化
34 }
```

 

# 语言特性之＜=default,=delete、using、noexcept、override、final、以及和const对比＞

## 一、=default,=delete

### 1、首先我们要回顾一下编译器提供的默认函数：

- **C++中，当我们设计与编写一个类时，若不显著申明，则类会默认为我们提供如下几个函数：**

（1）构造函数(A())

（2）析构函数（~A()）

（3）拷贝构造函数(A(A&))

（4）拷贝赋值函数（A& operator=(A&)）

（5）移动构造函数（A(A&&)）

（6）移动赋值函数（A& operator=(A&&)）

![img](https://img-blog.csdnimg.cn/20210210214402984.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

注意：拷贝函数如果涉及指针就要区分浅拷贝（指针只占4字节，浅拷贝只把指针所占的那4个字节拷贝过去）和深拷贝（不仅要拷贝指针所占的字节，还要把指针所指的东西也要拷贝过去）；

- **默认提供全局的默认操作符函数**

*（1）operator,*

（2）operator &,

（3）operator &&,

（4）operator *,

（5）operator->,

（6）operator->*,

（7）operator new,

（8）operator delete。



### 2、何时需要自定义big-three(构造函数、拷贝构造、拷贝赋值)/big-five(新增移动构造函数、移动赋值函数)

- ***如果类中带有point member（指针成员）*，那我们就可以断定*必须要给出big-three*；**
- **如果不带，\**绝大多与情况下就不必给出big-three，用默认的就好。\****

![img](https://img-blog.csdnimg.cn/20210210214645713.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



### 3、**default、delete**关键字使用示例

**（1）default、delete关键字的定义：**

- 如下图所示，分别是**构造函数、拷贝构造函数、移动构造函数（Zoo&&表示得是右值引用）、赋值函数、移动赋值函数等5种成员函数**，**default和delete基本就作用再这5种函数上。**
- **在c++中，如果你自定义了这5种函数，编译器就不会再为你生成默认的相关函数**，**但是如果我们在后边加上*****=default关键字*****，就****可以重新获得并使用编译器为我们生成的默认函数**（**显式缺省:告知编译器即使自己定义了也要生成函数默认的缺省版本)**）；
- ***=delete关键字***相对于上面来说则是相反的，**=delete表示不要这个函数，就是说这个函数已经删除了不能用了，一旦别人使用就会报错（****显式删除：告知编译器不生成函数默认的缺省版本****)，****引进这两种新特性的目的是为了增强对“类默认函数的控制”，从而让程序员更加精准地去控制默认版本的函数。**

![img](https://img-blog.csdnimg.cn/img_convert/38e74fcd36d4906fb4be81e184baae9c.png)



**（2）default、delete关键字的使用：**

![img](https://img-blog.csdnimg.cn/img_convert/22f54eb0fb251d5d80b261d32f9daa69.png)

**（3）No-Copy and Private-Copy：**

![img](https://img-blog.csdnimg.cn/20210210215139943.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

**boost::noncopyable源码剖析：**

## ![img](https://img-blog.csdnimg.cn/20210210215247780.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



## 二、using

### 1、Alias Template（模板的别名）【using在2.0有了新的意义，用来表示别名化的语法】

**1.1 Alias Template（模板的别名）**

- ***\*using\**用来给类型取别名，且这个别名化是可以带参数的**
- **同样具有别名化意思的还有\**define\**（可以带参数），\**typedef\**（不能带参数）**
- define和typedef无法达到同样的效果，它们在特殊时候都无法代替using
- 模板的别名（using）也没法做部分或完全特化，只能对原名做（化名不能代替本尊）

![img](https://img-blog.csdnimg.cn/20210210230932784.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

**1.2、应用实例(引出\**模板模板参数\**)**

考虑这样一种需求，假设我们需要实现一个函数**test_moveable**(***容器对象，类型对象***)，从而**能实现传入任意的容器和类型**，都能将其组合为一个新的东西：容器<类型>，这样的话我们的函数应该怎么设计呢？

**（1） 解法一：函数模板(无法实现)**

```cpp
template <typename Container, typename T>
void test_moveable(Container cntr, T elem)
{
    Container<T> c;            //[Error] 'Container' is not a template
    for(long i=0; i<SIZE; ++i)
        c.insert(c.end(), T());
    output_static_data(T());
    Container<T> c1(c);
    Container<T> c2(std::move(c));
    c1.swap(c2);
}
这样设计的思路是显而易见的，但很遗憾的是并不能通过编译，因为我们调用该函数传入的只能是对象，也就是假如我们传入一个list<int>的对象，那么Container就等同于list<int>，而list<int>并不是一个模板，我们希望改变list尖括号中的类型，但这样设计并不能做到。
```

**（2）解法二：函数模板+iterator+traits(可以实现)**

```cpp
template<typename Container>
void test_moveable(Container c)
{
    typedef typename iterator_traits<typename Container::iterator>::value_type Valtype;
    for(long i=0; i<SIZE; ++i)
        c.insert(c.end(), Valtype());
    output_static_data(*(c.begin()));
    Container<T> c1(c);
    Container<T> c2(std::move(c));
    c1.swap(c2);
}
(注：这里还涉及到了typename的第二种用法，用于表示后面跟着的是一个类型，主要是为了避免歧义，因为作用域符号后面跟着的可能是类型，也可能是成员，具体见链接https://www.cnblogs.com/wuchanming/p/3765345.html)
```

***这样做是可以达到效果的，但是却改变了函数签名，使用的时候我们需要这样调用：\**`test_moveable(list<int>())`\**，和我们开始设计的是不一样的。那么，有没有template语法能够在模板接受一个template参数Container时，当Container本身又是一个class template，能取出Container的template参数？例如收到一个`vector<string>`，能够取出其元素类型string？那么这就引出了模板模板参数的概念。也就是下面的解法三。***



**（3）解法三：模板模板参数 + alias template(可以实现)**

```cpp
template <typename T,
          template <typename T>
              class Container
         >
class XCls
{
private:
    Container<T> c;
public:
    XCLs()
    {
        for(long i=0; i<SIZE; ++i)
            c.insert(c.end(), T());
        output_static_data(T());
        Container<T> c1(c);
        Container<T> c2(std::move(c));
        c1.swap(c2);
    }
};
(注：模板模板参数中的T可以不写，默认就是前面的T)
```

使用上面的定义，在实际使用时还是会报错：

```cobol
XCls<MyString, vector> c1;        //[Error] vector的实际类型和模板中的Container<T>类型不匹配
```

这是因为vector其实有两个模板参数，虽然第二个有默认值，我们平时也可以像`vector<int>`这样用。但是在模板中直接这样写是不匹配的。所以这里就用到了我们一开始提到的模板别名，只要传入的是vector的模板别名就可以了，如下所示：

```cpp
//不得在function body之内声明
template<typename T>
using Vec = vector<T, allocator<T>>;
XCls<MyString, Vec> c1;
```

其中模板别名的定义不能在function body之内，也就是需要写在任何函数的外面，包括主函数。



### **2、Type Alias（类型别名）：类似typedef**

**类型别名类似于typedef，也是使用using来实现的。**

**(1)用于函数指针或者普通类型进行重命名**

```cpp
using func = void(*)(int, int);
//相当于
typedef void (*func)(int, int);
```

这两句话的意思都是func是一个函数类型

**(2)type alias can introduce a member typedef name：类型别名可以应用成员重定义名称**

```cpp
template<typename T>
struct Container{
    using value_type = T;    //typedef T value_type;
};
```

**这样定义就可以用在泛型编程当中：**

```cpp
template<typename Cntr>
void fn2(const Cntr& c)
{
    typename Cntr::value_type n;

}
```



### 3、所有using的使用情况归类

**using三种应用：**

- 1.打开命令空间或者命令空间的成员
- **2.类似第一种，打开类的成员**
- **3.类型别名**和**模板别名（C++ 11开始支持）**

![img](https://img-blog.csdnimg.cn/img_convert/f01ad4dce83b464ca9f882c617cd9734.png)



## 三、noexcept

- **noexcept**用于**申明函数保证不会抛出异常**，后面可以跟一个括号写一个条件，也就是说在某种条件满足情况下，不会抛出异常。
- **一般异常处理流程**：当程序发生异常时会将异常信息上报返回给调用者，如果；有异常处理则处理，如果该调用者没有处理异常则会接着上报上一层，若到了最上层都没有处理，就会调用std::terminate()->std::abort()，然后终止程序。

![img](https://img-blog.csdnimg.cn/img_convert/0e7239236071e485c0c9fbd9cbeb49cf.png)

**移动构造函数和移动赋值函数。如果构造函数没有noexcept，vector将不敢使用它：**

![img](https://img-blog.csdnimg.cn/20210210222310929.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



## 四、override

**override**用于**明确要重写父类的虚函数上**，相当于告诉编译器这个函数就是要**重写父类虚函数这样一个意图**，让编译器帮忙检查，而没有这个关键字，编译器是不会帮你检查的。

![img](https://img-blog.csdnimg.cn/img_convert/c20cee82c3aca4fb54ba5f249bbf5636.png)



## 五、final

**final新增两种功能：**

- **(1)、禁止基类被继承**
- **(2)、禁止虚函数被重写**

![img](https://img-blog.csdnimg.cn/img_convert/fe7bb0833c25914dbb53fe6e99563706.png)



## 六、const

该部分参考转载：[c++ 11 final, override，const 成员函数_杨玉庆的博客-CSDN博客_c++ override const](https://blog.csdn.net/u011327981/article/details/77656866)

**这是个人新的总结，非语法部分，目的是为了对比以上final和override.**

- **在C++中，若一个变量声明为const类型，则试图修改该变量的值的操作都被视编译错误**

![img](https://img-blog.csdnimg.cn/img_convert/25642e27530ff8e17ec3d6619cb242eb.png)



-  **只有被声明为const的成员函数才能被一个const类对象调用**

![img](https://img-blog.csdnimg.cn/img_convert/f762b25ab919f7b5fe9470ca0cb0938a.png)



- **若成员成员函数声明为const，则该函数不允许修改类的数据成员**

![img](https://img-blog.csdnimg.cn/img_convert/506c524c01b782f0bfada755d05fb9e3.png)

​    **在上面成员函数的定义中，ok()的定义是合法的，error()的定义则非法。**

​    值得注意的是，把一个成员函数声明为const可以保证这个成员函数不修改数据成员，但是，如果据成员是指针，则const成员函数并不能保证不修改指针指向的对象，编译器不会把这种修改检测为错误。例如，

```cpp
class Name {  
public:  
void setName(const string &s) const;  
private:  
    char *m_sName;  
};  
void setName(const string &s) const {  
    m_sName = s.c_str();      // 错误！不能修改m_sName;  
for (int i = 0; i < s.size(); ++i)   
    m_sName[i] = s[i];    // 不好的风格，但不是错误的  
} 
```



​    虽然m_Name不能被修改，但m_sName是char *类型，const成员函数可以修改其所指向的字符。

​    const成员函数可以被具有相同参数列表的非const成员函数重载，例如，

```cpp
class Screen {  
public:  
char get(int x,int y);  
char get(int x,int y) const;  
};  
```

​    在这种情况下，类对象的常量性决定调用哪个函数。

```cpp
const Screen cs;  
Screen cc2;  
char ch = cs.get(0, 0);  // 调用const成员函数  
ch = cs2.get(0, 0);     // 调用非const成员函数  
```

**小结：**

- 1）**const成员函数**可以访问非const对象的非const数据成员、const数据成员，也可以访问const对象内的所有数据成员；
- 2）**非const成员函数**可以访问非const对象的非const数据成员、const数据成员，但不可以访问const对象的任意数据成员；
- 3）作为一种良好的编程风格，在声明一个成员函数时，若该成员函数并不对数据成员进行修改操作，**应尽可能将该成员函数声明为const 成员函数。**

# 语言特性之＜decltype、lambda＞

# 一、新关键字decltype

## 1 decltype定义

引入新关键字**decltype** **可以让编译器找出表达式的类型**，为了区别typeof，以下做一个概念区分：

- **typeof**是一个一元运算，放在一个运算数之前，运算数可以  是任意类型，非常依赖平台，已过时，**由decltype代替**；理解为：**我们根据typeof（）括号里面的变量，自动识别变量类型并返回该类型；**
- **typedef**：定义一种类型的别名，而不只是简单的宏替换；
- **define**：简单的宏替换。

比如我想知道别人传给我testVec的类型是什么（前提是我只知道他是一个容器），因为**容器都有value_type这一个属性**，我可以下面这么写

```cpp
std::vector<int> testVec;
decltype(testVec)::value_type type;
```

## 2 decltype三种用法

### 2.1 decltype三种用法之一：***用来声明函数的返回值类型，一种新的指定函数返回值类型的方式***

```cpp
template<typename T1, typename T2>
auto Add(T1 x, T2 y) ->decltype(x + y);
```

![img](https://img-blog.csdnimg.cn/202102052311558.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

### 2.2 decltype三种用法之二：模板之间的应用

**注意：**

**下图中的typename，因为编译器编译到这并不知道obj是什么，这里加``::``前面就必须要加上typename告诉编译器这就是一个类型，不然编译器会犹豫不决。**

![img](https://img-blog.csdnimg.cn/2021020523175999.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

### 2.3 decltype三种用法之三：***用来求lambda表达式的类型***

- **lambda是匿名的函数对象或仿函数，每一个都是独一无二的；**
- **如果需要声明一个这种对象的话，需要用模板或者auto；**
- ***\*如果需要\**\**lambda表达式的类型\**\**type，可以使用decltype；\****
- **lambda没有默认构造函数和析构函数。**

![img](https://img-blog.csdnimg.cn/2021020523193724.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

## ![img](https://img-blog.csdnimg.cn/2021020523472228.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



# 二、lambda

## 1 lambda语法以及调用方式

**定义：****lambda是一组功能的组合定义，lambda可以定义为内联函数，可以被当做一个参数或者一个对象，类似于仿函数。**

***\**（1）\*lambda\*最简单形式：\*\****  ![img](https://img-blog.csdnimg.cn/20210209215910372.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

  **注意：加括号不是所谓的构造临时对象，而是直接就** **调用** **(相对于其他用法的特殊形式)**



**（2）*lambda*一般形式：**

- **[] : lambda导入器，取用外部变量。**
- **()：类似函数参数**
- **mutable：[]中的导入数据是否可变**
- **throwSpec：抛出异常**
- **retType：类似函数返回值**
- **{} : 类似函数体**

![img](https://img-blog.csdnimg.cn/20210205232742575.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)



## 2 **lambda**里面对应的是一个匿名的函数对象

　　**定义一个lambda相当于定义一个函数对象**（即仿函数：一个普通类并重载类的“()”运算符），但是**由于lambda的奇特写法，标准库没有提供默认构造函数和赋值函数的，并且里面有一个括号运算符重载函数**，***\*mutable\**（该关键字表示该函数是\**no-const\**，\**没有\**该关键字表示是\**const\**类型）。**

![img](https://img-blog.csdnimg.cn/20210205234435563.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

![img](https://img-blog.csdnimg.cn/img_convert/b94a1561ff3220be6a5adce35403ddc6.png)

 **上图说明：如果没有mutable，进行++id是编译不通过的，因为你是以value形式传进来的参数；**

![img](https://img-blog.csdnimg.cn/img_convert/030aec4f66f2f7ea534c38548d56ee2c.png)

## 3 lambda和[函数对象](https://so.csdn.net/so/search?q=函数对象&spm=1001.2101.3001.7020)（仿函数）的对比使用

![img](https://img-blog.csdnimg.cn/img_convert/2a969c33a3972f1437ea366dc72a17c3.png)

# 标准库之＜标准库＞

# 一、C++关键字

![img](https://img-blog.csdnimg.cn/a36d8591eec642f2b8a7af34e3619393.png)

# 二、标准库源代码分布

## 1 VC的编译器源码目录

**C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\include**

![img](https://img-blog.csdnimg.cn/20210215205508774.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

![img](https://img-blog.csdnimg.cn/img_convert/3b1371e8f3380a501e215931910696f3.png)

## 2 [GNU](https://so.csdn.net/so/search?q=GNU&spm=1001.2101.3001.7020) C++的编译器源码目录

![img](https://img-blog.csdnimg.cn/20210215205547825.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1MDQxNTY5,size_16,color_FFFFFF,t_70)

# 三、Rvalue references([右值引用](https://so.csdn.net/so/search?q=右值引用&spm=1001.2101.3001.7020))

Rvalue references are a new reference type introduced in C++ that help solve the problem of **unnecessary copying** and enable **perfect forwarding**. When the right-hand side of an assignment is an rvalue, then the left-hand side object can steal resources from the right-hand side object rather than performing a seperate allocation, thus enabling **move semantics**.

(注：***perfect forwarding被翻译为精确传递，精确转发等***，***其含义为将一组参数原封不动地传递给另一个函数***。**在这里“原封不动”不仅仅是参数的值不变，除了参数值之外，还有\**两组属性：左值 / 右值和 const / non-const\**， \**精确传递就是在参数传递过程中，所有这些属性和参数值都不能改变\****。**第二部分也会具体解释。**

**另参见[C++11之右值引用、完美转换（Perfect Forwarding）、std::move_云飞扬_Dylan的博客-CSDN博客](https://blog.csdn.net/jxianxu/article/details/62046839))**

## **1. 左值和右值的定义**

- **左值lvalue**：可以出现在operator=左边的值；（**表达式结束后依然存在的对象，我们也叫做变量;*可以出现在=左边也可以在右边*。**）
- **右值rvalue**：只能出现在operator=右边的值。（**表达式结束后就不存在的临时对象;\**只能出现在=右边\**；例如临时对象。**）

比如说**临时对象就是一种右值**，形似：

```cpp
int a = 0, b = 0;
a + b = 4;
```

**不能通过编译，因为a+b是右值**。

但例外的是，**很多class的临时对象竟然可以被赋值**，以string为例：

```cpp
string s1("Hello ");
string s2("World");
s1 + s2 = s2;            //竟然可以通过编译
//赋值之后s1, s2的值不变
string() = "World";      //竟然可以对temp obj(临时对象)赋值
```

但是这只是一种例外情况，可以理解为语言本身的“bug”，**临时对象是永远被当做右值的，即使有些class的临时对象可以放在等号左边(“可以”指可以通过编译，给临时对象赋值无意义)**。

![img](https://img-blog.csdnimg.cn/img_convert/6ea75e9d80ab9b1bdd36f0f9d845d209.png)

【注意】：

**虽然string和复数的举例推翻了左右值书写的准则，但是这是由于一些C++定义类型导致的，我们不要去管他；**

***\*我们只要记住两点：\****

- **1、临时对象就是一个右值；**
- **2、右值不要出现在等号左边。**



## **2. 为什么要引入一个新的"右值引用"的概念**

***【右值引用】*：**

-  一种新的引用类型，可以减少不必要的拷贝。
- 当右手边是一个右值时，左手边可以偷右边的资源，而不需要copy。
- 当rvalue出现于operator=(copy assignment)的右侧，我们认为对其资源进行偷取 / 搬移(move)而非拷贝(copy是可以的，是合理的。

那么：

**(1)\**必须有语法\**让我们\**在\**\**调用端\**\**告诉编译器：这是个rvalue\****

**(2)\**必须有语法\**让我们\**在\**\**被调用端\**\**写出一个专门处理rvalue的所谓move assignment函数\****



## **3. 一个例子**

![img](https://img-blog.csdnimg.cn/2020071619264252.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L29uZU5ZVA==,size_16,color_FFFFFF,t_70)

(1)**insert()往容器中插入元素，涉及到元素的移动**，所以**为了效率insert()有右值引用的版本**，**搬动元素的时候要调用元素的ctor，调用的ctor就是元素的\**move ctor；\****

(2)**一个对象的move ctor的逻辑**：**简单地copy 指针的值，所以原来的对象对资源的引用要销毁，要保证原来的对象不再使用，这样才安全**；

(3)**使用\**std::move()\**\**可以得到一个左值的右值引用；\****



​    **在C++11之前我们对一个函数返回值取地址是错误的**；但是***\*在C++11的新语法中，我们可以使用&&符号表示对右值取引用或者使用move函数将一个左值变为右值\**；**相应的，我**们也要为对应的元素对象实现一个move构造函数或者move赋值函数的重载版本（适用容器中操作元素时）**。比如在做容器的在C++ 2.0之后，容器的插入动作都提供了一个insert的重载版本，专门适用这种新语法，如下所示：

![img](https://img-blog.csdnimg.cn/img_convert/8fcaa72908569d509111d1b7309f4b8b.png)

 　当编译器检测到我们insert的值是一个右值(move函数返回一个右值)或者右值引用(&&，临时对象都会被当成右值引用)时，会调用下面新增的这个重载函数，让它偷取这个右值的东西免去自身取构造内存的动作，因为插入动作会调用拷贝构造函数，如果插入的元素是一个基本类型而不需要额外提供什么，但是如果插入的是一个复杂类型，原本我们需要写一个拷贝构造函数，开辟一块内存一个个的赋值过去，但现在我们要提供一个move搬移构造就行了（比如像string（编译器已经实现）类，move构造函数只是将既有的内部字符数组赋予新对象就行了，此时相当于新对象指针和原对象指针指向同一个地方，要注意执行move后原对象的指针是个不确定状态，不能使用），**所以任何非平凡的类（除了基本类型），都应该提供move构造和move assignment(赋值)函数：**

![img](https://img-blog.csdnimg.cn/img_convert/d654afb9ff848359eb0b86328086a801.png)

![img](https://img-blog.csdnimg.cn/img_convert/de3c2160a48297cee70babb6383ca251.png)

- 这里说一下**move中的偷**的概念，所谓偷就是借用之前的值，对于指针来说就是两个指针指向同一个地方，也就是说**move语义就是指针的浅拷贝，为了指针的安全我们还要在偷完之后将原来的指针打断以禁止后续再使用这个值**
- **右值经函数转交到下一个函数时会变成一个左值**



# 四、Perfect forwarding(完美转发)

这里只说了怎么写可以实现完美转发，但是没有解释为什么需要这么写？以及各种不同类型([左值](https://so.csdn.net/so/search?q=左值&spm=1001.2101.3001.7020)还是右值，const还是non-const)的情况是怎样得到正确处理的？得去别的地方找一下。

## **1、标准库中forward()和move()的定义**

**forward()：**

```cpp
//Forward on lvalue
template<typename _Tp>
    constexpr _Tp&&
    forward(typename std::remove_reference<_Tp>::type& __t) noexcept
    { return static_cast<_Tp&&>(__t); }
 
//Forward on rvalue
template<typename _Tp>
    constexpr _Tp&&
    forward(typename std::remove_reference<_Tp>::type&& __t) noexcept
    { 
        static_assert(!std::is_lvalue_reference<_Tp>::value, "template argument"
                " substituting _Tp is an lvalue reference type");
        return static_cast<_Tp&&>(__t); 
    }
```

**move()：**

```cpp
template<typename _Tp>
    constexpr typename std::remove_reference<_Tp>::type&&
    move(_Tp&& __t) noexcept
    { return static_cast<typename std::remove_reference<_Tp>::type&&>(__t); }
```



## **2、不完美转发**

![img](https://img-blog.csdnimg.cn/img_convert/61df2ebae1e6b46fe2ed2304522d7f53.png)

## **3、完美转发**

![img](https://img-blog.csdnimg.cn/20098fe5130e4559a2b4fc0adfec9167.png)

 





# 五、写一个move-aware class

**(1)定义了Big5和hashfunction，拷贝构造和拷贝赋值的逻辑很重要，具体见代码；**

**(2)move constructor和move assignment operator本质上都是浅拷贝，但在浅拷贝完成以后要把原先对象与资源的联系切断，在本例中表现为将指针置为NULL。所以在析构函数中，释放资源之前要先判断指针是否为NULL；**

```cpp
class MyString{
public:
    static size_t DCtor;        //累计default-ctor呼叫次数
    static size_t Ctor;         //累计ctor呼叫次数
    static size_t CCtor;        //累计copy-ctor呼叫次数
    static size_t CAsgn;        //累计copy-asgn呼叫次数
    static size_t MCtor;        //累计move-ctor呼叫次数
    static size_t MAsgn;        //累计move-asgn呼叫次数
    static size_t Dtor;         //累计dtor呼叫次数
private:
    char* _data;
    size_t _len;
    void init_data(const char *s){
        _data = new char[_len + 1];
        memcpy(_data, s, _len);
        _data[_len] = '\0';
    }
public:
    //default constructor
    MyString() : _data(NULL), _len(0) { ++DCtor; }
 
    //constructor
    MyString(const char* p) : _len(strlen(p)){
        ++Ctor;
        _init_data(p);
    }
 
    //copy constructor
    MyString(const MyString& str) : _len(str.len){
        ++CCtor;
        _init_data(str._data);
    }
 
    //move constructor, with "noexcept"
    MyString(MyString&& str) noexcept
        : _data(str._data), _len(str._len){
            ++MCtor;
            str._len = 0;
            str.data = NULL;        //重要
    }
 
    //copy assignment
    MyString& operator=(const MyString& str){
        ++CAsgn;
        if(this != &str){
            if(_data) delete _data;
            _len = str._len;
            _init_data(str._data);
        }
        else{
        }
        return *this;
    }
 
    //move assignment
    MyString& operator=(MyString&& str) noexcept{
        ++MAsgn;
        if(this != &str){
            if(_data) delete _data;
            _len = str._len;
            _data = str._data;
            str._len = 0;
            str._data = NULL;
        }
        return *this;
    }
 
    //dtor
    virtual ~MyString(){
        ++Dtor;
        if(_data){
            delete _data;
        }
    }
 
    bool operator<(const MyString& rhs) const
    {
        return string(this->_data) < string(rhs._data);
    }
 
    bool operator==(const MyString& rhs) const
    {
        return string(this->_data) == string(rhs._data);
    }
 
    char* get() const { return _data; }
};
size_t MyString::DCtor = 0;
size_t MyString::Ctor = 0;
size_t MyString::CCtor = 0;
size_t MyString::CAsgn = 0;
size_t MyString::MCtor = 0;
size_t MyString::MAsgn = 0;
size_t MyString::Dtor = 0;
 
namespace std    //必须放在std内
{
template<>
struct hash<MyString>{    //for unordered containers
    size_t operator()(const MyString& s) const noexcept
    { return hash<string>() (string(s.get())); } 
}；
```



# 六、使用三中定义的MyString测试容器的效能

**测试内容：**

(1)分别使用**定义了move语义**的和**没有定义move语义**的**class**，对容器进行多次插入操作(都只在尾部插入)

(2)测试拷贝容器，move容器，swap两个容器的效率



**测试结果：**

***\*(1)vector的两种时间差别巨大\**，**因为vector要扩容，所以涉及很多拷贝操作，使用move会大大节省时间，**而对于list，deque，multiset和unordered_multiset两种时间差别不大**。但其实按理说deque也可能要搬动元素，但本例中插入的元素都在尾部，所以不涉及搬动操作。

**(2)所有容器都体现出：copy容器耗时很多，move和swap容器几乎不耗时。**这是因为copy容器需要分配空间并依次拷贝元素，但是move容器仅仅是交换了三个指针的值(以vector为例，vector中的三个指针分别是首元素迭代器，尾后迭代器，指示最多容纳元素的迭代器)，自然快得不得了。swap应该也只是交换了指针。



# 五、标准库容器结构

![img](https://img-blog.csdnimg.cn/2020071714291910.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L29uZU5ZVA==,size_16,color_FFFFFF,t_70)

***\*其中标红的三个是C++11新增加的容器\**，其中\**array\**和\**forward_list\**比较简单，\**unordered_containers\**比较重要，可惜缺失了很多内容。**

## **1. array**

其实里面只是一个C语言的数组，只是包装成了一个class的样子。下面是TR1版本(C++03)的源代码，简洁易懂：

```cpp
template<typename _Tp, std::size_t _Nm>
struct array
{
    typedef _Tp            value_type;
    typedef _Tp*           pointer;
    typedef value_type*    iterator;
 
    value_type _M_instance[_Nm ? _Nm : 1];
    
    iterator begin()
    { return iterator(&_M_instance[0]); }
 
    iterator end()
    { return iterator(&_M_instance[_Nm]); }
 
    ......
};
```

注意里面并没有构造函数和析构函数。

与TR1版本不同，GCC4.9array的源码相当复杂，不容易读懂，见视频，这里就不截图了。



## **2. 容器hashtable**

注意这部分并不是新东西，老师也只简单介绍了原理：其实就是使用链地址法解决冲突的哈希表，key的计算方式是对哈希表长度取余，哈希表长度是一个素数。如果hash表放不下了，就要进行rehashing，将哈希表扩容为大概原先的两倍，当然扩容以后也得是个素数。

hashtable里面的key虽然是数字，但里面其实什么对象都能放，只是我们需要告诉它hashfunction是什么，我把hashfunction理解为一个怎样讲对象计算为一个数字的函数。当然最好一个对象能够唯一地对应一个数字。



## **3. hashfunction**

### **(1)标准库的hashfunction的用法**

给**unordered**容器所用的**哈希表**进行算法处理，将每个元素给予其标号的方法。

![img](https://img-blog.csdnimg.cn/20200717150950853.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L29uZU5ZVA==,size_16,color_FFFFFF,t_70)

上图是标准库已有的hashfunction，可以将一些类型转化为size_t的数值。其中`hash<T>代表一个类型，所以hash<T>()就是一个临时对象，并且这是个可调用对象。`

### **(2)标准库的hashfunction定义的逻辑**

以GCC2.9的定义为例：

```cpp
//泛化版本
template <class Key> struct hash { };
 
//很多特化版本
_STL_TEMPLATE_NULL struct hash<char>{                //_STL_TEMPLATE_NULL就是template<>
    size_t operator()(char x) const { return x; }
};
 
_STL_TEMPLATE_NULL struct hash<short>{
    size_t operator()(short x) const { return x; }
};
 
_STL_TEMPLATE_NULL struct hash<unsigned short>{
    size_t operator()(unsigned short x) const { return x; }
};
.......
```

基本逻辑是定义一个空的泛化版本，然后针对各种类型再定义特化的版本。GCC4.9的实现要复杂得多，并且不仅仅定义了整型的hashfunction，还有指针类型，float，double等等等等，但是结构复杂，具体实现原理也不明，有兴趣可以去看PPT。class string之类也有自己的hashfunction，但是是和string定义在一起的。

![在这里插入图片描述](https://img-blog.csdnimg.cn/2019071816145015.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80Mjk3OTY3OQ==,size_16,color_FFFFFF,t_70)

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190718161646498.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80Mjk3OTY3OQ==,size_16,color_FFFFFF,t_70)

 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20190718161823546.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80Mjk3OTY3OQ==,size_16,color_FFFFFF,t_70)



***下面我们来看一下G4.9的源码：***

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190718162022478.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80Mjk3OTY3OQ==,size_16,color_FFFFFF,t_70)

 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20190718162113874.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80Mjk3OTY3OQ==,size_16,color_FFFFFF,t_70)

 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20190718162241976.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80Mjk3OTY3OQ==,size_16,color_FFFFFF,t_70)



### **(3)定义自己的hashfunction------------一个万用的hashfunction(本部分内容缺失，有空对着PPT学一下)**

-  ***形式1：***

前面讲哈希表时说过Hash Function，在为整数时即标号为自己，为字符串类型时进行一个逐位运算。有没有一种可以直接万用的Hash Function呢？我们进行如下学习，见下图：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190523114922951.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80Mjk3OTY3OQ==,size_16,color_FFFFFF,t_70)
同样的东西，左边是成员函数，而右边是全局函数。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190523220626323.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80Mjk3OTY3OQ==,size_16,color_FFFFFF,t_70)
左上角的情况：可以运作，但碰撞很多，太过天真。
而右上角的情况：hash_val根据不同的参数类型，按顺序调用不同的重载的函数（黑色的圈1，圈2，圈3）。其中圈1调用了可变模板参数，逐个处理每一个（**见：**），一步步走到左下方。

综上，来看一下这个Hash Function的源码：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190523220545937.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80Mjk3OTY3OQ==,size_16,color_FFFFFF,t_70)

- ***形式2：***

![在这里插入图片描述](https://img-blog.csdnimg.cn/2019052322161563.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80Mjk3OTY3OQ==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019052322170966.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80Mjk3OTY3OQ==,size_16,color_FFFFFF,t_70)





# 六、tuple

***\*将多个类型整合到一起：\****

![img](https://img-blog.csdnimg.cn/20200717163247296.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L29uZU5ZVA==,size_16,color_FFFFFF,t_70)

不是28而是32的原因，暂无解释。。。
**源码如下：**

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190524170648471.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80Mjk3OTY3OQ==,size_16,color_FFFFFF,t_70)

基础：可变参数模板，简单来说就是：分成一个和一堆，把n分为1和n-1，随后继续将n-1分为1和n-2，这样不断递归。代码中体现为`...`。详**见：**
tuple最神秘的地方：有个private继承，继承一部分自己（Tail部分的自己），故可以**递归继承**，形成上图右边的继承顺序情况。终止条件：递归继承到空的tuple<>。

**来看一下tuple的历史：**

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190718164230839.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80Mjk3OTY3OQ==,size_16,color_FFFFFF,t_70)



![在这里插入图片描述](https://img-blog.csdnimg.cn/20190718164306736.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80Mjk3OTY3OQ==,size_16,color_FFFFFF,t_70)



[C++学习32：侯捷C++11,14新特性（标准库部分）_海洋之心。的博客-CSDN博客](https://blog.csdn.net/weixin_42979679/article/details/96370621?utm_medium=distribute.pc_relevant.none-task-blog-title-3&spm=1001.2101.3001.4242)