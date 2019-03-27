from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey, Table
from .connect import Base, session


#为双向多对多进行的定义

print(1)
class Category(Base):
    __tablename__='category'
    # name = models.CharField(max_length=100)
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    def __str__(self):
        return '<User(id=%s,name=%s)>'%(
            self.id,
            self.name
        )
print(2)
class User(Base):
    __tablename__='user'
    id = Column(Integer,primary_key=True,autoincrement=True)
    # id_card = Column(Integer,nullable=True,unique=True)
    username = Column(String(30))
    password = Column(String(30))
    # lost_login = Column(DateTime)
    # login_num = Column(Integer,default=0)
    def __str__(self):
        return '<User(id=%s,usename=%s,password=%s)>'%(
            self.id,
            self.username,
            self.password,
        )
    @classmethod
    def by_name(cls,name):
        return session.query(cls).filter_by(username=name).all()


print(3)

association_table = Table('association_table', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id')),
    Column('post_id', Integer, ForeignKey('post.id'))
)

class Tag(Base):
    __tablename__='tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    def __str__(self):
        return self.id,self.name
print(4)

class Post(Base):
    """
    文章的数据库表稍微复杂一点，主要是涉及的字段更多。
    """
    # 文章标题
    __tablename__='post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(70))
    body = Column(String(300))
    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = Column(DateTime, default=datetime.now)
    modified_time = Column(DateTime, default=datetime.now)
    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = Column(String(300),default='无')
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)
    author = relationship("User", backref="arctires",uselist=True,cascade='all')
    category_id = Column(Integer,ForeignKey('category.id'), unique=True)
    category = relationship("Category", backref="category",uselist=True,cascade='all')
    tags = relationship("Tag", backref="posts", secondary=association_table)
    def __repr__(self):
        # return self.id,self.title,self.body,self.created_time,self.modified_time,self.author
        return '(id=%s,title=%s,bogy=%s,created_time=%s,modified_time=%s,author=%s)'\
               %(self.id, self.title, self.body, self.created_time, self.modified_time, self.author)

    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
class Comment(Base):
    __tablename__='comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    text = Column(String(150))
    created_time = Column(DateTime, default=datetime.now)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship("Post", backref="post", uselist=True, cascade='all')
    def __repr__(self):
        # return self.id,self.title,self.body,self.created_time,self.modified_time,self.author
        return '(id=%s,name=%s,text=%s)'\
               %(self.id, self.name,self.text)

if __name__=='__main__':
    Base.metadata.create_all()

