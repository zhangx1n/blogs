---
title: 设计模式
time: 14:37
description: 设计模式
navbar: true
sidebar: true
footer: true
date: 2024-01-29
category: Document
author: Zhang Xin
next: true
tags:
  - cpp
---
## 1.单例模式代码设计

单例模式：一个类不管创建多少次对象，永远只能得到该类型一个对象的实例。

常用的：日志模块、数据库模块

**饿汉式单例模式**：还没有获取实例对象，实例对象就已经产生了

**懒汉式单例模式**：唯一的实例对象，直到第一次获取它的时候，才产生

饿汉式一定是线程安全的；但是会延长软件的启动时间

---
```cpp
#include <iostream>

class Singleton
{
public:
	static Singleton* getInstance() //#3 获取类的唯一实例对象的接口方法
	{
		return &instance;
	}
private:
	static Singleton instance; //#2 定义一个唯一的类的实例对象
	Singleton() //#1 构造函数私有化
	{

	}
	Singleton(const Singleton&) = delete; //#4 禁止深拷贝、运算符重载
	Singleton& operator=(const Singleton&) = delete;
};
Singleton Singleton::instance;

int main()
{
	Singleton* p1 = Singleton::getInstance();
	Singleton* p2 = Singleton::getInstance();
	Singleton* p3 = Singleton::getInstance();
	return 0;
}
```

懒汉式模式：变成指针。

```cpp
class Singleton
{
public:
	static Singleton* getInstance() //#3 获取类的唯一实例对象的接口方法
	{
		if (nullptr == instance)
		{
			instance = new Singleton();
		}
		return instance;
	}
private:
	static Singleton *instance; //#2 定义一个唯一的类的实例对象
	Singleton() //#1 构造函数私有化
	{

	}
	Singleton(const Singleton&) = delete; //#4 禁止深拷贝、运算符重载
	Singleton& operator=(const Singleton&) = delete;
};
Singleton *Singleton::instance = nullptr;

```

## 2. 线程安全的懒汉单例模式

可重入：没有执行完又被调用一次

开辟内存 => 构造对象、赋值（这两个不保证执行顺序）

有可能出现线程 1 运行后还没来得及赋值线程 2 也进去了

```cpp
class Singleton
{
public:
	static Singleton* getInstance() //#3 获取类的唯一实例对象的接口方法
	{
		if (nullptr == instance)
		{
			std::lock_guard<std::mutex> guard(mtx);
			if (nullptr == instance)
				instance = new Singleton();
		}
		return instance;
	}
private:
	static Singleton* volatile instance; //#2 定义一个唯一的类的实例对象
	Singleton() //#1 构造函数私有化
	{

	}
	Singleton(const Singleton&) = delete; //#4 禁止深拷贝、运算符重载
	Singleton& operator=(const Singleton&) = delete;
};
Singleton* volatile Singleton::instance = nullptr;

```

**也可以用 static 实现**

```cpp
class Singleton
{
public:
	static Singleton* getInstance() 
	{
		// 函数静态局部变量的初始化,在汇编上已经自动添加线程互斥指令了
		static Singleton instance; //运行到这里才会初始化
		return &instance;
	}
private:
	Singleton() 
	{

	}
	Singleton(const Singleton&) = delete; 
	Singleton& operator=(const Singleton&) = delete;
};

```

## 3. 简单工厂和工厂方法

简单工厂，一个工厂把所有的产品都造，同时也不符合“开闭”原则

```cpp
#include <iostream>
#include <memory>

/*
简单工厂 Simple Factory
工厂方法 Factory Method
抽象工厂 Abstract Factory

工厂模式：主要是封装了对象的创建
*/

class Car
{
public:
	Car(std::string name) : _name(name){}
	virtual void show() = 0;
protected:
	std::string _name;
};

class Bmw : public Car
{
public:
	Bmw(std::string name) : Car(name){}
	void show()
	{
		std::cout << "获取了一辆宝马 " << _name << std::endl;
	}
};

class Audi : public Car
{
public:
	Audi(std::string name) : Car(name) {}
	void show()
	{
		std::cout << "获取了一辆奥迪 " << _name << std::endl;
	}
};

enum CarType
{
	BMW, AUDI
};

class SimpleFactory
{
public:
	Car* createCar(CarType ct)
	{
		switch (ct)
		{
		case BMW:
			return new Bmw("x1");
			break;
		case AUDI:
			return new Audi("y1");
			break;
		default:
			std::cerr << "传入工厂的参数不正确 " << ct << std::endl;
			break;
		}
	}
};

int main()
{
	std::unique_ptr<SimpleFactory> factory(new SimpleFactory());
	std::unique_ptr<Car>p1(factory->createCar(BMW));
	std::unique_ptr<Car>p2 (factory->createCar(AUDI));
	p1->show();
	p2->show();

	return 0;
}

```

可以通过一个基类向外拓展。实现了修改关闭、拓展打开

```cpp
#include <iostream>
#include <memory>

/*
简单工厂 Simple Factory
工厂方法 Factory Method
抽象工厂 Abstract Factory

工厂模式：主要是封装了对象的创建
*/

class Car
{
public:
	Car(std::string name) : _name(name){}
	virtual void show() = 0;
protected:
	std::string _name;
};

class Bmw : public Car
{
public:
	Bmw(std::string name) : Car(name){}
	void show()
	{
		std::cout << "获取了一辆宝马 " << _name << std::endl;
	}
};

class Audi : public Car
{
public:
	Audi(std::string name) : Car(name) {}
	void show()
	{
		std::cout << "获取了一辆奥迪 " << _name << std::endl;
	}
};

class Factory
{
public:
	virtual Car* createCar(std::string name) = 0;
};

class BMWFactory : public Factory
{
public:
	Car* createCar(std::string name)
	{
		return new Bmw(name);
	}
};

class AudiFactory : public Factory
{
public:
	Car* createCar(std::string name)
	{
		return new Audi(name);
	}
};

int main()
{
	std::unique_ptr<Factory> bmwFactory(new BMWFactory());
	std::unique_ptr<Factory> audiFactory(new AudiFactory());
	std::unique_ptr<Car>p1(bmwFactory->createCar("x1"));
	std::unique_ptr<Car>p2(audiFactory->createCar("y1"));
	p1->show();
	p2->show();

	return 0;
}
```

## 4. 抽象工厂

现在考虑生产一类产品

缺点：重写接口很麻烦

```cpp
#include <iostream>
#include <memory>

/*
简单工厂 Simple Factory
优：客户不用自己负责new对象
缺：接口函数不闭合，不能对修改关闭

工厂方法 Factory Method
优：提供了一个纯虚函数（创建产品），定义派生类（具体产品的工厂）负责创建对应的产品，可以做到不同的产品在不同的工厂里面创建，能够对现有工厂以及产品的修改关闭。
缺：很多产品是有关联关系的，属于一个产品簇，不应该放在不同的工厂里去创建，且工厂类太多，不好维护

抽象工厂 Abstract Factory
把有关联关系的，属于一个产品簇的所有产品创建的接口函数放在一个抽象工厂里面，派生类（具体产品的工厂）应该负责创建该产品簇里面所有的产品。

工厂模式：主要是封装了对象的创建
*/

//系列产品1
class Car
{
public:
	Car(std::string name) : _name(name){}
	virtual void show() = 0;
protected:
	std::string _name;
};

class Bmw : public Car
{
public:
	Bmw(std::string name) : Car(name){}
	void show()
	{
		std::cout << "获取了一辆宝马 " << _name << std::endl;
	}
};

class Audi : public Car
{
public:
	Audi(std::string name) : Car(name) {}
	void show()
	{
		std::cout << "获取了一辆奥迪 " << _name << std::endl;
	}
};

//系列产品2
class Light
{
public:
	virtual void show() = 0;
};

class BmwLight : public Light
{
public:
	void show() { std::cout << "Bmw light" << std::endl; }
};

class AudiLight : public Light
{
public:
	void show() { std::cout << "Audi light" << std::endl; }
};

//抽象成抽象工厂 => 对有一组关联关系的产品簇提供产品对象的统一创建
class AbstractFactory
{
public:
	virtual Car* createCar(std::string name) = 0; //工厂方法 创建汽车
	virtual Light* createCarLight() = 0; //创建车灯
};

class BMWFactory : public AbstractFactory
{
public:
	Car* createCar(std::string name)
	{
		return new Bmw(name);
	}
	Light* createCarLight()
	{
		return new BmwLight();
	}
};

class AudiFactory : public AbstractFactory
{
public:
	Car* createCar(std::string name)
	{
		return new Audi(name);
	}
	Light* createCarLight()
	{
		return new AudiLight();
	}
};

int main()
{
	std::unique_ptr<AbstractFactory> bmwFactory(new BMWFactory());
	std::unique_ptr<AbstractFactory> audiFactory(new AudiFactory());
	std::unique_ptr<Car>p1(bmwFactory->createCar("x1"));
	std::unique_ptr<Car>p2(audiFactory->createCar("y1"));
	std::unique_ptr<Light>p3(bmwFactory->createCarLight());
	std::unique_ptr<Light>p4(audiFactory->createCarLight());
	p1->show();
	p2->show();
	p3->show();
	p4->show();

	return 0;
}
/*
获取了一辆宝马 x1
获取了一辆奥迪 y1
Bmw light
Audi light
*/

```

## 5. 代理模式

实现了逻辑与实现的解耦

```cpp
#include <iostream>
#include <memory>

using namespace std;

/*
代理Proxy模式：通过代理类，来控制实际对象的访问权限
客户     助理Proxy     老板 委托类
*/
class VideoSite
{
public:
	virtual void freeMovie() = 0; //免费电影
	virtual void vipMovie() = 0; //vip电影
	virtual void ticketMovie() = 0; //券电影
};
class FixBugVideoSite : public VideoSite  //委托类
{
public:
	virtual void freeMovie()  //免费电影
	{
		cout << "免费电影" << endl;
	}
	virtual void vipMovie()  //vip电影
	{
		cout << "vip电影" << endl;
	}
	virtual void ticketMovie()  //券电影
	{
		cout << "券电影" << endl;
	}
};

class FreeVideoSitProxy : public VideoSite
{
public:
	FreeVideoSitProxy(){ pVideo = new FixBugVideoSite(); }
	~FreeVideoSitProxy() { delete pVideo; }
	virtual void freeMovie() //免费电影
	{
		pVideo->freeMovie(); //通过代理对象的freeMovie，来访问真正委托类对象的freeMovie
	}
	virtual void vipMovie()//vip电影
	{
		cout << "请升级vip" << endl;
	}
	virtual void ticketMovie() //券电影
	{
		cout << "请充值" << endl;
	}
private:
	VideoSite* pVideo;
};

class VipVideoSitProxy : public VideoSite
{
public:
	VipVideoSitProxy() { pVideo = new FixBugVideoSite(); }
	~VipVideoSitProxy() { delete pVideo; }
	virtual void freeMovie() //免费电影
	{
		pVideo->freeMovie(); //通过代理对象的freeMovie，来访问真正委托类对象的freeMovie
	}
	virtual void vipMovie() //vip电影
	{
		pVideo->vipMovie();
	}
	virtual void ticketMovie()  //券电影
	{
		cout << "请充值" << endl;
	}
private:
	VideoSite* pVideo;
};

void watchMovie(unique_ptr<VideoSite>& ptr)
{
	ptr->freeMovie();
	ptr->vipMovie();
	ptr->ticketMovie();
}

int main()
{
	unique_ptr<VideoSite> p1(new FreeVideoSitProxy());
	unique_ptr<VideoSite> p2(new VipVideoSitProxy());

	watchMovie(p1);
	watchMovie(p2);

	return 0;
}
/*
免费电影
请升级vip
请充值
免费电影
vip电影
请充值
*/

```

## 6. 装饰器模式

```cpp
#include <iostream>
#include <memory>

using namespace std;

/*
装饰器模式
*/

class Car  //抽象基类
{
public:
	virtual void show() = 0;
};
//三个实体的汽车类
class Bmw : public Car
{
public:
	void show()
	{ 
		cout << "宝马,配置有：基类配置"; 
	}
};
class Audi : public Car
{
public:
	void show()
	{
		cout << "奥迪,配置有：基类配置" ;
	}
};
class Benz : public Car
{
public:
	void show()
	{
		cout << "奔驰,配置有：基类配置" ;
	}
};

//装饰器 定速巡航
class ConcreteDecorator01 : public Car
{
public:
	ConcreteDecorator01(Car* p) :pCar(p) {}
	void show()
	{
		pCar->show();
		cout << ",定速巡航" ;
	}
private:
	Car* pCar;
};

class ConcreteDecorator02 : public Car
{
public:
	ConcreteDecorator02(Car* p) :pCar(p) {}
	void show()
	{
		pCar->show();
		cout << ",自动刹车";
	}
private:
	Car* pCar;
};

class ConcreteDecorator03 : public Car
{
public:
	ConcreteDecorator03(Car* p) :pCar(p) {}
	void show()
	{
		pCar->show();
		cout << ",车道偏离" ;
	}
private:
	Car* pCar;
};


int main()
{
	Car* p1 = new ConcreteDecorator01(new Bmw());
	p1 = new ConcreteDecorator02(p1);
	p1 = new ConcreteDecorator03(p1);
	Car* p2 = new ConcreteDecorator02(new Audi());
	Car* p3 = new ConcreteDecorator03(new Benz());

	p1->show();
	cout << endl;
	p2->show();
	cout << endl;
	p3->show();

	return 0;
}
/*
宝马,配置有：基类配置,定速巡航,自动刹车,车道偏离
奥迪,配置有：基类配置,自动刹车
奔驰,配置有：基类配置,车道偏离
*/

```

## 7.适配器模式(除了单例和工厂，这个比较重要)

```cpp
#include <iostream>
#include <memory>

using namespace std;

/*
适配器模式：让不兼容的接口可以在一起工作
电脑 =》 投影到 =》 投影仪 
*/
class VGA //VGA接口类
{
public:
	virtual void play() = 0;
};

//进了一批新的投影仪，但是新的投影仪只支持HDMI接口
class HDMI
{
public:
	virtual void play() = 0;
};

//TV01 表示支持VGA接口的投影仪
class TV01 : public VGA
{
public:
	void play()
	{
		cout << "通过VGA接口连接投影仪，进行视频播放" << endl;
	}
};

//TV02 表示支持HDMI接口的投影仪
class TV02 : public HDMI
{
public:
	void play()
	{
		cout << "通过HDMI接口连接投影仪，进行视频播放" << endl;
	}
};

//实现一个电脑类(只支持VGA接口)
class Computer 
{
public:
	//由于电脑只支持VGA接口，所以该方法的参数只支持VGA接口的指针/引用
	void playVideo(VGA* pVGA) 
	{
		pVGA->play();
	}
};

/*
方法1：换一个支持HDMI接口的电脑，代码重构
方法2：买一个转换头（适配器），把VGA信号转为HDMI信号，添加适配器类
*/
class VGAToHDMIAdpter : public VGA
{
public:
	VGAToHDMIAdpter(HDMI* p) :pHdmi(p){}
	void play() //转换头
	{
		pHdmi->play();
	}
private:
	HDMI* pHdmi;
};

int main()
{
	Computer computer;
	computer.playVideo(new TV01());
	computer.playVideo(new VGAToHDMIAdpter(new TV02()));
	return 0;
}

```

## 8. 观察者模式

```cpp
#include <iostream>
#include <string>
#include <unordered_map>
#include <list>

using namespace std;

/*
行为形模式：主要关注的是对象之间的通信
观察者-监听者模式（发布-订阅模式）设计模式：主要关注的是对象的一对多的关系，
也就是多个对象都依赖一个对象，当该对象的状态发生改变时，其它对象都能接收到
相应的通知

一组数据（数据对象） => 通过这一组数据 => 曲线图/柱状图/圆饼图
当数据对象改变时，对象1、对象2、对象3应该及时地收到相应的通知 
*/

//观察者抽象类
class Observer 
{
public:
	//处理消息的接口
	virtual void handle(int msgid) = 0;
};

//第一个观察者实例 1 2
class Observer1 : public Observer
{
public:
	void handle(int msgid)
	{
		switch(msgid)
		{
		case 1:
			cout << "Observer1 recv 1 msg!" << endl;
			break;
		case 2:
			cout << "Observer1 recv 2 msg!" << endl;
			break;
		default:
			cout << "Observer1 recv unknow msg!" << endl;
			break;
		}
	}
};

//第二个观察者实例 2
class Observer2 : public Observer
{
public:
	void handle(int msgid)
	{
		switch (msgid)
		{
		case 2:
			cout << "Observer2 recv 2 msg!" << endl;
			break;
		default:
			cout << "Observer2 recv unknow msg!" << endl;
			break;
		}
	}
};

//第三个观察者实例  1 3
class Observer3 : public Observer
{
public:
	void handle(int msgid)
	{
		switch (msgid)
		{
		case 1:
			cout << "Observer3 recv 1 msg!" << endl;
			break;
		case 3:
			cout << "Observer3 recv 3 msg!" << endl;
			break;
		default:
			cout << "Observer3 recv unknow msg!" << endl;
			break;
		}
	}
};

class Subject
{
public:
	//给主题增加观察者对象
	void addObserver(Observer* obser, int msgid) //观察者和它感兴趣的id
	{
		_subMap[msgid].push_back(obser);
	}
	//主题检测发生改变，通知相应的观察者对象处理事件
	void dispatch(int msgid) 
	{
		auto it = _subMap.find(msgid);
		if (it != _subMap.end())
		{
			for (auto tmp : it->second)
			{
				tmp->handle(msgid);
			}
		}
	}
private:
	unordered_map<int, list<Observer*>> _subMap;
};

int main()
{
	Subject subject;
	Observer* p1 = new Observer1();
	Observer* p2 = new Observer2();
	Observer* p3 = new Observer3();

	subject.addObserver(p1, 1);
	subject.addObserver(p1, 2);
	subject.addObserver(p2, 2);
	subject.addObserver(p3, 1);
	subject.addObserver(p3, 3);

	int msgid = 0;
	for (;;)
	{
		cout << "输入消息id：";
		cin >> msgid;
		if (msgid == -1)
			break;
		subject.dispatch(msgid);
	}
	return 0;
}
/*
输入消息id：1
Observer1 recv 1 msg!
Observer3 recv 1 msg!
输入消息id：2
Observer1 recv 2 msg!
Observer2 recv 2 msg!
输入消息id：3
Observer3 recv 3 msg!
输入消息id：4
输入消息id：-1
*/

```

