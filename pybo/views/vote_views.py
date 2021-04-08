from flask import Blueprint, url_for, flash, g
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer
from pybo.views.auth_views import login_required

bp = Blueprint('vote', __name__, url_prefix='/vote')


@bp.route('/question/<int:question_id>/')
#@login_required
def question(question_id):
    _question = Question.query.get_or_404(question_id)
    if g.user!=None:
        if g.user == _question.user:
            flash('본인이 작성한 글은 추천할 수 없습니다')
        elif g.user in _question.voter:
            flash('이미 추천한 글입니다.')
        else:
            _question.voter.append(g.user)
            db.session.commit()
    else:
        flash('추천기능을 이용 하시려면 로그인을 해주세요.')
    return redirect(url_for('question.detail', question_id=question_id))

@bp.route('/answer/<int:answer_id>/')
def answer(answer_id):
    _answer = Answer.query.get_or_404(answer_id)
    if g.user!=None:
        if g.user == _answer.user:
            flash('본인이 작성한 글은 추천할 수 없습니다')
        elif g.user in _answer.voter:
            flash('이미 추천한 글입니다.')
        else:
            _answer.voter.append(g.user)
            db.session.commit()
    else:
        flash('추천기능을 이용 하시려면 로그인을 해주세요.')
    return redirect(url_for('question.detail', question_id=_answer.question.id))



