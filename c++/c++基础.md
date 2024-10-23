---
title: c++基础
time: 14:37
description: c++基础
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
## 基础语法

### inline内联函数

在编译过程中，没有函数的调用开销了，在函数的调用点直接把函数的代码进行展开处理了。

不是所有的inline都会被编译器处理成内联函数，比如“递归”。

inline只是建议编译器把这个函数处理成内联函数。

debug版本上，inline是不起作用的；inline只有在release版本下才能出现。符号表中不生成符号了。

### C++和C语言代码之间如何互相调用？

C++和C的符号生成规则不同，所以无法直接调用。注意初学要用大型编译器搞，命令行让其跑起来的方式我还不会。

```cpp
//C++调用C 和 C调用C++ 都是在C++里面写 extern
//告诉编译器这个符号用C的规则生成
#ifdef __cplusplus
extern "C"
{
#endif // __cplusplus
	int sum(int a, int b)
	{
		return a + b;
	}
#ifdef __cplusplus
}
#endif // __cplusplus

```

### const

**C里面**：const可以不初始化。const 修饰的量不是常量，是常变量。不能作为左值。`const int a = 10;` 仅仅是语法上的不能被修改（a 这个符号不能被改变，内存可以变）

**C++：**const **必须初始化**，初始值是立即数的叫做常量；是一个变量的可以被看成常变量。所以可以被用来定义数组的大小。

C中const就是被当作一个变量来编译生成指令的。

C++中，所有出现const变量名字的地方，都被常量的初始化替换了。

```cpp
//c语言
#include <stdio.h>

int main()
{
    const int a = 10;
    int *p = (int *)&a;
    *p = 20;
    printf("%d %d %d\n", a, *p, *(&a)); //20 20 20
    return 0;
}

```

同样一份代码，C++ 结果为 `10 20 10` 但是**内存被改变了**。

*(&a) 是被编译器优化了，直接是 a

让C++ 变为 C 的结果方式为将 const 由常量变为常变量。

```cpp
#include <stdio.h>

int main()
{
    int b = 10;
    const int a = b;
    int *p = (int *)&a;
    *p = 20;
    printf("%d %d %d\n", a, *p, *(&a)); //20 20 20
    return 0;
}

```

可以理解成将所有的 a 变成了 变量 b。

#### const 和 一二级指针的结合应用

##### const 和一级指针

const 修饰的量常出现的错误：

1. 常量不能再作为左值
2. 不能把常量的地址泄露给一个普通的指针或者普通的引用变量

**C++语言规范：const修饰的是离它最近的类型。**

```cpp
const int *p;  //去掉int, *p被修饰为const *p不能被修改，但是p可以被修改
int const* p; //和上面的一样
int *const p; //被修饰的是int *      const修饰的是p本身
int a = 1, b = 2;
int* const p = &a;
p = &b; //error!!!!!
int a = 1, b = 2;
int* const p = &a;
*p = 3;
cout << *p; //3

```

```cpp
const int *const p; //第一个const修饰*p 第二个const修饰p本身   严格模式

```

不想把常量的地址泄露给一个普通指针，用这种方法：

```cpp
const int a = 10;
const int *p = &a; //*p不能被修改

```

const 和指针的类型转换公式：

int* <= const int* **错**

const int* <= int* **对**

**const 如果右边没有指针 \* 的话，不参与类型**

```cpp
#include <iostream>
#include <typeinfo>

using namespace std;

int main()
{
	int a = 1;
	int* const p = &a;
	cout << typeid(p).name() << endl; //int *
	return 0;
}
```

##### const 和二级指针

```cpp
int a = 10;
int* p = &a;
const int** q = &p; //error!!!

//*q 是 const int *
//不能把常量的地址泄露给一个普通的指针 普通指针一解引用，就把常量的值改了

//可以这样
int a = 10;
const int* p = &a;
const int** q = &p;
//也可以这样
int a = 10;
int* p = &a;
const int*const* q = &p; //锁死*q

```

```cpp
const int **q; //**q锁定
int *const* q; //*q锁定
int **const q; //q锁定

```

int** <= const int ** **错误**

const int** <= int ** **错误**

`int ** <= int*const*` 错误 const修饰右边的指针，相当于一级指针的 `int* <= const int*`

`int*const* <= int **` 正确 相当于一级指针的`const int* <= int*`

### volatile

[详解volatile在C++中的作用 - teof - 博客园 (cnblogs.com)](https://www.cnblogs.com/s5279551/archive/2010/09/19/1831258.html)

   volatile对基本类型和对用户自定义类型的使用与const有区别，比如你可以把基本类型的non-volatile赋值给volatile，但不能把用户自定义类型的non-volatile赋值给volatile，而const都是可以的。还有一个区别就是编译器自动合成的复制控制不适用于volatile对象，因为合成的复制控制成员接收const形参，而这些形参又是对类类型的const引用，但是不能将volatile对象传递给普通引用或const引用。

### 左值引用和右值引用

引用和指针的区别？

1. 引用必须初始化的，指针可以不初始化。反汇编：引用和指针的底层一样。

   ```
   	int* p = &a;
   00D71FF9  lea         eax,[a]  
   00D71FFC  mov         dword ptr [p],eax  
   	int& b = a;
   00D71FFF  lea         eax,[a]  
   00D72002  mov         dword ptr [b],eax
   
   ```

2. 引用只有一级引用，没有多级引用。指针可以有多级指针。

3. 定义一个引用变量和定义一个指针变量，其汇编指令是一模一样的。都可以修改内存的值。

```cpp
int array[5];
int (*p)[5] = &array;
int(&q)[5] = array;
cout << sizeof(p) << ' ' << sizeof(q);  //4 20

```

使用引用变量时会解引用。array 和 q 是一回事儿。

**左值**：有内存，有名字，值可以被修改

**右值**：没内存（立即数，放在寄存器里面），没名字

C++11提供了右值引用。

1. `int &&c = 10;` 指令上，可以自动产生临时量然后直接引用临时量
2. 一个右值引用变量本身是一个左值。
3. 右值引用不能引用左值，左值引用可以引用右值。

```cpp
int&& a = 10;
a = 30;
const int &b = 20;

```



这两种方式的指令一样：

```
00391FF2  mov         dword ptr [ebp-18h],14h  
00391FF9  lea         eax,[ebp-18h]  
00391FFC  mov         dword ptr [a],eax
```

### const、指针、引用的结合使用

```cpp
int *p1 = (int*)0x0018ff44;
int*&&p2 = (int *)0x0018ff44;
int *const &p3 = (int*)0x0018ff44;
```

&和* 右边的一个`&`将左边的一个 `*` 变为`&`

```cpp
int a = 10;
int* const p = &a;
int *& q = p; //error 把常量地址泄露给普通指针   int *const& q = p;
```

## new 和 delete

1. malloc 和 free，称作 C 的库函数；new 和 delete，称作运算符
2. new 不仅可以做内存开辟，还可以做内存初始化操作
3. malloc开辟内存失败，是通过返回值和nullptr作比较；new开辟内存失败，是通过抛出bad_alloc类型的异常来判断的。

## 类和对象

```cpp
#include <iostream>

using namespace std;

const int NAME_LEN = 20;
class CGoods //类名最好用C开始 
{
	//类的成员方法一经编译,所有的方法参数都会加一个this指针,接收该方法的对象的地址
public: //给外部提供共有的方法来访问私有的属性
	void init(const char* name, double price, int amount); //商品数据初始化
	void show(); //打印商品信息
	//给成员变量提供一组getxxx或setxxx的方法
	void setName(const char* name) { strcpy(_name, name); } //类体内实现的方法,自动处理成inline内联函数
	const char* getName() { return _name; }//防止解引用修改
private: //属性一般都是私有的
	//总共40个字节
	char _name[NAME_LEN]; //按最长的8对齐  20 + 4
	double _price; //8
	int _amount; //4 + 4
};

void CGoods::init(const char* name, double price, int amount)
{
	strcpy(_name, name);
	_price = price;
	_amount = amount;
}

void CGoods::show()
{
	cout << _name << endl;
	cout << _price << endl;
	cout << _amount << endl;
}

int main()
{
	//对象的内存大小只和成员变量有关
	CGoods good;
	good.init("面包", 10.5, 200);
	good.setName("小面包");
	good.show();
	return 0;
}

```

### 构造函数和析构函数

先构造的后析构。

析构函数不带参数，所以析构函数只能有一个；构造函数可以提供多个，叫做**重载**。

堆上的对象要手动析构， 也就是new 和 delete

### this指针

类的成员方法一经编译，所有的方法参数都会加一个this指针， 接收调用该方法的对象的地址

### 对象的深拷贝和浅拷贝

有**指针**指向对象的**外部资源**时，**浅拷贝**的析构会出问题：先构造的指针变成了野指针。

`CTest t3 = t1;` 默认拷贝构造函数，浅拷贝

拷贝时扩容用 for 循环， 不用 memcpy 原因：避免指向外部的指针指向同一块

```cpp
#include <iostream>

using namespace std;
class CTest
{
public:
	CTest(int size)
	{
		this->_size = size;
		_p = new int[size];
		cout << this << "构造" << endl;
	}
	//自定义拷贝构造函数，对象的浅拷贝有问题了
	CTest(const CTest& t)
	{
		_p = new int[t._size];
		for (int i = 0; i < t._size; i++) { //扩容用for循环，不用memcpy 原因：仍然是指针
			_p[i] = t._p[i];
		}
		cout << this << "深拷贝" << endl;
	}
	~CTest()
	{
		delete[] _p;
		_p = nullptr;
		cout << this << "析构" << endl;
	}
private:
	int _size;
	int* _p;
};

int main()
{
	CTest t1(10);
	CTest t3 = t1;
	return 0;
}
```

#### 类的各类成员方法以及区别

普通的成员方法 =》编译器会添加一个 this 形参变量

1. 属于类的作用域
2. 调用该方法时，需要依赖一个对象
3. 可以任意访问对象的私有成员变量

static静态成员方法 =》 不会生成 this 形参

1. 属于类的作用域
2. 用类名作用域来调用方法
3. 可以任意访问对象的私有对象，仅限于不依赖对象的成员（只能调用其它的static静态成员）

const常成员方法 =》 const CGoods *this

1. 属于类的作用域
2. 调用依赖一个对象，普通对象或者常对象都可以
3. 可以任意访问对象的私有成员，但是只能读不能写

```cpp
#include <iostream>

using namespace std;

class Test
{
public:
	Test()
	{
		cnt++;
	}
	static int staticgetCnt() //静态成员方法，调用时不需要this指针
	{
		return cnt;
	}
	//常成员方法 只要是只读操作，一律实现为const方法
	int getCnt() const
	{
		return cnt;
	}
private:
	static int cnt; //声明 不属于对象，属于类级别的
};

int Test::cnt = 0;

int main()
{
	Test t1, t2;
	cout << t1.getCnt() << endl;
	cout << Test::staticgetCnt() << endl; //直接用类的作用域调
	const Test t3; //常对象无法调用普通方法，因为传的形参无法从const转为普通
	cout << t3.getCnt() << endl;
	return 0;
}
```

#### 指向类成员（成员变量和成员方法）的指针

```cpp
#include <iostream>

using namespace std;

class Test
{
public:
	void func() { cout << "call Test::func" << endl; }
	static void static_func() { cout << "static_func" << endl; }
	int ma;
	static int mb;
};

int Test::mb; 

int main()
{
	Test t1;
	Test* t2 = new Test();
	int Test::* p = &Test::ma; //类的指针

	t1.*p = 20;
	cout << t1.ma << endl;

	t2->*p = 30;
	cout << t2->*p << endl;

	int* p1 = &Test::mb; //不依赖于对象
	*p1 = 40;
	cout << t1.mb << endl;

	//指向成员方法的指针
	void(Test::*pfunc)() = &Test::func;
	(t1.*pfunc)(); //要依赖于对象调用

	//指针指向类的static成员方法
	void(*pfunc2)() = &Test::static_func;
	(*pfunc2)();

	delete t2;
	return 0;
}
```

## 模板编程

### 理解函数模板

模板只定义，不编译。如果将其放到另外一个文件中，如果没有对应的特例化将出错。

所以模板代码都是放在头文件中，然后在源文件中 #include 包含。

```cpp
#include <iostream>

using namespace std;

template<typename T> //typename 或 class
bool compare(T a, T b) //compare是一个函数模板 是无法编译的
{
	cout << "template compare" << endl;
	return a > b;
}

//模板特例化(比如比较字符串大小,原方案只能比较地址大小)
template<>
bool compare<const char*>(const char* a, const char* b)
{
	cout << "const char * compare" << endl;
	return strcmp(a, b) > 0;
}

//非模板函数   
bool compare(const char* a, const char* b)
{
	cout << "非模板函数" << endl;
	return true;
}

/*
在函数调用点,编译器用用户指定的类型,从原模板实例化一份函数代码出来
*/
int main()
{
	cout << compare<int>(1, 2) << endl; //函数的调用点
	cout << compare<double>(1.2, 1.1) << endl;
	cout << compare(2, 3) << endl; //模板的实参推演 
	//compare(10, 10.1);  //error 推导不出类型
	cout << compare<int>(10, 10.1) << endl; //强制转化 或 模板函数那里两个T
	cout << compare("aaa", "bbb") << endl; //优先普通函数
	cout << compare<const char*>("aaa", "bbb") << endl; //强制模板函数
	return 0;
}
```

### 类模板

演示下 template 用 T 以外的其它参数

可以加默认 T 参数。 但是声明时 `<>` 要写

```cpp
#include<iostream>
using namespace std;

template<typename T, int SIZE>	// SIZE模板的非类型参数，都是常量,只能使用而不能修改
void sort(T* arr) {}

int main()
{
	int arr[] = { 1,2,5,4,3 };
	const int size = sizeof(arr) / sizeof(arr[0]);
	sort<int, size>(arr);
	return 0;
}
```

构造和析构函数名不用加`<T>`，其它出现模板的地方都要加上类型参数列表。

类模板无非就是将存数据的类型改为 T

```cpp
template<typename T>
class SeqStack
{
public:
	void push(const T& val);
};

template<typename T>
void SeqStack<T>::push(const T& val)
{

}
```

### 实现STL向量容器vector代码

```cpp
#include <iostream>

using namespace std;

/*
实现 vector 向量容器
*/
template<typename T>
class vector
{
public:
	vector(int size = 10)
	{
		_first = new T[size];
		_last = _first;
		_end = _first + size;
	}
	~vector()
	{
		delete[]_first;
		_first = _last = _end = nullptr;
	}
	vector(const vector<T>& rhs)
	{
		int size = rhs._end - rhs._first;
		_first = new T[size];
		int len = rhs._last - rhs._first;
		for (int i = 0; i < len; ++i)
		{
			_first[i] = rhs._first[i];
		}
		_last = _first + len;
		_end = _first + size;
	}
	vector<T>& operator=(const vector<T>& rhs)
	{
		if (this == &rhs)
			return *this;
		delete[]_first;
		int size = rhs._end - rhs._first;
		_first = new T[size];
		int len = rhs._last - rhs._first;
		for (int i = 0; i < len; ++i)
		{
			_first[i] = rhs._first[i];
		}
		_last = _first + len;
		_end = _first + size;
		return *this;
	}
	void push_back(const T &val)
	{
		if (full())
			expand();
		*_last++ = val;
	}
	void pop_back()
	{
		if (empty())
			return;
		--_last;
	}
	T back() const
	{
		return *(_last - 1); //空的情况没写
	}
	bool full() const { return _last == _end; }
	bool empty() const { return _first == _last; }
	int size() const { return _last - _first; }
private:
	T* _first; //起始
	T* _last; //有效元素的后继位置
	T* _end; //数组空间的后继位置
	void expand() 
	{
		int size = _end - _first;
		T* ptmp = new T[2 * size];
		for (int i = 0; i < size; i++)
		{
			ptmp[i] = _first[i];
		}
		delete[]_first;
		_first = ptmp;
		_last = _first + size;
		_end = _first + size * 2;
	}
};


int main()
{
	vector<int>vec;
	for (int i = 0; i < 20; i++)
		vec.push_back(rand() % 100);
	while (!vec.empty())
	{
		cout << vec.back() << ' ';
		vec.pop_back();
	}
	return 0;
}
```

### 理解容器空间配置器allocator的重要性

上个代码存在以下问题：

构造：需要把内存开辟和对象构造分开处理

析构：析构容器有效的元素，然后释放_first指针指向的堆内存

pop_back：只需要析构对象。要把对象的析构和内存释放分开

```cpp
#include <iostream>

using namespace std;

/*
容器的空间配置器
*/
template<typename T>
class Allocator
{
public:
	T* allocate(size_t size) //负责内存开辟
	{
		return (T*)malloc(sizeof(T) * size);
	}
	void deallocate(void* p) //负责内存释放
	{
		free(p);
	}
	void construct(T* p, const T& val) //负责对象构造
	{
		new (p) T(val); //定位new  指定内存上构造
	}
	void destroy(T* p) //负责对象析构
	{
		p->~T(); //~T()代表了T类型的析构函数
	}
}
;


/*
实现 vector 向量容器
容器底层内存开辟,内存释放,对象构造和析构,都通过allocator空间配置器来实现
*/
template<typename T, typename Alloc = Allocator<T>>
class vector
{
public:
	vector(int size = 10)
	{
		//需要把内存开辟和对象构造分开处理
		//_first = new T[size];
		_first = _allocator.allocate(size);
		_last = _first;
		_end = _first + size;
	}
	~vector()
	{
		//delete[]_first;
		for (T* p = _first; p != _last; p++)
		{
			_allocator.destroy(p); //把_first指针指向的有效元素析构
		}
		_allocator.deallocate(_first); //释放堆上的内存
		_first = _last = _end = nullptr;
	}
	vector(const vector<T>& rhs)
	{
		int size = rhs._end - rhs._first;
		//_first = new T[size];
		_first = _allocator.allocate(size);
		int len = rhs._last - rhs._first;
		for (int i = 0; i < len; ++i)
		{
			//_first[i] = rhs._first[i];
			_allocator.construct(_first + 1, rhs._first[i]);
		}
		_last = _first + len;
		_end = _first + size;
	}
	vector<T>& operator=(const vector<T>& rhs)
	{
		if (this == &rhs)
			return *this;
		//delete[]_first;
		for (T* p = _first; p != _last; p++)
		{
			_allocator.destroy(p); //把_first指针指向的有效元素析构
		}
		_allocator.deallocate(_first);

		int size = rhs._end - rhs._first;
		//_first = new T[size];
		_first = _allocator.allocate(size);
		int len = rhs._last - rhs._first;
		for (int i = 0; i < len; ++i)
		{
			//_first[i] = rhs._first[i];
			_allocator.construct(_first + 1, rhs._first[i]);
		}
		_last = _first + len;
		_end = _first + size;

		return *this;
	}
	void push_back(const T &val)
	{
		if (full())
			expand();
		//*_last++ = val;
		_allocator.construct(_last, val);
		_last++;
	}
	void pop_back()
	{
		if (empty())
			return;
		//--_last;
		//析构删除的元素
		--_last;
		_allocator.destroy(_last);
	}
	T back() const
	{
		return *(_last - 1); //空的情况没写
	}
	bool full() const { return _last == _end; }
	bool empty() const { return _first == _last; }
	int size() const { return _last - _first; }
private:
	T* _first; //起始
	T* _last; //有效元素的后继位置
	T* _end; //数组空间的后继位置
	Alloc _allocator; //定义容器的空间配置器对象

	void expand() 
	{
		int size = _end - _first;
		//T* ptmp = new T[2 * size];
		T* ptmp = _allocator.allocate(2 * size);
		for (int i = 0; i < size; i++)
		{
			_allocator.construct(ptmp + i, _first[i]);
			//ptmp[i] = _first[i];
		}
		//delete[]_first;
		for (T* p = _first; p != _last; ++p)
		{
			_allocator.destroy(p);
		}
		_allocator.deallocate(_first);
		_first = ptmp;
		_last = _first + size;
		_end = _first + size * 2;
	}
};

class Test
{
public:
	Test() { cout << "Test()" << endl; }
	~Test() { cout << "~Test()" << endl; }
	Test(const Test&) { cout << "Test(const Test&)" << endl; }
};


int main()
{
	Test t1, t2, t3;
	cout << "----" << endl;
	vector<Test>vec;
	vec.push_back(t1);
	vec.push_back(t2);
	vec.push_back(t3);
	cout << "----" << endl;
	vec.pop_back();
	cout << "----" << endl;
	return 0;
}
```

## 运算符重载

### 模拟实现C++的string类代码

```cpp
#include <iostream>

using namespace std;

class String
{
public:
	String(const char* p = nullptr)
	{
		if (p != nullptr)
		{
			_pstr = new char[strlen(p) + 1];
			strcpy(_pstr, p);
		}
		else 
		{
			_pstr = new char[1];
			*_pstr = '\0';
		}
	}
	~String()
	{
		delete[]_pstr;
		_pstr = nullptr;
	}
	String(const String& str)
	{
		_pstr = new char[strlen(str._pstr) + 1];
		strcpy(_pstr, str._pstr);
	}
	String& operator=(const String& src)
	{
		if (this == &src)
			return *this;
		delete[]_pstr;
		_pstr = new char[strlen(src._pstr) + 1];
		strcpy(_pstr, src._pstr);
		return *this; 
	}
	bool operator>(const String& str) const
	{
		return strcmp(_pstr, str._pstr) > 0;
	}
	bool operator<(const String& str) const
	{
		return strcmp(_pstr, str._pstr) < 0;
	}
	bool operator==(const String& str) const
	{
		return strcmp(_pstr, str._pstr) == 0;
	}
	int length()
	{
		return strlen(_pstr);
	}
	char& operator[](int index)
	{
		return _pstr[index];
	}
	const char& operator[](int index) const
	{
		return _pstr[index];
	}
	const char* c_str() const { return _pstr; }
private:
	char* _pstr;
	friend ostream& operator<<(ostream& out, const String& str);
	friend String operator+(const String& lhs, const String& rhs);
};

String operator+(const String& lhs, const String& rhs)
{
	String tmp;
	tmp._pstr = new char[strlen(lhs._pstr) + strlen(rhs._pstr) + 1];
	strcpy(tmp._pstr, lhs._pstr);
	strcat(tmp._pstr, rhs._pstr);
	return tmp; 
}

ostream& operator<<(ostream& out, const String& str)
{
	out << str._pstr;
	return out;
}

int main()
{
	String s1;
	String s2 = "aa";
	String s3 = s2;
	String s4 = s3 + "bb";
	String s5 = "cc" + s2;
	cout << s4 << endl;
	cout << s5 << endl;
	cout << (s3 < s4) << endl;
	return 0;
}

```

### string字符串对象的迭代器iterator实现

```cpp
#include <iostream>

using namespace std;

class String
{
public:
	String(const char* p = nullptr)
	{
		if (p != nullptr)
		{
			_pstr = new char[strlen(p) + 1];
			strcpy(_pstr, p);
		}
		else 
		{
			_pstr = new char[1];
			*_pstr = '\0';
		}
	}
	~String()
	{
		delete[]_pstr;
		_pstr = nullptr;
	}
	String(const String& str)
	{
		_pstr = new char[strlen(str._pstr) + 1];
		strcpy(_pstr, str._pstr);
	}
	String& operator=(const String& src)
	{
		if (this == &src)
			return *this;
		delete[]_pstr;
		_pstr = new char[strlen(src._pstr) + 1];
		strcpy(_pstr, src._pstr);
		return *this; 
	}
	bool operator>(const String& str) const
	{
		return strcmp(_pstr, str._pstr) > 0;
	}
	bool operator<(const String& str) const
	{
		return strcmp(_pstr, str._pstr) < 0;
	}
	bool operator==(const String& str) const
	{
		return strcmp(_pstr, str._pstr) == 0;
	}
	int length()
	{
		return strlen(_pstr);
	}
	char& operator[](int index)
	{
		return _pstr[index];
	}
	const char& operator[](int index) const
	{
		return _pstr[index];
	}
	const char* c_str() const { return _pstr; }

	//给string提供迭代器的实现
	class iterator
	{
	public:
		iterator(char*p = nullptr):_p(p){}
		bool operator !=(const iterator& it)
		{
			return _p != it._p;
		}
		void operator++()
		{
			++_p;
		}
		char& operator*()
		{
			return *_p;
		}
	private:
		char* _p;
	};
	//首元素迭代器的表示
	iterator begin() 
	{
		return iterator(_pstr);
	}
	iterator end()
	{
		return iterator(_pstr + length());
	}

private:
	char* _pstr;
	friend ostream& operator<<(ostream& out, const String& str);
	friend String operator+(const String& lhs, const String& rhs);
};

String operator+(const String& lhs, const String& rhs)
{
	String tmp;
	tmp._pstr = new char[strlen(lhs._pstr) + strlen(rhs._pstr) + 1];
	strcpy(tmp._pstr, lhs._pstr);
	strcat(tmp._pstr, rhs._pstr);
	return tmp; 
}

ostream& operator<<(ostream& out, const String& str)
{
	out << str._pstr;
	return out;
}

int main()
{
	String str1 = "Hello World";
	String::iterator it = str1.begin();
	for (; it != str1.end(); ++it)
	{
		cout << *it;
	}
	cout << endl;

	for (char ch : str1) //begin() 和 end()实现
	{
		cout << ch; 
	}
	return 0;
}

```

### vector容器的迭代器iterator实现

泛型算法：参数接收的都是容器的迭代器

内置类

```cpp
class iterator
{
    public:
    iterator(T*ptr = nullptr)
        :_ptr(ptr){}
    bool operator !=(const iterator& it) const
    {
        return _ptr != it._ptr;
    }
    //前置++  即++it
    void operator++()
    {
        _ptr++;
    }
    T& operator*() { return *_ptr; }
    const T& operator*() const { return *_ptr; }
    private:
    T* _ptr;
};
iterator begin()
{
    return iterator(_first);
}
iterator end()
{
    return iterator(_last);
}

```

### 什么是容器的迭代器失效问题

迭代器在 erase 后失效；迭代器在 insert 之后失效

失效原因

1. 当容器调用 erase 后，当前位置到容器末尾元素的所有的迭代器全部失效了
2. 当容器调用 insert 后，当前位置到容器末尾元素的所有的迭代器全部失效了。
3. 如果 insert 引起扩容，原来容器的所有的迭代器全部失效。
4. 不同容器的迭代器不能进行比较运算

[面试题：vector迭代器什么时候会失效？_vector 迭代器什么时候失效_clw_18的博客-CSDN博客](https://blog.csdn.net/weixin_49199646/article/details/109264858)

### new和delete重载实现的对象池应用

```cpp
#include <iostream>
//#include <string>

using namespace std;

template<typename T>
class Queue
{
public:
	Queue()
	{
		_front = _rear = new QueueItem();
	}
	~Queue()
	{
		QueueItem* cur = _front;
		while (cur != nullptr)
		{
			_front = _front->_next;
			delete cur;
			cur = _front;
		}
	}
	void push(const T& val)
	{
		QueueItem *item = new QueueItem(val);
		_rear->_next = item;
		_rear = item;
	}
	void pop()
	{
		if (empty())
			return;
		QueueItem* first = _front->_next;
		_front->_next = first->_next;
		if (_front->_next == nullptr)
		{
			_rear = _front;
		}
		delete first;
	}
	T front() const
	{
		return _front->_next->_data;
	}
	bool empty() const { return _front == _rear; }
private:
	struct QueueItem //节点
	{
		QueueItem(T data = T()):_data(data), _next(nullptr){}
		//给QueueItem提供自定义内存管理
		void* operator new(size_t size)
		{
			if (_itemPool == nullptr) //用满了itemPool就是nullptr了
			{
				_itemPool = (QueueItem*)new char[POOL_ITEM_SIZE * sizeof(QueueItem)];
				QueueItem* p = _itemPool;
				for (; p < _itemPool + POOL_ITEM_SIZE - 1; ++p) //最后一个是nullptr
				{
					p->_next = p + 1;
				}
				p->_next = nullptr;
			}

			QueueItem* p = _itemPool;
			_itemPool = _itemPool->_next;
			return p;
		}
		void operator delete(void* ptr)
		{
			QueueItem* p = (QueueItem*)ptr;
			p->_next = _itemPool;
			_itemPool = p;
		}
		T _data;
		QueueItem* _next;
		static QueueItem* _itemPool; 
		static const int POOL_ITEM_SIZE = 1000000;
	};

	QueueItem* _front; //头
	QueueItem* _rear; //尾
};

template<typename T>
typename Queue<T>::QueueItem *Queue<T>::QueueItem::_itemPool = nullptr;

int main()
{
	Queue<int> que;
	for (int i = 0; i < 10000000; ++i)
	{
		que.push(i);
		que.pop();
	}
	cout << que.empty() << endl;
	return 0;
}

```

## 继承与多态

### 重载、隐藏、覆盖

子类可以调用基类的函数，但是一旦子类自定义同名函数，父类的该函数名不能被用。

**1.重载关系**

一组函数要重载，必须处在**同一个作用域**当中；并且函数名字相同，参数列表不同

**2.隐藏（作用域隐藏）关系**

在继承结构当中，派生类的同名成员，把基类的同名成员给隐藏调用了

**3.覆盖关系**

基类和派生类的方法，返回值、函数名以及参数列表都相同，而且基类的方法是虚函数，那么派生类的方法就自动处理成虚函数，它们之间成为覆盖关系。

**在继承结构中进行上下的类型转换，默认只支持从下到上的转换**

```cpp
#include<iostream>

using namespace std;

class Base
{
public:
	Base(int data = 10) : ma(data) {}
	void show() { cout << "Base::show()" << endl; }
	void show(int) { cout << "Base::show(int)" << endl; }
protected:
	int ma;
};

class Derive : public Base
{
public:
	Derive(int data = 20):Base(data), mb(data){}
	void show() { cout << "Derive::show()" << endl; }
private:
	int mb;
};

int main()
{
	Base b;
	Derive d;
	//d.show();
	//d.show(10); //error
	//d.Base::show();
	
	//基类 <- 派生 类型从下到上 Y
	//b = d;
	//派生 <- 基类 类型从上到下 N
	//d = b;

	//基类指针(引用) <- 派生类对象 类型从下到上 Y
	Base* pb = &d; //指针的类型的基类,限制了指针访问的内容只是派生类里面基类的内容
	pb->show();
	//((Derive*)pb)->show();  //非常危险 涉及内存的非法访问
	pb->show(10); 

	//派生类指针（引用）<- 基类对象 类型从上到下 N
	//指针解引用后非法内存越界访问
	//Derive* pd = &b; //error

	return 0;
}
```

### 虚函数、静态绑定和动态绑定

#### 静态绑定

```cpp
#include<iostream>
#include <typeinfo>

using namespace std;

class Base
{
public:
	Base(int data = 10) : ma(data) {}
	void show() { cout << "Base::show()" << endl; }
	void show(int) { cout << "Base::show(int)" << endl; }
protected:
	int ma;
};

class Derive : public Base
{
public:
	Derive(int data = 20):Base(data), mb(data){} //给基类继承来的初始化下
	void show() { cout << "Derive::show()" << endl; }
	void getma() { cout << "ma " << ma << endl; }
private:
	int mb;
};

int main()
{
	Derive d(50);
	Base* pb = &d;
	pb->show(); //静态(编译时期)的绑定(函数的调用) call Base::show(010112DAh)
	pb->show(10); //静态绑定 call Base::show (010112B2h)
	
	cout << sizeof(Base) << endl << sizeof(Derive) << endl; 
	cout << typeid(pb).name() << endl;
	cout << typeid(*pb).name() << endl;

	return 0;
}

/*
Base::show()
Base::show(int)
4
8
class Base *
class Base
*/

```

#### 动态绑定

```cpp
#include<iostream>
#include <typeinfo>

using namespace std;
/*
一个类添加了虚函数,对这个类有什么影响?
总结一
一个类里面定义了虚函数,那么编译阶段,编译器给这个类类型产生
一个唯一的vftable虚函数表,虚函数表中主要存储的内容就是RTTI指针和虚函数的地址
当程序运行时,每一张虚函数表都会加载 到.rodata区(只读 不能写)

总结二
一个类里面定义了虚函数,那么这个类定义的对象,其运行时,内存中开始部分,
多存储一个vfptr虚函数指针,指向相应类型的虚函数表vftable。
一个类型定义的n个对象，它们的额外vfptr指向的都是同一张虚函数表

总结三
一个类里面虚函数的个数，不影响对象内存的大小（vfptr），影响的是虚函数表的大小
*/
#if 1
class Base
{
public:
	Base(int data = 10) : ma(data) {}
	virtual void show() { cout << "Base::show()" << endl; }
	virtual void show(int) { cout << "Base::show(int)" << endl; }
protected:
	int ma;
};

class Derive : public Base
{
public:
	Derive(int data = 20):Base(data), mb(data){} //给基类继承来的初始化下
	/*
	总结四
	如果派生类中的方法，和基类继承来的某个方法，
	返回值、函数名、参数列表都相同，
	而且基类的方法是virtual虚函数，
	那么这个派生类的这个方法，自动处理为虚函数
	重写《=》覆盖
	*/
	void show() { cout << "Derive::show()" << endl; }
private:
	int mb;
};

int main()
{
	Derive d(50);
	Base* pb = &d; //vfptr指针 + ma ,8个字节

	/*
	如果发现show()是普通函数，就静态绑定
	如果发现show()是虚函数，就进行动态绑定
	*/
	/*
	006A294F  mov         ecx,dword ptr [pb]     vfptr
	006A2952  mov         eax,dword ptr [edx+4]  虚函数表
	006A2955  call        eax
	*/
	//需要在编译时确定调用哪个函数
	pb->show(); //动态的绑定
	pb->show(10); //动态绑定 虽然没重写
	
	cout << sizeof(Base) << endl << sizeof(Derive) << endl;
	cout << typeid(pb).name() << endl;
	//Base有虚函数,*pb实现的是运行时期的类型
	cout << typeid(*pb).name() << endl;  // 虚函数表中的RTTI存着，这里是Derive

	return 0;
}

#endif

```

![image-20230401151955907](https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/image-20230401151955907.png)

![image-20230401152410778](https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/image-20230401152410778.png)

 

### 虚析构函数

**哪些函数不能实现成虚函数？**

1. 构造函数不能用 virtual，因为构造完成了才产生对象
2. 构造函数中调用的任何函数都是静态绑定，不会发生动态绑定  派生类对象构造都是先调用的基类构造
3. static 静态，因为static 不依赖对象

**虚函数依赖：  **

1. 虚函数能产生地址，存储在vftable当中
2. 对象必须存在（vfptr -> vftable -> 虚函数地址）

**虚析构函数**

析构函数可以成为虚函数。因为析构函数调用时对象存在。

**==基类的指针指向堆上 new 出来的派生类对象时==，它调用析构函数的时候必须发生动态绑定，否则会导致派生类的析构无法调用。**

```cpp
#include <iostream>
#include <typeinfo>

using namespace std;
class Base
{
public:
	Base(int data)
	{
		ma = data;
		cout << "Base()" << endl;
	}
	~Base()
	{
		cout << "~Base()" << endl;
	}
	virtual void show() 
	{
		cout << "Base::show()" << endl;
	}
private:
	int ma;
};

class Derive : public Base
{
public:
	Derive(int data) :
		Base(data), mb(data)
	{
		cout << "Device()" << endl;
	}
	~Derive()
	{
		cout << "~Device()" << endl;
	}
	void show()
	{
		cout << "Derive::show()" << endl;
	}
private:
	int mb;
};

int main()
{
	Base* pb = new Derive(10);
  cout<< typeid(*pb).name() << endl;  // derive
  cout << typeid(pb).name() << endl;  // base*
  pb->show(); //派生类的析构函数没有被调用

  delete pb;
  /*
   * pb->base   Base::~Base()  对于析构函数的绑定是静态绑定
   * 没有机会调用到~Derive()
   * */
  return 0;
}
/*
Base()
Device()
Derive::show()
~Base()
*/

```

pb 的类型是 Base，析构函数是普通函数，静态绑定。

解决方案：将基类的析构函数变为虚函数。

```cpp
virtual ~Base()
{
    cout << "~Base()" << endl;
}

```

再跑一遍，结果为

```cpp
Base()
Device()
Derive::show()
~Device()
~Base()
```

### 再谈动态绑定

是不是虚函数的调用一定就是动态绑定？ 不是

1. 在类的构造函数中，调用虚函数，也是静态绑定（构造函数中不会发生动态）
2. 如果不是通过指针或引用变量来调用虚函数，那就是静态绑定

```cpp
#include <iostream>
#include <typeinfo>

using namespace std;
class Base
{
public:
	Base(int data = 10)
	{
		ma = data;
		cout << "Base()" << endl;
	}
	virtual ~Base()
	{
		cout << "~Base()" << endl;
	}
	virtual void show() 
	{
		cout << "Base::show()" << endl;
	}
private:
	int ma;
};

class Derive : public Base
{
public:
	Derive(int data = 10) :
		Base(data), mb(data)
	{
		cout << "Device()" << endl;
	}
	~Derive()
	{
		cout << "~Device()" << endl;
	}
	void show()
	{
		cout << "Derive::show()" << endl;
	}
private:
	int mb;
};

int main()
{
	Base b;
	Derive d;

	//不涉及前四个字节的指针
	//静态绑定 用对象本身调用虚函数，是静态绑定
	b.show(); //虚函数  call Base::show (06B1451h)
	d.show(); //虚函数

	//move move call 动态绑定（必须由指针调用虚函数）
	Base* pb1 = &b;
	pb1->show();
	Base* pb2 = &d;
	pb2->show();

	//仍然是动态绑定
	Base& rb1 = b;
	rb1.show();
	Base& rb2 = d;
	rb2.show();

	//仍然是动态绑定
	Derive* pd1 = &d;
	pd1->show();
	Derive& rd1 = d;
	rd1.show();

	//流氓强转类型
	Derive* pd2 = (Derive*)&b; //只能访问基类的表
	pd2->show(); //b的里面只有Base的函数

	return 0;
}

```

### 理解多态到底是什么

静态（编译时期）的多态：函数重载、模板（函数模板和类模板）

动态（运行时期）的多态：在继承结构中，基类指针（引用）指向派生类对象，通过该指针（引用）调用同名覆盖 方法（**虚函数**）。**基类指针**指向哪个派生类对象，就会调用哪个派生类对象的同名覆盖方法，称为多态。

多态底层是通过动态绑定来实现的。pbase 访问谁的 vfptr 就继续访问谁的 vftable，当然调用的是对应的派生类对象的方法了。

软件设计“开-闭”原则：对修改关闭，对拓展开放

继承的好处

1. 代码的复用
2. 在基类中提供统一的虚函数接口，让派生类进行重写，然后就可以使用多态了

### 理解抽象类

拥有纯虚函数的类叫做抽象类
抽象类不能再实例化对象了，但是可以定义指针和引用变量

```cpp
/*
1. 让所有的动物实体类通过继承Animal直接复用该属性
2. 给所有的派生类保留统一的覆盖/重写接口
*/
class Animal
{
public:
	Animal(string name):_name(name){}
	virtual void bark() = 0; //纯虚函数
protected:
	string _name;
};

```

### 笔试实战

#### 第一题

前四个字节是 vfptr ，指向的是当前对象的 vftable

<img src="https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/image-20230401162143524.png" alt="image-20230401162143524" style="zoom: 25%;" />

#### 第二题

```cpp
#include<iostream>

using namespace std;

class Base
{
public:
	virtual void show (int i = 10)
	{
		cout << "Base::show i:" << i << endl;
	}
};

class Derive : public Base
{
public:
	void show(int i = 20)
	{
		cout << "Derive::show i:" << i << endl;
	}
};

int main()
{
	Base* p = new Derive();
	p->show();	
	delete p;
	return 0;
}
/*
Derive::show i:10
*/

```

这个输出我第一次看到感到难以理解。**为什么**调用`show()`函数输出的是派生类，而输出的 i 是 10 ？

编译阶段p 只是base* ，因此入栈的是base 的参数

参数是编译时期压栈

```
008B2923  push        0Ah   =>  函数调用,参数压栈是在编译时期就确定好的
008B2925  mov         eax,dword ptr [p]  
008B2928  mov         edx,dword ptr [eax]  
008B292A  mov         ecx,dword ptr [p]  
008B292D  mov         eax,dword ptr [edx]  
008B292F  call        eax  
```

==**派生类的构造函数的默认值没有用**==

#### **第三题**

派生类的构造函数为 private

```cpp
#include<iostream>

using namespace std;

class Base
{
public:
	virtual void show ()
	{
		cout << "Base::show" << endl;
	}
};

class Derive : public Base
{
private:
	void show()
	{
		cout << "Derive::show" << endl;
	}
};

int main()
{
	Base* p = new Derive();
	p->show(); 
	delete p;
	return 0;
}

```

正常调用

最终能调用带Derive::show()，是在**运行时期**才确定的。

成员方法能不能调用，就是说方法的访问权限是不是public的，是在**编译阶段**就需要确定好的

如果把基类的构造函数标为private将编译出错

```cpp
#include<iostream>

using namespace std;

class Base
{
private:
	virtual void show ()
	{
		cout << "Base::show" << endl;
	}
};

class Derive : public Base
{
public:
	void show()
	{
		cout << "Derive::show" << endl;
	}
};

int main()
{
	Base* p = new Derive();
	p->show();  //error C2248: “Base::show”: 无法访问 private 成员(在“Base”类中声明)
	delete p;
	return 0;
}

```

#### **第四题**

构造函数的左大括号写入的虚指针

```cpp
#include<iostream>

using namespace std;

class Base
{
public:
	Base()
	{
		/*
		push ebp  压栈
		mov ebp, esp
		sub esp, 4Ch
		rep stos esp <-> ebp 0xCCCCCCCC(windows vs)
		vfptr <- &Base::vftable
		*/
		cout << "Base()" << endl;
		clear();
	}
	//~Base()
	//{
	//	cout << "~Base()";
	//}
	void clear()
	{
		memset(this, 0, sizeof(*this));
	}
	virtual void show ()
	{
		cout << "Base::show" << endl;
	}
};

class Derive : public Base
{
public :
	Derive()
	{
		/*
		vfptr <- &Derive::vftable
		*/
		cout << "Derive()" << endl;
	}
	//~Derive()
	//{
	//	cout << "~Derive()" << endl;
	//}
	void show()
	{
		cout << "Derive::show" << endl;
	}
};

int main()
{
	/*
	第一种情况虚函数指针为空,动态绑定时程序崩溃
	*/
	//Base* pb1 = new Base(); //error
	//pb1->show(); //动态绑定
	//delete pb1;

	/*
	vfptr里面存储的是vftable的地址
	vfptr <- vftable 要有这个指令写入指针
	*/
	Base* pb2 = new Derive();
	pb2->show();
	delete pb2;
	return 0;
}

```

# 多重继承的那些坑

多重继承：代码的复用 一个派生类有多个基类

```cpp
class C: public A, public B
{
};
```

## 理解虚基类和虚继承

抽象类：有纯虚函数的类

虚基类：被虚继承的类，称作虚基类

virtual：

1. 修饰成员方法是虚函数
2. 可以修饰继承方式，是虚继承。被虚继承的类，称作虚基类

当一个类有虚函数，这个类生成 vfptr ，指向 vftable

vbptr 指向 vbtable，派生类虚继承而来

```cpp
#include <iostream>

using namespace std;
class A
{
public:
private:
	int ma;
};

class B : virtual public A
{
public:
private:
	int mb;
};

class C
{
	virtual void fun(){}
};

class D : virtual public C
{

};

int main()
{
	A a;
	B b;
	C c;
	D d;
	cout << sizeof(a) << endl;
	cout << sizeof(b) << endl; //12 有虚继承时：基类的数据要被搬到最后面
	cout << sizeof(c) << endl << sizeof(d) << endl;
	return 0;
}

```

```cpp
#include <iostream>

using namespace std;

class A
{
public:
	virtual void func() { cout << "A::func" << endl; }
private:
	int ma;
};

class B : virtual public A
{
public:
	void func() { cout << "B::func" << endl; }
private:
	int mb;
};

int main()
{
	//基类指针指向派生类对象时,永远指向的是派生类基类部分数据的起始地址
	A* p = new B(); // 指向堆上的对象手动释放时候会出问题
	p->func();	// 能调用
	delete p;	// 会报错
	return 0;
}
```

> [C++ 虚继承实现原理（虚基类表指针与虚基类表）_c++基类实现_longlovefilm的博客-CSDN博客](https://blog.csdn.net/longlovefilm/article/details/80558879)

<img src="https://mdimagehosting.oss-cn-shanghai.aliyuncs.com/img/image-20230401173510245.png" alt="image-20230401173510245" style="zoom:50%;" />

### 菱形继承

采用虚继承解决菱形继承

好处：

1. 可以做更多代码的复用
2. D -> B, C B *p = new D() C *p = new D() 使用起来更灵活

```cpp
#include <iostream>

using namespace std;

class A
{
public:
	A(int data) :ma(data) { cout << "A()" << endl; }
	~A(){ cout << "~A()"<< endl;  }
protected:
	int ma;
};

class B : virtual public A  //virtual public
{
public:
	B(int data) :A(data), mb(data) { cout << "B()" << endl; }
	~B() { cout << "~B()" << endl; }
protected:
	int mb;
};

class C : virtual public A  //virtual public
{
public:
	C(int data) :A(data), mc(data) { cout << "C()" << endl; }
	~C() { cout << "~C()" << endl; }
protected:
	int mc;
};

class D : public B, public C
{
public:
	D(int data) :A(data), B(data), C(data), md(data) { cout << "D()" << endl; } //A(data)
	~D() { cout << "~D()" << endl; }
protected:
	int md;
};

int main()
{
	D d(10);
	return 0;
}

```

### C++的四种类型转换

C++**语言级别**提供的四种类型转换方式

[C++ | C++的四种类型转换_c++去常转换是所有的const吗_瘦弱的皮卡丘的博客-CSDN博客](https://blog.csdn.net/ThinPikachu/article/details/109052349)

const_cast : 去掉（指针或引用）常量属性的一个类型转换

**static_cast** : 提供编译器认为安全的类型转换（没有任何**联系**的类型之间的转换就被否定了）。**编译时期**的类型转换

reinterpret_cast : 类似于C风格的强制类型转换，谈不上安全

dynamic_cast : 主要用在继承结构中，可以支持RTTI类型识别的上下转换。**运行时期**的类型转换

```cpp
#include <iostream>

using namespace std;

//dynamic_cast
class Base
{
public:
   virtual void func() = 0;
};

class Derive1 : public Base
{
public:
   void func() { cout << "Derive1::func" << endl; }
};

class Derive2 : public Base
{
public:
   void func() { cout << "Derive2::func" << endl; }
   //Derive2实现新功能的API接口函数
   void drive02func() { cout << "Derive2::drive02func" << endl; }
};

void showFunc(Base* p)
{
   //dynamic_cast会检查p指针是否指向的是一个Derive2类型的对象
   //p->vfptr->vftable RTTI信息,
   //如果是,dynamic_cast转换类型成功,返回Derive2对象的地址
   //否则返回nullptr
   Derive2* pd2 = dynamic_cast<Derive2*>(p); //static_cast放这里不安全
   if (pd2 != nullptr)
   {
   	pd2->drive02func();
   }
   else 
   	p->func(); //动态绑定
}

int main()
{
   Derive1 d1;
   Derive2 d2;
   showFunc(&d1);
   showFunc(&d2);

   //const int a = 10;
   //int* p2 = const_cast<int*>(&a); //去掉常量属 性的一个类型转换
   //*p2 = 20;

   //const_cast<这里面必须是指针或引用类型 如 int* int&>
   //int b = const_cast<int>a; //error 

   //static_cast  
   //int a = 97;
   //char b = static_cast<char>(a);
   //cout << b;

   //reinterpret_cast C风格的强制转换
   //int* p = nullptr;
   //double* p2 = reinterpret_cast<double*>(p);
   return 0;
}

```

## [[STL]]

# reference

- [夯实C++基础学习笔记_伍树明的博客-CSDN博客](https://blog.csdn.net/weixin_51368613/article/details/128007165)
