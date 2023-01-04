[TOC]
## 1.Redis是什么
+ 是一个BSD许可开源的，内存数据库
+ 支持多种类型存储数据结构，常见的有：字符串（string），哈希表（hashes），列表（lists），集合（sets），有序集合（sorted sets）
+ 支持磁盘持久化（RDB和AOF）
+ 支持多种部署模式，主从（包含单机），哨兵（sentinel）和集群（cluster）
+ 单线程架构，从6.0版本开始，支持多线程
+ 所有操作都是原子性的，同时还支持多个操作合并成原子性执行
&nbsp;
## 2.高并发原理
+ 纯内存数据库，存取速度快
+ 使用的是非阻塞IO，IO多路复用，使用了单线程来轮询描述符
+ 采用了单线程模型，保证了每个操作的原子性，也减少了线程的上下文切换和竞争
&nbsp;
## 3.安装（单机、源码安装）
### 3.1.下载
当前版本7.0.6，下载目录为linux当前用户目录
```
wget https://download.redis.io/releases/redis-7.0.6.tar.gz
```
### 3.2.解压到安装目录（/usr/local/redis）
```
mkdir -p /usr/local/redis
```
```
tar -xzvf redis-7.0.6.tar.gz --strip-components 1 -C /usr/local/redis
```
### 3.3.编译
```
cd /usr/local/redis
```
```
make
```
### 3.4.安装
```
make PREFIX=/usr/local/redis install
```
PREFIX关键字的作用是，安装时候用于指定程序存放的路径。如果不指定，那么可执行文件会安装在/usr/local/bin目录，库文件安装在/usr/local/lib目录，配置文件安装在/usr/local/etc目录，其他资源文件安装在/usr/local/share目录。

目前统一安装在/usr/local/redis目录，卸载redis即删除这个目录。
### 3.5.配置文件详解
| 配置项名称 | 配置项值范围 | 说明 |
| :-----| :---- | :---- |
| daemonize | yes、no | yes：启用守护进程；no：不启用 |
| port |  | 指定redis监听端口，默认端口为6379 |
| bind |  | 绑定的主机地址，如果需要设置远程访问，则将这个属性注释或者改为bind * 即可，这个属性和下面的protected-mode控制了是否可以远程访问 |
| protected-mode | yes、no | 保护模式，该模式控制外部网是否可以连接redis服务，默认是yes，所以默认外网是无法访问的，如需外网连接redis服务则需要将此属性改为no |
| dir |  | 指定本地数据库存放目录 |
| dbfilename | dump.rdb | 指定本地数据库文件名，默认值为 dump.rdb |
| requirepass |  | 设置redis连接密码，如果配置了连接密码，客户端在连接 时需要通过 AUTH <password> 命令提供密码，默认关闭 |
| maxclients | 0 | 设置同一时间最大客户端连接数，默认无限制，redis可以同时打开的客户端连接数为redis进程可以打开的最大文件描述符数，如果设置 maxclients 0，表示不作限制。当客户端连接数到达限制时，redis会关闭新的连接并向客户端返回 max number of clients reached 错误信息 |
| maxmemory |  | 指定redis最大内存限制，redis在启动时会把数据加载到内存中，达到最大内存后，redis会先尝试清除已到期或即将到期的 Key，当此方法处理后，仍然到达最大内存设置，将无法再进行写入操作，但仍然可以进行读取操作。redis新的 vm 机制，会把Key存放内存，Value会存放在 swap 区。配置项值范围列里XXX为数值。 |
| logfile | /usr/local/redis/log/redis.log | 指定本地日志存放目录 |
| save 900 1<br/>save 300 10<br/>save 60 10000 |  | 默认rdb方式持久化<br/>900秒内，如果超过1个key被修改，则发起快照保存<br/>300秒内，如果超过10个key被修改，则发起快照保存<br/>60秒内，如果1万个key被修改，则发起快照保存 |
| appendonly | yes、no | yes：开启AOF持久化方式，默认为no，存在数据丢失情况 |
| appendfsync | always、everysec、no | AOF持久化策略 |
### 3.6.启动
```
./bin/redis-server ./redis.conf
```
&nbsp;
## 4.操作Redis
### 4.1.通用命令
+ keys：查看所有键
+ dbsize：键总数
+ exists key：检查键是否存在
+ del key [key ...]：删除键
+ expire key seconds：键过期
+ ttl key：通过 ttl 命令观察键键的剩余过期时间
+ type key：键的数据结构类型
+ object encoding key：查询内部编码
### 4.2.字符串（string）
+ set key value [ex seconds] [px milliseconds] [nx|xx]：设置值，返回 ok 表示成功
  + ex seconds：为键设置秒级过期时间
  + px milliseconds：为键设置毫秒级过期时间
  + nx：键必须不存在，才可以设置成功，用于添加。可单独用 setnx 命令替代
  + xx；与nx相反，键必须存在，才可以设置成功，用于更新。可单独用 setxx 命令替代
+ get key：获取值
+ mset key value [key value ...]：批量设置值，批量操作命令可以有效提高业务处理效率
+ mget key [key ...]：批量获取值
+ incr key：计数，返回结果分 3 种情况：
  + 值不是整数，返回错误
  + 值是整数，返回自增后的结果
  + 键不存在，按照值为0自增，返回结果为1
+ decr(自减)、incrby(自增指定数字)、 decrby(自减指定数字)
### 4.3.哈希表（hashes）
渐进式rehash策略。
+ hset key field value：设置值
+ hget key field：获取值
+ hdel key field [field ...]：删除field
+ hlen key：计算field个数
+ hmset key field value [field value ...]：批量设置field-value
+ hmget key field [field ...]：批量获取field-value
+ hexists key field：判断field是否存在
+ hkeys key：获取所有field
+ hvals key：获取所有value
+ hgetall key：获取所有的field-value
+ incrbyfloat和hincrbyfloat：就像incrby和incrbyfloat命令一样，但是它们的作 用域是 filed
### 4.4.列表（lists）
实现原理是一个双向链表（其底层是一个快速列表），即可以支持反向查找和遍历，更方便操作。插入和删除操作非常快，时间复杂度为 O(1)，但是索引定位很慢，时间复杂度为 O(n)。
+ rpush key value [value ...]：从右边插入元素
+ lpush key value [value ...]：从左边插入元素
+ linsert key before|after pivot value：向某个元素前或者后插入元素
+ lrange key start end：获取指定范围内的元素列表，lrange key 0 -1可以从左到右获取列表的所有元素
+ lindex key index：获取列表指定索引下标的元素
+ llen key：获取列表长度
+ lpop key：从列表左侧弹出元素
+ rpop key：从列表右侧弹出
+ lrem key count value：删除指定元素，lrem命令会从列表中找到等于value的元素进行删除，根据count的不同 分为三种情况:
  + count>0，从左到右，删除最多count个元素
  + count<0，从右到左，删除最多count绝对值个元素
  + count=0，删除所有
+ ltrim key start end：按照索引范围修剪列表
+ lset key index newValue：修改指定索引下标的元素
+ blpop key [key ...] timeout 和 brpop key [key ...] timeout：阻塞式弹出
### 4.5.集合（sets）
+ sadd key element [element ...]：添加元素，返回结果为添加成功的元素个数
+ srem key element [element ...]：删除元素，返回结果为成功删除元素个数
+ smembers key：获取所有元素
+ sismember key element：判断元素是否在集合中，如果给定元素element在集合内返回1，反之返回0
+ scard key：计算元素个数，scard的时间复杂度为O(1)，它不会遍历集合所有元素
+ spop key：从集合随机弹出元素，从3.2版本开始，spop也支持[count]参数。
+ srandmember key [count]：随机从集合返回指定个数元素，[count]是可选参数，如果不写默认为1
+ sinter key [key ...]：求多个集合的交集
+ suinon key [key ...]：求多个集合的并集
+ sdiff key [key ...]：求多个集合的差集
### 4.6.有序集合（sorted sets）
zset可能是redis提供的最为特色的数据结构。一方面它是一个set，保证了内部value的唯一性，另一方面它可以给每个value赋予一个score，代表这个value的排序权重。它的内部实现用的是一种叫着「跳跃列表」的数据结构。
+ zadd key score member [score member ...]：添加成员，返回结果代表成功添加成员的个数。Redis3.2为zadd命令添加了nx、xx、ch、incr四个选项:
  + nx:member必须不存在，才可以设置成功，用于添加
  + xx:member必须存在，才可以设置成功，用于更新
  + ch:返回此次操作后，有序集合元素和分数发生变化的个数
  + incr:对score做增加，相当于后面介绍的zincrby
+ zcard key：计算成员个数
+ zscore key member：计算某个成员的分数
+ zrank key member 和 zrevrank key member：计算成员的排名，zrank是从分数从低到高返回排名，zrevrank反之
+ zrem key member [member ...]：删除成员
+ zincrby key increment member：增加成员的分数
+ zrange key start end [withscores] 和 zrevrange key start end [withscores]：返回指定排名范围的成员，zrange是从低到高返回，zrevrange反之
+ zrangebyscore key min max [withscores] [limit offset count] 和 zrevrangebyscore key max min [withscores] [limit offset count] 返回指定分数范围的成员，其中zrangebyscore按照分数从低到高返回，zrevrangebyscore反之
+ zcount key min max：返回指定分数范围成员个数
+ zremrangebyrank key start end：删除指定排名内的升序元素
+ zremrangebyscore key min max：删除指定分数范围的成员
+ zinterstore 和 zunionstore 命令求集合的交集和并集，可用参数比较多，可用到再查文档
&nbsp;
## 5.慢查询
### 5.1.配置
| 配置项名称 | 配置值范围 | 说明 |
| :-----| :---- | :---- |
| slowlog-log-slower-than | int | 单位微妙，默认是 10000 微秒<br/>0：记录所有命令到日志<br/><0：将不记录任何命令到日志 |
| slowlog-max-len | int | 指定慢查询日志最多存储的条数 |
### 5.2.获取慢查询日志
```
>slowlog get count

# 获取慢查询日志的长度
>slowlog len

# 清理慢查询日志
>slowlog reset
```
&nbsp;
## 6.Pipeline机制
它能将一组redis命令进行组装，通过一次rtt传输给redis，再将这组 redis命令的执行结果按顺序返回给客户端。
&nbsp;
## 7.事务与Lua
### 7.1.multi和exec命令
### 7.2.Lua
&nbsp;
## 8.发布订阅
+ subscribe channel [channel ...]：订阅一个或多个频道
+ unsubscribe channel：退订指定频道
+ publish channel message：发送消息
+ psubscribe pattern：订阅指定模式
+ punsubscribe pattern：退订指定模式

```
>subscribe Testchannel
Reading messages... (press Ctrl-C to quit)
1) "subscribe"
2) "Testchannel"
3) (integer) 1

1) "message"
2) "Testchannel"
3) "Helloworld"

>publish Testchannel Helloworld
(integer) 1
```

publish的消息是不会被持久化的，也即是说新订阅的客户端不会接收到历史消息。
&nbsp;
## 9.持久化
&nbsp;
## 10.高可用机制
### 10.1.哨兵（sentinel）
### 10.2.集群（cluster）
&nbsp;
## 11.缓存策略
| 策略 | 数据一致性 | 成本 |
| :-----| :---- | :---- |
| LRU/LFU/FIFO | 最差 | 低 |
| 超时剔除 | 较差 | 低 |
| 主动更新 | 最好 | 高 |
### 11.1.缓存穿透
查询一个不存在的数据，缓存miss，每次均从存储层查询
### 11.2.缓存雪崩
设置缓存时采用了相同的过期时间，导致缓存在某一时刻同时失效
### 11.3.缓存击穿
热点数据缓存过期，并发请求透传到存储层
&nbsp;
## 12.知识拓展 - 缓存设计
如何保证缓存和数据库一致性呢？操作顺序大概可以分为下面四种情况：
+ 先更新数据库，再更新缓存
+ 先更新缓存，再更新数据库
+ 先删除缓存，再更新数据库
+ 先更新数据库，再删除缓存
&nbsp;
## 13.分布式锁
&nbsp;
## 14.FAQ