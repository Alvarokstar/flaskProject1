from flask import Flask, request, session, render_template, flash, redirect, url_for

app = Flask(__name__)

app.secret_key = "hola"

users = [{
    "username: Alvaro",
    "password: 123",
    "films: ",

}

]

@app.route('/')
def home():
    if 'logged_in' in session:
        return render_template('home.html')
    return redirect(url_for('register'))

@app.route('/films')
def films():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user_films = users[username].get('films', [])
    categories = {
        "wish_list": "Films that I want to watch",
        "watching": "Films that I'm watching",
        "watched": "Watched"
    }
    categorized_films = {key: [] for key in categories.keys()}
    for film in user_films:
        categorized_films[film['category']].append(film)
    return render_template('films.html', categories=categories, films=categorized_films)

@app.route('/add_films', methods=['GET', 'POST'])
def add_films():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_film = {
            "name": request.form['name'],
            "synopsis": request.form['synopsis'],
            "score": int(request.form['score']),
            "genre": request.form['genre'],
            "release_date": request.form['release_date'],
            "category": request.form['category'],
        }
        username = session['username']
        users[username]['films'].append(new_film)
        return redirect(url_for('films'))
    return render_template('add_films.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            error = 'This username is in use. Try with another username.'
            return render_template('register.html', error=error)
        users[username] = {'password': password, 'films': []}
        flash('The username was registered successfully. Please, login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username]['password'] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
