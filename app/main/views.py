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
        