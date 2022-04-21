# scrapy-redis-cluster
scrapy-redis 集群版

本项目基于原项目 [scrapy-redis](https://github.com/rmax/scrapy-redis)
参考 [scrapy-redis-sentinel](https://github.com/crawlaio/scrapy-redis-sentinel)

修改：
1. 更新 `redis>=4.2.2` 依赖库，添加 redis 集群支持

## 配置示例

> 原版本 scrapy-redis 的所有配置都支持, 优先级：哨兵模式 > 集群模式 > 单机模式

```python
# ----------------------------------------Bloomfilter 配置-------------------------------------
# 使用的哈希函数数，默认为 6
BLOOMFILTER_HASH_NUMBER = 6

# Bloomfilter 使用的 Redis 内存位，30 表示 2 ^ 30 = 128MB，默认为 30   (2 ^ 22 = 1MB 可去重 130W URL)
BLOOMFILTER_BIT = 30

# 是否开启去重调试模式 默认为 False 关闭
DUPEFILTER_DEBUG = False

# REDIS 配置参数
REDIS_PARAMS = {
    "password": "password",
    "db": 0
}

# ----------------------------------------Redis 单机模式-------------------------------------
# Redis 单机地址
# REDIS_HOST = "172.25.2.25"
# REDIS_PORT = 6379

# ----------------------------------------Redis 集群模式-------------------------------------
# Redis 集群地址
REDIS_STARTUP_NODES = [
    {"host": "172.25.2.25", "port": "6379"},
    {"host": "172.25.2.26", "port": "6379"},
    {"host": "172.25.2.27", "port": "6379"},
]

# ----------------------------------------Scrapy 其他参数-------------------------------------

# 在 redis 中保持 scrapy-redis 用到的各个队列，从而允许暂停和暂停后恢复，也就是不清理 redis queues
SCHEDULER_PERSIST = True
# 调度队列  
SCHEDULER = "scrapy_redis_cluster.scheduler.Scheduler"
# 基础去重
DUPEFILTER_CLASS = "scrapy_redis_cluster.dupefilter.RedisDupeFilter"
# BloomFilter
# DUPEFILTER_CLASS = "scrapy_redis_cluster.dupefilter.RedisBloomFilter" # TODO

# 启用基于 Redis 统计信息
STATS_CLASS = "scrapy_redis_cluster.stats.RedisStatsCollector"

# 指定排序爬取地址时使用的队列
# 默认的 按优先级排序( Scrapy 默认)，由 sorted set 实现的一种非 FIFO、LIFO 方式。
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis_cluster.queue.SpiderPriorityQueue'
# 可选的 按先进先出排序（FIFO）
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis_cluster.queue.SpiderQueue'
# 可选的 按后进先出排序（LIFO）
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis_cluster.queue.SpiderStack'
```
