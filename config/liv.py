import datetime
import os

# Secret key for hashing
SECRET_KEY = 'AT@u@5HgZ/g0zK)a<-1l1[%xihmk-|'
# database setting
#SQLALCHEMY_DATABASE_URI = os.environ.get('CLEARDB_DATABASE_URL')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://b5bd39bb94a0b0:7ff81330@eu-cdbr-west-02.cleardb.net/heroku_92f04b025bf199c?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE=60
JWT_COOKIE_DOMAIN = 'adaya.herokuapp.com goofy-pike-03a9ea.netlify.app'
JWT_HEADER_TYPE = None
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=365)
JWT_TOKEN_LOCATION = ['cookies']
JWT_SESSION_COOKIE = False
JWT_COOKIE_CSRF_PROTECT = False
#ALLOW_ORIGIN = 'http://localhost:8010'
ALLOW_ORIGIN = ['http://localhost:8010', 'http://localhost:8000', 'https://adaya.netlify.app', 'https://adayahouse.netlify.app', 'https://goofy-pike-03a9ea.netlify.app' ]#['https://adaya.netlify.app', 'https://adayahouse.netlify.app']
MAIL_SERVER='smtp-relay.sendinblue.com'
MAIL_USERNAME=''
MAIL_PASSWORD=''
MAIL_PORT=587
MAIL_USE_TLS=False
