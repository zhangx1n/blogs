•写sql时一律使用小写
•建表时先判断表是否已存在 if not exists
•所有的列和表都加comment
•字符串长度比较短时尽量使用char，定长有利于内存对齐，读写
性能更好，而varchar字段频繁修改时容易产生内存碎片
• 满足需求的前提下尽量使用短的数据类型，如tinyint vs int, float vs double, date vs datetime