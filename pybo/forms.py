from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('반드시 제목을 입력해주세요'), Length(min=1, max=30)])
    content = TextAreaField('내용', validators=[DataRequired('반드시 내용을 입력해주세요')])

class QuestionForm2(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('반드시 제목을 입력해주세요'), Length(min=1, max=30)])
    content = TextAreaField('내용', validators=[DataRequired('반드시 내용을 입력해주세요')])
    password = PasswordField('비밀번호', validators=[DataRequired('비회원 작성 글을 삭제 및 수정할때 필요합니다.(4글자~20글자)'), Length(min=4,max=20)])

class CheckPassword(FlaskForm):
    password_check = PasswordField('비밀번호 확인',validators=[DataRequired('삭제 및 수정을 위해 질문글의 비밀번호가 필요합니다.')])

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('반드시 내용을 입력해주세요')])

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(),Length(min=3, max=25)])
    password = PasswordField('비밀번호',validators=[DataRequired()])

class CommentForm(FlaskForm):
    content = TextAreaField('댓글 내용',validators=[DataRequired()])


    