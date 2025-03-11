from app import app, db, User, Product, generate_id
from datetime import datetime

# 初始化测试数据
with app.app_context():
    # 添加测试用户
    if User.query.count() == 0:
        test_user = User(
            id='test123',
            username='test',
            password='test123',
            created_at=datetime.now(),
            is_admin=False,
            affiliate_id='test1234'
        )
        
        admin_user = User(
            id=generate_id(),
            username='admin',
            password='admin123',
            created_at=datetime.now(),
            is_admin=True,
            affiliate_id='admin123'
        )
        
        db.session.add(test_user)
        db.session.add(admin_user)
        db.session.commit()
        print("测试用户已添加")
    
    # 添加测试商品
    if Product.query.count() == 0:
        products = [
            {
                "name": "iPhone 13 Pro",
                "price": 7999,
                "image": "/static/images/product1.jpg",
                "description": "苹果新一代智能手机，搭载A15芯片，性能强劲",
                "stock": 100,
                "category": "电子产品"
            },
            {
                "name": "MacBook Pro 14",
                "price": 14999,
                "image": "/static/images/product2.jpg",
                "description": "M1 Pro芯片，14英寸Retina显示屏，超长续航",
                "stock": 50,
                "category": "电子产品"
            },
            {
                "name": "Nike Air Max",
                "price": 999,
                "image": "/static/images/product3.jpg",
                "description": "耐克经典跑鞋，舒适透气，减震出色",
                "stock": 200,
                "category": "服装"
            },
            {
                "name": "Adidas卫衣",
                "price": 599,
                "image": "/static/images/product4.jpg",
                "description": "阿迪达斯三叶草系列卫衣，时尚保暖",
                "stock": 120,
                "category": "服装"
            },
            {
                "name": "索尼WH-1000XM4",
                "price": 2399,
                "image": "/static/images/product5.jpg",
                "description": "索尼旗舰级降噪耳机，音质出色，降噪效果一流",
                "stock": 80,
                "category": "电子产品"
            }
        ]
        
        for product_data in products:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        print("测试商品已添加")
    
    print("初始化数据完成!") 