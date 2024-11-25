from flask import Flask, request, session, render_template, flash, redirect, url_for

app = Flask(__name__)

app.secret_key = "hola"

users = [{
    "username": "Alvaro",
    "password": "123",
    "films": []

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
    if request.method == 'POST':
        name = request.form['name']
        synopsis = request.form['synopsis']
        rating = request.form['rating']
        date = request.form['date']
        genre = request.form['genre']
        category = request.form['category']

        if 'username' in session:
            username = session['username']
            for user in users:
                if user['username'] == username:
                    new_film = {
                        'name': name,
                        'synopsis': synopsis,
                        'rating': rating,
                        'date': date,
                        'genre': genre,
                        'category': category
                    }
        return redirect(url_for('home.html'))
    return render_template('add_films.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']

        if username in users:
            error = 'This username is in use. Try with another username.'
            return render_template('register.html', error=error)
        password = request.form['password']

        new_user = {'username': username,
                    'password': password,
                    'films': []
                    }

        users.append(new_user)

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        for user in users:
            if user['username'] == username and user['password'] == password:
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('home'))

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
