from app.models import User
from app import db
from werkzeug.security import generate_password_hash

def create_root_user(app):
    with app.app_context():
        if not User.query.filter_by(username='root').first():
            root_user = User(
                username='root',
                email='root',
                password_hash=generate_password_hash('123456', method='pbkdf2:sha256'),
                role='admin'
            )
            db.session.add(root_user)
            db.session.commit()
            print("Root user created successfully!")
        else:
            print("Root user already exists.")
