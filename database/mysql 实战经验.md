---
title: mysql 实战经验
time: 14:37
description: mysql 实战经验
navbar: true
sidebar: true
footer: true
date: 2024-09-29
category: Article
author: Zhang Xin
next: true
tags:
  - Mysql
---
# 经验
- 写sql时一律使用小写
- 建表时先判断表是否已存在 if not exists
- 所有的列和表都加comment
- 字符串长度比较短时尽量使用char，定长有利于内存对齐，读写性能更好，而varchar字段频繁修改时容易产生内存碎片
- 满足需求的前提下尽量使用短的数据类型，如tinyint vs int, float vs double, date vs datetime
- default null有别于default"和default 0
- is null, is not null有别于！="，！=0
- 尽量设为not null
	- 有些DB索引列不允许包含null
	- 对含有nul的列进行统计，结果可能不符合预期
	- null值有时候会严重拖慢系统性能
# 规避慢查询
- 大部分的慢查询都是因为没有正确地使用索引
- 不要过多地创建索引，否则写入会变慢
- 绝大部分情况使用默认的InnoDB引擎，不要使用MyISAM引擎
- 不要select*，只select你需要的列
- 尽量用in代替or，or的效率没有in高
- in的元素个数不要太多，一般300到500
- 不要使用模型查询like，模糊查询不能利用索引
- 如果确定结果只有一条，则使用limit 1，停止全表扫描
- 分页查询limit m,n会检索前m+n行，只是返回后n行，通常用id>x来代替这种分页方式
- 批量操作时最好一条sql语句搞定；其次打包成一个事务，一次性提交，高并发情况下减少对共享资源的争用
- 避免使用大事务，用短小的事务，减少锁等待和竞争
- 不要一次查询或更新太多数据，尽量控制在1000条左右
- 不要使用连表操作，join逻辑在业务代码里完成
- 不用MYSQL 内置的函数，因为内置函数不会建立查询缓存，复杂的计算逻辑放到自己的代码里去做
# sql 注入
- `sql ="'select username,password from user where username=" + username +" and password=" + password + "'";`
	变量username和password从前端输入框获取，如果用户输入的 username为lily，password为aaa' or '1'='1
	则完整的sql为`select username,password from user where username="ily' and password='aaa'or '1'='1'`
	会返回表里的所有记录，如果记录数大于0就允许登录，则lily的账号被盗
- `sql="insert into student （name） values （'"+username+" ）"；`
	变量username从前端输入框获取，如果用户输入的username为 `lily'）；arop table student；--`
	完整sql为`insert into student （name） values （lily'）； drop table student；--"）`
	通过注释符--屏蔽掉了末尾的'，删除了整个表
---
- **前端输入要加正则校验、长度限制**
- **对特殊符号（<>&\*；"等）进行转义或编码转换，Go的text/template 包里面的HTMLEscapeString函数可以对字符串进行转义处理**
- **不要将用户输入直接嵌入到sq|语句中，而应该使用参数化查询接口，如Prepare、Query、Exec（query string, args..interfacef）**
- **使用专业的SQL注入检测工具进行检测，如sqlmap、SQLninja**
- **避免网站打印出SQL错误信息，以防止攻击者利用这些错误信息进行 SQL注入**
- **没有任何一种方式能防住所有的sql注入，以上方法要结合使用**
```go
import (  
    "gorm.io/gorm"  
)  
  
// 登录成功返回true。容易被SQL注入攻击  
func LoginUnsafe(db *gorm.DB, name, passwd string) bool {  
    var cnt int64  
    db.Table("login").Select("*").Where("username='" + name + "' and password='" + passwd + "'").Count(&cnt)  
    return cnt > 0  
}  
  
// 登录成功返回true。拒绝SQL注入攻击  
func LoginSafe(db *gorm.DB, name, passwd string) bool {  
    var cnt int64  
    db.Table("login").Select("*").Where("username=? and password=?", name, passwd).Count(&cnt)  
    return cnt > 0  
}
```

## stmt

> MySQL从4.1版本开始提供了一种名为预处理语句（prepared statement）的机制。它可以将整个命令向MySQL服务器发送一次，以后只有参数发生变化，MySQL服务器只需对命令的结构做一次分析就够了。这不仅大大减少了需要传输的数据量，还提高了命令的处理效率。可以用mysqli扩展模式中提供的mysqli_stmt类的对象，去定义和执行参数化的SQL命令。
> 也可以用来防止 sql 注入

- 定义一个sql模板 `stmt, err ：= db.Prepare（"update student set score=score+？where city=？"）`
- 多次使用模板
	res, err：=stmt.Exec（10， "上海"）
	res, err=stmt.Exec（9，"深圳”）
- 不要拼接sql（容易被SQL注入攻击，且利用不上编译优化）
	`db.Where（fmt.Sprintf（"merchant_id = %s"， "， merchantld））`
### sql 预编译

DB执行sql分为3步：
1. 词法和语义解析
2. 优化 SQL语句，制定执行计划
3. 执行并返回结果
SQL预编译技术是指将用户输入用占位符？代替，先对这个模板化的sql进行预编译，实际运行时再将用户输入代入
除了可以防止 SQL注入，还可以对预编译的SQL语句进行缓存，之后的运行就省去了解析优化SQL语句的过程

# 分页查询优化

 **最大id查询法**

  举个例子，我查询第一页的时候是limit 0,10 查询到的最后一条id是10，那么下一页的查询只需要查询id大于10的10条数据即可。
```sql
  select * from user where id >10 limit 0, 10
```

- **between...and**

  ```sql
  select * from user where id BETWEEN 4000000 and 4000010
  ```

  ![img](https://img-blog.csdnimg.cn/20200322113011199.png)
  ![img](https://img-blog.csdnimg.cn/20200322112836413.png)

  这种方式也只能适用于自增主键，并且id没有断裂，否者不推荐这种方式，我们发现使用BETWEEN AND的时候查询出来11条记录，也就是说BETWEEN AND包含了两边的边间条件。使用的时候需要特别注意一下。

- **索引覆盖**

  可以利用表的 覆盖索引 来加速分页查询，利用了索引查询的语句中如果只包含了那个索引列（覆盖索引），那么这种情况会查询很快。因为利用索引查找有优化算法，且数据块就在查询索引上面，不用再去找相关的数据块，这样节省了很多时间，也就是说，查询的数据就在索引上，不用再经过 回表 的操作。例如：

  ```sql
  select id from tb_a where number=1 limit 100000, 100;

  -- 改成
  select * from tb_a where number = 1 and id >= (select id from tb_a where number = 1 limit 100000, 1) limit 100;
  ```

  id 是主键索引（聚簇索引），number 是二级索引（非聚簇索引），二级索引的叶子结点上存储的是主键索引值，而我们只需要查询主键即可，因此就不用 回表 查询多一次。

