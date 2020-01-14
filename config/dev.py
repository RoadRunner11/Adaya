import datetime

# Secret key for hashing
SECRET_KEY = 'AT@u@5HgZ/g0zK)a<-1l1[%xihmk-|'
# database setting
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:1q2w3e4r@localhost/test?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=365)