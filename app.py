import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options
import tornado.httpserver
from data.tables import Post,Comment,User,Tag
from data.connect import session,engine
import markdown
from util import photo
# import util.ui_modules as md
import json
from tornado.web import authenticated
import time

# from handlers import main
define('port',default='8888',help='listening port',type=int)
class sethandler(tornado.web.RequestHandler):
    def get(self):
        self.set_cookie('fjdska1','this_is_cookie',expires_days=30)
        self.set_cookie('cookie_test', 'this_is_test')
        self.set_secure_cookie('test555','test555')
        self.set_cookie('test3','test333',path='/set',expires_days=30,httponly=True)
        self.write('setcookie')

class gethandler(tornado.web.RequestHandler):
    def get(self):
        a = self.get_cookie('fjdska1')
        b = self.get_cookie('test3')
        print(a,b)
        self.write('getgetget')

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        current_user = self.get_secure_cookie('ID')
        if current_user:
            return current_user
        return None

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write('hi iam index')
        post_list = session.query(Post).all()
        print(post_list[0].body,type(post_list),)
        post_article = session.query(Post).all()[:5]
        post_archives = session.query(Post).filter().order_by(Post.created_time).all()
        l = []
        for i in post_archives:
            l.append((i.created_time.year, i.created_time.month))
        post_archives = list(set(l))

        self.render('index.html', post_list=post_list,post_archives=post_archives,post_article=post_article)
        # self.write('i am index')
# class ArchivesHandler(tornado.web.RequestHandler):
#     def get(self, year, month):
#         post_list = session.query(Post).filter(created_time__year=year,
#                                         created_time__month=month
#                                         ).all()
#         self.render('index.html', context={'post_list': post_list})


class DetailHandler(BaseHandler):
    # def get(self, *args, **kwargs):
    #     self.render('detail.html')
    @authenticated
    def get(self,id):
        post = session.query(Post).filter(Post.id==id).first()
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        post_article = session.query(Post).all()[:5]
        post_archives = session.query(Post).filter().order_by(Post.created_time).all()
        l = []
        for i in post_archives:
            l.append((i.created_time.year, i.created_time.month))
        post_archives = list(set(l))
        comment_list = session.query(Comment).filter(Comment.post_id==1).all()
        length_comment = len(comment_list)
        # print(count)
        self.render('detail.html',post=post,post_article=post_article,post_archives=post_archives,comment_list=comment_list,
                    length_comment=length_comment)

    def post(self,id):
        # self.write('110')
        # print(self.request.full_url())
        file_imgs = self.request.files.get('newimg',None)
        if file_imgs:
            for file_img in file_imgs:
                # print(file_img.keys())
                save_to = 'static/uploads/{}'.format(file_img['filename'])
                print(save_to)
                with open(save_to,'wb') as f:
                    f.write(file_img['body'])
        # ret = {'status':True,'path':save_to}
        # self.write(json.dumps(ret))
        post = session.query(Post).filter(Post.id==id).first()
        name = self.get_argument('name')
        print(name)
        comment = self.get_argument('comment')
        print(comment)
        shangchuan = Comment(name=name, text=comment, post_id=id)
        session.add(shangchuan)
        session.commit()
        url = '/detail/%s' %(id)
        # print(url)
        self.redirect(url)

class baseHandler(tornado.web.RequestHandler):
    def get(self,num=5):
        post_article = session.query(Post).all()[:num]
        post_archives = session.query(Post).filter().order_by(Post.created_time).all()
        l = []
        for i in post_archives:
            l.append((i.created_time.year,i.created_time.month))
        post_archives = list(set(l))
        self.render('base.html',post_article=post_article,post_archives=post_archives)

class postHandler(tornado.web.RequestHandler):
    def get(self):
        post_article = session.query(Post).all()[:5]
        post_archives = session.query(Post).filter().order_by(Post.created_time).all()
        l = []
        for i in post_archives:
            l.append((i.created_time.year, i.created_time.month))
        post_archives = list(set(l))
        self.render('edit.html',post_article=post_article,post_archives=post_archives)
    def post(self):
        title=self.get_argument('title')
        print(title)
        blog_md=self.get_argument('blog')
        print(blog_md)
        shangchuan = Post(title=title,body=blog_md)
        session.add(shangchuan)
        session.commit()
        self.render('index.html')

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('01.html')
    def post(self, *args, **kwargs):
        user = self.get_argument('name','')
        username = session.query(User).filter_by(username=user).all()
        print('11111110',username[0])
        passwd = self.get_argument('password', '')
        if username and passwd == username[0].password:
            self.set_secure_cookie('ID',username[0].username,max_age=100)
            self.redirect('/index')
        else:
            self.render('01.html')

class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('03.html')
    def post(self, *args, **kwargs):
        user = self.get_argument('name','')
        username = session.query(User).filter_by(username=user).all()
        passwd = self.get_argument('password', '')
        if username:
            self.write('已经存在该用户')
            time.sleep(1)
            #这里需要跳回去
            self.redirect('/register')
        else:
            shangchuan = User(username=user,password=passwd)
            session.add(shangchuan)
            session.commit()
            self.set_secure_cookie('ID', username.username, max_age=100)
            self.write('fff')
            self.redirect('index.html')

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/index',IndexHandler),
            (r'/detail/(?P<id>[0-9]+)',DetailHandler),
            (r'/edit', postHandler),
            (r'/base',baseHandler),
            (r'/login',LoginHandler),
            (r'/set',sethandler),
            (r'/get',gethandler),
            (r'/register', RegisterHandler),
            # (r'archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',ArchivesHandler),
        ],
        template_path='templates',
        static_path='static',
        autoescape=None,
        debug=True,
        login_url = '/login',
        cookie_secret='1231465'
        # ui_methods=mt,
        # ui_modules=md,
    )
    httpserver = tornado.httpserver.HTTPServer(app)
    httpserver.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

