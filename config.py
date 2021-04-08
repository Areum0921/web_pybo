import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
# 데이터베이스 접속 주소
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLAlchemy의 이벤트 처리옵션, 파이보에 필요하지않아 False 로 설정

SECRET_KEY="dev"




