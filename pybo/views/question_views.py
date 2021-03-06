from datetime import datetime

from sqlalchemy import func

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from .. import db
from .. models import Question, Answer, User, question_voter, Category

from ..forms import QuestionForm,AnswerForm,QuestionForm2,CheckPassword
from pybo.views.auth_views import login_required
bp = Blueprint('question',__name__, url_prefix='/question')
# url_prefix 는 함수의 애너테이션 URL 앞에 기본값으로 붙일 접두어다.
# url_prefix='/home' 으로 입력했으면,
# 아래 hello_pybo 함수를 호출하는 URL 은 localhost:5000/home/이 된다.

@bp.route('/list/<string:category_name>/')
def _list(category_name):
    category=Category.query.get_or_404(category_name)
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw',type=str, default='')
    so = request.args.get('so', type=str, default='recent')
    # 정렬

    if so == 'recommend':
        sub_query = db.session.query(question_voter.c.question_id, func.count('*').label('num_voter')) \
            .group_by(question_voter.c.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_voter.desc(), Question.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(Answer.question_id, func.count('*').label('num_answer')) \
            .group_by(Answer.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_answer.desc(), Question.create_date.desc())
    elif so == 'old':
        question_list = Question.query.order_by(Question.create_date)

    else:
        question_list = Question.query.order_by(Question.create_date.desc())

    question_list = question_list \
            .filter(category.name == Question.category_name) \
            .distinct()
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, User.username) \
            .outerjoin(User, Answer.user_id == User.id).subquery()  # 답변자에 대한 user정보 저장 쿼리
        question_list = question_list \
            .outerjoin(Answer) \
            .outerjoin(sub_query) \
            .outerjoin(User, User.id == Question.user_id) \
            .filter(Question.subject.ilike(search) |  # 질문 제목
                    Question.content.ilike(search) |  # 질문 내용
                    User.username.ilike(search) |  # 질문 or 답변 작성자
                    Answer.ip.ilike(search) |  # 비로그인상태의 답변 작성자
                    Question.ip.ilike(search) |  # 비로그인상태의 질문 작성자
                    Answer.content.ilike(search) |  # 답변 내용
                    sub_query.c.username.ilike(search)
                    ) \
            .distinct()
        """
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .outerjoin(Answer) \
            .outerjoin(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    Answer.ip.ilike(search) |  # 비로그인상태의 답변 작성자
                    Question.ip.ilike(search) |  # 비로그인상태의 질문 작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()
        """
    question_list = question_list.paginate(page, per_page=10)
    # 최근 작성일자부터 출력
    return render_template('question/question_list.html',question_list=question_list,page=page, kw=kw, so=so,
                           category=category)

@bp.route('/myquestion/')
@login_required
def myquestion():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')

    # 정렬
    if so == 'recommend':
        sub_query = db.session.query(question_voter.c.question_id, func.count('*').label('num_voter')) \
            .group_by(question_voter.c.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_voter.desc(), Question.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(Answer.question_id, func.count('*').label('num_answer')) \
            .group_by(Answer.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_answer.desc(), Question.create_date.desc())
    elif so == 'old':
        question_list = Question.query.order_by(Question.create_date)

    else:
        question_list = Question.query.order_by(Question.create_date.desc())
    #question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list \
            .filter(Question.user == g.user) \
            .distinct()
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, User.username) \
            .outerjoin(User, Answer.user_id == User.id).subquery()  # 답변자에 대한 user정보 저장 쿼리
        question_list = question_list \
            .outerjoin(Answer) \
            .outerjoin(sub_query) \
            .outerjoin(User, User.id == Question.user_id) \
            .filter(Question.subject.ilike(search) |  # 질문 제목
                    Question.content.ilike(search) |  # 질문 내용
                    User.username.ilike(search) |  # 질문 or 답변 작성자
                    Answer.ip.ilike(search) |  # 비로그인상태의 답변 작성자
                    Question.ip.ilike(search) |  # 비로그인상태의 질문 작성자
                    Answer.content.ilike(search) |  # 답변 내용
                    sub_query.c.username.ilike(search)
                    ) \
            .distinct()

    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/myquestion_list.html', question_list=question_list,page=page,kw=kw,so=so)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id) #현재 질문의 id를 받아온다.
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/create/<string:category_name>/',methods=('GET','POST'))
def create(category_name):
    category = Category.query.get_or_404(category_name)

    if g.user: # 로그인 상태에따라 적용하는 form 나누기
        form = QuestionForm()
    else:
        form = QuestionForm2()
    if request.method == 'POST' and form.validate_on_submit():
        get_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        if g.user:
            question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(),
                          user=g.user, category_name=category.name)
        elif not g.user:
            question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(),
                                ip=get_ip, password=form.password.data, category_name=category.name)

        db.session.add(question)
        db.session.commit()
        return redirect(url_for('question._list',category_name=category_name))
    return render_template('question/question_form.html', form=form, category=category)


@bp.route('/modify/<int:question_id>', methods=('GET','POST'))
#@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)

    if question.user: # 회원 작성글
        if g.user != question.user and g.user.roles!=1:
            flash('수정권한이 없습니다.')
            return redirect(url_for('question.detail', question_id=question_id))
        if request.method == 'POST': # 내용 쓴 후 저장하기 버튼
            form = QuestionForm()
            if form.validate_on_submit():
                form.populate_obj(question)
                question.modify_date = datetime.now()
                db.session.commit()
                return redirect(url_for('question.detail', question_id=question_id))
        else:
            form = QuestionForm(obj=question)

        return render_template('question/question_form.html', form=form)

    elif not question.user: # 비회원 작성글

        form = QuestionForm2(obj=question)

        if request.method == 'POST' and 'submit' in request.form: # 수정 후 저장하기 버튼 누를때
            form = QuestionForm2()
            if form.validate_on_submit():
                form.populate_obj(question)
                question.modify_date = datetime.now()
                db.session.commit()
                return redirect(url_for('question.detail', question_id=question_id))

        elif request.method == 'POST' and 'modify' in request.form : # 비밀번호 확인 버튼
            form = CheckPassword()
            password = form.password_check.data
            if password == question.password:
                form = QuestionForm2(obj=question)
            elif password != question.password:
                flash('비밀번호 틀림')
                return render_template('question/no_login_password.html', form=form)
            #return render_template('question/question_modify_form.html', form=form)

        elif request.method=='GET': # 수정 버튼
            if not g.user or g.user.roles==0:
                form = CheckPassword()
                return render_template('question/no_login_password.html', form=form)
            elif g.user.roles==1:
                form = QuestionForm2(obj=question)

        return render_template('question/question_modify_form.html', form=form)

"""
    if g.user != question.user:
        flash('수정권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
        else:
            form = QuestionForm(obj=question)
"""






@bp.route('/delete/<int:question_id>/',methods=('GET','POST'))
#@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)

    if g.user and question.user:
        if g.user != question.user:
            flash('삭제권한이 없습니다.')
            return redirect(url_for('question.detail', question_id=question_id))
        elif g.user.roles==1:
            db.session.delete(question)
            db.session.commit()
            return redirect(url_for('question._list', category_name=question.category_name))

    if not question.user: # 해당 질문글이 비회원 상태에서 써졌을경우
        if not g.user or g.user.roles==0:
            form = CheckPassword()
            if(request.method == 'POST' and form.validate_on_submit()):
                password = form.password_check.data # form으로 비밀번호 입력 받기

                if(password != question.password):
                    flash('해당 질문글의 비밀번호와 다릅니다.')
                    return render_template('question/no_login_password.html', form=form)
                    #return redirect(url_for('question.detail', question_id=question_id))
                else:
                    db.session.delete(question)
                    db.session.commit()
                    return redirect(url_for('question._list',category_name=question.category_name))

            return render_template('question/no_login_password.html', form=form)


    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list',category_name=question.category_name))








