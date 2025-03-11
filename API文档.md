# 电商H5后端API接口文档

本文档详细列出了电商H5应用后端API的所有接口、参数和返回数据格式。

## 基本信息

- **基础URL**: `http://47.100.101.95:5000`
- **数据返回格式**: JSON
- **状态码**:
  - 200: 成功
  - 400: 请求参数错误
  - 401: 未授权
  - 404: 资源不存在
  - 500: 服务器错误

## 用户相关接口

### 1. 注册新用户

- **URL**: `/api/user/register`
- **方法**: POST
- **请求体参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | username | 字符串 | 是 | 用户名 |
  | password | 字符串 | 是 | 密码 |

- **成功响应**:
  ```json
  {
    "code": 200,
    "data": {
      "id": "用户ID",
      "username": "用户名",
      "created_at": "创建时间",
      "is_admin": false,
      "affiliate_id": "分销ID"
    }
  }
  ```

- **错误响应**:
  ```json
  {
    "code": 400,
    "message": "用户名已存在"
  }
  ```

### 2. 用户登录

- **URL**: `/api/user/login`
- **方法**: POST
- **请求体参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | username | 字符串 | 是 | 用户名 |
  | password | 字符串 | 是 | 密码 |

- **成功响应**:
  ```json
  {
    "code": 200,
    "data": {
      "id": "用户ID",
      "username": "用户名",
      "created_at": "创建时间",
      "is_admin": false,
      "affiliate_id": "分销ID"
    }
  }
  ```

- **错误响应**:
  ```json
  {
    "code": 401,
    "message": "用户名或密码错误"
  }
  ```

### 3. 获取用户信息

- **URL**: `/api/user/info`
- **方法**: GET
- **URL参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | user_id | 字符串 | 是 | 用户ID |

- **成功响应**:
  ```json
  {
    "code": 200,
    "data": {
      "id": "用户ID",
      "username": "用户名",
      "created_at": "创建时间",
      "is_admin": false,
      "affiliate_id": "分销ID"
    }
  }
  ```

- **错误响应**:
  ```json
  {
    "code": 404,
    "message": "用户不存在"
  }
  ```

## 商品相关接口

### 4. 获取商品列表

- **URL**: `/api/products`
- **方法**: GET
- **URL参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | category | 字符串 | 否 | 商品类别 |

- **成功响应**:
  ```json
  {
    "code": 200,
    "data": [
      {
        "id": 1,
        "name": "商品名称",
        "price": 100.0,
        "image": "图片URL",
        "description": "商品描述",
        "stock": 100,
        "category": "商品类别"
      },
      // 更多商品...
    ]
  }
  ```

### 5. 获取商品详情

- **URL**: `/api/products/<product_id>`
- **方法**: GET
- **URL路径参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | product_id | 整数 | 是 | 商品ID |

- **成功响应**:
  ```json
  {
    "code": 200,
    "data": {
      "id": 1,
      "name": "商品名称",
      "price": 100.0,
      "image": "图片URL",
      "description": "商品描述",
      "stock": 100,
      "category": "商品类别"
    }
  }
  ```

- **错误响应**:
  ```json
  {
    "code": 404,
    "message": "商品不存在"
  }
  ```

## 购物车相关接口

### 6. 获取购物车

- **URL**: `/api/cart`
- **方法**: GET
- **URL参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | user_id | 字符串 | 是 | 用户ID |

- **成功响应**:
  ```json
  {
    "code": 200,
    "data": [
      {
        "id": "购物车项ID",
        "product_id": 1,
        "product_name": "商品名称",
        "product_image": "图片URL",
        "price": 100.0,
        "quantity": 1
      },
      // 更多购物车项...
    ]
  }
  ```

### 7. 添加商品到购物车

- **URL**: `/api/cart/add`
- **方法**: POST
- **请求体参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | user_id | 字符串 | 是 | 用户ID |
  | product_id | 整数 | 是 | 商品ID |
  | quantity | 整数 | 否 | 商品数量，默认为1 |

- **成功响应**:
  ```json
  {
    "code": 200,
    "message": "添加成功"
  }
  ```

- **错误响应**:
  ```json
  {
    "code": 404,
    "message": "商品不存在"
  }
  ```

### 8. 更新购物车项

- **URL**: `/api/cart/update`
- **方法**: POST
- **请求体参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | user_id | 字符串 | 是 | 用户ID |
  | cart_item_id | 字符串 | 是 | 购物车项ID |
  | quantity | 整数 | 是 | 新的商品数量 |

- **成功响应**:
  ```json
  {
    "code": 200,
    "message": "更新成功"
  }
  ```

- **错误响应**:
  ```json
  {
    "code": 404,
    "message": "购物车项不存在"
  }
  ```

### 9. 从购物车中移除商品

- **URL**: `/api/cart/remove`
- **方法**: POST
- **请求体参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | user_id | 字符串 | 是 | 用户ID |
  | cart_item_id | 字符串 | 是 | 购物车项ID |

- **成功响应**:
  ```json
  {
    "code": 200,
    "message": "删除成功"
  }
  ```

- **错误响应**:
  ```json
  {
    "code": 404,
    "message": "购物车项不存在"
  }
  ```

## 订单相关接口

### 10. 获取订单列表

- **URL**: `/api/orders`
- **方法**: GET
- **URL参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | user_id | 字符串 | 是 | 用户ID |

- **成功响应**:
  ```json
  {
    "code": 200,
    "data": [
      {
        "id": "订单ID",
        "total_amount": 100.0,
        "address": "收货地址",
        "payment_method": "支付方式",
        "status": "订单状态",
        "created_at": "创建时间",
        "items": [
          {
            "id": "订单项ID",
            "product_id": 1,
            "product_name": "商品名称",
            "product_image": "图片URL",
            "price": 100.0,
            "quantity": 1
          },
          // 更多订单项...
        ]
      },
      // 更多订单...
    ]
  }
  ```

### 11. 获取订单详情

- **URL**: `/api/orders/<order_id>`
- **方法**: GET
- **URL路径参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | order_id | 字符串 | 是 | 订单ID |

- **成功响应**:
  ```json
  {
    "code": 200,
    "data": {
      "id": "订单ID",
      "user_id": "用户ID",
      "total_amount": 100.0,
      "address": "收货地址",
      "payment_method": "支付方式",
      "status": "订单状态",
      "created_at": "创建时间",
      "referrer_id": "推荐人ID",
      "items": [
        {
          "id": "订单项ID",
          "product_id": 1,
          "product_name": "商品名称",
          "product_image": "图片URL",
          "price": 100.0,
          "quantity": 1
        },
        // 更多订单项...
      ]
    }
  }
  ```

- **错误响应**:
  ```json
  {
    "code": 404,
    "message": "订单不存在"
  }
  ```

### 12. 创建订单

- **URL**: `/api/orders/create`
- **方法**: POST
- **请求体参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | user_id | 字符串 | 是 | 用户ID |
  | address | 字符串 | 是 | 收货地址 |
  | payment_method | 字符串 | 是 | 支付方式 |
  | referrer_id | 字符串 | 否 | 推荐人ID（用于分销） |

- **成功响应**:
  ```json
  {
    "code": 200,
    "data": {
      "id": "订单ID",
      "user_id": "用户ID",
      "total_amount": 100.0,
      "address": "收货地址",
      "payment_method": "支付方式",
      "status": "pending",
      "created_at": "创建时间",
      "referrer_id": "推荐人ID",
      "items": [
        {
          "id": "订单项ID",
          "product_id": 1,
          "product_name": "商品名称",
          "product_image": "图片URL",
          "price": 100.0,
          "quantity": 1
        },
        // 更多订单项...
      ]
    }
  }
  ```

- **错误响应**:
  ```json
  {
    "code": 400,
    "message": "购物车为空"
  }
  ```

### 13. 更新订单状态

- **URL**: `/api/orders/<order_id>/status`
- **方法**: POST
- **请求体参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | order_id | 字符串 | 是 | 订单ID |
  | status | 字符串 | 是 | 新的订单状态（pending/paid/shipped/completed/cancelled） |

- **成功响应**:
  ```json
  {
    "code": 200,
    "message": "状态更新成功"
  }
  ```

- **错误响应**:
  ```json
  {
    "code": 400,
    "message": "无效的状态"
  }
  ```
  或
  ```json
  {
    "code": 404,
    "message": "订单不存在"
  }
  ```

## 分销相关接口

### 14. 获取推广链接列表

- **URL**: `/api/affiliate/links`
- **方法**: GET
- **URL参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | user_id | 字符串 | 是 | 用户ID |

- **成功响应**:
  ```json
  {
    "code": 200,
    "data": [
      {
        "id": "链接ID",
        "user_id": "用户ID",
        "link_url": "推广链接URL",
        "created_at": "创建时间",
        "clicks": 0,
        "conversions": 0,
        "product_id": 1,
        "product_name": "商品名称",
        "product_image": "图片URL"
      },
      // 更多推广链接...
    ]
  }
  ```

### 15. 创建推广链接

- **URL**: `/api/affiliate/links/create`
- **方法**: POST
- **请求体参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | user_id | 字符串 | 是 | 用户ID |
  | product_id | 整数 | 否 | 商品ID（如果不提供则创建通用推广链接） |

- **成功响应**:
  ```json
  {
    "code": 200,
    "data": {
      "id": "链接ID",
      "user_id": "用户ID",
      "link_url": "推广链接URL",
      "created_at": "创建时间",
      "clicks": 0,
      "conversions": 0,
      "product_id": 1,
      "product_name": "商品名称",
      "product_image": "图片URL"
    }
  }
  ```

- **错误响应**:
  ```json
  {
    "code": 404,
    "message": "用户不存在"
  }
  ```
  或
  ```json
  {
    "code": 404,
    "message": "商品不存在"
  }
  ```

### 16. 获取分销记录

- **URL**: `/api/affiliate/records`
- **方法**: GET
- **URL参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | user_id | 字符串 | 是 | 用户ID（推荐人ID） |

- **成功响应**:
  ```json
  {
    "code": 200,
    "data": [
      {
        "id": "记录ID",
        "buyer_id": "购买者ID",
        "order_id": "订单ID",
        "total_amount": 100.0,
        "commission": 10.0,
        "status": "pending",
        "created_at": "创建时间"
      },
      // 更多分销记录...
    ]
  }
  ```

### 17. 获取分销统计数据

- **URL**: `/api/affiliate/stats`
- **方法**: GET
- **URL参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | user_id | 字符串 | 是 | 用户ID（推荐人ID） |

- **成功响应**:
  ```json
  {
    "code": 200,
    "data": {
      "total_clicks": 100,
      "total_conversions": 10,
      "conversion_rate": 10.0,
      "total_commission": 1000.0,
      "paid_commission": 500.0,
      "pending_commission": 500.0
    }
  }
  ```

## 数据导出接口

### 18. 导出用户信息

- **URL**: `/api/export/user`
- **方法**: GET
- **URL参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | user_id | 字符串 | 是 | 用户ID |
  | format | 字符串 | 否 | 导出格式（json/csv），默认为json |

- **成功响应**:
  - JSON格式（默认）
    ```json
    {
      "code": 200,
      "data": {
        "id": "用户ID",
        "username": "用户名",
        "created_at": "创建时间",
        "is_admin": false,
        "affiliate_id": "分销ID"
      }
    }
    ```
  - CSV格式（当format=csv时）
    返回CSV文件下载

- **错误响应**:
  ```json
  {
    "code": 404,
    "message": "用户不存在"
  }
  ```
  或
  ```json
  {
    "code": 400,
    "message": "不支持的格式"
  }
  ```

### 19. 导出用户订单

- **URL**: `/api/export/orders`
- **方法**: GET
- **URL参数**:
  | 参数名 | 类型 | 必填 | 描述 |
  |-------|------|------|------|
  | user_id | 字符串 | 是 | 用户ID |
  | format | 字符串 | 否 | 导出格式（json/csv），默认为json |

- **成功响应**:
  - JSON格式（默认）
    ```json
    {
      "code": 200,
      "data": [
        {
          "id": "订单ID",
          "total_amount": 100.0,
          "status": "订单状态",
          "created_at": "创建时间",
          "items": [
            {
              "product_name": "商品名称",
              "price": 100.0,
              "quantity": 1
            },
            // 更多订单项...
          ]
        },
        // 更多订单...
      ]
    }
    ```
  - CSV格式（当format=csv时）
    返回CSV文件下载，内容为order_id,total_amount,status,created_at格式的订单数据

- **错误响应**:
  ```json
  {
    "code": 400,
    "message": "不支持的格式"
  }
  ```

## 测试数据

### 测试账户

- 普通用户: username=`test`, password=`test123`
- 管理员: username=`admin`, password=`admin123`

### 测试商品

系统已预载以下测试商品：

1. iPhone 13 Pro - ¥7999
2. MacBook Pro 14 - ¥14999
3. Nike Air Max - ¥999
4. Adidas卫衣 - ¥599
5. 索尼WH-1000XM4 - ¥2399 