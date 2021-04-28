# 개발 환경
from config.default import *
# 라인2 코드로 BASE_DIR 환경 변수 값 사용 가능.
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY="dev"