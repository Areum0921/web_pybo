from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flaskext.markdown import Markdown

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
UPLOAD_FOLDER = "static/uploads/"

def page_not_found(e): # 404 오류일때 띄울 화면
    return render_template('404.html'), 404

def create_app():
    app = Flask(__name__)  # 플라스크 애플리케이션을 생성하는 코드


    app.config.from_envvar('APP_CONFIG_FILE')
    # 환경 변수 APP_CONFIG_FILE에 정의된 파일을 환경 파일로 사용
    app.secret_key= "secret key"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


    # ORM
    db.init_app(app) # 초기화
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db) # 초기화
    from . import models # 플라스크의 Migrate 기능이 인식할 수 있도록

    # 블루 프린트
    from.views import  main_views, question_views, answer_views, auth_views, comment_views, vote_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(vote_views.bp)


    from .filter import format_datetime, format_ip
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['ip'] = format_ip

#마크다운
    Markdown(app, extensions=['nl2br','fenced_code'])
    #오류페이지
    app.register_error_handler(404, page_not_found)
    return app









