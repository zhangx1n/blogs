---
title: MongoDB
time: 14:37
description: MongoDB 基础
navbar: true
sidebar: true
footer: true
date: 2024-07-29
category: Document
author: Zhang Xin
next: true
tags:
  - MongoDB
---
# 基本概念
## 无模式数据库

​很多NoSQL数据库有无模式的共同点。若要在关系型数据库中存储数据，首先必须定义`模式`，也就是用一种预定义结构向数据库说明要有哪些表格，表中有哪些列，每一列都存放何种类型的数据。必须先定义好模式，然后才能存放数据。
相比之下，NoSQL数据库的数据存储就比较随意。`键值数据库`可以把任何数据存放在一个键的名下。`文档数据库`实际上也如此，因为它对所存储的文档结构没有限制。在列族数据库中，任意列里面都可以随意存放数据。你可以在`图数据库`中新增边，也可以随意向节点和边中添加属性。

---

## MongoDB三要素

**MongoDB三要素与传统关系型数据库概念类比**

|传统数据库|MongDB|解释说明|
|---|---|---|
|database|database|数据库|
|table|collection|数据库表/集合|
|row|document|数据记录行/文档|
|column|field|数据字段/域|
|index|index|索引|
|table joins||表连接，MongoDB不支持|
|primary key|primary key|主键，MongoDB自动将_id字段设置为主键|

**传统数据库的row与mongoDB的document对比**

row：每一行都是一样的字段，不可添加不可减少，也就说fields的个数在定义table的时候就已经声明完成的

document： 它的每一个document都是独立的，同时也不是在创建collection的时候经声明完成的

##  MongoDB的数据类型

|数据类型|描述|
|---|---|
|String|字符串，仅UTF-8编码合法|
|Integer|整型数值，根据服务器不同，可分为32位或64位|
|Boolean|布尔值|
|Double|双精度浮点数|
|Array|用于将数组或列表或多个值存储为一个键|
|Timestamp|时间戳|
|Object|用于内嵌文档|
|Null|用于创建空文档|
|Symbol|符号。该数据类型基本上等同于字符串类型，但不同的是，它一般用于使用了特殊符号类型的语言|
|Date|日期时间。用UNIX时间格式来存储日期|

## 用户权限

​ Mongodb作为时下最为热门的数据库，那么其安全验证也是必不可少的，否则一个没有验证的数据库暴露出去，任何人可随意操作，这将是非常危险的。我们可以通过使用为MongoDB创建用户的方式来降低风险。

|权限名|描述|
|---|---|
|read|允许用户读取指定数据库|
|readWrite|允许用户读写指定数据库|
|dbAdmin|允许用户在指定数据库中执行管理函数，如索引创建、删除，查看统计或访问system.profile|
|userAdmin|允许用户向system.users集合写入，可以在指定数据库里创建、删除和管理用户|
|clusterAdmin|只在admin数据库中可用，赋予用户所有分片和复制集相关函数的管理权限|
|readAnyDatabase|只在admin数据库中可用，赋予用户所有数据库的读权限，除系统库的集合|
|readWriteAnyDatabase|只在admin数据库中可用，赋予用户所有数据库的读写权限，除系统库的集合|
|userAdminAnyDatabase|只在admin数据库中可用，赋予用户所有数据库的userAdmin权限，除系统库的集合|
|dbAdminAnyDatabase|只在admin数据库中可用，赋予用户所有数据库的dbAdmin权限，除系统库的集合|
|root|只在admin数据库中可用。超级账号，超级权限|

### 创建用户

前置条件：在admin库下操作。如果配置`auth=true`启动参数则需要有权限的用户操作，否则先不配置此参数，创建完用户之后开启此参数，并重启服务。

```mongodb
语法：
db.createUser({ 
    user: "<name>",
    pwd: "<cleartext password>",
    customData: { <any Object Data> },
    roles: [
        { role: "<role>", db: "<database>" },
        ...
    ]
});
```

- user：新建用户名
    
- pwd：新建用户密码
    
- customData：存放一些用户相关的自定义数据，该属性也可忽略
    
- roles：数组类型，配置用户的权限
    

```mongodb
示例：
db.createUser({user:'root',pwd:'root',roles:[{role:'root',db:'admin'}]})
```

> 创建用户完成之后，配置`auth=true`启动参数

### 登陆用户

前置条件：在admin库下操作

```mongodb
语法：
db.auth('<username>', '<password>');

示例：
db.auth('root','root');
```

### 查看用户信息

前置条件：在admin库下操作

```mongodb
show users
db.system.users.find()
```

### 更新用户

前置条件：在admin库下操作

```mongodb
语法：
db.updateUser('<username>', {<新的用户数据对象>});

示例：
db.updateUser('root', {'pwd':'123456', 'roles':[{'role':'root', 'db':'admin'}]});
```

### 修改用户密码函数

虽然更新用户函数也可以修改用户密码，MongoDB也提供了独立修改密码的函数

前置条件：在admin库下操作

```mongodb
语法：
db.changeUserPassword("<newUserName>","<newPassword>")

示例：
db.changeUserPassword('root', '123456');
```

### 删除用户

前置条件：在admin库下操作

```mongodb
语法：
db.dropUser('<userName>')

示例：
db.dropUser('root');
```
# Database 操作

**创建数据库**

在MongoDB中创建数据库的命令使用的是use命令。该命令有两层含义：

1. 切换到指定数据库
2. 如果切换的数据库不存在，则创建该数据库

如果只创建数据库未在数据库中创建集合，则此创建为逻辑创建，在内存中，但并未在生成对应目录。使用查看数据库命令是扫描磁盘目录，所以无法看到

**查看数据库**

```mongodb
show dbs
show databases
```

**删除数据库**

在MongoDB中使用`db.dropDatabase()`函数来删除数据库。在删除数据库之前，需要切换到需要删除的数据库，执行即可

```mongodb
示例：
use test;
db.dropDatabase();
```

# Collection操作

MongoDB中的集合是一组文档的集，相当于关系型数据库中的表

**创建集合**

> 在MongoDB中，我们也可以不用创建集合，当我们插入一些数据时，会自动创建集合

语法格式：`db.createCollection(<collectionName>, <options>)`

options可以是如下参数

|字段|类型|描述|
|---|---|---|
|capped|布尔|（可选），如果为 true，则创建固定集合，且必须指定 size 参数  <br>固定集合是指当达到最大值时，它会自动覆盖最早的文档|
|size|数值|（可选）为固定集合指定一个最大值（以字节计）。 如果 capped 为 true，也需要指定该字段。|
|max|数值|（可选）指定固定集合中包含文档的最大数量。|

```mongodb
示例：
db.createCollection('testCollection');
db.createCollection('testCollection', {'capped':true, 'size':2000000, 'max':1000});
```

**查看集合**

如果要查看已有集合，可以使用`show collections`或`show tables`命令

```mongodb
show collections;
show tables;
```

**查看集合详情**

如果要查看已有集合的详情，可以使用`db.<collectionName>.stats()`命令

```mongodb
示例：
db.testCollection.stats();
```

**删除集合**

需要先切换到需要删除集合所在的数据库，使用`db.<collectionName>.drop()`函数删除集合即可

```mongodb
示例：
db.testCollection.drop();
```

# Document 操作

在MongoDB中文档是指多个键及其关联的值有序地放置在一起就是文档，其实指的就是数据。MongoDB中的文档的数据结构和JSON基本一样。所有存储在集合中的数据都是BSON格式。BSON是一种类似JSON的二进制形式的存储格式，是Binary JSON的简称。

## 新增文档

**新增单一文档**

- `insert`函数
    
    语法：`db.<collectionName>.insert(document)`
    
    ```mongodb
      示例：
      db.user.insert({name: '张三', nickName: 'Tom', 'age': 18, course: ['java', 'spring']});
    ```
    
- `save`函数
    
    语法：`db.<collectionName>.save(document)`
    
    ```mongodb
      示例：
      db.user.save({name: '李四', nickName: 'Jack', 'age': 18, course: ['html', 'js']});
    ```
    
- `insertOne`函数
    
    语法：`db.<collectionName>.insertOne(document)`
    
    ```mongodb
      示例：
      db.user.insertOne({name: '王五', nickName: 'King', 'age': 20, course: ['java', 'js']});
    ```
    

**批量新增文档**

- `insert`函数
    
    语法：`db.<collectionName>.insert(documents)`
    
    ```mongodb
      示例：
      db.user.insert([
      {name: '张三', nickName: 'Tom', 'age': 18, course: ['java', 'spring']},
      {name: '李四', nickName: 'Jack', 'age': 18, course: ['html', 'js']},
      {name: '王五', nickName: 'King', 'age': 20, course: ['java', 'js']}
      ]);
    ```
    
- `save`函数
    
    语法：`db.<collectionName>.save(documents)`
    
    ```mongodb
      示例：
      db.user.save([
      {name: '张三', nickName: 'Tom', 'age': 18, course: ['java', 'spring']},
      {name: '李四', nickName: 'Jack', 'age': 18, course: ['html', 'js']},
      {name: '王五', nickName: 'King', 'age': 20, course: ['java', 'js']}
      ]);
    ```
    
- `insertMany`函数
    
    语法：`db.<collectionName>.save(documents)`
    
    ```mongodb
      示例：
      db.user.insertMany([
      {name: '张三', nickName: 'Tom', 'age': 18, course: ['java', 'spring']},
      {name: '李四', nickName: 'Jack', 'age': 18, course: ['html', 'js']},
      {name: '王五', nickName: 'King', 'age': 20, course: ['java', 'js']}
      ]);
    ```
    

## 查询文档

### 基础应用

- `findOne`函数用于查询集合中的一个文档
    
    语法：`db.<collectionName>.findOne({<query>}, {<projection>});`
    
    1. query：可选，代表查询条件。
    2. projection：可选，代表查询结果的投影字段名。即查询结果需要返回哪些字段或不需要返回哪些字段。
    
    ```mongodb
      示例：
      db.user.findOne();
      db.user.findOne({name: '张三'});
      db.user.findOne({name: '张三'}, {name: 1, age: 1, _id: 0});
    ```
    
    > 投影时
    > 
    > `_id`为1的时候，其他字段必须是1
    > 
    > `_id`是0的时候，其他字段可以是0
    > 
    > 如果没有`_id`字段约束，多个其他字段必须同为0或同为1
    
- find函数用于查询集合中的若干文档
    
    语法：`db.<collectionName>.find({<query>}, {<projection>});`
    
    ```mongodb
      示例：
      db.user.find();
      db.user.find({name: '张三'});
      db.user.find({name: '张三'}, {name: 1, age: 1, _id: 0});
    ```
    

### 单条件逻辑运算符

|操作|格式|范例|类似DBM语句|
|---|---|---|---|
|等于|`{<key>:<value>`}或  <br>`{<key>:{$eq:<value>}}`|db.col.find({name: “张三”})|where name = ‘张三’|
|小于|`{<key>:{$lt:<value>}}`|db.col.find({age: {$lt: 20}})|where age < 20|
|小于等于|`{<key>:{$lte:<value>}}`|db.col.find({age: {$lte: 20}})|where age <= 20|
|大于|`{<key>:{$gt:<value>}}`|db.col.find({age: {$gt: 10}})|where age > 10|
|大于等于|`{<key>:{$gte:<value>}}`|db.col.find({age: {$gte: 10}})|where age >= 10|
|不等于|`{<key>:{$ne:<value>}}`|db.col.find({age: {$ne: 20}})|where age != 20|

### 多条件逻辑运算符

**And条件**

MongoDB的`find()`和`findOne()`函数可以传入多个键(key)，每个键(key)以逗号隔开，即常规SQL的AND条件

```mongodb
示例：
db.user.find({name: '张三', age :18});
```

**Or条件**

MongoDB的OR条件语句使用了关键字`$or`，语法格式如下

```mongodb
示例：
db.user.find({$or: [{name: '张三'}, {age :18}]});
```

### $type查询

在MongoDB中根据字段的数量类型来查询数据使用`$type`操作符来实现

语法：`db.<collectionName>.find({<attr>:{$type:<typeNum/typeAlias>}})`

|Type|Number|Alias|
|---|---|---|
|Double|1|“double”|
|String|2|“string”|
|Object|3|“object”|
|Array|4|“array”|
|Binary data|5|“binData”|
|ObjectId|7|“objectId”|
|Boolean|8|“bool”|
|Date|9|“date”|
|Null|10|“null”|
|Regular Expression|11|“regex”|
|JavaScript|13|“javascript”|
|JavaScript (with scope)|15|“javascriptWithScope”|
|32-bit integer|16|“int”|
|Timestamp|17|“timestamp”|
|64-bit integer|18|“long”|

```mongodb
示例：
db.user.find({name: {$type: 'string'}});
db.user.find({name: {$type: 2}});
```

### 正则查询

MongoDB中查询条件也可以使用正则表达式作为匹配约束

语法：`db.<collectionName>.find({<filedName>:<reg>/<option>})`

option的选项有

- i ：不区分大小写以匹配大小写的情况
- m：对于包含锚点的模式，将`\n`视作每行，每行都进行匹配
- x：设置x选项后，正则表达式中的非转义的空白字符将被忽略
- s：允许点字符（.）匹配包括换行符在内的所有字符

```mongodb
示例：
db.user.find({name: /^张/});
db.user.find({name: /三$/});
db.user.find({nickName: /t/i});
```

### 分页查询

在MongoDB中读取指定数量的数据记录，可以使用的`limit`方法，`limit(<num>)`方法接受一个数字参数，该参数指定读取的记录条数

在MongoDB中使用`skip`方法来跳过指定数量的文档，`skip(<num>)`方法同样接受一个数字参数作为跳过的文档条数

```mongodb
示例：
db.user.find().skip(5).limit(5);
```

### 排序

在 MongoDB中使用`sort`方法对数据进行排序，`sort(<param>)` 可以通过参数指定排序的字段，并使用`1`和`-1`来指定排序的方式，其中`1`为升序排列，而 `-1`是用于降序排列。

```mongodb
示例：
db.user.find().sort({age:'asc'})
```

## 更新文档

### save更新文档

save()函数的作用是保存文档，如果文档存在则覆盖，如果文档不存在则新增。save()函数对文档是否存在的唯一判断标准是`_id`系统唯一字段是否匹配。所以使用save()函数实现更新操作，则必须提供`_id`字段数据

```mongodb
示例：
db.user.save({name:"赵六"}); -- 新增
db.user.save({"_id" : ObjectId("6010c798fc86950278e5caac"),name:"赵六", age: 22}); --更新
```

### update更新文档

`update()`函数用于更新已存在的文档

```mongodb
语法：
db.<collectionName>.update(
    <query>,
    <update>,
    <upsert:boolean>,
    <multi:boolean>
)
```

- query：update的查询条件，类似sql的update更新语法内where后面的内容
- update：update的对象和一些更新的操作符等，也可以理解为sql update查询内set后面的
- upsert：可选，这个参数的意思是，如果不存在update的记录，是否插入这个document，true为插入，默认是false，不插入
- multi：可选，mongodb 默认是false，只更新找到的第一条记录，如果这个参数为true，就把按条件查出来多条记录全部更新。只有在表达式更新语法中才可使用。

在MongoDB中的update是有两种更新方式，一种是覆盖更新，一种是表达式更新。

- 覆盖更新：顾名思义，就是通过某条件，将新文档覆盖原有文档
- 表达式更新：这种更新方式是通过表达式来实现复杂更新操作，如：字段更新、数值计算、数组操作、字段名修改等

#### 覆盖更新

```mongodb
示例：
db.user.update({name: '张三'},{name: '张'});
```

将会给第一条符合添加的数据覆盖，因为`multi`选项默认为false

#### 表达式更新

**$inc**

作用：对一个数字字段的某个field增加value

```mongodb
示例：
db.user.update({name: '张三'},{$inc: {age: 1}});
```

**$set**

作用：把文档中某个字段field的值设为value，如果field不存在，则增加新的字段并赋值为value

```mongodb
示例：
db.user.update({name: '张三'},{$set: {age: 20}});
```

**$unset**

作用：删除某个字段field

```mongodb
示例：
db.user.update({name: '张三'},{$unset: {age: null}});
```

unset指定的字段后可以跟任何值，只是起占位作用

**$push**

作用：把value追加到field里。注：field只能是数组类型，如果field不存在，会自动插入一个数组类型

```mongodb
示例：
db.user.update({name: '张三'},{$push: {course: 'vue'}});
```

**$addToSet**

作用：加一个值到数组内，而且只有当这个值在数组中不存在时才增加

```mongodb
示例：
db.user.update({name: '张三'},{$addToSet: {course: 'vue'}});
```

**$pop**

删除数组内第一个值`{$pop:{<field>:-1}}`、删除数组内最后一个值`{$pop:{<field>:1}}`

```mongodb
示例：
db.user.update({name: '张三'},{$pop: {course: -1}});
```

**$pull**

从数组field内删除所有等于指定值的值

```mongodb
示例：
db.user.update({name: '张三'},{$pull: {course: 'vue'}});
```

**$pullAll**

用法同`$pull`一样，可以一次性删除数组内的多个值

```mongodb
示例：
db.user.update({name: '张三'},{$pullAll: {course: ['vue', 'java', 'spring']}});
```

**$rename**

作用：对字段进行重命名。底层实现是先删除old_field字段，再创建new_field字段

```mongodb
示例：
db.user.update({name: '张三'},{$rename: {nickName: 'nick'}});
```

## 删除文档

**deleteOne函数**

作用：删除一个满足添加的数据

语法：`db.<collectionName>.deleteOne({<query>})`

```mongodb
db.user.deleteOne({'name':'张三'});
```

**deleteMany函数**

作用：删除所有满足添加的数据

语法：`db.<collectionName>.deleteMany({<query>})`

```mongodb
db.user.deleteMany({'name':'张三'});
```

> 删除文档还有一个remove函数，但已过时，官方推荐用deleteOne()和deleteMany()函数来实现删除操作。且在4.0版本中，remove函数并不会真正的释放存储空间，需要使用db.repairDatabase()函数来释放存储空间。

# 内置函数

### aggregate函数

MongoDB中聚合的方法使用aggregate

语法：`db.<collectionName>.aggregate(<agg_options>)`

agg_options：数组类型参数，传入具体的聚合表达式，此参数代表聚合规则，如计算总和、平均值、最大最小值等。

### 求和$sum

语法：`db.collectionName.aggregate([{"$group":{"_id":<field/null>, "<aggeName>":{"$sum":"$<field>"}}}])`

- `$group`：分组，代表聚合的分组条件
- `_id`：分组的字段。相当于SQL分组语法group by column中的column部分。如果根据某字段的值分组，则定义为`_id:'$field'`。如果不需要分组则为`_id:null`
- `$sum`：求和表达式。相当于SQL中的`sum`函数
- `$<filed>`：代表文档中的需要求和字段

```mongodb
示例：
db.user.aggregate([{$group:{_id: null, sum_age: {$sum: '$age'}}}]);     --不分组求和
db.user.aggregate([{$group:{_id: '$name', sum_age: {$sum: '$age'}}}]);  --以name分组之后求和
```

### 统计$sum

```mongodb
示例：
db.user.aggregate([{$group:{_id: null, count: {'$sum': 1}}}]);     --不分组统计总数
db.user.aggregate([{$group:{_id: '$name', count: {'$sum': 1}}}]);  --以name分组之后统计总数
```

### 最大值$max

```mongodb
示例：
db.user.aggregate([{$group:{_id: null, count: {'$max': '$age'}}}]);     --不分组统计最大值
db.user.aggregate([{$group:{_id: '$name', count: {'$max': '$age'}}}]);  --以name分组之后统计最大值
```

### 最小值$min

```mongodb
示例：
db.user.aggregate([{$group:{_id: null, count: {'$min': '$age'}}}]);     --不分组统计最小值
db.user.aggregate([{$group:{_id: '$name', count: {'$min': '$age'}}}]);  --以name分组之后统计最小值
```

### 平均值$avg

```mongodb
示例：
db.user.aggregate([{$group:{_id: null, age_avg: {'$avg': '$age'}}}]);     --不分组统计平均值
db.user.aggregate([{$group:{_id: '$name', age_avg: {'$min': '$age'}}}]);  --以name分组之后统计平均值
```

### 字符串拼接

语法：`db.collection.aggregate([{"$project":{"<result_name>":{"$concat":["$<field>",...]}}}])`

连接字段必须是字符串，否则报错

`$project`：管道，进行字符串拼接处理，日期处理等操作的函数

```mongodb
示例：
db.user.aggregate([{$project: {'name-age':{$concat:['$name', '-', '$nickName']}}}]);
```

### 字符串转大写

```mongodb
示例：
db.user.aggregate([{$project: {nameUpper:{$toUpper:'$nickName'}}}]);
```

### 字符串转小写

```mongodb
示例：
db.user.aggregate([{$project: {nameUpper:{$toLower:'$nickName'}}}]);
```

### 截取字符串

```mongodb
示例：
db.user.aggregate([{$project: {nameSub:{$substr:['$nickName', 0, 3]}}}]);
```

### 日期格式化

```mongodb
示例：
db.user.insert({"birthDate":ISODate('2020-01-01T10:10:10.000Z')})
db.user.aggregate([{$project: {birth: {$dateToString: {format: '%Y年%m月%d日 %H:%M:%S', date: '$birthDate'}}}}]);
```

### 条件过滤

`$match`：匹配条件，放在前面，相当于SQL中的where子句，代表聚合之前进行条件筛选。放在后面，相当于SQL中的having子句。代表聚合之后进行条件筛选，只能筛选聚合结果，不能筛选聚合条件。

```mongodb
示例：
db.user.aggregate([{$match: {age: {$lt: 20}}},{$group:{_id: null, count: {$sum: 1}}}]);
```

# 运算符

在MongoDB中，数学类型（int/long/double）和日期类型（date）可以做数学运行。日期只能做加减。

**加法**

```mongodb
db.user.aggregate([{$project:{name: 1, new_age: {$add: ['$age', 1]}}}]);
```

**减法**

```mongodb
db.user.aggregate([{$project:{name: 1, new_age: {$subtract: ['$age', 1]}}}]);
```

**乘法**

```mongodb
db.user.aggregate([{$project:{name: 1, new_age: {$multiply: ['$age', 1]}}}]);
```

**除法**

```mongodb
db.user.aggregate([{$project:{name: 1, new_age: {$divide: ['$age', 1]}}}]);
```

**取模**

```mongodb
db.user.aggregate([{$project:{name: 1, new_age: {$mod: ['$age', 2]}}}]);
```

# 索引

在MongoDB3版本后，创建集合时默认为系统主键字段`_id`创建索引。且在关闭`_id`索引创建时会有警告提示。因为_id字段不创建索引，会导致Secondary在同步数据时负载变高。

## 创建索引

语法：`db.<collectionName>.ensureIndex(<keys>, <options>)`

- keys：用于创建索引的列及索引数据的排序规则。如：并升序索引`db.<collectionName>.ensureIndex({<keyName>:1})`、降序索引`db.<collectionName>.ensureIndex({<keyName>:-1})`
    
- options：创建索引时可定义的索引参数。可选参数如下
    
    |参数|类型|描述|
    |---|---|---|
    |background|Boolean|默认false。建索引过程会阻塞其它数据库操作，background可指定以后台方式创建索引|
    |unique|Boolean|默认false。建立的索引是否唯一，指定为true创建唯一索引|
    |name|string|索引的名称。如果未指定默认生成`<key>_<1/-1>`的名称|
    |sparse|Boolean|默认false，对文档中不存在的字段数据不启用索引|
    |expireAfterSeconds|integer|指定一个以秒为单位的数值，完成 TTL设定，设定索引的生存时间|
    
    如：`db.<collectionName>.ensureIndex({<key>:1}, {'background':true})`
    

## 查看索引

**查看集合的索引信息**

语法：`db.<collectionName>.getIndexes()`

**查看索引键**

语法：`db.<collectionName>.getIndexKeys()`

**查看索引详情**

语法：`db.<collectionName>.getIndexSpecs();`

**查看索引占用空间**

语法：`db.<collectionName>.totalIndexSize([is_detail])`

is_detail为false则只显示索引的总大小，为true显示该集合中每个索引的大小及总大小

**删除指定索引**

语法：`db.<collectionName>.dropIndex('<indexName>')`

**删除集合的所有自建索引**

语法：`db.<collectionName>.dropIndexes()`

此函数只删除自建索引，不会删除MongoDB创建的`_id`索引

**重建索引**

在MongoDB中使用`reIndex`函数重建索引。重建索引可以减少索引存储空间，减少索引碎片，优化索引查询效率。一般在数据大量变化后，会使用重建索引来提升索引性能。

语法：`db.<collectionName>.reIndex()`

## 索引类型

MongoDB支持多种类型的索引，包括单字段索引、复合索引、多key索引、文本索引等，每种类型的索引有不同的使用场合

### 单字段索引

`db.<collectionName>.ensureIndex({<field>:1});`

上述语句针对`field`创建了单字段索引，其能加速对此字段的各种查询请求，是最常见的索引形式。MongoDB默认创建的id索引也是这种类型。

### 交叉索引

为一个集合的多个字段分别建立索引，在查询的时候通过多个字段作为查询条件，这种情况称为交叉索引。

`db.<collectionName>.ensureIndex({<field_1>:1});`

`db.<collectionName>.ensureIndex({<field_2>:1});`

交叉索引的查询效率较低，例如`db.<collectionName>.find({<field_1>:<value_1>, <field_2>: <value_2>})`。在使用时，当查询使用到多个字段的时候，尽量使用复合索引，而不是交叉索引

### 复合|组合|聚合索引

针对多个字段联合创建索引，先按第一个字段排序，第一个字段相同的文档按第二个字段排序

`db.<collectionName>.ensureIndex({<field_1>:1, <field_2>:1})`

> 使用复合索引是需要注意最左前缀原则

### 多key索引

当索引的字段为数组时，创建出的索引称为多key索引，多key索引会为数组的每个元素建立一条索引

语法和建立一般索引一致`db.<collectionName>.ensureIndex( {<arrayFiled>: 1} )`

### 唯一索引

保证索引对应的字段不会出现相同的值，比如_id索引就是唯一索引。如果唯一索引所在字段有重复数据写入时，抛出异常

`db.<collectionName>.ensureIndex({<field_1>: 1}, {unique: true})`

### 部分索引

只针对符合某个特定条件的文档建立索引。部分索引就是带有过滤条件的索引，即索引只存在与某些文档之上

如：`db.<collectionName>.ensureIndex({<field_1>: 1},{partialFilterExpression: {field_1: {$gt: <filterValue>}}})`

只有当字段`field_1`大于指定的`filterValue`才建立索引，且`field_1`查询值比`filterValue`大时才生效

部分索引只为集合中那些满足指定的筛选条件的文档创建索引。如果你指定的partialFilterExpression和唯一约束、那么唯一性约束只适用于满足筛选条件的文档。具有唯一约束的部分索引不会阻止不符合唯一约束且不符合过滤条件的文档的插入。

## 查询计划

语法：`db.<collectionName>.find(<findContent>).explain()`

`winningPlain.stage`为`COLLSCAN`则为全表扫描，`IXSCAN`时使用了索引

# 集群

### 复制集（Replication Set）

MongoDB的复制至少需要两个节点。其中一个是主节点，负责处理客户端请求，其余的都是从节点，负责复制主节点上的数据。建议提供仲裁节点，此节点不存储数据，作用是当主节点出现故障时，选举出某个备用节点成为主节点，保证MongoDB的正常服务。客户端只需要访问主节点或从节点，不需要访问仲裁节点。

主节点记录在其上的所有操作oplog（操作日志），从节点定期轮询主节点获取这些操作，然后对自己的数据副本执行这些操作，从而保证从节点的数据与主节点一致。

MongoDB各个节点常见的搭配方式为：一主一从一仲裁、一主多从一仲裁。

### 环境准备

在一台主机上模拟使用单主机多端口的方式搭建复制集，1主2备1仲裁

①、创建数据目录

```
mkdir -p /opt/module/mongodb-replication-set/data/db-primary  主节点
mkdir -p /opt/module/mongodb-replication-set/data/db-s0       从节点
mkdir -p /opt/module/mongodb-replication-set/data/db-s1       从节点
mkdir -p /opt/module/mongodb-replication-set/data/db-arbiter  仲裁节点
```

②、创建配置目录

```
mkdir /opt/module/mongodb-replication-set/etc    创建配置目录
mkdir /opt/module/mongodb-replication-set/log    创建日志目录
mkdir /opt/module/mongodb-replication-set/pids   创建进程文件目录
```

③、配置文件

```
# Primary配置
vim /opt/module/mongodb-replication-set/etc/mongo-primary.conf
# 配置如下：
dbpath=/opt/module/mongodb-replication-set/data/db-primary          数据库目录
logpath=/opt/module/mongodb-replication-set/log/primary.log         日志文件
pidfilepath=/opt/module/mongodb-replication-set/pids/primary.pid    进程描述文件
bind_ip_all=true
directoryperdb=true                     为数据库自动提供重定向
logappend=true                          日志追加写入
replSet=rs                              复制集名称，一个复制集中的多个节点命名一致
port=37010                              端口
oplogSize=10000                         操作日志容量
fork=true                               后台启动

# Secondary-0配置
vim /opt/module/mongodb-replication-set/etc/mongo-s0.conf
# 配置如下：
dbpath=/opt/module/mongodb-replication-set/data/db-s0
logpath=/opt/module/mongodb-replication-set/log/secondary-0.log
pidfilepath=/opt/module/mongodb-replication-set/pids/secondary-0.pid
bind_ip_all=true
directoryperdb=true
logappend=true
replSet=rs
port=37011
oplogSize=10000
fork=true

# Secondary-1配置
vim /opt/module/mongodb-replication-set/etc/mongo-s1.conf
# 配置如下：
dbpath=/opt/module/mongodb-replication-set/data/db-s1
logpath=/opt/module/mongodb-replication-set/log/secondary-1.log
pidfilepath=/opt/module/mongodb-replication-set/pids/secondary-1.pid
bind_ip_all=true
directoryperdb=true
logappend=true
replSet=rs
port=37012
oplogSize=10000
fork=true

# Arbiter配置
vim /opt/module/mongodb-replication-set/etc/mongo-arbiter.conf
# 配置如下：
dbpath=/opt/module/mongodb-replication-set/data/db-arbiter
logpath=/opt/module/mongodb-replication-set/log/db-arbiter.log
pidfilepath=/opt/module/mongodb-replication-set/pids/db-arbiter.pid
bind_ip_all=true
directoryperdb=true
logappend=true
replSet=rs
port=37013
oplogSize=10000
fork=true
```

### 启动各节点

①、启动

```
bin/mongod --config /opt/module/mongodb-replication-set/etc/mongo-primary.conf
bin/mongod --config /opt/module/mongodb-replication-set/etc/mongo-s0.conf
bin/mongod --config /opt/module/mongodb-replication-set/etc/mongo-s1.conf
bin/mongod --config /opt/module/mongodb-replication-set/etc/mongo-arbiter.conf
```

②、访问主节点

```
 bin/mongo --port 37010
```

③、初始化复制集

```mongodb
rs.initiate({
    # 复制集命名，与配置文件对应
    _id:"rs",
    members:[
        # _id:唯一标记，host:主机地址，priority:权重（数字越大优先级越高），arbiterOnly:是否是仲裁节点
        {_id:0,host:"127.0.0.1:37010",priority:3},
        {_id:1,host:"127.0.0.1:37011",priority:1},
        {_id:2,host:"127.0.0.1:37012",priority:1},
        {_id:3,host:"127.0.0.1:37013",arbiterOnly:true}
    ]
});
```

④、查看状态

```mongodb
rs.status();
```

④、查看当前连接节点是否是Primary节点

```mongodb
rs.isMaster();
```

### 总结

当主节点宕机时，仲裁节点会根据配置信息中的权重值优先选举权重高的节点作为主节点继续提供服务。当宕机的主节点恢复后，复制集会恢复原主节点状态，临时主节点重新成为从节点。默认情况下直接连接从节点是无法查询数据的。因为从节点是不可读的。如果需要在从节点上读取数据，则需要在从节点控制台输入命令`rs.slaveOk([true|false])`来设置。`rs.slaveOk()`或`rs.slaveOk(true)`代表可以在从节点上做读操作；`rs.slaveOk(false)`代表不可在从节点上做读操作。

## 分片集群（shard cluster）

在Mongodb里面存在另一种集群，就是分片技术，可以满足MongoDB数据量大量增长的需求。当MongoDB存储海量的数据时，一台机器可能不足以存储数据，也可能不足以提供可接受的读写吞吐量。这时，我们就可以通过在多台机器上分割数据，使得数据库系统能存储和处理更多的数据。

sharding方案将整个数据集拆分成多个更小的chunk，并分布在集群中多个mongod节点上，最终达到存储和负载能力扩容、压力分流的作用。在sharding架构中，每个负责存储一部分数据的mongod节点称为shard（分片），shard上分布的数据块称为chunk，collections可以根据`shard key`（称为分片键）将数据集拆分为多个chunks，并相对均衡的分布在多个shards上。

### 各术语解释

**Shard**

用于存储实际的数据块，实际生产环境中一个shard server角色可由几台机器组个一个replica set承担，防止主机单点故障

**Config Server**

mongod实例，存储了整个ClusterMetadata，其中包括chunk信息。

**Routers**

前端路由，客户端由此接入，且让整个集群看上去像单一数据库，前端应用可以透明使用。

**Shard Key**

数据的分区根据`shard key`，对于每个需要sharding的collection，都需要指定`shard key`（分片键）；分片键必须是索引字段或者为组合索引的左前缀；mongodb根据分片键将数据分成多个chunks，并将它们均匀分布在多个shards节点上。目前，mongodb支持两种分区算法：区间分区（Range）和哈希（Hash）分区。

**Range分区**

首先`shard key`必须是数字类型或字符串类型（字符串类型根据索引排序作为分裂依据），整个区间的上下边界分别为正无穷大、负无穷大，每个chunk覆盖一段子区间，即整体而言，任何shard key均会被某个特定的chunk所覆盖。区间均为左闭右开。每个区间均不会有重叠覆盖，且互相临近。当然chunk并不是预先创建的，而是随着chunk数据的增大而不断split。

**Hash分区**

计算shard key的hash值（64位数字），并以此作为Range来分区。Hash值具有很强的散列能力，通常不同的shard key具有不同的hash值（冲突是有限的），这种分区方式可以将document更加随机的分散在不同的chunks上。

### 搭建分片集群

在一台主机上模拟使用单主机多端口的方式搭建集群，两个复制集（1主1备1仲裁），三个配置服务器（1主2备），一个路由节点

#### 环境准备

```mongodb
# 分片0的3个节点的数据目录，RS复制集，1主1备1仲裁
mkdir -p /opt/module/mongodb-cluster/data/rs0/primary
mkdir -p /opt/module/mongodb-cluster/data/rs0/slave
mkdir -p /opt/module/mongodb-cluster/data/rs0/arbiter

# 分片1的3个节点的数据目录，RS复制集，1主1备1仲裁
mkdir -p /opt/module/mongodb-cluster/data/rs1/primary
mkdir -p /opt/module/mongodb-cluster/data/rs1/slave
mkdir -p /opt/module/mongodb-cluster/data/rs1/arbiter

# 配置服务器的3个节点的数据目录，RS复制集，1主2备
mkdir -p /opt/module/mongodb-cluster/data/cf/primary
mkdir -p /opt/module/mongodb-cluster/data/cf/s0
mkdir -p /opt/module/mongodb-cluster/data/cf/s1

# 创建配置目录
mkdir -p /opt/module/mongodb-cluster/etc
mkdir -p /opt/module/mongodb-cluster/log
mkdir -p /opt/module/mongodb-cluster/pids
```

##### 搭建Shard

```mongodb
# RS0的Primary配置
vim /opt/module/mongodb-cluster/etc/rs0-primary.conf
# 配置如下：
shardsvr=true                                        代表当前节点是一个shard节点。
dbpath=/opt/module/mongodb-cluster/data/rs0/primary
logpath=/opt/module/mongodb-cluster/log/rs0-primary.log
pidfilepath=/opt/module/mongodb-cluster/pids/rs0-primary.pid
bind_ip_all=true
logappend=true
replSet=rs0
port=27010
oplogSize=10000
fork=true

# RS0的Secondary配置
vim /opt/module/mongodb-cluster/etc/rs0-slave.conf
# 配置如下：
dbpath=/opt/module/mongodb-cluster/data/rs0/slave
logpath=/opt/module/mongodb-cluster/log/rs0-slave.log
pidfilepath=/opt/module/mongodb-cluster/pids/rs0-slave.pid
bind_ip_all=true
shardsvr=true
logappend=true
replSet=rs0
port=27011
oplogSize=10000
fork=true

# RS0的arbiter配置
vim /opt/module/mongodb-cluster/etc/rs0-arbiter.conf
# 配置如下：
dbpath=/opt/module/mongodb-cluster/data/rs0/arbiter
logpath=/opt/module/mongodb-cluster/log/rs0-arbiter.log
pidfilepath=/opt/module/mongodb-cluster/pids/rs0-arbiter.pid
bind_ip_all=true
shardsvr=true
logappend=true
replSet=rs0
port=27012
oplogSize=10000
fork=true

# RS1的Primary配置
vim /opt/module/mongodb-cluster/etc/rs1-primary.conf
# 配置如下：
shardsvr=true
dbpath=/opt/module/mongodb-cluster/data/rs1/primary
logpath=/opt/module/mongodb-cluster/log/rs1-primary.log
pidfilepath=/opt/module/mongodb-cluster/pids/rs1-primary.pid
bind_ip_all=true
logappend=true
replSet=rs1
port=27020
oplogSize=10000
fork=true

# RS1的Secondary配置
vim /opt/module/mongodb-cluster/etc/rs1-slave.conf
# 配置如下：
dbpath=/opt/module/mongodb-cluster/data/rs1/slave
logpath=/opt/module/mongodb-cluster/log/rs1-slave.log
pidfilepath=/opt/module/mongodb-cluster/pids/rs1-slave.pid
bind_ip_all=true
shardsvr=true
logappend=true
replSet=rs1
port=27021
oplogSize=10000
fork=true

# RS1的arbiter配置
vim /opt/module/mongodb-cluster/etc/rs1-arbiter.conf
# 配置如下：
dbpath=/opt/module/mongodb-cluster/data/rs1/arbiter
logpath=/opt/module/mongodb-cluster/log/rs1-arbiter.log
pidfilepath=/opt/module/mongodb-cluster/pids/rs1-arbiter.pid
bind_ip_all=true
shardsvr=true
logappend=true
replSet=rs1
port=27022
oplogSize=10000
fork=true
```

#### 启动Shard

```
bin/mongod --config etc/rs0-primary.conf
bin/mongod --config etc/rs0-slave.conf
bin/mongod --config etc/rs0-arbiter.conf
bin/mongod --config etc/rs1-primary.conf
bin/mongod --config etc/rs1-slave.conf
bin/mongod --config etc/rs1-arbiter.conf
```

#### 配置Shard

```mongodb
bin/mongo --port 27010
rs.initiate({
    _id:"rs0",
    members:[
        {_id:0,host:"127.0.0.1:27010",priority:2},
        {_id:1,host:"127.0.0.1:27011",priority:1},
        {_id:3,host:"127.0.0.1:27012",arbiterOnly:true}
    ]
});

bin/mongo --port 27020
rs.initiate({
    _id:"rs1",
    members:[
        {_id:0,host:"127.0.0.1:27020",priority:2},
        {_id:1,host:"127.0.0.1:27021",priority:1},
        {_id:3,host:"127.0.0.1:27022",arbiterOnly:true}
    ]
});
```

#### 搭建Config Server

config server的复制集中不允许有单仲裁节点。复制集初始化命令中，不允许设置arbiterOnly:true参数

```
# Config Server的Primary配置
vim /opt/module/mongodb-cluster/etc/cf-primary.conf
# 配置如下：
dbpath=/opt/module/mongodb-cluster/data/cf/primary
logpath=/opt/module/mongodb-cluster/log/cf-primary.log
pidfilepath=/opt/module/mongodb-cluster/pids/cf-primary.pid
bind_ip_all=true
logappend=true
replSet=cf
port=27030
oplogSize=10000
fork=true
configsvr=true                     代表当前节点是一个配置服务节点

# Config Server的s0配置
vim /opt/module/mongodb-cluster/etc/cf-s0.conf
# 配置如下：
dbpath=/opt/module/mongodb-cluster/data/cf/s0
logpath=/opt/module/mongodb-cluster/log/cf-s0.log
pidfilepath=/opt/module/mongodb-cluster/pids/cf-s0.pid
bind_ip_all=true
logappend=true
replSet=cf
port=27031
oplogSize=10000
fork=true
configsvr=true

# Config Server的s1配置
vim /opt/module/mongodb-cluster/etc/cf-s1.conf
# 配置如下：
dbpath=/opt/module/mongodb-cluster/data/cf/s1
logpath=/opt/module/mongodb-cluster/log/cf-s1.log
pidfilepath=/opt/module/mongodb-cluster/pids/cf-s1.pid
bind_ip_all=true
logappend=true
replSet=cf
port=27032
oplogSize=10000
fork=true
configsvr=true
```

#### 启动Config Server

```
bin/mongod --config etc/cf-primary.conf
bin/mongod --config etc/cf-s0.conf
bin/mongod --config etc/cf-s1.conf
```

#### 配置Config Server

```
bin/mongo --port 27030
rs.initiate({
    _id:"cf",
    members:[
        {_id:0,host:"127.0.0.1:27030",priority:2},
        {_id:1,host:"127.0.0.1:27031",priority:1},
        {_id:3,host:"127.0.0.1:27032",priority:1}
    ]
});
```

#### 搭建Router

生成环境中通常提供多个，使用keepalive和haproxy实现高可用。router不需要数据库目录，不需要配置dbpath。

```mongodb
vim /opt/module/mongodb-cluster/etc/rt.conf
# 配置如下：
configdb=cf/127.0.0.1:27030,127.0.0.1:27031,127.0.0.1:27032
logpath=/opt/module/mongodb-cluster/log/rt.log
pidfilepath=/opt/module/mongodb-cluster/pids/rt.pid
port=27040
fork=true
bind_ip_all=true
```

#### 启动Router

注意使用的是`mongos`命令

```
bin/mongos --config etc/rt.conf
```

#### 配置Router

```mongodb
# 连接
bin/mongo --port 27040

# 进入admin库
use admin

# 加入分片信息
db.runCommand({'addShard':'rs0/127.0.0.1:27010,127.0.0.1:27011,127.0.0.1:27012'});
db.runCommand({'addShard':'rs1/127.0.0.1:27020,127.0.0.1:27021,127.0.0.1:27022'});
```

#### 开启Shard

首先需要将Database开启sharding，否则数据仍然无法在集群中分布。即数据库、collection默认为non-sharding。对于non-sharding的database或者collection均会保存在primary shard上，直到开启sharding才会在集群中分布。

```mongodb
# 创建测试库
use test
# 开启Shard，开启分片命令必须在admin库下运行。
use admin
db.runCommand({ enablesharding: 'test'})

# collection开启sharding，在此之前需要先指定shard key和建立"shard key索引"
use test
db.users.ensureIndex({'_id':'hashed'});
db.runCommand({ shardcollection: 'test.users', key: {'_id': 'hashed'}})

# users集合将使用"_id"作为第一维shard key，采用hashed分区模式，可以通过sh.status()查看每个chunk的分裂区间
sh.status()
```

在GridFS开启Shard

```mongodb
db.runCommand( { shardCollection : "test.fs.chunks" , key : {  files_id : 1 } } )
# 在GridFS中，对chunks集合进行分片时，只有两个片键可以选择，{ files_id : 1 , n : 1 } 与 {  files_id : 1 }
```

# golang 操作 Mongodb
### 安装mongoDB Go驱动包

```bash
go get github.com/mongodb/mongo-go-driver
```

### 通过Go代码连接mongoDB

```go
package main

import (
	"context"
	"fmt"
	"log"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func main() {
	// 设置客户端连接配置
	clientOptions := options.Client().ApplyURI("mongodb://localhost:27017")

	// 连接到MongoDB
	client, err := mongo.Connect(context.TODO(), clientOptions)
	if err != nil {
		log.Fatal(err)
	}

	// 检查连接
	err = client.Ping(context.TODO(), nil)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Connected to MongoDB!")
}
```

连接上MongoDB之后，可以通过下面的语句处理我们上面的q1mi数据库中的student数据集了：

```go
// 指定获取要操作的数据集
collection := client.Database("q1mi").Collection("student")
```

处理完任务之后可以通过下面的命令断开与MongoDB的连接：

```go
// 断开连接
err = client.Disconnect(context.TODO())
if err != nil {
	log.Fatal(err)
}
fmt.Println("Connection to MongoDB closed.")
```

### 连接池模式

```go
import (
	"context"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func ConnectToDB(uri, name string, timeout time.Duration, num uint64) (*mongo.Database, error) {
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()
	o := options.Client().ApplyURI(uri)
	o.SetMaxPoolSize(num)
	client, err := mongo.Connect(ctx, o)
	if err != nil {
		return nil, err
	}

	return client.Database(name), nil
}
```

### BSON

MongoDB中的JSON文档存储在名为BSON(二进制编码的JSON)的二进制表示中。与其他将JSON数据存储为简单字符串和数字的数据库不同，BSON编码扩展了JSON表示，使其包含额外的类型，如int、long、date、浮点数和decimal128。这使得应用程序更容易可靠地处理、排序和比较数据。

连接MongoDB的Go驱动程序中有两大类型表示BSON数据：`D`和`Raw`。

类型`D`家族被用来简洁地构建使用本地Go类型的BSON对象。这对于构造传递给MongoDB的命令特别有用。`D`家族包括四类:

- D：一个BSON文档。这种类型应该在顺序重要的情况下使用，比如MongoDB命令。
- M：一张无序的map。它和D是一样的，只是它不保持顺序。
- A：一个BSON数组。
- E：D里面的一个元素。

要使用BSON，需要先导入下面的包：

```go
import "go.mongodb.org/mongo-driver/bson"
```

下面是一个使用D类型构建的过滤器文档的例子，它可以用来查找name字段与’张三’或’李四’匹配的文档:

```go
bson.D{{
	"name",
	bson.D{{
		"$in",
		bson.A{"张三", "李四"},
	}},
}}
```

`Raw`类型家族用于验证字节切片。你还可以使用`Lookup()`从原始类型检索单个元素。如果你不想要将BSON反序列化成另一种类型的开销，那么这是非常有用的。这个教程我们将只使用D类型。

### CRUD

我们现在Go代码中定义一个`Studet`类型如下：

```go
type Student struct {
	Name string
	Age int
}
```

接下来，创建一些`Student`类型的值，准备插入到数据库中：

```go
s1 := Student{"小红", 12}
s2 := Student{"小兰", 10}
s3 := Student{"小黄", 11}
```

#### 插入文档

使用`collection.InsertOne()`方法插入一条文档记录：

```go
insertResult, err := collection.InsertOne(context.TODO(), s1)
if err != nil {
	log.Fatal(err)
}

fmt.Println("Inserted a single document: ", insertResult.InsertedID)
```

使用`collection.InsertMany()`方法插入多条文档记录：

```go
students := []interface{}{s2, s3}
insertManyResult, err := collection.InsertMany(context.TODO(), students)
if err != nil {
	log.Fatal(err)
}
fmt.Println("Inserted multiple documents: ", insertManyResult.InsertedIDs)
```

#### 更新文档

`updateone()`方法允许你更新单个文档。它需要一个筛选器文档来匹配数据库中的文档，并需要一个更新文档来描述更新操作。你可以使用`bson.D`类型来构建筛选文档和更新文档:

```go
filter := bson.D{{"name", "小兰"}}

update := bson.D{
	{"$inc", bson.D{
		{"age", 1},
	}},
}
```

接下来，就可以通过下面的语句找到小兰，给他增加一岁了：

```go
updateResult, err := collection.UpdateOne(context.TODO(), filter, update)
if err != nil {
	log.Fatal(err)
}
fmt.Printf("Matched %v documents and updated %v documents.\n", updateResult.MatchedCount, updateResult.ModifiedCount)
```

#### 查找文档

要找到一个文档，你需要一个filter文档，以及一个指向可以将结果解码为其值的指针。要查找单个文档，使用`collection.FindOne()`。这个方法返回一个可以解码为值的结果。

我们使用上面定义过的那个filter来查找姓名为’小兰’的文档。

```go
// 创建一个Student变量用来接收查询的结果
var result Student
err = collection.FindOne(context.TODO(), filter).Decode(&result)
if err != nil {
	log.Fatal(err)
}
fmt.Printf("Found a single document: %+v\n", result)
```

要查找多个文档，请使用`collection.Find()`。此方法返回一个游标。游标提供了一个文档流，你可以通过它一次迭代和解码一个文档。当游标用完之后，应该关闭游标。下面的示例将使用`options`包设置一个限制以便只返回两个文档。

```go
// 查询多个
// 将选项传递给Find()
findOptions := options.Find()
findOptions.SetLimit(2)

// 定义一个切片用来存储查询结果
var results []*Student

// 把bson.D{{}}作为一个filter来匹配所有文档
cur, err := collection.Find(context.TODO(), bson.D{{}}, findOptions)
if err != nil {
	log.Fatal(err)
}

// 查找多个文档返回一个光标
// 遍历游标允许我们一次解码一个文档
for cur.Next(context.TODO()) {
	// 创建一个值，将单个文档解码为该值
	var elem Student
	err := cur.Decode(&elem)
	if err != nil {
		log.Fatal(err)
	}
	results = append(results, &elem)
}

if err := cur.Err(); err != nil {
	log.Fatal(err)
}

// 完成后关闭游标
cur.Close(context.TODO())
fmt.Printf("Found multiple documents (array of pointers): %#v\n", results)
```

#### 删除文档

最后，可以使用`collection.DeleteOne()`或`collection.DeleteMany()`删除文档。如果你传递`bson.D{{}}`作为过滤器参数，它将匹配数据集中的所有文档。还可以使用`collection. drop()`删除整个数据集。

```go
// 删除名字是小黄的那个
deleteResult1, err := collection.DeleteOne(context.TODO(), bson.D{{"name","小黄"}})
if err != nil {
	log.Fatal(err)
}
fmt.Printf("Deleted %v documents in the trainers collection\n", deleteResult1.DeletedCount)
// 删除所有
deleteResult2, err := collection.DeleteMany(context.TODO(), bson.D{{}})
if err != nil {
	log.Fatal(err)
}
fmt.Printf("Deleted %v documents in the trainers collection\n", deleteResult2.DeletedCount)
```

更多方法请查阅[官方文档](https://godoc.org/go.mongodb.org/mongo-driver)。

