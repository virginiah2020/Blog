from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from ..models import User,Blog,Comment
from .forms import UpdateProfile,BlogForm,CommentForm,RegistrationForm
from .. import db,photos
from ..email import mail_message



# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    blogs=Blog.get_blogs(id)

    return render_template('index.html',blogs=blogs)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    blog=Blog.query.filter_by(user_id=user.id).all()

    return render_template("profile/profile.html", user = user,blog=blog)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/createblog',methods= ['GET','POST'])
@login_required
def newblog():
    '''
    View root page function that returns the index page and its data
    '''
    form=BlogForm()

    if form.validate_on_submit():
        title = form.title.data
        blog=form.blog.data
        new_blog=Blog(title=title,blog=blog,user=current_user)
        new_blog.save_blog()
        return redirect(url_for('main.index'))

    return render_template('blog.html',blog_form=form)


@main.route('/delete/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete_blog(id):
    blog = Blog.get_blog(id)
    db.session.delete(blog)
    db.session.commit()

    return render_template('index.html', id=id, blog = blog)

@main.route('/comment',methods= ['GET','POST'])
@login_required
def comment():
    '''
    View root page function that returns the index page and its data
    '''
    comments=Comment.get_comments(id)

    form=CommentForm()

    if form.validate_on_submit():

        comment=form.comment.data
        new_comment=Comment(comment=comment,user=current_user)
        new_comment.save_comment()
        return redirect(url_for('main.comment'))

    return render_template('comment.html',comment_form=form,comments=comments)

@main.route('/subscribe',methods = ["GET","POST"])
def subscribe():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()

        mail_message("You have successfully subcribed","email/subscriber.txt",user.email,user=user)

        return redirect(url_for('main.index'))
        title = "Subcription"
    return render_template('register.html',registration_form = form)