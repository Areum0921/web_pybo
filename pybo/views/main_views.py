from flask import Blueprint, url_for
from pybo.models import Question
from werkzeug.utils import redirect


bp = Blueprint('main',__name__, url_prefix='/')
# url_prefix 는 함수의 애너테이션 URL 앞에 기본값으로 붙일 접두어다.
# url_prefix='/home' 으로 입력했으면,
# 아래 hello_pybo 함수를 호출하는 URL 은 localhost:5000/home/이 된다.
@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo'

@bp.route('/')
def index():
    question_list = Question.query.order_by(Question.create_date.desc())
    # 최근 작성일자부터 출력
    return redirect(url_for('question._list'))

from flask import request
@bp.route("/ip") # 접속자 ip 받기
def get_ip():
    a=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    return a








