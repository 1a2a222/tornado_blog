from tables import User,Post,session

if __name__ == '__main__':
    rows = session.query(User).get(1)
    print(rows)
    print(dir(rows))
