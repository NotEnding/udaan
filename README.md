## 印度电商系统 https://udaan.com/ 爬虫 ##
* Udaan是一个以网络为中心的B2B平台，专为印度的中小型企业而设计

## 抓取要求
* 获取商品信息
* 获取供应商信息

## 抓取步骤
* 1、根据api https://udaan.com/api/search/v1?start={} 获取全部的orgId
```
该接口返回全部的商品信息
https://udaan.com/api/search/v1
```
* 2、api https://udaan.com/api/search/v1?orgId={orgId}&start={start} 获取该店铺下的的listingId
```
查看一个店铺下的商品 
https://udaan.com/api/search/v1?orgId={店铺orgId}
exp:https://udaan.com/api/search/v1?orgId=ORG6GMELVHG8PQVWFEJHSVRCNKPKD
exp:https://udaan.com/api/search/v1?orgId=ORG6GMELVHG8PQVWFEJHSVRCNKPKD&start=12 查看更多
```
* 3、通过api https://udaan.com/api/listings/v1/{listingId} 获取对应listingId 的商品详情数据
```
获取一个商品的详情
https://udaan.com/api/listings/v1/{商品listingId}
exp:https://udaan.com/api/listings/v1/TLESIFPPM41PKNZC6TFDBHSRBF370ST
```

## 代码结构
* api 目录下为爬虫请求基础类
* auxiliary 目录下为辅助类，包含数据库连接类，自动刷新token类，日志类
* conf 目录下为 source.yaml 文件，存放基础配置
* crawler 目录下为 获取orgId,获取listingId,获取listing detail,获取categories,best-seller,fast-moving,latest-arrival 
* log 目录存放日志文件
* categories_runner 为获取分类启动文件
* listing_detail_runner 为获取商品详情启动文件
* listingId_runner 为获取商品id启动文件
* orgId_runner 为获取店铺ID启动文件
* settings 常量配置文件

## 数据库---数据存储在mongo 数据库中
* listings_info 商品表
* orgs_info 供应商表(店铺信息)
* categories_info 分类表
* fast_moving_listings_info 
* best_seller_listings_info
* latest_arrival_listings_info