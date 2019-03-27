from connect import session
from tables import Post
from connect import engine

conn = engine.connect()

def search_user():
    #查询所有
    rows = session.query(Post).all()
    print(rows)

    #查询第一条
    # rows = session.query(Post).first()
    # print(rows)

    #查询name='budong'的数据
    # rows = session.query(User).filter(User.username=='budong').all()
    # print(rows)

if __name__ == '__main__':
    search_user()
