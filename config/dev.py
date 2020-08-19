import datetime

# Secret key for hashing
SECRET_KEY = 'AT@u@5HgZ/g0zK)a<-1l1[%xihmk-|'
# database setting
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://linuxjobber:8iu7*IU&@localhost/adayahouse?charset=utf8mb4'
# heroku db
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://b5bd39bb94a0b0:7ff81330@eu-cdbr-west-02.cleardb.net/heroku_92f04b025bf199c?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE=60
JWT_COOKIE_DOMAIN = '127.0.0.1 localhost dev.localhost'
JWT_HEADER_TYPE = None
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=365)
JWT_TOKEN_LOCATION = ['cookies']
JWT_SESSION_COOKIE = False
JWT_COOKIE_CSRF_PROTECT = False
ALLOW_ORIGIN = ['http://localhost:8010', 'http://localhost:8000' ]#'https://adayahouse.netlify.app' 
# ALLOW_ORIGIN = ['https://adaya.netlify.app', 'https://adayahouse.netlify.app']
MAIL_SERVER='smtp-relay.sendinblue.com'
MAIL_USERNAME='adayahouseshop@gmail.com'
MAIL_PASSWORD='gzryVUPZHa1GW7n6'
MAIL_PORT=587
MAIL_USE_TLS=False
ENV= 'development'
# print("ehllo")
