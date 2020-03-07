import datetime
import os

# Secret key for hashing
SECRET_KEY = 'AT@u@5HgZ/g0zK)a<-1l1[%xihmk-|'
# database setting
SQLALCHEMY_DATABASE_URI = os.environ.get('sql')
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=365)
JWT_TOKEN_LOCATION = ['cookies']
JWT_SESSION_COOKIE = False
JWT_COOKIE_CSRF_PROTECT = False
ALLOW_ORIGIN = 'http://localhost:8000'
MAIL_SERVER='smtp-relay.sendinblue.com'
MAIL_USERNAME='adayahouseshop@gmail.com'
MAIL_PASSWORD='gzryVUPZHa1GW7n6'
MAIL_PORT=587
MAIL_USE_TLS=False
