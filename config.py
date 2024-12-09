import os

LOCAL_DB_CONFIG = {
    'host': 'localhost',
    'database': 'it_helpdesk',
    'user': 'postgres',
    'password': '1234'
}
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"postgresql://{LOCAL_DB_CONFIG['user']}:{LOCAL_DB_CONFIG['password']}@{LOCAL_DB_CONFIG['host']}/{LOCAL_DB_CONFIG['database']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False