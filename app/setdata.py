import json
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://ljhihi:ljhihi198992@ljhihi.mysql.pythonanywhere-services.com/ljhihi$default"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] ='de8437235dff4aef8ce4029f29325bf6'
app.config['UP_DIR'] = "/home/ljhihi/books/app/static/uploads"
app.debug = True
db = SQLAlchemy(app)


from datetime import datetime

# 会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),unique=True)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(11))
    face = db.Column(db.String(255),unique=True)
    addtime = db.Column(db.DateTime,index=True,default=datetime.now)
    uuid = db.Column(db.String(100),unique=True)
    userlogs = db.relationship('Userlog',backref='user')

    def __repr__(self):
        return "<User %r>" % self.name

    def check_pwd(self,pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd,pwd)


# 会员登录
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Userlog %r>" % self.id

# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),unique=True)
    addtime = db.Column(db.DateTime,index=True,default=datetime.now)
    movies = db.relationship("Movie",backref='tag')

    def __repr__(self):
        return "<Tag %r>" % self.name




# 电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),unique=True)
    url = db.Column(db.String(255),unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255),unique=True)
    star = db.Column(db.SmallInteger)
    playnum = db.Column(db.BigInteger)
    commentnum = db.Column(db.BigInteger)
    tag_id = db.Column(db.Integer,db.ForeignKey('tag.id'))
    area = db.Column(db.String(255))
    release_time = db.Column(db.Date)
    length = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    comments = db.relationship('Comment', backref='movie')
    moviecols = db.relationship('Moviecol', backref='movie')

    def __repr__(self):
        return "<Movie %r>" % self.title

#上映预告
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),unique=True)
    logo = db.Column(db.String(255),unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Preview %r>" % self.title

#评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer,db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Comment %r>" % self.id

#电影收藏
class Moviecol(db.Model):
    __tablename__="moviecol"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Moviecol %r>" % self.id

# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True)
    url = db.Column(db.String(255),unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Auth %r>" % self.id


#角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True)
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    admins = db.relationship('Admin', backref='role')
    def __repr__(self):
        return "<Role %r>" % self.id

#管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    adminlogs = db.relationship('Adminlog', backref='admin')
    oplogs = db.relationship('Oplog', backref='admin')

    def __repr__(self):
        return "<Role %r>" % self.id

    def check_pwd(self,pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd,pwd)


#管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer,primary_key=True)
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Adminlog %r>" % self.id

#操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer,primary_key=True)
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Oplog %r>" % self.id

#邀请码
class Yqm(db.Model):
    __tablename__ = "yqm"
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(100))

    def __repr__(self):
        return "<Yqm %r>" % self.id

from random import choice,randrange
n = [ str(x) for x in range(0,10)]
az = [chr(x) for x in range(97,123)]
m = [n,az]

def ow():
    data = [choice(az),choice(az)]
    for i in range(1,randrange(5,10)):
        data.append(choice(choice(m)))
    return "".join(data)

if __name__ == "__main__":
# 添加资源
     f = open("bookdata.json", encoding='utf-8')
     d = json.load(f)
     for i in d['data']:
         print(i)
         movie = Movie(
             title = i['title'],
             logo = i['logo'],
             area = i['area'],
             tag_id = i['tag_id'],
             info = i['info'],
             url = i['url'],
             length = i['length'],
             playnum = i['playnum'],
             commentnum= i['commentnum'],
             star = i['star'],
             )
         db.session.add(movie)
         db.session.commit()


# 添加评论
    # f = open("comments.json", encoding='utf-8')
    # d = json.load(f)
    # for i in d['data']:
    #     for u in i['comments']:
    #         print(u)
    #         comment = Comment(movie_id=i['id'],content=u)
    #         db.session.add(comment)
    #         db.session.commit()
# 添加验证码
    #yqm = Yqm(data="wtmxb")
    #db.session.add(yqm)
    #db.session.commit()

#更新图片
    # movie = Movie.query.all()
    # for i in movie:
    #     # i.logo = 'img'+str(i.id)+'.jpg'
    #     # db.session.add(i)
    #     # db.session.commit()
    #     print(i.title,len(i.title))

#添加标签
    # tag = Tag(name="C++")
    # db.session.add(tag)
    # db.session.commit()













