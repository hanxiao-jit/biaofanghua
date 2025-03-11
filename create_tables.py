from app import app, db

with app.app_context():
    # 创建所有表
    db.create_all()
    print("所有数据表已成功创建！") 