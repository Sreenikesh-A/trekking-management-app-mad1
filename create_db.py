from flask import Flask
from config import Config
from models import db,User
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
with app.app_context():
    db.create_all()
    admin = User.query.filter_by(mail="admin@gmail.com").first()
    if admin is None:
        admin = User(name="sreenikesh",mail="sree@gmail.com",password="admin123",role="Admin",status="Approved")
        db.session.add(admin)
        db.session.commit()
        print("Admin account created successfully!")
    print("Database Created Successfully!")