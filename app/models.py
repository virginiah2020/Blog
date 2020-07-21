from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(240))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure=db.Column(db.String(240))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    blogs=db.relationship('Blog',backref = 'user',lazy = "dynamic")
    comments=db.relationship('Comment',backref = 'user',lazy = "dynamic")



    @property
    def password(self):
        raise AttributeError('You cannot see password')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)


    def __repr__(self):
        return f'User {self.username}'




class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")



    def __repr__(self):
        return f'User {self.name}'




class Blog(db.Model):
    __tablename__='blogs'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200))
    blog = db.Column(db.String(100000))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    # comments=db.relationship('Comment',backref = 'blog_id',lazy = "dynamic")




    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blogs(cls,id):

        blogs = Blog.query.order_by(Blog.posted.desc())
        # blogs= Blog.query.all()
        return blogs

    @classmethod
    def get_blog(cls,id):
        blog = Blog.query.filter_by(id = id).first()

        return blog



class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(200))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    # blog_id = db.Column(db.Integer,db.ForeignKey("blogs.id"))


    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments= Comment.query.all()
        return comments

    
