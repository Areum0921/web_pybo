# config 파일안에 생성함으로써 깊이가 1늘어나 os.path.dirname를 한번 더 사용하여 설정
# default.py 파일 기준으로 C:/projects/myproject/config/default.py
# os.path.dirname 2번 사용 -> BASE_DIR = C:/projects/myproject
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))