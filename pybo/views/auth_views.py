from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User
import functools

bp = Blueprint('auth',__name__, url_prefix='/auth')


@bp.route('/signup/',methods=('GET','POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        if not user and not email:
            user = User(username=form.username.data, password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            if(email):
                flash('이미 존재하는 메일 입니다.')
            elif(user):
                flash('이미 존재하는 사용자 입니다.')
            else:
                flash('이미 존재하는 사용자, 메일 입니다.')
    return render_template('auth/signup.html',form=form)



@bp.route('/login/', methods=('GET','POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first() # 폼으로 사용자 이름 입력받기
        if not user: # 존재하지 않는 사용자 이름일때
            error ="존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data): # 패스워드가 틀릴때
            error ="비밀번호가 올바르지 않습니다."
        if error is None: # 사용자 이름 있고, 패스워드 맞을때
            session.clear()
            session['user_id'] = user.id # 세션에 키('user_id')와 키값(user.id) 저장
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html',form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view







