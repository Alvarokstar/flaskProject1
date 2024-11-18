from flask import Flask, request, session, render_template, flash

app = Flask(__name__)

app.secret_key = "hola"

USERNAME= 'username'
PASSWORD= 'password'
users = {}
series = {}

@app.route('/')
def home():
    if 'logged in' in session:
        return render_template('home.html')
    else:
        return render_template('register.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if users.get(username):
            error = 'This username is in use. Try with another username.'
            return render_template('register.html', error=error)

        users[username] = password
        flash('The username was registered successfully. Please, login.')
        return render_template('login.html')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return render_template('home.html')
        else:
            error= 'Invalid username or password'
            return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
