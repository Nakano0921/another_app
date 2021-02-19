import cryptography
from flask import Flask, render_template, request, flash
import MySQLdb
import requests
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# conn = MySQLdb.connect(host='127.0.0.1', user='root', password='0921Nknkn',  db='another_user')
# cursor = conn.cursor()
engine = sqlalchemy.create_engine('mysql+pymysql://be692cbcc38f76:825b465f@s-cdbr-east-03.cleardb.com/heroku_bbea5c2b08bb200')
# engine = sqlalchemy.create_engine('mysql+pymysql://root:0921Nknkn@127.0.0.1/another_user')
Base = sqlalchemy.ext.declarative.declarative_base()

class AnotherUser(Base):
    __tablename__ = 'another_users'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_name = sqlalchemy.Column(
        sqlalchemy.Text(20), nullable=False)
    password = sqlalchemy.Column(
        sqlalchemy.Text(20), nullable=False)

Base.metadata.create_all(engine)

Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

@app.route('/', methods=['GET', 'POST'])
def top_page():
    if request.method == 'GET':
        return render_template('top.html')
    elif request.method == 'POST':
        if request.form['username'] == "":
            flash("ユーザー名を入力してください。")
            return render_template('create_page.html')
        elif request.form['password'] == "":
            flash("パスワードを入力してください。")
            return render_template('create_page.html')
        else:
            username = request.form['username']
            password = request.form['password']
            # cursor.execute(
            #             'INSERT INTO users (user_name, password) values (%s, %s)',
            #             (username, password))
            # conn.commit()
            reg_user = AnotherUser(user_name=username, password=password)
            session.add(reg_user)
            session.commit()
            session.close()
            return render_template('top.html')
    


@app.route('/create_page', methods=['POST'])
def create_page():
    return render_template('create_page.html')


@app.route('/my_page', methods=['GET', 'POST'])
def login_my_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # rows = cursor.execute(
        #               'SELECT * FROM users WHERE user_name = %s',
        #               (username,))
        # rows = cursor.fetchone()
        # user = rows
        # db_password = cursor.execute(
        #               'SELECT * FROM users WHERE password = %s',
        #               (password,))
        # rows = cursor.fetchone()
        # db_password = rows
        user = session.query(AnotherUser).filter(AnotherUser.user_name == username).first()
        print(user)
        db_password = session.query(AnotherUser).filter(AnotherUser.password == password).first()
        print(db_password)
        if user != None and db_password != None:
            return render_template('my_page.html', username=username)
        else:
            print('ユーザ名かパスワードが違います。')


@app.route('/insta_api', methods=['POST'])
def insta_api():
    if request.method == 'POST':
        if request.form['hashtag_word'] == "":
            flash('ワードを入力してください。')
            return render_template('my_page.html')
        else:
            hashtag_word = request.form['hashtag_word']
            hashtag_id = requests.get(f'https://graph.facebook.com/ig_hashtag_search?user_id=17841444881116627&q={hashtag_word}&access_token=EAATE5NJ3cpABAHA4cZBUeYcqI6ZAZB8goujfOApsIM5fpeUzgs3gkYaE234HgAQGhC9jJ9AtiltR0ZBNWvzIrZApZCJnm7dzbZA9rHPRDfDdKG0dH7q44B9fitaTFqU6JUeJLWx44Q0vjfz0f3608tJQNz6P07qn5JUWwwf7R8vmqB146XY6ebqAGFV9ZAhH0s4ZD')
            hashtag_id = hashtag_id.json()
            hashtag_id = hashtag_id['data']
            hashtag_id = [d.get('id') for d in hashtag_id]
            hashtag_id = hashtag_id[0]
            results = requests.get(f'https://graph.facebook.com/{hashtag_id}/top_media?user_id=17841444881116627&fields=id,media_type,media_url,permalink&access_token=EAATE5NJ3cpABAHA4cZBUeYcqI6ZAZB8goujfOApsIM5fpeUzgs3gkYaE234HgAQGhC9jJ9AtiltR0ZBNWvzIrZApZCJnm7dzbZA9rHPRDfDdKG0dH7q44B9fitaTFqU6JUeJLWx44Q0vjfz0f3608tJQNz6P07qn5JUWwwf7R8vmqB146XY6ebqAGFV9ZAhH0s4ZD')
            results = results.json()
            results = results['data']
            results = [d.get('media_url') for d in results]
            results = [d for d in results if d != None]
            return render_template('my_page.html', results=results)


@app.route('/api_with_ac', methods=['POST'])
def api_with_ac():
    if request.method == 'POST':
        if request.form['hashtag_word'] == "":
            flash('ワードを入力してください。')
            return render_template('my_page.html')
        else:
            hashtag_word = request.form['hashtag_word']
            hashtag_id = requests.get(f'https://graph.facebook.com/ig_hashtag_search?user_id=17841444881116627&q={hashtag_word}&access_token=EAATE5NJ3cpABAHA4cZBUeYcqI6ZAZB8goujfOApsIM5fpeUzgs3gkYaE234HgAQGhC9jJ9AtiltR0ZBNWvzIrZApZCJnm7dzbZA9rHPRDfDdKG0dH7q44B9fitaTFqU6JUeJLWx44Q0vjfz0f3608tJQNz6P07qn5JUWwwf7R8vmqB146XY6ebqAGFV9ZAhH0s4ZD')
            hashtag_id = hashtag_id.json()
            hashtag_id = hashtag_id['data']
            hashtag_id = [d.get('id') for d in hashtag_id]
            hashtag_id = hashtag_id[0]
            post_results = requests.get(f'https://graph.facebook.com/{hashtag_id}/top_media?user_id=17841444881116627&fields=id,media_type,media_url,permalink&access_token=EAATE5NJ3cpABAHA4cZBUeYcqI6ZAZB8goujfOApsIM5fpeUzgs3gkYaE234HgAQGhC9jJ9AtiltR0ZBNWvzIrZApZCJnm7dzbZA9rHPRDfDdKG0dH7q44B9fitaTFqU6JUeJLWx44Q0vjfz0f3608tJQNz6P07qn5JUWwwf7R8vmqB146XY6ebqAGFV9ZAhH0s4ZD')
            post_results = post_results.json()
            post_results = post_results['data']
            post_results = [d.get('permalink') for d in post_results]
            post_results = [d for d in post_results if d != None]
            return render_template('my_page.html', post_results=post_results)


if __name__ == "__main__":
    app.run()