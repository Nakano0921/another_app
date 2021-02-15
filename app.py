from flask import Flask, render_template, request
import MySQLdb

app = Flask(__name__)
conn = MySQLdb.connect(host='127.0.0.1', user='root', password='0921Nknkn',  db='another_user')
cursor = conn.cursor()

@app.route('/', methods=['GET', 'POST'])
def top_page():
    if request.method == 'GET':
        return render_template('top.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute(
                       'INSERT INTO users (user_name, password) values (%s, %s)',
                      (username, password))
        conn.commit()
        return render_template('top.html')


@app.route('/create_page', methods=['POST'])
def create_page():
    return render_template('create_page.html')


@app.route('/my_page', methods=['GET', 'POST'])
def login_my_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        rows = cursor.execute(
                      'SELECT * FROM users WHERE user_name = %s',
                      (username,))
        rows = cursor.fetchone()
        user = rows
        db_password = cursor.execute(
                      'SELECT * FROM users WHERE password = %s',
                      (password,))
        rows = cursor.fetchone()
        db_password = rows
        if user != None and db_password != None:
            return render_template('my_page.html', username=username)
        else:
            print('ユーザ名かパスワードが違います。')


if __name__ == "__main__":
    app.run(debug=True)