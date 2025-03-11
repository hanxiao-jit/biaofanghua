# 电商H5应用后端API

这是一个基于Flask的电商H5应用后端API服务，为前端Vue.js应用提供数据支持。使用MySQL数据库存储数据。

## 功能特点

- 用户管理：注册、登录、获取用户信息
- 商品管理：获取商品列表、商品详情
- 购物车：添加、更新、删除购物车项
- 订单管理：创建订单、获取订单列表、更新订单状态
- 分销系统：创建推广链接、查看分销记录、统计分销数据
- 数据导出：导出用户信息和购买记录

## 项目结构

```
biaofanghua_user_h5/
├── app.py                # Flask应用主文件，包含API实现和数据库模型
├── requirements.txt      # 依赖文件
├── create_tables.py      # 创建数据库表
├── init_data.py          # 初始化测试数据
├── run.py                # 启动应用程序
├── static/               # 静态资源
│   └── images/           # 图片资源
└── templates/            # 模板文件
    └── index.html        # API文档页面
```

## 数据库设置

本项目使用MySQL数据库存储数据：

- 主机：47.100.101.95
- 端口：3306
- 用户名：root
- 数据库名：biaofanghua_user_h5

## 安装和运行

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 创建数据库表

```bash
python create_tables.py
```

3. 初始化测试数据

```bash
python init_data.py
```

4. 运行应用

```bash
python run.py
```

应用将在 http://127.0.0.1:5000/ 运行。

## 数据库表结构

系统包含以下主要数据表：

- `users` - 用户信息
- `products` - 商品信息
- `cart_items` - 购物车项
- `orders` - 订单信息
- `order_items` - 订单商品项
- `affiliate_links` - 分销推广链接
- `affiliate_records` - 分销记录

## API接口文档

### 用户相关接口

- `POST /api/user/register` - 注册新用户
- `POST /api/user/login` - 用户登录
- `GET /api/user/info` - 获取用户信息

### 商品相关接口

- `GET /api/products` - 获取商品列表
- `GET /api/products/<product_id>` - 获取商品详情

### 购物车相关接口

- `GET /api/cart` - 获取购物车
- `POST /api/cart/add` - 添加商品到购物车
- `POST /api/cart/update` - 更新购物车项
- `POST /api/cart/remove` - 从购物车中移除商品

### 订单相关接口

- `GET /api/orders` - 获取订单列表
- `GET /api/orders/<order_id>` - 获取订单详情
- `POST /api/orders/create` - 创建订单
- `POST /api/orders/<order_id>/status` - 更新订单状态

### 分销相关接口

- `GET /api/affiliate/links` - 获取推广链接列表
- `POST /api/affiliate/links/create` - 创建推广链接
- `GET /api/affiliate/records` - 获取分销记录
- `GET /api/affiliate/stats` - 获取分销统计数据

### 数据导出接口

- `GET /api/export/user` - 导出用户信息
- `GET /api/export/orders` - 导出用户订单

## 测试账户

初始化数据提供了以下测试账户：

- 普通用户: username=`test`, password=`test123`
- 管理员: username=`admin`, password=`admin123`

## 前端项目

本API服务设计用于配合Vue.js前端项目使用。前端项目结构请参考相关文档。 