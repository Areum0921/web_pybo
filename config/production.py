# 서버 환경
from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\xe5\x0e\xa0X\xf9\x18\xb6T\xf2\x96\xc7\xf9\x8aX#\xc6'