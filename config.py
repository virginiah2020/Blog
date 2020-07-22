import os

class Config:


    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:access@localhost/blog'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    QUOTES_URL = 'http://quotes.stormconsultancy.co.uk/random.json'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    # SQLALCHEMY_TRACK_MODIFICATIONS = True

    


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")



class DevConfig(Config):
 

    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,

}
