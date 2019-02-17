from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from ..request import get_quotes
from .forms import PostForm,UpdateProfile,CommentForm,SubscribeForm,PostUpdateForm
from ..import db,photos
from ..models import Quote,User,Post,Subscribe,Comment
from flask_login import login_required,current_user
import datetime
from ..email import mail_message




@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    # Getting popular movie
    quotes = get_quotes()
 
    title = 'Home - Welcome to The best Movie Review Website Online'
    print (quotes)
    
    return render_template('index.html',quotes = quotes)

@main.route('/blogs')
def blog():

    posts= None
    posts = Post.query.order_by(Post.date.desc())
    #author = User.query.filter_by(author_name = uname).first()
    return render_template('blog.html', posts = posts  )

@main.route('/blog/<int:post_id>')
def read_post(post_id):
    
    post = Post.query.filter_by(id = post_id).first()
    comments = Comment.get_comments(id)
    
    return render_template("blog_page.html",post=post,comments= comments)
        
@main.route('/new/blog/<uname>', methods = ['GET','POST'])
@login_required
def new_blog(uname):
    form = PostForm()
    title = 'Express yourself'
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)
      
    if form.validate_on_submit():
        title = form.title.data
        body = form.post.data
        dateNow = datetime.datetime.now()
        date = str(dateNow)
        #author = User.query.filter_by(author_name = uname).first()


        add_post = Post(title = title,body=body,date=date,user = current_user)
        add_post.save_post()
        posts = Post.query.all()
        return redirect(url_for('main.blog'))
    return render_template('new_blog.html', form = form, title =title)
@main.route("/delete/<post_id>",methods = ['GET','POST'])
@login_required
def delete(post_id):
    post = Post.query.filter_by(id = post_id).first()
    #user = User.query.filter_by(username = uname).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.blog'))

@main.route("/update/<post_id>", methods= ['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.filter_by(id = post_id).first()
    form = PostUpdateForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('main.blog'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body


    return render_template('new_blog.html', title='Update Post', form=form)



@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    posts = Post.query.filter_by(author_id = user.id)
    title = user.username

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,posts=posts)

        