import datetime

# Secret key for hashing
SECRET_KEY = 'AT@u@5HgZ/g0zK)a<-1l1[%xihmk-|'
TESTING = True
# database setting
SQLALCHEMY_DATABASE_URI = 'sqlite://'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=365)
JWT_TOKEN_LOCATION = ['cookies']
JWT_SESSION_COOKIE = False
JWT_COOKIE_CSRF_PROTECT = False
ALLOW_ORIGIN = 'http://localhost:8000'
