#coding:utf8
from . import home
from flask import render_template,redirect,url_for,flash,session,request
from app.home.forms import RegistForm,LoginForm,UserdetailForm,PwdForm
from app.models import User,Userlog,Preview,Tag,Movie
from werkzeug.security import generate_password_hash
import uuid
from functools import wraps
from app import db

def user_login_req(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if 'user' not in session.keys():
            return redirect(url_for('home.login',next=request.url))
        return f(*args,**kwargs)
    return decorated_function


@home.route("/login/",methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['name']).first()
        if  user:
            if not user.check_pwd(data['pwd']):
                flash('密码错误')
                return redirect(url_for('home.login'))
            session['user'] = user.name
            session['user_id'] = user.id
            userlog = Userlog(
                user_id = user.id,
                ip = request.remote_addr
            )
            db.session.add(userlog)
            db.session.commit()
            return redirect(url_for('home.user'))
        else:
            flash('none user')
    return render_template("home/login.html",form=form)

@home.route("/logout/")
def logout():
    session.pop('user',None)
    session.pop('user_id',None)
    return redirect(url_for('home.login'))

@home.route("/register/",methods=['GET','POST'])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name = data['name'],
            email = data['email'],
            phone = data['phone'],
            pwd = generate_password_hash(data['pwd']),
            uuid = uuid.uuid4().hex
            )
        db.session.add(user)
        db.session.commit()
        flash ('ok')
    return render_template("home/register.html",form=form)

@home.route("/user/",methods=['GET','POST'])
@user_login_req
def user():
    form = UserdetailForm()
    user = User.query.get(int(session['user_id']))
    if request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
    if form.validate_on_submit():
        data = form.data
        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        db.session.add(user)
        db.session.commit()
        flash('change finish')
        return redirect(url_for("home.user"))
    return render_template("home/user.html",form=form)

@home.route("/pwd/",methods=['GET','POST'])
@user_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=session['user']).first()
        if not user.check_pwd(data['old_pwd']):
            flash("密码错误")
            return redirect(url_for('home.pwd'))
        user.pwd = generate_password_hash(data['new_pwd'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home.logout'))
    return render_template("home/pwd.html",form=form)

@home.route("/comments/")
@user_login_req
def comments():
    return render_template("home/comments.html")

@home.route("/loginlog/<int:page>",methods=["GET"])
@user_login_req
def loginlog(page=None):
    if page is None:
        page = 1
    page_data = Userlog.query.filter_by(user_id=int(session['user_id'])).order_by(Userlog.addtime.desc()).paginate(page=page,per_page=10)
    return render_template("home/loginlog.html",page_data=page_data)

@home.route("/moviecol/")
@user_login_req
def moviecol():
    return render_template("home/moviecol.html")

@home.route("/<int:page>",methods=["GET"])
def index(page=None):
    tags = Tag.query.all()
    page_data = Movie.query
    tid = request.args.get('tid',0)
    if int(tid) != 0:
        page_data = page_data.filter_by(tag_id=int(tid))

    star = request.args.get('star',0)
    if int(star) != 0:
        page_data = page_data.filter_by(star=int(star))

    time = request.args.get('time',0)
    if int(time) !=0:
        if int(time) ==1:
            page_data = page_data.order_by(Movie.addtime.desc())
        else:
            page_data = page_data.order_by(Movie.addtime.asc())

    pm = request.args.get('pm',0)
    if int(pm) !=0:
        if int(pm) ==1:
            page_data = page_data.order_by(Movie.playnum.desc())
        else:
            page_data = page_data.order_by(Movie.playnum.asc())

    cm = request.args.get('cm',0)
    if int(cm) !=0:
        if int(cm) ==1:
            page_data = page_data.order_by(Movie.commentnum.desc())
        else:
            page_data = page_data.order_by(Movie.commentnum.asc())
    if page is None:
        page =1
    page_data = page_data.paginate(page=page,per_page=10)

    p = dict(tid=tid,star=star,time=time,pm=pm,cm=cm)

    return render_template("home/index.html",tags=tags,p=p,page_data=page_data)

@home.route("/animation")
def animation():
    data = Preview.query.all()
    return render_template("home/animation.html",data=data)

@home.route("/search/<int:page>/")
def search(page=None):
    if page is None:
        page =1
    key = request.args.get("key","")
    page_data = Movie.query.filter(Movie.title.ilike('%'+key+'%')).order_by(Movie.addtime.desc()).paginate(page=page,per_page=10)
    movie_count = Movie.query.filter(Movie.title.ilike('%'+key+'%')).count()

    return render_template("home/search.html",key=key,page_data=page_data,movie_count=movie_count)

@home.route("/play/<int:id>/",methods=['GET','POST'])
def play(id=None):
    movie = Movie.query.join(Tag).filter(Tag.id==Movie.tag_id,Movie.id==int(id)).first_or_404()
    return render_template("home/play.html",movie=movie)
















