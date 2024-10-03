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
- `sql ="'select username,password from user where username=" + username +" and password=" + password + `
变量username和password从前端输入框获取，如果用户输入的
username为lily，password为aaa' or '1'='1
则完整的sql为select username,password from user where
username="ily' and password='aaa'or '1'='1'
会返回表里的所有记录，如果记录数大于0就允许登录，则lily的
账号被盗