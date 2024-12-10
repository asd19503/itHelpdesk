from app import create_app
from app.init_root import create_root_user

app = create_app()

if __name__ == '__main__':
    create_root_user(app)
    app.run(debug=True)
