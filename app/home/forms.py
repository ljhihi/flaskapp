#coding:utf8
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField,StringField,PasswordField,FileField,TextAreaField
from wtforms.validators import DataRequired,EqualTo,ValidationError
from app.models import User,Yqm

class RegistForm(FlaskForm):
    name = StringField(
        label="名称",
        validators=[
            DataRequired('请输入名称!')
        ],
        description='名称',
        render_kw={
            'class':"form-control input-lg" ,
            'placeholder':"请输入名称!",
        }
    )
    yqm = StringField(
        label="邀请码",
        validators=[
            DataRequired('请输入邀请码!')
        ],
        description='邀请码',
        render_kw={
            'class':"form-control input-lg" ,
            'placeholder':"请输入邀请码!",
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired('请输入邮箱!')
        ],
        description='邮箱',
        render_kw={
            'class':"form-control input-lg" ,
            'placeholder':"请输入邮箱!",
        }
    )
    phone = StringField(
        label="手机",
        validators=[
            DataRequired('请输入手机!')
        ],
        description='手机',
        render_kw={
            'class':"form-control input-lg" ,
            'placeholder':"请输入手机!",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired('请输入密码!')
        ],
        description='密码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入密码!",
            'required': 'required'
        }
    )
    repwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired('请输入确认密码!'),
            EqualTo('pwd','两次密码不一致')
        ],
        description='密码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入确认密码!",
            'required': 'required'
        }
    )
    submit = SubmitField(
        '注册',
        render_kw={
            'class':'btn btn-lg btn-success btn-block'
        }
    )


    def validate_name(self,field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user ==1:
            raise ValidationError('名称已经存在')

    def validate_email(self,field):
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user ==1:
            raise ValidationError('邮箱已经存在')

    def validate_phone(self,field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user ==1:
            raise ValidationError('手机已经存在')

class LoginForm(FlaskForm):

    name = StringField(
        label="帐号",
        validators=[
            DataRequired('请输入帐号!')
        ],
        description='名称',
        render_kw={
            'class':"form-control input-lg" ,
            'placeholder':"请输入帐号!",
        }
    )

    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired('请输入密码!')
        ],
        description='密码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入密码!",
            'required': 'required'
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            'class':'btn btn-lg btn-primary btn-block'
        }
    )

class UserdetailForm(FlaskForm):
    name = StringField(
        label="帐号",
        validators=[
            DataRequired('请输入帐号!')
        ],
        description='名称',
        render_kw={
            'class':"form-control",
            'placeholder':"请输入帐号!",
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired('请输入邮箱!')
        ],
        description='邮箱',
        render_kw={
            'class':"form-control",
            'placeholder':"请输入邮箱!",
        }
    )
    phone = StringField(
        label="手机",
        validators=[
            DataRequired('请输入手机!')
        ],
        description='手机',
        render_kw={
            'class':"form-control",
            'placeholder':"请输入手机!",
        }
    )
    submit = SubmitField(
        '保存',
        render_kw={
            'class':'btn btn-success'
        }
    )

class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label = "旧密码",
        validators = [
            DataRequired("请输入旧密码"),
            ],
            description = "旧密码",
            render_kw = {
                "class":"form-control",
                "placeholder":"请输入旧密码",
            }
    )
    new_pwd = PasswordField(
        label = "新密码",
        validators = [
            DataRequired("请输入新密码"),
            ],
            description = "新密码",
            render_kw = {
                "class":"form-control",
                "placeholder":"请输入新密码",
            }
    )
    submit = SubmitField(
        '保存',
        render_kw={
            'class':'btn btn-primary'
        }
    )

class CommentForm(FlaskForm):
    content = TextAreaField(
        label = "内容",
        validators=[
            DataRequired("请输入内容"),
            ],
        description="内容",
        render_kw={
            "id":"input_content"
            }
        )

    submit = SubmitField(
        '提交评论',
        render_kw={
            "class":"btn btn-success", "id":"btn-sub"
        }
    )


















