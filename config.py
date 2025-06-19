# seperate logic from configuration. keeps secrets and settings flask app uses

class Config:
    SECRET_KEY = "your-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'bhattaraisabu@gmail.com'
    MAIL_PASSWORD = 'mphi vppl ysep opbv'
    MAIL_DEFAULT_SENDER = 'bhattaraisabu@gmail.com'
