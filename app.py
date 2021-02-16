from flask import Flask, render_template, request
import MySQLdb
import requests

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
    if request.method == 'GET':
        return render_template('my_page.html')
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


@app.route('/insta_api', methods=['POST'])
def insta_api():
    r = requests.get('https://graph.facebook.com/17841593698074073/top_media?user_id=17841444881116627&fields=id,media_type,media_url,permalink&access_token=EAATE5NJ3cpABAHA4cZBUeYcqI6ZAZB8goujfOApsIM5fpeUzgs3gkYaE234HgAQGhC9jJ9AtiltR0ZBNWvzIrZApZCJnm7dzbZA9rHPRDfDdKG0dH7q44B9fitaTFqU6JUeJLWx44Q0vjfz0f3608tJQNz6P07qn5JUWwwf7R8vmqB146XY6ebqAGFV9ZAhH0s4ZD')
    print(r.json())
    return render_template('my_page.html')


if __name__ == "__main__":
    app.run(debug=True)