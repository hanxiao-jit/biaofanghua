from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # 启用跨域支持

# 配置MySQL数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@47.100.101.95:3306/biaofanghua_user_h5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定义数据库模型
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_admin = db.Column(db.Boolean, default=False)
    affiliate_id = db.Column(db.String(8), unique=True)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50))

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product', backref='cart_items')

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(255))
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')  # pending, paid, shipped, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.now)
    referrer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    # 关系
    user = db.relationship('User', foreign_keys=[user_id], backref='orders')
    referrer = db.relationship('User', foreign_keys=[referrer_id], backref='referred_orders')
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.String(36), primary_key=True)
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(100))
    product_image = db.Column(db.String(255))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    
    # 关系
    product = db.relationship('Product')

class AffiliateLink(db.Model):
    __tablename__ = 'affiliate_links'
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    link_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)
    clicks = db.Column(db.Integer, default=0)
    conversions = db.Column(db.Integer, default=0)
    
    # 关系
    user = db.relationship('User', backref='affiliate_links')
    product = db.relationship('Product')

class AffiliateRecord(db.Model):
    __tablename__ = 'affiliate_records'
    id = db.Column(db.String(36), primary_key=True)
    referrer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    buyer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    total_amount = db.Column(db.Float)
    commission = db.Column(db.Float)
    status = db.Column(db.String(20), default='pending')  # pending, paid
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # 关系
    referrer = db.relationship('User', foreign_keys=[referrer_id], backref='affiliate_records_as_referrer')
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref='affiliate_records_as_buyer')
    order = db.relationship('Order', backref='affiliate_record')

# 工具函数
def generate_id():
    return str(uuid.uuid4())

# ==================== 用户相关接口 ====================
@app.route('/api/user/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # 检查用户是否已存在
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'code': 400, 'message': '用户名已存在'}), 400
    
    # 创建新用户
    user_id = generate_id()
    new_user = User(
        id=user_id,
        username=username,
        password=password,  # 实际应用中应当加密
        created_at=datetime.now(),
        is_admin=False,
        affiliate_id=user_id[:8]  # 用于分销的简短ID
    )
    db.session.add(new_user)
    db.session.commit()
    
    # 返回信息（不含密码）
    return jsonify({
        'code': 200, 
        'data': {
            'id': new_user.id,
            'username': new_user.username,
            'created_at': new_user.created_at.isoformat(),
            'is_admin': new_user.is_admin,
            'affiliate_id': new_user.affiliate_id
        }
    })

@app.route('/api/user/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # 验证用户
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({
            'code': 200, 
            'data': {
                'id': user.id,
                'username': user.username,
                'created_at': user.created_at.isoformat(),
                'is_admin': user.is_admin,
                'affiliate_id': user.affiliate_id
            }
        })
    
    return jsonify({'code': 401, 'message': '用户名或密码错误'}), 401

@app.route('/api/user/info', methods=['GET'])
def get_user_info():
    user_id = request.args.get('user_id')
    
    # 查找用户
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'code': 200, 
            'data': {
                'id': user.id,
                'username': user.username,
                'created_at': user.created_at.isoformat(),
                'is_admin': user.is_admin,
                'affiliate_id': user.affiliate_id
            }
        })
    
    return jsonify({'code': 404, 'message': '用户不存在'}), 404

# ==================== 商品相关接口 ====================
@app.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    
    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    
    products_data = [{
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'image': product.image,
        'description': product.description,
        'stock': product.stock,
        'category': product.category
    } for product in products]
    
    return jsonify({'code': 200, 'data': products_data})

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            'code': 200, 
            'data': {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image': product.image,
                'description': product.description,
                'stock': product.stock,
                'category': product.category
            }
        })
    
    return jsonify({'code': 404, 'message': '商品不存在'}), 404

# ==================== 购物车相关接口 ====================
@app.route('/api/cart', methods=['GET'])
def get_cart():
    user_id = request.args.get('user_id')
    
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    cart_data = []
    
    for item in cart_items:
        product = item.product
        cart_data.append({
            'id': item.id,
            'product_id': product.id,
            'product_name': product.name,
            'product_image': product.image,
            'price': product.price,
            'quantity': item.quantity
        })
    
    return jsonify({'code': 200, 'data': cart_data})

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    # 查找商品
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'code': 404, 'message': '商品不存在'}), 404
    
    # 检查购物车中是否已存在该商品
    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        # 添加新商品到购物车
        cart_item = CartItem(
            id=generate_id(),
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '添加成功'})

@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    data = request.json
    user_id = data.get('user_id')
    cart_item_id = data.get('cart_item_id')
    quantity = data.get('quantity')
    
    cart_item = CartItem.query.filter_by(id=cart_item_id, user_id=user_id).first()
    if not cart_item:
        return jsonify({'code': 404, 'message': '购物车项不存在'}), 404
    
    cart_item.quantity = quantity
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '更新成功'})

@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    data = request.json
    user_id = data.get('user_id')
    cart_item_id = data.get('cart_item_id')
    
    cart_item = CartItem.query.filter_by(id=cart_item_id, user_id=user_id).first()
    if not cart_item:
        return jsonify({'code': 404, 'message': '购物车项不存在'}), 404
    
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '删除成功'})

# ==================== 订单相关接口 ====================
@app.route('/api/orders', methods=['GET'])
def get_orders():
    user_id = request.args.get('user_id')
    
    orders = Order.query.filter_by(user_id=user_id).all()
    orders_data = []
    
    for order in orders:
        items_data = []
        for item in order.items:
            items_data.append({
                'id': item.id,
                'product_id': item.product_id,
                'product_name': item.product_name,
                'product_image': item.product_image,
                'price': item.price,
                'quantity': item.quantity
            })
        
        orders_data.append({
            'id': order.id,
            'total_amount': order.total_amount,
            'address': order.address,
            'payment_method': order.payment_method,
            'status': order.status,
            'created_at': order.created_at.isoformat(),
            'items': items_data
        })
    
    return jsonify({'code': 200, 'data': orders_data})

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'code': 404, 'message': '订单不存在'}), 404
    
    items_data = []
    for item in order.items:
        items_data.append({
            'id': item.id,
            'product_id': item.product_id,
            'product_name': item.product_name,
            'product_image': item.product_image,
            'price': item.price,
            'quantity': item.quantity
        })
    
    order_data = {
        'id': order.id,
        'user_id': order.user_id,
        'total_amount': order.total_amount,
        'address': order.address,
        'payment_method': order.payment_method,
        'status': order.status,
        'created_at': order.created_at.isoformat(),
        'referrer_id': order.referrer_id,
        'items': items_data
    }
    
    return jsonify({'code': 200, 'data': order_data})

@app.route('/api/orders/create', methods=['POST'])
def create_order():
    data = request.json
    user_id = data.get('user_id')
    address = data.get('address')
    payment_method = data.get('payment_method')
    referrer_id = data.get('referrer_id')  # 推荐人ID，用于分销
    
    # 获取用户购物车
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({'code': 400, 'message': '购物车为空'}), 400
    
    # 计算订单总价
    total_amount = 0
    for item in cart_items:
        total_amount += item.product.price * item.quantity
    
    # 创建订单
    order_id = generate_id()
    new_order = Order(
        id=order_id,
        user_id=user_id,
        total_amount=total_amount,
        address=address,
        payment_method=payment_method,
        status='pending',
        created_at=datetime.now(),
        referrer_id=referrer_id
    )
    db.session.add(new_order)
    
    # 创建订单项
    for cart_item in cart_items:
        product = cart_item.product
        order_item = OrderItem(
            id=generate_id(),
            order_id=order_id,
            product_id=product.id,
            product_name=product.name,
            product_image=product.image,
            price=product.price,
            quantity=cart_item.quantity
        )
        db.session.add(order_item)
    
    # 清空购物车
    for cart_item in cart_items:
        db.session.delete(cart_item)
    
    # 如果有推荐人，创建分销记录
    if referrer_id:
        commission = total_amount * 0.1  # 假设10%的佣金
        affiliate_record = AffiliateRecord(
            id=generate_id(),
            referrer_id=referrer_id,
            buyer_id=user_id,
            order_id=order_id,
            total_amount=total_amount,
            commission=commission,
            status='pending',
            created_at=datetime.now()
        )
        db.session.add(affiliate_record)
        
        # 更新推广链接的转化数
        affiliate_links = AffiliateLink.query.filter_by(user_id=referrer_id).all()
        for link in affiliate_links:
            link.conversions += 1
    
    db.session.commit()
    
    # 返回订单信息
    return get_order(order_id)

@app.route('/api/orders/<order_id>/status', methods=['POST'])
def update_order_status():
    data = request.json
    order_id = data.get('order_id')
    new_status = data.get('status')
    
    valid_statuses = ['pending', 'paid', 'shipped', 'completed', 'cancelled']
    if new_status not in valid_statuses:
        return jsonify({'code': 400, 'message': '无效的状态'}), 400
    
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'code': 404, 'message': '订单不存在'}), 404
    
    order.status = new_status
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '状态更新成功'})

# ==================== 分销相关接口 ====================
@app.route('/api/affiliate/links', methods=['GET'])
def get_affiliate_links():
    user_id = request.args.get('user_id')
    
    links = AffiliateLink.query.filter_by(user_id=user_id).all()
    links_data = []
    
    for link in links:
        link_data = {
            'id': link.id,
            'user_id': link.user_id,
            'link_url': link.link_url,
            'created_at': link.created_at.isoformat(),
            'clicks': link.clicks,
            'conversions': link.conversions
        }
        
        if link.product:
            link_data.update({
                'product_id': link.product.id,
                'product_name': link.product.name,
                'product_image': link.product.image
            })
        
        links_data.append(link_data)
    
    return jsonify({'code': 200, 'data': links_data})

@app.route('/api/affiliate/links/create', methods=['POST'])
def create_affiliate_link():
    data = request.json
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    
    # 查找用户
    user = User.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404
    
    # 查找产品
    product = None
    if product_id:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'code': 404, 'message': '商品不存在'}), 404
    
    # 创建推广链接
    link_id = generate_id()
    base_url = request.host_url.rstrip('/')
    
    if product_id:
        link_url = f"{base_url}/product/{product_id}?referrer={user.affiliate_id}"
    else:
        link_url = f"{base_url}?referrer={user.affiliate_id}"
    
    affiliate_link = AffiliateLink(
        id=link_id,
        user_id=user_id,
        product_id=product_id,
        link_url=link_url,
        created_at=datetime.now(),
        clicks=0,
        conversions=0
    )
    
    db.session.add(affiliate_link)
    db.session.commit()
    
    # 返回链接信息
    link_data = {
        'id': affiliate_link.id,
        'user_id': affiliate_link.user_id,
        'link_url': affiliate_link.link_url,
        'created_at': affiliate_link.created_at.isoformat(),
        'clicks': affiliate_link.clicks,
        'conversions': affiliate_link.conversions
    }
    
    if product:
        link_data.update({
            'product_id': product.id,
            'product_name': product.name,
            'product_image': product.image
        })
    
    return jsonify({'code': 200, 'data': link_data})

@app.route('/api/affiliate/records', methods=['GET'])
def get_affiliate_records():
    user_id = request.args.get('user_id')
    
    records = AffiliateRecord.query.filter_by(referrer_id=user_id).all()
    records_data = []
    
    for record in records:
        records_data.append({
            'id': record.id,
            'buyer_id': record.buyer_id,
            'order_id': record.order_id,
            'total_amount': record.total_amount,
            'commission': record.commission,
            'status': record.status,
            'created_at': record.created_at.isoformat()
        })
    
    return jsonify({'code': 200, 'data': records_data})

@app.route('/api/affiliate/stats', methods=['GET'])
def get_affiliate_stats():
    user_id = request.args.get('user_id')
    
    # 统计点击量
    links = AffiliateLink.query.filter_by(user_id=user_id).all()
    total_clicks = sum(link.clicks for link in links)
    total_conversions = sum(link.conversions for link in links)
    
    # 统计佣金
    records = AffiliateRecord.query.filter_by(referrer_id=user_id).all()
    total_commission = sum(record.commission for record in records)
    paid_commission = sum(record.commission for record in records if record.status == 'paid')
    pending_commission = total_commission - paid_commission
    
    stats = {
        'total_clicks': total_clicks,
        'total_conversions': total_conversions,
        'conversion_rate': (total_conversions / total_clicks * 100) if total_clicks > 0 else 0,
        'total_commission': total_commission,
        'paid_commission': paid_commission,
        'pending_commission': pending_commission
    }
    
    return jsonify({'code': 200, 'data': stats})

# ==================== 数据导出接口 ====================
@app.route('/api/export/user', methods=['GET'])
def export_user_info():
    user_id = request.args.get('user_id')
    format_type = request.args.get('format', 'json')  # json 或 csv
    
    # 查找用户
    user = User.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404
    
    # 准备导出数据
    user_data = {
        'id': user.id,
        'username': user.username,
        'created_at': user.created_at.isoformat(),
        'is_admin': user.is_admin,
        'affiliate_id': user.affiliate_id
    }
    
    if format_type == 'json':
        return jsonify({'code': 200, 'data': user_data})
    elif format_type == 'csv':
        csv_data = ','.join([f"{k},{v}" for k, v in user_data.items()])
        response = app.response_class(
            response=csv_data,
            status=200,
            mimetype='text/csv'
        )
        response.headers["Content-Disposition"] = f"attachment; filename=user_{user_id}.csv"
        return response
    else:
        return jsonify({'code': 400, 'message': '不支持的格式'}), 400

@app.route('/api/export/orders', methods=['GET'])
def export_user_orders():
    user_id = request.args.get('user_id')
    format_type = request.args.get('format', 'json')  # json 或 csv
    
    # 查找用户的订单
    orders = Order.query.filter_by(user_id=user_id).all()
    orders_data = []
    
    for order in orders:
        items_data = []
        for item in order.items:
            items_data.append({
                'product_name': item.product_name,
                'price': item.price,
                'quantity': item.quantity
            })
        
        orders_data.append({
            'id': order.id,
            'total_amount': order.total_amount,
            'status': order.status,
            'created_at': order.created_at.isoformat(),
            'items': items_data
        })
    
    if format_type == 'json':
        return jsonify({'code': 200, 'data': orders_data})
    elif format_type == 'csv':
        # 简化处理，实际应用中应当更复杂
        csv_header = "order_id,total_amount,status,created_at"
        csv_rows = [f"{order['id']},{order['total_amount']},{order['status']},{order['created_at']}" for order in orders_data]
        csv_data = csv_header + '\n' + '\n'.join(csv_rows)
        
        response = app.response_class(
            response=csv_data,
            status=200,
            mimetype='text/csv'
        )
        response.headers["Content-Disposition"] = f"attachment; filename=orders_{user_id}.csv"
        return response
    else:
        return jsonify({'code': 400, 'message': '不支持的格式'}), 400

# 根目录路由，渲染index.html模板
@app.route('/')
def index():
    return render_template('index.html')

# 创建初始测试数据
def create_test_data():
    # 如果数据库中没有商品，则添加测试商品
    if Product.query.count() == 0:
        test_products = [
            {
                "name": "商品1",
                "price": 100,
                "image": "/static/images/product1.jpg",
                "description": "这是商品1的详细描述",
                "stock": 100,
                "category": "电子产品"
            },
            {
                "name": "商品2",
                "price": 200,
                "image": "/static/images/product2.jpg",
                "description": "这是商品2的详细描述",
                "stock": 50,
                "category": "服装"
            }
        ]
        
        for product_data in test_products:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
    
    # 如果数据库中没有用户，则添加测试用户
    if User.query.count() == 0:
        test_user = User(
            id='test123',
            username='test',
            password='test123',
            created_at=datetime.now(),
            is_admin=False,
            affiliate_id='test1234'
        )
        db.session.add(test_user)
        db.session.commit()

if __name__ == '__main__':
    # 创建数据库表
    with app.app_context():
        db.create_all()
        create_test_data()
    
    app.run(host='0.0.0.0', port=5000,debug=True)
