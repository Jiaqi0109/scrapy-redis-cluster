# scrapy-redis-cluster
scrapy-redis 集群版

本项目基于原项目 [scrapy-redis](https://github.com/rmax/scrapy-redis)  
参考 [scrapy-redis-sentinel](https://github.com/crawlaio/scrapy-redis-sentinel)

更新：
1. 更新 `redis>=4.2.2` 依赖库，添加 redis cluster支持，不支持redis sentinel
2. 添加支持bloomfilter

## 配置示例

> 原版本 scrapy-redis 的所有配置都支持

```python
# ----------------------------------------Bloomfilter 配置-------------------------------------
# 布隆过滤器期望过滤的数量，默认为 100000000
BLOOMFILTER_CAPACITY = 100000000
# 期望错误率 默认为 1 / 100000
BLOOMFILTER_ERRORRATE = 1e-5

# 是否开启去重调试模式 默认为 False 关闭
DUPEFILTER_DEBUG = False

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

# REDIS 配置参数
REDIS_PARAMS = {
    "password": "password",
    "db": 0
}

# ----------------------------------------Scrapy 其他参数-------------------------------------

# 在 redis 中保持 scrapy-redis 用到的各个队列，从而允许暂停和暂停后恢复，也就是不清理 redis queues
SCHEDULER_PERSIST = True
# 调度队列  
SCHEDULER = "scrapy_redis_cluster.scheduler.Scheduler"
# 基础去重
DUPEFILTER_CLASS = "scrapy_redis_cluster.dupefilter.RedisDupeFilter"

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
